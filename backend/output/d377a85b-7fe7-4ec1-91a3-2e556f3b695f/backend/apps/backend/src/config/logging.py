"""Structured logging configuration."""
import logging
import sys
from typing import Any

from .env import settings

LOG_LEVEL = logging.DEBUG if settings.is_development else logging.INFO


def setup_logging() -> None:
    """Configure root logger with structured format."""
    handler = logging.StreamHandler(sys.stdout)

    if settings.is_production:
        import json

        class JSONFormatter(logging.Formatter):
            def format(self, record: logging.LogRecord) -> str:
                log_data: dict[str, Any] = {
                    "level": record.levelname,
                    "message": record.getMessage(),
                    "logger": record.name,
                    "timestamp": self.formatTime(record),
                }
                if record.exc_info:
                    log_data["exception"] = self.formatException(record.exc_info)
                return json.dumps(log_data)

        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )

    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

    # Quiet down noisy libraries
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)


logger = logging.getLogger("taskflow")
