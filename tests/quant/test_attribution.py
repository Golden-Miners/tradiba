from tradiba.quant.attribution.performance import PerformanceAttribution

def test_attribution():
    attr = PerformanceAttribution()
    res = attr.attribute("p1")
    assert res["selection_effect"] == 0.02
