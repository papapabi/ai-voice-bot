import logging
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler
from pathlib import Path

# log to project root
project_root = Path(__file__).parent.parent.resolve()
logs_dir = project_root / "logs"
logs_dir.mkdir(exist_ok=True, parents=True)
logs_target = logs_dir / "python.log"


logging_schema = {
    # Always 1. Schema versioning may be added in a future release of logging
    "version": 1,
    # "Name of formatter" : {Formatter Config Dict}
    "formatters": {
        # Formatter Name
        "standard": {
            # class is always "logging.Formatter"
            "class": "logging.Formatter",
            # Optional: logging output format
            "format": "%(asctime)s\t%(levelname)s\t%(filename)s\t%(message)s",
            # Optional: asctime format
            "datefmt": "%d %b %y %H:%M:%S",
        }
    },
    # Handlers use the formatter names declared above
    "handlers": {
        # Name of handler
        "console": {
            # The class of logger. A mixture of logging.config.dictConfig() and
            # logger class-specific keyword arguments (kwargs) are passed in here.
            "class": "logging.StreamHandler",
            # This is the formatter name declared above
            "formatter": "standard",
            "level": "INFO",
            # The default is stderr
            "stream": "ext://sys.stdout",
        },
        # Same as the StreamHandler example above, but with different
        # handler-specific kwargs.
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "level": "INFO",
            "filename": str(logs_target),
            "mode": "a",
            "encoding": "utf-8",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
    },
    # Loggers use the handler names declared above
    "loggers": {
        "__main__": {  # if __name__ == "__main__"
            # Use a list even if one handler is used
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        }
    },
    # Just a standalone kwarg for the root logger
    "root": {"level": "INFO", "handlers": ["file"]},
}

dictConfig(logging_schema)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.info("testing an info log entry")
    logging.warning("testing a warning log entry")
