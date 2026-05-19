"""
PusoyOS Process Management Module
Handles process creation, state management, and process lifecycle
"""

from enum import Enum
from datetime import datetime
from config import MAX_PRIORITY, DEFAULT_PRIORITY, PAGE_FAULT_PROBABILITY, SYSTEM_CALL_PROBABILITY
import random


class ProcessState(Enum):
    """Process states in PusoyOS"""
    NEW = "NEW"
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    TERMINATED = "TERMINATED"


class Process:
    """Represents a single process in PusoyOS"""
    _pid_counter = 1000
    
    def __init__(self, name, burst_time, memory_required, io_operations=0, priority=DEFAULT_PRIORITY):
        self.pid = Process._pid_counter
        Process._pid_counter += 1
        
        self.name = name
        self.state = ProcessState.NEW
        self.arrival_time = 0
        self.created_at = datetime.now()
        self.start_time = None
        self.end_time = None
        self.remaining_burst_time = burst_time
        self.total_burst_time = burst_time
        self.memory_required = memory_required
        self.memory_allocated = 0
        self.io_operations = io_operations
        self.priority = min(priority, MAX_PRIORITY)
        
        # Tracking
        self.context_switches = 0
        self.page_faults = 0
        self.system_calls = 0
        self.cpu_time = 0
        self.wait_time = 0
        self.turnaround_time = 0
        
        # Virtual memory
        self.virtual_page_table = []
        self.page_faults_list = []
        
    def execute(self, time_slice=5):
        """Execute process for given time slice"""
        if self.state != ProcessState.RUNNING:
            return 0
        
        executed = min(time_slice, self.remaining_burst_time)
        self.remaining_burst_time -= executed
        self.cpu_time += executed
        
        # Simulate page fault
        if random.random() < PAGE_FAULT_PROBABILITY:
            self.page_faults += 1
            self.page_faults_list.append({
                'time': self.cpu_time,
                'page': random.randint(0, 10)
            })
        
        # Simulate system call
        if random.random() < SYSTEM_CALL_PROBABILITY:
            self.system_calls += 1
        
        return executed
    
    def move_to_waiting(self):
        """Move process to waiting state"""
        self.state = ProcessState.WAITING
    
    def move_to_ready(self):
        """Move process to ready state"""
        self.state = ProcessState.READY
    
    def move_to_running(self):
        """Move process to running state"""
        self.state = ProcessState.RUNNING
        if self.start_time is None:
            self.start_time = datetime.now()
    
    def terminate(self):
        """Terminate the process"""
        self.state = ProcessState.TERMINATED
        self.end_time = datetime.now()
        if self.start_time:
            self.turnaround_time = (self.end_time - self.start_time).total_seconds()
    
    def is_complete(self):
        """Check if process has completed"""
        return self.remaining_burst_time <= 0
    
    def to_dict(self):
        """Convert process to dictionary"""
        return {
            'pid': self.pid,
            'name': self.name,
            'state': self.state.value,
            'app_id': getattr(self, 'app_id', None),
            'instance_id': getattr(self, 'instance_id', None),
            'created_at': self.created_at.isoformat(),
            'started_at': self.start_time.isoformat() if self.start_time else None,
            'priority': self.priority,
            'memory_required': self.memory_required,
            'memory_allocated': self.memory_allocated,
            'cpu_time': self.cpu_time,
            'remaining_burst_time': self.remaining_burst_time,
            'total_burst_time': self.total_burst_time,
            'context_switches': self.context_switches,
            'page_faults': self.page_faults,
            'system_calls': self.system_calls,
            'wait_time': self.wait_time,
            'turnaround_time': self.turnaround_time,
            'io_operations': self.io_operations
        }


class ProcessManager:
    """Manages process creation, termination, and querying"""
    
    def __init__(self):
        self.processes = {}  # {pid: Process}
        self.ready_queue = []
        self.waiting_queue = []
        self.terminated_processes = []
    
    def create_process(self, name, burst_time, memory_required, io_operations=0, priority=DEFAULT_PRIORITY):
        """Create a new process"""
        process = Process(name, burst_time, memory_required, io_operations, priority)
        process.state = ProcessState.READY
        self.processes[process.pid] = process
        self.ready_queue.append(process)
        return process
    
    def get_process(self, pid):
        """Get process by PID"""
        return self.processes.get(pid)
    
    def get_all_processes(self):
        """Get all processes"""
        return list(self.processes.values())
    
    def get_running_processes(self):
        """Get all running processes"""
        return [p for p in self.processes.values() if p.state == ProcessState.RUNNING]
    
    def get_ready_processes(self):
        """Get all ready processes"""
        return [p for p in self.processes.values() if p.state == ProcessState.READY]
    
    def get_waiting_processes(self):
        """Get all waiting processes"""
        return [p for p in self.processes.values() if p.state == ProcessState.WAITING]
    
    def terminate_process(self, pid):
        """Terminate a process"""
        if pid in self.processes:
            process = self.processes[pid]
            process.terminate()
            self.terminated_processes.append(process)
            return True
        return False
    
    def remove_process(self, pid):
        """Remove process from tracking"""
        if pid in self.processes:
            process = self.processes[pid]
            if process in self.ready_queue:
                self.ready_queue.remove(process)
            if process in self.waiting_queue:
                self.waiting_queue.remove(process)
            del self.processes[pid]
            return True
        return False
    
    def kill_process(self, pid, signal='SIGTERM'):
        """Kill a process with signal"""
        if pid in self.processes:
            process = self.processes[pid]
            if signal == 'SIGKILL':
                self.terminate_process(pid)
                return {'success': True, 'message': f'Process {pid} killed'}
            elif signal == 'SIGTERM':
                if process.state != ProcessState.TERMINATED:
                    self.terminate_process(pid)
                    return {'success': True, 'message': f'Process {pid} terminated'}
        return {'success': False, 'message': f'Process {pid} not found'}
    
    def get_process_info(self, pid):
        """Get detailed process information"""
        if pid in self.processes:
            return self.processes[pid].to_dict()
        return None
    
    def get_statistics(self):
        """Get process statistics"""
        all_procs = self.get_all_processes()
        running = self.get_running_processes()
        
        avg_wait_time = sum(p.wait_time for p in all_procs) / len(all_procs) if all_procs else 0
        avg_turnaround = sum(p.turnaround_time for p in all_procs) / len(all_procs) if all_procs else 0
        total_context_switches = sum(p.context_switches for p in all_procs)
        total_page_faults = sum(p.page_faults for p in all_procs)
        
        return {
            'total_processes': len(all_procs),
            'running_processes': len(running),
            'ready_processes': len(self.get_ready_processes()),
            'waiting_processes': len(self.get_waiting_processes()),
            'terminated_processes': len(self.terminated_processes),
            'average_wait_time': avg_wait_time,
            'average_turnaround_time': avg_turnaround,
            'total_context_switches': total_context_switches,
            'total_page_faults': total_page_faults
        }
