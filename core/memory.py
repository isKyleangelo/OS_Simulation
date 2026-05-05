"""
PusoyOS Memory Management Module
Handles physical memory, virtual memory, page faults, and page replacement
"""

from collections import defaultdict
from config import (
    TOTAL_MEMORY, MEMORY_PARTITIONS, PARTITION_SIZE, PAGE_SIZE,
    TOTAL_PAGES, SWAP_SIZE
)


class PageFrame:
    """Represents a page in memory"""
    
    def __init__(self, page_number, process_pid=None):
        self.page_number = page_number
        self.process_pid = process_pid
        self.in_memory = False
        self.dirty = False
        self.last_accessed = 0
        self.access_count = 0


class VirtualMemory:
    """Manages virtual memory and page faults"""
    
    def __init__(self, swap_size=SWAP_SIZE):
        self.swap_size = swap_size  # MB
        self.swap_pages = {}  # {page_num: data}
        self.page_table = {}  # {pid: {virtual_page: physical_frame}}
        self.page_faults = 0
        self.page_hits = 0
    
    def allocate_virtual_memory(self, pid, num_pages):
        """Allocate virtual memory for a process"""
        if pid not in self.page_table:
            self.page_table[pid] = {}
        return True
    
    def access_page(self, pid, virtual_page):
        """Access a page - may cause page fault"""
        if pid not in self.page_table:
            self.page_table[pid] = {}
        
        if virtual_page in self.page_table[pid]:
            self.page_hits += 1
            return True
        else:
            self.page_faults += 1
            return False
    
    def page_in(self, pid, virtual_page, physical_frame):
        """Load page from swap into physical memory"""
        if pid not in self.page_table:
            self.page_table[pid] = {}
        
        self.page_table[pid][virtual_page] = physical_frame
        return True
    
    def page_out(self, pid, virtual_page):
        """Swap page from physical to virtual memory"""
        if pid in self.page_table and virtual_page in self.page_table[pid]:
            del self.page_table[pid][virtual_page]
            return True
        return False
    
    def get_page_fault_rate(self):
        """Get page fault rate"""
        total = self.page_faults + self.page_hits
        if total == 0:
            return 0.0
        return (self.page_faults / total) * 100


