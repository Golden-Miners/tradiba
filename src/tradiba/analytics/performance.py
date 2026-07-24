def calculate_net_profit(trades) -> float:
    return sum(t.profit for t in trades)

def calculate_gross_profit(trades) -> float:
    return sum(t.profit for t in trades if t.profit > 0)

def calculate_gross_loss(trades) -> float:
    return abs(sum(t.profit for t in trades if t.profit < 0))

def calculate_win_rate(trades) -> float:
    if not trades:
        return 0.0
    wins = len([t for t in trades if t.profit > 0])
    return wins / len(trades)

def calculate_loss_rate(trades) -> float:
    if not trades:
        return 0.0
    return 1.0 - calculate_win_rate(trades)

def calculate_average_win(trades) -> float:
    wins = [t.profit for t in trades if t.profit > 0]
    return sum(wins) / len(wins) if wins else 0.0

def calculate_average_loss(trades) -> float:
    losses = [t.profit for t in trades if t.profit < 0]
    return sum(losses) / len(losses) if losses else 0.0

def calculate_profit_factor(trades) -> float:
    gp = calculate_gross_profit(trades)
    gl = calculate_gross_loss(trades)
    if gl == 0:
        return float('inf') if gp > 0 else 0.0
    return gp / gl

def calculate_expectancy(trades) -> float:
    win_rate = calculate_win_rate(trades)
    avg_win = calculate_average_win(trades)
    avg_loss = abs(calculate_average_loss(trades))
    return (win_rate * avg_win) - ((1 - win_rate) * avg_loss)

def calculate_risk_reward_ratio(trades) -> float:
    avg_win = calculate_average_win(trades)
    avg_loss = abs(calculate_average_loss(trades))
    if avg_loss == 0:
        return float('inf')
    return avg_win / avg_loss
