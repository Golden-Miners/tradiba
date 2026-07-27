from tradiba.ai.models.platform import ModelPlatform

def test_models():
    plat = ModelPlatform()
    plat.register_model("gpt-4", "openai", 0.03)
    assert plat.get_model("gpt-4")["provider"] == "openai"
    plat.record_usage("gpt-4", 1000)
    assert plat.get_model("gpt-4")["usage"] == 1000
