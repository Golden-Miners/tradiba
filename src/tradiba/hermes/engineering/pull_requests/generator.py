from typing import Dict, Any

class PullRequestGenerator:
    """
    Produces complete draft PRs containing motivation, test results, etc.
    """
    def __init__(self):
        self.prs = {}
        
    def generate_pr(self, title: str, description: str) -> Dict[str, Any]:
        pr = {
            "title": title,
            "description": description,
            "status": "DRAFT"
        }
        self.prs[title] = pr
        return pr
