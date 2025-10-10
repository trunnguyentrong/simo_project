import pandas as pd
from io import BytesIO
from typing import List, Dict, Any
from datetime import datetime
from loguru import logger
from .minio_service import minio_service
from .mongodb_service import mongodb_service
from .external_api import external_api_service
from .processing_strategies import ProcessingStrategyFactory
from ..models import ProcessingType, ProcessingConfig


class DataProcessor:
    async def process_uploaded_file(
        self,
        file_id: str,
        processing_type: ProcessingType
    ) -> Dict[str, Any]:
      
        config = ProcessingConfig.get_config(processing_type)

        logger.debug(config)    

        collection_names = config.get("collections")

        strategy = ProcessingStrategyFactory.get_strategy(processing_type)
        endpoint = strategy.endpoint_string

        file_data = minio_service.download_file(file_id)
        upload_df = pd.read_excel(BytesIO(file_data))

        reference_data = await mongodb_service.get_multiple_collections(
            collection_names=collection_names
        )
        reference_data["EXCEL"] = upload_df
        transformed_df = strategy.transform_data(reference_data)
        records = transformed_df.to_dict('records')
        
        api_response = await external_api_service.send_data(endpoint,records)
        logger.info(api_response)

        return {
            "status": "success",
            "processing_type": processing_type.value,
            "records_processed": len(records),
            "join_key_used": "user_id",
            "collection_used": ", ".join(collection_names),
            "external_api_response": api_response
        }


# Singleton instance
data_processor = DataProcessor()
