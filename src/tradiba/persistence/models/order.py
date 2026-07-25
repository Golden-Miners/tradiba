from sqlalchemy import Column, BigInteger, String, Numeric, DateTime, Integer, ForeignKey
from tradiba.persistence.models.base import Base

class OrderModel(Base):
    __tablename__ = "orders"

    # We use a surrogate primary key to allow the same ticket across different snapshot versions
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket = Column(BigInteger, nullable=False, index=True)
    snapshot_version = Column(Integer, ForeignKey("snapshots.version"), nullable=False, index=True)

    symbol = Column(String, nullable=False)
    volume = Column(Numeric, nullable=False)
    order_type = Column(String, nullable=False)
    expiry = Column(DateTime(timezone=True), nullable=True)
    broker_state = Column(String, nullable=False)
    status = Column(String, nullable=False)
