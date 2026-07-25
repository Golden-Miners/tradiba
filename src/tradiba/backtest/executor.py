from __future__ import annotations

from typing import Dict

from tradiba.execution.models import TradeResult
from tradiba.ports.execution import ExecutionProvider


class PaperExecutionAdapter(ExecutionProvider):
    """
    Simulates order execution for backtesting without connecting to a broker.
    Maintains internal dictionaries for simulated positions and pending orders.
    """

    def __init__(self, initial_balance: float = 10000.0):
        self._initial_balance = initial_balance
        self._balance = initial_balance
        self._equity = initial_balance
        self._margin = 0.0

        # Simulated state
        self._positions: Dict[int, dict] = {}
        self._orders: Dict[int, dict] = {}
        
        self._ticket_counter = 1000

    def _next_ticket(self) -> int:
        self._ticket_counter += 1
        return self._ticket_counter

    def buy_market(
        self,
        *,
        symbol: str,
        volume: float,
        sl: float,
        tp: float,
    ) -> TradeResult:
        ticket = self._next_ticket()
        self._positions[ticket] = {
            "ticket": ticket,
            "symbol": symbol,
            "type": "BUY",
            "volume": volume,
            "price_open": 0.0, # Would be set by BacktestEngine on next tick
            "sl": sl,
            "tp": tp,
            "profit": 0.0
        }
        return TradeResult(success=True, ticket=ticket, message="Market BUY placed")

    def sell_market(
        self,
        *,
        symbol: str,
        volume: float,
        sl: float,
        tp: float,
    ) -> TradeResult:
        ticket = self._next_ticket()
        self._positions[ticket] = {
            "ticket": ticket,
            "symbol": symbol,
            "type": "SELL",
            "volume": volume,
            "price_open": 0.0,
            "sl": sl,
            "tp": tp,
            "profit": 0.0
        }
        return TradeResult(success=True, ticket=ticket, message="Market SELL placed")

    def place_pending_order(
        self,
        *,
        symbol: str,
        order_type: str,
        volume: float,
        price: float,
        sl: float,
        tp: float,
    ) -> TradeResult:
        ticket = self._next_ticket()
        self._orders[ticket] = {
            "ticket": ticket,
            "symbol": symbol,
            "type": order_type,
            "volume": volume,
            "price_open": price,
            "sl": sl,
            "tp": tp,
        }
        return TradeResult(success=True, ticket=ticket, message=f"Pending {order_type} placed")

    def close_position(self, ticket: int) -> TradeResult:
        if ticket in self._positions:
            pos = self._positions.pop(ticket)
            # Update balance with profit
            self._balance += pos.get("profit", 0.0)
            return TradeResult(success=True, ticket=ticket, message="Position closed")
        return TradeResult(success=False, ticket=None, message="Position not found")

    def modify_position(self, ticket: int, sl: float, tp: float) -> TradeResult:
        if ticket in self._positions:
            self._positions[ticket]["sl"] = sl
            self._positions[ticket]["tp"] = tp
            return TradeResult(success=True, ticket=ticket, message="Position modified")
        return TradeResult(success=False, ticket=None, message="Position not found")

    def cancel_order(self, ticket: int) -> TradeResult:
        if ticket in self._orders:
            self._orders.pop(ticket)
            return TradeResult(success=True, ticket=ticket, message="Order cancelled")
        return TradeResult(success=False, ticket=None, message="Order not found")

    def orders(self):
        # Format required by Tradiba: tuple of something or dict
        return tuple(self._orders.values())

    def account_info(self):
        class _AccountInfo:
            def __init__(self, bal, eq, marg):
                self.balance = bal
                self.equity = eq
                self.margin = marg
                self.profit = eq - bal
                
        return _AccountInfo(self._balance, self._equity, self._margin)

    def positions(self):
        return tuple(self._positions.values())

    # --- Backtest Simulator hooks ---

    def simulate_candle(self, high: float, low: float, close: float) -> None:
        """Called by the BacktestEngine to simulate filling orders and SL/TP."""
        
        # 1. Update floating profit for open positions
        # Simple simulation: just arbitrary calculation or let it be handled elsewhere.
        
        # 2. Check pending orders
        filled_orders = []
        for ticket, order in self._orders.items():
            if order["type"] == "BUY_LIMIT" and low <= order["price_open"]:
                filled_orders.append(ticket)
            elif order["type"] == "SELL_LIMIT" and high >= order["price_open"]:
                filled_orders.append(ticket)
            elif order["type"] == "BUY_STOP" and high >= order["price_open"]:
                filled_orders.append(ticket)
            elif order["type"] == "SELL_STOP" and low <= order["price_open"]:
                filled_orders.append(ticket)
                
        for t in filled_orders:
            o = self._orders.pop(t)
            # Create position
            self._positions[t] = {
                "ticket": t,
                "symbol": o["symbol"],
                "type": "BUY" if "BUY" in o["type"] else "SELL",
                "volume": o["volume"],
                "price_open": o["price_open"],
                "sl": o["sl"],
                "tp": o["tp"],
                "profit": 0.0
            }
            
        # 3. Check SL/TP of open positions
        closed_positions = []
        for ticket, pos in self._positions.items():
            if pos["type"] == "BUY":
                if pos["sl"] > 0 and low <= pos["sl"]:
                    pos["profit"] = -abs(pos["price_open"] - pos["sl"]) * pos["volume"] * 100000 # Dummy calculation
                    closed_positions.append(ticket)
                elif pos["tp"] > 0 and high >= pos["tp"]:
                    pos["profit"] = abs(pos["tp"] - pos["price_open"]) * pos["volume"] * 100000
                    closed_positions.append(ticket)
            elif pos["type"] == "SELL":
                if pos["sl"] > 0 and high >= pos["sl"]:
                    pos["profit"] = -abs(pos["sl"] - pos["price_open"]) * pos["volume"] * 100000
                    closed_positions.append(ticket)
                elif pos["tp"] > 0 and low <= pos["tp"]:
                    pos["profit"] = abs(pos["price_open"] - pos["tp"]) * pos["volume"] * 100000
                    closed_positions.append(ticket)
                    
        for t in closed_positions:
            self.close_position(t)
            
        # 4. Update equity
        total_floating = sum(p.get("profit", 0.0) for p in self._positions.values())
        self._equity = self._balance + total_floating
