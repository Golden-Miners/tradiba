from tradiba.hermes.skills.certification.framework import SkillCertificationFramework, CertificationLevel

def test_certification():
    framework = SkillCertificationFramework()
    
    c1 = framework.certify("s1", 0.98, True)
    assert c1 == CertificationLevel.ENTERPRISE

    c2 = framework.certify("s2", 0.90, True)
    assert c2 == CertificationLevel.PRODUCTION

    c3 = framework.certify("s3", 0.80, False)
    assert c3 == CertificationLevel.EXPERIMENTAL

    assert framework.get_certification("s1") == CertificationLevel.ENTERPRISE
