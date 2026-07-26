from dataclasses import dataclass
from typing import List, Optional

@dataclass
class DiscoveredFeature:
    name: str
    source: str
    description: str
    version: str

class FeatureStore:
    """Framework for discovering and registering new predictive features."""
    def __init__(self):
        self._features: List[DiscoveredFeature] = []

    def register(self, feature: DiscoveredFeature):
        self._features.append(feature)

    def get_features(self) -> List[DiscoveredFeature]:
        return self._features
