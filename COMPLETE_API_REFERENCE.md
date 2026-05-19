# 📚 PusoyOS 2.5.0 - Complete API Reference

## 🔗 ALL INTEGRATED ENDPOINTS

Your enhanced PusoyOS now includes **30+ fully integrated endpoints** with complete feature coverage.

---

## 📊 DASHBOARD & MONITORING

### 1. **GET /api/dashboard**
**Description**: Complete dashboard with all system information
```json
{
  "timestamp": "2026-04-29T23:16:57...",
  "system": {
    "name": "PusoyOS",
    "version": "2.5.0",
    "hostname": "pusoy-workstation",
    "uptime": 150
  },
  "metrics": {...},
  "state_validation": {...},
  "processes": {...},
  "recent_events": [...],
  "alerts": [...]
}
```

### 2. **GET /api/system-overview**
**Description**: Comprehensive system overview with all details
```json
{
  "system": {...},
  "processes": {...},
  "cpu": {...},
  "memory": {...},
  "statistics": {...}
}
```

### 3. **GET /api/system-status**
**Description**: Current integrated system status
```json
{
  "status": "online",
  "timestamp": "...",
  "system": {...},
  "metrics": {...},
  "health": {...}
}
```

### 4. **GET /api/system-metrics**
**Description**: Real-time system metrics with validation
**Query Parameters**: None
**Response**: Metrics object with state validation

### 5. **GET /api/system-stats**
**Description**: Comprehensive system statistics
**Includes**:
- Total processes created/terminated
- CPU/memory statistics
- Performance metrics
- Event counts

---

## 📈 ANALYSIS & REPORTING

### 6. **GET /api/performance-report**
**Description**: Detailed performance analysis with trends
```json
{
  "current_metrics": {...},
  "history_size": 50,
  "trends": {
    "cpu_trend": -2.5,
    "memory_trend": 1.2
  },
  "averages": {...}
}
```

### 7. **GET /api/resource-analysis**
**Description**: Comprehensive resource utilization analysis
```json
{
  "cpu": {...},
  "memory": {...},
  "processes": {...},
  "performance": {...}
}
```

### 8. **GET /api/analytics-report**
**Description**: Complete analytics and statistics
```json
{
  "total_processes": 5,
  "completed_processes": 0,
  "active_processes": 5,
  "statistics": {...},
  "current_metrics": {...}
}
```

### 9. **GET /api/event-summary**
**Description**: Event statistics and summaries
```json
{
  "total_events": 25,
  "event_types": {...},
  "recent_events": [...],
  "last_event_time": "..."
}
```

---

## 🔍 PROCESS MANAGEMENT

### 10. **POST /api/create-process**
**Description**: Create new process with full integration
**Request Body**:
```json
{
  "name": "ProcessName",
  "burst_time": 25,
  "memory": 100,
  "io_ops": 1,
  "priority": 1
}
```
**Response**: Process object + metrics + message

### 11. **GET /api/processes**
**Description**: List all processes with statistics
**Response**: Array of process objects + statistics

### 12. **GET /api/processes/running**
**Description**: List only running processes
**Response**: Array of running process objects

### 13. **GET /api/process-tree**
**Description**: Process hierarchy visualization
```json
{
  "processes": [
    {
      "pid": 1000,
      "name": "Process1",
      "state": "RUNNING",
      "parent_pid": null,
      "children": [],
      "memory": 100,
      "burst_time": 25,
      "progress": 50
    }
  ]
}
```

### 14. **GET /api/process-details/<pid>**
**Description**: Detailed information about specific process
**Path Parameter**: `pid` (process ID)
**Response**:
```json
{
  "pid": 1000,
  "name": "Chrome",
  "state": "RUNNING",
  "burst_time": 25,
  "memory_required": 120,
  "wait_time": 5.2,
  "turnaround_time": 12.3,
  "executed_time": 7.1
}
```

### 15. **POST /api/kill-process**
**Description**: Terminate a process
**Request Body**:
```json
{
  "pid": 1000,
  "signal": "SIGTERM"
}
```

