from tradiba.platform.lts.lifecycle import LTSLifecycle

def test_lts():
    lts = LTSLifecycle()
    assert lts.get_support_status()["status"] == "supported"
