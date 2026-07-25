from typing import Any
from tradiba.research.features import Feature

class FeaturePipeline:
    """
    Executes a sequence of features deterministically.
    """
    def __init__(self, features: list[Feature]):
        self.features = features

    def process(self, data: Any) -> dict[str, Any]:
        """
        Processes data through all features.
        Returns a dictionary of feature names to computed values.
        """
        results = {}
        for feature in self.features:
            results[feature.name] = feature.compute(data)
        return results
