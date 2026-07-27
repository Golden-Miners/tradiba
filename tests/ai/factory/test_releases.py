from tradiba.ai.factory.releases.manager import ReleaseManager

def test_releases():
    manager = ReleaseManager()
    manager.create_release("v1", ["model_1", "dataset_1"])
    assert manager.releases["v1"]["status"] == "CANDIDATE"
    
    manager.approve_release("v1", "admin")
    assert manager.releases["v1"]["status"] == "APPROVED"
