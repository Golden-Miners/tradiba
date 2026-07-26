from tradiba.digital_twin.deployment import DeploymentValidator

def test_deployment_validation():
    validator = DeploymentValidator()
    
    assert validator.validate_deployment("v2.5.0", {}) is True
    assert validator.validate_deployment("v1.0.0", {}) is False
