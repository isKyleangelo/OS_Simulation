"""
PusoyOS File System Module
Handles file creation, deletion, reading, writing, and permissions
"""

from datetime import datetime
from config import ROOT_DIRECTORY, MAX_FILES, DEFAULT_FILE_PERMISSIONS


class File:
    """Represents a file in PusoyOS"""
    _inode_counter = 1000
    
    def __init__(self, filename, owner='root', permissions='644', content=''):
        self.inode = File._inode_counter
        File._inode_counter += 1
        
        self.filename = filename
        self.path = f'{ROOT_DIRECTORY}/{filename}'
        self.owner = owner
        self.permissions = permissions
        self.content = content
        self.size = len(content)
        self.created_at = datetime.now()
        self.modified_at = datetime.now()
        self.accessed_at = datetime.now()
        self.extension = filename.split('.')[-1] if '.' in filename else 'txt'
    
    def read(self):
        """Read file content"""
        self.accessed_at = datetime.now()
        return self.content
    
    def write(self, content):
        """Write content to file"""
        self.content = content
        self.size = len(content)
        self.modified_at = datetime.now()
        self.accessed_at = datetime.now()
    
    def append(self, content):
        """Append content to file"""
        self.content += content
        self.size = len(self.content)
        self.modified_at = datetime.now()
        self.accessed_at = datetime.now()
    
    def get_size_kb(self):
        """Get file size in KB"""
        return round(self.size / 1024, 2) if self.size > 0 else 0
    
    def change_permissions(self, permissions):
        """Change file permissions"""
        self.permissions = permissions
        self.modified_at = datetime.now()
    
    def to_dict(self):
        """Convert file to dictionary"""
        return {
            'inode': self.inode,
            'filename': self.filename,
            'path': self.path,
            'owner': self.owner,
            'permissions': self.permissions,
            'size': self.size,
            'size_kb': self.get_size_kb(),
            'extension': self.extension,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'modified_at': self.modified_at.isoformat(),
            'accessed_at': self.accessed_at.isoformat()
        }


class FileSystem:
    """File system manager for PusoyOS"""
    
    def __init__(self):
        self.files = {}  # {filename: File}
        self.file_count = 0
        self.total_reads = 0
        self.total_writes = 0
        self.total_deletes = 0
    
    def create_file(self, filename, owner='root', permissions=DEFAULT_FILE_PERMISSIONS, content=''):
        """Create a new file"""
        if filename in self.files:
            return None
        
        if self.file_count >= MAX_FILES:
            return None
        
        file = File(filename, owner, permissions, content)
        self.files[filename] = file
        self.file_count += 1
        self.total_writes += 1
        return file
    
    def delete_file(self, filename):
        """Delete a file"""
        if filename in self.files:
            del self.files[filename]
            self.file_count -= 1
            self.total_deletes += 1
            return True
        return False
    
    def read_file(self, filename):
        """Read file content"""
        if filename in self.files:
            self.total_reads += 1
            return self.files[filename].read()
        return None
    
    def write_file(self, filename, content):
        """Write to file"""
        if filename in self.files:
            self.total_writes += 1
            self.files[filename].write(content)
            return True
        return False
    
    def append_file(self, filename, content):
        """Append to file"""
        if filename in self.files:
            self.files[filename].append(content)
            return True
        return False
    
    def get_file(self, filename):
        """Get file object"""
        return self.files.get(filename)
    
    def get_all_files(self):
        """Get all files"""
        return list(self.files.values())
    
    def list_files(self):
        """List all files"""
        return [f.to_dict() for f in self.files.values()]
    
    def get_file_info(self, filename):
        """Get file information"""
        if filename in self.files:
            return self.files[filename].to_dict()
        return None
    
    def file_exists(self, filename):
        """Check if file exists"""
        return filename in self.files
    
    def rename_file(self, old_name, new_name):
        """Rename file"""
        if old_name in self.files and new_name not in self.files:
            file = self.files[old_name]
            file.filename = new_name
            file.path = f'{ROOT_DIRECTORY}/{new_name}'
            file.extension = new_name.split('.')[-1] if '.' in new_name else 'txt'
            file.modified_at = datetime.now()
            self.files[new_name] = file
            del self.files[old_name]
            return True
        return False
    
    def copy_file(self, source, destination):
        """Copy file"""
        if source in self.files and destination not in self.files:
            source_file = self.files[source]
            self.create_file(destination, source_file.owner, 
                           source_file.permissions, source_file.content)
            return True
        return False
    
    def get_filesystem_info(self):
        """Get file system information"""
        total_size = sum(f.size for f in self.files.values())
        
        return {
            'file_count': self.file_count,
            'max_files': MAX_FILES,
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'total_reads': self.total_reads,
            'total_writes': self.total_writes,
            'total_deletes': self.total_deletes,
            'inode_count': File._inode_counter - 1000
        }
