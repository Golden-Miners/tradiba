from tradiba.core.service import Service
from tradiba.events import EventBus
from tradiba.execution.events import OrderFilledEvent
from tradiba.ports.execution import ExecutionProvider
from tradiba.logging import get_logger
from tradiba.scheduler import Scheduler, Task

from tradiba.persistence.models.trade import TradeEntity
from tradiba.persistence.models.snapshot import SnapshotEntity
from tradiba.persistence.repositories.trade_repository import TradeRepository
from tradiba.persistence.repositories.snapshot_repository import SnapshotRepository

from .events import PortfolioUpdatedEvent, PositionClosedEvent

logger = get_logger(__name__)

class PortfolioService(Service):

    def __init__(self, event_bus: EventBus, provider: ExecutionProvider, scheduler: Scheduler, database):
        self._event_bus = event_bus
        self._provider = provider
        self._scheduler = scheduler
        self._database = database
        self._session_gen = self._database.get_session()
        self._session = next(self._session_gen)
        self._trade_repo = TradeRepository(self._session)
        self._snapshot_repo = SnapshotRepository(self._session)

    def start(self) -> None:
        self._event_bus.subscribe(OrderFilledEvent, self._on_order_filled)
        self._event_bus.subscribe(PositionClosedEvent, self._on_position_closed)
        
        self._scheduler.add_task(Task(
            name="portfolio_snapshot",
            interval=60.0,
            action=self._snapshot_portfolio,
        ))
        
        self.refresh()
        logger.info("PortfolioService started.")

    def stop(self) -> None:
        self._event_bus.unsubscribe(OrderFilledEvent, self._on_order_filled)
        self._event_bus.unsubscribe(PositionClosedEvent, self._on_position_closed)
        self._scheduler.remove_task("portfolio_snapshot")
        self._session.close()
        logger.info("PortfolioService stopped.")

    def _on_order_filled(self, event: OrderFilledEvent) -> None:
        self.refresh()

    def _on_position_closed(self, event: PositionClosedEvent) -> None:
        trade = TradeEntity(
            ticket=event.ticket,
            symbol=event.symbol,
            side=event.side,
            volume=event.volume,
            entry=event.entry,
            exit=event.exit,
            profit=event.profit,
        )
        self._trade_repo.add(trade)
        logger.info(f"Persisted closed position: {event.ticket}")
        self.refresh()

    def refresh(self) -> None:
        try:
            portfolio = self._provider.account_info()
            if portfolio:
                self._event_bus.publish(PortfolioUpdatedEvent(portfolio=portfolio))
        except Exception as e:
            logger.error(f"Failed to refresh portfolio: {e}")

    def _snapshot_portfolio(self) -> None:
        try:
            portfolio = self._provider.account_info()
            if portfolio:
                snapshot = SnapshotEntity(
                    equity=portfolio.equity,
                    balance=portfolio.balance,
                    margin=portfolio.margin,
                    profit=portfolio.profit,
                    free_margin=portfolio.free_margin,
                )
                self._snapshot_repo.add(snapshot)
                logger.debug("Persisted portfolio snapshot.")
        except Exception as e:
            logger.error(f"Failed to snapshot portfolio: {e}")
