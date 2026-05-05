"""
PusoyOS I/O System Module
Manages I/O devices, requests, and advanced disk scheduling algorithms
"""

from collections import deque
from config import IO_DEVICES


class IORequest:
    """Represents an I/O request"""
    _request_id = 5000
    
    def __init__(self, process_pid, device_name, operation='read', data_size=512, disk_cylinder=0):
        self.request_id = IORequest._request_id
        IORequest._request_id += 1
        
        self.process_pid = process_pid
        self.device_name = device_name
        self.operation = operation  # 'read' or 'write'
        self.data_size = data_size
        self.disk_cylinder = disk_cylinder  # Cylinder address for disk operations
        self.status = 'pending'
        self.start_time = None
        self.completion_time = None
        self.wait_time = 0
        self.seek_time = 0


class IODevice:
    """Represents an I/O device with advanced scheduling"""
    
    def __init__(self, name, device_type, service_time, scheduling_algorithm='fifo'):
        self.name = name
        self.device_type = device_type  # 'block' or 'character'
        self.service_time = service_time  # ms per operation
        self.request_queue = deque()
        self.current_request = None
        self.completed_requests = 0
        self.total_service_time = 0
        self.total_seek_time = 0
        self.device_busy = False
        
        # Disk scheduling
        self.scheduling_algorithm = scheduling_algorithm  # 'fifo', 'scan', 'cscan', 'look', 'clook'
        self.disk_head_position = 0  # Current head position (0-200 cylinders)
        self.max_cylinder = 200
        self.head_direction = 1  # 1 for moving right (high), -1 for moving left (low)
        
        # Cache
        self.cache = {}  # {cylinder: cached_data}
        self.cache_hits = 0
        self.cache_misses = 0
        self.max_cache_size = 20
    
    def set_scheduling_algorithm(self, algorithm):
        """Change scheduling algorithm"""
        if algorithm in ['fifo', 'scan', 'cscan', 'look', 'clook']:
            self.scheduling_algorithm = algorithm
            return True
        return False
    
    def _calculate_seek_time(self, from_cylinder, to_cylinder):
        """Calculate seek time (proportional to distance)"""
        distance = abs(to_cylinder - from_cylinder)
        seek_time = distance * 0.5  # 0.5ms per cylinder
        return seek_time
    
    def _get_next_request_fifo(self):
        """FIFO: First In First Out"""
        return self.request_queue[0] if self.request_queue else None
    
    def _get_next_request_scan(self):
        """SCAN: Move head from one end to other, servicing requests"""
        if not self.request_queue:
            return None
        
        # Find closest request in current direction
        closest = None
        closest_distance = float('inf')
        
        for req in self.request_queue:
            if self.head_direction == 1:
                # Moving right, prefer requests to the right
                if req.disk_cylinder >= self.disk_head_position:
                    distance = req.disk_cylinder - self.disk_head_position
                    if distance < closest_distance:
                        closest = req
                        closest_distance = distance
            else:
                # Moving left, prefer requests to the left
                if req.disk_cylinder <= self.disk_head_position:
                    distance = self.disk_head_position - req.disk_cylinder
                    if distance < closest_distance:
                        closest = req
                        closest_distance = distance
        
        # If no request in current direction, reverse and get closest
        if closest is None:
            self.head_direction *= -1
            return self._get_next_request_scan()
        
        return closest
    
    def _get_next_request_cscan(self):
        """C-SCAN: Circular SCAN (always return to cylinder 0)"""
        if not self.request_queue:
            return None
        
        # Always prefer requests ahead in current direction
        closest = None
        closest_distance = float('inf')
        
        for req in self.request_queue:
            if self.head_direction == 1:
                if req.disk_cylinder >= self.disk_head_position:
                    distance = req.disk_cylinder - self.disk_head_position
                    if distance < closest_distance:
                        closest = req
                        closest_distance = distance
            else:
                if req.disk_cylinder <= self.disk_head_position:
                    distance = self.disk_head_position - req.disk_cylinder
                    if distance < closest_distance:
                        closest = req
                        closest_distance = distance
        
        # If no request ahead, jump to other end
        if closest is None:
            self.disk_head_position = self.max_cylinder if self.head_direction == 1 else 0
            self.head_direction *= -1
            return self._get_next_request_cscan()
        
        return closest
    
    def _get_next_request_look(self):
        """LOOK: Like SCAN but stop at last request"""
        if not self.request_queue:
            return None
        
        # Find closest request in current direction
        closest = None
        closest_distance = float('inf')
        
        for req in self.request_queue:
            if self.head_direction == 1:
                if req.disk_cylinder >= self.disk_head_position:
                    distance = req.disk_cylinder - self.disk_head_position
                    if distance < closest_distance:
                        closest = req
                        closest_distance = distance
            else:
                if req.disk_cylinder <= self.disk_head_position:
                    distance = self.disk_head_position - req.disk_cylinder
                    if distance < closest_distance:
                        closest = req
                        closest_distance = distance
        
        # If no request in current direction, reverse
        if closest is None:
            self.head_direction *= -1
            return self._get_next_request_look()
        
        return closest
    
    def _get_next_request_clook(self):
        """C-LOOK: Circular LOOK"""
        if not self.request_queue:
            return None
        
        closest = None
        closest_distance = float('inf')
        
        for req in self.request_queue:
            if self.head_direction == 1:
                if req.disk_cylinder >= self.disk_head_position:
                    distance = req.disk_cylinder - self.disk_head_position
                    if distance < closest_distance:
                        closest = req
                        closest_distance = distance
            else:
                if req.disk_cylinder <= self.disk_head_position:
                    distance = self.disk_head_position - req.disk_cylinder
                    if distance < closest_distance:
                        closest = req
                        closest_distance = distance
        
        # If no request ahead, jump to other end
        if closest is None:
            self.disk_head_position = 0 if self.head_direction == 1 else self.max_cylinder
            self.head_direction *= -1
            return self._get_next_request_clook()
        
        return closest
    
    def add_request(self, request):
        """Add I/O request to queue"""
        # Check cache first
        if request.disk_cylinder in self.cache and request.operation == 'read':
            self.cache_hits += 1
            request.status = 'completed'
            return True
        else:
            self.cache_misses += 1
        
        self.request_queue.append(request)
        return True
    
    def get_next_request(self):
        """Get next request based on scheduling algorithm"""
        if self.scheduling_algorithm == 'fifo':
            return self._get_next_request_fifo()
        elif self.scheduling_algorithm == 'scan':
            return self._get_next_request_scan()
        elif self.scheduling_algorithm == 'cscan':
            return self._get_next_request_cscan()
        elif self.scheduling_algorithm == 'look':
            return self._get_next_request_look()
        elif self.scheduling_algorithm == 'clook':
            return self._get_next_request_clook()
        else:
            return self._get_next_request_fifo()
    
    def process_request(self):
        """Process next request in queue"""
        if self.current_request and self.current_request.status == 'completed':
            self.current_request = None
        
        if not self.current_request and self.request_queue:
            self.current_request = self.get_next_request()
            if self.current_request:
                self.request_queue.remove(self.current_request)
                
                # Calculate seek time
                seek_time = self._calculate_seek_time(self.disk_head_position, self.current_request.disk_cylinder)
                self.current_request.seek_time = seek_time
                self.total_seek_time += seek_time
                
                # Update head position
                self.disk_head_position = self.current_request.disk_cylinder
                
                self.current_request.status = 'processing'
                self.device_busy = True
            return self.current_request
        
        return None
    
    def complete_request(self):
        """Complete current request"""
        if self.current_request:
            self.current_request.status = 'completed'
            self.completed_requests += 1
            self.total_service_time += self.service_time
            
            # Update cache
            if len(self.cache) < self.max_cache_size:
                self.cache[self.current_request.disk_cylinder] = True
            
            self.device_busy = False
            return self.current_request
        return None
    
    def get_queue_size(self):
        """Get request queue size"""
        return len(self.request_queue)
    
    def is_busy(self):
        """Check if device is busy"""
        return self.device_busy or len(self.request_queue) > 0
    
    def get_device_info(self):
        """Get device information"""
        return {
            'name': self.name,
            'type': self.device_type,
            'service_time_ms': self.service_time,
            'queue_size': self.get_queue_size(),
            'is_busy': self.is_busy(),
            'completed_requests': self.completed_requests,
            'total_service_time': self.total_service_time,
            'scheduling_algorithm': self.scheduling_algorithm,
            'disk_head_position': self.disk_head_position,
            'total_seek_time': self.total_seek_time,
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'cache_hit_rate': (self.cache_hits / max(1, self.cache_hits + self.cache_misses)) * 100
        }


