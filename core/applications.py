"""
PusoyOS Applications Module
Manages running applications and their lifecycle
"""

from datetime import datetime
from config import APPLICATIONS


class Application:
    """Represents a running application"""
    
    def __init__(self, app_id, name, cpu_usage, memory_required):
        self.app_id = app_id
        self.name = name
        self.cpu_usage = cpu_usage
        self.memory_required = memory_required
        self.pid = None
        self.status = 'running'
        self.window_open = True
        self.start_time = datetime.now()
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
    
    def to_dict(self):
        """Convert application to dictionary"""
        return {
            'app_id': self.app_id,
            'name': self.name,
            'pid': self.pid,
            'status': self.status,
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
        self.running_apps = {}  # {app_id: Application}
    
    def launch_application(self, app_id):
        """Launch an application"""
        if app_id not in self.applications:
            return {'success': False, 'message': 'Application not found'}
        
        if app_id in self.running_apps:
            return {'success': False, 'message': 'Application already running'}
        
        app_info = self.applications[app_id]
        app = Application(
            app_id,
            app_info['name'],
            app_info['cpu_usage'],
            app_info['memory_required']
        )
        
        self.running_apps[app_id] = app
        return {
            'success': True,
            'message': f'{app_info["name"]} launched',
            'app': app.to_dict()
        }
    
    def close_application(self, app_id):
        """Close a running application"""
        if app_id not in self.running_apps:
            return {'success': False, 'message': 'Application not running'}
        
        app = self.running_apps[app_id]
        app.window_open = False
        app.status = 'closed'
        del self.running_apps[app_id]
        return {'success': True, 'message': f'{app.name} closed'}
    
    def kill_application(self, app_id):
        """Force kill an application"""
        return self.close_application(app_id)
    
    def get_running_applications(self):
        """Get list of running applications"""
        return [app.to_dict() for app in self.running_apps.values()]
    
    def get_available_applications(self):
        """Get list of available applications with running status"""
        available = []
        for app_id, app_info in self.applications.items():
            available.append({
                'app_id': app_id,
                'name': app_info['name'],
                'icon': app_info['icon'],
                'category': app_info['category'],
                'description': app_info['description'],
                'cpu_usage': app_info['cpu_usage'],
                'memory_required': app_info['memory_required'],
                'running': app_id in self.running_apps
            })
        return available
    
    def get_application(self, app_id):
        """Get running application"""
        return self.running_apps.get(app_id)
    
    def update_application_metrics(self, app_id, cpu_time, memory_used):
        """Update application metrics"""
        if app_id in self.running_apps:
            self.running_apps[app_id].update_metrics(cpu_time, memory_used)
    
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
