from tradiba.quant_ai.validation.laboratory import AIValidationLaboratory

def test_validation():
    lab = AIValidationLaboratory()
    assert lab.validate_model("m1")
