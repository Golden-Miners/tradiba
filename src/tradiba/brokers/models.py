from dataclasses import dataclass
from enum import Enum, auto
from decimal import Decimal
from typing import Any

class AssetClass(Enum):
    FOREX = auto()
    CFD = auto()
    FUTURES = auto()
    EQUITY = auto()
    CRYPTO = auto()
    OPTION = auto()
    INDEX = auto()

@dataclass(slots=True, frozen=True)
class Instrument:
    symbol: str
    asset_class: AssetClass
    base_currency: str
    quote_currency: str
    tick_size: Decimal
    contract_size: Decimal
    lot_step: Decimal
    min_volume: Decimal
    max_volume: Decimal

@dataclass(slots=True)
class TradingAccount:
    broker_name: str
    account_id: str
    currency: str
    leverage: float
    permissions: dict[str, Any]
