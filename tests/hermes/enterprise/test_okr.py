from tradiba.hermes.enterprise.okr.platform import OKRPlatform

def test_okr():
    platform = OKRPlatform()
    platform.add_okr("okr1", "Goal")
    platform.update_progress("okr1", 0.5)
    assert platform.okrs["okr1"]["progress"] == 0.5
