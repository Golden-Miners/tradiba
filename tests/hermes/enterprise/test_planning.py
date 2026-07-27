from tradiba.hermes.enterprise.planning.resource import ResourcePlanner

def test_planning():
    planner = ResourcePlanner()
    assert planner.forecast("engineering") == 100
