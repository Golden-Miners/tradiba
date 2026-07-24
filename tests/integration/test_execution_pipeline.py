from decimal import Decimal
from datetime import datetime, timezone
from tradiba.execution.service import ExecutionService
from tradiba.execution.validator import ExecutionValidator
from tradiba.execution.repository import ExecutionRepository
from tradiba.execution.models import ExecutionReport, ExecutionStatus
from tradiba.execution.broker import BrokerExecutor
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
    def submit(self, trade_plan):
        return ExecutionReport(
            execution_id="123",
            trade_plan_id=trade_plan.signal_id,
            broker_order_id=456,
            symbol=trade_plan.symbol,
            status=ExecutionStatus.FILLED,
            requested_price=trade_plan.entry,
            executed_price=trade_plan.entry,
            volume=trade_plan.position_size,
            submitted_at=datetime.now(timezone.utc),
            completed_at=datetime.now(timezone.utc)
        )
    def modify(self, order): pass
    def cancel(self, order_id): pass
    def synchronize(self): pass

def test_execution_pipeline():
    # 1. TradePlan
    plan = TradePlan(
        signal_id="sig_test_pipe",
        symbol="GBPUSD",
        side="SELL",
        entry=Decimal('1.2500'),
        stop_loss=Decimal('1.2600'),
        take_profit=Decimal('1.2300'),
        position_size=Decimal('1.0'),
        risk_amount=Decimal('100.0'),
        decision=RiskDecision.APPROVED
    )
    
    # 2. Dependencies
    broker = MockBroker()
    repo = MockRepository()
    val = ExecutionValidator()
    bus = EventBus()
    acc = AccountSnapshot(datetime.now(timezone.utc), Decimal(0), Decimal(0), Decimal(0), Decimal(0), Decimal(0), Decimal(0), Decimal(0))
    portfolio = Portfolio(acc)
    
    # 3. ExecutionService
    svc = ExecutionService(broker, repo, val, bus, portfolio)
    
    # 4. Execute
    report = svc.execute(plan)
    
    # 5. Verify ExecutionReport
    assert report.status == ExecutionStatus.FILLED
    assert report.trade_plan_id == "sig_test_pipe"
    assert report.broker_order_id == 456
    assert report.symbol == "GBPUSD"
