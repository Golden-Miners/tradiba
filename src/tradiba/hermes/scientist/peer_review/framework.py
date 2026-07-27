from typing import Dict, List

class PeerReviewFramework:
    """
    Enforces automated and human reviews before research approval.
    """
    def __init__(self):
        self.reviews: Dict[str, List[str]] = {}
        
    def submit_for_review(self, study_id: str):
        self.reviews[study_id] = []
        
    def add_review(self, study_id: str, reviewer: str):
        if study_id in self.reviews:
            self.reviews[study_id].append(reviewer)
            
    def is_approved(self, study_id: str) -> bool:
        if study_id in self.reviews:
            return "human" in self.reviews[study_id] and "ai" in self.reviews[study_id]
        return False
