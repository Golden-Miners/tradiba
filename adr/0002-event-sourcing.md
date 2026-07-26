# 0002 - Event Sourcing

## Context
In trading systems, the historical sequence of state changes is often as important as the current state itself. We need a reliable audit trail for compliance, and a way to reconstruct state for debugging or backtesting.

## Decision
While the entire platform will not necessarily use Event Sourcing, critical aggregates (such as `Order`, `Position`, and `Account`) will emit Domain Events for every meaningful state change. These events will be the primary mechanism for cross-domain communication.

## Consequences
- **Pros:** Decouples bounded contexts. Perfect audit log. Enables time-travel debugging.
- **Cons:** Eventual consistency becomes the norm across contexts. Requires managing event schemas and versioning.

## Alternatives Considered
- **Direct RPC (gRPC/REST) between domains:** Rejected due to tight temporal coupling.
