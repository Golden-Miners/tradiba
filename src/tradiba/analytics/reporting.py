from dataclasses import dataclass
from typing import Any
import json

@dataclass(slots=True)
class PortfolioAnalyticsReport:
    """
    Immutable representation of portfolio risk state intended for
    export, dashboards, and enterprise reporting.
    """
    exposures: dict[str, dict[str, float]]
    correlations: dict[str, dict[str, float]]
    var: dict[str, Any]
    expected_shortfall: dict[str, Any]
    stress_results: dict[str, Any]
    recommendations: dict[str, float]

    def to_json(self) -> str:
        """Serializes the report to JSON format."""
        return json.dumps({
            "exposures": self.exposures,
            "correlations": self.correlations,
            "var": self.var,
            "expected_shortfall": self.expected_shortfall,
            "stress_results": self.stress_results,
            "recommendations": self.recommendations
        }, indent=2)