class IOSystem:
    """Manages all I/O devices and requests"""
    
    def __init__(self, disk_scheduling='fifo'):
        self.devices = {}
        self.all_requests = []
        self.completed_requests = 0
        self.disk_scheduling = disk_scheduling  # Global disk scheduling algorithm
        self._initialize_devices()
    
    def _initialize_devices(self):
        """Initialize I/O devices"""
        for dev_name, dev_config in IO_DEVICES.items():
            # For disk device, use specified scheduling algorithm
            algo = self.disk_scheduling if dev_config['type'] == 'block' else 'fifo'
            
            device = IODevice(
                dev_config['name'],
                dev_config['type'],
                dev_config['service_time'],
                algo
            )
            self.devices[dev_name] = device
    
    def set_disk_scheduling_algorithm(self, algorithm):
        """Change disk scheduling algorithm for block devices"""
        if algorithm in ['fifo', 'scan', 'cscan', 'look', 'clook']:
            self.disk_scheduling = algorithm
            # Update all block devices
            for device in self.devices.values():
                if device.device_type == 'block':
                    device.set_scheduling_algorithm(algorithm)
            return True
        return False
    
    def submit_io_request(self, process_pid, device_name, operation='read', data_size=512, disk_cylinder=0):
        """Submit I/O request to device"""
        if device_name not in self.devices:
            return None
        
        request = IORequest(process_pid, device_name, operation, data_size, disk_cylinder)
        self.devices[device_name].add_request(request)
        self.all_requests.append(request)
        return request
    
    def process_io(self):
        """Process I/O for all devices"""
        for device in self.devices.values():
            device.process_request()
            if device.current_request:
                device.complete_request()
                self.completed_requests += 1
    
    def get_device(self, device_name):
        """Get device by name"""
        return self.devices.get(device_name)
    
    def get_all_devices(self):
        """Get all devices"""
        return list(self.devices.values())
    
    def get_io_status(self):
        """Get I/O system status"""
        devices_info = [d.get_device_info() for d in self.devices.values()]
        total_queue_size = sum(d['queue_size'] for d in devices_info)
        busy_devices = sum(1 for d in devices_info if d['is_busy'])
        total_seek_time = sum(d.get('total_seek_time', 0) for d in devices_info)
        total_cache_hits = sum(d.get('cache_hits', 0) for d in devices_info)
        
        return {
            'devices': devices_info,
            'total_queue_size': total_queue_size,
            'busy_devices': busy_devices,
            'completed_requests': self.completed_requests,
            'total_requests': len(self.all_requests),
            'disk_scheduling_algorithm': self.disk_scheduling,
            'total_seek_time': total_seek_time,
            'total_cache_hits': total_cache_hits
        }
    
    def get_device_info(self, device_name):
        """Get specific device information"""
        if device_name in self.devices:
            return self.devices[device_name].get_device_info()
        return None
