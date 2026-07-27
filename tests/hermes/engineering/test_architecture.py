from tradiba.hermes.engineering.architecture.analyzer import ArchitectureAnalyzer

def test_architecture():
    analyzer = ArchitectureAnalyzer()
    res = analyzer.analyze_boundaries()
    assert res["healthy"]
