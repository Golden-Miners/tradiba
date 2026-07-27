from tradiba.hermes.scientist.peer_review.framework import PeerReviewFramework

def test_peer_review():
    framework = PeerReviewFramework()
    framework.submit_for_review("s1")
    assert not framework.is_approved("s1")
    
    framework.add_review("s1", "human")
    framework.add_review("s1", "ai")
    assert framework.is_approved("s1")
