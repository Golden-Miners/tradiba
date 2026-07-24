"""
CQRS Handlers.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .commands import Command
from .queries import Query

C = TypeVar("C", bound=Command)
Q = TypeVar("Q", bound=Query)
R = TypeVar("R")


class CommandHandler(ABC, Generic[C]):
    """Base class for handling a specific Command."""

    @abstractmethod
    def handle(self, command: C) -> None:
        """Process the command."""
        pass


class QueryHandler(ABC, Generic[Q, R]):
    """Base class for handling a specific Query."""

    @abstractmethod
    def handle(self, query: Q) -> R:
        """Process the query and return a result."""
        pass