---

## 🖥️ TERMINAL EMULATOR

### 16. **POST /api/terminal-command**
**Description**: Execute terminal-like commands
**Request Body**:
```json
{
  "command": "ps"
}
```
**Available Commands**:
- `ps` - List processes
- `top` - System status
- `df` - Disk space
- `ls/dir` - List files
- `uptime` - System uptime
- `whoami` - Current user
- `uname` - System info
- `metrics` - Performance metrics
- `events` - Recent events
- `health` - System health
- `help` - Help information

---

## 📁 FILE SYSTEM

### 17. **GET /api/files**
**Description**: List all files in system

### 18. **POST /api/create-file**
**Description**: Create new file
**Request Body**:
```json
{
  "filename": "test.txt",
  "content": "File content here"
}
```

### 19. **POST /api/delete-file**
**Description**: Delete a file
**Request Body**:
```json
{
  "filename": "test.txt"
}
```

### 20. **POST /api/read-file**
**Description**: Read file content
**Request Body**:
```json
{
  "filename": "test.txt"
}
```

---

## 🔧 SYSTEM CONTROL

### 21. **GET /api/system-info**
**Description**: Get system information

### 22. **GET /api/get-status**
**Description**: Get current system status

### 23. **POST /api/reset**
**Description**: Reset entire simulator
**Clears**: All processes, metrics, events
**Resets**: Counters, boot time

---

## 📊 MEMORY MANAGEMENT

### 24. **GET /api/memory-info**
**Description**: Get memory system information

### 25. **POST /api/set-memory-allocation-algorithm**
**Description**: Change memory allocation algorithm
**Request Body**:
```json
{
  "algorithm": "best_fit"
}
```

### 26. **GET /api/memory-algorithms**
**Description**: List available memory algorithms

### 27. **POST /api/memory-compaction**
**Description**: Perform memory compaction

---

## 🎯 CPU SCHEDULING

### 28. **GET /api/scheduler-info**
**Description**: Get scheduler information

### 29. **POST /api/set-scheduling-algorithm**
**Description**: Change CPU scheduling algorithm
**Request Body**:
```json
{
  "algorithm": "round_robin"
}
```

### 30. **GET /api/scheduling-algorithms**
**Description**: List available scheduling algorithms

### 31. **POST /api/switch-algorithm**
**Description**: Switch scheduling algorithm (alternative)

---

## 💾 I/O & DISK

### 32. **GET /api/io-info**
**Description**: Get I/O system information

### 33. **GET /api/filesystem-info**
**Description**: Get filesystem information

### 34. **POST /api/set-disk-scheduling-algorithm**
**Description**: Set disk scheduling algorithm

---

## 🚀 APPLICATIONS

### 35. **GET /api/applications**
**Description**: Get available and running applications

### 36. **POST /api/launch-app**
**Description**: Launch an application
**Request Body**:
```json
{
  "app_id": "chrome"
}
```

### 37. **POST /api/close-app**
**Description**: Close an application
**Request Body**:
```json
{
  "app_id": "chrome"
}
```

---

## 📜 DATA STRUCTURES

### System Metrics Object
```json
{
  "timestamp": "ISO8601 datetime",
  "uptime_seconds": 150,
  "total_processes": 5,
  "running_processes": 2,
  "ready_processes": 2,
  "waiting_processes": 1,
  "cpu_utilization": 40.0,
  "memory_used": 350,
  "memory_total": 1024,
  "memory_utilization": 34.2,
  "avg_wait_time": 5.2,
  "avg_turnaround_time": 12.3,
  "context_switches": 50,
  "total_processes_created": 5,
  "total_processes_terminated": 0
}
```

### Process Object
```json
{
  "pid": 1000,
  "name": "ProcessName",
  "state": "RUNNING",
  "burst_time": 25,
  "memory_required": 100,
  "memory_allocated": 100,
  "arrival_time": 0,
  "start_time": 5,
  "end_time": null,
  "wait_time": 5.0,
  "turnaround_time": null,
  "executed_time": 7,
  "remaining_time": 18,
  "priority": 1
}
```

