from fastapi import APIRouter, HTTPException
from loguru import logger
from ..models import ProcessRequest, ProcessResponse
from ..services import data_processor

router = APIRouter(prefix="", tags=["Process"])


@router.post("/", response_model=ProcessResponse)
async def process_data(request: ProcessRequest):
    """
    Process uploaded file with specific processing type.

    Each processing type has:
    - Different MongoDB collection for reference data
    - Different join logic
    - Different data validation rules
    """
    try:
        result = await data_processor.process_uploaded_file(
            file_id=request.file_id,
            processing_type=request.processing_type
        )

        logger.info(result)

        return ProcessResponse(
            status=result["status"],
            message=f"Data processed successfully using {request.processing_type.value} strategy",
            processing_type=result["processing_type"],
            records_processed=result["records_processed"],
            join_key_used=result["join_key_used"],
            collection_used=result["collection_used"],
            external_api_response=result.get("external_api_response")
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing data: {str(e)}")


# @router.get("/types")
# async def get_processing_types():
#     """Get available processing types and their configurations"""
#     from ..models import ProcessingConfig

#     return {
#         "processing_types": [
#             {
#                 "type": ptype.value,
#                 "config": ProcessingConfig.get_config(ptype)
#             }
#             for ptype in ProcessingType
#         ]
#     }
