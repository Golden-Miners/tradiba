from tradiba.hermes.federation.learning.federated_learning import FederatedLearning

def test_learning():
    fl = FederatedLearning()
    fl.exchange_model("m1", {"acc": 0.95})
    assert len(fl.get_shared_models()) == 1
