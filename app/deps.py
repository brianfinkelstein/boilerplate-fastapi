from functools import lru_cache
from structlog import get_logger

from logging import Logger
from app.core.config import Settings

logger: Logger = get_logger()


@lru_cache()
def get_settings() -> Settings:
    logger.info("read settings")
    return Settings()
