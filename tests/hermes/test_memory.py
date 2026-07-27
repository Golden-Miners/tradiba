from tradiba.hermes.memory.working_memory import WorkingMemory

def test_working_memory():
    wm = WorkingMemory()
    wm.update("current_asset", "EURUSD")
    assert wm.retrieve("current_asset") == "EURUSD"
    wm.clear()
    assert wm.retrieve("current_asset") is None
