from tradiba.hermes.enterprise.analytics.executive import ExecutiveAnalytics

def test_analytics():
    analytics = ExecutiveAnalytics()
    assert analytics.get_kpi("engineering_velocity") == 85.0
