# 0003 - Domain Boundaries

## Context
Tradiba encapsulates multiple business capabilities: trading, research, operations, AIOps, analytics, and control plane. Without explicit boundaries, these domains can become a "Big Ball of Mud."

## Decision
We define strict Bounded Contexts for each major capability. Each context owns its database schemas, domain models, and application services. Cross-context communication must occur either via Domain Events or explicit Anti-Corruption Layers (ACL). 

A Shared Kernel will exist but will be strictly limited to foundational primitives (Identifiers, Result types, Money value objects).

## Consequences
- **Pros:** Teams can work independently. Concepts like "Order" can exist differently in "Trading" vs "Analytics".
- **Cons:** Requires mapping between bounded contexts when communicating.

## Alternatives Considered
- **Shared Enterprise Data Model:** Rejected. Trying to define a single canonical "Order" that satisfies execution, analytics, and UI invariably fails in large systems.
