from tradiba.hermes.engineering.documentation.generator import DocumentationGenerator

def test_documentation():
    generator = DocumentationGenerator()
    content = generator.update_doc("api", "# API")
    assert generator.docs["api"] == "# API"
