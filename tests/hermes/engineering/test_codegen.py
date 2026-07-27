from tradiba.hermes.engineering.codegen.generator import CodeGenerator

def test_codegen():
    generator = CodeGenerator()
    code = generator.generate("service", "Test")
    assert "class TestService:" in code
