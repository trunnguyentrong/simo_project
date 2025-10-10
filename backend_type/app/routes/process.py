from fastapi import APIRouter, HTTPException
from loguru import logger
from ..models import ProcessRequest, ProcessResponse, ProcessingType
# from ..services import data_processor

router = APIRouter(prefix="/types", tags=["Type"])

@router.get("/")
async def get_processing_types():
    """Get available processing types and their configurations"""
    from ..models import ProcessingConfig

    return {
        "processing_types": [
            {
                "type": ptype.value,
                "config": ProcessingConfig.get_config(ptype)
            }
            for ptype in ProcessingType
        ]
    }
