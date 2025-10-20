"""
Strategy Pattern for different data processing types
Each strategy implements specific join logic for different data types
"""

from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Any, List
import duckdb
from ..models import ProcessingType


class ProcessingStrategy(ABC):
    """Abstract base class for processing strategies"""

    endpoint_string = ""
    sql_string = ""

    @abstractmethod
    def transform_data(self, dataframes: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Transform data after join"""
        pass


class ProcessingStrategyType5(ProcessingStrategy):
    endpoint_string = "upload-bao-cao-danh-sachtktt-khdn-api"
    sql_string = """
    SELECT
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
    """

    def transform_data(self, dataframes: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        conn = duckdb.connect()
        for name in dataframes:
            conn.register(name, dataframes[name])

        result_df = conn.execute(self.sql_string).df()

        conn.close()
        return result_df


class ProcessingStrategyFactory:
    """Factory to get the appropriate processing strategy"""

    _strategies = {
        ProcessingType.TYPE5: ProcessingStrategyType5(),
        # ProcessingType.INVENTORY: InventoryProcessingStrategy(),
        # ProcessingType.CUSTOMER: CustomerProcessingStrategy(),
        # ProcessingType.PRODUCT: ProductProcessingStrategy(),
        # ProcessingType.FINANCIAL: FinancialProcessingStrategy(),
    }

    @classmethod
    def get_strategy(cls, processing_type: ProcessingType) -> ProcessingStrategy:
        """Get processing strategy for given type"""
        strategy = cls._strategies.get(processing_type)
        if not strategy:
            raise ValueError(f"Unknown processing type: {processing_type}")
        return strategy