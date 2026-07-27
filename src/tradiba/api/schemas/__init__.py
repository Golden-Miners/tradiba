from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str


class PositionResponse(BaseModel):
    symbol: str
    ticket: int
    volume: float
    price_open: float
    current_price: float
    profit: Decimal
    type: str


class PortfolioResponse(BaseModel):
    equity: Decimal
    balance: Decimal
    free_margin: Decimal
    positions_count: int


class StrategyResponse(BaseModel):
    name: str
    enabled: bool
    description: str


class BacktestJobResponse(BaseModel):
    id: str
    status: str
    strategy: str
    symbol: str
    progress: float
    result: Optional[dict] = None


class BacktestRequest(BaseModel):
    strategy: str
    symbol: str
    timeframe: str
    start_date: datetime
    end_date: datetime


class NarrativeResponse(BaseModel):
    symbol: str
    trend: str
    bias: str
    active_order_blocks: int
    active_fvgs: int
