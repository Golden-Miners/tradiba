"""
Shared logger factory.
"""

from __future__ import annotations

import logging

from .config import (
    DATE_FORMAT,
    DEFAULT_LEVEL,
    LOG_FORMAT,
)

_configured = False


def _configure() -> None:
    global _configured

    if _configured:
        return

    logging.basicConfig(
        level=getattr(logging, DEFAULT_LEVEL),
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

    _configured = True


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger.

    Parameters
    ----------
    name:
        Module name.

    Returns
    -------
    logging.Logger
    """

    _configure()

    return logging.getLogger(name)