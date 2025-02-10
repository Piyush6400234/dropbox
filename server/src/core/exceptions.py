class StorageError(Exception):
    """Base exception for storage operations"""
    pass

class FileNotFoundError(StorageError):
    """Raised when file is not found"""
    pass

class StorageConnectionError(StorageError):
    """Raised when storage connection fails"""
    pass
