from tradiba.modelops.datasets.versioning import DatasetVersioning

def test_datasets():
    versioning = DatasetVersioning()
    assert versioning.version_dataset("d1", "v1")
