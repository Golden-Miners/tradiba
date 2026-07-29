from tradiba.knowledge.brain.core import DigitalBrainCore

def test_brain():
    brain = DigitalBrainCore()
    brain.store_knowledge("k1", {"val": 1})
    res = brain.retrieve_knowledge("k1")
    assert res["val"] == 1
    assert not brain.retrieve_knowledge("k2")
