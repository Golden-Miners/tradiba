from tradiba.ecosystem.certification.framework import CertificationFramework

def test_certification():
    cf = CertificationFramework()
    assert cf.certify_app("app1") == "Certified"
