from tradiba.hermes.scientist.portfolio.manager import ResearchPortfolioManager

def test_portfolio():
    manager = ResearchPortfolioManager()
    manager.add_project("p1")
    assert manager.projects["p1"]["status"] == "ACTIVE"
    manager.complete_project("p1", 9.5)
    assert manager.projects["p1"]["status"] == "COMPLETED"
    assert manager.projects["p1"]["impact"] == 9.5
