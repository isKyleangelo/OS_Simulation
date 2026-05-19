# SimpleOS Quick Start Guide

A step-by-step guide to getting started with SimpleOS and understanding its core features.

---

## Installation & First Run

### Step 1: Navigate to Project Directory

```bash
cd c:\Users\kyleski\OneDrive\Desktop\CMSC_314
```

### Step 2: Run the Simulator

```bash
python os_cli.py
```

### Step 3: You should see the boot sequence

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

Press Enter to continue...
```

Press **Enter** to proceed to the main desktop.

---

## Main Desktop Menu

After boot, you'll see:

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

--------------------------------------------------
Enter option: 
```

---

## Feature Walkthrough

### Feature 1: Task Manager (Option 1)

#### What it does:
- View running processes
- Create new processes
- Terminate processes
- View process details

#### Try this:

```
Main Menu > 1 (Task Manager)

TASK MANAGER
==================================================

1. View All Processes
2. Create New Process
3. Terminate Process
4. View Process Details
5. Back to Desktop

--------------------------------------------------
Enter option: 1
```

**Expected Output**:
```
RUNNING PROCESSES
==================================================

PID      Name                 State        Burst      Memory      Progress
---------------------------------------------------------------------------
1000     Chrome               NEW          25         0           0.0%
1001     Code Editor          NEW          30         0           0.0%
1002     File Manager         NEW          15         0           0.0%
1003     Notepad              NEW          20         0           0.0%
1004     Calculator           NEW          10         0           0.0%

---------------------------------------------------------------------------
Press Enter to continue...
```

#### Create a New Process

```
Enter option: 2
Enter process name: MyApp
Enter burst time (ms): 50
Enter memory required (units): 100

✓ Process created: P1005 - MyApp
  Memory allocated: 100 units

Press Enter to continue...
```

### Feature 2: File Explorer (Option 2)

#### What it does:
- List files in the system
- Create new files
- Delete files
- View file contents
- Edit files

#### Try this:

```
Main Menu > 2 (File Explorer)

FILE EXPLORER
==================================================

1. List Files
2. Create File
3. Delete File
4. View File Content
5. Edit File
6. Back to Desktop

--------------------------------------------------
Enter option: 1
```

**Expected Output**:
```
FILE LIST
==================================================

  Files:
  1. system.log (29 bytes)
     Created: 2026-04-29 22:52:03
  2. readme.txt (20 bytes)
     Created: 2026-04-29 22:52:03

--------------------------------------------------
Press Enter to continue...
```

#### Create a New File

```
Enter option: 2

CREATE FILE
==================================================

Enter filename: notes.txt
Enter content (or 'skip' for empty): My important notes

✓ File created: notes.txt

Press Enter to continue...
```

### Feature 3: Memory Manager (Option 3)

#### What it does:
- View memory status
- Allocate memory manually
- Deallocate memory
- View memory map

#### Try this:

```
Main Menu > 3 (Memory Manager)

MEMORY MANAGER
==================================================

1. View Memory Status
2. Allocate Memory
3. Deallocate Memory
4. View Memory Map
5. Back to Desktop

--------------------------------------------------
Enter option: 4
```

**Expected Output**:
```
MEMORY MAP
==================================================

  Memory Map:
  [P1002:100] [P1000:150] [P1001:200] [P1003:250]
  Memory Usage: 700/700 (100.0%)

--------------------------------------------------
Press Enter to continue...
```

### Feature 4: CPU Scheduler (Option 4)

#### What it does:
- Execute Round Robin scheduling
- View scheduling results
- Set custom time quantum
- Display Gantt chart

#### Try this:

```
Main Menu > 4 (CPU Scheduler)

CPU SCHEDULER - ROUND ROBIN
==================================================

1. Run Scheduling Algorithm (Quantum: 5ms)
2. View Scheduling Results
3. Set Time Quantum
4. Back to Desktop

--------------------------------------------------
Enter option: 1

RUNNING ROUND ROBIN SCHEDULING
==================================================

  Allocating memory to processes...
  Starting CPU execution...

  Time 0-5: Chrome (PID: 1000)
  Time 5-10: Code Editor (PID: 1001)
  Time 10-15: File Manager (PID: 1002)
  Time 15-20: Notepad (PID: 1003)
  Time 20-25: Calculator (PID: 1004)
  Time 25-30: Chrome (PID: 1000)
  ...
  Time 95-100: Code Editor (PID: 1001)

  Scheduling complete!
  Total time: 100ms

Press Enter to continue...
```

