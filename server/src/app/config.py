from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
load_dotenv(override=True)


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://myuser:mypassword@localhost:3306/filestore"
    
    # AWS settings
    print("AWS:: ", os.environ.get("ACCESS_KEY_ID"))
    AWS_ACCESS_KEY_ID: str = os.environ.get("ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = os.environ.get("SECRET_ACCESS_KEY")
    AWS_REGION: str = os.environ.get("AWS_REGION")
    S3_BUCKET_NAME: str = os.environ.get("AWS_BUCKET")
    
    
    ALLOWED_MIME_TYPES: dict = {
        'text/plain': '.txt',
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'application/json': '.json'
    }

setting = Settings()