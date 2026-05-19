"""
PusoyOS Applications Module
Manages running applications and their lifecycle
"""

from datetime import datetime
from config import APPLICATIONS


class Application:
    """Represents a running application"""
    
    def __init__(self, app_id, name, cpu_usage, memory_required, instance_id):
        self.app_id = app_id
        self.instance_id = instance_id
        self.name = name
        self.cpu_usage = cpu_usage
        self.memory_required = memory_required
        self.pid = None
        self.status = 'running'
        self.window_open = True
        self.window_count = 1
        self.window_state = 'open'
        self.active = False
        self.start_time = datetime.now()
        self.last_active_at = None
        self.cpu_time = 0
        self.memory_used = 0
        self.threads = 1
        self.file_descriptors = []
    
    def update_metrics(self, cpu_time, memory_used):
        """Update application metrics"""
        self.cpu_time += cpu_time
        self.memory_used = memory_used
    
    def get_uptime(self):
        """Get application uptime in seconds"""
        return (datetime.now() - self.start_time).total_seconds()

    def open_window(self):
        """Register an additional window for this application process."""
        self.window_count += 1
        self.window_open = True
        self.status = 'running'
        if self.window_state in ('closed', 'minimized'):
            self.window_state = 'open'

    def close_window(self):
        """Release one window and return whether the process still owns windows."""
        self.window_count = max(0, self.window_count - 1)
        self.window_open = self.window_count > 0
        if self.window_open:
            if self.window_state == 'closed':
                self.window_state = 'open'
            return True
        self.status = 'closed'
        self.window_state = 'closed'
        self.active = False
        return False

    def update_window_state(self, window_state=None, window_count=None, active=None):
        """Synchronize browser window state with the application process."""
        if window_count is not None:
            self.window_count = max(0, int(window_count))
            self.window_open = self.window_count > 0

        if window_state:
            self.window_state = window_state
            self.window_open = window_state != 'closed' and self.window_count > 0

        if active is not None:
            self.active = bool(active)
            if self.active:
                self.last_active_at = datetime.now()

        self.status = 'running' if self.window_open else 'closed'
    
    def to_dict(self):
        """Convert application to dictionary"""
        return {
            'instance_id': self.instance_id,
            'app_id': self.app_id,
            'name': self.name,
            'pid': self.pid,
            'status': self.status,
            'opened_at': self.start_time.isoformat(),
            'window_state': self.window_state if self.window_open else 'closed',
            'window_count': self.window_count,
            'active': self.active,
            'last_active_at': self.last_active_at.isoformat() if self.last_active_at else None,
            'cpu_usage_percent': self.cpu_usage,
            'memory_required': self.memory_required,
            'memory_used': self.memory_used,
            'cpu_time': self.cpu_time,
            'uptime_seconds': self.get_uptime(),
            'threads': self.threads,
            'window_open': self.window_open
        }


