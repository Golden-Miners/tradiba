from tradiba.hermes.metacognition.reasoning.tool_selection import ToolSelectionOptimizer

def test_tool_selection():
    opt = ToolSelectionOptimizer()
    opt.record_usage("t1", True, 0.5)
    opt.record_usage("t2", False, 1.0)
    
    ranked = opt.rank_tools(["t2", "t1"])
    assert ranked[0] == "t1"
    assert ranked[1] == "t2"
