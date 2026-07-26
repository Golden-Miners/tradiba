# 0001 - Hexagonal Architecture

## Context
Tradiba has grown into a large modular monolith. As business capabilities expanded, the risk of coupling between infrastructure (databases, APIs, third-party libraries) and core trading logic has increased.

## Decision
We will adopt a Hexagonal (Ports and Adapters) Architecture globally across the Tradiba platform. 
The core domain model will not depend on any external libraries or infrastructure details (e.g., SQLAlchemy, FastAPI, Kafka).
All external communication will happen through Ports (Protocols/Interfaces) which will be implemented by Adapters in the infrastructure layer.

## Consequences
- **Pros:** Business logic becomes trivially testable in isolation. Swapping infrastructure (e.g., Postgres for an Event Store) does not require changing domain logic.
- **Cons:** More boilerplate code (interfaces and mapping layers) is required.

## Alternatives Considered
- **Layered Architecture:** Rejected because it often leads to domain logic bleeding into the database layer via ORM annotations.
