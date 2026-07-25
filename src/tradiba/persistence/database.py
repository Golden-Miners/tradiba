from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tradiba.config import load_settings

settings = load_settings()

# Fallback to SQLite if URL is not provided
db_url = getattr(settings.database, "url", None)
if not db_url:
    db_url = "sqlite:///tradiba.db"

engine = create_engine(
    db_url,
    future=True,
    pool_pre_ping=True,
    pool_recycle=3600,
)

SessionFactory = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

class DatabaseHealth:
    def ping(self) -> bool:
        from sqlalchemy import text
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
