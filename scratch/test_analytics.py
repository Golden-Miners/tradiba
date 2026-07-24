from tradiba.persistence.database import Database
from tradiba.config.loader import load_settings
from tradiba.persistence.repositories.trade_repository import TradeRepository
from tradiba.persistence.repositories.snapshot_repository import SnapshotRepository
from tradiba.analytics.report import generate_report
import os

def test_analytics():
    settings = load_settings()
    database = Database(settings.database.url)
    session_gen = database.get_session()
    session = next(session_gen)
    
    trade_repo = TradeRepository(session)
    snapshot_repo = SnapshotRepository(session)
    
    filename = generate_report(trade_repo, snapshot_repo)
    print(f"Generated report at {filename}")
    
    assert os.path.exists(filename)
    session.close()

if __name__ == "__main__":
    test_analytics()
