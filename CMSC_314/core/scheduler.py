"""
PusoyOS CPU Scheduler Module
Implements Round Robin, FCFS, Priority, MLFQ, and Aging scheduling algorithms
"""

from config import TIME_QUANTUM, CONTEXT_SWITCH_OVERHEAD
from core.process import ProcessState


class CPUScheduler:
    """CPU scheduler with multiple scheduling algorithms"""
    
    def __init__(self, algorithm='round_robin', num_cores=4):
        self.algorithm = algorithm
        self.num_cores = num_cores  # Number of CPU cores
        self.current_processes = [None] * num_cores  # Current process per core
        self.cpu_utilization = 0
        self.context_switches = 0
        self.cpu_ticks = 0
        self.idle_ticks = 0
        self.ready_queue = []
        self.time_quantum_remaining = [0] * num_cores
        self.execution_log = []
        
        # MLFQ (Multi-Level Feedback Queue)
        self.mlfq_queues = [[], [], []]  # 3 priority levels
        self.mlfq_time_quantum = [5, 10, 20]  # Different time quanta for each level
        
        # Aging mechanism
        self.process_age = {}  # {pid: age_ticks}
        self.aging_threshold = 10  # Promote after 10 ticks waiting
    
    def set_algorithm(self, algorithm):
        """Change scheduling algorithm"""
        if algorithm in ['round_robin', 'fcfs', 'priority', 'mlfq', 'aging']:
            self.algorithm = algorithm
            return True
        return False
    
    def add_process_to_queue(self, process):
        """Add process to ready queue"""
        if process not in self.ready_queue:
            process.state = ProcessState.READY
            self.ready_queue.append(process)
            self.process_age[process.pid] = 0
            
            # For MLFQ, add to highest priority queue
            if self.algorithm == 'mlfq':
                self.mlfq_queues[0].append(process)
            else:
                self._sort_ready_queue()
    
    def remove_process_from_queue(self, process):
        """Remove process from ready queue"""
        if process in self.ready_queue:
            self.ready_queue.remove(process)
        
        # Remove from MLFQ queues
        for queue in self.mlfq_queues:
            if process in queue:
                queue.remove(process)
        
        # Clean up age tracking
        if process.pid in self.process_age:
            del self.process_age[process.pid]

        for core, current in enumerate(self.current_processes):
            if current == process:
                self.current_processes[core] = None
                self.time_quantum_remaining[core] = 0
    
    def _sort_ready_queue(self):
        """Sort ready queue based on algorithm"""
        if self.algorithm == 'priority':
            # Higher priority (lower number) comes first
            self.ready_queue.sort(key=lambda p: p.priority)
        elif self.algorithm == 'aging':
            # Sort by priority, but boost age
            self.ready_queue.sort(key=lambda p: (p.priority - self.process_age.get(p.pid, 0) // 2))
        elif self.algorithm in ['fcfs', 'round_robin']:
            # Maintain order
            pass
    
    def _get_next_process_mlfq(self):
        """Get next process using MLFQ"""
        # Check if any process in queue 0
        for queue_idx, queue in enumerate(self.mlfq_queues):
            if queue:
                return queue[0], queue_idx
        return None, -1
    
    def get_next_process(self):
        """Get next process to execute"""
        if not self.ready_queue:
            return None
        
        if self.algorithm == 'mlfq':
            process, _ = self._get_next_process_mlfq()
            return process
        elif self.algorithm == 'fcfs':
            return self.ready_queue[0]
        elif self.algorithm == 'priority':
            return self.ready_queue[0]
        elif self.algorithm == 'aging':
            return self.ready_queue[0]
        elif self.algorithm == 'round_robin':
            # Rotate queue for round robin
            if self.time_quantum_remaining[0] <= 0 and self.ready_queue:
                self.ready_queue.append(self.ready_queue.pop(0))
            return self.ready_queue[0] if self.ready_queue else None
        
        return self.ready_queue[0] if self.ready_queue else None
    
    def schedule_process(self, process, core=0):
        """Schedule a process to run on a specific core"""
        if self.current_processes[core] != process:
            if self.current_processes[core]:
                self.context_switches += 1
                self.current_processes[core].context_switches += 1
                if self.current_processes[core].state == ProcessState.RUNNING:
                    self.current_processes[core].move_to_ready()
            
            process.move_to_running()
            process.context_switches += 1
            self.current_processes[core] = process
            
            # Set time quantum based on algorithm
            if self.algorithm == 'mlfq':
                _, queue_idx = self._get_next_process_mlfq()
                if queue_idx >= 0:
                    self.time_quantum_remaining[core] = self.mlfq_time_quantum[queue_idx]
            else:
                self.time_quantum_remaining[core] = TIME_QUANTUM
    
    def execute_cycle(self, process, time_slice=1, core=0):
        """Execute one scheduling cycle"""
        if not process or process.state == ProcessState.TERMINATED:
            self.idle_ticks += time_slice
            return 0
        
        # Increment age for waiting processes
        for p in self.ready_queue:
            if p != process and p.pid in self.process_age:
                self.process_age[p.pid] += time_slice
                p.wait_time += time_slice
        
        # Context switch overhead
        if process.state != ProcessState.RUNNING:
            process.state = ProcessState.RUNNING
        
        start_tick = self.cpu_ticks
        executed = process.execute(time_slice)
        self.cpu_ticks += time_slice
        if executed > 0:
            self.execution_log.append({
                'pid': process.pid,
                'name': process.name,
                'start': start_tick,
                'end': start_tick + executed,
                'duration': executed,
                'algorithm': self.algorithm
            })
        self.time_quantum_remaining[core] -= executed
        
        # MLFQ: demote if time quantum exceeded
        if self.algorithm == 'mlfq':
            _, queue_idx = self._get_next_process_mlfq()
            if queue_idx >= 0 and self.time_quantum_remaining[core] <= 0 and queue_idx < 2:
                # Move to lower priority queue
                self.mlfq_queues[queue_idx].remove(process)
                self.mlfq_queues[queue_idx + 1].append(process)
                self.time_quantum_remaining[core] = self.mlfq_time_quantum[queue_idx + 1]
        
        # Check for aging promotion
        if self.algorithm == 'aging' and process.pid in self.process_age:
            if self.process_age[process.pid] >= self.aging_threshold:
                if process.priority > 0:
                    process.priority -= 1
                self.process_age[process.pid] = 0
                self._sort_ready_queue()
        
        # Check if process is complete
        if process.is_complete():
            process.terminate()
            self.current_processes[core] = None
            self.remove_process_from_queue(process)
        
        return executed
    
    def get_statistics(self):
        """Get scheduler statistics"""
        total_ticks = self.cpu_ticks + self.idle_ticks
        utilization = (self.cpu_ticks / total_ticks * 100) if total_ticks > 0 else 0
        
        running_processes = [p for p in self.current_processes if p]
        running_names = ', '.join([p.name for p in running_processes]) if running_processes else 'None'
        
        return {
            'algorithm': self.algorithm,
            'num_cores': self.num_cores,
            'cpu_utilization': f'{utilization:.1f}%',
            'context_switches': self.context_switches,
            'cpu_ticks': self.cpu_ticks,
            'idle_ticks': self.idle_ticks,
            'ready_queue_size': len(self.ready_queue),
            'running_processes': running_names,
            'active_cores': len([p for p in self.current_processes if p is not None])
        }

    def get_gantt_chart(self):
        """Get text-friendly execution order and timing."""
        segments = self.execution_log[-50:]
        if not segments:
            return {
                'segments': [],
                'text_chart': '(No CPU execution yet)',
                'time_axis': '',
                'execution_order': []
            }

        return {
            'segments': segments,
            'text_chart': ' | '.join([f"P{s['pid']}" for s in segments]),
            'time_axis': ' '.join([str(s['start']) for s in segments] + [str(segments[-1]['end'])]),
            'execution_order': [s['name'] for s in segments]
        }
    
    def get_utilization_percent(self):
        """Get CPU utilization percentage"""
        total_ticks = self.cpu_ticks + self.idle_ticks
        if total_ticks == 0:
            return 0.0
        return (self.cpu_ticks / total_ticks) * 100
