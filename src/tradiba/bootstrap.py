from tradiba.config.loader import load_settings
from tradiba.core.application import Application
from tradiba.events import EventBus
from tradiba.scheduler import Scheduler
from tradiba.persistence.database import Database
from tradiba.ports.market_data import MarketDataProvider
from tradiba.execution.adapters.mt5_execution import MT5ExecutionAdapter
from tradiba.market.adapters.mt5_market import MT5MarketDataAdapter
from tradiba.mt5.connection import MT5ConnectionManager
from tradiba.market.service import MarketDataService
from tradiba.market.session import SessionEngine
from tradiba.market_structure.service import MarketStructureService
from tradiba.strategy.manager import StrategyManager
from tradiba.strategy.confluence import ConfluenceEngine
from tradiba.strategy.bias import MarketBiasService
from tradiba.portfolio.service import PortfolioService
from tradiba.risk.service import RiskService
from tradiba.execution.service import ExecutionService
from tradiba.execution.synchronizer import ExecutionSynchronizer
from tradiba.risk.rules.max_position_size import MaximumPositionSizeRule
from tradiba.risk.rules.max_open_trades import MaximumOpenTradesRule
from tradiba.risk.rules.max_symbol_exposure import MaximumSymbolExposureRule
from tradiba.logging import get_logger
from tradiba.cqrs import CommandDispatcher

# Ensure SMC strategy is registered at import time
import tradiba.strategy.smc  # noqa: F401

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
    mt5_execution = MT5ExecutionAdapter()
    mt5_market = MT5MarketDataAdapter()
    mt5_connection = MT5ConnectionManager(event_bus=event_bus, scheduler=scheduler)
    dispatcher = CommandDispatcher()

    container.register_singleton(EventBus, event_bus)
    container.register_singleton(Scheduler, scheduler)
    container.register_singleton(Database, database)
    container.register_singleton(MarketDataProvider, mt5_market)
    container.register_singleton(CommandDispatcher, dispatcher)
    container.register_singleton(MT5ConnectionManager, mt5_connection)

    # Core Services
    execution_sync = ExecutionSynchronizer(event_bus, mt5_execution, scheduler)
    portfolio_service = PortfolioService(
        event_bus=event_bus,
        provider=mt5_execution,
        scheduler=scheduler,
        database=database,
    )
    
    risk_service = RiskService(event_bus=event_bus)
    risk_service.add_rule(MaximumPositionSizeRule(maximum=settings.risk.get("max_position_size", 2.0)))
    risk_service.add_rule(MaximumOpenTradesRule(maximum=int(settings.risk.get("max_open_positions", 5)), provider=mt5_execution))
    risk_service.add_rule(MaximumSymbolExposureRule(maximum=int(settings.risk.get("max_symbol_positions", 2)), provider=mt5_execution))

    execution_service = ExecutionService(
        event_bus=event_bus,
        provider=mt5_execution,
    )

    market_data = MarketDataService(
        provider=mt5_market,
        event_bus=event_bus,
        scheduler=scheduler,
    )

    market_structure = MarketStructureService(event_bus=event_bus)

    # SMC Intelligence Services
    confluence_engine = ConfluenceEngine(event_bus=event_bus)
    bias_service = MarketBiasService(event_bus=event_bus)
    session_engine = SessionEngine(event_bus=event_bus)

    from tradiba.strategy.narrative import NarrativeEngine
    narrative_engine = NarrativeEngine(
        event_bus=event_bus,
        market_structure_service=market_structure,
        market_bias_service=bias_service,
        session_engine=session_engine,
        confluence_engine=confluence_engine,
    )

    strategy_manager = StrategyManager(
        event_bus=event_bus,
        strategy_configs=settings.strategies,
    )

    container.register_singleton(PortfolioService, portfolio_service)
    container.register_singleton(RiskService, risk_service)
    container.register_singleton(ExecutionService, execution_service)
    container.register_singleton(MarketDataService, market_data)
    container.register_singleton(MarketStructureService, market_structure)
    container.register_singleton(ConfluenceEngine, confluence_engine)
    container.register_singleton(MarketBiasService, bias_service)
    container.register_singleton(SessionEngine, session_engine)
    container.register_singleton(NarrativeEngine, narrative_engine)
    container.register_singleton(StrategyManager, strategy_manager)

    # Attach to Lifecycle
    app.lifecycle.add(mt5_connection)
    app.lifecycle.add(execution_sync)
    app.lifecycle.add(portfolio_service)
    app.lifecycle.add(execution_service)
    app.lifecycle.add(risk_service)
    app.lifecycle.add(market_data)
    app.lifecycle.add(market_structure)
    app.lifecycle.add(confluence_engine)
    app.lifecycle.add(bias_service)
    app.lifecycle.add(session_engine)
    app.lifecycle.add(narrative_engine)
    app.lifecycle.add(strategy_manager)
    
    app.event_bus = event_bus
    app.scheduler = scheduler
    
    from tradiba.api.service import APIService
    api_service = APIService(settings.api, container)
    app.lifecycle.add(api_service)

    logger.info("Application bootstrap complete.")
    return app
