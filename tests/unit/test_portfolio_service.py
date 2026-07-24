import pytest
from datetime import datetime, timezone
from decimal import Decimal
from tradiba.portfolio.account import AccountSnapshot
from tradiba.portfolio.position import Position, PositionStatus
from tradiba.portfolio.order import PendingOrder, PendingOrderStatus
from tradiba.portfolio.aggregate import Portfolio
from tradiba.portfolio.synchronizer import PortfolioSynchronizer
from tradiba.portfolio.repository import PortfolioRepository
from tradiba.portfolio.service import PortfolioService
from tradiba.portfolio.events import PortfolioUpdatedEvent
from tradiba.events.bus import EventBus
from tradiba.portfolio.statistics import StatisticsCalculator

class DummySynchronizer(PortfolioSynchronizer):
    def synchronize(self) -> Portfolio:
        account = AccountSnapshot(
            timestamp=datetime.now(timezone.utc),
            balance=Decimal('10000.0'),
            equity=Decimal('10500.0'),
            margin=Decimal('100.0'),
            free_margin=Decimal('10400.0'),
            margin_level=Decimal('10500.0'),
            floating_profit=Decimal('500.0'),
            realized_profit=Decimal('0.0')
        )
        port = Portfolio(account)
        pos = Position(
            ticket=1,
            symbol="EURUSD",
            volume=Decimal('1.0'),
            entry_price=Decimal('1.10'),
            current_price=Decimal('1.11'),
            stop_loss=Decimal('1.09'),
            take_profit=Decimal('1.12'),
            open_time=datetime.now(timezone.utc),
            profit=Decimal('500.0'),
            status=PositionStatus.OPEN
        )
        port.open_position(pos)
        
        order = PendingOrder(
            ticket=2,
            symbol="GBPUSD",
            volume=Decimal('0.5'),
            order_type="BUY_LIMIT",
            expiry=None,
            broker_state="PLACED",
            status=PendingOrderStatus.PENDING
        )
        port.add_order(order)
        return port

class DummyRepository(PortfolioRepository):
    def __init__(self):
        self.saved = None
    
    def save(self, portfolio: Portfolio):
        self.saved = portfolio
        
    def load(self) -> Portfolio | None:
        return self.saved

def test_portfolio_service():
    sync = DummySynchronizer()
    repo = DummyRepository()
    bus = EventBus()
    
    events_received = []
    def on_update(event):
        events_received.append(event)
        
    bus.subscribe(PortfolioUpdatedEvent, on_update)
    
    service = PortfolioService(sync, repo, bus)
    service.synchronize()
    
    # Verify Repository persistence
    assert repo.saved is not None
    assert repo.saved.account.balance == Decimal('10000.0')
    
    # Verify Portfolio update event emission
    assert len(events_received) == 1
    event = events_received[0]
    assert isinstance(event, PortfolioUpdatedEvent)
    assert event.portfolio.account.balance == Decimal('10000.0')
    
    # Verify Account snapshot creation
    assert event.portfolio.account.floating_profit == Decimal('500.0')

def test_position_lifecycle():
    port = Portfolio(AccountSnapshot(datetime.now(timezone.utc), Decimal(0), Decimal(0), Decimal(0), Decimal(0), Decimal(0), Decimal(0), Decimal(0)))
    
    pos = Position(1, "EURUSD", Decimal('1.0'), Decimal('1.1'), Decimal('1.1'), Decimal('1.0'), Decimal('1.2'), datetime.now(timezone.utc), Decimal('0'), PositionStatus.OPEN)
    
    # Open
    port.open_position(pos)
    assert len(port.positions) == 1
    assert port.positions[1].status == PositionStatus.OPEN
    
    # Close
    port.close_position(1)
    assert port.positions[1].status == PositionStatus.CLOSED

def test_pending_order_lifecycle():
    port = Portfolio(AccountSnapshot(datetime.now(timezone.utc), Decimal(0), Decimal(0), Decimal(0), Decimal(0), Decimal(0), Decimal(0), Decimal(0)))
    
    order = PendingOrder(2, "GBPUSD", Decimal('0.5'), "BUY_LIMIT", None, "", PendingOrderStatus.PENDING)
    
    # Add
    port.add_order(order)
    assert len(port.pending_orders) == 1
    assert port.pending_orders[2].status == PendingOrderStatus.PENDING
    
    # Fill
    port.fill_order(2)
    assert port.pending_orders[2].status == PendingOrderStatus.FILLED
    
    # Cancel
    port.cancel_order(2)
    assert port.pending_orders[2].status == PendingOrderStatus.CANCELLED

def test_statistics_recalculation():
    port = Portfolio(AccountSnapshot(datetime.now(timezone.utc), Decimal(0), Decimal(0), Decimal(0), Decimal(0), Decimal(0), Decimal(0), Decimal(0)))
    pos1 = Position(1, "EURUSD", Decimal('1.0'), Decimal('1.1'), Decimal('1.1'), Decimal('1.0'), Decimal('1.2'), datetime.now(timezone.utc), Decimal('0'), PositionStatus.OPEN)
    pos2 = Position(2, "GBPUSD", Decimal('1.0'), Decimal('1.1'), Decimal('1.1'), Decimal('1.0'), Decimal('1.2'), datetime.now(timezone.utc), Decimal('0'), PositionStatus.OPEN)
    
    port.open_position(pos1)
    port.open_position(pos2)
    
    calc = StatisticsCalculator()
    stats = calc.calculate(port)
    
    assert stats.open_positions == 2
