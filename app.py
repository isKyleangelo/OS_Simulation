"""
PusoyOS - A Complete Operating System Simulator
Educational OS simulation with realistic process management, memory management, scheduling, and I/O

Author: CMSC 314 Students
Version: 2.5.0 - Enhanced Interactive Edition
"""

from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
from collections import deque
from math import ceil
import posixpath
from core.simulator import PusoyOSSimulator
from config import HOSTNAME, SYSTEM_NAME, SYSTEM_VERSION, ROOT_DIRECTORY

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Disable template caching
app.jinja_env.cache = {}  # Clear Jinja2 cache

# Create global simulator instance
simulator = PusoyOSSimulator()
simulator.is_running = True

# Desktop filesystem and printing state live in memory, just like the simulator.
# They wrap the original flat filesystem with folders, file associations, and
# OS-style print spooling without touching the user's real disk.
HOME_PATH = ROOT_DIRECTORY
VIRTUAL_DIRECTORIES = {
    HOME_PATH,
    f'{HOME_PATH}/Desktop',
    f'{HOME_PATH}/Documents',
    f'{HOME_PATH}/Pictures',
    f'{HOME_PATH}/Music',
    f'{HOME_PATH}/Downloads',
    f'{HOME_PATH}/System',
}

TEXT_EXTENSIONS = {'txt', 'log', 'md', 'py', 'js', 'html', 'css', 'json', 'csv'}
IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
PDF_EXTENSIONS = {'pdf'}
MEDIA_EXTENSIONS = {'mp3', 'wav', 'ogg', 'm4a'}

system_preferences = {
    'theme': 'dark',
    'wallpaper': 'aurora',
    'accent': '#2f7df6'
}

printers = [
    {
        'id': 'office-laser',
        'name': 'PusoyOffice Laser 314',
        'driver': 'PS-314 Universal',
        'location': 'CMSC Lab',
        'status': 'Online',
        'default': True,
    },
    {
        'id': 'pdf-printer',
        'name': 'Print to PDF',
        'driver': 'Virtual PDF Driver',
        'location': 'Local',
        'status': 'Online',
        'default': False,
    }
]
print_jobs = []
print_history = deque(maxlen=100)
print_job_counter = 7000

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


def normalize_desktop_path(path=None, parent=None, name=None):
    """Return a safe virtual path under the simulated home directory."""
    if name is not None:
        base = normalize_desktop_path(parent or HOME_PATH)
        path = f'{base}/{name}'

    raw_path = (path or HOME_PATH).strip().replace('\\', '/')
    if not raw_path:
        raw_path = HOME_PATH
    if not raw_path.startswith('/'):
        raw_path = f'{HOME_PATH}/{raw_path}'

    normalized = posixpath.normpath(raw_path)
    if normalized in ('.', '/'):
        normalized = HOME_PATH
    if normalized != HOME_PATH and not normalized.startswith(f'{HOME_PATH}/'):
        normalized = posixpath.normpath(f'{HOME_PATH}/{normalized.lstrip("/")}')
    return normalized


def relative_file_key(path):
    """Convert an absolute virtual path to the filesystem's relative key."""
    normalized = normalize_desktop_path(path)
    relative = normalized[len(HOME_PATH):].lstrip('/')
    return relative


def ensure_parent_directories(path):
    """Create all virtual parent folders for a path."""
    current = HOME_PATH
    VIRTUAL_DIRECTORIES.add(current)
    for part in relative_file_key(path).split('/')[:-1]:
        if not part:
            continue
        current = f'{current}/{part}'
        VIRTUAL_DIRECTORIES.add(current)


def file_extension(name):
    """Return a normalized file extension without the dot."""
    basename = posixpath.basename(name)
    return basename.rsplit('.', 1)[-1].lower() if '.' in basename else ''


def file_association(extension):
    """Map a file type to the application that should open it."""
    ext = (extension or '').lower()
    if ext in TEXT_EXTENSIONS:
        return 'texteditor'
    if ext in IMAGE_EXTENSIONS:
        return 'imageviewer'
    if ext in PDF_EXTENSIONS:
        return 'pdfviewer'
    if ext in MEDIA_EXTENSIONS:
        return 'mediaplayer'
    return 'texteditor'


