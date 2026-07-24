from tradiba.persistence.database import Database
from tradiba.config.loader import load_settings
from tradiba.persistence.base import Base
from tradiba.persistence.models.trade import TradeEntity
from tradiba.persistence.repositories.trade_repository import TradeRepository

def test_persistence():
    settings = load_settings()
    database = Database(settings.database.url)
    
    # Ensure tables exist
    Base.metadata.create_all(bind=database.engine)
    
    session_gen = database.get_session()
    session = next(session_gen)
    repo = TradeRepository(session)
    
    trade = TradeEntity(
        ticket=123456,
        symbol="EURUSD",
        side="BUY",
        volume=0.1,
        entry=1.1000,
        exit=1.1050,
        profit=50.0
    )
    repo.add(trade)
    
    trades = repo.all()
    print("Persisted Trades:")
    for t in trades:
        print(f"Ticket: {t.ticket}, Profit: {t.profit}")
        
    session.close()

if __name__ == "__main__":
    test_persistence()
