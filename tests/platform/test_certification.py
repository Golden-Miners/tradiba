from tradiba.platform.certification.suite import CertificationSuite

def test_certification():
    suite = CertificationSuite()
    assert suite.run_certification()
