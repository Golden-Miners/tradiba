from tradiba.sdk_v2.indicators import SMA, EMA, RSI

def test_sma():
    sma = SMA(window=3)
    sma.update(10)
    assert sma.value() == 10.0
    sma.update(20)
    assert sma.value() == 15.0
    sma.update(30)
    assert sma.value() == 20.0
    sma.update(40) # 10 falls off, [20, 30, 40] -> 90 / 3
    assert sma.value() == 30.0

def test_ema():
    ema = EMA(window=3)
    ema.update(10)
    assert ema.value() == 10.0
    ema.update(20)
    # alpha = 2/(3+1) = 0.5
    # (20-10)*0.5 + 10 = 15.0
    assert ema.value() == 15.0

def test_rsi():
    rsi = RSI(window=2)
    # Not enough data
    assert rsi.value() == 50.0
    
    rsi.update(10)
    rsi.update(20) # gain 10
    rsi.update(30) # gain 10
    
    # 2 gains, 0 losses -> avg loss is 0, rs is inf -> rsi is 100
    assert rsi.value() == 100.0
