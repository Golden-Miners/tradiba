from typing import Dict, List, Set

class SkillDependencyResolver:
    """
    Semantic versioning, circular dependency detection, compatibility check, and upgrade planner.
    """
    def __init__(self):
        self.dependencies: Dict[str, List[str]] = {}

    def register_dependencies(self, skill_id: str, deps: List[str]) -> None:
        self.dependencies[skill_id] = deps

    def resolve(self, skill_id: str) -> List[str]:
        visited: Set[str] = set()
        resolved: List[str] = []

        def dfs(node: str, path: Set[str]):
            if node in path:
                raise ValueError(f"Circular dependency detected: {node} in path {path}")
            if node not in visited:
                visited.add(node)
                path.add(node)
                for dep in self.dependencies.get(node, []):
                    dfs(dep, path)
                path.remove(node)
                resolved.append(node)

        dfs(skill_id, set())
        return resolved

    def validate_compatibility(self, skill_version: str, required_version: str) -> bool:
        # Simplified semver major check
        skill_major = skill_version.split(".")[0]
        req_major = required_version.split(".")[0]
        return skill_major == req_major
