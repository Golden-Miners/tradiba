from tradiba.hermes.hcos.planner.hierarchical import HierarchicalPlanner

def test_planner():
    planner = HierarchicalPlanner()
    mid = planner.create_plan("m1", "mission")
    planner.add_objective(mid, "obj1")
    
    assert len(planner.active_plans[mid]["objectives"]) == 1
    
    planner.pause_plan(mid)
    assert planner.active_plans[mid]["status"] == "PAUSED"
    
    planner.resume_plan(mid)
    assert planner.active_plans[mid]["status"] == "ACTIVE"
