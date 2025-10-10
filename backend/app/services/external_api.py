import httpx
from typing import List, Dict, Any
from datetime import datetime
import uuid
from base64 import b64encode
from loguru import logger
from ..config import settings


class ExternalAPIService:
    def __init__(self):
        self.api_url_prefix = settings.EXTERNAL_API_URL_PREFIX
        self.api_token = settings.EXTERNAL_API_TOKEN
        self.consumerkey = settings.CONSUMERKEY
        self.consumersecret = settings.CONSUMERSECRET
        self.username = settings.USERNAME
        self.password = settings.PASSWORD


    async def get_token(self):
        header = {}
        body = {}
        auth = f"{self.consumerkey}:{self.consumersecret}"
        base64Auth = "Basic" + b64encode(auth.encode()).decode()

        header["Authorized"] = base64Auth
        header["Content-Type"] = "application/x-www-form-urlencoded"

        body["grant_type"] = "password"
        body["username"] = self.username
        body["password"] = self.password

        try:
            respone = httpx.post(url=self.api_token, headers=header, data=body)
            data = respone.json()
            access_token = data.get("access_token")
            logger.info("Get access token successfully!!!")
            return access_token
        except httpx._exceptions.RequestError as e:
            return {
                "status": "error",
                "error": str(e)
            }


    async def send_data(self, endpoint: str, data: List[Dict[str, Any]], batch_size: int = 5000) -> Dict[str, Any]:
        """Send processed data to external API in batches"""
        token = await self.get_token()

        logger.debug(token)

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "maYeuCau": str(uuid.uuid4()),
            "kyBaoCao": datetime.now().strftime("%m/%Y")
        }
        logger.info(data)
        batches = [data[i:i + batch_size] for i in range(0, len(data), batch_size)]
        results = []
        failed_batches = []

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                for batch_index, batch in enumerate(batches):
                    try:
                        response = await client.post(
                            f"{self.api_url_prefix}{endpoint}",
                            json=batch,
                            headers=headers
                        )
                        response.raise_for_status()
                        results.append({
                            "batch": batch_index + 1,
                            "status": "success",
                            "status_code": response.status_code,
                            "records_sent": len(batch),
                            "response": response.json()
                        })
                        logger.info(f"Batch {batch_index + 1}/{len(batches)} sent successfully ({len(batch)} records)")
                    except httpx.HTTPStatusError as e:
                        failed_batches.append({
                            "batch": batch_index + 1,
                            "status_code": e.response.status_code,
                            "error": str(e),
                            "records_count": len(batch)
                        })
                        logger.error(f"Batch {batch_index + 1} failed: {str(e)}")
                    except Exception as e:
                        failed_batches.append({
                            "batch": batch_index + 1,
                            "error": str(e),
                            "records_count": len(batch)
                        })
                        logger.error(f"Batch {batch_index + 1} failed: {str(e)}")

                return {
                    "status": "success" if not failed_batches else "partial_success",
                    "total_records": len(data),
                    "total_batches": len(batches),
                    "successful_batches": len(results),
                    "failed_batches": len(failed_batches),
                    "results": results,
                    "failures": failed_batches
                }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }


# Singleton instance
external_api_service = ExternalAPIService()
