from tradiba.ai.runtime.agent_runtime import AIRuntime

def test_runtime():
    rt = AIRuntime()
    rt.start_session("s1", "agent1")
    resp = rt.execute_turn("s1", "hello")
    assert "Processed hello by agent1" in resp["output"]
