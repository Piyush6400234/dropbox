import pydantic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from pydantic import BaseModel
from .models import FileModel
from ...domain.models.file import File
from .session import DatabaseSessionManager

class FileRepository():
    def __init__(self):
        self.session = DatabaseSessionManager()

    async def create(self, file: File):
        db_file = FileModel(
            filename=file.filename,
            s3_key=file.s3_key,
            size=file.size,
            content_type=file.content_type,
            uploaded_at=file.uploaded_at,
            download_url=""
        )
        session = await self.session.get_session()
        # print("sessionrepo ", session)
        try:
            session.add(db_file)
            await session.commit()
            await session.refresh(db_file)
        finally:
            # await session.close()
            pass
        file_dict = {key: value for key, value in db_file.__dict__.items() if key != '_sa_instance_state'}
        print("file_dict ", file_dict)
        return file_dict
    

    async def get_by_id(self, file_id: int) -> Optional[File]:
    
        session = await self.session.get_session()
        try:
            result = await session.execute(
                select(FileModel).where(FileModel.id == file_id)
            )
        finally:
            # await session.close()
            pass
        file = result.scalar_one_or_none()
        return File(**file.__dict__) if file else None

    async def get_all(self) -> List[File]:
        session = await self.session.get_session()
        print("session ", session)
        try:
            result = await session.execute(select(FileModel))
        finally:
            print("session ", session)
            # await session.close()
        # print("result:: ", (result.scalars().all()[0]).__dict__)
        return [File(**{key: value for key, value in file.__dict__.items() if key != '_sa_instance_state'}) for file in result.scalars().all()]


    async def delete(self, file_id: int) -> bool:
        session = await self.session.get_session()
        try:
            result = await session.execute(
                select(FileModel).where(FileModel.id == file_id)
            )
        finally:
            # await session.close()
            pass
        file = result.scalar_one_or_none()
        if file:
            session = await self.session.get_session()
            try:
                await session.delete(file)
                await session.commit()
                
            finally:
                pass
                # await session.close()
            return True
        return False
