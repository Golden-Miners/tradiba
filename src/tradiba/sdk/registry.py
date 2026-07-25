from typing import Dict, List, Optional
import logging

from tradiba.sdk.plugin import Plugin
from tradiba.sdk.metadata import PluginManifest

logger = logging.getLogger(__name__)

class PluginRegistry:
    def __init__(self):
        # name -> (manifest, instance)
        self._plugins: Dict[str, tuple[PluginManifest, Plugin]] = {}

    def register(self, manifest: PluginManifest, instance: Plugin) -> None:
        if manifest.name in self._plugins:
            logger.warning(f"Plugin '{manifest.name}' is already registered. Overwriting.")
        self._plugins[manifest.name] = (manifest, instance)
        logger.info(f"Registered plugin '{manifest.name}' v{manifest.version}")

    def unregister(self, name: str) -> None:
        if name in self._plugins:
            del self._plugins[name]
            logger.info(f"Unregistered plugin '{name}'")

    def get(self, name: str) -> Optional[tuple[PluginManifest, Plugin]]:
        return self._plugins.get(name)

    def list(self) -> List[tuple[PluginManifest, Plugin]]:
        return list(self._plugins.values())

    def list_by_type(self, plugin_type: str) -> List[tuple[PluginManifest, Plugin]]:
        return [
            (manifest, instance) for manifest, instance in self._plugins.values()
            if manifest.type == plugin_type
        ]
