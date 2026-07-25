import logging
from tradiba.sdk.plugin import PluginContext
from tradiba.sdk.registry import PluginRegistry

logger = logging.getLogger(__name__)

class PluginLifecycleManager:
    def __init__(self, registry: PluginRegistry, context: PluginContext):
        self.registry = registry
        self.context = context

    def initialize_all(self) -> None:
        for manifest, instance in self.registry.list():
            try:
                logger.info(f"Initializing plugin '{manifest.name}'...")
                instance.initialize(self.context)
            except Exception as e:
                logger.error(f"Failed to initialize plugin '{manifest.name}': {e}", exc_info=True)

    def start_all(self) -> None:
        for manifest, instance in self.registry.list():
            try:
                logger.info(f"Starting plugin '{manifest.name}'...")
                instance.start()
            except Exception as e:
                logger.error(f"Failed to start plugin '{manifest.name}': {e}", exc_info=True)

    def stop_all(self) -> None:
        for manifest, instance in reversed(self.registry.list()):
            try:
                logger.info(f"Stopping plugin '{manifest.name}'...")
                instance.stop()
            except Exception as e:
                logger.error(f"Failed to stop plugin '{manifest.name}': {e}", exc_info=True)

    def dispose_all(self) -> None:
        for manifest, instance in reversed(self.registry.list()):
            try:
                logger.info(f"Disposing plugin '{manifest.name}'...")
                instance.dispose()
            except Exception as e:
                logger.error(f"Failed to dispose plugin '{manifest.name}': {e}", exc_info=True)
