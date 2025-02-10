from abc import ABC, abstractmethod
from typing import BinaryIO

class StorageInterface(ABC):
    @abstractmethod
    async def upload(self, file_obj: BinaryIO, key: str, content_type: str) -> str:
        pass

    @abstractmethod
    async def get_download_url(self, key: str) -> str:
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        pass