class ApplicationManager:
    """Manages applications running on PusoyOS"""
    
    def __init__(self):
        self.applications = APPLICATIONS  # Available apps
        self.running_apps = {}  # {instance_id: Application}
        self.instance_counter = 0

    def _next_instance_id(self, app_id):
        """Create a stable application instance id for multi-process apps."""
        self.instance_counter += 1
        return f'{app_id}-{self.instance_counter}'

    def get_application_by_pid(self, pid):
        """Find a running application by process id."""
        if pid is None:
            return None
        numeric_pid = int(pid)
        return next((app for app in self.running_apps.values() if app.pid == numeric_pid), None)

    def get_applications_by_app_id(self, app_id):
        """Return all running instances for an application id."""
        return [app for app in self.running_apps.values() if app.app_id == app_id]

    def get_primary_application(self, app_id):
        """Return the first running instance for compatibility paths."""
        return next((app for app in self.running_apps.values() if app.app_id == app_id), None)
    
    def launch_application(self, app_id, instance_id=None, singleton=False):
        """Launch an application"""
        if app_id not in self.applications:
            return {'success': False, 'message': 'Application not found'}

        if singleton:
            app = self.get_primary_application(app_id)
            if app:
                return {
                    'success': True,
                    'message': f'{app.name} already running',
                    'app': app.to_dict(),
                    'already_running': True
                }

        instance_id = instance_id or self._next_instance_id(app_id)
        if instance_id in self.running_apps:
            app = self.running_apps[instance_id]
            return {
                'success': True,
                'message': f'{app.name} already running',
                'app': app.to_dict(),
                'already_running': True
            }
        
        app_info = self.applications[app_id]
        app = Application(
            app_id,
            app_info['name'],
            app_info['cpu_usage'],
            app_info['memory_required'],
            instance_id
        )
        
        self.running_apps[instance_id] = app
        return {
            'success': True,
            'message': f'{app_info["name"]} launched',
            'app': app.to_dict()
        }
    
    def resolve_application(self, app_id=None, instance_id=None, pid=None):
        """Resolve a running app from the most specific identifier available."""
        if pid is not None:
            app = self.get_application_by_pid(pid)
            if app:
                return app
        if instance_id and instance_id in self.running_apps:
            return self.running_apps[instance_id]
        if app_id:
            return self.get_primary_application(app_id)
        return None

    def close_application(self, app_id=None, instance_id=None, pid=None, force=False):
        """Close a running application or release one owned window."""
        app = self.resolve_application(app_id, instance_id, pid)
        if not app:
            return {'success': False, 'message': 'Application not running'}
        
        if not force and app.close_window():
            return {
                'success': True,
                'message': f'{app.name} window closed',
                'app': app.to_dict(),
                'still_running': True
            }

        app.window_open = False
        app.status = 'closed'
        app.window_count = 0
        app.window_state = 'closed'
        app.active = False
        self.running_apps.pop(app.instance_id, None)
        return {'success': True, 'message': f'{app.name} closed'}
    
    def kill_application(self, app_id):
        """Force kill an application"""
        return self.close_application(app_id=app_id, force=True)
    
    def get_running_applications(self):
        """Get list of running applications"""
        return [app.to_dict() for app in self.running_apps.values()]
    
    def get_available_applications(self):
        """Get list of available applications with running status"""
        available = []
        for app_id, app_info in self.applications.items():
            if not app_info.get('desktop', False):
                continue
            available.append({
                'app_id': app_id,
                'name': app_info['name'],
                'icon': app_info['icon'],
                'category': app_info['category'],
                'description': app_info['description'],
                'cpu_usage': app_info['cpu_usage'],
                'memory_required': app_info['memory_required'],
                'running': any(app.app_id == app_id for app in self.running_apps.values())
            })
        return sorted(available, key=lambda app: app['name'].lower())
    
    def get_application(self, app_id=None, instance_id=None, pid=None):
        """Get running application"""
        return self.resolve_application(app_id, instance_id, pid)

    def update_window_state(self, app_id=None, instance_id=None, pid=None, window_state=None, window_count=None, active=None):
        """Update window state for a running app."""
        app = self.resolve_application(app_id, instance_id, pid)
        if not app:
            return {'success': True, 'message': 'Application is not running'}
        app.update_window_state(window_state, window_count, active)
        return {'success': True, 'app': app.to_dict()}
    
    def update_application_metrics(self, app_id, cpu_time, memory_used):
        """Update application metrics"""
        for app in self.get_applications_by_app_id(app_id):
            app.update_metrics(cpu_time, memory_used)
    
    def get_application_info(self, app_id):
        """Get application information"""
        if app_id in self.applications:
            return self.applications[app_id]
        return None
    
    def get_running_count(self):
        """Get count of running applications"""
        return len(self.running_apps)
    
    def get_total_cpu_usage(self):
        """Get total CPU usage of all running apps"""
        return sum(app.cpu_usage for app in self.running_apps.values())
    
    def get_total_memory_usage(self):
        """Get total memory usage of all running apps"""
        return sum(app.memory_required for app in self.running_apps.values())
