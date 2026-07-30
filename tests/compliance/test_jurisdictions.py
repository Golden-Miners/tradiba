from tradiba.compliance.jurisdictions.packs import JurisdictionPacks

def test_jurisdictions():
    packs = JurisdictionPacks()
    assert packs.get_rules_for_jurisdiction("US")[0] == "rule_1_US"
