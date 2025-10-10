from pydantic import BaseModel
from datetime import datetime

class UploadResponse(BaseModel):
    file_id: str
    filename: str
    message: str
    uploaded_at: datetime
