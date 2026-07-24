from __future__ import annotations

import MetaTrader5 as mt5

from tradiba.ports.execution import ExecutionProvider
from tradiba.logging import get_logger

from ..models.result import TradeResult
from ..request_builder import RequestBuilder

logger = get_logger(__name__)


class MT5ExecutionAdapter(ExecutionProvider):

    def buy_market(
        self,
        *,
        symbol: str,
        volume: float,
        sl: float,
        tp: float,
    ) -> TradeResult:
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return TradeResult(success=False, ticket=None, message=f"Symbol not found: {symbol}")
        
        request = RequestBuilder.market_buy(
            symbol=symbol,
            volume=volume,
            price=tick.ask,
            sl=sl,
            tp=tp,
        )
        
        result = mt5.order_send(request)
        if result is None:
            return TradeResult(success=False, ticket=None, message="order_send returned None")
            
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return TradeResult(
                success=False, 
                ticket=None, 
                message=f"Order failed. Retcode: {result.retcode}. Comment: {result.comment}"
            )
            
        return TradeResult(success=True, ticket=result.order, message="Order executed successfully")

    def sell_market(
        self,
        *,
        symbol: str,
        volume: float,
        sl: float,
        tp: float,
    ) -> TradeResult:
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return TradeResult(success=False, ticket=None, message=f"Symbol not found: {symbol}")
            
        request = RequestBuilder.market_sell(
            symbol=symbol,
            volume=volume,
            price=tick.bid,
            sl=sl,
            tp=tp,
        )
        
        result = mt5.order_send(request)
        if result is None:
            return TradeResult(success=False, ticket=None, message="order_send returned None")
            
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return TradeResult(
                success=False, 
                ticket=None, 
                message=f"Order failed. Retcode: {result.retcode}. Comment: {result.comment}"
            )
            
        return TradeResult(success=True, ticket=result.order, message="Order executed successfully")

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
        order_builders = {
            "BUY_LIMIT": RequestBuilder.buy_limit,
            "SELL_LIMIT": RequestBuilder.sell_limit,
            "BUY_STOP": RequestBuilder.buy_stop,
            "SELL_STOP": RequestBuilder.sell_stop,
        }
        
        builder = order_builders.get(order_type)
        if not builder:
            return TradeResult(success=False, ticket=None, message=f"Unsupported pending order type: {order_type}")
            
        request = builder(
            symbol=symbol,
            volume=volume,
            price=price,
            sl=sl,
            tp=tp,
        )
        
        result = mt5.order_send(request)
        if result is None:
            return TradeResult(success=False, ticket=None, message="order_send returned None")
            
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return TradeResult(
                success=False, 
                ticket=None, 
                message=f"Pending order failed. Retcode: {result.retcode}. Comment: {result.comment}"
            )
            
        return TradeResult(success=True, ticket=result.order, message="Pending order placed successfully")

    def close_position(self, ticket: int) -> TradeResult:
        position = mt5.positions_get(ticket=ticket)
        if not position:
            return TradeResult(success=False, ticket=None, message=f"Position {ticket} not found")
        position = position[0]
        
        tick = mt5.symbol_info_tick(position.symbol)
        if not tick:
            return TradeResult(success=False, ticket=None, message=f"Symbol {position.symbol} not found")
            
        type_dict = {
            mt5.ORDER_TYPE_BUY: mt5.ORDER_TYPE_SELL,
            mt5.ORDER_TYPE_SELL: mt5.ORDER_TYPE_BUY
        }
        price_dict = {
            mt5.ORDER_TYPE_BUY: tick.bid,
            mt5.ORDER_TYPE_SELL: tick.ask
        }
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "position": ticket,
            "symbol": position.symbol,
            "volume": position.volume,
            "type": type_dict[position.type],
            "price": price_dict[position.type],
            "deviation": 20,
            "magic": 0,
            "comment": "python script close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        result = mt5.order_send(request)
        if result is None:
            return TradeResult(success=False, ticket=None, message="order_send returned None")
            
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return TradeResult(success=False, ticket=None, message=f"Close failed: {result.comment}")
            
        return TradeResult(success=True, ticket=result.order, message="Position closed")

    def modify_position(self, ticket: int, sl: float, tp: float) -> TradeResult:
        position = mt5.positions_get(ticket=ticket)
        if not position:
            return TradeResult(success=False, ticket=None, message=f"Position {ticket} not found")
        position = position[0]
        
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": ticket,
            "symbol": position.symbol,
            "sl": sl,
            "tp": tp,
            "magic": 0
        }
        
        result = mt5.order_send(request)
        if result is None:
            return TradeResult(success=False, ticket=None, message="order_send returned None")
            
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return TradeResult(success=False, ticket=None, message=f"Modify failed: {result.comment}")
            
        return TradeResult(success=True, ticket=ticket, message="Position modified")

    def cancel_order(self, ticket: int) -> TradeResult:
        request = {
            "action": mt5.TRADE_ACTION_REMOVE,
            "order": ticket,
        }
        
        result = mt5.order_send(request)
        if result is None:
            return TradeResult(success=False, ticket=None, message="order_send returned None")
            
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return TradeResult(success=False, ticket=None, message=f"Cancel failed: {result.comment}")
            
        return TradeResult(success=True, ticket=ticket, message="Order canceled")

    def account_info(self):
        from tradiba.portfolio.models import Portfolio
        info = mt5.account_info()
        if not info:
            return None
        return Portfolio(
            equity=info.equity,
            balance=info.balance,
            margin=info.margin,
            free_margin=info.margin_free,
            profit=info.profit,
            open_positions=mt5.positions_total()
        )

    def positions(self):
        from tradiba.execution.models.position import Position
        positions = mt5.positions_get()
        if not positions:
            return []
        
        return [
            Position(
                ticket=p.ticket,
                symbol=p.symbol,
                volume=p.volume,
                price_open=p.price_open,
                stop_loss=p.sl,
                take_profit=p.tp,
                profit=p.profit
            )
            for p in positions
        ]

    def orders(self):
        orders = mt5.orders_get()
        if not orders:
            return []
        
        return list(orders)