#### View Results

```
Enter option: 2

SCHEDULING RESULTS
==================================================

Execution Summary:

PID      Name                 Burst Time   Turnaround   Wait Time
---------------------------------------------------------------------------
1000     Chrome               25           50           25
1001     Code Editor          30           65           35
1002     File Manager         15           40           25
1003     Notepad              20           50           30
---------------------------------------------------------------------------
Average Turnaround Time: 51.25ms

  Gantt Chart:
  P1000 | P1001 | P1002 | P1003 | P1004 | P1000 | P1001 | P1002 | P1003 | P1004 | P1000 | P1001 | P1002 | P1003 | P1000 | P1001 | P1003 | P1000 | P1001 | P1001
  0 5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95 100

--------------------------------------------------
Press Enter to continue...
```

### Feature 5: I/O Devices - Printer (Option 5)

#### What it does:
- Send print jobs
- View printer queue
- Process print jobs
- View job history

#### Try this:

```
Main Menu > 5 (I/O Devices)

I/O DEVICES - PRINTER MANAGEMENT
==================================================

1. Send Print Job
2. View Printer Queue
3. Process Next Job
4. View Job History
5. Back to Desktop

--------------------------------------------------
Enter option: 1

SEND PRINT JOB
==================================================

RUNNING PROCESSES
==================================================

PID      Name                 State        Burst      Memory      Progress
---------------------------------------------------------------------------
1000     Chrome               TERMINATED   25         150         100.0%
1001     Code Editor          TERMINATED   30         200         100.0%
1002     File Manager         TERMINATED   15         100         100.0%
1003     Notepad              TERMINATED   20         250         100.0%
1004     Calculator           TERMINATED   10         0           100.0%

---------------------------------------------------------------------------

Enter source PID: 1000
Enter print data: Document_Quarterly_Report_2026.pdf

✓ Print job queued from P1000

Press Enter to continue...
```

#### View Printer Queue

```
Enter option: 2

PRINTER QUEUE
==================================================

  Printer Queue Status:
  Currently printing: (None)

  Pending Jobs (1):
    - Job 1 (P1000): Document_Quarterly_Report_2026...

  Completed Jobs: 0

--------------------------------------------------
Press Enter to continue...
```

#### Process Print Job

```
Enter option: 3

PROCESS PRINTER JOB
==================================================

✓ Job 1 completed!
  Data: Document_Quarterly_Report_2026.pdf

Press Enter to continue...
```

### Feature 6: System Settings (Option 6)

```
Main Menu > 6 (System Settings)

SYSTEM SETTINGS
==================================================

  System Information:
  └─ System Name: SimpleOS
  └─ Version: 1.0
  └─ Kernel: SimpleOS Kernel 1.0
  └─ CPU Cores: 4
  └─ Total Memory: 700 units
  └─ Boot Time: 2026-04-29 22:52:03

  Configuration:
  └─ Time Quantum: 5ms
  └─ Memory Partitions: 4
  └─ Total Processes: 5

--------------------------------------------------
Press Enter to continue...
```

---

## Complete Workflow Example

### Scenario: Run a full OS simulation

**Step 1**: Start SimpleOS

```bash
python os_cli.py
Press Enter
```

**Step 2**: View initial processes

```
Main Menu > 1 > 1
```

Check that 5 sample processes exist (Chrome, Code Editor, etc.)

**Step 3**: Create a new process

```
Main Menu > 1 > 2
Name: CustomApp
Burst Time: 40
Memory: 80
Result: Process created but memory not allocated (full)
```

**Step 4**: View memory map

```
Main Menu > 3 > 4
Result: All 700 memory units allocated
```

**Step 5**: Run CPU scheduler

```
Main Menu > 4 > 1
Result: All processes execute in round robin order
```

**Step 6**: View scheduling results

```
Main Menu > 4 > 2
Result: Gantt chart and performance metrics displayed
```

**Step 7**: Create a file

```
Main Menu > 2 > 2
Name: results.txt
Content: Scheduling completed successfully
```

**Step 8**: Send print job

```
Main Menu > 5 > 1
PID: 1000
Data: Result_Summary.pdf
```

**Step 9**: Process print job

