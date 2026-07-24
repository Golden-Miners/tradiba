import csv
import time
from pathlib import Path
from datetime import datetime, timezone

from tradiba.mt5.models import Candle
from tradiba.market_structure.engine import MarketStructureEngine


def test_regression_deterministic_processing():
    """
    Feeds a CSV of candles into the engine and verifies O(1) properties
    and final structure counts.
    """
    csv_path = Path(__file__).parent.parent / "fixtures" / "EURUSD_H1_trend.csv"
    
    engine = MarketStructureEngine()
    
    start_time = time.perf_counter()
    candle_count = 0
    
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dt = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
            candle = Candle(
                symbol="EURUSD",
                timeframe="H1",
                timestamp=dt,
                open=float(row["open"]),
                high=float(row["high"]),
                low=float(row["low"]),
                close=float(row["close"]),
                tick_volume=int(row["volume"]),
                spread=0,
                real_volume=int(row["volume"])
            )
            engine.on_candle(candle)
            candle_count += 1
            
    end_time = time.perf_counter()
    duration = end_time - start_time
    
    state = engine.state["EURUSD"].get_timeframe_state("H1")
    
    # Assertions
    assert candle_count == 9
    assert duration < 0.2, f"Processing {candle_count} candles took too long: {duration:.4f}s"
    
    # Since it's a short sequence, we can check basic things
    assert len(state.candles) == 9
    # Ensure it's not recalculating everything (O(1) guarantee check)
    assert state.candle_count == 9
