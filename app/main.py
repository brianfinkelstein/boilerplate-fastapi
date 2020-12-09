import traceback
from logging import Logger

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from starlette.responses import JSONResponse
from structlog import get_logger

from app.api.api import router
from app.core.version import git_version
from app.core.logging import setup_app_logging
from app.deps import get_settings

setup_app_logging()
logger: Logger = get_logger()

app = FastAPI(title=get_settings().APP_NAME, version=git_version())


@app.exception_handler(Exception)
async def http_error_handler(_: Request, exc: Exception) -> JSONResponse:
    settings = get_settings()  # cannot inject into exception handlers
    data = {"status_code": 500}
    if settings.ENVIRON == "local":
        data["exc"] = traceback.format_exception_only(type(exc), exc)[-1].strip()
    return JSONResponse(data, status_code=500)


@app.on_event("startup")
def startup():
    logger.info("startup")
    # services.startup()


@app.on_event("shutdown")
def shutdown():
    logger.info("shutdown")
    try:
        pass
        # services.shutdown()
    except Exception as e:
        logger.error("exception shutting down services", exc_info=e)


@app.middleware("http")
async def before_request(request: Request, call_next):
    if request.url.path is not None and request.url.path not in ("/health_check", "/liveness_check",):
        pass
        # if not auth.auth_api(request=request):
        #     return Response(status_code=401)

    response = await call_next(request)
    return response


app.include_router(router)
