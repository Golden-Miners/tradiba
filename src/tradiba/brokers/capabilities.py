from dataclasses import dataclass

@dataclass(frozen=True)
class BrokerCapabilities:
    supports_market_orders: bool
    supports_limit_orders: bool
    supports_stop_orders: bool
    supports_partial_fill: bool
    supports_hedging: bool
    supports_netting: bool
    supports_streaming_ticks: bool