def full_path_for_file(file_obj):
    """Translate a File object into a virtual absolute path."""
    filename = file_obj.filename.replace('\\', '/')
    if filename.startswith(HOME_PATH):
        return normalize_desktop_path(filename)
    return normalize_desktop_path(f'{HOME_PATH}/{filename}')


def get_file_by_path(path):
    """Find a file by virtual absolute path."""
    key = relative_file_key(path)
    return simulator.filesystem.get_file(key)


def serialize_file_entry(file_obj):
    """Build the common file entry used by file manager and app launchers."""
    path = full_path_for_file(file_obj)
    name = posixpath.basename(path)
    ext = file_extension(name)
    return {
        'type': 'file',
        'name': name,
        'filename': file_obj.filename,
        'path': path,
        'parent': posixpath.dirname(path),
        'extension': ext,
        'association': file_association(ext),
        'size': file_obj.size,
        'size_kb': file_obj.get_size_kb(),
        'owner': file_obj.owner,
        'permissions': file_obj.permissions,
        'created_at': file_obj.created_at.isoformat(),
        'modified_at': file_obj.modified_at.isoformat(),
        'accessed_at': file_obj.accessed_at.isoformat(),
    }


def serialize_folder_entry(path):
    """Build the common folder entry used by the desktop file manager."""
    normalized = normalize_desktop_path(path)
    return {
        'type': 'folder',
        'name': posixpath.basename(normalized) or 'Home',
        'path': normalized,
        'parent': None if normalized == HOME_PATH else posixpath.dirname(normalized),
        'extension': '',
        'association': 'filemanager',
        'size': 0,
        'modified_at': None,
    }


def breadcrumbs_for(path):
    """Build clickable breadcrumb segments for a virtual path."""
    normalized = normalize_desktop_path(path)
    crumbs = [{'name': 'Home', 'path': HOME_PATH}]
    relative = normalized[len(HOME_PATH):].strip('/')
    running = HOME_PATH
    for part in relative.split('/'):
        if not part:
            continue
        running = f'{running}/{part}'
        crumbs.append({'name': part, 'path': running})
    return crumbs


def create_virtual_file(path, content='', owner='root', permissions='644'):
    """Create a file at a virtual path, including missing parent folders."""
    normalized = normalize_desktop_path(path)
    ensure_parent_directories(normalized)
    key = relative_file_key(normalized)
    return simulator.filesystem.create_file(key, owner=owner, permissions=permissions, content=content)


def list_virtual_directory(path=HOME_PATH, search=''):
    """List folders and files for the desktop file manager."""
    normalized = normalize_desktop_path(path)
    VIRTUAL_DIRECTORIES.add(HOME_PATH)
    if normalized not in VIRTUAL_DIRECTORIES:
        VIRTUAL_DIRECTORIES.add(normalized)

    query = (search or '').strip().lower()
    folder_entries = []
    for directory in sorted(VIRTUAL_DIRECTORIES):
        if directory == normalized:
            continue
        parent = posixpath.dirname(directory)
        direct_child = parent == normalized
        descendant_match = query and directory.startswith(f'{normalized}/')
        if direct_child or descendant_match:
            entry = serialize_folder_entry(directory)
            if not query or query in entry['name'].lower():
                folder_entries.append(entry)

    file_entries = []
    for file_obj in simulator.filesystem.get_all_files():
        entry = serialize_file_entry(file_obj)
        direct_child = entry['parent'] == normalized
        descendant_match = query and entry['path'].startswith(f'{normalized}/')
        if direct_child or descendant_match:
            if not query or query in entry['name'].lower():
                file_entries.append(entry)

    entries = sorted(folder_entries, key=lambda item: item['name'].lower())
    entries.extend(sorted(file_entries, key=lambda item: item['name'].lower()))
    return {
        'path': normalized,
        'parent': None if normalized == HOME_PATH else posixpath.dirname(normalized),
        'breadcrumbs': breadcrumbs_for(normalized),
        'entries': entries,
        'count': len(entries),
        'search': search or '',
    }


