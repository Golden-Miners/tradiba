from tradiba.hermes.live.supervision.safety import SafetySupervisor

def test_safety_supervisor_safe():
    supervisor = SafetySupervisor({
        "max_drawdown": 500.0,
        "max_slippage": 0.05
    })
    
    metrics = {
        "drawdown": 200.0,
        "slippage": 0.02,
        "broker_connected": True
    }
    
    assert supervisor.check_safety(metrics) == "SAFE"

def test_safety_supervisor_drawdown_breach():
    supervisor = SafetySupervisor({"max_drawdown": 500.0})
    metrics = {"drawdown": 600.0}
    assert supervisor.check_safety(metrics) == "BREACH_DRAWDOWN"

def test_safety_supervisor_broker_disconnect():
    supervisor = SafetySupervisor({})
    metrics = {"broker_connected": False}
    assert supervisor.check_safety(metrics) == "BREACH_BROKER_DISCONNECTED"
