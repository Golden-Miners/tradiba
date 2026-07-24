"""
Shared logger factory using JSON formatting.
"""

from __future__ import annotations

import logging
import json
import sys
from datetime import datetime

from .config import DEFAULT_LEVEL

_configured = False


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage()
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


def _configure() -> None:
    global _configured

    if _configured:
        return

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, DEFAULT_LEVEL))
    root_logger.addHandler(handler)

    _configured = True


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured JSON logger.
    """
    _configure()
    return logging.getLogger(name)