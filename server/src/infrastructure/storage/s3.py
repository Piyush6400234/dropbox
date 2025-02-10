import aioboto3
from typing import BinaryIO
from botocore.exceptions import ClientError
from ...core.exceptions import StorageError, StorageConnectionError
import logging
import typing
from .interface import StorageInterface
logger = logging.getLogger(__name__)
from src.app.config import setting


class S3Storage(StorageInterface):
    def __init__(self):
        print("class invoked")
        self.bucket_name = setting.S3_BUCKET_NAME
        self.session = aioboto3.Session(
            aws_access_key_id=setting.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=setting.AWS_SECRET_ACCESS_KEY,
            region_name=setting.AWS_REGION
        )

    async def upload(self, file_obj: BinaryIO, key: str, content_type: str) -> str:
        try:
            async with self.session.client('s3') as s3:
                await s3.upload_fileobj(
                    file_obj,
                    self.bucket_name,
                    key,
                    ExtraArgs={'ContentType': content_type}
                )
            return key
        except ClientError as e:
            logger.error(f"S3 upload error: {str(e)}")
            raise StorageError(f"Failed to upload file: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during upload: {str(e)}")
            raise StorageConnectionError(f"Storage connection error: {str(e)}")

    async def get_download_url(self, key: str) -> str:
        try:
            async with self.session.client('s3') as s3:
                url = await s3.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': self.bucket_name,
                        'Key': key
                    },
                    ExpiresIn=3600
                )
                return url
        except ClientError as e:
            logger.error(f"S3 presigned URL generation error: {str(e)}")
            raise StorageError(f"Failed to generate download URL: {str(e)}")

    async def delete(self, key: str) -> bool:
        try:
            async with self.session.client('s3') as s3:
                await s3.delete_object(
                    Bucket=self.bucket_name,
                    Key=key
                )
            return True
        except ClientError as e:
            logger.error(f"S3 delete error: {str(e)}")
            raise StorageError(f"Failed to delete file: {str(e)}")
