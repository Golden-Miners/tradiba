from decimal import Decimal

from tradiba.portfolio.position import Position, PositionStatus
from tradiba.portfolio.account import AccountSnapshot
from tradiba.portfolio.order import PendingOrder, PendingOrderStatus
from tradiba.portfolio.aggregate import Portfolio
from tradiba.execution.models import ExecutionReport, ExecutionStatus

from tradiba.persistence.models.position import PositionModel
from tradiba.persistence.models.account import AccountModel
from tradiba.persistence.models.order import OrderModel
from tradiba.persistence.models.execution import ExecutionModel

class PositionMapper:
    @staticmethod
    def to_domain(model: PositionModel) -> Position:
        return Position(
            ticket=int(model.ticket),
            symbol=model.symbol,
            volume=Decimal(str(model.volume)),
            entry_price=Decimal(str(model.entry_price)),
            current_price=Decimal(str(model.current_price)),
            stop_loss=Decimal(str(model.stop_loss)),
            take_profit=Decimal(str(model.take_profit)),
            open_time=model.open_time,
            profit=Decimal(str(model.profit)),
            status=PositionStatus(model.status)
        )

    @staticmethod
    def to_model(position: Position, snapshot_version: int) -> PositionModel:
        return PositionModel(
            ticket=position.ticket,
            snapshot_version=snapshot_version,
            symbol=position.symbol,
            volume=position.volume,
            entry_price=position.entry_price,
            current_price=position.current_price,
            stop_loss=position.stop_loss,
            take_profit=position.take_profit,
            open_time=position.open_time,
            profit=position.profit,
            status=position.status.value
        )


class AccountMapper:
    @staticmethod
    def to_domain(model: AccountModel) -> AccountSnapshot:
        return AccountSnapshot(
            timestamp=model.timestamp,
            balance=Decimal(str(model.balance)),
            equity=Decimal(str(model.equity)),
            margin=Decimal(str(model.margin)),
            free_margin=Decimal(str(model.free_margin)),
            margin_level=Decimal(str(model.margin_level)),
            floating_profit=Decimal(str(model.floating_profit)),
            realized_profit=Decimal(str(model.realized_profit)),
        )

    @staticmethod
    def to_model(account: AccountSnapshot, snapshot_version: int) -> AccountModel:
        return AccountModel(
            snapshot_version=snapshot_version,
            timestamp=account.timestamp,
            balance=account.balance,
            equity=account.equity,
            margin=account.margin,
            free_margin=account.free_margin,
            margin_level=account.margin_level,
            floating_profit=account.floating_profit,
            realized_profit=account.realized_profit,
        )


class OrderMapper:
    @staticmethod
    def to_domain(model: OrderModel) -> PendingOrder:
        return PendingOrder(
            ticket=int(model.ticket),
            symbol=model.symbol,
            volume=Decimal(str(model.volume)),
            order_type=model.order_type,
            expiry=model.expiry,
            broker_state=model.broker_state,
            status=PendingOrderStatus(model.status)
        )

    @staticmethod
    def to_model(order: PendingOrder, snapshot_version: int) -> OrderModel:
        return OrderModel(
            ticket=order.ticket,
            snapshot_version=snapshot_version,
            symbol=order.symbol,
            volume=order.volume,
            order_type=order.order_type,
            expiry=order.expiry,
            broker_state=order.broker_state,
            status=order.status.value
        )


class ExecutionMapper:
    @staticmethod
    def to_domain(model: ExecutionModel) -> ExecutionReport:
        return ExecutionReport(
            execution_id=model.execution_id,
            trade_plan_id=model.trade_plan_id,
            broker_order_id=model.broker_order_id,
            symbol=model.symbol,
            status=ExecutionStatus(model.status),
            requested_price=Decimal(str(model.requested_price)),
            executed_price=Decimal(str(model.executed_price)) if model.executed_price else None,
            volume=Decimal(str(model.volume)),
            submitted_at=model.submitted_at,
            completed_at=model.completed_at,
            reason=model.reason
        )

    @staticmethod
    def to_model(execution: ExecutionReport) -> ExecutionModel:
        return ExecutionModel(
            execution_id=execution.execution_id,
            trade_plan_id=execution.trade_plan_id,
            broker_order_id=execution.broker_order_id,
            symbol=execution.symbol,
            status=execution.status.value,
            requested_price=execution.requested_price,
            executed_price=execution.executed_price,
            volume=execution.volume,
            submitted_at=execution.submitted_at,
            completed_at=execution.completed_at,
            reason=execution.reason
        )


class PortfolioMapper:
    @staticmethod
    def to_domain(account_model: AccountModel, position_models: list[PositionModel], order_models: list[OrderModel]) -> Portfolio:
        portfolio = Portfolio(
            account=AccountMapper.to_domain(account_model)
        )
        for pos_model in position_models:
            portfolio.positions[pos_model.ticket] = PositionMapper.to_domain(pos_model)
        
        for ord_model in order_models:
            portfolio.pending_orders[ord_model.ticket] = OrderMapper.to_domain(ord_model)

        return portfolio
