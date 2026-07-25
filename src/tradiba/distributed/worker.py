from abc import ABC, abstractmethod
import logging
from typing import Any
import asyncio

logger = logging.getLogger(__name__)

class Worker(ABC):
    """
    Base class for all distributed workers.
    """
    def __init__(self, name: str):
        self.name = name
        self._is_running = False

    async def start(self) -> None:
        """Starts the worker processing loop."""
        logger.info(f"Worker {self.name} starting...")
        self._is_running = True
        try:
            await self._run()
        except asyncio.CancelledError:
            logger.info(f"Worker {self.name} cancelled, shutting down.")
        except Exception as e:
            logger.error(f"Worker {self.name} encountered fatal error: {e}", exc_info=True)
        finally:
            await self.stop()

    async def stop(self) -> None:
        """Gracefully stops the worker."""
        if self._is_running:
            logger.info(f"Worker {self.name} stopping...")
            self._is_running = False
            await self._cleanup()

    def health(self) -> dict[str, Any]:
        """Returns health information and capacity metrics."""
        return {
            "name": self.name,
            "status": "running" if self._is_running else "stopped",
        }

    @abstractmethod
    async def process(self, message: Any) -> None:
        """Process an incoming message/command."""
        pass

    @abstractmethod
    async def _run(self) -> None:
        """Internal loop logic to be implemented by specific workers."""
        pass

    async def _cleanup(self) -> None:
        """Cleanup resources on shutdown."""
        pass
