from tradiba.hermes.engineering.reviews.secure_review import SecureCodeReviewAgent

def test_reviews():
    agent = SecureCodeReviewAgent()
    assert agent.review("def test(): pass")
    assert not agent.review("def test(): eval('1+1')")
