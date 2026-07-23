"""
Tradiba entry point.
"""

from __future__ import annotations

from tradiba.core import Application
from tradiba.logging import get_logger

logger = get_logger(__name__)


def main() -> None:
    from tradiba.mt5.service import MT5Service
    mt5 = MT5Service()
    app = Application(market_provider=mt5)
    app.lifecycle.add(mt5)

    logger.info("Tradiba starting...")
    logger.info("Configuration loaded.")
    logger.info("Infrastructure initialized.")

    app.start()

    logger.info("Tradiba ready.")


if __name__ == "__main__":
    main()