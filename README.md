# Simple Operating System Simulator - Web Edition
## CMSC 314 Final Project

A fully-functional web-based Operating System Simulator that demonstrates core OS concepts including process management, CPU scheduling, memory management, file systems, and I/O operations.

---

## Features

### ✅ Process Management
- Create and manage multiple processes
- Display process states: Ready, Running, Waiting, Terminated
- Track process metadata (PID, burst time, memory requirements)
- Real-time process table

### ✅ CPU Scheduling
- **Round Robin Algorithm** with configurable time quantum (5ms)
- Visual Gantt chart showing execution timeline
- Track process execution order and timing
- Ready queue management

### ✅ Memory Management
- Fixed memory partitions (4 partitions × 256 MB each = 1024 MB)
- Dynamic memory allocation/deallocation to processes
- Visual memory map showing partition status
- Free/allocated memory tracking

### ✅ File System
- Create, delete, read files
- File metadata (creation time, size)
- Simple file operations without actual disk access
- Pre-initialized system files

### ✅ I/O Simulation
- Printer device simulation
- I/O request queue (basic spooling)
- Request completion tracking
- Process-to-device communication

### 🎨 Beautiful Web UI
- Modern, responsive design
- Dark gradient theme with purple accents
- Interactive modals for detailed views
- Real-time status updates
- Mobile-friendly layout

---

## Installation & Setup

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Access the Web Interface
Open your browser and navigate to:
```
http://localhost:8001
```

---

## Usage Guide

### Quick Start
1. Click **"Load Sample Processes"** to automatically create 3 sample processes
2. Click **"Run Full Simulation"** to execute the complete simulation (30 cycles)
3. View results in the Gantt chart, memory map, and I/O status

### Create Custom Process
1. Fill in the process details:
   - **Process Name**: Name of the process (e.g., P1)
   - **Burst Time**: CPU time needed (in milliseconds)
   - **Memory Required**: Memory allocation needed (64-1024 MB)
   - **I/O Operations**: Number of I/O requests
2. Click **"Create Process"** to add the process

### Run Simulation
- **Run One Step**: Execute a single scheduling cycle
- **Run Full Simulation**: Execute 30 complete scheduling cycles

### Manage Files
- **Create Tab**: Create new files with content
- **Files Tab**: View all files, read content, or delete files

### View Details
- Click **"View Processes"** to see all process details in a table
- Click **"Detailed Memory Map"** to see partition breakdown
- Click **"View I/O Details"** to see I/O queue and completed requests
- Click **"View Full Chart"** for detailed Gantt chart

### Reset
- Click **"Reset Simulation"** to clear all processes and start fresh

---

## Project Structure

```
CMSC_314/
├── app.py                 # Flask backend with OS simulator logic
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── templates/
    └── index.html        # Web UI (HTML + CSS + JavaScript)
```

---

## Technical Details

### Backend (Python/Flask)
- **app.py**: Contains all OS simulator classes and Flask routes
  - `ProcessState`: Enum for process states
  - `Process`: Process class with execution logic
  - `CPUScheduler`: Round Robin scheduler implementation
  - `MemoryManager`: Fixed partition memory management
  - `File` & `FileSystem`: File system simulation
  - `IODevice`: I/O device with queue simulation
  - `OSSimulator`: Main coordinator class

### Frontend (HTML/CSS/JavaScript)
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Updates**: Auto-refresh status every 5 seconds
- **Interactive Modals**: Detailed views for processes, memory, and I/O
- **API Communication**: Uses fetch() for async communication

### API Endpoints
- `GET /` - Main web interface
- `POST /api/create-process` - Create new process
- `POST /api/step` - Execute one scheduling cycle
- `POST /api/run-simulation` - Run full simulation
- `GET /api/get-status` - Get current system status
- `POST /api/reset` - Reset simulator
- `GET /api/files` - Get all files
- `POST /api/create-file` - Create file
- `POST /api/delete-file` - Delete file
- `POST /api/read-file` - Read file contents

---

## OS Concepts Demonstrated

1. **Process Management**: 
   - Process creation and state transitions
   - PID assignment and tracking
   - Process metadata management

2. **CPU Scheduling**:
   - Round Robin algorithm
   - Time quantum-based preemption
   - Ready queue management
   - Execution timeline visualization

3. **Memory Management**:
   - Fixed partition allocation
   - Partition fragmentation avoidance
   - Memory allocation/deallocation
   - Memory utilization tracking

4. **File System**:
   - File creation and deletion
   - File metadata
   - Simple file operations
   - Directory structure simulation

5. **I/O Management**:
   - I/O request queuing
   - Device simulation
   - Process-device synchronization
   - Request completion tracking

---

## Sample Output

When you load sample processes and run the simulation, you'll see:

1. **Process Table**: Shows all processes with PID, name, state, remaining time, and memory allocation
2. **Gantt Chart**: Visual timeline of process execution (e.g., [P1][P2][P3][P1][P2]...)
3. **Memory Map**: Shows which partitions are allocated/free and which process uses them
4. **I/O Status**: Displays queue size, completed requests, and pending I/O operations
5. **File System**: Lists all files with creation time and size

---

## Customization

### Change Time Quantum
Edit in `app.py`:
```python
self.scheduler = CPUScheduler(time_quantum=10)  # Change from 5 to 10
```

### Adjust Total Memory
Edit in `app.py`:
```python
self.memory_manager = MemoryManager(total_memory=2048)  # Change from 1024 to 2048
```

### Change I/O Device Name
Edit in `app.py`:
```python
self.io_device = IODevice("Disk")  # Change from "Printer" to "Disk"
```

---

## Troubleshooting

### Port Already in Use
If the default port is busy, edit the launch configuration or set `PUSOYOS_PORT`:
```python
app.run(debug=True, port=8001)  # Clean default port
```

### Flask Not Found
Install Flask:
```bash
pip install Flask==2.3.0
```

### Browser Can't Connect
- Make sure Flask server is running: `python app.py`
- Check that you're accessing: `http://localhost:8001`
- Check terminal for any error messages

---

## Future Enhancements

- Multiple scheduling algorithms (FCFS, Priority Queue, SJF)
- Multiple I/O devices
- Virtual memory simulation
- Page replacement algorithms
- Fork/join process operations
- Signal handling simulation

---

## Author

Created for CMSC 314: Operating Systems
Final Project - 2026

---

## License

Educational Use Only - CMSC 314 Course Project
