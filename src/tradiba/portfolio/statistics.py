from decimal import Decimal
from dataclasses import dataclass
from .aggregate import Portfolio

@dataclass(slots=True, frozen=True)
class PortfolioStatistics:
    open_positions: int
    closed_trades: int
    win_rate: Decimal
    profit_factor: Decimal
    expectancy: Decimal
    average_win: Decimal
    average_loss: Decimal
    largest_win: Decimal
    largest_loss: Decimal
    current_drawdown: Decimal
    maximum_drawdown: Decimal

class StatisticsCalculator:
    def calculate(self, portfolio: Portfolio) -> PortfolioStatistics:
        return PortfolioStatistics(
            open_positions=len(portfolio.positions),
            closed_trades=0,
            win_rate=Decimal('0'),
            profit_factor=Decimal('0'),
            expectancy=Decimal('0'),
            average_win=Decimal('0'),
            average_loss=Decimal('0'),
            largest_win=Decimal('0'),
            largest_loss=Decimal('0'),
            current_drawdown=Decimal('0'),
            maximum_drawdown=Decimal('0')
        )
