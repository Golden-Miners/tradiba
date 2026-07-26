from tradiba.data_platform.feature_store import FeatureStore, Feature

def test_feature_store():
    store = FeatureStore()
    
    feat_v1 = Feature(name="vwap", version="v1", description="Volume weighted average price", data=[{"value": 100}])
    feat_v2 = Feature(name="vwap", version="v2", description="VWAP with outlier rejection", data=[{"value": 101}])
    
    store.register(feat_v1)
    store.register(feat_v2)
    
    latest = store.retrieve("vwap")
    assert latest is not None
    assert latest.version == "v2"
    
    specific = store.retrieve("vwap", version="v1")
    assert specific is not None
    assert specific.version == "v1"
    
    versions = store.list_versions("vwap")
    assert "v1" in versions
    assert "v2" in versions
