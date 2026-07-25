from sqlalchemy import Column, Integer, String, Numeric, DateTime
from tradiba.persistence.models.base import Base

class CandleModel(Base):
    __tablename__ = "candles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String, nullable=False, index=True)
    timeframe = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    
    open = Column(Numeric, nullable=False)
    high = Column(Numeric, nullable=False)
    low = Column(Numeric, nullable=False)
    close = Column(Numeric, nullable=False)
    tick_volume = Column(Integer, nullable=False)
    real_volume = Column(Integer, nullable=False)
    spread = Column(Integer, nullable=False)

class TickModel(Base):
    __tablename__ = "ticks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    
    bid = Column(Numeric, nullable=False)
    ask = Column(Numeric, nullable=False)
    last = Column(Numeric, nullable=False)
    volume = Column(Numeric, nullable=False)
