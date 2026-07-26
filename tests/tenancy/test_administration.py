from tradiba.tenancy.administration import PlatformAdministration

def test_platform_administration():
    admin = PlatformAdministration()
    
    assert not admin.is_feature_enabled("beta_ui")
    admin.set_feature_flag("beta_ui", True)
    assert admin.is_feature_enabled("beta_ui")
