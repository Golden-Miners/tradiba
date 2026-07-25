from abc import ABC, abstractmethod
from typing import Any, Callable

MessageHandler = Callable[[Any], None]

class MessageBus(ABC):
    """
    Abstract interface for the distributed message bus.
    """
    @abstractmethod
    def publish(self, topic: str, event: Any) -> None:
        """Publish an event to a topic."""
        pass

    @abstractmethod
    def subscribe(self, topic: str, handler: MessageHandler) -> None:
        """Subscribe a handler to a topic."""
        pass

    @abstractmethod
    def acknowledge(self, message: Any) -> None:
        """Acknowledge the successful processing of a message."""
        pass

    @abstractmethod
    def reject(self, message: Any, requeue: bool = False) -> None:
        """Reject a message, optionally requeueing it."""
        pass
