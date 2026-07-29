from tradiba.quant_ai.bayesian.analytics import BayesianPortfolioAnalytics

def test_bayesian():
    analytics = BayesianPortfolioAnalytics()
    res = analytics.decompose_risk("p1")
    assert res["market_risk"] == 0.6
