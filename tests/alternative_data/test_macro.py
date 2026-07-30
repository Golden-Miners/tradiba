from tradiba.alternative_data.macro.intelligence import MacroIntelligence

def test_macro():
    macro = MacroIntelligence()
    assert macro.update_macro("m1")
