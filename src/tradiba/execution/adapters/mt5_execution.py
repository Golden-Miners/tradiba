from __future__ import annotations

import MetaTrader5 as mt5

from tradiba.ports.execution import ExecutionProvider
from tradiba.logging import get_logger

from ..models.result import TradeResult
from ..request_builder import RequestBuilder

logger = get_logger(__name__)


class MT5ExecutionAdapter(ExecutionProvider):

    def buy(
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

    def sell(
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
