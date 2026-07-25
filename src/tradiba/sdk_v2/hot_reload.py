import importlib
import sys
from tradiba.sdk_v2.strategy import Strategy

class HotReloader:
    """
    Manages safe hot-swapping of strategy instances.
    """
    def __init__(self, module_name: str, strategy_class_name: str) -> None:
        self.module_name = module_name
        self.strategy_class_name = strategy_class_name

    def reload(self, old_instance: Strategy) -> Strategy:
        """
        Reloads the module, extracts state from the old instance,
        creates a new instance, and injects the state.
        """
        # Tell old instance to pause and extract state
        old_instance.on_pause(old_instance.ctx) # type: ignore
        state = old_instance.extract_state()
        old_instance.on_dispose(old_instance.ctx) # type: ignore
        
        # Reload the module
        if self.module_name not in sys.modules:
            raise RuntimeError(f"Module {self.module_name} not loaded.")
        
        module = sys.modules[self.module_name]
        importlib.reload(module)
        
        # Instantiate the new class
        new_class = getattr(module, self.strategy_class_name)
        new_instance: Strategy = new_class()
        
        # Restore state
        new_instance._bind_context(old_instance.ctx) # type: ignore
        new_instance.restore_state(state)
        new_instance.on_resume(new_instance.ctx) # type: ignore
        
        return new_instance
