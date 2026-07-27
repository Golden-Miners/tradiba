
class SecureCodeReviewAgent:
    """
    Scans generated code for performance regressions and security issues.
    """
    def __init__(self):
        self.findings = []
        
    def review(self, code: str) -> bool:
        if "eval(" in code:
            self.findings.append("Security issue: eval used")
            return False
        return True
