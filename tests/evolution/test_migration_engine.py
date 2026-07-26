from tradiba.evolution.migration_engine import MigrationEngine

def test_migration_engine():
    engine = MigrationEngine()
    
    # Should execute successfully
    assert engine.execute_migration("migration_001")
    
    # Second run should be idempotent and return true
    assert engine.execute_migration("migration_001")
