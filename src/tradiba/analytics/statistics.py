import math

def calculate_consecutive_wins(trades) -> int:
    max_streak = 0
    current_streak = 0
    for t in trades:
        if t.profit > 0:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
    return max_streak

def calculate_consecutive_losses(trades) -> int:
    max_streak = 0
    current_streak = 0
    for t in trades:
        if t.profit < 0:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
    return max_streak

def calculate_sharpe_ratio(returns: list[float], risk_free_rate: float = 0.0) -> float:
    if len(returns) < 2:
        return 0.0
    avg_return = sum(returns) / len(returns)
    excess_returns = [r - risk_free_rate for r in returns]
    avg_excess_return = sum(excess_returns) / len(excess_returns)
    variance = sum((r - avg_return) ** 2 for r in returns) / (len(returns) - 1)
    std_dev = math.sqrt(variance)
    if std_dev == 0:
        return 0.0
    return avg_excess_return / std_dev

def calculate_sortino_ratio(returns: list[float], risk_free_rate: float = 0.0) -> float:
    if len(returns) < 2:
        return 0.0
    excess_returns = [r - risk_free_rate for r in returns]
    avg_excess_return = sum(excess_returns) / len(excess_returns)
    downside_returns = [r for r in returns if r < 0]
    if not downside_returns:
        return float('inf')
    downside_variance = sum(r ** 2 for r in downside_returns) / len(downside_returns)
    downside_std_dev = math.sqrt(downside_variance)
    if downside_std_dev == 0:
        return float('inf')
    return avg_excess_return / downside_std_dev
