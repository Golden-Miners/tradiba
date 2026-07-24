from tradiba.events.bus import EventBus
from .models import ExecutionReport, ExecutionStatus
from .broker import BrokerExecutor
from .repository import ExecutionRepository
from .validator import ExecutionValidator
from .retry import RetryPolicy, RecoverableExecutionError
from .events import OrderSubmittedEvent, OrderFilledEvent, OrderRejectedEvent, ExecutionFailedEvent
from tradiba.risk.models import TradePlan
from tradiba.portfolio.aggregate import Portfolio
import uuid
from datetime import datetime, timezone

class ExecutionService:
    def __init__(
        self,
        executor: BrokerExecutor,
        repository: ExecutionRepository,
        validator: ExecutionValidator,
        bus: EventBus,
        portfolio: Portfolio
    ):
        self.executor = executor
        self.repository = repository
        self.validator = validator
        self.bus = bus
        self.portfolio = portfolio
        self.retry_policy = RetryPolicy()

    def execute(self, trade_plan: TradePlan) -> ExecutionReport:
        # Idempotency check: use signal_id as the execution key
        key = trade_plan.signal_id
        existing = self.repository.find_by_execution_key(key)
        if existing:
            return existing

        # Validation
        try:
            self.validator.validate(trade_plan, self.portfolio)
        except Exception as e:
            report = ExecutionReport(
                execution_id=str(uuid.uuid4()),
                trade_plan_id=trade_plan.signal_id,
                broker_order_id=None,
                symbol=trade_plan.symbol,
                status=ExecutionStatus.FAILED,
                requested_price=trade_plan.entry,
                executed_price=None,
                volume=trade_plan.position_size,
                submitted_at=datetime.now(timezone.utc),
                completed_at=datetime.now(timezone.utc),
                reason=str(e)
            )
            self.repository.save(report)
            self.publish(report)
            return report

        # Execution with Retries
        try:
            report = self.retry_policy.execute(self.executor.submit, trade_plan)
        except RecoverableExecutionError as e:
            report = ExecutionReport(
                execution_id=str(uuid.uuid4()),
                trade_plan_id=trade_plan.signal_id,
                broker_order_id=None,
                symbol=trade_plan.symbol,
                status=ExecutionStatus.FAILED,
                requested_price=trade_plan.entry,
                executed_price=None,
                volume=trade_plan.position_size,
                submitted_at=datetime.now(timezone.utc),
                completed_at=datetime.now(timezone.utc),
                reason="Retry exhaustion: " + str(e)
            )
        except Exception as e:
            report = ExecutionReport(
                execution_id=str(uuid.uuid4()),
                trade_plan_id=trade_plan.signal_id,
                broker_order_id=None,
                symbol=trade_plan.symbol,
                status=ExecutionStatus.REJECTED,
                requested_price=trade_plan.entry,
                executed_price=None,
                volume=trade_plan.position_size,
                submitted_at=datetime.now(timezone.utc),
                completed_at=datetime.now(timezone.utc),
                reason="Broker rejection: " + str(e)
            )

        self.repository.save(report)
        self.publish(report)
        return report

    def publish(self, report: ExecutionReport):
        if report.status == ExecutionStatus.SUBMITTED:
            self.bus.publish(OrderSubmittedEvent(report))
        elif report.status == ExecutionStatus.FILLED:
            self.bus.publish(OrderFilledEvent(report))
        elif report.status == ExecutionStatus.REJECTED:
            self.bus.publish(OrderRejectedEvent(report))
        elif report.status == ExecutionStatus.FAILED:
            self.bus.publish(ExecutionFailedEvent(report))
