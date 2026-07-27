from tradiba.hermes.scientist.statistics.validator import StatisticalValidator

def test_statistics():
    validator = StatisticalValidator()
    assert validator.validate(0.01)
    assert not validator.validate(0.10)
