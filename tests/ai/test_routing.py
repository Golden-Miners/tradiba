from tradiba.ai.routing.router import MultiModelRouter

def test_routing():
    router = MultiModelRouter()
    assert router.route("HIGH", 0.1) == "model-heavy"
    assert router.route("MEDIUM", 0.1) == "model-balanced"
    assert router.route("LOW", 0.1) == "model-fast"
