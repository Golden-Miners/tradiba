from tradiba.ecosystem.billing.metering import BillingMeter

def test_billing():
    bm = BillingMeter()
    bm.record_usage("t1", "a1", 100)
    assert bm.get_bill("t1", "a1") == 5.0
