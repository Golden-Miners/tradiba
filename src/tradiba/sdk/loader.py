import os
import yaml
import importlib
import logging

from tradiba.sdk.metadata import PluginManifest
from tradiba.sdk.registry import PluginRegistry
from tradiba.sdk.validator import PluginValidator
from tradiba.sdk.exceptions import PluginLoadError

logger = logging.getLogger(__name__)

class PluginLoader:
    def __init__(self, registry: PluginRegistry, validator: PluginValidator, plugin_dir: str = "plugins"):
        self.registry = registry
        self.validator = validator
        self.plugin_dir = plugin_dir

    def load_all(self) -> None:
        if not os.path.exists(self.plugin_dir):
            logger.info(f"Plugin directory '{self.plugin_dir}' does not exist. Skipping.")
            return

        for entry in os.listdir(self.plugin_dir):
            plugin_path = os.path.join(self.plugin_dir, entry)
            if os.path.isdir(plugin_path):
                manifest_path = os.path.join(plugin_path, "plugin.yaml")
                if os.path.isfile(manifest_path):
                    self.load_plugin(plugin_path)

    def load_plugin(self, plugin_path: str) -> None:
        manifest_path = os.path.join(plugin_path, "plugin.yaml")
        try:
            with open(manifest_path, 'r') as f:
                data = yaml.safe_load(f)
            
            manifest = PluginManifest(**data)
            self.validator.validate_manifest(manifest)
            
            # entrypoint e.g., "my_plugin:MyPluginClass"
            module_name, class_name = manifest.entrypoint.split(':')
            
            # We need to temporarily add the plugin_dir to sys.path so it can be imported,
            # or use importlib.util.spec_from_file_location if we want to import directly.
            # Using simple import mechanism assuming packages are pip installed or in PYTHONPATH
            # For local plugins directory, let's load it dynamically.
            import sys
            parent_dir = os.path.dirname(plugin_path)
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)
                
            plugin_module = importlib.import_module(f"{os.path.basename(plugin_path)}.{module_name}")
            plugin_class = getattr(plugin_module, class_name)
            
            instance = plugin_class()
            self.validator.validate_instance(instance)
            
            self.registry.register(manifest, instance)
        except Exception as e:
            logger.error(f"Failed to load plugin from {plugin_path}: {e}")
            raise PluginLoadError(f"Failed to load plugin: {e}") from e
