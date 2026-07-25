from tradiba.sdk_v2.context import StrategyContext

class LifecycleHooks:
    """
    Standard lifecycle methods for strategies.
    Strategies should override these to manage resources safely.
    """
    def on_initialize(self, ctx: StrategyContext) -> None:
        """Called once when the strategy is loaded."""
        pass
        
    def on_start(self, ctx: StrategyContext) -> None:
        """Called when the strategy begins active trading."""
        pass
        
    def on_pause(self, ctx: StrategyContext) -> None:
        """Called to temporarily suspend trading activity."""
        pass
        
    def on_resume(self, ctx: StrategyContext) -> None:
        """Called to resume from a paused state."""
        pass
        
    def on_stop(self, ctx: StrategyContext) -> None:
        """Called when active trading ends."""
        pass
        
    def on_dispose(self, ctx: StrategyContext) -> None:
        """Called right before the instance is destroyed (or hot reloaded)."""
        pass
