import pytest
from datetime import datetime
from decimal import Decimal

from tradiba.persistence.unit_of_work import SqlAlchemyUnitOfWork
from tradiba.persistence.repositories.portfolio import SqlAlchemyPortfolioRepository
from tradiba.persistence.models import Base
from tradiba.portfolio.aggregate import Portfolio
from tradiba.portfolio.account import AccountSnapshot
from tradiba.portfolio.position import Position, PositionStatus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

test_engine = create_engine("sqlite:///:memory:", future=True)
TestSessionFactory = sessionmaker(bind=test_engine, expire_on_commit=False)

class MockSqlAlchemyUnitOfWork(SqlAlchemyUnitOfWork):
    def __enter__(self):
        self.session = TestSessionFactory()
        return self

@pytest.fixture(scope="module")
def setup_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

def test_save_and_load_portfolio(setup_db):
    # Setup test portfolio
    account = AccountSnapshot(
        timestamp=datetime.utcnow(),
        balance=Decimal("10000.00"),
        equity=Decimal("10000.00"),
        margin=Decimal("0.00"),
        free_margin=Decimal("10000.00"),
        margin_level=Decimal("0.00"),
        floating_profit=Decimal("0.00"),
        realized_profit=Decimal("0.00")
    )
    portfolio = Portfolio(account=account)
    
    pos = Position(
        ticket=12345,
        symbol="EURUSD",
        volume=Decimal("1.0"),
        entry_price=Decimal("1.1000"),
        current_price=Decimal("1.1050"),
        stop_loss=Decimal("1.0900"),
        take_profit=Decimal("1.1200"),
        open_time=datetime.utcnow(),
        profit=Decimal("50.00"),
        status=PositionStatus.OPEN
    )
    portfolio.open_position(pos)

    # Use UoW to save
    with MockSqlAlchemyUnitOfWork() as uow:
        repo = SqlAlchemyPortfolioRepository(uow.session)
        repo.save(portfolio)

    # New UoW to load
    with MockSqlAlchemyUnitOfWork() as uow:
        repo = SqlAlchemyPortfolioRepository(uow.session)
        loaded = repo.load()
        
        assert loaded is not None
        assert loaded.account.balance == Decimal("10000.00")
        assert len(loaded.positions) == 1
        assert 12345 in loaded.positions
        assert loaded.positions[12345].symbol == "EURUSD"

def test_transaction_rollback(setup_db):
    try:
        with MockSqlAlchemyUnitOfWork() as uow:
            repo = SqlAlchemyPortfolioRepository(uow.session)
            
            account = AccountSnapshot(
                timestamp=datetime.utcnow(),
                balance=Decimal("5000.00"),
                equity=Decimal("5000.00"),
                margin=Decimal("0.00"),
                free_margin=Decimal("5000.00"),
                margin_level=Decimal("0.00"),
                floating_profit=Decimal("0.00"),
                realized_profit=Decimal("0.00")
            )
            portfolio = Portfolio(account=account)
            repo.save(portfolio)
            
            # Intentionally raise an exception to trigger rollback
            raise ValueError("Intentional rollback")
    except ValueError:
        pass

    with MockSqlAlchemyUnitOfWork() as uow:
        repo = SqlAlchemyPortfolioRepository(uow.session)
        loaded = repo.load()
        # Since it rolled back, it should not have the 5000 balance account
        # It should still be the 10000 balance account from the previous test
        assert loaded is not None
        assert loaded.account.balance == Decimal("10000.00")
