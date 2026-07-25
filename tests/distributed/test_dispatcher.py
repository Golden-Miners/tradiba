from uuid import uuid4
from tradiba.distributed.dispatcher import CommandDispatcher, CommandMetadata
from tradiba.distributed.messaging.in_memory import InMemoryMessageBus

def test_command_dispatcher():
    bus = InMemoryMessageBus()
    dispatcher = CommandDispatcher(bus)
    
    received = []
    def handler(msg):
        received.append(msg)
        
    bus.subscribe("test.topic", handler)
    
    command = {"action": "buy", "symbol": "AAPL"}
    meta = CommandMetadata(
        command_id=uuid4(),
        correlation_id=uuid4(),
        idempotency_key="idemp-1"
    )
    
    # Check idempotency handling
    assert not dispatcher.is_processed("idemp-1")
    dispatcher.mark_processed("idemp-1")
    assert dispatcher.is_processed("idemp-1")
    
    # Dispatch
    dispatcher.dispatch("test.topic", command, meta)
    
    assert len(received) == 1
    assert received[0]["command"] == command
    assert received[0]["metadata"]["idempotency_key"] == "idemp-1"