class MemoryManager:
    """Manages physical memory allocation and deallocation"""
    
    def __init__(self, allocation_algorithm='first_fit'):
        self.physical_memory = TOTAL_MEMORY
        self.partitions = [
            {'size': PARTITION_SIZE, 'allocated': False, 'process_pid': None, 'allocated_size': 0}
            for _ in range(MEMORY_PARTITIONS)
        ]
        self.allocated_memory = defaultdict(int)  # {pid: allocated_mb}
        self.virtual_memory = VirtualMemory()
        self.lru_cache = {}  # {pid: [pages in LRU order]}
        self.page_replacements = 0
        self.allocation_algorithm = allocation_algorithm  # 'dynamic', 'first_fit', 'best_fit', 'worst_fit'
        self.fragmentation_ratio = 0.0
        self.allocation_attempts = 0
        self.allocation_failures = 0
    
    def set_allocation_algorithm(self, algorithm):
        """Change memory allocation algorithm"""
        if algorithm in ['dynamic', 'first_fit', 'best_fit', 'worst_fit']:
            self.allocation_algorithm = algorithm
            return True
        return False
    
    def _find_partition_first_fit(self, memory_required):
        """First Fit: Allocate to first partition that fits"""
        for idx, partition in enumerate(self.partitions):
            if not partition['allocated'] and partition['size'] >= memory_required:
                return idx
        return -1
    
    def _find_partition_best_fit(self, memory_required):
        """Best Fit: Allocate to smallest partition that fits"""
        best_idx = -1
        best_size = float('inf')
        
        for idx, partition in enumerate(self.partitions):
            if not partition['allocated'] and partition['size'] >= memory_required:
                if partition['size'] < best_size:
                    best_size = partition['size']
                    best_idx = idx
        
        return best_idx
    
    def _find_partition_worst_fit(self, memory_required):
        """Worst Fit: Allocate to largest available partition"""
        worst_idx = -1
        worst_size = -1
        
        for idx, partition in enumerate(self.partitions):
            if not partition['allocated'] and partition['size'] >= memory_required:
                if partition['size'] > worst_size:
                    worst_size = partition['size']
                    worst_idx = idx
        
        return worst_idx
    
    def allocate_memory(self, process_pid, memory_required):
        """Allocate memory for a process using selected algorithm"""
        self.allocation_attempts += 1
        available = self.get_available_memory()
        
        if memory_required > available:
            self.allocation_failures += 1
            return False
        
        # Use dynamic allocation - simple and effective
        if self.allocation_algorithm == 'dynamic':
            self.allocated_memory[process_pid] = memory_required
            
            # Allocate virtual memory pages
            pages_needed = (memory_required * 1024) // PAGE_SIZE
            self.virtual_memory.allocate_virtual_memory(process_pid, pages_needed)
            
            return True
        
        # Use partition-based allocation for other algorithms
        # Find suitable partition based on algorithm
        if self.allocation_algorithm == 'first_fit':
            partition_idx = self._find_partition_first_fit(memory_required)
        elif self.allocation_algorithm == 'best_fit':
            partition_idx = self._find_partition_best_fit(memory_required)
        elif self.allocation_algorithm == 'worst_fit':
            partition_idx = self._find_partition_worst_fit(memory_required)
        else:
            partition_idx = self._find_partition_best_fit(memory_required)
        
        if partition_idx == -1:
            self.allocation_failures += 1
            return False
        
        # Allocate the partition
        self.partitions[partition_idx]['allocated'] = True
        self.partitions[partition_idx]['process_pid'] = process_pid
        self.partitions[partition_idx]['allocated_size'] = memory_required
        self.allocated_memory[process_pid] = memory_required
        
        # Allocate virtual memory pages
        pages_needed = (memory_required * 1024) // PAGE_SIZE
        self.virtual_memory.allocate_virtual_memory(process_pid, pages_needed)
        
        # Update fragmentation
        self._update_fragmentation()
        
        return True
    
    def deallocate_memory(self, process_pid):
        """Deallocate memory for a process"""
        # Free up allocated partition
        for partition in self.partitions:
            if partition['process_pid'] == process_pid:
                partition['allocated'] = False
                partition['process_pid'] = None
                partition['allocated_size'] = 0
        
        # Free up allocated memory tracking
        if process_pid in self.allocated_memory:
            del self.allocated_memory[process_pid]
        
        # Clean up virtual memory
        if process_pid in self.virtual_memory.page_table:
            del self.virtual_memory.page_table[process_pid]
        
        # Clean up LRU cache
        if process_pid in self.lru_cache:
            del self.lru_cache[process_pid]
        
        # Update fragmentation
        self._update_fragmentation()
    
    def get_available_memory(self):
        """Get available free memory"""
        used = self.get_allocated_memory()
        return self.physical_memory - used
    
    def get_allocated_memory(self):
        """Get total allocated memory"""
        return sum(self.allocated_memory.values())
    
    def get_memory_status(self):
        """Get memory status"""
        allocated = self.get_allocated_memory()
        available = self.get_available_memory()
        
        return {
            'total': self.physical_memory,
            'allocated': allocated,
            'available': available,
            'percentage_used': (allocated / self.physical_memory) * 100,
            'process_count': len(self.allocated_memory),
            'page_faults': self.virtual_memory.page_faults,
            'page_hits': self.virtual_memory.page_hits,
            'page_fault_rate': self.virtual_memory.get_page_fault_rate(),
            'page_replacements': self.page_replacements,
            'allocation_algorithm': self.allocation_algorithm,
            'fragmentation_ratio': self.fragmentation_ratio,
            'allocation_efficiency': (self.allocation_attempts - self.allocation_failures) / max(1, self.allocation_attempts) * 100
        }
    
    def _update_fragmentation(self):
        """Calculate fragmentation ratio"""
        free_partitions = [p for p in self.partitions if not p['allocated']]
        if not free_partitions:
            self.fragmentation_ratio = 0.0
            return
        
        # Internal fragmentation: wasted space in allocated partitions
        wasted_space = 0
        for p in self.partitions:
            if p['allocated']:
                wasted_space += p['size'] - p['allocated_size']
        
        # External fragmentation: total free space / number of holes
        total_free = self.get_available_memory()
        num_holes = len(free_partitions)
        
        if total_free > 0 and num_holes > 0:
            self.fragmentation_ratio = (wasted_space + (total_free / num_holes)) / self.physical_memory
        else:
            self.fragmentation_ratio = wasted_space / self.physical_memory
    
    def memory_compaction(self):
        """Compact memory to reduce fragmentation"""
        # Reorganize allocated partitions to be contiguous
        allocated = [p for p in self.partitions if p['allocated']]
        free = [p for p in self.partitions if not p['allocated']]
        
        # Reset partitions
        self.partitions = allocated + free
        self._update_fragmentation()
        return len(allocated), len(free)
    
    def lru_replacement(self, process_pid):
        """Least Recently Used page replacement"""
        if process_pid not in self.lru_cache:
            self.lru_cache[process_pid] = []
        
        if len(self.lru_cache[process_pid]) > 0:
            lru_page = self.lru_cache[process_pid].pop(0)
            self.virtual_memory.page_out(process_pid, lru_page)
            self.page_replacements += 1
            return lru_page
        
        return None
    
    def get_process_memory(self, process_pid):
        """Get memory allocated to a process"""
        return self.allocated_memory.get(process_pid, 0)
    
    def get_partition_status(self):
        """Get fixed memory partition status."""
        if self.allocation_algorithm != 'dynamic':
            return [
                {
                    'partition': idx + 1,
                    'size': partition['size'],
                    'allocated': partition['allocated'],
                    'process_pid': partition['process_pid'],
                    'allocated_size': partition['allocated_size'],
                    'free_size': partition['size'] - partition['allocated_size'] if partition['allocated'] else partition['size']
                }
                for idx, partition in enumerate(self.partitions)
            ]

        return [
            {
                'partition': idx + 1,
                'process_pid': pid,
                'size': memory,
                'allocated': True,
                'allocated_size': memory,
                'free_size': 0
            }
            for idx, (pid, memory) in enumerate(self.allocated_memory.items())
        ]
