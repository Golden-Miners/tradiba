from tradiba.platform.upgrade.manager import UpgradeManager

def test_upgrade():
    mgr = UpgradeManager()
    assert mgr.upgrade("v10.0")
