"""
Tradiba entry point.
"""

from __future__ import annotations

from tradiba.core import Application
from tradiba.logging import get_logger

logger = get_logger(__name__)


def main() -> None:
    app = Application()

    logger.info("Tradiba starting...")
    logger.info("Configuration loaded.")
    logger.info("Infrastructure initialized.")

    app.start()

    logger.info("Tradiba ready.")


if __name__ == "__main__":
    main()