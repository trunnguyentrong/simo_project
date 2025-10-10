from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

from .processing_types import ProcessingType


class ProcessRequest(BaseModel):
    file_id: str
    processing_type: ProcessingType = Field(
        ...,
        description="Type of data processing to perform"
    )


class ProcessResponse(BaseModel):
    status: str
    message: str
    processing_type: str
    records_processed: int
    join_key_used: str
    collection_used: str
    external_api_response: Optional[Dict[str, Any]] = None


class DataRecord(BaseModel):
    """Model for joined data"""
    id: str
    data: Dict[str, Any]
    processed_at: datetime
