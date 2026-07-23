from __future__ import annotations

from tradiba.config import Settings, load_settings
from tradiba.events import EventBus
<<<<<<< HEAD
from tradiba.ports.market_data import MarketDataProvider
=======
from tradiba.mt5 import MT5Service
>>>>>>> 34969956ca730352cc2463af754bd6f37fec03d7
from tradiba.scheduler import Scheduler

from .container import Container
from .lifecycle import Lifecycle


class Application:
<<<<<<< HEAD
    """Root application object."""

    def __init__(
        self,
        market_provider: MarketDataProvider,
    ) -> None:
        from tradiba.market.service import MarketDataService
        from tradiba.market_structure.service import MarketStructureService
        from tradiba.strategy.manager import StrategyManager

=======
    def __init__(self) -> None:
>>>>>>> 34969956ca730352cc2463af754bd6f37fec03d7
        self.settings: Settings = load_settings()
        self.container = Container()
        self.lifecycle = Lifecycle()

        self.event_bus = EventBus()
        self.scheduler = Scheduler()
<<<<<<< HEAD
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
=======
        self.mt5 = MT5Service()
>>>>>>> 34969956ca730352cc2463af754bd6f37fec03d7

        self.container.register_singleton(Application, self)
        self.container.register_singleton(EventBus, self.event_bus)
        self.container.register_singleton(Scheduler, self.scheduler)
<<<<<<< HEAD
        self.container.register_singleton(MarketDataProvider, self.market_provider)
        self.container.register_singleton(MarketDataService, self.market_data)
        self.container.register_singleton(MarketStructureService, self.market_structure)
        self.container.register_singleton(StrategyManager, self.strategy_manager)

        # Adapters like MT5Service should manage their own lifecycle outside the core,
        # or be added by the composition root (__main__.py)
        self.lifecycle.add(self.market_data)
        self.lifecycle.add(self.market_structure)
        self.lifecycle.add(self.strategy_manager)
=======
        self.container.register_singleton(MT5Service, self.mt5)

        self.lifecycle.add(self.mt5)
>>>>>>> 34969956ca730352cc2463af754bd6f37fec03d7

    def start(self) -> None:
        self.lifecycle.start()
        self.scheduler.start()

    def stop(self) -> None:
        self.scheduler.stop()
        self.lifecycle.stop()
