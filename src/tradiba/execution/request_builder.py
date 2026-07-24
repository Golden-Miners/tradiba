import MetaTrader5 as mt5


class RequestBuilder:

    @staticmethod
    def market_buy(
        symbol: str,
        volume: float,
        price: float,
        sl: float,
        tp: float,
    ) -> dict:
        return {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "type": mt5.ORDER_TYPE_BUY,
            "volume": volume,
            "price": price,
            "sl": sl,
            "tp": tp,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

    @staticmethod
    def market_sell(
        symbol: str,
        volume: float,
        price: float,
        sl: float,
        tp: float,
    ) -> dict:
        return {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "type": mt5.ORDER_TYPE_SELL,
            "volume": volume,
            "price": price,
            "sl": sl,
            "tp": tp,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

    @staticmethod
    def buy_limit(
        symbol: str,
        volume: float,
        price: float,
        sl: float,
        tp: float,
    ) -> dict:
        return {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "type": mt5.ORDER_TYPE_BUY_LIMIT,
            "volume": volume,
            "price": price,
            "sl": sl,
            "tp": tp,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

    @staticmethod
    def sell_limit(
        symbol: str,
        volume: float,
        price: float,
        sl: float,
        tp: float,
    ) -> dict:
        return {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "type": mt5.ORDER_TYPE_SELL_LIMIT,
            "volume": volume,
            "price": price,
            "sl": sl,
            "tp": tp,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

    @staticmethod
    def buy_stop(
        symbol: str,
        volume: float,
        price: float,
        sl: float,
        tp: float,
    ) -> dict:
        return {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "type": mt5.ORDER_TYPE_BUY_STOP,
            "volume": volume,
            "price": price,
            "sl": sl,
            "tp": tp,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

    @staticmethod
    def sell_stop(
        symbol: str,
        volume: float,
        price: float,
        sl: float,
        tp: float,
    ) -> dict:
        return {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "type": mt5.ORDER_TYPE_SELL_STOP,
            "volume": volume,
            "price": price,
            "sl": sl,
            "tp": tp,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }
