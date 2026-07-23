"""
MT5-related exceptions.
"""


class MT5Error(Exception):
    """Base exception for MT5 operations."""


class MT5ConnectionError(MT5Error):
    """Raised when MT5 cannot be initialized or connected."""