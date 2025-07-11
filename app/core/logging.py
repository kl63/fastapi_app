import logging
import sys
from pathlib import Path
from loguru import logger
import json
from datetime import datetime


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentation.
    See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


class CustomizeJsonSink:
    """
    Custom JSON formatter for loguru
    """

    def __init__(self):
        self.serialize = json.dumps

    def __call__(self, message):
        record = message.record
        data = {
            "timestamp": datetime.fromtimestamp(record["time"].timestamp()).isoformat(),
            "level": record["level"].name,
            "message": record["message"],
            "module": record["name"],
        }
        
        if record["exception"]:
            data["exception"] = record["exception"]
            
        return self.serialize(data) + "\n"


def setup_logging(log_level: str = "INFO", json_logs: bool = False):
    """
    Configure logging with loguru
    """
    # Remove default handlers
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(log_level)

    # Remove all existing loggers
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # Configure loguru
    logger.configure(
        handlers=[
            {
                "sink": sys.stdout, 
                "level": log_level,
                "format": (
                    "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
                    "{name}:{function}:{line} - {message}"
                ) if not json_logs else CustomizeJsonSink(),
            }
        ]
    )
