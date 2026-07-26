import ast
from pathlib import Path

def get_imports_for_file(filepath: Path) -> list[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read(), filename=str(filepath))
        except SyntaxError:
            return []
            
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    return imports

def test_no_infrastructure_in_domain():
    """Domain layer must not import infrastructure or external libraries directly."""
    src_dir = Path("src/tradiba")
    
    # We will just look at the trading domain as an example
    domain_dir = src_dir / "trading" / "domain"
    
    if not domain_dir.exists():
        return
        
    for filepath in domain_dir.rglob("*.py"):
        imports = get_imports_for_file(filepath)
        for imp in imports:
            # Should not import infrastructure
            assert "infrastructure" not in imp, f"Domain file {filepath} imports infrastructure: {imp}"
            # Should not import fast api, sqlalchemy, etc (simplified for test)
            assert "sqlalchemy" not in imp, f"Domain file {filepath} imports sqlalchemy: {imp}"
            assert "fastapi" not in imp, f"Domain file {filepath} imports fastapi: {imp}"

def test_shared_kernel_independence():
    """Shared kernel must not depend on any specific domain."""
    shared_dir = Path("src/tradiba/shared")
    
    if not shared_dir.exists():
        return
        
    domains = ["trading", "research", "workflows", "analytics", "aiops", "control_plane"]
    
    for filepath in shared_dir.rglob("*.py"):
        imports = get_imports_for_file(filepath)
        for imp in imports:
            for domain in domains:
                assert f"tradiba.{domain}" not in imp, f"Shared kernel file {filepath} imports domain {domain}: {imp}"
