from tradiba.ai.workflows.sdk import AIWorkflowSDK

def test_workflows():
    sdk = AIWorkflowSDK()
    sdk.create_workflow("w1", ["Planner", "Reasoner", "Response"])
    res = sdk.execute("w1", "Goal")
    assert "Goal -> Planner -> Reasoner -> Response" in res