def rename_virtual_path(old_path, new_name):
    """Rename a file or folder inside the virtual filesystem."""
    old_path = normalize_desktop_path(old_path)
    clean_name = posixpath.basename((new_name or '').strip().replace('\\', '/'))
    if not clean_name:
        return False, 'Name is required'

    parent = posixpath.dirname(old_path)
    new_path = normalize_desktop_path(parent=parent, name=clean_name)
    if old_path == HOME_PATH:
        return False, 'Home cannot be renamed'
    if new_path in VIRTUAL_DIRECTORIES or get_file_by_path(new_path):
        return False, 'An item with that name already exists'

    if old_path in VIRTUAL_DIRECTORIES:
        affected_dirs = sorted(
            [d for d in VIRTUAL_DIRECTORIES if d == old_path or d.startswith(f'{old_path}/')],
            key=len
        )
        for directory in affected_dirs:
            VIRTUAL_DIRECTORIES.remove(directory)
            VIRTUAL_DIRECTORIES.add(directory.replace(old_path, new_path, 1))

        for file_obj in list(simulator.filesystem.get_all_files()):
            path = full_path_for_file(file_obj)
            if path.startswith(f'{old_path}/'):
                simulator.filesystem.rename_file(
                    relative_file_key(path),
                    relative_file_key(path.replace(old_path, new_path, 1))
                )
        return True, 'Folder renamed'

    file_obj = get_file_by_path(old_path)
    if not file_obj:
        return False, 'File not found'

    success = simulator.filesystem.rename_file(relative_file_key(old_path), relative_file_key(new_path))
    return success, 'File renamed' if success else 'Rename failed'


def delete_virtual_path(path):
    """Delete a file or folder from the virtual filesystem."""
    normalized = normalize_desktop_path(path)
    if normalized == HOME_PATH:
        return False, 'Home cannot be deleted'

    if normalized in VIRTUAL_DIRECTORIES:
        for file_obj in list(simulator.filesystem.get_all_files()):
            file_path = full_path_for_file(file_obj)
            if file_path.startswith(f'{normalized}/'):
                simulator.filesystem.delete_file(relative_file_key(file_path))
        for directory in sorted(
            [d for d in VIRTUAL_DIRECTORIES if d == normalized or d.startswith(f'{normalized}/')],
            key=len,
            reverse=True
        ):
            VIRTUAL_DIRECTORIES.discard(directory)
        return True, 'Folder deleted'

    if get_file_by_path(normalized):
        return simulator.filesystem.delete_file(relative_file_key(normalized)), 'File deleted'
    return False, 'Item not found'


def move_virtual_path(source_path, destination_folder):
    """Move a file or folder into another virtual folder."""
    source_path = normalize_desktop_path(source_path)
    destination_folder = normalize_desktop_path(destination_folder)
    if destination_folder not in VIRTUAL_DIRECTORIES:
        return False, 'Destination folder not found'
    if source_path == HOME_PATH or destination_folder.startswith(f'{source_path}/'):
        return False, 'Cannot move item there'
    if posixpath.dirname(source_path) == destination_folder:
        return True, 'Item is already in that folder'
    return _move_virtual_path_to_folder(source_path, destination_folder)


def _move_virtual_path_to_folder(source_path, destination_folder):
    """Internal move helper once validation is complete."""
    new_path = normalize_desktop_path(parent=destination_folder, name=posixpath.basename(source_path))
    if new_path in VIRTUAL_DIRECTORIES or get_file_by_path(new_path):
        return False, 'Destination already contains that item'

    if source_path in VIRTUAL_DIRECTORIES:
        affected_dirs = sorted(
            [d for d in VIRTUAL_DIRECTORIES if d == source_path or d.startswith(f'{source_path}/')],
            key=len
        )
        for directory in affected_dirs:
            VIRTUAL_DIRECTORIES.remove(directory)
            VIRTUAL_DIRECTORIES.add(directory.replace(source_path, new_path, 1))
        for file_obj in list(simulator.filesystem.get_all_files()):
            path = full_path_for_file(file_obj)
            if path.startswith(f'{source_path}/'):
                simulator.filesystem.rename_file(
                    relative_file_key(path),
                    relative_file_key(path.replace(source_path, new_path, 1))
                )
        return True, 'Folder moved'

    file_obj = get_file_by_path(source_path)
    if not file_obj:
        return False, 'File not found'
    success = simulator.filesystem.rename_file(relative_file_key(source_path), relative_file_key(new_path))
    return success, 'File moved' if success else 'Move failed'


