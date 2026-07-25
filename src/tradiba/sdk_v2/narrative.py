from typing import Any

class MarketNarrative:
    """
    Query API for market state logic (trends, ICT concepts, etc)
    without directly inspecting engine internals.
    """
    def bias(self) -> str:
        """Returns the current directional bias (bullish/bearish/neutral)."""
        return "neutral"
        
    def trend(self) -> str:
        return "ranging"
        
    def active_fvgs(self) -> list[dict[str, Any]]:
        """Returns active Fair Value Gaps."""
        return []
        
    def active_order_blocks(self) -> list[dict[str, Any]]:
        """Returns active Order Blocks."""
        return []
        
    def active_liquidity(self) -> list[dict[str, Any]]:
        """Returns active Liquidity pools/sweeps."""
        return []
