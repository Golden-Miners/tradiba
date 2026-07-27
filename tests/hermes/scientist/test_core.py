from tradiba.hermes.scientist.core.coordinator import AIScientistCore

def test_core():
    core = AIScientistCore()
    core.start_investigation("inv_1")
    assert "inv_1" in core.get_investigations()
