from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

class Database:
    def __init__(self, url: str):
        self.engine = create_engine(url, future=True)
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
        )

    def get_session(self) -> Generator:
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()
