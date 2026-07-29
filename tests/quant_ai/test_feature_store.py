from tradiba.quant_ai.feature_store.repository import QuantitativeFeatureStore

def test_feature_store():
    store = QuantitativeFeatureStore()
    store.features["f1"] = {"status": "active"}
    assert store.get_feature("f1")["status"] == "active"
