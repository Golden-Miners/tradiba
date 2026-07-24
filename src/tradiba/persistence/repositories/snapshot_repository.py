from sqlalchemy.orm import Session
from ..models.snapshot import SnapshotEntity

class SnapshotRepository:

    def __init__(self, session: Session):
        self.session = session

    def add(self, snapshot: SnapshotEntity):
        self.session.add(snapshot)
        self.session.commit()

    def all(self) -> list[SnapshotEntity]:
        return self.session.query(SnapshotEntity).order_by(SnapshotEntity.timestamp.asc()).all()
