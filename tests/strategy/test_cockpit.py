from tradiba.strategy.cockpit.dashboard import ExecutiveDecisionCockpit

def test_cockpit():
    cockpit = ExecutiveDecisionCockpit()
    assert "revenue" in cockpit.get_dashboard()["kpis"]
