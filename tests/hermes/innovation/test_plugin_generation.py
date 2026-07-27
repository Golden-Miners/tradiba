from tradiba.hermes.innovation.plugins.generator import PluginGenerator

def test_plugin_generation():
    gen = PluginGenerator()
    plugin = gen.generate_plugin("TestPlugin")
    
    assert plugin["manifest"]["name"] == "TestPlugin"
    assert plugin["manifest"]["status"] == "DRAFT"
    assert "class MyPlugin:" in plugin["code"]