```
Main Menu > 5 > 3
Result: Job completed
```

**Step 10**: Shutdown

```
Main Menu > 7
Result: System shuts down gracefully
```

---

## Tips & Tricks

### Tip 1: Memory Management

- Memory is limited (700 units total)
- Partitions are fixed: [100, 150, 200, 250]
- Use First-Fit allocation (first suitable partition)
- Deallocate processes to free memory

### Tip 2: CPU Scheduling

- Default time quantum: 5ms
- Change time quantum to see different scheduling behavior
- Smaller quantum = more context switches, higher overhead
- Larger quantum = less responsive, less overhead

### Tip 3: File Operations

- System files (system.log, readme.txt) cannot be deleted
- File size increases with content length
- File operations are O(1) - instant lookup

### Tip 4: Printer Queue

- Maximum 20 jobs in printer queue
- Jobs processed in FIFO order
- Cannot exceed queue limit

### Tip 5: Process Lifecycle

- NEW → READY → RUNNING → TERMINATED
- New processes start with 0 memory allocated
- Memory allocated during scheduling
- Processes use up all their burst time

---

## Common Tasks

### Task 1: Create and Schedule Processes

```
1. Main Menu > 1 > 1 (View processes)
2. Main Menu > 1 > 2 (Create new)
3. Main Menu > 4 > 1 (Run scheduler)
4. Main Menu > 4 > 2 (View results)
```

### Task 2: Manage Files

```
1. Main Menu > 2 > 1 (List files)
2. Main Menu > 2 > 2 (Create file)
3. Main Menu > 2 > 4 (View content)
4. Main Menu > 2 > 5 (Edit file)
```

### Task 3: Monitor Memory

```
1. Main Menu > 3 > 1 (Check status)
2. Main Menu > 3 > 4 (View map)
3. Main Menu > 1 > 1 (Check process memory)
```

### Task 4: Simulate Printing

```
1. Main Menu > 5 > 1 (Queue job)
2. Main Menu > 5 > 2 (View queue)
3. Main Menu > 5 > 3 (Process job)
4. Main Menu > 5 > 4 (View history)
```

---

## Understanding the Output

### Process State Values

| State | Meaning |
|-------|---------|
| NEW | Process created, not started |
| READY | Ready to run, waiting for CPU |
| RUNNING | Currently executing |
| WAITING | Waiting for I/O |
| TERMINATED | Completed |

### Memory Display

```
[P1000:120] = Process 1000 using 120 units
[Free:150]  = 150 units available
```

### Gantt Chart

```
P1000 | P1001 | P1000
0     5      10     15

Process  | Time Slice | Cumulative Time
```

---

## Troubleshooting

### Q: I get "Insufficient memory" when creating process

**A**: All memory partitions are allocated. Either:
1. Terminate existing processes first
2. Reduce memory requirement of new process
3. View memory map to see allocations

### Q: Scheduling doesn't start processes

**A**: Processes must have memory allocated first. The scheduler automatically does this, but ensure:
1. Processes exist (check Task Manager)
2. Memory is available
3. Run from CPU Scheduler menu

### Q: Can't delete a file

**A**: System files cannot be deleted:
- system.log
- readme.txt

Only user-created files can be deleted.

### Q: Print queue is full

**A**: Maximum 20 jobs allowed. Process some jobs first before sending new ones.

---

## Performance Tips

### Faster Scheduling
- Increase time quantum to reduce context switches
- Fewer context switches = less overhead
- But reduces responsiveness

### Better Memory Utilization
- Deallocate processes you don't need
- Monitor memory map to find fragmentation
- Consider process size when creating new processes

### Efficient File Operations
- Use short filenames
- Avoid very large file content
- Delete temporary files to keep system clean

---

## Next Steps

1. **Explore all features** - Try each menu option
2. **Create custom processes** - Experiment with different burst times
3. **Modify time quantum** - See how it affects scheduling
4. **Study the code** - Read implementation in `os_cli.py`
5. **Extend the system** - Add new features or algorithms

---

## For More Information

See these files in the project:
- `OS_SIMULATOR_README.md` - Detailed system documentation
- `IMPLEMENTATION_GUIDE.md` - Code architecture and design patterns
- `os_cli.py` - Complete source code

---

**Enjoy exploring SimpleOS!** 🎉

Version 1.0 | April 2026