def sample_image_data_url():
    """Return a lightweight embedded image for the simulated image viewer."""
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 560">'
        '<rect width="900" height="560" fill="%23101f3f"/>'
        '<rect x="70" y="70" width="760" height="420" rx="22" fill="%23f8fafc"/>'
        '<circle cx="245" cy="210" r="72" fill="%23f5b23c"/>'
        '<path d="M90 455 305 270 445 385 560 300 810 455Z" fill="%232f7df6"/>'
        '<path d="M90 455 330 330 485 455Z" fill="%2314b88f"/>'
        '<text x="450" y="132" text-anchor="middle" font-family="Segoe UI,Arial" font-size="38" fill="%23182735">PusoyOS Gallery</text>'
        '</svg>'
    )
    return f'data:image/svg+xml;utf8,{svg}'


def ensure_desktop_demo_files():
    """Seed practical sample files so every file association has something to open."""
    samples = {
        f'{HOME_PATH}/Documents/welcome.txt': (
            'Welcome to PusoyOS.\n\n'
            'This document opens in Text Editor, can be saved, and can be sent to the print queue.'
        ),
        f'{HOME_PATH}/Documents/print-demo.md': (
            '# Printing demo\n\n'
            'Use File Manager to open this file in Text Editor, then choose Print. '
            'The job will move from Waiting to Printing to Completed.'
        ),
        f'{HOME_PATH}/Pictures/sample-landscape.png': sample_image_data_url(),
        f'{HOME_PATH}/Downloads/course-outline.pdf': (
            'PusoyOS PDF Viewer\n\n'
            'Simulated one-page PDF content for CMSC 314. '
            'The viewer opens PDF-associated files from File Manager.'
        ),
        f'{HOME_PATH}/Music/startup-theme.mp3': (
            'PUSOYOS_MEDIA\n'
            'title=Startup Theme\n'
            'artist=CMSC 314\n'
            'duration=95'
        ),
    }
    for path, content in samples.items():
        if not get_file_by_path(path):
            create_virtual_file(path, content=content, owner='student')


def get_printer(printer_id):
    """Find a configured printer by id."""
    return next((printer for printer in printers if printer['id'] == printer_id), None)


def serialize_print_job(job):
    """Return a JSON-safe print job copy."""
    return {
        **job,
        'created_at': job['created_at'].isoformat(),
        'started_at': job['started_at'].isoformat() if job.get('started_at') else None,
        'completed_at': job['completed_at'].isoformat() if job.get('completed_at') else None,
    }


def add_print_history(job, event_type, message):
    """Store a concise print history event."""
    print_history.appendleft({
        'timestamp': datetime.now().isoformat(),
        'job_id': job['id'],
        'document_name': job['document_name'],
        'event': event_type,
        'message': message,
    })


def refresh_print_system():
    """Advance print jobs based on elapsed time, like a small print spooler."""
    now = datetime.now()

    for job in print_jobs:
        if job['status'] != 'Printing':
            continue
        printer = get_printer(job['printer_id'])
        if not printer or printer['status'] == 'Offline':
            job['status'] = 'Error'
            job['completed_at'] = now
            add_print_history(job, 'error', 'Printer went offline while printing')
            continue
        elapsed = (now - job['started_at']).total_seconds()
        job['progress'] = min(100, int((elapsed / job['duration_seconds']) * 100))
        if elapsed >= job['duration_seconds']:
            job['status'] = 'Completed'
            job['progress'] = 100
            job['completed_at'] = now
            add_print_history(job, 'completed', 'Print job completed')

    for printer in printers:
        if printer['status'] == 'Offline':
            continue
        is_busy = any(
            job['printer_id'] == printer['id'] and job['status'] == 'Printing'
            for job in print_jobs
        )
        printer['status'] = 'Busy' if is_busy else 'Online'

    for printer in printers:
        if printer['status'] != 'Online':
            continue
        next_job = next(
            (
                job for job in print_jobs
                if job['printer_id'] == printer['id'] and job['status'] == 'Waiting'
            ),
            None
        )
        if next_job:
            next_job['status'] = 'Printing'
            next_job['started_at'] = now
            next_job['progress'] = 0
            printer['status'] = 'Busy'
            add_print_history(next_job, 'printing', 'Printer started the job')


