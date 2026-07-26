from tradiba.digital_twin.validation import ContinuousValidator

def test_continuous_validation():
    validator = ContinuousValidator()
    
    assert validator.validate_continuous({"latency_ms": 10}, {"latency_ms": 15}) is True
    assert validator.validate_continuous({"latency_ms": 10}, {"latency_ms": 80}) is False
