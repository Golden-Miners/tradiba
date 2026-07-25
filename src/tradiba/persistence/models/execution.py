from sqlalchemy import Column, Integer, String, Numeric, DateTime, BigInteger
from tradiba.persistence.models.base import Base

class ExecutionModel(Base):
    __tablename__ = "executions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    execution_id = Column(String, nullable=False, unique=True, index=True)
    trade_plan_id = Column(String, nullable=False, index=True)
    broker_order_id = Column(BigInteger, nullable=True)
    symbol = Column(String, nullable=False)
    status = Column(String, nullable=False)
    requested_price = Column(Numeric, nullable=False)
    executed_price = Column(Numeric, nullable=True)
    volume = Column(Numeric, nullable=False)
    submitted_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    reason = Column(String, nullable=True)
