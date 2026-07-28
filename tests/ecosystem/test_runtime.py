from tradiba.ecosystem.runtime.sandbox import RuntimeSandbox

def test_runtime():
    sb = RuntimeSandbox()
    assert sb.start_app("app1")
    assert sb.stop_app("app1")
    assert not sb.stop_app("app2")
