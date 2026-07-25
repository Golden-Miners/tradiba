from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
from tradiba.persistence.models.base import Base

class AccountModel(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    snapshot_version = Column(Integer, ForeignKey("snapshots.version"), nullable=False, index=True)

    timestamp = Column(DateTime(timezone=True), nullable=False)
    balance = Column(Numeric, nullable=False)
    equity = Column(Numeric, nullable=False)
    margin = Column(Numeric, nullable=False)
    free_margin = Column(Numeric, nullable=False)
    margin_level = Column(Numeric, nullable=False)
    floating_profit = Column(Numeric, nullable=False)
    realized_profit = Column(Numeric, nullable=False)