ensure_desktop_demo_files()


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


@app.route('/api/print-system', methods=['GET'])
def print_system():
    """Return the desktop print spooler state."""
    refresh_print_system()
    return jsonify({
        'success': True,
        'printers': printers,
        'jobs': [serialize_print_job(job) for job in print_jobs],
        'active_jobs': [
            serialize_print_job(job) for job in print_jobs
            if job['status'] in ['Waiting', 'Printing', 'Error']
        ],
        'history': list(print_history),
    })


@app.route('/api/print-jobs', methods=['POST'])
def create_print_job():
    """Submit a document to the simulated print spooler."""
    global print_job_counter
    try:
        refresh_print_system()
        data = request.get_json() or {}
        document_name = data.get('document_name') or 'Untitled Document'
        content = data.get('content', '')
        printer_id = data.get('printer_id') or next((p['id'] for p in printers if p.get('default')), printers[0]['id'])
        printer = get_printer(printer_id)
        if not printer:
            return jsonify({'success': False, 'error': 'Printer not found'}), 404

        copies = max(1, int(data.get('copies', 1)))
        pages = max(1, ceil(max(1, len(content)) / 1500))
        duration = min(18, max(4, pages * copies * 3))
        print_job_counter += 1
        job = {
            'id': print_job_counter,
            'document_name': document_name,
            'source_app': data.get('source_app', 'Text Editor'),
            'printer_id': printer_id,
            'printer_name': printer['name'],
            'status': 'Waiting',
            'progress': 0,
            'pages': pages,
            'copies': copies,
            'page_size': data.get('page_size', 'Letter'),
            'orientation': data.get('orientation', 'Portrait'),
            'color_mode': data.get('color_mode', 'Black and white'),
            'quality': data.get('quality', 'Normal'),
            'duration_seconds': duration,
            'content_preview': content[:600],
            'created_at': datetime.now(),
            'started_at': None,
            'completed_at': None,
        }
        print_jobs.append(job)
        add_print_history(job, 'queued', 'Document entered the print queue')
        simulator.io_system.submit_io_request(0, 'printer', operation='print', data_size=max(128, pages * copies * 128))
        refresh_print_system()
        log_event('desktop_print_job_submitted', {
            'job_id': job['id'],
            'document': document_name,
            'printer': printer_id,
            'pages': pages,
        })
        return jsonify({
            'success': True,
            'message': 'Print job submitted',
            'job': serialize_print_job(job),
            'print_system': {
                'printers': printers,
                'jobs': [serialize_print_job(item) for item in print_jobs],
                'history': list(print_history),
            }
        })
    except Exception as e:
        log_event('desktop_print_job_error', {'error': str(e)})
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/print-jobs/<int:job_id>/cancel', methods=['POST'])
def cancel_print_job(job_id):
    """Cancel a waiting or printing job."""
    refresh_print_system()
    job = next((item for item in print_jobs if item['id'] == job_id), None)
    if not job:
        return jsonify({'success': False, 'error': 'Print job not found'}), 404
    if job['status'] in ['Completed', 'Cancelled']:
        return jsonify({'success': False, 'error': f'Job is already {job["status"].lower()}'}), 400

    job['status'] = 'Cancelled'
    job['completed_at'] = datetime.now()
    add_print_history(job, 'cancelled', 'Print job cancelled by user')
    refresh_print_system()
    log_event('desktop_print_job_cancelled', {'job_id': job_id})
    return jsonify({'success': True, 'message': 'Print job cancelled', 'job': serialize_print_job(job)})


