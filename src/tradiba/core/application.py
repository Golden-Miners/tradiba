from __future__ import annotations

from tradiba.config import Settings, load_settings
from tradiba.events import EventBus
from tradiba.ports.market_data import MarketDataProvider
from tradiba.scheduler import Scheduler

from .container import Container
from .lifecycle import Lifecycle


class Application:
    """Root application object."""

    def __init__(
        self,
        market_provider: MarketDataProvider,
    ) -> None:
        from tradiba.market.service import MarketDataService
        from tradiba.market_structure.service import MarketStructureService
        from tradiba.strategy.manager import StrategyManager

        self.settings: Settings = load_settings()
        self.container = Container()
        self.lifecycle = Lifecycle()

        self.event_bus = EventBus()
        self.scheduler = Scheduler()
        self.market_provider = market_provider
        self.market_data = MarketDataService(
            provider=self.market_provider,
            event_bus=self.event_bus,
            scheduler=self.scheduler,
        )
        self.market_structure = MarketStructureService(
            event_bus=self.event_bus,
        )
        self.strategy_manager = StrategyManager(
            event_bus=self.event_bus,
            strategy_configs=self.settings.strategies,
        )

        self.container.register_singleton(Application, self)
        self.container.register_singleton(EventBus, self.event_bus)
        self.container.register_singleton(Scheduler, self.scheduler)
        self.container.register_singleton(MarketDataProvider, self.market_provider)
        self.container.register_singleton(MarketDataService, self.market_data)
        self.container.register_singleton(MarketStructureService, self.market_structure)
        self.container.register_singleton(StrategyManager, self.strategy_manager)

        # Adapters like MT5Service should manage their own lifecycle outside the core,
        # or be added by the composition root (__main__.py)
        self.lifecycle.add(self.market_data)
        self.lifecycle.add(self.market_structure)
        self.lifecycle.add(self.strategy_manager)

    def start(self) -> None:
        self.lifecycle.start()
        self.scheduler.start()

    def stop(self) -> None:
        self.scheduler.stop()
        self.lifecycle.stop()