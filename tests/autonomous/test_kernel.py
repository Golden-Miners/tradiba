from tradiba.autonomous.kernel.os import EnterpriseCognitiveKernel

def test_kernel():
    kernel = EnterpriseCognitiveKernel()
    assert kernel.execute_mission("m1")
