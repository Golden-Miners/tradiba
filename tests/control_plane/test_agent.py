import uuid
import pytest
from tradiba.control_plane.agent import TradibaAgent
from tradiba.control_plane.exceptions import AgentConnectionError

def test_agent_heartbeat():
    agent = TradibaAgent(uuid.uuid4())
    assert agent.connected is False
    
    with pytest.raises(AgentConnectionError):
        agent.ping()
        
    agent.connect()
    assert agent.connected is True
    assert agent.last_heartbeat > 0
    
    agent.disconnect()
    assert agent.connected is False
