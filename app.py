"""
PusoyOS - A Complete Operating System Simulator
Educational OS simulation with realistic process management, memory management, scheduling, and I/O

Author: CMSC 314 Students
Version: 2.5.0 - Enhanced Interactive Edition
"""

from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
from collections import deque
from core.simulator import PusoyOSSimulator
from config import HOSTNAME, SYSTEM_NAME, SYSTEM_VERSION

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Disable template caching
app.jinja_env.cache = {}  # Clear Jinja2 cache

# Create global simulator instance
simulator = PusoyOSSimulator()
simulator.is_running = True

# ===========================
# SYSTEM MONITORING & ANALYTICS
# ===========================

# Event logging system
system_events = deque(maxlen=1000)  # Keep last 1000 events
performance_history = deque(maxlen=100)  # Keep last 100 measurements
system_metrics = {
    'total_processes_created': 0,
    'total_processes_terminated': 0,
    'context_switches': 0,
    'total_wait_time': 0,
    'total_turnaround_time': 0,
    'boot_time': datetime.now(),
}

def log_event(event_type, details):
    """Log a system event"""
    event = {
        'timestamp': datetime.now().isoformat(),
        'type': event_type,
        'details': details
    }
    system_events.append(event)
    return event


def serialize_io_request(req):
    """Convert an I/O request to JSON-friendly data."""
    return {
        'request_id': req.request_id,
        'process_pid': req.process_pid,
        'device_name': req.device_name,
        'operation': req.operation,
        'data_size': req.data_size,
        'disk_cylinder': req.disk_cylinder,
        'status': req.status,
        'seek_time': req.seek_time,
        'wait_time': req.wait_time
    }


def build_memory_map():
    """Build fixed-partition memory map for the assignment requirement."""
    processes = {
        p.pid: p.to_dict()
        for p in simulator.process_manager.get_all_processes()
    }
    partitions = []
    for part in simulator.memory_manager.get_partition_status():
        process = processes.get(part.get('process_pid'))
        partitions.append({
            **part,
            'process_name': process['name'] if process else None,
            'state': process['state'] if process else None
        })

    status = simulator.memory_manager.get_memory_status()
    return {
        'algorithm': simulator.memory_manager.allocation_algorithm,
        'total_memory': status['total'],
        'used_memory': status['allocated'],
        'free_memory': status['available'],
        'usage_percent': status['percentage_used'],
        'partitions': partitions,
        'text_map': ' '.join([
            f"[P{p['process_pid']}:{p['allocated_size']}/{p['size']}MB]"
            if p.get('allocated') else f"[Free:{p['size']}MB]"
            for p in partitions
        ])
    }


def build_scheduling_report():
    """Build execution order, waiting time, and text Gantt data."""
    processes = simulator.process_manager.get_all_processes()
    gantt = simulator.scheduler.get_gantt_chart()
    return {
        'algorithm': simulator.scheduler.algorithm,
        'gantt_chart': gantt,
        'waiting_times': [
            {
                'pid': p.pid,
                'name': p.name,
                'state': p.state.value,
                'wait_time': p.wait_time,
                'turnaround_time': p.turnaround_time,
                'remaining_time': p.remaining_burst_time,
                'burst_time': p.total_burst_time
            }
            for p in processes
        ],
        'average_wait_time': (
            sum(p.wait_time for p in processes) / len(processes)
            if processes else 0
        )
    }


def build_printer_status():
    """Build printer queue/spooling status."""
    printer = simulator.io_system.get_device('printer')
    if not printer:
        return {'available': False, 'message': 'Printer device not configured'}

    return {
        'available': True,
        'device': printer.get_device_info(),
        'current_request': (
            serialize_io_request(printer.current_request)
            if printer.current_request else None
        ),
        'queue': [serialize_io_request(req) for req in printer.request_queue],
        'completed_requests': printer.completed_requests,
        'spooling': {
            'pending_jobs': len(printer.request_queue),
            'is_printing': printer.current_request is not None,
            'total_submitted': len([
                req for req in simulator.io_system.all_requests
                if req.device_name == 'printer'
            ])
        }
    }


def build_project_requirements_report():
    """Map the current simulator state to the project rubric."""
    processes = simulator.process_manager.get_all_processes()
    process_states = {state: 0 for state in ['READY', 'RUNNING', 'WAITING', 'TERMINATED']}
    for process in processes:
        if process.state.value in process_states:
            process_states[process.state.value] += 1

    files = simulator.get_files().get('files', [])
    printer = build_printer_status()
    scheduling = build_scheduling_report()
    memory = build_memory_map()

    return {
        'process_management': {
            'required': 'Create at least 3 simulated processes and display states',
            'met': len(processes) >= 3 and any(process_states.values()),
            'process_count': len(processes),
            'states': process_states,
            'processes': [p.to_dict() for p in processes]
        },
        'cpu_scheduling': {
            'required': 'Implement FCFS or Round Robin and show execution order/waiting time',
            'met': simulator.scheduler.algorithm in ['fcfs', 'round_robin'] and bool(scheduling['gantt_chart']['segments']),
            **scheduling
        },
        'memory_management': {
            'required': 'Simulate fixed memory partitions and show usage',
            'met': simulator.memory_manager.allocation_algorithm in ['first_fit', 'best_fit', 'worst_fit'] and len(memory['partitions']) > 0,
            **memory
        },
        'file_system': {
            'required': 'Create/delete/display files without actual disk access',
            'met': len(files) > 0,
            'file_count': len(files),
            'files': files
        },
        'io_simulation': {
            'required': 'Simulate one I/O device such as a printer with queued requests',
            'met': printer.get('available') and (
                printer['spooling']['pending_jobs'] > 0 or
                printer['spooling']['total_submitted'] > 0
            ),
            **printer
        }
    }


def ensure_project_demo_data():
    """Seed a small demo that satisfies the assignment scenario."""
    if simulator.memory_manager.allocation_algorithm == 'dynamic':
        simulator.set_memory_allocation_algorithm('first_fit')

    active_processes = [
        p for p in simulator.process_manager.get_all_processes()
        if p.state.value != 'TERMINATED'
    ]

    demo_specs = [
        ('StudentProcess_A', 8, 64, 1),
        ('StudentProcess_B', 12, 96, 2),
        ('StudentProcess_C', 6, 48, 1),
    ]
    for spec in demo_specs:
        if len(active_processes) >= 3:
            break
        process = simulator.create_process(
            spec[0], burst_time=spec[1], memory_required=spec[2],
            io_operations=1, priority=spec[3]
        )
        if process:
            active_processes.append(process)

    simulator.is_running = True
    for _ in range(10):
        simulator.step_simulation()

    ready_processes = [
        p for p in simulator.process_manager.get_all_processes()
        if p.state.value == 'READY'
    ]
    if ready_processes:
        ready_processes[-1].move_to_waiting()

    if not simulator.filesystem.file_exists('demo.txt'):
        simulator.create_file(
            'demo.txt',
            'This file is stored in the simulated in-memory file system.'
        )

    printer = simulator.io_system.get_device('printer')
    if printer and not printer.request_queue and printer.completed_requests == 0:
        source_pid = active_processes[0].pid if active_processes else 0
        simulator.io_system.submit_io_request(
            source_pid, 'printer', operation='print', data_size=128
        )

    log_event('project_demo_seeded', {'timestamp': datetime.now().isoformat()})
    return build_project_requirements_report()

