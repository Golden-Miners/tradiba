import pytest
import os
from tradiba.hermes.learning.knowledge.consolidation import KnowledgeConsolidator

@pytest.fixture
def consolidator():
    db_path = "test_knowledge.db"
    c = KnowledgeConsolidator(db_path)
    c.clear_db()
    yield c
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except PermissionError:
            pass

def test_add_and_get_knowledge(consolidator):
    consolidator.add_knowledge("BTC_RSI", {"insight": "oversold"}, 0.8, "research_agent")
    results = consolidator.get_knowledge("BTC_RSI")
    assert len(results) == 1
    assert results[0]["content"]["insight"] == "oversold"

def test_consolidation_marks_superseded(consolidator):
    import time
    consolidator.add_knowledge("ETH_MACD", {"val": 1}, 0.5, "agent1")
    time.sleep(0.01)
    consolidator.add_knowledge("ETH_MACD", {"val": 2}, 0.9, "agent2")
    
    consolidator.consolidate()
    
    results = consolidator.get_knowledge("ETH_MACD")
    assert len(results) == 2
    
    drafts = [r for r in results if r["status"] == "DRAFT"]
    superseded = [r for r in results if r["status"] == "SUPERSEDED"]
    
    assert len(drafts) == 1
    assert len(superseded) == 1
    assert drafts[0]["content"]["val"] == 2