@app.route('/api/print-jobs/<int:job_id>/retry', methods=['POST'])
def retry_print_job(job_id):
    """Return an errored job to the waiting queue."""
    refresh_print_system()
    job = next((item for item in print_jobs if item['id'] == job_id), None)
    if not job:
        return jsonify({'success': False, 'error': 'Print job not found'}), 404
    if job['status'] != 'Error':
        return jsonify({'success': False, 'error': 'Only errored jobs can be retried'}), 400
    job['status'] = 'Waiting'
    job['progress'] = 0
    job['started_at'] = None
    job['completed_at'] = None
    add_print_history(job, 'retry', 'Print job returned to the queue')
    refresh_print_system()
    return jsonify({'success': True, 'message': 'Print job queued again', 'job': serialize_print_job(job)})


@app.route('/api/printers/<printer_id>/status', methods=['POST'])
def update_printer_status(printer_id):
    """Toggle a printer between online and offline."""
    try:
        printer = get_printer(printer_id)
        if not printer:
            return jsonify({'success': False, 'error': 'Printer not found'}), 404
        data = request.get_json() or {}
        status = data.get('status', 'Online')
        if status not in ['Online', 'Offline']:
            return jsonify({'success': False, 'error': 'Status must be Online or Offline'}), 400
        printer['status'] = status
        refresh_print_system()
        log_event('printer_status_changed', {'printer_id': printer_id, 'status': status})
        return jsonify({'success': True, 'printer': printer})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/printers/install', methods=['POST'])
def install_printer():
    """Install a simulated printer driver and printer."""
    try:
        data = request.get_json() or {}
        name = data.get('name') or f'Lab Printer {len(printers) + 1}'
        printer_id = ''.join(ch.lower() if ch.isalnum() else '-' for ch in name).strip('-')
        if get_printer(printer_id):
            printer_id = f'{printer_id}-{len(printers) + 1}'
        printer = {
            'id': printer_id,
            'name': name,
            'driver': data.get('driver') or 'Generic PusoyOS Driver',
            'location': data.get('location') or 'Local',
            'status': 'Online',
            'default': False,
        }
        printers.append(printer)
        log_event('printer_driver_installed', {'printer_id': printer_id, 'name': name})
        return jsonify({'success': True, 'message': 'Printer installed', 'printer': printer})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


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
        new_metrics = calculate_system_metrics()
        
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
    files_payload = simulator.get_files()
    files_payload['entries'] = [serialize_file_entry(f) for f in simulator.filesystem.get_all_files()]
    return jsonify(files_payload)


@app.route('/api/fs/list', methods=['GET'])
def fs_list():
    """List a virtual folder with optional search."""
    path = request.args.get('path', HOME_PATH)
    search = request.args.get('search', '')
    return jsonify({
        'success': True,
        **list_virtual_directory(path, search)
    })


