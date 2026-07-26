# Tradiba Engineering Standards

## 1. Python Style
- We strictly follow PEP 8.
- Code is formatted using `ruff` with line length 120.
- All functions must have type hints. `mypy` strict mode must pass.
- Docstrings follow Google style.

## 2. Architecture Boundaries
- Domain boundaries are enforced via `tests/engineering/test_architecture_rules.py`.
- Domains may not import external infrastructure libraries.
- Domains communicate via Domain Events (e.g., `OrderSubmitted`) using the standard `EventEnvelope`.

## 3. APIs and Versioning
- APIs follow RESTful conventions.
- Breaking changes require a new major version (e.g., `/api/v2/...`).
- Semantic Versioning is strictly enforced.

## 4. Testing
- Test coverage must remain above 90%.
- Contract tests must pass for bounded contexts before merge.
- API compatibility tests must pass before merge.
