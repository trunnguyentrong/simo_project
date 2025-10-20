from pydantic_settings import BaseSettings

mapping = {
    "5": ["upload-bao-cao-danh-sachtktt-khdn-api",
          """SELECT
            cus.ID AS Cif
            ,cus.VN_FULL_NAME AS TenToChuc
            ,cus.ESTAB_LIC_CODE AS SoGiayPhepThanhLap
            ,'1' AS LoaiGiayToThanhLapToChuc
            ,TO_CHAR(TO_DATE(COALESCE(cus.BIRTH_INCORP_DATE,cus.ESTAB_ISS_DATE),'YYYYMMDD'),'DD/MM/YYYY') AS NgayThanhLap
            ,COALESCE(cus.MST_ADDRESS,cus.VN_FULL_ADDRESS) AS DiaChiToChuc
            ,TRIM(REGEXP_SUBSTR(cus.REP_NAME, '[^#]+', 1, 1)) AS HoTenNguoiDaiDien
            ,TRIM(REGEXP_SUBSTR(cus.REP_ID_NUM, '[^#]+', 1, 1)) AS SoGiayToTuyThan
            ,DECODE(TRIM(REGEXP_SUBSTR(cus.REP_ID_TYPE, '[^#]+', 1, 1)),'CCCD',1,'HO.CHIEU',4,'CMTND',3,'KHAC',7,7) AS LoaiGiayToTuyThan
            ,TO_CHAR(TO_DATE(TRIM(REGEXP_SUBSTR(cus.REP_BIRTH_DAY, '[^#]+', 1, 1)),'YYYYMMDD'),'DD/MM/YYYY') AS NgaySinh
            ,DECODE(TRIM(REGEXP_SUBSTR(cus.REP_GENDER, '[^#]+', 1, 1)),'MALE',1,'FEMALE',0,2) AS GioiTinh
            ,'VN' AS QuocTich
            ,TRIM(REGEXP_SUBSTR(cus.REP_PHONE, '[^#]+', 1, 1)) AS DienThoai
            ,acc.ID AS SoTaiKhoanToChuc
            ,TO_CHAR(TO_DATE(acc.OPENING_DATE,'YYYYMMDD'),'DD/MM/YYYY') AS NgayMoTaiKhoan
            ,ACC.LOCKED_AMOUNT 
            AS TrangThaiTaiKhoan --CAN DONG BO BIZ VE ODS --Can xac dinh TK bi phong toa, TK tam khoa
            ,'Không thu thập được' AS DiaChiMAC
            ,'Không thu thập được' AS SO_IMEI
        FROM T24_T24CORE_ACCOUNT acc
            INNER JOIN T24_T24CORE_CUSTOMER cus ON acc.CUSTOMER = cus.ID 
            INNER JOIN EXCEL ON cus.ID = EXCEL.MAKH
            LEFT JOIN 
            (
            SELECT 
                ACCT_NO
                ,ROW_NUMBER() OVER (PARTITION BY ACCT_NO ORDER BY ACCT_NO DESC) AS RN
            FROM BIZ_CORP_ACCT ca 
                INNER JOIN BIZ_CORP corp ON ca.CORP_ID = corp.ID
            WHERE corp.IS_DELETE = 'N'
            ) biz ON biz.ACCT_NO = acc.ID AND biz.RN = 1
        WHERE 1=1
            AND cus.KHOI IN ('SME','FI','CIB','DVC');
        """],
    "6": [""]
}



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
