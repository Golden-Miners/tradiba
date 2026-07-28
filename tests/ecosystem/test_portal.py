from tradiba.ecosystem.portal.enterprise_dashboard import EnterprisePortal

def test_portal():
    ep = EnterprisePortal()
    assert ep.get_dashboard_data()["stats"]["active_users"] == 0
