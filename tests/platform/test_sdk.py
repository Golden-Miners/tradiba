from tradiba.platform.compatibility.checker import CompatibilityChecker

def test_sdk():
    checker = CompatibilityChecker()
    assert checker.verify()
