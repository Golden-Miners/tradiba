import pytest
from tradiba.hermes.skills.dependency.resolver import SkillDependencyResolver

def test_dependency_resolution():
    resolver = SkillDependencyResolver()
    resolver.register_dependencies("A", ["B", "C"])
    resolver.register_dependencies("B", ["D"])
    resolver.register_dependencies("C", [])
    resolver.register_dependencies("D", [])

    resolved = resolver.resolve("A")
    assert resolved == ["D", "B", "C", "A"]

def test_circular_dependency():
    resolver = SkillDependencyResolver()
    resolver.register_dependencies("A", ["B"])
    resolver.register_dependencies("B", ["A"])

    with pytest.raises(ValueError, match="Circular dependency detected"):
        resolver.resolve("A")

def test_version_compatibility():
    resolver = SkillDependencyResolver()
    assert resolver.validate_compatibility("1.2.0", "1.0.0")
    assert not resolver.validate_compatibility("2.0.0", "1.0.0")
