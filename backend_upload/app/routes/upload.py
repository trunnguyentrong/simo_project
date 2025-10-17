from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime

from ..models import UploadResponse
from ..services import minio_service

router = APIRouter(prefix="", tags=["Upload"])


@router.post("/", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """Upload Excel file to MinIO"""
    # Validate file type
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Only Excel files (.xlsx, .xls) are allowed")

    try:
        # Upload to MinIO
        file_id = minio_service.upload_file(file.file, file.filename)

        return UploadResponse(
            file_id=file_id,
            filename=file.filename,
            message="File uploaded successfully",
            uploaded_at=datetime.utcnow()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")
