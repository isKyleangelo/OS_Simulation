# SimpleOS - Interactive Operating System Simulator

## Overview

**SimpleOS** is a Python-based interactive operating system simulator that mimics a simplified Windows-like environment using a command-line interface. It demonstrates core OS functionalities including process management, CPU scheduling, memory management, file handling, and I/O operations.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [System Architecture](#system-architecture)
3. [Core Components](#core-components)
4. [Process Lifecycle](#process-lifecycle)
5. [CPU Scheduling Algorithm](#cpu-scheduling-algorithm)
6. [Memory Management Strategy](#memory-management-strategy)
7. [File System Simulation](#file-system-simulation)
8. [I/O Device Handling](#io-device-handling)
9. [Sample Execution](#sample-execution)
10. [Features & Usage](#features--usage)

---

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Windows, macOS, or Linux environment
- Terminal or Command Prompt

### Installation & Execution

```bash
# Navigate to the project directory
cd /path/to/CMSC_314

# Run the simulator
python os_cli.py
```

### Boot Sequence

When you launch SimpleOS, the system performs initialization:

```
==================================================
                Starting SimpleOS...              
==================================================

  [*] Initializing system...
  [*] Loading kernel...
  [*] Initializing memory manager...
  [*] Starting device drivers...
  [*] Mounting file system...

  ✓ System ready!
```

---

## System Architecture

### Class Hierarchy

```
SimpleOSSimulator (Main Simulator)
├── ProcessState (Enum)
├── Process (Process Management)
├── MemoryManager (Memory Management)
├── CPUScheduler (CPU Scheduling)
├── FileSystem (File System)
│   └── File
└── IOManager (I/O Device Management)
    └── PrintJob
```

### System Configuration

| Parameter | Value | Purpose |
|-----------|-------|---------|
| Total Memory | 700 units | System memory pool |
| Memory Partitions | [100, 150, 200, 250] | Fixed memory blocks |
| Time Quantum | 5 ms | Round Robin scheduling interval |
| IO Queue Limit | 20 jobs | Maximum printer queue size |

---

## Core Components

### 1. Process Management

#### Process Class

Each process is represented with:

| Attribute | Description |
|-----------|-------------|
| `pid` | Unique process identifier (auto-incremented from 1000) |
| `name` | Process name (e.g., "Chrome", "Code Editor") |
| `state` | Current state (NEW, READY, RUNNING, WAITING, TERMINATED) |
| `burst_time` | Total CPU time needed (milliseconds) |
| `remaining_time` | Remaining CPU time to execute |
| `memory_required` | Memory needed for execution |
| `memory_allocated` | Actual allocated memory |
| `arrival_time` | When process arrived in system |
| `start_time` | When process started executing |
| `end_time` | When process completed |
| `wait_time` | Time waiting in queue |
| `turnaround_time` | Total time from arrival to completion |

#### Default Sample Processes

```python
Process("Chrome", 25, 120)          # 25ms burst, 120 units memory
Process("Code Editor", 30, 150)     # 30ms burst, 150 units memory
Process("File Manager", 15, 80)     # 15ms burst, 80 units memory
Process("Notepad", 20, 60)          # 20ms burst, 60 units memory
Process("Calculator", 10, 40)       # 10ms burst, 40 units memory
```

---

## Process Lifecycle

### State Transition Diagram

```
NEW → READY → RUNNING → [WAITING] → READY → TERMINATED
              ↓        ↑            ↑
              └────────┴────────────┘
                (I/O Operation)
```

### Detailed Lifecycle

1. **NEW State**
   - Process is created but not yet admitted
   - Memory requirements checked
   - Not added to ready queue

2. **READY State**
   - Process admitted to system
   - Memory allocated successfully
   - Waiting for CPU time

3. **RUNNING State**
   - Process executing on CPU
   - Executes for time quantum (5ms)
   - CPU cycle counter incremented

4. **WAITING State**
   - Process waiting for I/O operation to complete
   - Printer queue example: process sending print job
   - Returns to READY when I/O completes

5. **TERMINATED State**
   - Process completed execution
   - Memory deallocated
   - Statistics calculated (turnaround time, wait time)

---

## CPU Scheduling Algorithm

### Algorithm: Round Robin (RR)

**Description**: Each process gets equal CPU time (time quantum). When time quantum expires, process goes to back of queue.

### Implementation Details

```python
class CPUScheduler:
    def __init__(self, time_quantum):
        self.time_quantum = time_quantum  # Default: 5ms
        self.ready_queue = deque()
        self.gantt_chart = []
        self.current_time = 0
```

### Scheduling Process

1. **Initialization**
   - All processes added to ready queue
   - All marked as READY state

2. **Execution Loop**
   ```
   While ready_queue not empty:
       - Dequeue process from front
       - Move to RUNNING state
       - Execute for min(time_quantum, remaining_time)
       - Update current_time
       - Record in Gantt chart
       
       If process complete:
           - Move to TERMINATED
           - Calculate turnaround_time
           - Record completion statistics
       Else:
           - Enqueue at back of ready_queue
   ```

3. **Gantt Chart Generation**
   - Visual representation of process execution
   - Shows which process ran at which time intervals
   
   **Example Output:**
   ```
   Gantt Chart:
   P1000 | P1001 | P1002 | P1003 | P1004 | P1000 | P1001 | ...
   0     5      10     15     20     25     30     35     ...
   ```

### Performance Metrics

After scheduling completes:

| Metric | Calculation | Example |
|--------|-------------|---------|
| Turnaround Time | end_time - arrival_time | 45ms |
| Wait Time | turnaround_time - burst_time | 15ms |
| Average Turnaround | Sum of all turnaround / num_processes | 35ms |

---

## Memory Management Strategy

### Algorithm: Fixed Partitioning with First-Fit Allocation

### Memory Layout

```
System Memory: 700 units total
┌─────────────┐
│ Partition 1 │ 100 units
├─────────────┤
│ Partition 2 │ 150 units
├─────────────┤
│ Partition 3 │ 200 units
├─────────────┤
│ Partition 4 │ 250 units
└─────────────┘
```

### Allocation Strategy

**First-Fit Algorithm:**
```python
def allocate_memory(self, process):
    for partition in self.partitions:
        if not partition['allocated'] and \
           partition['size'] >= process.memory_required:
            
            partition['allocated'] = True
            partition['process_pid'] = process.pid
            process.memory_allocated = process.memory_required
            return True
    return False
```

### Allocation Flow

1. **Process Creation Request**
   - Memory requirement specified
   - System scans partitions from first to last

2. **Partition Search**
   - Find first partition that is:
     - Not allocated to another process
     - Large enough for process

3. **Allocation**
   - Mark partition as allocated
   - Assign process PID to partition
   - Update process memory_allocated field

4. **Deallocation**
   - When process terminates
   - Partition marked as free
   - Available for future allocations

### Memory Map Display

```
Memory Map:
[P1002:100] [Free:150] [P1001:200] [P1003:250]
Memory Usage: 550/700 (78.6%)
```

### Fragmentation Handling

- **Internal Fragmentation**: Occurs when allocated partition > process requirement
  - Example: Process needs 80 units, allocated 100 units, 20 units wasted
  - Trade-off: Simple allocation vs. wasted memory

- **External Fragmentation**: Not possible with fixed partitioning
  - Partitions fixed, no coalescing needed

---

## File System Simulation

### In-Memory File System

Files stored in dictionary (no actual disk access):

```python
self.files = {
    'filename': File_object,
    'system.log': File_object,
    ...
}
```

### File Class Structure

```python
class File:
    filename: str          # File name
    content: str          # File content
    size: int             # Content size in bytes
    created_at: datetime  # Creation timestamp
    modified_at: datetime # Last modification timestamp
```

### File Operations

#### 1. Create File

```
Operation: CREATE
Input: filename, content
Process:
  1. Check if file already exists
  2. If not exists:
     - Create new File object
     - Store in files dictionary
     - Return success
```

#### 2. Delete File

```
Operation: DELETE
Input: filename
Constraints:
  - Cannot delete system files (system.log, readme.txt)
  - Only user files can be deleted
Process:
  1. Check if file exists
  2. Check if not system file
  3. If valid:
     - Remove from files dictionary
     - Return success
```

#### 3. Read File

```
Operation: READ
Input: filename
Process:
  1. Check if file exists
  2. If exists:
     - Return file content
     - Update accessed_at timestamp
```

#### 4. Write File

```
Operation: WRITE
Input: filename, content
Process:
  1. Check if file exists
  2. If exists:
     - Replace content
     - Update size
     - Update modified_at timestamp
```

### Sample File Operations

```
System Files (Protected):
├── system.log      "System log file created"
└── readme.txt      "Welcome to SimpleOS!"

User Files (Created/Managed):
├── document.txt
├── data.csv
└── notes.md
```

---

## I/O Device Handling

### Device: Network Printer

#### PrintJob Class

```python
class PrintJob:
    process_pid: int          # Source process ID
    job_id: int              # Unique job identifier
    data: str                # Print data
    status: str              # "pending", "printing", "completed"
    created_at: datetime     # When job was queued
```

### Printer Queue Management

#### FIFO Queue Implementation

```python
class IOManager:
    printer_queue: deque()      # Queue of pending jobs
    current_job: PrintJob       # Currently printing job
    completed_jobs: list        # Completed job history
```

### I/O Operation Flow

#### 1. Send Print Job

```
Process: Process sends print request
├── Check: Queue not full (max 20 jobs)
├── If space available:
│   ├── Create PrintJob object
│   ├── Assign job_id
│   ├── Add to printer_queue
│   └── Status = "pending"
└── If queue full:
    └── Reject request, process may wait
```

#### 2. Process Print Job

```
Process: Printer processes next job
├── Complete current job (if any)
│   ├── Update status = "completed"
│   └── Move to completed_jobs list
├── Dequeue next job from printer_queue
│   ├── Update status = "printing"
│   └── Simulate printing
```

### Example Printer Session

```
Step 1: Process P1000 sends print job
  Input data: "Document_Quarterly_Report_2026.pdf"
  Output: "✓ Print job queued from P1000"

Step 2: View printer status
  Currently printing: (None)
  Pending Jobs (1):
    - Job 1 (P1000): Document_Quarterly_Report_2026...
  Completed Jobs: 0

Step 3: Process next job
  Output: "✓ Job 1 completed!"

Step 4: View updated status
  Currently printing: (None)
  Pending Jobs: (None)
  Completed Jobs: 1
```

---

## Sample Execution

### Complete System Workflow

#### Scenario: 5 Processes, Round Robin Scheduling

**Initial Conditions:**
```
Total Memory: 700 units
Time Quantum: 5ms
Processes:
  - Chrome        (burst: 25ms, memory: 120)
  - Code Editor   (burst: 30ms, memory: 150)
  - File Manager  (burst: 15ms, memory: 80)
  - Notepad       (burst: 20ms, memory: 60)
  - Calculator    (burst: 10ms, memory: 40)
```

**Step 1: Memory Allocation**

```
Allocation Process (First-Fit):

Process P1000 (Chrome, 120 units)
  ├── Check Partition 1 (100 units) - Too small
  ├── Check Partition 2 (150 units) - Allocate ✓
  
Process P1001 (Code Editor, 150 units)
  ├── Check Partition 1 (100 units) - Too small
  ├── Check Partition 3 (200 units) - Allocate ✓

Process P1002 (File Manager, 80 units)
  ├── Check Partition 1 (100 units) - Allocate ✓

Process P1003 (Notepad, 60 units)
  ├── Check Partition 4 (250 units) - Allocate ✓

Process P1004 (Calculator, 40 units)
  ├── All partitions allocated
  └── Allocation fails (memory insufficient)

Memory Map After Allocation:
[P1002:100] [P1000:150] [P1001:200] [P1003:250]
Memory Usage: 700/700 (100.0%)
```

**Step 2: CPU Scheduling (Round Robin, Quantum=5ms)**

```
Queue State at Start: [P1000, P1001, P1002, P1003, P1004]

Timeline:
Time 0-5:   P1000 executes (Chrome)
            - Remaining: 25 - 5 = 20ms
            - Enqueue back: [P1001, P1002, P1003, P1004, P1000]

Time 5-10:  P1001 executes (Code Editor)
            - Remaining: 30 - 5 = 25ms
            - Enqueue back: [P1002, P1003, P1004, P1000, P1001]

Time 10-15: P1002 executes (File Manager)
            - Remaining: 15 - 5 = 10ms
            - Enqueue back: [P1003, P1004, P1000, P1001, P1002]

Time 15-20: P1003 executes (Notepad)
            - Remaining: 20 - 5 = 15ms
            - Enqueue back: [P1004, P1000, P1001, P1002, P1003]

Time 20-25: P1004 executes (Calculator)
            - Remaining: 10 - 5 = 5ms
            - Enqueue back: [P1000, P1001, P1002, P1003, P1004]

Time 25-30: P1000 executes (Chrome)
            - Remaining: 20 - 5 = 15ms
            - Enqueue back: [P1001, P1002, P1003, P1004, P1000]

... (continues until all processes complete)

Time 95-100: P1001 executes (Code Editor)
            - Remaining: 5 - 5 = 0ms
            - TERMINATE ✓

Final time: 100ms
```

**Step 3: Gantt Chart Display**

```
Gantt Chart:
P1000 | P1001 | P1002 | P1003 | P1004 | P1000 | P1001 | P1002 | P1003 | P1004 | P1000 | P1001 | P1002 | P1003 | P1000 | P1001 | P1003 | P1000 | P1001 | P1001
0     5      10     15     20     25     30     35     40     45     50     55     60     65     70     75     80     85     90     95     100
```

**Step 4: Execution Summary**

```
Scheduling Results:
─────────────────────────────────────────────────────────────────────
PID      Name                 Burst Time   Turnaround   Wait Time
─────────────────────────────────────────────────────────────────────
1000     Chrome               25           50           25
1001     Code Editor          30           65           35
1002     File Manager         15           40           25
1003     Notepad              20           50           30
─────────────────────────────────────────────────────────────────────
Average Turnaround Time: 51.25ms
```

**Step 5: I/O Operations**

```
Send Print Job:
  Source PID: 1000 (Chrome)
  Data: "Document_Quarterly_Report_2026.pdf"
  Result: ✓ Print job queued

Printer Queue Status:
  Currently printing: (None)
  Pending Jobs (1):
    - Job 1 (P1000): Document_Quarterly_Report_2026...
  Completed Jobs: 0

Process Job:
  Job 1 completed!

Updated Status:
  Currently printing: (None)
  Pending Jobs: (None)
  Completed Jobs: 1
```

---

## Features & Usage

### Main Menu Options

```
==================================================
SIMPLE OS DESKTOP
=================================================

1. Task Manager
2. File Explorer
3. Memory Manager
4. CPU Scheduler
5. I/O Devices (Printer)
6. System Settings
7. Shutdown
```

### Task Manager Features

```
TASK MANAGER
├── 1. View All Processes
│   └── Display table with: PID, Name, State, Burst, Memory, Progress
├── 2. Create New Process
│   ├── Input: process name, burst time, memory required
│   └── Action: Create and allocate memory
├── 3. Terminate Process
│   ├── Input: Process ID
│   └── Action: Free memory and mark TERMINATED
└── 4. View Process Details
    ├── Input: Process ID
    └── Display: All process metrics
```

### File Explorer Features

```
FILE EXPLORER
├── 1. List Files
│   └── Show all files with sizes and timestamps
├── 2. Create File
│   ├── Input: filename, content
│   └── Action: Add to file system
├── 3. Delete File
│   ├── Input: filename
│   └── Constraint: Cannot delete system files
├── 4. View File Content
│   ├── Input: filename
│   └── Display: File content
└── 5. Edit File
    ├── Input: filename, new content
    └── Action: Update file
```

### Memory Manager Features

```
MEMORY MANAGER
├── 1. View Memory Status
│   └── Show: Total, Used, Free, Percentage
├── 2. Allocate Memory
│   ├── Manual allocation to specific process
│   └── Uses First-Fit algorithm
├── 3. Deallocate Memory
│   ├── Manual deallocation
│   └── Frees up partition
└── 4. View Memory Map
    └── Visual representation of partitions
```

### CPU Scheduler Features

```
CPU SCHEDULER
├── 1. Run Scheduling Algorithm
│   └── Execute Round Robin scheduling on all processes
├── 2. View Scheduling Results
│   ├── Display: PID, Name, Burst, Turnaround, Wait Time
│   └── Generate: Gantt chart
└── 3. Set Time Quantum
    └── Change scheduling time slice (1-50ms)
```

### I/O Devices Features

```
I/O DEVICES (PRINTER)
├── 1. Send Print Job
│   ├── Input: source PID, data
│   └── Action: Queue job for printing
├── 2. View Printer Queue
│   ├── Display: current job, pending jobs, completed jobs
│   └── Shows job details and status
├── 3. Process Next Job
│   ├── Move current job to completed
│   └── Dequeue next pending job
└── 4. View Job History
    └── List all completed print jobs
```

---

## Command-Mode Interface (Future Enhancement)

While the current system uses interactive menus, future versions could support command-line input:

```bash
> create process Chrome 25 120
✓ Process P1000 created

> run scheduler
✓ Scheduling complete (100ms)

> delete file document.txt
✓ File deleted

> send print job P1000 "data.pdf"
✓ Print job queued
```

---

## Performance Characteristics

### Time Complexity

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Process Creation | O(1) | Direct PID assignment |
| Memory Allocation | O(n) | n = number of partitions (4) |
| Scheduling | O(n²) | n = number of processes |
| File Operations | O(1) | Dictionary lookup |
| Print Job Queue | O(1) | Deque operations |

### Space Complexity

| Component | Complexity | Max Size |
|-----------|-----------|----------|
| Process Table | O(n) | 128 processes |
| Memory Map | O(1) | 4 partitions |
| File System | O(f) | 1000 files |
| Print Queue | O(j) | 20 jobs |

---

## System Limitations & Improvements

### Current Limitations

1. **Fixed Memory Partitioning**
   - Potential internal fragmentation
   - No dynamic partition sizing

2. **Single CPU Scheduling Algorithm**
   - Only Round Robin implemented
   - No priority-based scheduling

3. **Simple I/O Management**
   - Only printer supported
   - No disk I/O simulation

4. **No Inter-Process Communication**
   - Processes isolated
   - No IPC mechanisms

### Future Enhancements

1. **Additional Scheduling Algorithms**
   - Priority-based scheduling
   - Multi-Level Feedback Queues (MLFQ)

2. **Advanced Memory Management**
   - Virtual memory simulation
   - Page replacement algorithms
   - Demand paging

3. **Extended I/O Simulation**
   - Disk I/O with seek time calculation
   - Multiple device support
   - Device drivers

4. **Network Simulation**
   - Inter-process communication
   - Message passing
   - Shared memory

5. **Persistence**
   - Save/load system state
   - Audit logging
   - Performance statistics

---

## Conclusion

SimpleOS provides a comprehensive educational platform for understanding operating system concepts. Through hands-on interaction with process management, CPU scheduling, memory allocation, file handling, and I/O operations, users gain practical insight into how real operating systems function.

The modular architecture allows for easy extension and modification, making it ideal for learning and experimentation in OS courses.

---

## References

- Operating System Concepts by Silberschatz, Galvin, Gagne
- Modern Operating Systems by Andrew S. Tanenbaum
- CPU Scheduling Algorithms: Round Robin, FCFS, Priority
- Memory Management: Partitioning, Paging, Segmentation
- I/O Management: Device Queuing and Scheduling

---

**Version**: 1.0  
**Author**: CMSC 314 Students  
**Last Updated**: April 2026
