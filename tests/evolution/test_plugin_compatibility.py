from tradiba.evolution.plugin_compatibility import PluginCompatibility

def test_plugin_compatibility():
    compat = PluginCompatibility(platform_version="1.5.0")
    
    compat.register_compatibility("my_plugin", ["1.4.0", "1.5.0"])
    
    assert compat.is_compatible("my_plugin")
    assert not compat.is_compatible("unknown_plugin")
