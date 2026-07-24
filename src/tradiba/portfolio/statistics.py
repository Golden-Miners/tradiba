def calculate_win_rate(trades: list) -> float:
    if not trades:
        return 0.0
    wins = [t for t in trades if getattr(t, 'profit', 0) > 0]
    return len(wins) / len(trades)

def calculate_realized_pl(trades: list) -> float:
    return sum(getattr(t, 'profit', 0) for t in trades)

def calculate_unrealized_pl(positions: list) -> float:
    return sum(getattr(p, 'profit', 0) for p in positions)

def calculate_average_win(trades: list) -> float:
    wins = [getattr(t, 'profit', 0) for t in trades if getattr(t, 'profit', 0) > 0]
    return sum(wins) / len(wins) if wins else 0.0

def calculate_average_loss(trades: list) -> float:
    losses = [getattr(t, 'profit', 0) for t in trades if getattr(t, 'profit', 0) <= 0]
    return sum(losses) / len(losses) if losses else 0.0

def calculate_expectancy(trades: list) -> float:
    win_rate = calculate_win_rate(trades)
    avg_win = calculate_average_win(trades)
    avg_loss = abs(calculate_average_loss(trades))
    return (win_rate * avg_win) - ((1 - win_rate) * avg_loss)

def calculate_profit_factor(trades: list) -> float:
    gross_profit = sum(getattr(t, 'profit', 0) for t in trades if getattr(t, 'profit', 0) > 0)
    gross_loss = abs(sum(getattr(t, 'profit', 0) for t in trades if getattr(t, 'profit', 0) < 0))
    return gross_profit / gross_loss if gross_loss != 0 else float('inf')

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
