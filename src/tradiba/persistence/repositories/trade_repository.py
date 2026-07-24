from sqlalchemy.orm import Session
from ..models.trade import TradeEntity

class TradeRepository:

    def __init__(self, session: Session):
        self.session = session

    def add(self, trade: TradeEntity):
        self.session.add(trade)
        self.session.commit()

    def all(self) -> list[TradeEntity]:
        return self.session.query(TradeEntity).all()
