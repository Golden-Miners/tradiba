from tradiba.evolution.api_versioning import APIVersioning

def test_api_versioning():
    versioning = APIVersioning()
    
    assert versioning.is_supported("v1")
    
    versioning.deprecate_version("v1")
    
    assert not versioning.is_supported("v1")
