"""
Strategy Pattern for different data processing types
Each strategy implements specific join logic for different data types
"""

from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Any, List
import duckdb
from ..models import ProcessingType
from ..config.settings import mapping


class ProcessingStrategy(ABC):
    """Abstract base class for processing strategies"""
    def __init__(self, endpoint_string: str, sql_string: str):
        self.endpoint_string = endpoint_string
        self.sql_string = sql_string

    @abstractmethod
    def transform_data(self, dataframes: Dict[str,pd.DataFrame]) -> pd.DataFrame:
        """Transform data after join"""
        pass


class ProcessingStrategyType5(ProcessingStrategy):
    def __init__(self, endpoint_string, sql_string):
        super().__init__(endpoint_string, sql_string)

    def transform_data(self, dataframes: Dict[str,pd.DataFrame]) -> pd.DataFrame:
        conn = duckdb.connect()
        for name in dataframes:
            conn.register(name, dataframes[name])

        result_df = conn.execute(self.sql_string).df()

        conn.close()
        return result_df


class ProcessingStrategyFactory:
    """Factory to get the appropriate processing strategy"""

    _strategies = {
        ProcessingType.TYPE5: ProcessingStrategyType5(mapping["5"][0], mapping["5"][1]),
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
    
    # @classmethod
    # def get_api_endpoint(cls, processing_type: ProcessingType) -> str:

    #     pass
