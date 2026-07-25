from collections import defaultdict
from typing import Any, List, Dict
import logging

from tradiba.distributed.messaging.base import MessageBus, MessageHandler

logger = logging.getLogger(__name__)

class InMemoryMessageBus(MessageBus):
    """
    In-memory implementation of the MessageBus, primarily for local development
    and testing.
    """
    def __init__(self):
        self._handlers: Dict[str, List[MessageHandler]] = defaultdict(list)
        self._processed = 0

    def publish(self, topic: str, event: Any) -> None:
        """Publish an event to a topic."""
        handlers = self._handlers[topic]
        for handler in handlers:
            try:
                handler(event)
                self._processed += 1
            except Exception as e:
                logger.error(f"Error handling message on topic {topic}: {e}", exc_info=True)
                # In-memory bus just logs and moves on, emulating dead-letter behaviour or retry 
                # mechanism depending on higher level implementations.

    def subscribe(self, topic: str, handler: MessageHandler) -> None:
        """Subscribe a handler to a topic."""
        if handler not in self._handlers[topic]:
            self._handlers[topic].append(handler)
            logger.info(f"Subscribed to topic '{topic}'")

    def acknowledge(self, message: Any) -> None:
        """Acknowledge the successful processing of a message."""
        # For in-memory, acknowledgement is a no-op as publish is synchronous
        pass

    def reject(self, message: Any, requeue: bool = False) -> None:
        """Reject a message, optionally requeueing it."""
        logger.warning(f"Message rejected. Requeue: {requeue}")
        if requeue:
            # Requeueing logic would involve pushing it back to a queue for an async loop,
            # but since in-memory is currently a simple synchronous loop, we won't implement
            # a full retry loop here to avoid infinite recursion blocks.
            pass
