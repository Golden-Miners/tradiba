"""
Tradiba version information.
"""

from __future__ import annotations

from typing import Final

MAJOR: Final[int] = 0
MINOR: Final[int] = 1
PATCH: Final[int] = 0

VERSION: Final[tuple[int, int, int]] = (
    MAJOR,
    MINOR,
    PATCH,
)

__version__: Final[str] = (
    f"{MAJOR}.{MINOR}.{PATCH}"
)