from tradiba.compliance.surveillance.platform import TradeSurveillancePlatform

def test_surveillance():
    platform = TradeSurveillancePlatform()
    assert not platform.detect_anomalies({})
