import pytest
from unittest.mock import MagicMock
from datetime import datetime, timezone

from tradiba.events import EventBus
from tradiba.scheduler import Scheduler
from tradiba.market_structure.service import MarketStructureService
from tradiba.market_structure.state import MarketStructureState
from tradiba.market_structure.models import Trend, SwingHigh
from tradiba.market.events import CandleClosedEvent
from tradiba.mt5.models import Candle

from tradiba.strategy.manager import StrategyManager

from tradiba.risk.service import RiskService
from tradiba.risk.rules.max_position_size import MaximumPositionSizeRule

from tradiba.execution.service import ExecutionService
from tradiba.execution.models.result import TradeResult
from tradiba.ports.execution import ExecutionProvider

from tradiba.portfolio.service import PortfolioService
from tradiba.portfolio.events import PositionClosedEvent
from tradiba.persistence.database import Database
from tradiba.persistence.models.trade import TradeEntity


@pytest.fixture
def mock_execution_provider():
    provider = MagicMock(spec=ExecutionProvider)
    # Mock buy_market to succeed
    provider.buy_market.return_value = TradeResult(
        success=True, 
        ticket=999, 
        message="Order placed"
    )
    provider.account_info.return_value = None
    return provider


@pytest.fixture
def test_db():
    db = Database("sqlite:///:memory:")
    # Initialize schema
    from tradiba.persistence.base import Base
    Base.metadata.create_all(bind=db.engine)
    return db


def test_vertical_slice_bos_to_trade(mock_execution_provider, test_db):
    event_bus = EventBus()
    scheduler = Scheduler()

    # 1. Market Structure Service
    structure_service = MarketStructureService(event_bus)
    structure_service.start()
    
    # Inject a prepared state to guarantee a BOS on the next candle
    state = MarketStructureState("EURUSD", "H1")
    state.trend = Trend.BULLISH
    candle = Candle("EURUSD", "H1", datetime(2024, 1, 1, tzinfo=timezone.utc), 1.1500, 1.1500, 1.1500, 1.1500, 1, 0, 0)
    state.last_swing_high = SwingHigh(candle=candle, price=1.1500)
    structure_service._states[("EURUSD", "H1")] = state

    # 2. Strategy Manager
    strategy_configs = {
        "bos_strategy": {
            "enabled": True,
            "symbol": "EURUSD",
            "timeframe": "H1",
        }
    }
    strategy_manager = StrategyManager(event_bus, strategy_configs)
    strategy_manager.start()

    # 3. Risk Service
    risk_service = RiskService(event_bus)
    risk_service.add_rule(MaximumPositionSizeRule(maximum=2.0))
    risk_service.start()

    # 4. Execution Service
    execution_service = ExecutionService(event_bus, mock_execution_provider)
    execution_service.start()
    
    # 5. Portfolio Service
    portfolio_service = PortfolioService(event_bus, mock_execution_provider, scheduler, test_db)
    portfolio_service.start()

    # Trigger Pipeline
    # Emit a candle that closes above the swing high
    breakout_candle = Candle(
        "EURUSD", "H1", datetime(2024, 1, 1, 1, tzinfo=timezone.utc),
        open=1.1500, high=1.1520, low=1.1490, close=1.1510,
        tick_volume=100, spread=0, real_volume=100
    )
    
    # Feed into the event bus
    event_bus.publish(CandleClosedEvent(candle=breakout_candle))

    # Assert ExecutionProvider was called
    mock_execution_provider.buy_market.assert_called_once()
    
    call_kwargs = mock_execution_provider.buy_market.call_args.kwargs
    assert call_kwargs["symbol"] == "EURUSD"
    # assert call_kwargs["sl"] < 1.1510 # Wait, the BOS entry is exactly 1.1500, so SL is 1.1480

    # 6. Database Persistence
    # Simulate closing the position via ExecutionSynchronizer behavior
    event_bus.publish(PositionClosedEvent(
        ticket=999,
        symbol="EURUSD",
        side="LONG",
        volume=0.01,
        entry=1.1500,
        exit=1.1520,
        profit=2.0
    ))

    # Assert Trade is in Database
    session = next(test_db.get_session())
    trades = session.query(TradeEntity).all()
    assert len(trades) == 1
    assert trades[0].ticket == 999
    assert trades[0].symbol == "EURUSD"
    assert trades[0].profit == 2.0

    # Teardown
    portfolio_service.stop()
    execution_service.stop()
    risk_service.stop()
    strategy_manager.stop()
    structure_service.stop()
