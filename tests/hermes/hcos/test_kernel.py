from tradiba.hermes.hcos.kernel.core import CognitiveKernel

def test_kernel_lifecycle():
    kernel = CognitiveKernel()
    sess_id = kernel.start_session()
    state = kernel.get_state(sess_id)
    assert state is not None
    assert state.session_id == sess_id
    
    res = kernel.route_task(sess_id, {"task": "test"})
    assert res == "TASK_ROUTED"
    assert len(state.running_tasks) == 1

def test_kernel_recovery():
    kernel = CognitiveKernel()
    kernel.recover_session("sess_123", {"active_goals": [{"id": "g1"}], "market_context": {"BTC": 50000}})
    state = kernel.get_state("sess_123")
    assert state is not None
    assert state.system_health == "RECOVERED"
    assert state.market_context["BTC"] == 50000
