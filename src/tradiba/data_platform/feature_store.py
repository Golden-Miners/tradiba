from dataclasses import dataclass
from typing import Any

@dataclass
class Feature:
    name: str
    version: str
    description: str
    data: list[dict[str, Any]]

class FeatureStore:
    """Central repository for reusable research and AI features."""
    def __init__(self) -> None:
        # Maps feature name to a list of versions (Feature objects)
        self._features: dict[str, list[Feature]] = {}

    def register(self, feature: Feature) -> None:
        if feature.name not in self._features:
            self._features[feature.name] = []
        self._features[feature.name].append(feature)

    def retrieve(self, name: str, version: str | None = None) -> Feature | None:
        if name not in self._features:
            return None
        versions = self._features[name]
        if not versions:
            return None
        if version:
            for feat in versions:
                if feat.version == version:
                    return feat
            return None
        # Return latest
        return sorted(versions, key=lambda f: f.version)[-1]
        
    def list_versions(self, name: str) -> list[str]:
        if name not in self._features:
            return []
        return [f.version for f in self._features[name]]
