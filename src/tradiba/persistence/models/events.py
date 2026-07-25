from sqlalchemy import Column, Integer, String, DateTime, JSON
from tradiba.persistence.models.base import Base

class MarketEventModel(Base):
    __tablename__ = "market_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String, nullable=False, index=True) # e.g. CandleClosedEvent, TickEvent
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    symbol = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
