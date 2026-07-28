from tradiba.operations.chaos.framework import ChaosFramework

def test_chaos():
    chaos = ChaosFramework()
    assert chaos.execute_experiment("node_failure")
    assert not chaos.execute_experiment("unknown")
