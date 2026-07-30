from tradiba.platform.security.hardening import SecurityHardening

def test_security():
    sec = SecurityHardening()
    assert sec.scan()
