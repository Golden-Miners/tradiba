from sqlalchemy import Column, BigInteger, String, Numeric, DateTime, Integer, ForeignKey
from tradiba.persistence.models.base import Base

class PositionModel(Base):
    __tablename__ = "positions"

    # We use a surrogate primary key to allow the same ticket across different snapshot versions
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket = Column(BigInteger, nullable=False, index=True)
    snapshot_version = Column(Integer, ForeignKey("snapshots.version"), nullable=False, index=True)

    symbol = Column(String, nullable=False)
    volume = Column(Numeric, nullable=False)
    entry_price = Column(Numeric, nullable=False)
    current_price = Column(Numeric, nullable=False)
    stop_loss = Column(Numeric, nullable=False)
    take_profit = Column(Numeric, nullable=False)
    open_time = Column(DateTime(timezone=True), nullable=False)
    profit = Column(Numeric, nullable=False)
    status = Column(String, nullable=False)
