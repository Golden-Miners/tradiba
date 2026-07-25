from fastapi import Request
from tradiba.portfolio.service import PortfolioService
from tradiba.strategy.engine import StrategyEngine
from tradiba.market_structure.narrative_builder import NarrativeBuilder
from tradiba.events import EventBus


def get_event_bus(request: Request) -> EventBus:
    return request.app.state.event_bus

def get_portfolio_service(request: Request) -> PortfolioService:
    return request.app.state.portfolio_service

def get_strategy_engine(request: Request) -> StrategyEngine:
    return request.app.state.strategy_engine

def get_narrative_builder(request: Request) -> NarrativeBuilder:
    return request.app.state.narrative_builder
