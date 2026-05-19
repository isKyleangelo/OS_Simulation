#!/usr/bin/env python3
"""
SimpleOS - Interactive Operating System Simulator
A complete command-line based OS simulator demonstrating process management,
CPU scheduling, memory management, file handling, and I/O operations.

Author: CMSC 314
Date: 2024
"""

import os
import sys
import time
from collections import deque
from datetime import datetime
from enum import Enum
import random

# ===========================
# CONSTANTS & CONFIGURATION
# ===========================

TOTAL_MEMORY = 700
MEMORY_PARTITIONS = [100, 150, 200, 250]
TIME_QUANTUM = 5
IO_QUEUE_LIMIT = 20

class ProcessState(Enum):
    """Process states"""
    NEW = "NEW"
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    TERMINATED = "TERMINATED"


# ===========================
# UTILITY FUNCTIONS
# ===========================

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title, width=50):
    """Print a formatted header"""
    print("=" * width)
    print(f"  {title}".center(width))
    print("=" * width)


def print_separator(width=50):
    """Print a separator line"""
    print("-" * width)


def print_menu(title, options, width=50):
    """Print a formatted menu"""
    print_header(title, width)
    for idx, option in enumerate(options, 1):
        print(f"  {idx}. {option}")
    print_separator(width)


def get_valid_input(prompt, input_type=str, valid_range=None):
    """Get validated user input"""
    while True:
        try:
            user_input = input(prompt).strip()
            
            if input_type == int:
                value = int(user_input)
                if valid_range and (value < valid_range[0] or value > valid_range[1]):
                    print(f"  ✗ Please enter a number between {valid_range[0]} and {valid_range[1]}")
                    continue
                return value
            elif input_type == float:
                return float(user_input)
            else:
                return user_input
        except ValueError:
            print(f"  ✗ Invalid input. Please try again.")


# ===========================
# PROCESS CLASS
# ===========================

class Process:
    """Represents a process in the OS"""
    _pid_counter = 1000
    
    def __init__(self, name, burst_time, memory_required):
        self.pid = Process._pid_counter
        Process._pid_counter += 1
        
        self.name = name
        self.state = ProcessState.NEW
        self.arrival_time = 0
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.memory_required = memory_required
        self.memory_allocated = 0
        self.start_time = None
        self.end_time = None
        self.wait_time = 0
        self.turnaround_time = 0
    
    def __repr__(self):
        return f"P{self.pid}"
    
    def execute(self, time_slice):
        """Execute for given time slice"""
        if self.state != ProcessState.RUNNING:
            return 0
        
        executed = min(time_slice, self.remaining_time)
        self.remaining_time -= executed
        return executed
    
    def is_complete(self):
        """Check if process is complete"""
        return self.remaining_time <= 0


# ===========================
# MEMORY MANAGER
# ===========================

class MemoryManager:
    """Manages memory allocation and deallocation"""
    
    def __init__(self, partitions):
        self.partitions = [{'size': size, 'allocated': False, 'process_pid': None} 
                          for size in partitions]
        self.total_memory = sum(partitions)
        self.allocation_history = []
    
    def allocate_memory(self, process):
        """Allocate memory to a process"""
        # Try to find a suitable partition (First-Fit)
        for partition in self.partitions:
            if not partition['allocated'] and partition['size'] >= process.memory_required:
                partition['allocated'] = True
                partition['process_pid'] = process.pid
                process.memory_allocated = process.memory_required
                self.allocation_history.append(
                    f"Allocated {process.memory_required} units to P{process.pid}"
                )
                return True
        
        return False
    
    def deallocate_memory(self, process_pid):
        """Deallocate memory from a process"""
        for partition in self.partitions:
            if partition['process_pid'] == process_pid:
                partition['allocated'] = False
                partition['process_pid'] = None
                self.allocation_history.append(f"Deallocated memory from P{process_pid}")
                return True
        return False
    
    def get_memory_status(self):
        """Get current memory status"""
        used = sum(p['size'] for p in self.partitions if p['allocated'])
        return used, self.total_memory
    
    def display_memory_map(self):
        """Display memory map"""
        print("\n  Memory Map:")
        map_str = ""
        for partition in self.partitions:
            if partition['allocated']:
                map_str += f"[P{partition['process_pid']}:{partition['size']}] "
            else:
                map_str += f"[Free:{partition['size']}] "
        print(f"  {map_str}")
        
        used, total = self.get_memory_status()
        percentage = (used / total) * 100
        print(f"  Memory Usage: {used}/{total} ({percentage:.1f}%)")


