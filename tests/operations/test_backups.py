import pytest
import os
from tradiba.operations.backups import BackupManager

def test_trigger_database_backup(tmp_path):
    """Test simulating a database backup."""
    manager = BackupManager(backup_dir=str(tmp_path))
    backup_file = manager.trigger_database_backup()
    
    assert os.path.exists(backup_file)
    assert manager.verify_backup(backup_file)

def test_trigger_event_store_backup(tmp_path):
    """Test simulating an event store backup."""
    manager = BackupManager(backup_dir=str(tmp_path))
    backup_file = manager.trigger_event_store_backup()
    
    assert os.path.exists(backup_file)
    assert manager.verify_backup(backup_file)
