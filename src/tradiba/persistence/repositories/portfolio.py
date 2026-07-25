import uuid
from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.orm import Session

from tradiba.portfolio.aggregate import Portfolio
from tradiba.persistence.models.snapshot import PortfolioSnapshotModel
from tradiba.persistence.models.account import AccountModel
from tradiba.persistence.models.position import PositionModel
from tradiba.persistence.models.order import OrderModel
from tradiba.persistence.mappers import AccountMapper, PositionMapper, OrderMapper, PortfolioMapper


class PortfolioRepository(ABC):
    @abstractmethod
    def save(self, portfolio: Portfolio) -> None:
        ...

    @abstractmethod
    def load(self) -> Optional[Portfolio]:
        ...


class SqlAlchemyPortfolioRepository(PortfolioRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, portfolio: Portfolio) -> None:
        # Create a new snapshot
        last_snapshot = self.session.query(PortfolioSnapshotModel).order_by(PortfolioSnapshotModel.version.desc()).first()
        new_version = last_snapshot.version + 1 if last_snapshot else 1

        snapshot = PortfolioSnapshotModel(
            version=new_version,
            uuid=str(uuid.uuid4())
        )
        self.session.add(snapshot)
        self.session.flush() # to ensure snapshot is available

        account_model = AccountMapper.to_model(portfolio.account, new_version)
        self.session.add(account_model)

        for pos in portfolio.positions.values():
            pos_model = PositionMapper.to_model(pos, new_version)
            self.session.add(pos_model)

        for ord in portfolio.pending_orders.values():
            ord_model = OrderMapper.to_model(ord, new_version)
            self.session.add(ord_model)

    def load(self) -> Optional[Portfolio]:
        last_snapshot = self.session.query(PortfolioSnapshotModel).order_by(PortfolioSnapshotModel.version.desc()).first()
        if not last_snapshot:
            return None

        version = last_snapshot.version
        account_model = self.session.query(AccountModel).filter_by(snapshot_version=version).first()
        if not account_model:
            return None

        position_models = self.session.query(PositionModel).filter_by(snapshot_version=version).all()
        order_models = self.session.query(OrderModel).filter_by(snapshot_version=version).all()

        return PortfolioMapper.to_domain(account_model, list(position_models), list(order_models))
