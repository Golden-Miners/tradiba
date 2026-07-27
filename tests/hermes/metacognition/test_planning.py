from tradiba.hermes.metacognition.planning.template_optimizer import PlanningOptimizer

def test_planning_optimizer():
    opt = PlanningOptimizer()
    assert opt.get_template("default")["version"] == 1
    
    res = opt.optimize_template("default", "redundant step")
    assert res == "OPTIMIZED_V2"
    assert opt.get_template("default")["version"] == 2
