def calculate_max_drawdown(equity_curve: list[float]) -> float:
    if not equity_curve:
        return 0.0
    peak = equity_curve[0]
    max_dd = 0.0
    for equity in equity_curve:
        if equity > peak:
            peak = equity
        dd = (peak - equity) / peak if peak > 0 else 0
        if dd > max_dd:
            max_dd = dd
    return max_dd

def calculate_recovery_factor(trades, max_drawdown: float) -> float:
    net_profit = sum(t.profit for t in trades)
    if max_drawdown == 0:
        return float('inf')
    return net_profit / max_drawdown
