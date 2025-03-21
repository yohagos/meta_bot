import logging, logging.config 


def configure_logging():
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {  # Root-Logger
                "handlers": ["console"],
                "level": "INFO",
            },
            "sqlalchemy.engine": {
                "level": "WARNING",
                "propagate": False
            },
        },
    })

logger = logging.getLogger(__name__)