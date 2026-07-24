from unittest.mock import MagicMock, patch
from tradiba.mt5.connection import MT5ConnectionManager, BrokerConnectedEvent
from tradiba.events import EventBus
from tradiba.scheduler import Scheduler

@patch("tradiba.mt5.connection.mt5")
def test_connection_manager_success(mock_mt5):
    # Setup mock
    mock_mt5.initialize.return_value = True
    terminal_info_mock = MagicMock()
    terminal_info_mock.connected = True
    terminal_info_mock.name = "Test Broker"
    terminal_info_mock._asdict.return_value = {"name": "Test Broker"}
    mock_mt5.terminal_info.return_value = terminal_info_mock
    
    event_bus = EventBus()
    scheduler = Scheduler()
    manager = MT5ConnectionManager(event_bus, scheduler)
    
    # Catch events
    events = []
    event_bus.subscribe(BrokerConnectedEvent, lambda e: events.append(e))
    
    # Act
    manager.start()
    
    # Assert
    mock_mt5.initialize.assert_called_once()
    assert manager._connected is True
    assert len(events) == 1
    assert events[0].terminal_info["name"] == "Test Broker"
    
    # Stop
    manager.stop()
    mock_mt5.shutdown.assert_called_once()

@patch("tradiba.mt5.connection.mt5")
def test_connection_manager_reconnect(mock_mt5):
    # Setup initial success
    mock_mt5.initialize.return_value = True
    terminal_info_mock = MagicMock()
    terminal_info_mock.connected = True
    mock_mt5.terminal_info.return_value = terminal_info_mock
    
    event_bus = EventBus()
    scheduler = Scheduler()
    manager = MT5ConnectionManager(event_bus, scheduler)
    manager.start()
    
    assert manager._connected is True
    
    # Simulate connection drop
    terminal_info_mock.connected = False
    
    # Trigger monitor manually
    manager._monitor_connection()
    
    # Should attempt reconnect
    assert mock_mt5.initialize.call_count == 2
