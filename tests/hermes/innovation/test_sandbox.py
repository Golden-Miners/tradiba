from tradiba.hermes.innovation.sandbox.cognitive_sandbox import CognitiveSandbox

def test_sandbox():
    sandbox = CognitiveSandbox()
    
    assert sandbox.evaluate({"code": "works"}) == "PASSED_SANDBOX"
    assert sandbox.evaluate({"code": "fail"}) == "FAILED_STATIC_VALIDATION"
