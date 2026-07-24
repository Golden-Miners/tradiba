from abc import ABC, abstractmethod
from .models import ExecutionReport

class ExecutionRepository(ABC):
    @abstractmethod
    def save(self, report: ExecutionReport):
        pass

    @abstractmethod
    def find_by_execution_key(self, key: str) -> ExecutionReport | None:
        pass
