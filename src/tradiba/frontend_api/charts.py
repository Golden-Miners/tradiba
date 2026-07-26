from typing import Dict, Any, List

class ChartDataService:
    """Serves candlestick data and Market Structure overlays."""
    
    def get_candlesticks(self, symbol: str, timeframe: str) -> List[Dict[str, Any]]:
        # Mock data return
        return [{"time": "2026-07-26", "open": 100, "high": 105, "low": 98, "close": 102}]
        
    def get_ict_overlays(self, symbol: str) -> Dict[str, List[Any]]:
        return {
            "order_blocks": [],
            "fvg": [],
            "choch": []
        }
