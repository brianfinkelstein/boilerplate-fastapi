from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

from structlog import get_logger
from logging import Logger

logger: Logger = get_logger()
router = APIRouter()


class HealthResponse(BaseModel):
    success: bool


@router.get("/health_check", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    current_time = f"Time: {str(datetime.today())}"
    if current_time:
        logger.info(current_time)
        return HealthResponse(success=True)
    else:
        raise HTTPException(status_code=500, detail="background service unhealthy")


@router.get("/liveness_check", response_model=HealthResponse)
async def liveness_check() -> HealthResponse:
    return HealthResponse(success=True)


@router.get("/500")
async def fivehundred():
    raise HTTPException(detail="error 500", status_code=500)


@router.get("/error")
async def error():
    return 1 / 0
