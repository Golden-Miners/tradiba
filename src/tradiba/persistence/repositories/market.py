from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

from tradiba.persistence.models.market import CandleModel, TickModel

# Since we don't have Domain objects explicitly passed for candles/ticks in context,
# we will just save/load raw models or dictionaries for now.
class MarketRepository(ABC):
    @abstractmethod
    def save_candle(self, symbol: str, timeframe: str, data: dict) -> None:
        ...

    @abstractmethod
    def save_tick(self, symbol: str, data: dict) -> None:
        ...

class SqlAlchemyMarketRepository(MarketRepository):
    def __init__(self, session: Session):
        self.session = session

    def save_candle(self, symbol: str, timeframe: str, data: dict) -> None:
        candle = CandleModel(
            symbol=symbol,
            timeframe=timeframe,
            timestamp=data["timestamp"],
            open=data["open"],
            high=data["high"],
            low=data["low"],
            close=data["close"],
            tick_volume=data["tick_volume"],
            real_volume=data["real_volume"],
            spread=data["spread"]
        )
        self.session.add(candle)

    def save_tick(self, symbol: str, data: dict) -> None:
        tick = TickModel(
            symbol=symbol,
            timestamp=data["timestamp"],
            bid=data["bid"],
            ask=data["ask"],
            last=data["last"],
            volume=data["volume"]
        )
        self.session.add(tick)
