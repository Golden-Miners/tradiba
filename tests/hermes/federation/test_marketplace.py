from tradiba.hermes.federation.marketplace.distributed_catalog import DistributedCatalog

def test_marketplace():
    cat = DistributedCatalog()
    cat.publish_skill("skill1", {"publisher": "org1"})
    assert len(cat.search_skills("skill1")) == 1
