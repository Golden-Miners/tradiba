from tradiba.ecosystem.licensing.license_manager import LicenseManager

def test_licensing():
    lm = LicenseManager()
    lic = lm.issue_license("t1", "a1", "pro")
    assert lm.verify_license(lic)
