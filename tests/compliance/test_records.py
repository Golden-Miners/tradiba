from tradiba.compliance.records.management import RecordsManagement

def test_records():
    mgr = RecordsManagement()
    assert mgr.store_record("r1", {})
