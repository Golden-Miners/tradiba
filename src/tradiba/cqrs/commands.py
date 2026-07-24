"""
CQRS Commands.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Command:
    """Base class for all commands."""
    pass


@dataclass(frozen=True, slots=True)
class OpenTradeCommand(Command):
    symbol: str
    side: str
    volume: float
    stop_loss: float = 0.0
    take_profit: float = 0.0


@dataclass(frozen=True, slots=True)
class CloseTradeCommand(Command):
    ticket: int


@dataclass(frozen=True, slots=True)
class CancelOrderCommand(Command):
    order_id: str


@dataclass(frozen=True, slots=True)
class StartReplayCommand(Command):
    session_id: str


@dataclass(frozen=True, slots=True)
class StopReplayCommand(Command):
    session_id: str
