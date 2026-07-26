from tradiba.evolution.feature_flags import FeatureFlagManager

def test_feature_flags():
    manager = FeatureFlagManager()
    
    manager.configure_flag("new_ui", enabled=True)
    assert manager.is_enabled("new_ui")
    
    manager.configure_flag("beta_algo", enabled=False, percentage=0.0)
    assert not manager.is_enabled("beta_algo")
