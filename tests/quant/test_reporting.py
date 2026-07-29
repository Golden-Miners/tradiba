from tradiba.quant.reports.institutional import InstitutionalReporting

def test_reporting():
    reporter = InstitutionalReporting()
    res = reporter.generate_daily_report()
    assert res["status"] == "generated"
