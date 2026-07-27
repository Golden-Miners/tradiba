from typing import Dict, Any

class PortfolioReportGenerator:
    """
    Generates reports showing:
    - Current allocation
    - Risk metrics
    - Rebalance history
    - Learning parameters
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def generate_overview(
        self,
        allocations: Dict[str, float],
        attribution: Dict[str, Any],
        learned_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generates a summary report of the portfolio's current state.
        """
        return {
            "title": "Hermes Portfolio Overview",
            "environment": self.config.get("environment", "digital_twin"),
            "allocations": allocations,
            "attribution": attribution,
            "learned_parameters": learned_params
        }