# ===========================
# CPU SCHEDULER (Round Robin)
# ===========================

class CPUScheduler:
    """Implements Round Robin scheduling"""
    
    def __init__(self, time_quantum):
        self.time_quantum = time_quantum
        self.ready_queue = deque()
        self.gantt_chart = []
        self.current_time = 0
        self.processes_completed = []
    
    def add_process(self, process):
        """Add process to ready queue"""
        if process not in self.ready_queue:
            process.state = ProcessState.READY
            self.ready_queue.append(process)
    
    def remove_process(self, process):
        """Remove process from ready queue"""
        if process in self.ready_queue:
            self.ready_queue.remove(process)
    
    def run_scheduling(self, processes, memory_manager, io_manager):
        """Run Round Robin scheduling"""
        self.ready_queue.clear()
        self.gantt_chart = []
        self.current_time = 0
        self.processes_completed = []
        
        # Add all processes to ready queue
        for process in processes:
            if process.state != ProcessState.TERMINATED:
                self.add_process(process)
        
        total_processes = len(self.ready_queue)
        execution_steps = []
        
        while self.ready_queue:
            process = self.ready_queue.popleft()
            
            if process.start_time is None:
                process.start_time = self.current_time
                process.state = ProcessState.RUNNING
            
            # Execute for time quantum
            executed = min(self.time_quantum, process.remaining_time)
            process.remaining_time -= executed
            self.current_time += executed
            
            self.gantt_chart.append((str(process), self.current_time - executed, self.current_time))
            execution_steps.append(f"  Time {self.current_time - executed}-{self.current_time}: {process.name} (PID: {process.pid})")
            
            # Check if process is complete
            if process.is_complete():
                process.state = ProcessState.TERMINATED
                process.end_time = self.current_time
                process.turnaround_time = process.end_time - process.arrival_time
                self.processes_completed.append(process)
            else:
                # Add back to ready queue
                self.ready_queue.append(process)
        
        return execution_steps
    
    def display_gantt_chart(self):
        """Display Gantt chart"""
        if not self.gantt_chart:
            print("  (No processes executed)")
            return
        
        print("\n  Gantt Chart:")
        chart = " | ".join([p[0] for p in self.gantt_chart])
        timings = " ".join([str(p[1]) for p in self.gantt_chart[:-1]])
        timings += f" {self.gantt_chart[-1][2]}"
        
        print(f"  {chart}")
        print(f"  {timings}")


# ===========================
# FILE SYSTEM
# ===========================

class File:
    """Represents a file"""
    
    def __init__(self, filename, content=""):
        self.filename = filename
        self.content = content
        self.size = len(content)
        self.created_at = datetime.now()
        self.modified_at = datetime.now()
    
    def read(self):
        """Read file content"""
        return self.content
    
    def write(self, content):
        """Write to file"""
        self.content = content
        self.size = len(content)
        self.modified_at = datetime.now()
    
    def __repr__(self):
        return f"{self.filename} ({self.size} bytes)"


