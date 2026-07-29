from tradiba.quant_ai.regimes.intelligence import MarketRegimeIntelligence

def test_regimes():
    regimes = MarketRegimeIntelligence()
    assert regimes.detect_regime({}) == "trending"
