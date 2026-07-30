from tradiba.platform.documentation.generator import DocumentationGenerator

def test_documentation():
    gen = DocumentationGenerator()
    assert gen.generate()