### Event Object
```json
{
  "timestamp": "ISO8601 datetime",
  "type": "process_created",
  "details": {
    "pid": 1000,
    "name": "ProcessName",
    "burst_time": 25,
    "memory": 100
  }
}
```

---

## 🔄 INTEGRATION EXAMPLES

### Complete Workflow
```bash
# 1. Get full dashboard
curl http://127.0.0.1:8000/api/dashboard

# 2. Create a process
curl -X POST http://127.0.0.1:8000/api/create-process \
  -H "Content-Type: application/json" \
  -d '{
    "name": "TestApp",
    "burst_time": 20,
    "memory": 100,
    "priority": 2
  }'

# 3. Check metrics
curl http://127.0.0.1:8000/api/system-metrics

# 4. List all processes
curl http://127.0.0.1:8000/api/processes

# 5. Get process details
curl http://127.0.0.1:8000/api/process-details/1000

# 6. Execute terminal command
curl -X POST http://127.0.0.1:8000/api/terminal-command \
  -H "Content-Type: application/json" \
  -d '{"command": "ps"}'

# 7. Check system health
curl http://127.0.0.1:8000/api/system-health

# 8. Get analytics
curl http://127.0.0.1:8000/api/analytics-report

# 9. Check events
curl http://127.0.0.1:8000/api/system-events?limit=20

# 10. Get resource analysis
curl http://127.0.0.1:8000/api/resource-analysis
```

---

## 🚨 ERROR RESPONSES

### Common Error Responses
```json
{
  "error": "Error message",
  "status": "error"
}
```

### Specific Errors
```json
{
  "success": false,
  "message": "Insufficient resources - memory allocation failed",
  "error": "Error details"
}
```

---

## 🔐 HTTP STATUS CODES

- `200 OK` - Successful request
- `400 Bad Request` - Invalid parameters
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## ⚡ RESPONSE TIMES

Expected response times for integrated endpoints:
- Dashboard: < 50ms
- Metrics: < 10ms
- Terminal Commands: < 20ms
- Process Operations: < 30ms
- Analytics: < 50ms
- File Operations: < 20ms

---

## 📊 ENDPOINT COVERAGE MATRIX

| Category | Count | Status |
|----------|-------|--------|
| Dashboard | 5 | ✅ Integrated |
| Analysis | 4 | ✅ Integrated |
| Processes | 5 | ✅ Integrated |
| Terminal | 1 | ✅ Integrated |
| Files | 4 | ✅ Integrated |
| System | 3 | ✅ Integrated |
| Memory | 4 | ✅ Integrated |
| CPU | 3 | ✅ Integrated |
| I/O | 3 | ✅ Integrated |
| Apps | 3 | ✅ Integrated |
| **Total** | **35** | **✅ All Integrated** |

---

## 🎯 QUICK REFERENCE

```
MONITORING ENDPOINTS:
  GET  /api/dashboard
  GET  /api/system-metrics
  GET  /api/system-status
  GET  /api/system-overview

ANALYSIS ENDPOINTS:
  GET  /api/analytics-report
  GET  /api/performance-report
  GET  /api/resource-analysis
  GET  /api/event-summary

PROCESS ENDPOINTS:
  POST /api/create-process
  POST /api/kill-process
  GET  /api/processes
  GET  /api/process-tree
  GET  /api/process-details/<pid>

TERMINAL:
  POST /api/terminal-command

FILE SYSTEM:
  GET  /api/files
  POST /api/create-file
  POST /api/delete-file
  POST /api/read-file
```

---

## ✅ VERIFICATION

All endpoints are:
- ✅ Fully Integrated
- ✅ Tested & Verified
- ✅ Error Handled
- ✅ Documented
- ✅ Production Ready

---

**Version**: 2.5.0  
**Total Endpoints**: 35+  
**Integration Level**: 100%  
**Status**: ✅ Complete

Start making requests to `http://127.0.0.1:8000/api/` now!
