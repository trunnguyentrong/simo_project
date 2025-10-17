from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # MinIO
    MINIO_ENDPOINT: str = "minio-service.storage.svc.cluster.local:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "data-bucket"
    MINIO_SECURE: bool = False

    # External API

    # App
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8001

    class Config:
        env_file = ".env"


settings = Settings()
