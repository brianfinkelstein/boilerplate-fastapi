import logging
from logging import Logger

import structlog.contextvars
from structlog import get_logger

from app.deps import get_settings

logger: Logger = get_logger()


def get_extra_loggers():
    # make sure to attach to these as well
    extra = [
        "uvicorn",
        "uvicorn.access",
    ]
    for e in extra:
        yield logging.getLogger(e)


def _quiet_noisy_third_parties():
    # disable invalid https cert warnings that were spamming logs
    import urllib3

    urllib3.disable_warnings()

    # allow user auth with google
    import warnings

    warnings.filterwarnings("ignore", "Your application has authenticated using end user credentials")

    # info level
    names = [
        "urllib3",
        "google",
    ]
    for name in names:
        logging.getLogger(name).setLevel(logging.INFO)

    # warning level
    names = []
    for name in names:
        logging.getLogger(name).setLevel(logging.WARNING)


def setup_app_logging():

    import logging.config
    import structlog

    timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")
    pre_chain = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        timestamper,
        structlog.processors.format_exc_info,
    ]

    setting = get_settings()

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "colored": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.dev.ConsoleRenderer(colors=True),
                    "foreign_pre_chain": pre_chain,
                },
                "json": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.processors.JSONRenderer(),
                    "foreign_pre_chain": pre_chain,
                },
            },
            "handlers": {
                "default": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    # colored pretty logs for local, json logs for k8s
                    "formatter": "colored" if setting.ENVIRON == "local" else "json",
                },
            },
            "root": {"handlers": ["default"], "level": "DEBUG" if setting.ENVIRON == "local" else "INFO",},
        }
    )

    # clear all the other handlers. make sure that everything propagates to the root
    for _logger in get_extra_loggers():
        _logger.handlers = []
        _logger.propagate = True

    _quiet_noisy_third_parties()

    structlog.configure(
        processors=[
            *pre_chain,
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
