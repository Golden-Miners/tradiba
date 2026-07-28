from tradiba.ecosystem.sdk.developer_tools import DeveloperSDK

def test_sdk():
    sdk = DeveloperSDK()
    assert sdk.package_app("src") == "pkg_src"
    assert sdk.simulate("app1")
