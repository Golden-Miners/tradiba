from tradiba.compliance.analytics.dashboards import ComplianceAnalytics

def test_analytics():
    analytics = ComplianceAnalytics()
    assert analytics.get_dashboard_data()["open_investigations"] == 5