class FileSystem:
    """In-memory file system"""
    
    def __init__(self):
        self.files = {}
        self.create_file("system.log", "System log file created")
        self.create_file("readme.txt", "Welcome to SimpleOS!")
    
    def create_file(self, filename, content=""):
        """Create a new file"""
        if filename not in self.files:
            self.files[filename] = File(filename, content)
            return True
        return False
    
    def delete_file(self, filename):
        """Delete a file"""
        if filename in self.files and filename not in ["system.log", "readme.txt"]:
            del self.files[filename]
            return True
        return False
    
    def read_file(self, filename):
        """Read file content"""
        if filename in self.files:
            return self.files[filename].read()
        return None
    
    def write_file(self, filename, content):
        """Write to file"""
        if filename in self.files:
            self.files[filename].write(content)
            return True
        return False
    
    def list_files(self):
        """List all files"""
        return list(self.files.keys())
    
    def get_file_info(self, filename):
        """Get file information"""
        if filename in self.files:
            f = self.files[filename]
            return {
                'name': f.filename,
                'size': f.size,
                'created': f.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'modified': f.modified_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        return None


# ===========================
# I/O SYSTEM (Printer)
# ===========================

class PrintJob:
    """Represents a print job"""
    
    def __init__(self, process_pid, job_id, data):
        self.process_pid = process_pid
        self.job_id = job_id
        self.data = data
        self.status = "pending"
        self.created_at = datetime.now()
    
    def __repr__(self):
        return f"Job {self.job_id} (P{self.process_pid}): {self.data[:30]}..."


class IOManager:
    """Manages I/O devices (Printer)"""
    
    def __init__(self):
        self.printer_queue = deque()
        self.current_job = None
        self.job_counter = 1
        self.completed_jobs = []
    
    def send_to_printer(self, process_pid, data):
        """Send data to printer"""
        if len(self.printer_queue) < IO_QUEUE_LIMIT:
            job = PrintJob(process_pid, self.job_counter, data)
            self.job_counter += 1
            self.printer_queue.append(job)
            return True
        return False
    
    def process_printer_job(self):
        """Process a printer job"""
        if self.current_job:
            self.current_job.status = "completed"
            self.completed_jobs.append(self.current_job)
        
        if self.printer_queue:
            self.current_job = self.printer_queue.popleft()
            self.current_job.status = "printing"
            return self.current_job
        
        self.current_job = None
        return None
    
    def display_printer_status(self):
        """Display printer status"""
        print("\n  Printer Queue Status:")
        if self.current_job:
            print(f"  Currently printing: {self.current_job}")
        else:
            print(f"  Currently printing: (None)")
        
        if self.printer_queue:
            print(f"\n  Pending Jobs ({len(self.printer_queue)}):")
            for job in self.printer_queue:
                print(f"    - {job}")
        else:
            print(f"  Pending Jobs: (None)")
        
        print(f"\n  Completed Jobs: {len(self.completed_jobs)}")


# ===========================
# MAIN SIMULATOR
# ===========================

class SimpleOSSimulator:
    """Main OS Simulator"""
    
    def __init__(self):
        self.running = True
        self.system_time = 0
        self.processes = []
        self.memory_manager = MemoryManager(MEMORY_PARTITIONS)
        self.scheduler = CPUScheduler(TIME_QUANTUM)
        self.filesystem = FileSystem()
        self.io_manager = IOManager()
        
        # Sample processes
        self.init_sample_processes()
    
    def init_sample_processes(self):
        """Initialize sample processes"""
        self.processes = [
            Process("Chrome", 25, 120),
            Process("Code Editor", 30, 150),
            Process("File Manager", 15, 80),
            Process("Notepad", 20, 60),
            Process("Calculator", 10, 40),
        ]
    
    def display_main_menu(self):
        """Display main desktop menu"""
        clear_screen()
        options = [
            "Task Manager",
            "File Explorer",
            "Memory Manager",
            "CPU Scheduler",
            "I/O Devices (Printer)",
            "System Settings",
            "Shutdown"
        ]
        print_menu("SIMPLE OS DESKTOP", options)
    
    def task_manager(self):
        """Task Manager application"""
        clear_screen()
        print_header("TASK MANAGER")
        
        while True:
            print("\n1. View All Processes")
            print("2. Create New Process")
            print("3. Terminate Process")
            print("4. View Process Details")
            print("5. Back to Desktop")
            print_separator()
            
            choice = get_valid_input("Enter option: ", int, [1, 5])
            
            if choice == 1:
                self.display_processes()
            elif choice == 2:
                self.create_process()
            elif choice == 3:
                self.terminate_process()
            elif choice == 4:
                self.view_process_details()
            elif choice == 5:
                break
    
    def display_processes(self):
        """Display all processes in table format"""
        clear_screen()
        print_header("RUNNING PROCESSES")
        
        print("\n{:<8} {:<20} {:<12} {:<10} {:<12} {:<10}".format(
            "PID", "Name", "State", "Burst", "Memory", "Progress"
        ))
        print_separator(70)
        
        for process in self.processes:
            progress = ((process.burst_time - process.remaining_time) / process.burst_time * 100) if process.burst_time > 0 else 0
            print("{:<8} {:<20} {:<12} {:<10} {:<12} {:<10.1f}%".format(
                process.pid,
                process.name,
                process.state.value,
                process.burst_time,
                process.memory_allocated,
                progress
            ))
        
        print_separator(70)
        input("\nPress Enter to continue...")
    
    def create_process(self):
        """Create a new process"""
        clear_screen()
        print_header("CREATE NEW PROCESS")
        
        name = get_valid_input("Enter process name: ", str)
        burst_time = get_valid_input("Enter burst time (ms): ", int, [1, 100])
        memory = get_valid_input("Enter memory required (units): ", int, [10, 300])
        
        process = Process(name, burst_time, memory)
        
        # Try to allocate memory
        if self.memory_manager.allocate_memory(process):
            process.state = ProcessState.READY
            self.processes.append(process)
            print(f"\n✓ Process created: P{process.pid} - {process.name}")
            print(f"  Memory allocated: {process.memory_allocated} units")
        else:
            print(f"\n✗ Failed to create process: Insufficient memory")
        
        input("\nPress Enter to continue...")
    
    def terminate_process(self):
        """Terminate a process"""
        clear_screen()
        print_header("TERMINATE PROCESS")
        
        self.display_processes()
        
        pid = get_valid_input("\nEnter PID to terminate: ", int)
        
        for process in self.processes:
            if process.pid == pid:
                self.memory_manager.deallocate_memory(pid)
                process.state = ProcessState.TERMINATED
                print(f"\n✓ Process P{pid} terminated and memory freed")
                break
        else:
            print(f"\n✗ Process P{pid} not found")
        
        input("\nPress Enter to continue...")
    
    def view_process_details(self):
        """View detailed information about a process"""
        clear_screen()
        print_header("PROCESS DETAILS")
        
        pid = get_valid_input("Enter PID: ", int)
        
        for process in self.processes:
            if process.pid == pid:
                print(f"\n  Process Information:")
                print(f"  └─ PID: {process.pid}")
                print(f"  └─ Name: {process.name}")
                print(f"  └─ State: {process.state.value}")
                print(f"  └─ Arrival Time: {process.arrival_time}")
                print(f"  └─ Burst Time: {process.burst_time} ms")
                print(f"  └─ Remaining Time: {process.remaining_time} ms")
                print(f"  └─ Memory Allocated: {process.memory_allocated} units")
                print(f"  └─ Wait Time: {process.wait_time} ms")
                print(f"  └─ Turnaround Time: {process.turnaround_time} ms")
                input("\nPress Enter to continue...")
                return
        
        print(f"\n✗ Process P{pid} not found")
        input("\nPress Enter to continue...")
    
    def file_explorer(self):
        """File Explorer application"""
        clear_screen()
        print_header("FILE EXPLORER")
        
        while True:
            print("\n1. List Files")
            print("2. Create File")
            print("3. Delete File")
            print("4. View File Content")
            print("5. Edit File")
            print("6. Back to Desktop")
            print_separator()
            
            choice = get_valid_input("Enter option: ", int, [1, 6])
            
            if choice == 1:
                self.list_files()
            elif choice == 2:
                self.create_file()
            elif choice == 3:
                self.delete_file()
            elif choice == 4:
                self.view_file()
            elif choice == 5:
                self.edit_file()
            elif choice == 6:
                break
    
    def list_files(self):
        """List all files"""
        clear_screen()
        print_header("FILE LIST")
        
        files = self.filesystem.list_files()
        
        if files:
            print("\n  Files:")
            for idx, filename in enumerate(files, 1):
                info = self.filesystem.get_file_info(filename)
                print(f"  {idx}. {info['name']} ({info['size']} bytes)")
                print(f"     Created: {info['created']}")
        else:
            print("\n  (No files found)")
        
        print_separator()
        input("\nPress Enter to continue...")
    
    def create_file(self):
        """Create a new file"""
        clear_screen()
        print_header("CREATE FILE")
        
        filename = get_valid_input("Enter filename: ", str)
        content = get_valid_input("Enter content (or 'skip' for empty): ", str)
        
        if content.lower() == 'skip':
            content = ""
        
        if self.filesystem.create_file(filename, content):
            print(f"\n✓ File created: {filename}")
        else:
            print(f"\n✗ File already exists or cannot be created")
        
        input("\nPress Enter to continue...")
    
    def delete_file(self):
        """Delete a file"""
        clear_screen()
        print_header("DELETE FILE")
        
        self.list_files()
        filename = get_valid_input("Enter filename to delete: ", str)
        
        if self.filesystem.delete_file(filename):
            print(f"\n✓ File deleted: {filename}")
        else:
            print(f"\n✗ Cannot delete system files or file not found")
        
        input("\nPress Enter to continue...")
    
    def view_file(self):
        """View file content"""
        clear_screen()
        print_header("VIEW FILE")
        
        filename = get_valid_input("Enter filename: ", str)
        content = self.filesystem.read_file(filename)
        
        if content is not None:
            print(f"\n  Content of '{filename}':")
            print(f"  {'-' * 40}")
            print(f"  {content}")
            print(f"  {'-' * 40}")
        else:
            print(f"\n✗ File not found: {filename}")
        
        input("\nPress Enter to continue...")
    
    def edit_file(self):
        """Edit file content"""
        clear_screen()
        print_header("EDIT FILE")
        
        filename = get_valid_input("Enter filename: ", str)
        
        if filename not in self.filesystem.files:
            print(f"\n✗ File not found: {filename}")
            input("\nPress Enter to continue...")
            return
        
        new_content = get_valid_input("Enter new content: ", str)
        
        if self.filesystem.write_file(filename, new_content):
            print(f"\n✓ File updated: {filename}")
        else:
            print(f"\n✗ Failed to update file")
        
        input("\nPress Enter to continue...")
    
    def memory_manager_app(self):
        """Memory Manager application"""
        clear_screen()
        print_header("MEMORY MANAGER")
        
        while True:
            print("\n1. View Memory Status")
            print("2. Allocate Memory")
            print("3. Deallocate Memory")
            print("4. View Memory Map")
            print("5. Back to Desktop")
            print_separator()
            
            choice = get_valid_input("Enter option: ", int, [1, 5])
            
            if choice == 1:
                self.view_memory_status()
            elif choice == 2:
                self.allocate_memory()
            elif choice == 3:
                self.deallocate_memory()
            elif choice == 4:
                self.view_memory_map()
            elif choice == 5:
                break
    
    def view_memory_status(self):
        """View memory status"""
        clear_screen()
        print_header("MEMORY STATUS")
        
        used, total = self.memory_manager.get_memory_status()
        percentage = (used / total) * 100
        
        print(f"\n  Total Memory: {total} units")
        print(f"  Used Memory: {used} units")
        print(f"  Free Memory: {total - used} units")
        print(f"  Usage: {percentage:.1f}%")
        
        print(f"\n  Partitions:")
        for idx, partition in enumerate(self.memory_manager.partitions, 1):
            status = "Allocated" if partition['allocated'] else "Free"
            pid_info = f"(P{partition['process_pid']})" if partition['process_pid'] else ""
            print(f"    Partition {idx}: {partition['size']} units - {status} {pid_info}")
        
        print_separator()
        input("\nPress Enter to continue...")
    
    def allocate_memory(self):
        """Allocate memory manually"""
        clear_screen()
        print_header("ALLOCATE MEMORY")
        
        self.display_processes()
        
        pid = get_valid_input("\nEnter PID: ", int)
        
        for process in self.processes:
            if process.pid == pid and process.memory_allocated == 0:
                if self.memory_manager.allocate_memory(process):
                    print(f"\n✓ Memory allocated to P{pid}")
                else:
                    print(f"\n✗ Insufficient memory or process not found")
                break
        
        input("\nPress Enter to continue...")
    
    def deallocate_memory(self):
        """Deallocate memory manually"""
        clear_screen()
        print_header("DEALLOCATE MEMORY")
        
        self.display_processes()
        
        pid = get_valid_input("\nEnter PID: ", int)
        
        if self.memory_manager.deallocate_memory(pid):
            print(f"\n✓ Memory deallocated from P{pid}")
        else:
            print(f"\n✗ Process not found or not allocated")
        
        input("\nPress Enter to continue...")
    
    def view_memory_map(self):
        """View memory map"""
        clear_screen()
        print_header("MEMORY MAP")
        
        self.memory_manager.display_memory_map()
        
        print_separator()
        input("\nPress Enter to continue...")
    
    def cpu_scheduler_app(self):
        """CPU Scheduler application"""
        clear_screen()
        print_header("CPU SCHEDULER - ROUND ROBIN")
        
        while True:
            print(f"\n1. Run Scheduling Algorithm (Quantum: {TIME_QUANTUM}ms)")
            print("2. View Scheduling Results")
            print("3. Set Time Quantum")
            print("4. Back to Desktop")
            print_separator()
            
            choice = get_valid_input("Enter option: ", int, [1, 4])
            
            if choice == 1:
                self.run_scheduling()
            elif choice == 2:
                self.view_scheduling_results()
            elif choice == 3:
                self.set_time_quantum()
            elif choice == 4:
                break
    
    def run_scheduling(self):
        """Run the scheduler"""
        clear_screen()
        print_header("RUNNING ROUND ROBIN SCHEDULING")
        
        print("\n  Allocating memory to processes...")
        for process in self.processes:
            if process.state != ProcessState.TERMINATED:
                if not process.memory_allocated:
                    self.memory_manager.allocate_memory(process)
        
        print("  Starting CPU execution...\n")
        
        execution_steps = self.scheduler.run_scheduling(
            self.processes, 
            self.memory_manager, 
            self.io_manager
        )
        
        for step in execution_steps:
            print(step)
        
        print(f"\n  Scheduling complete!")
        print(f"  Total time: {self.scheduler.current_time}ms")
        
        input("\nPress Enter to continue...")
    
    def view_scheduling_results(self):
        """View scheduling results"""
        clear_screen()
        print_header("SCHEDULING RESULTS")
        
        if not self.scheduler.processes_completed:
            print("\n  (No scheduling results available)")
            print("  Run the scheduler first!")
            input("\nPress Enter to continue...")
            return
        
        print("\n  Execution Summary:")
        print("\n{:<8} {:<20} {:<12} {:<12} {:<12}".format(
            "PID", "Name", "Burst Time", "Turnaround", "Wait Time"
        ))
        print_separator(70)
        
        total_turnaround = 0
        for process in self.scheduler.processes_completed:
            print("{:<8} {:<20} {:<12} {:<12} {:<12}".format(
                process.pid,
                process.name,
                process.burst_time,
                process.turnaround_time,
                process.wait_time
            ))
            total_turnaround += process.turnaround_time
        
        avg_turnaround = total_turnaround / len(self.scheduler.processes_completed)
        print_separator(70)
        print(f"Average Turnaround Time: {avg_turnaround:.2f}ms")
        
        print("\n")
        self.scheduler.display_gantt_chart()
        
        print_separator()
        input("\nPress Enter to continue...")
    
    def set_time_quantum(self):
        """Set time quantum"""
        clear_screen()
        print_header("SET TIME QUANTUM")
        
        global TIME_QUANTUM
        quantum = get_valid_input(f"Enter time quantum (current: {TIME_QUANTUM}ms): ", int, [1, 50])
        TIME_QUANTUM = quantum
        self.scheduler.time_quantum = quantum
        
        print(f"\n✓ Time quantum set to {TIME_QUANTUM}ms")
        input("\nPress Enter to continue...")
    
    def io_devices_app(self):
        """I/O Devices (Printer) application"""
        clear_screen()
        print_header("I/O DEVICES - PRINTER MANAGEMENT")
        
        while True:
            print("\n1. Send Print Job")
            print("2. View Printer Queue")
            print("3. Process Next Job")
            print("4. View Job History")
            print("5. Back to Desktop")
            print_separator()
            
            choice = get_valid_input("Enter option: ", int, [1, 5])
            
            if choice == 1:
                self.send_print_job()
            elif choice == 2:
                self.view_printer_queue()
            elif choice == 3:
                self.process_printer_job()
            elif choice == 4:
                self.view_job_history()
            elif choice == 5:
                break
    
    def send_print_job(self):
        """Send a print job"""
        clear_screen()
        print_header("SEND PRINT JOB")
        
        self.display_processes()
        
        pid = get_valid_input("\nEnter source PID: ", int)
        data = get_valid_input("Enter print data: ", str)
        
        # Verify process exists
        process_found = any(p.pid == pid for p in self.processes)
        
        if process_found:
            if self.io_manager.send_to_printer(pid, data):
                print(f"\n✓ Print job queued from P{pid}")
            else:
                print(f"\n✗ Printer queue is full")
        else:
            print(f"\n✗ Process P{pid} not found")
        
        input("\nPress Enter to continue...")
    
    def view_printer_queue(self):
        """View printer queue"""
        clear_screen()
        print_header("PRINTER QUEUE")
        
        self.io_manager.display_printer_status()
        
        print_separator()
        input("\nPress Enter to continue...")
    
    def process_printer_job(self):
        """Process a printer job"""
        clear_screen()
        print_header("PROCESS PRINTER JOB")
        
        job = self.io_manager.process_printer_job()
        
        if job:
            print(f"\n✓ Job {job.job_id} completed!")
            print(f"  Data: {job.data[:50]}...")
        else:
            print(f"\n  (No jobs to process)")
        
        input("\nPress Enter to continue...")
    
    def view_job_history(self):
        """View job history"""
        clear_screen()
        print_header("PRINT JOB HISTORY")
        
        if self.io_manager.completed_jobs:
            print(f"\n  Completed Jobs ({len(self.io_manager.completed_jobs)}):")
            for idx, job in enumerate(self.io_manager.completed_jobs, 1):
                print(f"  {idx}. {job}")
        else:
            print(f"\n  (No completed jobs)")
        
        print_separator()
        input("\nPress Enter to continue...")
    
    def system_settings(self):
        """System Settings application"""
        clear_screen()
        print_header("SYSTEM SETTINGS")
        
        print(f"\n  System Information:")
        print(f"  └─ System Name: SimpleOS")
        print(f"  └─ Version: 1.0")
        print(f"  └─ Kernel: SimpleOS Kernel 1.0")
        print(f"  └─ CPU Cores: 4")
        print(f"  └─ Total Memory: {TOTAL_MEMORY} units")
        print(f"  └─ Boot Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"\n  Configuration:")
        print(f"  └─ Time Quantum: {TIME_QUANTUM}ms")
        print(f"  └─ Memory Partitions: {len(MEMORY_PARTITIONS)}")
        print(f"  └─ Total Processes: {len(self.processes)}")
        
        print_separator()
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main run loop"""
        # Boot sequence
        clear_screen()
        print_header("Starting SimpleOS...")
        print("\n  [*] Initializing system...")
        print("  [*] Loading kernel...")
        print("  [*] Initializing memory manager...")
        print("  [*] Starting device drivers...")
        print("  [*] Mounting file system...")
        print("\n  ✓ System ready!")
        input("\nPress Enter to continue...")
        
        # Main menu loop
        while self.running:
            self.display_main_menu()
            
            choice = get_valid_input("Enter option: ", int, [1, 7])
            
            if choice == 1:
                self.task_manager()
            elif choice == 2:
                self.file_explorer()
            elif choice == 3:
                self.memory_manager_app()
            elif choice == 4:
                self.cpu_scheduler_app()
            elif choice == 5:
                self.io_devices_app()
            elif choice == 6:
                self.system_settings()
            elif choice == 7:
                self.shutdown()
    
    def shutdown(self):
        """Shutdown the system"""
        clear_screen()
        print_header("SHUTTING DOWN")
        print("\n  [*] Closing all applications...")
        print("  [*] Saving system state...")
        print("  [*] Unmounting file system...")
        print("  [*] Stopping device drivers...")
        print("  [*] Powering down...\n")
        print("  ✓ System shut down successfully!")
        print("\n  Thank you for using SimpleOS!")
        self.running = False


# ===========================
# MAIN ENTRY POINT
# ===========================

def main():
    """Main entry point"""
    simulator = SimpleOSSimulator()
    try:
        simulator.run()
    except KeyboardInterrupt:
        print("\n\n✗ System interrupted!")
        simulator.shutdown()


if __name__ == "__main__":
    main()
