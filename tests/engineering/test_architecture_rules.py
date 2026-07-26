import yaml # type: ignore
from pathlib import Path
import ast

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

def load_matrix():
    matrix_file = Path("engineering/architecture/dependency_matrix.yaml")
    if not matrix_file.exists():
        return {}
        
    with open(matrix_file, "r") as f:
        data = yaml.safe_load(f)
        
    return {d["name"]: d["allowed_dependencies"] for d in data.get("domains", [])}

def test_dependency_matrix():
    matrix = load_matrix()
    if not matrix:
        return
        
    src_dir = Path("src/tradiba")
    
    for domain_name, allowed in matrix.items():
        domain_dir = src_dir / domain_name
        if not domain_dir.exists():
            continue
            
        for filepath in domain_dir.rglob("*.py"):
            imports = get_imports_for_file(filepath)
            
            for imp in imports:
                # We only care about cross-domain imports within tradiba
                if not imp.startswith("tradiba."):
                    continue
                    
                # A domain can import itself
                if imp.startswith(f"tradiba.{domain_name}"):
                    continue
                    
                # Check if the imported module is in the allowed list
                is_allowed = any(imp.startswith(a) for a in allowed)
                assert is_allowed, f"Illegal import in {domain_name} ({filepath}): {imp} is not in allowed dependencies {allowed}"
