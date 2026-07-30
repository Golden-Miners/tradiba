from tradiba.modelops.monitoring.online import OnlineMonitoring

def test_monitoring():
    mon = OnlineMonitoring()
    assert mon.monitor("m1")
