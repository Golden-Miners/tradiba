from tradiba.platform.migration.pipeline import MigrationPipeline

def test_migration():
    pipe = MigrationPipeline()
    assert pipe.migrate()
