import logging
from typing import Any

logger = logging.getLogger(__name__)

class StrategyDebugger:
    """
    Utilities for interactively tracing decision paths and state in the SDK.
    """
    @staticmethod
    def trace(msg: str, *args: Any) -> None:
        """Trace a step in the strategy execution."""
        logger.debug(f"[TRADITIONAL DEBUG] {msg}", *args)
        
    @staticmethod
    def inspect(obj: Any) -> dict[str, Any]:
        """Inspects internal state of an object."""
        return {k: v for k, v in vars(obj).items() if not k.startswith('_')}