def calculate_system_metrics():
    """Calculate real-time system metrics"""
    try:
        processes = simulator.process_manager.get_all_processes()
        
        running_count = len([p for p in processes if p.state.name == 'RUNNING'])
        ready_count = len([p for p in processes if p.state.name == 'READY'])
        waiting_count = len([p for p in processes if p.state.name == 'WAITING'])
        total_count = len(processes)
        
        memory_used = simulator.memory_manager.get_allocated_memory()
        memory_total = simulator.memory_manager.physical_memory
        memory_percent = (memory_used / memory_total * 100) if memory_total > 0 else 0
        
        avg_wait_time = sum([p.wait_time for p in processes]) / total_count if total_count > 0 else 0
        avg_turnaround = sum([p.turnaround_time for p in processes]) / total_count if total_count > 0 else 0
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'uptime_seconds': (datetime.now() - system_metrics['boot_time']).total_seconds(),
            'total_processes': total_count,
            'running_processes': running_count,
            'ready_processes': ready_count,
            'waiting_processes': waiting_count,
            'cpu_utilization': min(100, (running_count / max(1, total_count)) * 100),
            'memory_used': memory_used,
            'memory_total': memory_total,
            'memory_utilization': memory_percent,
            'avg_wait_time': round(avg_wait_time, 2),
            'avg_turnaround_time': round(avg_turnaround, 2),
            'context_switches': system_metrics['context_switches'],
            'total_processes_created': system_metrics['total_processes_created'],
            'total_processes_terminated': system_metrics['total_processes_terminated']
        }
        
        performance_history.append(metrics)
        return metrics
    except Exception as e:
        log_event('metrics_calculation_error', {'error': str(e)})
        return {
            'timestamp': datetime.now().isoformat(),
            'error': str(e),
            'status': 'error'
        }

def get_system_overview():
    """Get comprehensive system overview"""
    try:
        metrics = calculate_system_metrics()
        processes = simulator.process_manager.get_all_processes()
        
        return {
            'system': {
                'name': SYSTEM_NAME,
                'version': '2.5.0',
                'hostname': HOSTNAME,
                'uptime': metrics['uptime_seconds']
            },
            'processes': {
                'total': metrics['total_processes'],
                'running': metrics['running_processes'],
                'ready': metrics['ready_processes'],
                'waiting': metrics['waiting_processes']
            },
            'cpu': {
                'utilization': metrics['cpu_utilization'],
                'context_switches': metrics['context_switches']
            },
            'memory': {
                'used': metrics['memory_used'],
                'total': metrics['memory_total'],
                'utilization': metrics['memory_utilization']
            },
            'statistics': {
                'avg_wait_time': metrics['avg_wait_time'],
                'avg_turnaround_time': metrics['avg_turnaround_time'],
                'total_created': metrics['total_processes_created'],
                'total_terminated': metrics['total_processes_terminated']
            }
        }
    except Exception as e:
        log_event('overview_error', {'error': str(e)})
        return {'error': str(e), 'status': 'error'}

def validate_system_state():
    """Validate and maintain system integrity"""
    try:
        issues = []
        warnings = []
        
        metrics = calculate_system_metrics()
        
        # Check CPU utilization
        if metrics['cpu_utilization'] > 95:
            issues.append('Critical CPU overload')
        elif metrics['cpu_utilization'] > 80:
            warnings.append('High CPU utilization')
        
        # Check memory
        if metrics['memory_utilization'] > 95:
            issues.append('Critical memory shortage')
        elif metrics['memory_utilization'] > 80:
            warnings.append('Memory usage high')
        
        # Check process queue
        if metrics['waiting_processes'] > 20:
            issues.append('Too many waiting processes')
        elif metrics['waiting_processes'] > 10:
            warnings.append('Process queue building up')
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings,
            'metrics': metrics
        }
    except Exception as e:
        return {'valid': False, 'error': str(e)}


# ===========================
# ROUTES - Main Pages
# ===========================

@app.route('/')
def index():
    """Serve main UI"""
    return render_template('index.html')


# ===========================
# NEW INTERACTIVE FEATURES - ENHANCED MONITORING
# ===========================

@app.route('/api/system-metrics', methods=['GET'])
def api_system_metrics():
    """Get real-time system metrics"""
    metrics = calculate_system_metrics()
    state = validate_system_state()
    
    return jsonify({
        'metrics': metrics,
        'state_validation': state
    })


@app.route('/api/system-overview', methods=['GET'])
def api_system_overview():
    """Get comprehensive system overview"""
    overview = get_system_overview()
    return jsonify(overview)


@app.route('/api/dashboard', methods=['GET'])
def api_dashboard():
    """Get complete dashboard data"""
    try:
        metrics = calculate_system_metrics()
        overview = get_system_overview()
        state = validate_system_state()
        
        # Get recent events
        recent_events = list(system_events)[-10:] if system_events else []
        
        # Get process summary
        processes = simulator.process_manager.get_all_processes()
        process_summary = {
            'by_state': {
                'running': len([p for p in processes if p.state.name == 'RUNNING']),
                'ready': len([p for p in processes if p.state.name == 'READY']),
                'waiting': len([p for p in processes if p.state.name == 'WAITING']),
                'terminated': len([p for p in processes if p.state.name == 'TERMINATED'])
            },
            'by_priority': {}
        }
        
        dashboard = {
            'timestamp': datetime.now().isoformat(),
            'system': overview,
            'metrics': metrics,
            'state_validation': state,
            'processes': process_summary,
            'recent_events': recent_events,
            'alerts': state['issues'] + state['warnings']
        }
        
        return jsonify(dashboard)
    except Exception as e:
        log_event('dashboard_error', {'error': str(e)})
        return jsonify({'error': str(e), 'status': 'error'}), 500


@app.route('/api/performance-history', methods=['GET'])
def api_performance_history():
    """Get performance history"""
    return jsonify({
        'history': list(performance_history)
    })


@app.route('/api/system-events', methods=['GET'])
def api_system_events():
    """Get system events log"""
    limit = request.args.get('limit', 50, type=int)
    events_list = list(system_events)[-limit:]
    return jsonify({
        'events': events_list,
        'total': len(system_events)
    })