@app.route('/api/fs/open', methods=['POST'])
def fs_open():
    """Open a file and return content plus its associated application."""
    try:
        data = request.get_json() or {}
        path = data.get('path') or data.get('filename')
        if not path:
            return jsonify({'success': False, 'error': 'Path is required'}), 400
        file_obj = get_file_by_path(path)
        if not file_obj:
            return jsonify({'success': False, 'error': 'File not found'}), 404
        content = file_obj.read()
        entry = serialize_file_entry(file_obj)
        log_event('file_opened', {'path': entry['path'], 'association': entry['association']})
        return jsonify({'success': True, 'entry': entry, 'content': content})
    except Exception as e:
        log_event('file_open_error', {'error': str(e)})
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/fs/create-file', methods=['POST'])
def fs_create_file():
    """Create a file in a virtual folder."""
    try:
        data = request.get_json() or {}
        name = data.get('name') or data.get('filename') or 'untitled.txt'
        directory = data.get('directory') or data.get('parent') or HOME_PATH
        content = data.get('content', '')
        path = data.get('path') or normalize_desktop_path(parent=directory, name=name)
        if get_file_by_path(path):
            return jsonify({'success': False, 'error': 'File already exists'}), 400
        file_obj = create_virtual_file(path, content=content, owner='student')
        if not file_obj:
            return jsonify({'success': False, 'error': 'Unable to create file'}), 400
        entry = serialize_file_entry(file_obj)
        log_event('file_created', {'path': entry['path'], 'size': len(content)})
        return jsonify({'success': True, 'message': 'File created', 'entry': entry})
    except Exception as e:
        log_event('file_creation_error', {'error': str(e)})
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/fs/create-folder', methods=['POST'])
def fs_create_folder():
    """Create a virtual folder."""
    try:
        data = request.get_json() or {}
        name = posixpath.basename((data.get('name') or 'New Folder').strip().replace('\\', '/'))
        directory = normalize_desktop_path(data.get('directory') or data.get('parent') or HOME_PATH)
        path = normalize_desktop_path(parent=directory, name=name)
        if path in VIRTUAL_DIRECTORIES or get_file_by_path(path):
            return jsonify({'success': False, 'error': 'Folder already exists'}), 400
        VIRTUAL_DIRECTORIES.add(path)
        log_event('folder_created', {'path': path})
        return jsonify({'success': True, 'message': 'Folder created', 'entry': serialize_folder_entry(path)})
    except Exception as e:
        log_event('folder_creation_error', {'error': str(e)})
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/fs/save', methods=['POST'])
def fs_save():
    """Save content to a virtual file, creating it if needed."""
    try:
        data = request.get_json() or {}
        path = data.get('path')
        filename = data.get('filename')
        content = data.get('content', '')
        if not path and filename:
            path = normalize_desktop_path(filename)
        if not path:
            return jsonify({'success': False, 'error': 'Path is required'}), 400

        normalized = normalize_desktop_path(path)
        file_obj = get_file_by_path(normalized)
        if file_obj:
            success = simulator.filesystem.write_file(relative_file_key(normalized), content)
            if not success:
                return jsonify({'success': False, 'error': 'Write failed'}), 500
            file_obj = get_file_by_path(normalized)
        else:
            file_obj = create_virtual_file(normalized, content=content, owner='student')
            if not file_obj:
                return jsonify({'success': False, 'error': 'Create failed'}), 400
        entry = serialize_file_entry(file_obj)
        log_event('file_saved', {'path': entry['path'], 'size': len(content)})
        return jsonify({'success': True, 'message': 'File saved', 'entry': entry})
    except Exception as e:
        log_event('file_save_error', {'error': str(e)})
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/fs/rename', methods=['POST'])
def fs_rename():
    """Rename a file or folder."""
    try:
        data = request.get_json() or {}
        success, message = rename_virtual_path(data.get('path'), data.get('new_name'))
        status = 200 if success else 400
        log_event('item_renamed' if success else 'item_rename_failed', {
            'path': data.get('path'),
            'new_name': data.get('new_name'),
            'message': message
        })
        return jsonify({'success': success, 'message': message}), status
    except Exception as e:
        log_event('rename_error', {'error': str(e)})
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/fs/delete', methods=['POST'])
def fs_delete():
    """Delete a file or folder."""
    try:
        data = request.get_json() or {}
        success, message = delete_virtual_path(data.get('path'))
        status = 200 if success else 400
        log_event('item_deleted' if success else 'item_delete_failed', {
            'path': data.get('path'),
            'message': message
        })
        return jsonify({'success': success, 'message': message}), status
    except Exception as e:
        log_event('delete_error', {'error': str(e)})
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/fs/move', methods=['POST'])
def fs_move():
    """Move a file or folder into a virtual folder."""
    try:
        data = request.get_json() or {}
        success, message = move_virtual_path(data.get('source_path'), data.get('destination_folder'))
        status = 200 if success else 400
        log_event('item_moved' if success else 'item_move_failed', {
            'source': data.get('source_path'),
            'destination': data.get('destination_folder'),
            'message': message
        })
        return jsonify({'success': success, 'message': message}), status
    except Exception as e:
        log_event('move_error', {'error': str(e)})
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/create-file', methods=['POST'])
def create_file():
    """Create a file"""
    try:
        data = request.get_json() or {}
        filename = data.get('filename', 'new_file.txt')
        content = data.get('content', '')
        path = data.get('path') or normalize_desktop_path(filename)
        
        if not filename or not filename.strip():
            return jsonify({'success': False, 'error': 'Filename cannot be empty'}), 400
        
        file_obj = create_virtual_file(path, content=content, owner='student')
        
        if file_obj:
            entry = serialize_file_entry(file_obj)
            log_event('file_created', {'filename': filename, 'path': entry['path'], 'size': len(content)})
            return jsonify({
                'success': True,
                'message': f'File created: {filename}',
                'file': file_obj.to_dict(),
                'entry': entry
            })
        else:
            log_event('file_creation_failed', {'filename': filename, 'reason': 'file_exists_or_limit_reached'})
            return jsonify({'success': False, 'error': 'Failed to create file - file may already exist or file limit reached'}), 400
    except Exception as e:
        log_event('file_creation_error', {'error': str(e)})
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/delete-file', methods=['POST'])
def delete_file():
    """Delete a file"""
    try:
        data = request.get_json() or {}
        filename = data.get('filename')
        path = data.get('path') or filename
        
        if not path:
            return jsonify({'success': False, 'error': 'Filename is required'}), 400
        
        success, message = delete_virtual_path(path)
        
        if success:
            log_event('file_deleted', {'filename': filename, 'path': normalize_desktop_path(path)})
            return jsonify({
                'success': True,
                'message': message,
                'filename': filename
            })
        else:
            log_event('file_deletion_failed', {'filename': filename, 'reason': 'not_found'})
            return jsonify({'success': False, 'error': f'File not found: {filename}'}), 404
    except Exception as e:
        log_event('file_deletion_error', {'error': str(e)})
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/read-file', methods=['POST'])
def read_file():
    """Read file content"""
    try:
        data = request.get_json() or {}
        filename = data.get('filename')
        path = data.get('path') or filename
        if not path:
            return jsonify({'success': False, 'content': None, 'error': 'Filename is required'}), 400
        
        file_obj = get_file_by_path(path)
        if file_obj:
            content = file_obj.read()
            entry = serialize_file_entry(file_obj)
            log_event('file_read', {'filename': filename, 'path': entry['path'], 'size': len(content)})
            return jsonify({'success': True, 'content': content, 'entry': entry})
        else:
            log_event('file_read_failed', {'filename': filename, 'reason': 'not_found'})
            return jsonify({'success': False, 'content': None, 'error': 'File not found'}), 404
    except Exception as e:
        log_event('file_read_error', {'error': str(e)})
        return jsonify({'success': False, 'content': None, 'error': str(e)}), 400


