import os
from dataclasses import dataclass
from datetime import datetime
from tradiba.persistence.repositories.trade_repository import TradeRepository
from tradiba.persistence.repositories.snapshot_repository import SnapshotRepository

from .performance import (
    calculate_net_profit, calculate_gross_profit, calculate_gross_loss,
    calculate_win_rate, calculate_expectancy
)
from .drawdown import calculate_max_drawdown
from .statistics import calculate_sharpe_ratio

@dataclass(slots=True)
class TradingReport:
    net_profit: float
    gross_profit: float
    gross_loss: float
    win_rate: float
    drawdown: float
    sharpe: float
    expectancy: float

def generate_report(trade_repo: TradeRepository, snapshot_repo: SnapshotRepository, output_dir: str = "reports") -> str:
    trades = trade_repo.all()
    snapshots = snapshot_repo.all()
    
    if not trades:
        return "No trades to report."
        
    equity_curve = [s.equity for s in snapshots] if snapshots else [1000.0 + sum(t.profit for t in trades[:i+1]) for i in range(len(trades))]
    
    returns = []
    if len(equity_curve) > 1:
        returns = [(equity_curve[i] - equity_curve[i-1])/equity_curve[i-1] for i in range(1, len(equity_curve))]
    
    report = TradingReport(
        net_profit=calculate_net_profit(trades),
        gross_profit=calculate_gross_profit(trades),
        gross_loss=calculate_gross_loss(trades),
        win_rate=calculate_win_rate(trades),
        drawdown=calculate_max_drawdown(equity_curve),
        sharpe=calculate_sharpe_ratio(returns),
        expectancy=calculate_expectancy(trades)
    )
    
    html = f"""
    <html>
    <head><title>Trading Report</title></head>
    <body style="font-family: sans-serif; margin: 2rem;">
        <h1>Trading Report - {datetime.now().date()}</h1>
        <h2>Summary</h2>
        <ul>
            <li>Net Profit: {report.net_profit:.2f}</li>
            <li>Gross Profit: {report.gross_profit:.2f}</li>
            <li>Gross Loss: {report.gross_loss:.2f}</li>
            <li>Win Rate: {report.win_rate*100:.1f}%</li>
            <li>Max Drawdown: {report.drawdown*100:.1f}%</li>
            <li>Sharpe Ratio: {report.sharpe:.2f}</li>
            <li>Expectancy: {report.expectancy:.2f}</li>
        </ul>
    </body>
    </html>
    """
    
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"{datetime.now().strftime('%Y-%m-%d')}.html")
    with open(filename, "w") as f:
        f.write(html)
        
    return filename
