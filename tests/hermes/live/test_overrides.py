from tradiba.hermes.live.rollback.human_override import HumanOverrideManager

def test_human_override_pause_resume():
    manager = HumanOverrideManager()
    assert not manager.is_paused()
    
    manager.pause_hermes("Market volatility")
    assert manager.is_paused()
    assert not manager.is_manual_only()
    
    manager.resume_hermes("Volatility subsided")
    assert not manager.is_paused()
    
    history = manager.get_history()
    assert len(history) == 2
    assert history[0]["action"] == "PAUSE"
    assert history[1]["action"] == "RESUME"

def test_human_override_manual_mode():
    manager = HumanOverrideManager()
    manager.force_manual_mode("Testing")
    assert manager.is_manual_only()