@app.route('/api/write-file', methods=['POST'])
def write_file():
    """Create or update a file's content."""
    try:
        data = request.get_json() or {}
        filename = data.get('filename')
        path = data.get('path') or filename
        content = data.get('content', '')

        if not path:
            return jsonify({'success': False, 'message': 'Filename is required'}), 400

        normalized = normalize_desktop_path(path)
        file_obj = get_file_by_path(normalized)
        if file_obj:
            success = simulator.filesystem.write_file(relative_file_key(normalized), content)
            if success:
                file_obj = get_file_by_path(normalized)
                entry = serialize_file_entry(file_obj)
                log_event('file_saved', {'filename': filename, 'path': entry['path'], 'size': len(content)})
                return jsonify({
                    'success': True,
                    'filename': filename or entry['name'],
                    'message': 'File saved successfully',
                    'size': len(content),
                    'entry': entry
                })
            else:
                log_event('file_save_failed', {'filename': filename, 'reason': 'write_error'})
                return jsonify({'success': False, 'error': 'Failed to write file'}), 500
        else:
            file_obj = create_virtual_file(normalized, content=content, owner='student')
            if file_obj:
                entry = serialize_file_entry(file_obj)
                log_event('file_created', {'filename': filename, 'path': entry['path'], 'size': len(content)})
                return jsonify({
                    'success': True,
                    'filename': filename or entry['name'],
                    'message': 'File created successfully',
                    'size': len(content),
                    'file': file_obj.to_dict(),
                    'entry': entry
                })
            else:
                log_event('file_creation_failed', {'filename': filename})
                return jsonify({'success': False, 'error': 'Failed to create file'}), 400

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
        data = request.get_json() or {}
        for key in ['theme', 'wallpaper', 'accent']:
            if key in data:
                system_preferences[key] = data[key]
        log_event('settings_updated', system_preferences.copy())
        return jsonify({'success': True, 'message': 'Settings updated', 'settings': system_preferences})
    else:
        # Get settings
        return jsonify({
            'settings': {
                **system_preferences,
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

