from dataclasses import dataclass, field
from typing import Any

@dataclass
class ConfigurationNode:
    """Represents a hierarchical configuration block."""
    settings: dict[str, Any] = field(default_factory=dict)

@dataclass
class HierarchicalConfig:
    """
    Configuration resolution hierarchy: Node > Cluster > Environment > Global
    """
    global_cfg: ConfigurationNode = field(default_factory=ConfigurationNode)
    environment_cfg: ConfigurationNode = field(default_factory=ConfigurationNode)
    cluster_cfg: ConfigurationNode = field(default_factory=ConfigurationNode)
    node_cfg: ConfigurationNode = field(default_factory=ConfigurationNode)

    def resolve(self, key: str, default: Any = None) -> Any:
        # Check from most specific to least specific
        if key in self.node_cfg.settings:
            return self.node_cfg.settings[key]
        if key in self.cluster_cfg.settings:
            return self.cluster_cfg.settings[key]
        if key in self.environment_cfg.settings:
            return self.environment_cfg.settings[key]
        if key in self.global_cfg.settings:
            return self.global_cfg.settings[key]
        return default
