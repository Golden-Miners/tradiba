from fastapi.testclient import TestClient

from tradiba.api.app import app

from tradiba.events import EventBus
from tradiba.api.websocket import WebSocketManager
import tradiba.api.websocket

client = TestClient(app)

def test_websocket():
    # Mock global ws_manager without running loop
    tradiba.api.websocket.ws_manager = WebSocketManager(EventBus())
    
    with client.websocket_connect("/ws"):
        assert len(tradiba.api.websocket.ws_manager.active_connections) == 1
        
    assert len(tradiba.api.websocket.ws_manager.active_connections) == 0
