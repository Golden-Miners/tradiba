import pytest
from datetime import datetime, timezone
from decimal import Decimal
from tradiba.execution.models import ExecutionReport, ExecutionStatus
from tradiba.execution.service import ExecutionService
from tradiba.execution.broker import BrokerExecutor
from tradiba.execution.repository import ExecutionRepository
from tradiba.execution.validator import ExecutionValidator
from tradiba.execution.retry import RecoverableExecutionError
from tradiba.execution.events import (
    OrderFilledEvent, OrderRejectedEvent, ExecutionFailedEvent
)
from tradiba.events.bus import EventBus
from tradiba.risk.models import TradePlan, RiskDecision
from tradiba.portfolio.aggregate import Portfolio
from tradiba.portfolio.account import AccountSnapshot

class MockRepository(ExecutionRepository):
    def __init__(self):
        self.store = {}
    
    def save(self, report: ExecutionReport):
        self.store[report.trade_plan_id] = report
        
    def find_by_execution_key(self, key: str) -> ExecutionReport | None:
        return self.store.get(key)

class MockBroker(BrokerExecutor):
    def __init__(self, behavior="success", fail_count=0):
        self.behavior = behavior
        self.fail_count = fail_count
        self.attempts = 0
        
    def submit(self, trade_plan):
        self.attempts += 1
        if self.fail_count > 0:
            self.fail_count -= 1
            raise RecoverableExecutionError("Network timeout")
            
        if self.behavior == "success":
            return ExecutionReport(
                execution_id="test_exec_id",
                trade_plan_id=trade_plan.signal_id,
                broker_order_id=123,
                symbol=trade_plan.symbol,
                status=ExecutionStatus.FILLED,
                requested_price=trade_plan.entry,
                executed_price=trade_plan.entry,
                volume=trade_plan.position_size,
                submitted_at=datetime.now(timezone.utc),
                completed_at=datetime.now(timezone.utc)
            )
        elif self.behavior == "reject":
            raise Exception("Insufficient margin")
            
    def modify(self, order): pass
    def cancel(self, order_id): pass
    def synchronize(self): pass

@pytest.fixture
def base_plan():
    return TradePlan(
        signal_id="sig123",
        symbol="EURUSD",
        side="BUY",
        entry=Decimal('1.10'),
        stop_loss=Decimal('1.09'),
        take_profit=Decimal('1.12'),
        position_size=Decimal('1.0'),
        risk_amount=Decimal('100.0'),
        decision=RiskDecision.APPROVED
    )

@pytest.fixture
def empty_portfolio():
    acc = AccountSnapshot(datetime.now(timezone.utc), Decimal(0), Decimal(0), Decimal(0), Decimal(0), Decimal(0), Decimal(0), Decimal(0))
    return Portfolio(acc)

def test_successful_execution(base_plan, empty_portfolio):
    broker = MockBroker("success")
    repo = MockRepository()
    val = ExecutionValidator()
    bus = EventBus()
    
    events = []
    bus.subscribe(OrderFilledEvent, lambda e: events.append(e))
    
    svc = ExecutionService(broker, repo, val, bus, empty_portfolio)
    report = svc.execute(base_plan)
    
    assert report.status == ExecutionStatus.FILLED
    assert repo.find_by_execution_key("sig123") is not None
    assert len(events) == 1
    assert events[0].report == report

def test_broker_rejection(base_plan, empty_portfolio):
    broker = MockBroker("reject")
    repo = MockRepository()
    val = ExecutionValidator()
    bus = EventBus()
    
    events = []
    bus.subscribe(OrderRejectedEvent, lambda e: events.append(e))
    
    svc = ExecutionService(broker, repo, val, bus, empty_portfolio)
    report = svc.execute(base_plan)
    
    assert report.status == ExecutionStatus.REJECTED
    assert "Insufficient margin" in report.reason
    assert len(events) == 1

def test_validator_failure(empty_portfolio):
    broker = MockBroker("success")
    repo = MockRepository()
    val = ExecutionValidator()
    bus = EventBus()
    
    events = []
    bus.subscribe(ExecutionFailedEvent, lambda e: events.append(e))
    
    # 0 volume should fail validation
    plan = TradePlan("sig1", "EURUSD", "BUY", Decimal(1), Decimal(1), Decimal(1), Decimal(0), Decimal(0), RiskDecision.APPROVED)
    
    svc = ExecutionService(broker, repo, val, bus, empty_portfolio)
    report = svc.execute(plan)
    
    assert report.status == ExecutionStatus.FAILED
    assert "greater than zero" in report.reason
    assert len(events) == 1

def test_duplicate_execution_prevention(base_plan, empty_portfolio):
    broker = MockBroker("success")
    repo = MockRepository()
    val = ExecutionValidator()
    bus = EventBus()
    
    svc = ExecutionService(broker, repo, val, bus, empty_portfolio)
    r1 = svc.execute(base_plan)
    r2 = svc.execute(base_plan)
    
    assert r1 is r2
    assert broker.attempts == 1

def test_retry_success(base_plan, empty_portfolio):
    broker = MockBroker("success", fail_count=2)
    repo = MockRepository()
    val = ExecutionValidator()
    bus = EventBus()
    
    svc = ExecutionService(broker, repo, val, bus, empty_portfolio)
    svc.retry_policy.initial_delay = 0.01
    report = svc.execute(base_plan)
    
    assert report.status == ExecutionStatus.FILLED
    assert broker.attempts == 3

def test_retry_exhaustion(base_plan, empty_portfolio):
    broker = MockBroker("success", fail_count=10)
    repo = MockRepository()
    val = ExecutionValidator()
    bus = EventBus()
    
    svc = ExecutionService(broker, repo, val, bus, empty_portfolio)
    svc.retry_policy.initial_delay = 0.01
    svc.retry_policy.max_attempts = 3
    
    report = svc.execute(base_plan)
    
    assert report.status == ExecutionStatus.FAILED
    assert "Retry exhaustion" in report.reason
    assert broker.attempts == 3
