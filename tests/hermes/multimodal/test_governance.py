from tradiba.hermes.multimodal.governance.safety import SafetyGovernance

def test_governance():
    sg = SafetyGovernance()
    assert sg.validate_content("clean text", "text")
    assert not sg.validate_content("some MALWARE here", "text")
    assert sg.detect_pii("text") == []
