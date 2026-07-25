from abc import ABC, abstractmethod
from typing import Optional, List
from sqlalchemy.orm import Session

from tradiba.execution.models import ExecutionReport
from tradiba.persistence.models.execution import ExecutionModel
from tradiba.persistence.mappers import ExecutionMapper


class ExecutionRepository(ABC):
    @abstractmethod
    def save(self, execution: ExecutionReport) -> None:
        ...

    @abstractmethod
    def get(self, execution_id: str) -> Optional[ExecutionReport]:
        ...
        
    @abstractmethod
    def get_all(self) -> List[ExecutionReport]:
        ...


class SqlAlchemyExecutionRepository(ExecutionRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, execution: ExecutionReport) -> None:
        model = ExecutionMapper.to_model(execution)
        # Assuming we just append or overwrite
        existing = self.session.query(ExecutionModel).filter_by(execution_id=execution.execution_id).first()
        if existing:
            # Update fields
            for key, value in model.__dict__.items():
                if not key.startswith('_'):
                    setattr(existing, key, value)
        else:
            self.session.add(model)

    def get(self, execution_id: str) -> Optional[ExecutionReport]:
        model = self.session.query(ExecutionModel).filter_by(execution_id=execution_id).first()
        if model:
            return ExecutionMapper.to_domain(model)
        return None
        
    def get_all(self) -> List[ExecutionReport]:
        models = self.session.query(ExecutionModel).all()
        return [ExecutionMapper.to_domain(m) for m in models]
