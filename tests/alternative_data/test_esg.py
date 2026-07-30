from tradiba.alternative_data.esg.framework import ESGFramework

def test_esg():
    esg = ESGFramework()
    assert esg.process_esg("e1")["e_score"] == 85.0
