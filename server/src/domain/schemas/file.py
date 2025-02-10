from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import ClassVar

class FileBase(BaseModel):
    """Base file schema with common attributes"""
    filename: str
    size: int
    content_type: str
    uploaded_at: datetime

    # Define supported file types
    SUPPORTED_MIME_TYPES: ClassVar[set[str]] = {
        'application/pdf',
        'image/jpeg',
        'image/png',
        'image/gif',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }

    SUPPORTED_EXTENSIONS: ClassVar[set[str]] = {
        '.pdf', '.jpg', '.jpeg', '.png', '.gif', 
        '.doc', '.docx', '.txt', '.xls', '.xlsx'
    }

    @validator('content_type')
    def validate_content_type(cls, v):
        if v not in cls.SUPPORTED_MIME_TYPES:
            raise ValueError(f"Unsupported file type. Supported types are: {', '.join(cls.SUPPORTED_MIME_TYPES)}")
        return v

    class Config:
        from_attributes = True

class FileUploadResponse(BaseModel):
    """Response schema for file upload operation"""
    id: int
    s3_key: str
    download_url: str

class FileDetailsResponse(FileBase):
    """Response schema for getting file details"""
    id: int
    download_url: str

class FileListResponse(FileBase):
    """Response schema for listing files"""
    id: int
    download_url: str

class FileDeleteResponse(BaseModel):
    """Response schema for file deletion"""
    message: str
    file_id: int
