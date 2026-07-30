from tradiba.modelops.deployment.manager import DeploymentManager

def test_deployment():
    dep = DeploymentManager()
    assert dep.deploy("m1", "shadow")
