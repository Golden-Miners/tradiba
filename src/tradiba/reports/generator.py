from typing import Protocol, Dict, Any
from datetime import date

class ReportGenerator(Protocol):
    """Protocol for generating institutional reports."""
    
    def generate_daily_pnl(self, target_date: date) -> Dict[str, Any]:
        ...
        
    def generate_weekly_risk(self, start_date: date, end_date: date) -> Dict[str, Any]:
        ...
        
    def export_to_csv(self, report_data: Dict[str, Any], filepath: str) -> bool:
        ...

class StandardReportGenerator:
    """
    Reference Implementation: Standard Reporting Generator.
    Aggregates data and exports to structured formats.
    """
    
    def __init__(self, data_store: Any):
        self.db = data_store
        
    def generate_daily_pnl(self, target_date: date) -> Dict[str, Any]:
        """Generate a Daily P&L report."""
        # Mock aggregation
        return {
            "date": target_date.isoformat(),
            "gross_pnl": 12500.0,
            "commissions": 450.0,
            "net_pnl": 12050.0,
            "total_trades": 142,
            "win_rate": 0.54,
            "top_strategy": "ict_silver_bullet"
        }
        
    def generate_weekly_risk(self, start_date: date, end_date: date) -> Dict[str, Any]:
        """Generate a Weekly Risk and Exposure report."""
        return {
            "period": f"{start_date.isoformat()} to {end_date.isoformat()}",
            "max_drawdown_usd": 45000.0,
            "avg_daily_var_95": 12000.0,
            "margin_utilization_peak_pct": 0.65
        }
        
    def export_to_csv(self, report_data: Dict[str, Any], filepath: str) -> bool:
        """Export flat report data to CSV."""
        import csv
        try:
            with open(filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(report_data.keys())
                writer.writerow(report_data.values())
            return True
        except Exception:
            return False
