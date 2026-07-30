from tradiba.compliance.controls.library import ComplianceControlLibrary

def test_controls():
    lib = ComplianceControlLibrary()
    assert lib.check_control("c1", {})
