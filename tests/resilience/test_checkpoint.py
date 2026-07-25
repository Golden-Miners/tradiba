from tradiba.resilience.checkpoint import RecoveryCheckpoint, InMemoryCheckpointRepository

def test_checkpoint_creation_and_retrieval():
    repo = InMemoryCheckpointRepository()
    checkpoint1 = RecoveryCheckpoint(portfolio_version=1, event_sequence=10)
    repo.save(checkpoint1)
    
    latest = repo.get_latest()
    assert latest is not None
    assert latest.portfolio_version == 1
    assert latest.event_sequence == 10
    
    checkpoint2 = RecoveryCheckpoint(portfolio_version=2, event_sequence=20)
    repo.save(checkpoint2)
    
    latest2 = repo.get_latest()
    assert latest2 is not None
    assert latest2.portfolio_version == 2
    assert latest2.event_sequence == 20
