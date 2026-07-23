"""
Base service definitions.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class Service(ABC):
    """
    Base class for all Tradiba services.
    """

    @abstractmethod
    def start(self) -> None:
        """Start the service."""

    @abstractmethod
    def stop(self) -> None:
        """Stop the service."""