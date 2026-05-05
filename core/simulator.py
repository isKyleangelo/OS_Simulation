"""
PusoyOS Simulator
Main OS simulator class that coordinates all subsystems
"""

from datetime import datetime
from config import (
    SYSTEM_NAME, SYSTEM_VERSION, KERNEL_VERSION, HOSTNAME,
    TOTAL_MEMORY, AUTO_LAUNCH_APPS
)
from core import (
    ProcessManager, CPUScheduler, MemoryManager,
    FileSystem, IOSystem, ApplicationManager
)


class PusoyOSSimulator:
    """Main OS Simulator - coordinates all subsystems"""
    
    def __init__(self):
        # System info
        self.system_name = SYSTEM_NAME
        self.system_version = SYSTEM_VERSION
        self.kernel_version = KERNEL_VERSION
        self.hostname = HOSTNAME
        self.start_time = datetime.now()
        self.system_clock = 0  # Clock ticks
        
        # Subsystems
        self.process_manager = ProcessManager()
        self.scheduler = CPUScheduler('round_robin')
        self.memory_manager = MemoryManager('first_fit')
        self.filesystem = FileSystem()
        self.io_system = IOSystem()
        self.application_manager = ApplicationManager()
        
        # Simulation tracking
        self.simulation_log = []
        self.system_calls_count = 0
        self.interrupts_count = 0
        self.is_running = False
        
        # Initialize system
        self._initialize_system()
    
    def _initialize_system(self):
        """Initialize system with default files"""
        # Create default system files
        self.filesystem.create_file(
            'system.log',
            owner='root',
            permissions='644',
            content=f'{self.system_name} {self.system_version} - System Log\n'
        )
        self.filesystem.create_file(
            'boot.log',
            owner='root',
            permissions='644',
            content=f'Booting {self.system_name}...\nKernel: {self.kernel_version}\n'
        )
    
    def create_process(self, name, burst_time, memory_required, io_operations=0, priority=1):
        """Create a new process"""
        # Create process
        process = self.process_manager.create_process(
            name, burst_time, memory_required, io_operations, priority
        )

        # Allocate memory against the real PID so process cleanup releases it.
        if not self.memory_manager.allocate_memory(process.pid, memory_required):
            self.process_manager.remove_process(process.pid)
            return None

        process.memory_allocated = memory_required
        
        # Add to scheduler
        self.scheduler.add_process_to_queue(process)
        
        # Log event
        self.simulation_log.append({
            'timestamp': self.system_clock,
            'event': 'process_created',
            'pid': process.pid,
            'name': name,
            'memory': memory_required
        })
        
        return process
    
    def launch_application(self, app_id):
        """Launch an application"""
        result = self.application_manager.launch_application(app_id)
        
        if not result['success']:
            return result
        
        app_info = self.application_manager.get_application_info(app_id)
        
        # Create process for app
        process = self.create_process(
            app_info['name'],
            burst_time=30,
            memory_required=app_info['memory_required'],
            io_operations=2,
            priority=1
        )
        
        if process:
            app = self.application_manager.get_application(app_id)
            app.pid = process.pid
            process.app_id = app_id
            process.process_type = 'application'
            return result
        else:
            self.application_manager.close_application(app_id)
            return {'success': False, 'message': 'Insufficient resources'}
    
    def close_application(self, app_id):
        """Close an application"""
        app = self.application_manager.get_application(app_id)
        if app and app.pid:
            self.process_manager.kill_process(app.pid, 'SIGTERM')
            self.memory_manager.deallocate_memory(app.pid)
        
        return self.application_manager.close_application(app_id)
    
    def step_simulation(self):
        """Execute one simulation cycle"""
        if not self.is_running:
            return
        
        self.system_clock += 1
        
        # Schedule next process
        next_process = self.scheduler.get_next_process()
        if next_process:
            self.scheduler.schedule_process(next_process)
            self.scheduler.execute_cycle(next_process, 1)
        
        # Process I/O
        self.io_system.process_io()
        
        # Update process metrics
        running_processes = self.process_manager.get_running_processes()
        for process in running_processes:
            if process.is_complete():
                self.memory_manager.deallocate_memory(process.pid)
                self.scheduler.remove_process_from_queue(process)
    
    def run_simulation(self, cycles=100):
        """Run simulation for N cycles"""
        self.is_running = True
        for _ in range(cycles):
            self.step_simulation()
        self.is_running = False
    
    def reset_simulation(self):
        """Reset simulation"""
        self.system_clock = 0
        self.process_manager = ProcessManager()
        self.scheduler = CPUScheduler('round_robin')
        self.memory_manager = MemoryManager('first_fit')
        self.io_system = IOSystem()
        self.application_manager = ApplicationManager()
        self.simulation_log = []
        self._initialize_system()
    
    def get_status(self):
        """Get current system status"""
        processes = self.process_manager.get_all_processes()
        scheduler_stats = self.scheduler.get_statistics()
        memory_status = self.memory_manager.get_memory_status()
        io_status = self.io_system.get_io_status()
        
        return {
            'system_clock': self.system_clock,
            'processes': [p.to_dict() for p in processes],
            'scheduler': scheduler_stats,
            'memory': memory_status,
            'io': io_status,
            'uptime': (datetime.now() - self.start_time).total_seconds()
        }
    
    def get_system_info(self):
        """Get comprehensive system information"""
        memory_status = self.memory_manager.get_memory_status()
        process_stats = self.process_manager.get_statistics()
        
        # Calculate actual CPU usage from running applications
        running_apps = self.application_manager.get_running_applications()
        actual_cpu_usage = sum(app['cpu_usage_percent'] for app in running_apps)
        actual_cpu_usage = min(actual_cpu_usage, 100.0)  # Cap at 100%
        
        # Calculate actual memory from running apps
        actual_memory_used = sum(app['memory_required'] for app in running_apps)
        actual_memory_percent = (actual_memory_used / memory_status['total']) * 100 if memory_status['total'] > 0 else 0
        
        return {
            'system': {
                'hostname': self.hostname,
                'os_name': self.system_name,
                'os_version': self.system_version,
                'kernel': self.kernel_version,
                'uptime': int((datetime.now() - self.start_time).total_seconds()),
                'system_clock': self.system_clock,
                'cpu_cores': 4,
                'cpu_freq': 2400,
                'cpu_utilization': actual_cpu_usage,
                'total_memory': memory_status['total'],
                'used_memory': actual_memory_used,
                'free_memory': memory_status['total'] - actual_memory_used,
                'memory_percent': actual_memory_percent,
                'running_processes': process_stats['running_processes'],
                'total_processes': process_stats['total_processes'],
                'context_switches': process_stats['total_context_switches'],
                'page_faults': process_stats['total_page_faults']
            }
        }
    
    def get_scheduler_info(self):
        """Get scheduler information"""
        return self.scheduler.get_statistics()
    
    def set_scheduling_algorithm(self, algorithm):
        """Change CPU scheduling algorithm"""
        self.scheduler.set_algorithm(algorithm)
        return {'success': True, 'algorithm': algorithm}
    
    def set_memory_allocation_algorithm(self, algorithm):
        """Change memory allocation algorithm"""
        success = self.memory_manager.set_allocation_algorithm(algorithm)
        return {'success': success, 'algorithm': algorithm}
    
    def set_disk_scheduling_algorithm(self, algorithm):
        """Change disk scheduling algorithm"""
        success = self.io_system.set_disk_scheduling_algorithm(algorithm)
        return {'success': success, 'algorithm': algorithm}
    
    def perform_memory_compaction(self):
        """Perform memory compaction"""
        allocated, free = self.memory_manager.memory_compaction()
        return {'success': True, 'allocated_partitions': allocated, 'free_partitions': free}
    
    def get_memory_info(self):
        """Get memory information"""
        return self.memory_manager.get_memory_status()
    
    def get_filesystem_info(self):
        """Get file system information"""
        return self.filesystem.get_filesystem_info()
    
    def get_io_info(self):
        """Get I/O system information"""
        return self.io_system.get_io_status()
    
    def get_running_applications(self):
        """Get running applications"""
        return self.application_manager.get_running_applications()
    
    def get_available_applications(self):
        """Get available applications"""
        return self.application_manager.get_available_applications()
    
    def create_file(self, filename, content=''):
        """Create a file"""
        file = self.filesystem.create_file(filename, owner='root', content=content)
        return {'success': file is not None, 'file': file.to_dict() if file else None}
    
    def delete_file(self, filename):
        """Delete a file"""
        success = self.filesystem.delete_file(filename)
        return {'success': success, 'filename': filename}
    
    def read_file(self, filename):
        """Read file content"""
        content = self.filesystem.read_file(filename)
        return {'success': content is not None, 'content': content}
    
    def get_files(self):
        """Get all files"""
        return {'files': self.filesystem.list_files()}
    
    def get_log(self, limit=100):
        """Get simulation log"""
        return self.simulation_log[-limit:]
