from dataclasses import dataclass
from datetime import datetime

@dataclass
class File:
    id: int | None
    filename: str
    s3_key: str
    size: int
    content_type: str
    uploaded_at: datetime
    download_url: str
