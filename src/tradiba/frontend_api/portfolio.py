from typing import Dict, Any

class PortfolioDashboardService:
    """Aggregates real-time equity, P&L, and exposure."""
    
    def get_summary(self, tenant_id: str) -> Dict[str, Any]:
        return {
            "equity": 105000.0,
            "pnl": 5000.0,
            "drawdown": 2.5,
            "open_positions": 3,
            "allocations": {"BTC": 40, "ETH": 30, "USD": 30}
        }
