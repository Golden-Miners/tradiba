from tradiba.data_mesh.contracts.registry import ContractRegistry

def test_contracts():
    reg = ContractRegistry()
    assert reg.validate_contract({})
