import pytest

from tradiba.sdk.metadata import PluginManifest
from tradiba.sdk.registry import PluginRegistry
from tradiba.sdk.validator import PluginValidator
from tradiba.sdk.exceptions import IncompatibleApiVersionError, PluginValidationError
from tradiba.sdk.plugin import Plugin

class DummyPlugin(Plugin):
    def initialize(self, context): pass
    def start(self): pass
    def stop(self): pass
    def dispose(self): pass

def test_manifest_validation():
    validator = PluginValidator(platform_api_version="1.0")
    
    # Valid
    manifest = PluginManifest(
        name="test", version="1.0.0", author="auth", 
        api_version="1.0", type="strategy", entrypoint="mod:cls"
    )
    validator.validate_manifest(manifest)
    
    # Invalid API version
    manifest_invalid = PluginManifest(
        name="test", version="1.0.0", author="auth", 
        api_version="2.0", type="strategy", entrypoint="mod:cls"
    )
    with pytest.raises(IncompatibleApiVersionError):
        validator.validate_manifest(manifest_invalid)

def test_instance_validation():
    validator = PluginValidator(platform_api_version="1.0")
    
    # Valid
    validator.validate_instance(DummyPlugin())
    
    # Invalid
    with pytest.raises(PluginValidationError):
        validator.validate_instance(object())

def test_plugin_registry():
    registry = PluginRegistry()
    manifest = PluginManifest(
        name="dummy", version="1.0.0", author="auth", 
        api_version="1.0", type="strategy", entrypoint="mod:cls"
    )
    plugin = DummyPlugin()
    
    registry.register(manifest, plugin)
    assert len(registry.list()) == 1
    
    assert registry.get("dummy")[1] == plugin
    assert len(registry.list_by_type("strategy")) == 1
    assert len(registry.list_by_type("indicator")) == 0
    
    registry.unregister("dummy")
    assert len(registry.list()) == 0
