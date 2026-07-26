from tradiba.autonomous_research.feature_discovery import FeatureStore, DiscoveredFeature

def test_feature_registration():
    store = FeatureStore()
    feat = DiscoveredFeature(name="test_feat", source="test", description="desc", version="v1")
    store.register(feat)
    
    features = store.get_features()
    assert len(features) == 1
    assert features[0].name == "test_feat"
