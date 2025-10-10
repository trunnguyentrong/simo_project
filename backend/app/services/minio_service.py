from minio import Minio
from minio.error import S3Error
from io import BytesIO
from typing import BinaryIO
import uuid
from datetime import datetime
from ..config import settings


class MinioService:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        self._ensure_bucket()

    def _ensure_bucket(self):
        """Ensure bucket exists, create if not"""
        try:
            if not self.client.bucket_exists(settings.MINIO_BUCKET):
                self.client.make_bucket(settings.MINIO_BUCKET)
        except S3Error as e:
            print(f"Error ensuring bucket: {e}")

    def upload_file(self, file: BinaryIO, filename: str) -> str:
        """Upload file to MinIO and return file ID"""
        file_id = f"{uuid.uuid4()}_{filename}"

        # Read file content
        file_content = file.read()
        file_size = len(file_content)

        # Upload to MinIO
        self.client.put_object(
            settings.MINIO_BUCKET,
            file_id,
            BytesIO(file_content),
            file_size,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        return file_id

    def download_file(self, file_id: str) -> bytes:
        """Download file from MinIO"""
        try:
            response = self.client.get_object(settings.MINIO_BUCKET, file_id)
            data = response.read()
            response.close()
            response.release_conn()
            return data
        except S3Error as e:
            raise Exception(f"Error downloading file: {e}")

    def delete_file(self, file_id: str):
        """Delete file from MinIO"""
        try:
            self.client.remove_object(settings.MINIO_BUCKET, file_id)
        except S3Error as e:
            print(f"Error deleting file: {e}")


# Singleton instance
minio_service = MinioService()
