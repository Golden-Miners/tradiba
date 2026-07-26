import json
from pathlib import Path
import subprocess

def test_sbom_generation():
    """Verify that SBOM can be generated and meets required schema."""
    script_path = Path("engineering/security/sbom/generate_sbom.py")
    sbom_path = Path("engineering/security/sbom/sbom.json")
    
    if sbom_path.exists():
        sbom_path.unlink()
        
    # Run the generator
    subprocess.run(["python", str(script_path)], check=True)
    
    assert sbom_path.exists(), "SBOM file was not created"
    
    with open(sbom_path, "r") as f:
        sbom = json.load(f)
        
    assert sbom["bomFormat"] == "CycloneDX"
    assert "components" in sbom
    assert len(sbom["components"]) > 0
    
    # Clean up
    sbom_path.unlink()
