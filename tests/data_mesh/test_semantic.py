from tradiba.data_mesh.semantic.layer import SemanticLayer

def test_semantic():
    layer = SemanticLayer()
    assert layer.get_definition("term") == "Definition"
