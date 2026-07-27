import pytest
from tradiba.hermes.live.execution.agent import LiveTradingAgent
from tradiba.hermes.live.autonomy.profile import AutonomyProfile, AutonomyLevel
from tradiba.hermes.live.policies.engine import PolicyEngine
from tradiba.hermes.live.approvals.workflow import ExecutionApprovalFramework
from tradiba.hermes.live.supervision.safety import SafetySupervisor
from tradiba.hermes.live.rollback.human_override import HumanOverrideManager
from tradiba.hermes.live.emergency.kill_switch import KillSwitch

@pytest.fixture
def execution_agent():
    profile = AutonomyProfile({"autonomy_level": AutonomyLevel.LIVE_AUTONOMOUS})
    policy = PolicyEngine({"max_position_size": 2.0})
    framework = ExecutionApprovalFramework(profile, policy)
    safety = SafetySupervisor({"max_drawdown": 1000.0})
    override = HumanOverrideManager()
    kill_switch = KillSwitch()
    return LiveTradingAgent(framework, safety, override, kill_switch)

def test_execution_agent_approve(execution_agent):
    decision = {"symbol": "BTC/USD", "size": 1.0}
    current_state = {}
    metrics = {"drawdown": 500.0}
    
    result = execution_agent.propose_trade(decision, current_state, risk_approved=True, metrics=metrics)
    assert result["status"] == "APPROVED"

def test_execution_agent_kill_switch_blocks(execution_agent):
    decision = {"symbol": "BTC/USD", "size": 1.0}
    current_state = {}
    metrics = {"drawdown": 500.0}
    
    execution_agent.kill_switch.activate_global()
    result = execution_agent.propose_trade(decision, current_state, risk_approved=True, metrics=metrics)
    assert result["status"] == "BLOCKED"
    assert result["reason"] == "KILL_SWITCH_ACTIVE"

def test_execution_agent_pause_blocks(execution_agent):
    decision = {"symbol": "BTC/USD", "size": 1.0}
    current_state = {}
    metrics = {"drawdown": 500.0}
    
    execution_agent.human_override.pause_hermes("Test")
    result = execution_agent.propose_trade(decision, current_state, risk_approved=True, metrics=metrics)
    assert result["status"] == "BLOCKED"
    assert result["reason"] == "SYSTEM_PAUSED"

def test_execution_agent_safety_blocks(execution_agent):
    decision = {"symbol": "BTC/USD", "size": 1.0}
    current_state = {}
    metrics = {"drawdown": 1500.0} # Breach
    
    result = execution_agent.propose_trade(decision, current_state, risk_approved=True, metrics=metrics)
    assert result["status"] == "BLOCKED"
    assert "SAFETY_" in result["reason"]
