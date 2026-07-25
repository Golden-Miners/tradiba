from tradiba.dev.docs import DocumentationGenerator

def test_docs_generator():
    generator = DocumentationGenerator()
    
    # Verify the simulated methods exist and don't raise
    generator.generate_html("out")
    generator.generate_markdown("out")
    generator.generate_openapi("openapi.json")
