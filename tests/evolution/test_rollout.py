from tradiba.evolution.rollout import RollingUpgradeManager

def test_rollout_manager():
    manager = RollingUpgradeManager()
    
    manager.start_canary("web_ui", "v2")
    assert manager.get_deployment_status("web_ui") == "v2_canary"
    
    manager.promote_to_production("web_ui", "v2")
    assert manager.get_deployment_status("web_ui") == "v2"
