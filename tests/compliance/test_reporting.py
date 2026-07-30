from tradiba.compliance.reporting.engine import RegulatoryReportingEngine

def test_reporting():
    engine = RegulatoryReportingEngine()
    assert engine.generate_report("r1") == "report_data_for_r1"
