from tradiba.hermes.scientist.questions.generator import ResearchQuestionGenerator

def test_questions():
    gen = ResearchQuestionGenerator()
    q = gen.generate_question("q1", "Trading", "High")
    assert q["topic"] == "Trading"
    assert q["priority"] == "HIGH"
