from tradiba.config.loader import load_settings
from tradiba.core.application import Application
from tradiba.events import EventBus
from tradiba.scheduler import Scheduler
from tradiba.persistence.database import Database
from tradiba.ports.market_data import MarketDataProvider
from tradiba.execution.adapters.mt5_execution import MT5ExecutionAdapter
from tradiba.market.service import MarketDataService
from tradiba.market_structure.service import MarketStructureService
from tradiba.strategy.manager import StrategyManager
from tradiba.portfolio.service import PortfolioService
from tradiba.risk.service import RiskService
from tradiba.execution.service import ExecutionService
from tradiba.execution.synchronizer import ExecutionSynchronizer
from tradiba.risk.rules.max_position_size import MaximumPositionSizeRule
from tradiba.risk.rules.max_open_trades import MaximumOpenTradesRule
from tradiba.risk.rules.max_symbol_exposure import MaximumSymbolExposureRule
from tradiba.logging import get_logger
from tradiba.cqrs import CommandDispatcher

logger = get_logger("tradiba.bootstrap")

def bootstrap() -> Application:
    logger.info("Bootstrapping application...")
    settings = load_settings()
    
    app = Application(settings)
    container = app.container

    # Infrastructure
    event_bus = EventBus()
    scheduler = Scheduler()
    database = Database(settings.database.url)
    mt5_adapter = MT5ExecutionAdapter()
    dispatcher = CommandDispatcher()

    container.register_singleton(EventBus, event_bus)
    container.register_singleton(Scheduler, scheduler)
    container.register_singleton(Database, database)
    container.register_singleton(MarketDataProvider, mt5_adapter)
    container.register_singleton(CommandDispatcher, dispatcher)

    # Core Services
    execution_sync = ExecutionSynchronizer(event_bus, mt5_adapter, scheduler)
    portfolio_service = PortfolioService(
        event_bus=event_bus,
        provider=mt5_adapter,
        scheduler=scheduler,
        database=database,
    )
    
    risk_service = RiskService(event_bus=event_bus)
    risk_service.add_rule(MaximumPositionSizeRule(maximum=settings.risk.get("max_position_size", 2.0)))
    risk_service.add_rule(MaximumOpenTradesRule(maximum=int(settings.risk.get("max_open_positions", 5)), provider=mt5_adapter))
    risk_service.add_rule(MaximumSymbolExposureRule(maximum=int(settings.risk.get("max_symbol_positions", 2)), provider=mt5_adapter))

    execution_service = ExecutionService(
        event_bus=event_bus,
        provider=mt5_adapter,
    )

    market_data = MarketDataService(
        provider=mt5_adapter,
        event_bus=event_bus,
        scheduler=scheduler,
    )

    market_structure = MarketStructureService(event_bus=event_bus)

    strategy_manager = StrategyManager(
        event_bus=event_bus,
        strategy_configs=settings.strategies,
    )

    container.register_singleton(PortfolioService, portfolio_service)
    container.register_singleton(RiskService, risk_service)
    container.register_singleton(ExecutionService, execution_service)
    container.register_singleton(MarketDataService, market_data)
    container.register_singleton(MarketStructureService, market_structure)
    container.register_singleton(StrategyManager, strategy_manager)

    # Attach to Lifecycle
    app.lifecycle.add(execution_sync)
    app.lifecycle.add(portfolio_service)
    app.lifecycle.add(execution_service)
    app.lifecycle.add(risk_service)
    app.lifecycle.add(market_data)
    app.lifecycle.add(market_structure)
    app.lifecycle.add(strategy_manager)
    
    app.event_bus = event_bus
    app.scheduler = scheduler
    
    logger.info("Application bootstrap complete.")
    return app
