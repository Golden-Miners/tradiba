from sqlalchemy import Column, String, Integer, DateTime, JSON
from tradiba.persistence.models.base import Base

class StoredEventModel(Base):
    __tablename__ = "events"

    event_id = Column(String, primary_key=True)
    aggregate_id = Column(String, nullable=False, index=True)
    aggregate_type = Column(String, nullable=False)
    sequence = Column(Integer, nullable=False, index=True)
    event_type = Column(String, nullable=False, index=True)
    event_version = Column(Integer, nullable=False)
    occurred_at = Column(DateTime(timezone=True), nullable=False, index=True)
    payload = Column(JSON, nullable=False)
    metadata_json = Column(JSON, nullable=True) # avoiding 'metadata' keyword clash

    # Optional: UniqueConstraint('aggregate_id', 'sequence', name='uix_aggregate_sequence')
