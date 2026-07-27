from tradiba.hermes.metacognition.optimizer.workflow_optimizer import WorkflowOptimizer

def test_workflow_optimizer():
    opt = WorkflowOptimizer()
    workflow = [
        {"tool": "fetch_price"},
        {"tool": "fetch_price"}, # redundant
        {"tool": "fetch_price", "requires_fresh": True} # not redundant
    ]
    
    res = opt.optimize_workflow(workflow)
    assert len(res) == 2
    assert res[0]["tool"] == "fetch_price"
    assert res[1].get("requires_fresh") == True
