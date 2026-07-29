from tradiba.knowledge.ontology.manager import OntologyManager

def test_ontology():
    manager = OntologyManager()
    manager.register_schema("Trading", {})
    assert manager.validate_entity("Trading", {})
    assert not manager.validate_entity("Risk", {})
