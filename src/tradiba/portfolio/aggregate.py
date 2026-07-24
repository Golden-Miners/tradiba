from dataclasses import dataclass, field
from .account import AccountSnapshot
from .position import Position
from .order import PendingOrder

@dataclass(slots=True)
class Portfolio:
    account: AccountSnapshot
    positions: dict[int, Position] = field(default_factory=dict)
    pending_orders: dict[int, PendingOrder] = field(default_factory=dict)

    def open_position(self, position: Position):
        self.positions[position.ticket] = position

    def close_position(self, ticket: int):
        from .position import PositionStatus
        if ticket in self.positions:
            self.positions[ticket].status = PositionStatus.CLOSED

    def add_order(self, order: PendingOrder):
        self.pending_orders[order.ticket] = order

    def cancel_order(self, ticket: int):
        from .order import PendingOrderStatus
        if ticket in self.pending_orders:
            self.pending_orders[ticket].status = PendingOrderStatus.CANCELLED

    def fill_order(self, ticket: int):
        from .order import PendingOrderStatus
        if ticket in self.pending_orders:
            self.pending_orders[ticket].status = PendingOrderStatus.FILLED
