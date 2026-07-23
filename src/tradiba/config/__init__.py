"""
Tradiba configuration package.
"""

from .loader import load_settings
from .settings import Settings

__all__ = (
    "Settings",
    "load_settings",
)