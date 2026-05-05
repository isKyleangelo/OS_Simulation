# PusoyOS Configuration
# System-wide constants and settings

# System Information
SYSTEM_NAME = "PusoyOS"
SYSTEM_VERSION = "2.4.1"
KERNEL_VERSION = "2.4.1-generic"
HOSTNAME = "pusoy-workstation"

# CPU Configuration
CPU_CORES = 4
CPU_FREQUENCY = 2400  # MHz
TIME_QUANTUM = 5  # milliseconds for round-robin
CONTEXT_SWITCH_OVERHEAD = 1  # milliseconds

# Memory Configuration
TOTAL_MEMORY = 1024  # MB (1GB)
MEMORY_PARTITIONS = 4
PARTITION_SIZE = 256  # MB
PAGE_SIZE = 4  # KB
TOTAL_PAGES = (TOTAL_MEMORY * 1024) // PAGE_SIZE
SWAP_SIZE = 512  # MB

# Process Configuration
DEFAULT_PRIORITY = 1
MAX_PRIORITY = 10
MIN_PRIORITY = 0
MAX_PROCESSES = 128
PAGE_FAULT_PROBABILITY = 0.20  # 20% chance
SYSTEM_CALL_PROBABILITY = 0.15  # 15% chance

# I/O Configuration
IO_DEVICES = {
    'disk': {
        'name': 'Primary Disk Drive',
        'type': 'block',
        'service_time': 50  # ms per operation
    },
    'printer': {
        'name': 'Network Printer',
        'type': 'character',
        'service_time': 100  # ms per operation
    },
    'usb': {
        'name': 'USB Storage Device',
        'type': 'block',
        'service_time': 30  # ms per operation
    }
}

# File System Configuration
ROOT_DIRECTORY = '/home/pusoy'
MAX_FILES = 1000
DEFAULT_FILE_PERMISSIONS = '644'

# CLI Configuration
MEMORY_PARTITIONS_CLI = [100, 150, 200, 250]  # Different partition sizes for CLI
TOTAL_MEMORY_CLI = 700  # Total memory in units
TIME_QUANTUM_SCHEDULING = 5  # Time quantum for Round Robin

# Application Definitions
APPLICATIONS = {
    'firefox': {
        'name': 'Firefox Web Browser',
        'icon': '🌐',
        'category': 'internet',
        'cpu_usage': 15,  # percent
        'memory_required': 120,  # MB
        'description': 'Web Browsing'
    },
    'vscode': {
        'name': 'PusoyCode Editor',
        'icon': '💻',
        'category': 'development',
        'cpu_usage': 20,
        'memory_required': 150,
        'description': 'Code Development'
    },
    'filemanager': {
        'name': 'File Manager',
        'icon': '📁',
        'category': 'system',
        'cpu_usage': 5,
        'memory_required': 45,
        'description': 'File Browsing'
    },
    'terminal': {
        'name': 'PusoyShell Terminal',
        'icon': '⌨️',
        'category': 'system',
        'cpu_usage': 2,
        'memory_required': 25,
        'description': 'Command Line'
    },
    'settings': {
        'name': 'System Settings',
        'icon': '⚙️',
        'category': 'system',
        'cpu_usage': 3,
        'memory_required': 40,
        'description': 'Configuration'
    },
    'taskmanager': {
        'name': 'Task Manager',
        'icon': '📊',
        'category': 'system',
        'cpu_usage': 4,
        'memory_required': 35,
        'description': 'Process Monitor'
    },
    'mediaplay': {
        'name': 'Media Player',
        'icon': '🎵',
        'category': 'media',
        'cpu_usage': 10,
        'memory_required': 70,
        'description': 'Audio/Video'
    },
    'messenger': {
        'name': 'Messenger',
        'icon': '💬',
        'category': 'communication',
        'cpu_usage': 12,
        'memory_required': 85,
        'description': 'Messaging'
    }
}

# Scheduling Algorithms
SCHEDULING_ALGORITHMS = ['round_robin', 'fcfs', 'priority']
DEFAULT_SCHEDULING = 'round_robin'

# Logging
SIMULATION_LOG_SIZE = 10000  # max log entries
ENABLE_DEBUG_LOGGING = True

# UI Settings
THEME = 'dark'
RESOLUTION = '1920x1080'
AUTO_LAUNCH_APPS = ['filemanager', 'taskmanager', 'settings']