@app.route('/api/process-tree', methods=['GET'])
def api_process_tree():
    """Get process tree/hierarchy"""
    processes = simulator.process_manager.get_all_processes()
    tree_data = []
    
    for p in processes:
        tree_data.append({
            'pid': p.pid,
            'name': p.name,
            'state': p.state.name,
            'parent_pid': getattr(p, 'parent_pid', None),
            'children': [],
            'memory': p.memory_required,
            'burst_time': p.burst_time,
            'progress': getattr(p, 'progress', 0)
        })
    
    return jsonify({
        'processes': tree_data
    })


@app.route('/api/resource-forecast', methods=['GET'])
def api_resource_forecast():
    """Forecast resource usage"""
    processes = simulator.process_manager.get_all_processes()
    total_burst = sum([getattr(p, 'remaining_burst_time', p.burst_time) for p in processes])
    total_memory_needed = sum([p.memory_required for p in processes])
    memory_total = simulator.memory_manager.physical_memory
    
    forecast = {
        'estimated_completion_time': total_burst,
        'total_memory_needed': total_memory_needed,
        'processes_count': len(processes),
        'average_burst_time': sum([p.burst_time for p in processes]) / len(processes) if processes else 0,
        'memory_pressure': min(100, (total_memory_needed / memory_total * 100)) if memory_total > 0 else 0
    }
    
    return jsonify(forecast)


@app.route('/api/system-health', methods=['GET'])
def api_system_health():
    """Get system health report"""
    metrics = calculate_system_metrics()
    
    health_status = 'GOOD'
    issues = []
    
    if metrics['cpu_utilization'] > 90:
        health_status = 'WARNING'
        issues.append('CPU utilization very high')
    if metrics['memory_utilization'] > 85:
        health_status = 'WARNING'
        issues.append('Memory usage critical')
    if metrics['waiting_processes'] > 10:
        issues.append('Many processes waiting for resources')
    
    return jsonify({
        'status': health_status,
        'metrics': metrics,
        'issues': issues
    })


