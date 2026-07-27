from tradiba.hermes.enterprise.portfolio.decision import DecisionPortfolio

def test_decisions():
    portfolio = DecisionPortfolio()
    portfolio.record_decision("d1", "reason")
    assert not portfolio.decisions["d1"]["approved"]
    portfolio.approve("d1")
    assert portfolio.decisions["d1"]["approved"]
