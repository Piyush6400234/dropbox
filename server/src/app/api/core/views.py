from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from src.service.file_service import FileService, UnsupportedFileTypeError
from ....domain.schemas.file import FileUploadResponse, FileDetailsResponse, FileDeleteResponse
from ....core.exceptions import StorageError, FileNotFoundError
from typing import List, Annotated

router = APIRouter()

@router.post("/files")
async def upload_file(
    file: UploadFile = File(...),
    file_service: FileService = Depends()
):
    try:
        return await file_service.upload_file(
            file.file,
            file.filename,
            file.content_type,
            file.size
        )
    except UnsupportedFileTypeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except StorageError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/files")
async def list_files():
    file_service = FileService()
    return await file_service.list_files()

@router.get("/files/{s3_key}")
async def get_file(s3_key: str, file_service: FileService = Depends()):
    try:
        return await file_service.get_file(s3_key)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except StorageError as e:
        raise HTTPException(status_code=500, detail=str(e))
