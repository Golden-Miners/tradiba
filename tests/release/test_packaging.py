import os

def test_packaging_structure():
    """Verify that all distribution directories exist for GA release."""
    base_dir = "distribution"
    required_dirs = [
        "docker", "kubernetes", "helm", "documentation",
        "sample_strategies", "demo_data", "release", "licensing"
    ]
    for d in required_dirs:
        assert os.path.exists(os.path.join(base_dir, d))

def test_docker_compose_exists():
    assert os.path.exists("docker-compose.yml")

def test_setup_script_exists():
    assert os.path.exists("setup.sh")
    
def test_documentation_exists():
    assert os.path.exists("distribution/documentation/architecture.md")

def test_sample_strategies_exist():
    assert os.path.exists("distribution/sample_strategies/ict_trend.py")
