from tradiba.alternative_data.validation.quality import DataQualityEngine

def test_validation():
    engine = DataQualityEngine()
    assert engine.validate_quality("d1")
