import os
from logging import Logger

from structlog import get_logger

logger: Logger = get_logger()


def git_version():
    try:
        # see if it is in the path
        version_path = f"/app/version"
        if os.path.exists(version_path):
            with open(version_path) as fin:
                return fin.readlines()[0].strip()

        # see if it is in the env
        app_version = os.getenv("APP_VERSION", "").strip()
        if app_version:
            return app_version

    except Exception as e:
        logger.error("unable to find version", exc_info=e)
    finally:
        return "unknown"
