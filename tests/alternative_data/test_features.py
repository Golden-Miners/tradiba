from tradiba.alternative_data.features.engineering import FeatureEngineeringPlatform

def test_features():
    features = FeatureEngineeringPlatform()
    assert features.generate_feature("f1")
