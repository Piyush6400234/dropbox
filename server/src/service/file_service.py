import fastapi 
from ..infrastructure.database.repository import FileRepository
from ..infrastructure.storage.interface import StorageInterface
from ..infrastructure.storage.s3 import S3Storage
from ..domain.models.file import File
from ..domain.schemas.file import FileUploadResponse, FileDetailsResponse, FileListResponse, FileDeleteResponse, FileBase
from ..core.exceptions import FileNotFoundError, StorageError
from typing import List, BinaryIO
from datetime import datetime
from fastapi import Depends
import uuid
import logging
import os

logger = logging.getLogger(__name__)

class UnsupportedFileTypeError(StorageError):
    """Raised when file type is not supported"""
    pass

class FileService:
    def __init__(self):
        self.repository = FileRepository()
        self.storage = S3Storage()

    def _validate_file_type(self, filename: str, content_type: str) -> None:
        # Check file extension
        _, ext = os.path.splitext(filename.lower())
        if ext not in FileBase.SUPPORTED_EXTENSIONS:
            raise UnsupportedFileTypeError(
                f"Unsupported file extension. Supported extensions are: {', '.join(FileBase.SUPPORTED_EXTENSIONS)}"
            )

        # Check MIME type
        if content_type not in FileBase.SUPPORTED_MIME_TYPES:
            raise UnsupportedFileTypeError(
                f"Unsupported MIME type. Supported types are: {', '.join(FileBase.SUPPORTED_MIME_TYPES)}"
            )

    async def upload_file(self, file_obj: BinaryIO, filename: str, 
                         content_type: str, size: int) -> FileUploadResponse:
        try:
            self._validate_file_type(filename, content_type)
            
            s3_key = f"files/{uuid.uuid4()}-{filename}"
            await self.storage.upload(file_obj, s3_key, content_type)
            download_url = await self.storage.get_download_url(s3_key)
            
            file = File(
                id=None,
                filename=filename,
                s3_key=s3_key,
                size=size,
                content_type=content_type,
                uploaded_at=datetime.utcnow(),
                download_url = download_url
            )
            
            db_file = await self.repository.create(file)
            
            return FileUploadResponse(
                id=db_file['id'],
                # filename=db_file.filename,
                # size=db_file.size,
                # content_type=db_file.content_type,
                # uploaded_at=db_file.uploaded_at,
                s3_key=db_file['s3_key'],
                download_url=download_url
            )
        except UnsupportedFileTypeError:
            raise
        except Exception as e:
            logger.error(f"File upload error: {str(e)}")
            try:
                await self.storage.delete(s3_key)
            except:
                pass
            raise

    async def get_file(self, s3_key: str):
        
        download_url = await self.storage.get_download_url(s3_key)
        return {   
            "download_url":download_url
        }

    async def list_files(self):
        files = await self.repository.get_all()
        result = []
        for file in files:
            download_url = await self.storage.get_download_url(file.s3_key)
            result.append({
                **file.__dict__
            })
        return result

    async def delete_file(self, file_id: int) -> FileDeleteResponse:
        file = await self.repository.get_by_id(file_id)
        if not file:
            raise FileNotFoundError(f"File with id {file_id} not found")
        
        await self.storage.delete(file.s3_key)
        await self.repository.delete(file_id)
        
        return FileDeleteResponse(
            message="File deleted successfully",
            file_id=file_id
        )
