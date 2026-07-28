from tradiba.hermes.skills.marketplace.catalog import SkillMarketplaceCatalog

def test_marketplace():
    catalog = SkillMarketplaceCatalog()
    catalog.publish_skill("s1", {"domain": "trading", "tags": ["alpha", "fx"]})
    catalog.publish_skill("s2", {"domain": "research", "tags": ["nlp"]})

    results = catalog.search(domain="trading")
    assert len(results) == 1
    assert results[0]["domain"] == "trading"

    tag_results = catalog.search(tag="nlp")
    assert len(tag_results) == 1
    assert tag_results[0]["domain"] == "research"
