from tradiba.autonomous_research.validation import ValidationFramework

def test_validation_framework():
    framework = ValidationFramework()
    
    good_results = {"results": {"sharpe_ratio": 1.5, "max_drawdown": 0.10}}
    bad_results = {"results": {"sharpe_ratio": 0.8, "max_drawdown": 0.20}}
    
    assert framework.validate(good_results) is True
    assert framework.validate(bad_results) is False
