# SimpleOS Implementation Guide

## Code Architecture & Design Patterns

This document explains the implementation details of SimpleOS, including key design decisions and code patterns used.

---

## Table of Contents

1. [Class Hierarchy](#class-hierarchy)
2. [Design Patterns](#design-patterns)
3. [Core Implementation](#core-implementation)
4. [Algorithm Analysis](#algorithm-analysis)
5. [Code Examples](#code-examples)
6. [Testing Guide](#testing-guide)

---

## Class Hierarchy

### ProcessState Enum

```python
class ProcessState(Enum):
    """Process states"""
    NEW = "NEW"              # Process created, not admitted
    READY = "READY"          # Ready to execute, waiting for CPU
    RUNNING = "RUNNING"      # Currently executing on CPU
    WAITING = "WAITING"      # Waiting for I/O operation
    TERMINATED = "TERMINATED"  # Completed execution
```

**Usage**: Represents the current state of a process in the system.

**Transitions**:
```
NEW → READY → RUNNING → [WAITING ↔ READY] → TERMINATED
```

### Process Class

```python
class Process:
    """Represents a process in the OS"""
    _pid_counter = 1000  # Static counter for unique PIDs
    
    def __init__(self, name, burst_time, memory_required):
        self.pid = Process._pid_counter
        Process._pid_counter += 1
        
        self.name = name
        self.state = ProcessState.NEW
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.memory_required = memory_required
        self.memory_allocated = 0
        # ... timing metrics
```

**Key Methods**:

```python
def execute(self, time_slice):
    """Execute process for given time slice"""
    executed = min(time_slice, self.remaining_time)
    self.remaining_time -= executed
    return executed

def is_complete(self):
    """Check if process is complete"""
    return self.remaining_time <= 0
```

### MemoryManager Class

```python
class MemoryManager:
    """Manages memory allocation and deallocation"""
    
    def __init__(self, partitions):
        self.partitions = [
            {'size': size, 'allocated': False, 'process_pid': None} 
            for size in partitions
        ]
        self.total_memory = sum(partitions)
```

**Allocation Algorithm (First-Fit)**:

```python
def allocate_memory(self, process):
    """Allocate memory to a process"""
    # Try to find a suitable partition (First-Fit)
    for partition in self.partitions:
        if not partition['allocated'] and \
           partition['size'] >= process.memory_required:
            
            partition['allocated'] = True
            partition['process_pid'] = process.pid
            process.memory_allocated = process.memory_required
            return True
    
    return False
```

**Time Complexity**: O(n) where n = number of partitions
**Space Complexity**: O(1) - constant space for partition tracking

### CPUScheduler Class

```python
class CPUScheduler:
    """Implements Round Robin scheduling"""
    
    def __init__(self, time_quantum):
        self.time_quantum = time_quantum
        self.ready_queue = deque()
        self.gantt_chart = []
        self.current_time = 0
```

**Round Robin Algorithm**:

```python
def run_scheduling(self, processes, memory_manager, io_manager):
    """Run Round Robin scheduling"""
    self.ready_queue.clear()
    self.current_time = 0
    
    # Add all processes to ready queue
    for process in processes:
        if process.state != ProcessState.TERMINATED:
            self.add_process(process)
    
    # Schedule processes
    while self.ready_queue:
        process = self.ready_queue.popleft()
        
        # Set start time on first run
        if process.start_time is None:
            process.start_time = self.current_time
            process.state = ProcessState.RUNNING
        
        # Execute for time quantum
        executed = min(self.time_quantum, process.remaining_time)
        process.remaining_time -= executed
        self.current_time += executed
        
        # Record in Gantt chart
        self.gantt_chart.append((str(process), 
                                 self.current_time - executed, 
                                 self.current_time))
        
        # Check completion
        if process.is_complete():
            process.state = ProcessState.TERMINATED
            process.end_time = self.current_time
            process.turnaround_time = process.end_time - process.arrival_time
        else:
            # Re-enqueue for next round
            self.ready_queue.append(process)
```

**Time Complexity**: O(n × m) where n = processes, m = context switches
**Gantt Chart**: Records all process executions

### FileSystem Class

```python
class FileSystem:
    """In-memory file system"""
    
    def __init__(self):
        self.files = {}  # {filename: File object}
        self.file_count = 0
```

**File Operations**:

```python
def create_file(self, filename, content=""):
    """Create a new file"""
    if filename not in self.files:
        self.files[filename] = File(filename, content)
        return True
    return False

def delete_file(self, filename):
    """Delete a file (system files protected)"""
    if filename in self.files and \
       filename not in ["system.log", "readme.txt"]:
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
```

**Data Structure**: Dictionary for O(1) average lookup time

### IOManager Class

```python
class IOManager:
    """Manages I/O devices (Printer)"""
    
    def __init__(self):
        self.printer_queue = deque()
        self.current_job = None
        self.job_counter = 1
        self.completed_jobs = []
```

**Print Job Operations**:

```python
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
```

**Data Structure**: FIFO queue with deque for O(1) operations

---

## Design Patterns

### 1. Enum Pattern (ProcessState)

**Purpose**: Type-safe representation of process states

**Advantages**:
- Prevents invalid state assignments
- Self-documenting code
- Compile-time checking

```python
# Good: Type-safe
process.state = ProcessState.RUNNING

# Bad: String prone to typos
process.state = "RUNING"  # Typo not caught
```

### 2. Static Counter Pattern (Process._pid_counter)

**Purpose**: Ensure unique Process IDs

**Implementation**:
```python
class Process:
    _pid_counter = 1000
    
    def __init__(self, name, burst_time, memory_required):
        self.pid = Process._pid_counter
        Process._pid_counter += 1
```

**Advantages**:
- Automatic unique ID generation
- Thread-safe in single-threaded context
- No external ID management needed

### 3. Deque Pattern (Scheduler Queue)

**Purpose**: Efficient queue operations for scheduling

**Usage**:
```python
from collections import deque

self.ready_queue = deque()

# O(1) operations
self.ready_queue.append(process)      # Enqueue
process = self.ready_queue.popleft()  # Dequeue
```

**Advantages**:
- O(1) time for both ends
- Better than list for queue operations
- Memory efficient

### 4. Dictionary Pattern (File System)

**Purpose**: Fast file lookup and management

**Usage**:
```python
self.files = {
    'system.log': File_obj,
    'readme.txt': File_obj,
    'document.txt': File_obj
}

# O(1) average access time
file = self.files.get(filename)
```

---

## Core Implementation

### Round Robin Scheduling Detailed Flow

**Input**: List of processes, time quantum

**Process**:

```
1. Initialize
   ├── Clear ready queue
   ├── Set current_time = 0
   └── Add all unfinished processes to queue

2. While ready_queue is not empty
   ├── Dequeue first process
   ├── If first execution:
   │   ├── Set start_time = current_time
   │   └── Set state = RUNNING
   ├── Execute
   │   ├── time_to_execute = min(time_quantum, remaining_time)
   │   ├── remaining_time -= time_to_execute
   │   ├── current_time += time_to_execute
   │   └── Record in gantt_chart
   ├── Check completion
   │   ├── If remaining_time == 0:
   │   │   ├── Set state = TERMINATED
   │   │   ├── Set end_time = current_time
   │   │   └── Calculate metrics
   │   └── Else:
   │       └── Re-enqueue at end of queue
   
3. Return
   ├── Gantt chart with all executions
   ├── Scheduling statistics
   └── Process completion order
```

**Example Trace**:

```
Input: Processes [P1(burst=10), P2(burst=5)], Quantum=3

Step 1: Queue=[P1, P2], time=0
Step 2: Execute P1 for 3 (remaining=7)
        Queue=[P2, P1], time=3
Step 3: Execute P2 for 3 (remaining=2)
        Queue=[P1, P2], time=6
Step 4: Execute P1 for 3 (remaining=4)
        Queue=[P2, P1], time=9
Step 5: Execute P2 for 2 (remaining=0, DONE)
        Queue=[P1], time=11
Step 6: Execute P1 for 3 (remaining=1)
        Queue=[P1], time=14
Step 7: Execute P1 for 1 (remaining=0, DONE)
        Queue=[], time=15

Gantt Chart: P1|P2|P1|P2|P1|P1
Times:       0-3|3-6|6-9|9-11|11-14|14-15
```

### First-Fit Memory Allocation Detailed Flow

**Input**: Process with memory requirement

**Process**:

```
1. Iterate through partitions (in order)
   
2. For each partition:
   ├── Check if not allocated
   │   └── Check if size >= requirement
   │       └── Yes:
   │           ├── Mark partition as allocated
   │           ├── Assign process PID
   │           ├── Update process.memory_allocated
   │           └── Return True (success)
   
3. If no suitable partition found:
   └── Return False (allocation fails)

4. Deallocation (when process terminates):
   ├── Iterate through partitions
   ├── Find partition with matching PID
   ├── Mark as not allocated
   └── Process can now use memory again
```

**Example Trace**:

```
Partitions: [100, 150, 200, 250]
Process P1 (requires 120):
  ├── Check partition 0 (100) - too small
  ├── Check partition 1 (150) - suitable ✓
  └── Allocate

State: [Free, P1, Free, Free]

Process P2 (requires 150):
  ├── Check partition 0 (100) - too small
  ├── Check partition 1 (150) - allocated
  ├── Check partition 2 (200) - suitable ✓
  └── Allocate

State: [Free, P1, P2, Free]

Process P3 (requires 100):
  ├── Check partition 0 (100) - suitable ✓
  └── Allocate

State: [P3, P1, P2, Free]

Process P1 terminates (deallocate):
  ├── Find partition 1
  ├── Mark as free

State: [P3, Free, P2, Free]
```

---

## Algorithm Analysis

### Round Robin Scheduling

**Time Complexity**: O(n × m)
- n = number of processes
- m = number of context switches
- Worst case: each process switches multiple times

**Space Complexity**: O(n)
- Storage for ready queue: O(n)
- Gantt chart: O(n × m)

**Advantages**:
- Fair allocation (each process gets equal CPU time)
- No starvation (every process gets CPU)
- Good for time-sharing systems

**Disadvantages**:
- High context switch overhead
- Turnaround time can be high with large quantum
- Performance depends on time quantum selection

### First-Fit Allocation

**Time Complexity**: O(n)
- n = number of memory partitions
- Linear scan through partitions

**Space Complexity**: O(1)
- Only store partition metadata

**Advantages**:
- Simple implementation
- Fast allocation
- Low overhead

**Disadvantages**:
- May cause external fragmentation (with other algorithms)
- Leaves small free spaces

**Comparison with other algorithms**:

| Algorithm | Allocation Time | Space Waste |
|-----------|-----------------|-------------|
| First-Fit | O(n) Fast | Medium |
| Best-Fit | O(n) | Low |
| Worst-Fit | O(n) | High |
| Next-Fit | O(n) | Medium |

---

## Code Examples

### Example 1: Creating a Process

```python
# Create a new process
process = Process("Chrome", burst_time=25, memory_required=120)

print(f"PID: {process.pid}")              # 1000
print(f"Name: {process.name}")            # Chrome
print(f"State: {process.state.value}")    # NEW
print(f"Burst Time: {process.burst_time}") # 25
print(f"Memory: {process.memory_required}") # 120
```

### Example 2: Memory Allocation

```python
# Initialize memory manager
memory_mgr = MemoryManager([100, 150, 200, 250])

# Create process
process = Process("App", 20, 120)

# Try to allocate
if memory_mgr.allocate_memory(process):
    print(f"✓ Allocated {process.memory_allocated} to P{process.pid}")
else:
    print(f"✗ Insufficient memory")

# Display memory map
memory_mgr.display_memory_map()
# Output:
# [P1000:120] [Free:150] [Free:200] [Free:250]
# Memory Usage: 120/700 (17.1%)
```

### Example 3: CPU Scheduling

```python
# Create scheduler
scheduler = CPUScheduler(time_quantum=5)

# Create processes
processes = [
    Process("P1", burst_time=10, memory_required=50),
    Process("P2", burst_time=8, memory_required=40),
]

# Add to ready queue
for p in processes:
    scheduler.add_process(p)

# Run scheduling
scheduler.run_scheduling(processes, memory_mgr, io_mgr)

# Display results
scheduler.display_gantt_chart()
# Output:
# P1 | P2 | P1 | P2 | P1
# 0    5   10   13  15
```

### Example 4: File Operations

```python
# Initialize file system
fs = FileSystem()

# Create file
if fs.create_file("data.txt", "Hello, World!"):
    print("✓ File created")

# Read file
content = fs.read_file("data.txt")
print(f"Content: {content}")  # Hello, World!

# Update file
fs.write_file("data.txt", "Hello, SimpleOS!")
print(f"Updated: {fs.read_file('data.txt')}")

# List files
files = fs.list_files()
print(f"Files: {files}")
# [system.log, readme.txt, data.txt]
```

### Example 5: I/O Operations

```python
# Initialize I/O manager
io_mgr = IOManager()

# Send print job
if io_mgr.send_to_printer(1000, "Document.pdf"):
    print("✓ Job queued")

# Send another job
io_mgr.send_to_printer(1001, "Image.jpg")

# View queue status
io_mgr.display_printer_status()
# Output:
# Currently printing: (None)
# Pending Jobs (2):
#   - Job 1 (P1000): Document.pdf
#   - Job 2 (P1001): Image.jpg

# Process first job
job = io_mgr.process_printer_job()
print(f"Processing: {job}")
# Processing: Job 1 (P1000): Document.pdf
```

---

## Testing Guide

### Unit Tests

#### Test Process Creation

```python
def test_process_creation():
    p1 = Process("Chrome", 25, 120)
    p2 = Process("Firefox", 30, 150)
    
    assert p1.pid == 1000
    assert p2.pid == 1001
    assert p1.state == ProcessState.NEW
    assert p1.remaining_time == 25
    print("✓ Process creation tests passed")
```

#### Test Memory Allocation

```python
def test_memory_allocation():
    mm = MemoryManager([100, 150])
    p = Process("App", 20, 120)
    
    # Should fail (need 120, max partition is 150)
    assert not mm.allocate_memory(p)
    
    p2 = Process("App2", 20, 100)
    # Should succeed
    assert mm.allocate_memory(p2)
    print("✓ Memory allocation tests passed")
```

#### Test Scheduling

```python
def test_round_robin():
    scheduler = CPUScheduler(5)
    processes = [
        Process("P1", 10, 50),
        Process("P2", 10, 50)
    ]
    
    scheduler.run_scheduling(processes, mm, io_mgr)
    assert scheduler.current_time == 20
    assert len(scheduler.gantt_chart) > 0
    print("✓ Scheduling tests passed")
```

#### Test File System

```python
def test_filesystem():
    fs = FileSystem()
    
    # Test create
    assert fs.create_file("test.txt", "data")
    assert not fs.create_file("test.txt", "data")  # duplicate
    
    # Test read
    assert fs.read_file("test.txt") == "data"
    
    # Test write
    fs.write_file("test.txt", "new data")
    assert fs.read_file("test.txt") == "new data"
    
    # Test delete
    assert fs.delete_file("test.txt")
    assert fs.read_file("test.txt") is None
    
    print("✓ File system tests passed")
```

### Integration Tests

#### Complete Workflow Test

```python
def test_complete_workflow():
    # Initialize simulator
    sim = SimpleOSSimulator()
    
    # Create process
    initial_count = len(sim.processes)
    sim.create_process()  # Manual user input
    assert len(sim.processes) == initial_count + 1
    
    # Check memory allocation
    used, total = sim.memory_manager.get_memory_status()
    assert used <= total
    
    # Run scheduler
    results = sim.scheduler.run_scheduling(
        sim.processes,
        sim.memory_manager,
        sim.io_manager
    )
    assert len(results) > 0
    
    # Check file operations
    assert sim.filesystem.create_file("test.md", "content")
    
    print("✓ Integration tests passed")
```

---

## Performance Optimization Tips

### 1. Memory Allocation

```python
# Current: O(n) first-fit
# Optimized: Bitmap for quick free space detection
class OptimizedMemoryManager:
    def __init__(self, total_size):
        self.bitmap = [False] * total_size  # False = free
        
    def allocate(self, size):
        # Faster for large memory systems
        # Use bit operations for speed
        pass
```

### 2. Process Scheduling

```python
# Current: Deque O(1) per operation
# For many processes, could add:
class OptimizedScheduler:
    def __init__(self):
        self.ready_queue = deque()
        self.ready_queue_index = 0  # Cache to avoid repeated scans
        
    def get_next_process_cached(self):
        # Skip completed processes
        pass
```

### 3. File System

```python
# Current: Dictionary O(1) average
# For file searching:
class OptimizedFileSystem:
    def __init__(self):
        self.files = {}
        self.index_by_type = {}  # Cache by extension
        
    def find_by_type(self, extension):
        # O(1) lookup for file type
        return self.index_by_type.get(extension, [])
```

---

## Debugging Tips

### 1. Process State Tracking

```python
def debug_process_state(process):
    print(f"Process {process.pid}:")
    print(f"  State: {process.state.value}")
    print(f"  Remaining: {process.remaining_time}ms")
    print(f"  Memory: {process.memory_allocated}/{process.memory_required}")
    print(f"  Start: {process.start_time}")
```

### 2. Gantt Chart Validation

```python
def validate_gantt_chart(gantt_chart, total_time):
    current_time = 0
    for process, start, end in gantt_chart:
        if start != current_time:
            print(f"Gap detected: {current_time} to {start}")
        current_time = end
    
    if current_time != total_time:
        print(f"Incorrect total time: {current_time} vs {total_time}")
```

### 3. Memory Leak Detection

```python
def check_memory_leaks(memory_manager, processes):
    allocated_by_mm = sum(p['size'] for p in memory_manager.partitions 
                         if p['allocated'])
    allocated_by_proc = sum(p.memory_allocated for p in processes)
    
    if allocated_by_mm != allocated_by_proc:
        print(f"Memory mismatch: MM={allocated_by_mm}, Procs={allocated_by_proc}")
```

---

## Conclusion

This implementation guide provides comprehensive insight into SimpleOS's design and implementation. Understanding these patterns and algorithms will help in extending the system with additional features and optimizations.

The modular architecture allows for easy testing, debugging, and enhancement of individual components without affecting the rest of the system.

---

**Last Updated**: April 2026  
**Version**: 1.0
