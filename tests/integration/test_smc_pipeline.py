from datetime import datetime, timezone

from tradiba.events import EventBus
from tradiba.market_structure.models import Trend
from tradiba.mt5.models import Candle

from tradiba.market_structure.engine import MarketStructureEngine
from tradiba.strategy.confluence import ConfluenceEngine
from tradiba.strategy.bias import MarketBiasService, MarketBias
from tradiba.strategy.pipeline import SignalBuilder, StrategyPipeline, ConfluenceFilter, BiasFilter, PipelineContext
from tradiba.strategy.models import Direction

def make_candle(h, l, c, o, t, tf="H1"):
    return Candle(
        symbol="EURUSD",
        timeframe=tf,
        timestamp=datetime.fromtimestamp(t, tz=timezone.utc),
        open=o,
        high=h,
        low=l,
        close=c,
        tick_volume=100,
        real_volume=0,
        spread=1
    )

def test_smc_pipeline():
    bus = EventBus()
    
    # 1. Start Services
    bias_service = MarketBiasService(bus)
    bias_service.start()
    
    confluence_engine = ConfluenceEngine(bus)
    confluence_engine.start()
    
    # We'll just run candles through the engine directly for this test
    ms_engine = MarketStructureEngine()
    
    # 2. Track outputs
    computed_biases = []
    computed_confluences = []
    
    from tradiba.strategy.bias import BiasComputedEvent
    from tradiba.strategy.confluence import ConfluenceComputedEvent
    
    bus.subscribe(BiasComputedEvent, lambda e: computed_biases.append(e))
    bus.subscribe(ConfluenceComputedEvent, lambda e: computed_confluences.append(e))
    
    # 3. Simulate Price Action (Bullish setup)
    t = 1600000000
    
    # Create an H4 Bullish trend (just a quick swing and break)
    candles_h4 = [
        make_candle(1.0010, 1.0000, 1.0005, 1.0000, t + 3600*4*1, "H4"),
        make_candle(1.0020, 1.0005, 1.0010, 1.0005, t + 3600*4*2, "H4"),
        make_candle(1.0030, 1.0010, 1.0015, 1.0010, t + 3600*4*3, "H4"), # Swing High
        make_candle(1.0020, 1.0000, 1.0005, 1.0015, t + 3600*4*4, "H4"),
        make_candle(1.0010, 0.9990, 0.9995, 1.0005, t + 3600*4*5, "H4"),
        make_candle(1.0050, 0.9995, 1.0040, 0.9995, t + 3600*4*6, "H4"), # Break Swing High -> BULLISH
    ]
    for c in candles_h4:
        events = ms_engine.on_candle(c)
        for e in events: bus.publish(e)
        
    assert len(computed_biases) > 0
    # Bias is NEUTRAL because only H4 is BULLISH (1), H1 is NEUTRAL, M15 is NEUTRAL
    assert computed_biases[-1].bias == MarketBias.NEUTRAL
    
    # Now simulate H1
    # We just need to trigger a CHOCH or BOS to get confluence
    candles_h1 = [
        make_candle(1.0010, 1.0000, 1.0005, 1.0000, t + 3600*1, "H1"),
        make_candle(1.0020, 1.0005, 1.0010, 1.0005, t + 3600*2, "H1"),
        make_candle(1.0030, 1.0010, 1.0015, 1.0010, t + 3600*3, "H1"), # Swing High
        make_candle(1.0020, 1.0000, 1.0005, 1.0015, t + 3600*4, "H1"),
        make_candle(1.0010, 0.9990, 0.9995, 1.0005, t + 3600*5, "H1"),
        make_candle(1.0050, 0.9995, 1.0040, 0.9995, t + 3600*6, "H1"), # Break Swing High -> BULLISH (TrendChanged)
        
        # Now we form another swing and break it for a BOS
        make_candle(1.0060, 1.0030, 1.0040, 1.0040, t + 3600*7, "H1"),
        make_candle(1.0070, 1.0040, 1.0050, 1.0040, t + 3600*8, "H1"), # Swing High
        make_candle(1.0060, 1.0030, 1.0040, 1.0050, t + 3600*9, "H1"),
        make_candle(1.0050, 1.0020, 1.0030, 1.0040, t + 3600*10, "H1"),
        make_candle(1.0090, 1.0020, 1.0080, 1.0030, t + 3600*11, "H1"), # Break Swing High -> BOS!
    ]
    for c in candles_h1:
        events = ms_engine.on_candle(c)
        for e in events: bus.publish(e)
        
    # Now H4 and H1 are BULLISH, so Bias is BULLISH
    assert computed_biases[-1].bias == MarketBias.BULLISH
    
    # Check confluence
    assert len(computed_confluences) > 0
    assert computed_confluences[-1].confluence.score > 0
    assert computed_confluences[-1].confluence.direction == Trend.BULLISH
    
    # 4. Strategy Pipeline Execution
    # Build a pipeline
    filters = [
        ConfluenceFilter(min_score=10),
        BiasFilter(allowed_biases=[MarketBias.STRONG_BULLISH, MarketBias.BULLISH]),
        # Skipping session filter for brevity in mock data
    ]
    builder = SignalBuilder(atr_multiplier_sl=1.5, atr_multiplier_tp=3.0)
    pipeline = StrategyPipeline(bus, filters, builder)
    
    ctx = PipelineContext(
        symbol="EURUSD",
        timeframe="H1",
        confluence=computed_confluences[-1].confluence,
        bias=computed_biases[-1].bias,
        atr=0.005, # 50 pips
    )
    
    signal = pipeline.execute_pipeline(ctx, entry_price=1.0050, strategy_id="test_strat")
    
    assert signal is not None
    assert signal.direction == Direction.LONG
    assert signal.entry == 1.0050
    assert signal.stop_loss == 1.0050 - (0.005 * 1.5)
    assert signal.take_profit == 1.0050 + (0.005 * 3.0)
