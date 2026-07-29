from tradiba.knowledge.lifecycle.manager import KnowledgeLifecycleManager

def test_lifecycle():
    manager = KnowledgeLifecycleManager()
    manager.set_state("k1", "Published")
    assert manager.get_state("k1") == "Published"
    assert manager.get_state("k2") == "Draft"
