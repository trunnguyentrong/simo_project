from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # MongoDB
    MONGODB_URL: str = "mongodb://admin:password@mongodb-service.storage.svc.cluster.local:27017"
    MONGODB_DB: str = "ecommerce"
    # http://external-minio.default.svc.cluster.local:9000
    # MinIO
    MINIO_ENDPOINT: str = "minio-service.storage.svc.cluster.local:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "data-bucket"
    MINIO_SECURE: bool = False

    # External API
    EXTERNAL_API_URL_PREFIX: str = "http://127.0.0.1:8000/"
    EXTERNAL_API_TOKEN: str = "http://127.0.0.1:8000/token"
    CONSUMERKEY: str = "Gj4N6nuufORe1E_YSyAV5Jwf5JQa"
    CONSUMERSECRET: str = "EXAx6JOAuJlveuw52mzRb1ZGIOIa"
    USERNAME: str = "simo-vietnamhiendai"
    PASSWORD: str = "vietnamhiendai123@"

    # App
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8001

    class Config:
        env_file = ".env"


settings = Settings()
