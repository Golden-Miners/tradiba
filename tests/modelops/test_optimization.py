from tradiba.modelops.optimization.hyperparameters import HyperparameterOptimization

def test_optimization():
    opt = HyperparameterOptimization()
    assert opt.optimize("m1")["lr"] == 0.01
