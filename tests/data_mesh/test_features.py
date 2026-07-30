from tradiba.data_mesh.features.platform import FeaturePlatform

def test_features():
    feat = FeaturePlatform()
    assert feat.compute_feature("f1")
