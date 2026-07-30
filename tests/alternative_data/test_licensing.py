from tradiba.alternative_data.licensing.engine import LicensingEngine

def test_licensing():
    engine = LicensingEngine()
    assert engine.verify_license("d1")
