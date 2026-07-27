from typing import Dict, Any

class ResearchQuestionGenerator:
    """
    Generates research questions with impact and success criteria.
    """
    def __init__(self):
        self.questions: Dict[str, Dict[str, Any]] = {}
        
    def generate_question(self, question_id: str, topic: str, expected_impact: str) -> Dict[str, Any]:
        question = {
            "id": question_id,
            "topic": topic,
            "expected_impact": expected_impact,
            "priority": "HIGH"
        }
        self.questions[question_id] = question
        return question
