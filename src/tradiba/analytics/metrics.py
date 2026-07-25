from decimal import Decimal

def calculate_diversification_ratio(portfolio_volatility: float, weighted_average_volatility: float) -> float:
    """
    Calculates the diversification ratio of a portfolio.
    Ratio > 1 indicates benefit from diversification.
    """
    if portfolio_volatility == 0:
        return 1.0
    return weighted_average_volatility / portfolio_volatility

def calculate_drawdown(peak_equity: Decimal, current_equity: Decimal) -> float:
    """
    Calculates the current drawdown from peak equity.
    """
    if peak_equity == 0:
        return 0.0
    return float((peak_equity - current_equity) / peak_equity)
