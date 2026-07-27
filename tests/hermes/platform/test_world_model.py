from tradiba.hermes.platform.world.model import UnifiedWorldModel

def test_world_model():
    model = UnifiedWorldModel()
    model.sync("e1", {"status": "ok"})
    assert model.get_state("e1")["status"] == "ok"
