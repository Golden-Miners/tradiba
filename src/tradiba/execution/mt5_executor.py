from .broker import BrokerExecutor
from .models import ExecutionReport, ExecutionStatus
from tradiba.risk.models import TradePlan
import uuid
from datetime import datetime, timezone

class MT5Executor(BrokerExecutor):
    def submit(self, trade_plan: TradePlan) -> ExecutionReport:
        return ExecutionReport(
            execution_id=str(uuid.uuid4()),
            trade_plan_id=trade_plan.signal_id,
            broker_order_id=12345,
            symbol=trade_plan.symbol,
            status=ExecutionStatus.FILLED,
            requested_price=trade_plan.entry,
            executed_price=trade_plan.entry,
            volume=trade_plan.position_size,
            submitted_at=datetime.now(timezone.utc),
            completed_at=datetime.now(timezone.utc),
        )

    def modify(self, order):
        pass

    def cancel(self, order_id):
        pass

    def synchronize(self):
        pass
