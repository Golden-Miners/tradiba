from tradiba.distributed.messaging.in_memory import InMemoryMessageBus

def test_dead_letter_routing():
    # Simulate a DLQ pattern
    main_bus = InMemoryMessageBus()
    dlq_bus = InMemoryMessageBus()
    
    dlq_messages = []
    dlq_bus.subscribe("dlq.topic", lambda m: dlq_messages.append(m))
    
    def failing_handler(msg):
        # We simulate the bus handler rejecting and passing to DLQ
        # In a real broker this is native. Here we catch and forward.
        try:
            raise ValueError("Processing failed")
        except Exception:
            dlq_bus.publish("dlq.topic", msg)
            
    main_bus.subscribe("main.topic", failing_handler)
    
    main_bus.publish("main.topic", {"data": "test"})
    
    assert len(dlq_messages) == 1
    assert dlq_messages[0] == {"data": "test"}
