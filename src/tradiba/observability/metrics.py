from prometheus_client import Counter, Gauge, Histogram, start_http_server

# Counters
ticks_received_total = Counter("ticks_received_total", "Total ticks received")
candles_completed_total = Counter("candles_completed_total", "Total candles completed")
signals_generated_total = Counter("signals_generated_total", "Total signals generated")
signals_rejected_total = Counter("signals_rejected_total", "Total signals rejected")
orders_submitted_total = Counter("orders_submitted_total", "Total orders submitted")
orders_filled_total = Counter("orders_filled_total", "Total orders filled")
orders_failed_total = Counter("orders_failed_total", "Total orders failed")
position_open_total = Counter("position_open_total", "Total positions opened")

# Histograms
strategy_latency_seconds = Histogram(
    "strategy_latency_seconds", "Latency of strategy evaluation"
)
execution_latency_seconds = Histogram(
    "execution_latency_seconds", "Latency of execution processing"
)
market_structure_latency_seconds = Histogram(
    "market_structure_latency_seconds", "Latency of market structure processing"
)

# Gauges
open_positions = Gauge("open_positions", "Number of currently open positions")
portfolio_equity = Gauge("portfolio_equity", "Current portfolio equity")
daily_drawdown = Gauge("daily_drawdown", "Current daily drawdown percentage")
active_strategies = Gauge("active_strategies", "Number of active strategies")


class MetricsServer:
    """Manages the Prometheus metrics HTTP endpoint."""
    
    _started = False
    
    @classmethod
    def start(cls, port: int = 8000) -> None:
        if not cls._started:
            start_http_server(port)
            cls._started = True
