import logging
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler
from pathlib import Path

import colorlog

# log to project root
project_root = Path(__file__).parent.parent.resolve()
logs_dir = project_root / "logs"
logs_dir.mkdir(exist_ok=True, parents=True)
logs_target = logs_dir / "python.log"

logging_schema = {
    "version": 1,
    "formatters": {
        "standard": {
            "class": "logging.Formatter",
            "format": "%(asctime)s | %(levelname)-8s | %(filename)-20s | %(message)s",
            "datefmt": "%d %b %y %H:%M:%S",
        },
        "colored": {
            "class": "colorlog.ColoredFormatter",
            "format": "%(asctime)s | %(log_color)s%(levelname)-8s%(reset)s | %(filename)-20s | %(message)s",
            "datefmt": "%d %b %y %H:%M:%S",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored",
            "level": "DEBUG",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "level": "DEBUG",
            "filename": str(logs_target),
            "mode": "a",
            "encoding": "utf-8",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
    },
    "loggers": {
        "__main__": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        }
    },
    "root": {"level": "DEBUG", "handlers": ["console", "file"]},
}

dictConfig(logging_schema)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.debug("This is another test")
    logger.info("testing an info log entry")
    logger.warning("testing a warning log entry")
    logger.error("testing an error log entry")
    logger.critical("THINGS WILL EXPLODE IN A FEW SECONDS")
