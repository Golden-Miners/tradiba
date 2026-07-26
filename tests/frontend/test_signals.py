from tradiba.frontend_api.signals import SignalStreamService

def test_signal_stream_service():
    service = SignalStreamService()
    
    signals = service.get_active_signals()
    assert len(signals) > 0
    assert signals[0]["direction"] == "Buy"
    assert "confidence" in signals[0]
