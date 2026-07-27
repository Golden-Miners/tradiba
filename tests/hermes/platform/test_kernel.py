from tradiba.hermes.platform.kernel.core import UnifiedCognitiveKernel

def test_kernel():
    kernel = UnifiedCognitiveKernel()
    assert kernel.state == "STOPPED"
    kernel.start()
    assert kernel.state == "RUNNING"
    assert kernel.execute_task("t1")
