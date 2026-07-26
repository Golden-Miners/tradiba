import json
from pathlib import Path
from datetime import datetime

def generate_sbom():
    """Simulates generating a CycloneDX/SPDX SBOM."""
    # In reality, this would use a tool like Syft or CycloneDX-Python
    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.4",
        "serialNumber": "urn:uuid:3e671687-395b-41f5-a30f-a58921a69b79",
        "version": 1,
        "metadata": {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "component": {
                "type": "application",
                "name": "tradiba",
                "version": "1.0.0"
            }
        },
        "components": [
            {
                "type": "library",
                "name": "sqlalchemy",
                "version": "2.0.29",
                "purl": "pkg:pypi/sqlalchemy@2.0.29"
            },
            {
                "type": "library",
                "name": "fastapi",
                "version": "0.111.0",
                "purl": "pkg:pypi/fastapi@0.111.0"
            }
        ]
    }
    
    out_dir = Path("engineering/security/sbom")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    with open(out_dir / "sbom.json", "w") as f:
        json.dump(sbom, f, indent=2)
        
    print("SBOM generated at engineering/security/sbom/sbom.json")

if __name__ == "__main__":
    generate_sbom()
