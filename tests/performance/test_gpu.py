import pytest
from tradiba.performance.gpu import CpuComputeBackend, GpuComputeBackend
from tradiba.performance.exceptions import ComputeBackendError

def test_cpu_backend():
    backend = CpuComputeBackend()
    result = backend.execute("test_op")
    assert result is None

def test_gpu_backend_fallback():
    backend = GpuComputeBackend()
    assert not backend.available
    
    with pytest.raises(ComputeBackendError):
        backend.execute("test_op")
