from typing import List, Dict, Any

class SignalStreamService:
    """Streams strategy signals to the Signal Panel."""
    
    def get_active_signals(self) -> List[Dict[str, Any]]:
        return [
            {
                "time": "2026-07-26T10:00:00Z",
                "asset": "BTC/USD",
                "strategy": "MeanReversion",
                "direction": "Buy",
                "confidence": 0.85,
                "entry": 60000.0,
                "stop": 59000.0,
                "targets": [62000.0, 64000.0],
                "status": "Pending"
            }
        ]
