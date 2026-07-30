from tradiba.modelops.lineage.engine import LineageEngine

def test_lineage():
    lin = LineageEngine()
    assert lin.record_lineage("s1", "t1")
