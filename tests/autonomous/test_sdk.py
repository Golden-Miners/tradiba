from tradiba.autonomous.sdk.client import AutonomousEnterpriseSDK

def test_sdk():
    sdk = AutonomousEnterpriseSDK()
    m = sdk.create_mission("sdk_test")
    assert m.goal == "sdk_test"
    assert sdk.execute(m)
