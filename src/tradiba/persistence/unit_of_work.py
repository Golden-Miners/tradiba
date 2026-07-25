from abc import ABC, abstractmethod
from typing import Any, Type

from tradiba.persistence.database import SessionFactory


class UnitOfWork(ABC):

    @abstractmethod
    def commit(self) -> None:
        ...

    @abstractmethod
    def rollback(self) -> None:
        ...

    def __enter__(self) -> "UnitOfWork":
        return self

    def __exit__(self, exc_type: Type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any | None) -> None:
        ...


class SqlAlchemyUnitOfWork(UnitOfWork):

    def __init__(self):
        self.session = None

    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        self.session = SessionFactory()
        return self

    def commit(self) -> None:
        if self.session:
            self.session.commit()

    def rollback(self) -> None:
        if self.session:
            self.session.rollback()

    def __exit__(self, exc_type: Type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any | None) -> None:
        if self.session:
            if exc_type:
                self.rollback()
            else:
                self.commit()
            self.session.close()
            self.session = None
