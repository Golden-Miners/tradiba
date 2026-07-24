"""
Tradiba entry point.
"""

from __future__ import annotations

from tradiba.logging import get_logger

logger = get_logger(__name__)


def main() -> None:
    from tradiba.bootstrap import bootstrap
    
    logger.info("Tradiba starting...")
    app = bootstrap()
    logger.info("Infrastructure initialized.")

    app.start()

    logger.info("Tradiba ready.")


if __name__ == "__main__":
    main()