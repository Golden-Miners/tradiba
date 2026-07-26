import pytest
from tradiba.data_platform.validation import DataQualityValidator
from tradiba.data_platform.exceptions import SchemaValidationError

def test_schema_validation():
    validator = DataQualityValidator()
    
    good_data = [{"price": 100, "volume": 10}, {"price": 101, "volume": 12}]
    assert validator.validate_schema(good_data, {"price", "volume"}) is True
    
    bad_data = [{"price": 100}, {"price": 101, "volume": 12}]
    with pytest.raises(SchemaValidationError):
        validator.validate_schema(bad_data, {"price", "volume"})
        
def test_quality_report():
    validator = DataQualityValidator()
    
    data = [
        {"a": 1, "b": 2},
        {"a": 3, "b": None}
    ]
    
    report = validator.generate_quality_report(data)
    assert report["score"] == 0.75  # 3 valid out of 4 total fields
    assert len(report["issues"]) == 1
    assert "1 missing" in report["issues"][0]
