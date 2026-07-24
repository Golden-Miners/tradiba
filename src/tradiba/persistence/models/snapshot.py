from sqlalchemy import Float, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from ..base import Base

class SnapshotEntity(Base):
    __tablename__ = "snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    equity: Mapped[float] = mapped_column(Float)
    balance: Mapped[float] = mapped_column(Float)
    margin: Mapped[float] = mapped_column(Float)
    profit: Mapped[float] = mapped_column(Float)
    free_margin: Mapped[float] = mapped_column(Float)
