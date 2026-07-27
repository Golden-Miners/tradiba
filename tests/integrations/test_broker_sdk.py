from tradiba.integrations.brokers.paper.adapter import PaperBrokerAdapter
from tradiba.integrations.certification.suite import AdapterCertificationSuite

def test_paper_adapter_conformance():
    adapter = PaperBrokerAdapter()
    assert adapter.connect() is True
    
    account = adapter.get_account()
    assert "balance" in account
    assert "equity" in account
    
    order = adapter.submit_order("EURUSD", 1.0, "BUY")
    assert "ticket" in order
    assert order["status"] == "ACCEPTED"
    
    orders = adapter.get_orders()
    assert len(orders) == 1
    
    adapter.cancel_order(order["ticket"])
    assert adapter.get_orders()[0]["status"] == "CANCELLED"

def test_certification_suite():
    adapter = PaperBrokerAdapter()
    suite = AdapterCertificationSuite(adapter)
    assert suite.run_all() is True
