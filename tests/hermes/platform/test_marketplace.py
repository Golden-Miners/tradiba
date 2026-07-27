from tradiba.hermes.platform.skills.marketplace import SkillMarketplace

def test_marketplace():
    marketplace = SkillMarketplace()
    marketplace.install("skill1", {"version": "1.0"})
    assert marketplace.get_skill("skill1")["version"] == "1.0"
