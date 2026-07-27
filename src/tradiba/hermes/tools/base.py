from abc import ABC, abstractmethod
from typing import Any

class BaseTool(ABC):
    """Abstract base class for tools that Hermes can invoke."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        pass
        
    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """Executes the tool logic."""
        pass

class PortfolioQueryTool(BaseTool):
    @property
    def name(self) -> str: return "portfolio_query"
    
    @property
    def description(self) -> str: return "Queries the user's portfolio exposure and balance."
    
    async def execute(self, **kwargs) -> Any:
        # Mocks a call to tradiba.portfolio
        return {"balance": 100000, "exposure": "Long EURUSD 1.0 lot"}

class StrategyBacktestTool(BaseTool):
    @property
    def name(self) -> str: return "strategy_backtest"
    
    @property
    def description(self) -> str: return "Runs a backtest for a given strategy and symbol."
    
    async def execute(self, strategy: str, symbol: str, **kwargs) -> Any:
        # Mocks a call to tradiba.research
        return {"sharpe": 1.5, "max_drawdown": 4.2, "win_rate": 0.55}
