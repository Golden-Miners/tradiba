from typing import Any
from tradiba.sdk_v2.context import StrategyContext
from tradiba.sdk_v2.lifecycle import LifecycleHooks
from tradiba.sdk_v2.parameters import Parameter

class Strategy(LifecycleHooks):
    """
    Base Strategy for SDK v2.
    Integrates declarative parameters and the canonical context.
    """
    def __init__(self) -> None:
        self.ctx: StrategyContext | None = None
        
    def _bind_context(self, ctx: StrategyContext) -> None:
        """Internal hook used by the runtime to inject context."""
        self.ctx = ctx
        
    def get_parameters(self) -> dict[str, Any]:
        """Extracts all declarative parameters and their current values."""
        params = {}
        for name in dir(self):
            # Inspect the class dictionary for Parameter descriptors
            cls_attr = getattr(type(self), name, None)
            if isinstance(cls_attr, Parameter):
                params[name] = getattr(self, name)
        return params
        
    def extract_state(self) -> dict[str, Any]:
        """
        Called prior to hot reload. Strategies should return a dict of their 
        important runtime state (e.g., active orders, local caches).
        """
        return {}
        
    def restore_state(self, state: dict[str, Any]) -> None:
        """
        Called after hot reload. Strategies should restore their internal state.
        """
        pass
