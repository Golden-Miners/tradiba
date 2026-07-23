"""
Low-level MetaTrader 5 client.

This module is the only place that talks directly to the MetaTrader5 package.
"""

from __future__ import annotations

import MetaTrader5 as mt5

from .exceptions import MT5ConnectionError, MT5Error
from datetime import datetime


class MT5Client:
    """Thin wrapper around the MetaTrader5 package."""

    def connect(self) -> None:
        if mt5.initialize():
            return

        code, message = mt5.last_error()
        raise MT5ConnectionError(
            f"MT5 initialize failed ({code}): {message}"
        )

    def disconnect(self) -> None:
        mt5.shutdown()

    def terminal_info(self):
        return mt5.terminal_info()

    def account_info(self):
        return mt5.account_info()

    def version(self):
        return mt5.version()

    def copy_rates_range(
        self,
        symbol: str,
        timeframe: int,
        date_from: datetime,
        date_to: datetime,
    ):
        rates = mt5.copy_rates_range(
            symbol,
            timeframe,
            date_from,
            date_to,
        )

        if rates is None:
            code, message = mt5.last_error()
            raise MT5ConnectionError(
                f"copy_rates_range failed ({code}): {message}"
            )

        return rates

    def copy_rates_from_pos(
        self,
        symbol: str,
        timeframe: int,
        start_pos: int,
        count: int,
    ):
        rates = mt5.copy_rates_from_pos(
            symbol,
            timeframe,
            start_pos,
            count,
        )

        if rates is None:
            code, message = mt5.last_error()
            raise MT5ConnectionError(
                f"copy_rates_from_pos failed ({code}): {message}"
            )

        return rates

    def symbol_info_tick(self, symbol: str):
        tick = mt5.symbol_info_tick(symbol)

        if tick is None:
            code, message = mt5.last_error()
            raise MT5Error(
                f"symbol_info_tick failed ({code}): {message}"
            )

        return tick