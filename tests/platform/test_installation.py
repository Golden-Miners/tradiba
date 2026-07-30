from tradiba.platform.installation.framework import InstallationFramework

def test_installation():
    inst = InstallationFramework()
    assert inst.install("developer")
