"""
CQRS Command Dispatcher.
"""

from typing import Type

from tradiba.logging import get_logger

from .commands import Command
from .handlers import CommandHandler

logger = get_logger(__name__)


class CommandDispatcher:
    """
    Routes commands to their registered handlers.
    """

    def __init__(self) -> None:
        self._handlers: dict[Type[Command], CommandHandler] = {}

    def register(self, command_type: Type[Command], handler: CommandHandler) -> None:
        """Register a handler for a specific command type."""
        if command_type in self._handlers:
            logger.warning("Overwriting existing handler for %s", command_type.__name__)
        self._handlers[command_type] = handler
        logger.debug("Registered handler %s for %s", type(handler).__name__, command_type.__name__)

    def dispatch(self, command: Command) -> None:
        """
        Dispatch a command to its registered handler.
        Raises ValueError if no handler is registered.
        """
        command_type = type(command)
        handler = self._handlers.get(command_type)
        if not handler:
            raise ValueError(f"No handler registered for command: {command_type.__name__}")

        logger.debug("Dispatching %s to %s", command_type.__name__, type(handler).__name__)
        try:
            handler.handle(command)
        except Exception as e:
            logger.exception("Error handling command %s: %s", command_type.__name__, e)
            raise
