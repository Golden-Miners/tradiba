from tradiba.hermes.enterprise.dashboards.executive import ExecutiveDashboard

def test_dashboards():
    dash = ExecutiveDashboard()
    assert dash.render() == {}
