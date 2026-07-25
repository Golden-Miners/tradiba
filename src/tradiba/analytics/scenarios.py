from tradiba.analytics.portfolio import PortfolioSnapshot
from tradiba.analytics.stress import StressScenario

class ScenarioAnalysis:
    """
    Evaluates hypothetical portfolio states based on provided scenarios.
    """
    def __init__(self, scenarios: list[StressScenario]):
        self.scenarios = scenarios

    def evaluate(self, snapshot: PortfolioSnapshot) -> dict[str, PortfolioSnapshot]:
        """
        Applies each scenario and returns the shocked snapshots.
        """
        results = {}
        for scenario in self.scenarios:
            results[scenario.name] = scenario.apply(snapshot)
        return results
