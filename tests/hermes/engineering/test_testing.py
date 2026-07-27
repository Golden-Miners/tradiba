from tradiba.hermes.engineering.testing.generator import TestGenerationEngine

def test_testing():
    generator = TestGenerationEngine()
    test_code = generator.generate_tests("auth")
    assert "def test_auth():" in test_code
