from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from tradiba.persistence.models.base import Base

class PortfolioSnapshotModel(Base):
    __tablename__ = "snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(Integer, nullable=False, unique=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    uuid = Column(String, unique=True, nullable=False)