@app.route('/api/terminal-command', methods=['POST'])
def api_terminal_command():
    """Execute terminal-like command with full integration"""
    try:
        data = request.get_json()
        command = data.get('command', '').strip().lower()
        
        output = ""
        success = True
        
        if command.startswith('ps'):
            # List processes with detailed info
            processes = simulator.process_manager.get_all_processes()
            output = "PID\tNAME\t\t\tSTATE\t\tMEMORY\tBURST\tWAIT\n"
            output += "---\t----\t\t\t-----\t\t------\t-----\t-----\n"
            for p in processes:
                wait_time = getattr(p, 'wait_time', 0)
                output += f"{p.pid}\t{p.name[:15]:<15}\t{p.state.name:<10}\t{p.memory_required}\t{p.total_burst_time}\t{wait_time:.1f}\n"
            if not processes:
                output = "No processes running\n"
        
        elif command.startswith('top'):
            # System top-like info with integration
            metrics = calculate_system_metrics()
            state = validate_system_state()
            output = f"System Status - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            output += f"==========================================\n"
            output += f"Uptime: {int(metrics['uptime_seconds'])}s\n"
            output += f"CPU Utilization: {metrics['cpu_utilization']:.1f}%\n"
            output += f"Memory: {metrics['memory_used']}/{metrics['memory_total']} MB ({metrics['memory_utilization']:.1f}%)\n"
            output += f"Running: {metrics['running_processes']} | Ready: {metrics['ready_processes']} | Waiting: {metrics['waiting_processes']}\n"
            output += f"Context Switches: {metrics['context_switches']}\n"
            output += f"System Health: {'GOOD' if state['valid'] else 'ISSUES DETECTED'}\n"
            if state['warnings']:
                output += f"Warnings: {', '.join(state['warnings'])}\n"
        
        elif command.startswith('df'):
            # Disk free with file system integration
            try:
                info = simulator.get_filesystem_info()
                output = f"Filesystem\tSize\tUsed\tAvail\tUse%\n"
                total = info.get('total_size', 1000)
                used = info.get('used_size', 0)
                available = total - used
                percent = (used / total * 100) if total > 0 else 0
                output += f"/dev/sda1\t{total}MB\t{used}MB\t{available}MB\t{percent:.1f}%\n"
            except:
                output = "Unable to get filesystem info\n"

        elif command == 'gantt':
            report = build_scheduling_report()
            output = "CPU Scheduling Report\n"
            output += f"Algorithm: {report['algorithm']}\n"
            output += f"Gantt: {report['gantt_chart']['text_chart']}\n"
            output += f"Time:  {report['gantt_chart']['time_axis']}\n"
            output += "Waiting Times:\n"
            for item in report['waiting_times']:
                output += f"  P{item['pid']} {item['name']}: {item['wait_time']} ticks\n"

        elif command == 'memmap':
            memory = build_memory_map()
            output = "Fixed Partition Memory Map\n"
            output += f"{memory['text_map']}\n"
            output += f"Used: {memory['used_memory']}/{memory['total_memory']} MB ({memory['usage_percent']:.1f}%)\n"

        elif command == 'printer':
            printer = build_printer_status()
            output = "Printer Spooling Queue\n"
            output += f"Pending jobs: {printer['spooling']['pending_jobs']}\n"
            output += f"Completed jobs: {printer['completed_requests']}\n"
            for job in printer['queue']:
                output += f"  Job {job['request_id']} from P{job['process_pid']} - {job['status']}\n"
        
        elif command.startswith('ls') or command.startswith('dir'):
            # List files with details
            try:
                files = simulator.get_files()
                output = "Files in system:\n"
                output += "NAME\t\t\t\tSIZE\tTYPE\n"
                for f in files:
                    size = f.get('size', 0)
                    ftype = f.get('extension', 'file')
                    filename = f.get('filename', f.get('name', 'unknown'))
                    output += f"  {filename:<30}\t{size}\t{ftype}\n"
                if not files:
                    output = "No files in system\n"
            except:
                output = "Unable to list files\n"
        
        elif command == 'uptime':
            metrics = calculate_system_metrics()
            uptime = int(metrics['uptime_seconds'])
            hours = uptime // 3600
            minutes = (uptime % 3600) // 60
            seconds = uptime % 60
            output = f"System uptime: {uptime}s ({hours}h {minutes}m {seconds}s)\n"
        
        elif command == 'whoami':
            output = f"user@{HOSTNAME}\n"
        
        elif command == 'uname':
            output = f"{SYSTEM_NAME} {HOSTNAME} 2.5.0\n"
        
        elif command == 'metrics':
            metrics = calculate_system_metrics()
            output = f"System Metrics:\n"
            output += f"Total Processes: {metrics['total_processes']}\n"
            output += f"CPU Utilization: {metrics['cpu_utilization']:.2f}%\n"
            output += f"Memory Used: {metrics['memory_used']}/{metrics['memory_total']} MB\n"
            output += f"Avg Wait Time: {metrics['avg_wait_time']:.2f}ms\n"
            output += f"Context Switches: {metrics['context_switches']}\n"
        
        elif command == 'events':
            recent = list(system_events)[-5:]
            output = "Recent System Events:\n"
            for event in recent:
                output += f"[{event['timestamp']}] {event['type']}\n"
        
        elif command == 'health':
            state = validate_system_state()
            output = f"System Health: {'âœ“ GOOD' if state['valid'] else 'âœ— ISSUES'}\n"
            if state['issues']:
                output += "Issues:\n"
                for issue in state['issues']:
                    output += f"  - {issue}\n"
            if state['warnings']:
                output += "Warnings:\n"
                for warning in state['warnings']:
                    output += f"  - {warning}\n"
        
        elif command == 'help' or command == '?':
            output = "PusoyOS 2.5.0 Terminal Commands:\n"
            output += "  ps         - List all processes\n"
            output += "  top        - System status\n"
            output += "  df         - Disk space\n"
            output += "  ls/dir     - List files\n"
            output += "  uptime     - System uptime\n"
            output += "  whoami     - Current user\n"
            output += "  uname      - System info\n"
            output += "  metrics    - Performance metrics\n"
            output += "  events     - Recent events\n"
            output += "  health     - System health\n"
            output += "  gantt      - Text Gantt chart and waiting times\n"
            output += "  memmap     - Fixed-partition memory map\n"
            output += "  printer    - Printer spooling queue\n"
            output += "  clear      - Clear screen\n"
            output += "  help/?     - This help\n"
        
        elif command == 'clear':
            output = "\n" * 3
        
        elif command == '':
            output = ""
        
        else:
            output = f"Command not found: {command}\nType 'help' for available commands.\n"
            success = False
        
        log_event('terminal_command', {
            'command': command,
            'success': success,
            'output_length': len(output)
        })
        
        return jsonify({
            'success': True,
            'command': command,
            'output': output,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        log_event('terminal_command_error', {'error': str(e)})
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/analytics-report', methods=['GET'])
def api_analytics_report():
    """Generate comprehensive analytics report"""
    processes = simulator.process_manager.get_all_processes()
    
    terminated_processes = [p for p in processes if p.state.name == 'TERMINATED']
    
    total_burst = sum([p.burst_time for p in terminated_processes])
    total_wait = sum([p.wait_time for p in terminated_processes])
    total_turnaround = sum([p.turnaround_time for p in terminated_processes])
    
    avg_burst = total_burst / len(terminated_processes) if terminated_processes else 0
    avg_wait = total_wait / len(terminated_processes) if terminated_processes else 0
    avg_turnaround = total_turnaround / len(terminated_processes) if terminated_processes else 0
    
    report = {
        'total_processes': len(processes),
        'completed_processes': len(terminated_processes),
        'active_processes': len([p for p in processes if p.state.name in ['RUNNING', 'READY', 'WAITING']]),
        'statistics': {
            'average_burst_time': round(avg_burst, 2),
            'average_wait_time': round(avg_wait, 2),
            'average_turnaround_time': round(avg_turnaround, 2),
            'total_context_switches': system_metrics['context_switches'],
            'system_uptime_seconds': (datetime.now() - system_metrics['boot_time']).total_seconds()
        },
        'current_metrics': calculate_system_metrics()
    }
    
    return jsonify(report)


@app.route('/api/scheduling-algorithms', methods=['GET'])
def api_scheduling_algorithms():
    """Get available scheduling algorithms"""
    return jsonify({
        'algorithms': [
            {'name': 'Round Robin', 'id': 'round_robin', 'description': 'Time-shared scheduling with configurable quantum'},
            {'name': 'First Come First Served', 'id': 'fcfs', 'description': 'Process by arrival order'},
            {'name': 'Shortest Job First', 'id': 'sjf', 'description': 'Execute shortest burst time first'},
            {'name': 'Priority Scheduling', 'id': 'priority', 'description': 'Process by priority level'},
            {'name': 'Multilevel Queue', 'id': 'multilevel', 'description': 'Multiple queues with different priorities'}
        ]
    })


@app.route('/api/memory-algorithms', methods=['GET'])
def api_memory_algorithms():
    """Get available memory allocation algorithms"""
    return jsonify({
        'algorithms': [
            {'name': 'First Fit', 'id': 'first_fit', 'description': 'Allocate first available partition'},
            {'name': 'Best Fit', 'id': 'best_fit', 'description': 'Allocate smallest suitable partition'},
            {'name': 'Worst Fit', 'id': 'worst_fit', 'description': 'Allocate largest available partition'},
            {'name': 'Next Fit', 'id': 'next_fit', 'description': 'Allocate from next available after last'}
        ]
    })


# ===========================
# API ROUTES - System Control
# ===========================

@app.route('/api/get-status', methods=['GET'])
def get_status():
    """Get current system status"""
    return jsonify(simulator.get_status())


@app.route('/api/system-info', methods=['GET'])
def system_info():
    """Get system information"""
    return jsonify(simulator.get_system_info())


@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset simulator"""
    try:
        simulator.reset_simulation()
        
        # Reset metrics
        system_events.clear()
        performance_history.clear()
        system_metrics['total_processes_created'] = 0
        system_metrics['total_processes_terminated'] = 0
        system_metrics['context_switches'] = 0
        system_metrics['boot_time'] = datetime.now()
        
        log_event('system_reset', {'timestamp': datetime.now().isoformat()})
        
        return jsonify({
            'success': True,
            'message': 'Simulator reset successfully',
            'metrics': calculate_system_metrics()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/project-requirements', methods=['GET'])
def project_requirements():
    """Return a rubric-aligned status report for the OS simulator project."""
    return jsonify(build_project_requirements_report())


@app.route('/api/project-demo-setup', methods=['POST'])
def project_demo_setup():
    """Seed processes, files, scheduling, memory, and printer spooling demo data."""
    return jsonify({
        'success': True,
        'report': ensure_project_demo_data()
    })


@app.route('/api/scheduling-report', methods=['GET'])
def scheduling_report():
    """Return text Gantt chart, execution order, and waiting times."""
    return jsonify(build_scheduling_report())


@app.route('/api/memory-map', methods=['GET'])
def memory_map():
    """Return fixed-partition memory map."""
    return jsonify(build_memory_map())


@app.route('/api/printer', methods=['GET'])
def printer_status():
    """Return printer queue/spooling status."""
    return jsonify(build_printer_status())


@app.route('/api/printer/submit', methods=['POST'])
def printer_submit():
    """Submit a basic printer I/O request."""
    try:
        data = request.get_json() or {}
        pid = int(data.get('pid', 0))
        data_size = int(data.get('data_size', 128))
        request_obj = simulator.io_system.submit_io_request(
            pid, 'printer', operation='print', data_size=data_size
        )
        if not request_obj:
            return jsonify({'success': False, 'message': 'Printer unavailable'}), 400
        log_event('printer_job_submitted', {
            'pid': pid,
            'request_id': request_obj.request_id,
            'data_size': data_size
        })
        return jsonify({
            'success': True,
            'request': serialize_io_request(request_obj),
            'printer': build_printer_status()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/printer/process', methods=['POST'])
def printer_process():
    """Process the next printer queue item."""
    simulator.io_system.process_io()
    log_event('printer_queue_processed', {
        'timestamp': datetime.now().isoformat()
    })
    return jsonify({
        'success': True,
        'printer': build_printer_status()
    })


# ===========================
# API ROUTES - Process Management
# ===========================

@app.route('/api/create-process', methods=['POST'])
def create_process():
    """Create a new process with full integration"""
    try:
        data = request.get_json()
        name = data.get('name', f'Process{system_metrics["total_processes_created"]}')
        burst_time = int(data.get('burst_time', 10))
        memory = int(data.get('memory', 100))
        io_ops = int(data.get('io_ops', 1))
        priority = int(data.get('priority', 1))
        
        # Validate parameters
        if burst_time <= 0 or memory <= 0:
            log_event('process_validation_failed', {'name': name, 'reason': 'invalid_parameters'})
            return jsonify({
                'success': False,
                'message': 'Invalid parameters: burst_time and memory must be positive'
            }), 400
        
        # Check system state before creation
        state = validate_system_state()
        
        # Create process
        process = simulator.create_process(name, burst_time, memory, io_ops, priority)
        
        if process:
            system_metrics['total_processes_created'] += 1
            
            log_event('process_created', {
                'pid': process.pid,
                'name': name,
                'burst_time': burst_time,
                'memory': memory,
                'priority': priority,
                'system_health': state['valid']
            })
            
            # Calculate new metrics
            new_metrics = calculate_system_metrics()
            
            return jsonify({
                'success': True,
                'process': process.to_dict() if hasattr(process, 'to_dict') else {
                    'pid': process.pid,
                    'name': process.name,
                    'state': process.state.name,
                    'burst_time': burst_time,
                    'memory': memory,
                    'priority': priority
                },
                'message': f'Process {name} (PID: {process.pid}) created successfully',
                'metrics': new_metrics
            })
        else:
            log_event('process_creation_failed', {
                'name': name,
                'reason': 'insufficient_resources',
                'memory_required': memory,
                'memory_available': new_metrics['memory_total'] - new_metrics['memory_used']
            })
            return jsonify({
                'success': False,
                'message': f'Failed to create process: Insufficient resources (need {memory}MB memory)'
            }), 400
    except ValueError as ve:
        log_event('process_creation_error', {'error': f'ValueError: {str(ve)}'})
        return jsonify({'success': False, 'error': f'Invalid input: {str(ve)}'}), 400
    except Exception as e:
        log_event('process_creation_error', {'error': str(e)})
        return jsonify({'success': False, 'error': str(e)}), 500
        log_event('process_creation_error', {'error': str(e)})
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/kill-process', methods=['POST'])
def kill_process():
    """Kill a process"""
    try:
        data = request.get_json()
        pid = int(data.get('pid'))
        signal = data.get('signal', 'SIGTERM')

        app = get_app_by_pid(pid)
        if app:
            result = simulator.close_application(app.app_id)
            if result.get('success'):
                system_metrics['total_processes_terminated'] += 1
                log_event('app_terminated_from_task_manager', {
                    'pid': pid,
                    'app_id': app.app_id,
                    'signal': signal
                })
            return jsonify(result)
        
        result = simulator.process_manager.kill_process(pid, signal)
        
        if result.get('success'):
            simulator.memory_manager.deallocate_memory(pid)
            system_metrics['total_processes_terminated'] += 1
            log_event('process_terminated', {'pid': pid, 'signal': signal})
        else:
            log_event('process_termination_failed', {'pid': pid, 'reason': result.get('message')})
        
        return jsonify(result)
    except Exception as e:
        log_event('process_termination_error', {'error': str(e)})
        return jsonify({'success': False, 'error': str(e)}), 400


def get_app_by_pid(pid):
    """Find a running application by process id."""
    for app in simulator.application_manager.running_apps.values():
        if app.pid == pid:
            return app
    return None


def build_task_manager_snapshot():
    """Build an ownership-aware task list like a desktop OS task manager."""
    processes = simulator.process_manager.get_all_processes()
    running_apps = simulator.application_manager.get_running_applications()
    process_by_pid = {p.pid: p for p in processes}
    app_by_pid = {app['pid']: app for app in running_apps if app.get('pid') is not None}

    app_tasks = []
    for app in running_apps:
        process = process_by_pid.get(app.get('pid'))
        app_tasks.append({
            'type': 'app',
            'app_id': app['app_id'],
            'name': app['name'],
            'pid': app.get('pid'),
            'status': app.get('status', 'running'),
            'state': process.state.value if process else 'RUNNING',
            'cpu_usage': app.get('cpu_usage_percent', 0),
            'cpu_time': process.cpu_time if process else app.get('cpu_time', 0),
            'memory': process.memory_required if process else app.get('memory_required', 0),
            'priority': process.priority if process else 1,
            'threads': app.get('threads', 1),
            'uptime_seconds': app.get('uptime_seconds', 0),
            'remaining_time': process.remaining_burst_time if process else 0,
            'can_switch': True,
            'can_end': True
        })

    background_tasks = []
    for process in processes:
        if process.pid in app_by_pid:
            continue
        if getattr(process, 'process_type', None) == 'application':
            continue
        background_tasks.append({
            'type': 'process',
            'app_id': None,
            'name': process.name,
            'pid': process.pid,
            'status': 'terminated' if process.state.value == 'TERMINATED' else 'running',
            'state': process.state.value,
            'cpu_usage': 0 if process.state.value != 'RUNNING' else 5,
            'cpu_time': process.cpu_time,
            'memory': process.memory_required,
            'priority': process.priority,
            'threads': 1,
            'uptime_seconds': 0,
            'remaining_time': process.remaining_burst_time,
            'can_switch': False,
            'can_end': process.state.value != 'TERMINATED'
        })

    stats = simulator.process_manager.get_statistics()
    metrics = calculate_system_metrics()
    return {
        'apps': app_tasks,
        'background_processes': background_tasks,
        'tasks': app_tasks + background_tasks,
        'statistics': {
            **stats,
            'running_apps': len(app_tasks),
            'background_processes': len(background_tasks),
            'cpu_utilization': metrics.get('cpu_utilization', 0),
            'memory_utilization': metrics.get('memory_utilization', 0),
            'memory_used': metrics.get('memory_used', 0),
            'memory_total': metrics.get('memory_total', 0)
        }
    }


@app.route('/api/task-manager', methods=['GET'])
def task_manager():
    """Get app-aware Task Manager data."""
    return jsonify(build_task_manager_snapshot())


@app.route('/api/task-action', methods=['POST'])
def task_action():
    """Perform a Task Manager action against an app or process."""
    try:
        data = request.get_json() or {}
        action = data.get('action')
        app_id = data.get('app_id')
        pid = data.get('pid')

        process = None
        if pid is not None:
            pid = int(pid)
            process = next(
                (p for p in simulator.process_manager.get_all_processes() if p.pid == pid),
                None
            )

        if action == 'end':
            if app_id:
                result = simulator.close_application(app_id)
            elif process:
                result = simulator.process_manager.kill_process(pid, 'SIGTERM')
                if result.get('success'):
                    simulator.memory_manager.deallocate_memory(pid)
            else:
                return jsonify({'success': False, 'message': 'Task not found'}), 404

            if result.get('success'):
                system_metrics['total_processes_terminated'] += 1
                log_event('task_manager_end_task', {'pid': pid, 'app_id': app_id})
            return jsonify(result)

        if action == 'force_end':
            if app_id:
                result = simulator.close_application(app_id)
            elif process:
                result = simulator.process_manager.kill_process(pid, 'SIGKILL')
                if result.get('success'):
                    simulator.memory_manager.deallocate_memory(pid)
            else:
                return jsonify({'success': False, 'message': 'Task not found'}), 404

            if result.get('success'):
                system_metrics['total_processes_terminated'] += 1
                log_event('task_manager_force_end_task', {'pid': pid, 'app_id': app_id})
            return jsonify(result)

        if action == 'suspend' and process:
            process.move_to_waiting()
            log_event('task_suspended', {'pid': pid})
            return jsonify({'success': True, 'message': f'Task {pid} suspended'})

        if action == 'resume' and process:
            process.move_to_ready()
            log_event('task_resumed', {'pid': pid})
            return jsonify({'success': True, 'message': f'Task {pid} resumed'})

        if action == 'switch' and app_id:
            log_event('task_switched', {'app_id': app_id})
            return jsonify({'success': True, 'message': f'Switched to {app_id}'})

        return jsonify({'success': False, 'message': 'Unsupported action'}), 400
    except Exception as e:
        log_event('task_action_error', {'error': str(e)})
        return jsonify({'success': False, 'error': str(e)}), 400


# ===========================
# API ROUTES - Scheduling
# ===========================

@app.route('/api/step', methods=['POST'])
def step():
    """Execute one simulation cycle"""
    simulator.step_simulation()
    return jsonify({
        'success': True,
        'system_clock': simulator.system_clock
    })


@app.route('/api/run-simulation', methods=['POST'])
def run_simulation():
    """Run simulation for N cycles"""
    try:
        data = request.get_json() or {}
        cycles = int(data.get('cycles', 100))
        simulator.run_simulation(cycles)
        return jsonify({
            'success': True,
            'cycles_run': cycles,
            'system_clock': simulator.system_clock
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/switch-algorithm', methods=['POST'])
def switch_algorithm():
    """Switch CPU scheduling algorithm"""
    try:
        data = request.get_json()
        algorithm = data.get('algorithm', 'round_robin')
        result = simulator.set_scheduling_algorithm(algorithm)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ===========================
# API ROUTES - Applications
# ===========================

@app.route('/api/applications', methods=['GET'])
def applications():
    """Get available and running applications"""
    return jsonify({
        'available': simulator.get_available_applications(),
        'running': simulator.get_running_applications()
    })


@app.route('/api/launch-app', methods=['POST'])
def launch_app():
    """Launch an application"""
    try:
        data = request.get_json()
        app_id = data.get('app_id')
        result = simulator.launch_application(app_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/close-app', methods=['POST'])
def close_app():
    """Close an application"""
    try:
        data = request.get_json()
        app_id = data.get('app_id')
        result = simulator.close_application(app_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ===========================
# API ROUTES - File System
# ===========================

@app.route('/api/files', methods=['GET'])
def files():
    """Get all files"""
    return jsonify(simulator.get_files())


@app.route('/api/create-file', methods=['POST'])
def create_file():
    """Create a file"""
    try:
        data = request.get_json()
        filename = data.get('filename', 'new_file.txt')
        content = data.get('content', '')
        result = simulator.create_file(filename, content)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/delete-file', methods=['POST'])
def delete_file():
    """Delete a file"""
    try:
        data = request.get_json()
        filename = data.get('filename')
        result = simulator.delete_file(filename)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/read-file', methods=['POST'])
def read_file():
    """Read file content"""
    try:
        data = request.get_json()
        filename = data.get('filename')
        result = simulator.read_file(filename)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/write-file', methods=['POST'])
def write_file():
    """Create or update a file's content."""
    try:
        data = request.get_json()
        filename = data.get('filename')
        content = data.get('content', '')

        if not filename:
            return jsonify({'success': False, 'message': 'Filename is required'}), 400

        if simulator.filesystem.file_exists(filename):
            success = simulator.filesystem.write_file(filename, content)
            result = {'success': success, 'filename': filename, 'message': 'File saved'}
        else:
            result = simulator.create_file(filename, content)
            result['message'] = 'File created'

        log_event('file_saved', {'filename': filename, 'size': len(content)})
        return jsonify(result)
    except Exception as e:
        log_event('file_save_error', {'error': str(e)})
        return jsonify({'success': False, 'error': str(e)}), 400


# ===========================
# API ROUTES - System Settings
# ===========================

@app.route('/api/system-settings', methods=['GET', 'POST'])
def system_settings():
    """Get or update system settings"""
    if request.method == 'POST':
        # Update settings
        return jsonify({'success': True, 'message': 'Settings updated'})
    else:
        # Get settings
        return jsonify({
            'settings': {
                'theme': 'dark',
                'resolution': '1920x1080',
                'hostname': HOSTNAME,
                'os_name': SYSTEM_NAME,
                'os_version': SYSTEM_VERSION
            }
        })


# ===========================
# API ROUTES - System Information
# ===========================

@app.route('/api/scheduler-info', methods=['GET'])
def scheduler_info():
    """Get scheduler information"""
    return jsonify(simulator.get_scheduler_info())


@app.route('/api/set-scheduling-algorithm', methods=['POST'])
def set_scheduling_algorithm():
    """Set CPU scheduling algorithm"""
    try:
        data = request.get_json()
        algorithm = data.get('algorithm', 'round_robin')
        result = simulator.set_scheduling_algorithm(algorithm)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/set-memory-allocation-algorithm', methods=['POST'])
def set_memory_allocation_algorithm():
    """Set memory allocation algorithm"""
    try:
        data = request.get_json()
        algorithm = data.get('algorithm', 'best_fit')
        result = simulator.set_memory_allocation_algorithm(algorithm)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/set-disk-scheduling-algorithm', methods=['POST'])
def set_disk_scheduling_algorithm():
    """Set disk scheduling algorithm"""
    try:
        data = request.get_json()
        algorithm = data.get('algorithm', 'fifo')
        result = simulator.set_disk_scheduling_algorithm(algorithm)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/memory-compaction', methods=['POST'])
def memory_compaction():
    """Perform memory compaction"""
    try:
        result = simulator.perform_memory_compaction()
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/memory-info', methods=['GET'])
def memory_info():
    """Get memory information"""
    return jsonify(simulator.get_memory_info())


@app.route('/api/filesystem-info', methods=['GET'])
def filesystem_info():
    """Get file system information"""
    return jsonify(simulator.get_filesystem_info())


@app.route('/api/io-info', methods=['GET'])
def io_info():
    """Get I/O system information"""
    return jsonify(simulator.get_io_info())


# ===========================
# API ROUTES - Process Listing
# ===========================

@app.route('/api/processes', methods=['GET'])
def processes():
    """Get all processes"""
    return jsonify({
        'processes': [p.to_dict() for p in simulator.process_manager.get_all_processes()],
        'statistics': simulator.process_manager.get_statistics()
    })


@app.route('/api/processes/running', methods=['GET'])
def running_processes():
    """Get running processes"""
    return jsonify({
        'processes': [p.to_dict() for p in simulator.process_manager.get_running_processes()]
    })


# ===========================
# INTEGRATED ADVANCED FEATURES
# ===========================

@app.route('/api/system-status', methods=['GET'])
def api_system_status():
    """Get integrated system status"""
    try:
        metrics = calculate_system_metrics()
        state = validate_system_state()
        overview = get_system_overview()
        
        return jsonify({
            'status': 'online',
            'timestamp': datetime.now().isoformat(),
            'system': overview,
            'metrics': metrics,
            'health': state
        })
    except Exception as e:
        log_event('status_error', {'error': str(e)})
        return jsonify({'error': str(e)}), 500


@app.route('/api/performance-report', methods=['GET'])
def api_performance_report():
    """Get detailed performance report"""
    try:
        metrics = calculate_system_metrics()
        history = list(performance_history)
        
        # Calculate trends
        if len(history) > 1:
            cpu_trend = history[-1]['cpu_utilization'] - history[-2]['cpu_utilization']
            memory_trend = history[-1]['memory_utilization'] - history[-2]['memory_utilization']
        else:
            cpu_trend = 0
            memory_trend = 0
        
        report = {
            'current_metrics': metrics,
            'history_size': len(history),
            'trends': {
                'cpu_trend': cpu_trend,
                'memory_trend': memory_trend
            },
            'averages': {
                'avg_cpu': sum([h['cpu_utilization'] for h in history]) / len(history) if history else 0,
                'avg_memory': sum([h['memory_utilization'] for h in history]) / len(history) if history else 0
            }
        }
        
        return jsonify(report)
    except Exception as e:
        log_event('performance_report_error', {'error': str(e)})
        return jsonify({'error': str(e)}), 500


@app.route('/api/process-details/<int:pid>', methods=['GET'])
def api_process_details(pid):
    """Get detailed information about a specific process"""
    try:
        processes = simulator.process_manager.get_all_processes()
        process = next((p for p in processes if p.pid == pid), None)
        
        if not process:
            return jsonify({'error': f'Process {pid} not found'}), 404
        
        details = {
            'pid': process.pid,
            'name': process.name,
            'state': process.state.name,
            'burst_time': process.burst_time,
            'memory_required': process.memory_required,
            'memory_allocated': getattr(process, 'memory_allocated', 0),
            'arrival_time': getattr(process, 'arrival_time', 0),
            'start_time': getattr(process, 'start_time', 0),
            'end_time': getattr(process, 'end_time', 0),
            'wait_time': getattr(process, 'wait_time', 0),
            'turnaround_time': getattr(process, 'turnaround_time', 0),
            'executed_time': getattr(process, 'executed_time', 0),
            'remaining_time': getattr(process, 'remaining_time', process.burst_time)
        }
        
        return jsonify(details)
    except Exception as e:
        log_event('process_details_error', {'error': str(e), 'pid': pid})
        return jsonify({'error': str(e)}), 500


@app.route('/api/resource-analysis', methods=['GET'])
def api_resource_analysis():
    """Get comprehensive resource analysis"""
    try:
        metrics = calculate_system_metrics()
        processes = simulator.process_manager.get_all_processes()
        
        # Resource utilization analysis
        analysis = {
            'cpu': {
                'utilization': metrics['cpu_utilization'],
                'available_capacity': 100 - metrics['cpu_utilization']
            },
            'memory': {
                'used': metrics['memory_used'],
                'total': metrics['memory_total'],
                'utilization': metrics['memory_utilization'],
                'available': metrics['memory_total'] - metrics['memory_used'],
                'fragmentation': 'low' if metrics['memory_utilization'] < 60 else 'medium' if metrics['memory_utilization'] < 80 else 'high'
            },
            'processes': {
                'total': metrics['total_processes'],
                'running': metrics['running_processes'],
                'ready': metrics['ready_processes'],
                'waiting': metrics['waiting_processes'],
                'queue_length': metrics['ready_processes'] + metrics['waiting_processes']
            },
            'performance': {
                'avg_wait_time': metrics['avg_wait_time'],
                'avg_turnaround_time': metrics['avg_turnaround_time'],
                'context_switches': metrics['context_switches']
            }
        }
        
        return jsonify(analysis)
    except Exception as e:
        log_event('resource_analysis_error', {'error': str(e)})
        return jsonify({'error': str(e)}), 500


@app.route('/api/event-summary', methods=['GET'])
def api_event_summary():
    """Get event summary and statistics"""
    try:
        events = list(system_events)
        
        event_counts = {}
        for event in events:
            event_type = event['type']
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        summary = {
            'total_events': len(events),
            'event_types': event_counts,
            'recent_events': events[-10:] if len(events) > 10 else events,
            'last_event_time': events[-1]['timestamp'] if events else None
        }
        
        return jsonify(summary)
    except Exception as e:
        log_event('event_summary_error', {'error': str(e)})
        return jsonify({'error': str(e)}), 500


@app.route('/api/system-stats', methods=['GET'])
def api_system_stats():
    """Get comprehensive system statistics"""
    try:
        metrics = calculate_system_metrics()
        processes = simulator.process_manager.get_all_processes()
        
        terminated = [p for p in processes if p.state.name == 'TERMINATED']
        
        stats = {
            'uptime': metrics['uptime_seconds'],
            'total_processes_created': system_metrics['total_processes_created'],
            'total_processes_terminated': system_metrics['total_processes_terminated'],
            'current_processes': metrics['total_processes'],
            'cpu': {
                'utilization_percent': metrics['cpu_utilization'],
                'context_switches': metrics['context_switches']
            },
            'memory': {
                'used_mb': metrics['memory_used'],
                'total_mb': metrics['memory_total'],
                'utilization_percent': metrics['memory_utilization']
            },
            'performance': {
                'avg_wait_time_ms': metrics['avg_wait_time'],
                'avg_turnaround_time_ms': metrics['avg_turnaround_time'],
                'total_events_logged': len(system_events)
            }
        }
        
        return jsonify(stats)
    except Exception as e:
        log_event('system_stats_error', {'error': str(e)})
        return jsonify({'error': str(e)}), 500


# ===========================
# Error Handlers
# ===========================

# ===========================
# API ROUTES - System Control: Shutdown & Restart
# ===========================

@app.route('/api/shutdown', methods=['POST'])
def api_shutdown():
    """Shutdown the operating system"""
    try:
        data = request.get_json() or {}
        force = data.get('force', False)
        save_state = data.get('save_state', True)
        
        # Log shutdown event
        log_event('system_shutdown', {
            'force': force,
            'uptime_seconds': (datetime.now() - system_metrics['boot_time']).total_seconds(),
            'total_processes': len(simulator.process_manager.get_all_processes()),
            'save_state': save_state
        })
        
        # Close all running applications
        running_apps = simulator.application_manager.get_running_applications()
        for app in running_apps:
            try:
                simulator.close_application(app['app_id'])
            except:
                pass
        
        # Gracefully terminate processes if not forced
        if not force:
            processes = simulator.process_manager.get_all_processes()
            for process in processes:
                if process.state.value != 'TERMINATED':
                    try:
                        simulator.process_manager.kill_process(process.pid, 'SIGTERM')
                    except:
                        pass
        
        simulator.is_running = False
        
        return jsonify({
            'success': True,
            'message': 'System shutdown initiated',
            'shutdown_reason': 'User requested shutdown',
            'uptime': int((datetime.now() - system_metrics['boot_time']).total_seconds()),
            'processes_terminated': len(running_apps)
        })
    
    except Exception as e:
        log_event('shutdown_error', {'error': str(e)})
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/restart', methods=['POST'])
def api_restart():
    """Restart the operating system"""
    try:
        data = request.get_json() or {}
        save_state = data.get('save_state', True)
        
        # Log restart event
        log_event('system_restart', {
            'uptime_seconds': (datetime.now() - system_metrics['boot_time']).total_seconds(),
            'save_state': save_state
        })
        
        # Close all running applications
        running_apps = simulator.application_manager.get_running_applications()
        for app in running_apps:
            try:
                simulator.close_application(app['app_id'])
            except:
                pass
        
        # Terminate all processes gracefully
        processes = simulator.process_manager.get_all_processes()
        for process in processes:
            if process.state.value != 'TERMINATED':
                try:
                    simulator.process_manager.kill_process(process.pid, 'SIGTERM')
                except:
                    pass
        
        # Reset the simulator
        simulator.reset_simulation()
        
        # Reset metrics
        system_events.clear()
        performance_history.clear()
        system_metrics['total_processes_created'] = 0
        system_metrics['total_processes_terminated'] = 0
        system_metrics['context_switches'] = 0
        system_metrics['boot_time'] = datetime.now()
        
        simulator.is_running = True
        
        log_event('system_restart_complete', {
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({
            'success': True,
            'message': 'System restart successful',
            'boot_time': system_metrics['boot_time'].isoformat(),
            'system_status': 'ONLINE'
        })
    
    except Exception as e:
        log_event('restart_error', {'error': str(e)})
        return jsonify({'success': False, 'error': str(e)}), 500


# ===========================
# API ROUTES - Settings & Personalization
# ===========================



@app.route('/api/background-settings', methods=['GET', 'POST'])
def background_settings():
    """Get or update background settings"""
    try:
        if request.method == 'POST':
            data = request.get_json() or {}
            bg_type = data.get('type', 'gradient')  # gradient, color, image
            bg_value = data.get('value', '#eff6ff')
            
            log_event('background_changed', {
                'type': bg_type,
                'value': bg_value[:50] if len(bg_value) > 50 else bg_value
            })
            
            return jsonify({
                'success': True,
                'message': 'Background updated',
                'setting': {
                    'type': bg_type,
                    'value': bg_value
                }
            })
        else:
            # Return current background settings
            return jsonify({
                'success': True,
                'current_background': {
                    'type': 'gradient',
                    'value': 'radial-gradient(circle at 16% 18%,rgba(37,99,235,.55),transparent 28%),radial-gradient(circle at 76% 12%,rgba(20,184,166,.38),transparent 30%),linear-gradient(135deg,#eff6ff,#dbeafe 38%,#f8fafc)'
                },
                'options': [
                    {'name': 'Blue Gradient', 'type': 'gradient', 'value': 'radial-gradient(circle at 16% 18%,rgba(37,99,235,.55),transparent 28%),linear-gradient(135deg,#eff6ff,#dbeafe)'},
                    {'name': 'Teal Sunset', 'type': 'gradient', 'value': 'linear-gradient(135deg, #0f766e, #14b8a6, #f0fdfa)'},
                    {'name': 'Purple Dream', 'type': 'gradient', 'value': 'linear-gradient(135deg, #7c3aed, #c4b5fd, #f3e8ff)'},
                    {'name': 'Light Gray', 'type': 'color', 'value': '#f5f5f5'},
                    {'name': 'Dark Theme', 'type': 'color', 'value': '#1a1a1a'}
                ]
            })
    except Exception as e:
        log_event('background_settings_error', {'error': str(e)})
        return jsonify({'success': False, 'error': str(e)}), 400


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


# ===========================
# Start Application
# ===========================

if __name__ == '__main__':
    log_event('system_boot', {'hostname': HOSTNAME, 'version': '2.5.0'})
    
    print(f"""
    ------------------------------------------------------------------
       {SYSTEM_NAME}
       {SYSTEM_VERSION}
       Enhanced Interactive Edition v2.5.0
    ------------------------------------------------------------------

    NEW INTERACTIVE FEATURES:
       - Real-time System Metrics Dashboard
       - Performance History & Analytics
       - Interactive Terminal Emulator
       - Resource Forecasting
       - System Health Monitoring
       - Process Tree Visualization
       - Event Logging System
       - Advanced Algorithm Selection

    API ENDPOINTS:
       /api/system-metrics        - Real-time system status
       /api/performance-history   - Historical performance data
       /api/system-events         - Event log stream
       /api/process-tree          - Process hierarchy
       /api/resource-forecast     - Resource predictions
       /api/system-health         - Health report
       /api/terminal-command      - Execute shell commands
       /api/analytics-report      - Comprehensive statistics

    Server Information:
       Hostname: {HOSTNAME}
       Running on http://127.0.0.1:8000
       Version: 2.5.0 (Enhanced)
       Status: ONLINE

    Documentation: Visit http://127.0.0.1:8000 to access the UI
    API Docs: All endpoints support JSON requests

    Press CTRL+C to shutdown gracefully...
    """)
    
    print("=" * 66)
    print("System initialized and ready for simulation")
    print("=" * 66 + "\n")
    
    app.run(debug=False, use_reloader=False, port=8000, host='127.0.0.1')

