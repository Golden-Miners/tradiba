# Tradiba v4.0 Architecture

Tradiba is an enterprise-grade algorithmic trading platform built on an event-driven architecture, featuring institutional-grade execution, risk management, and AI copilot integration.

## Core Components
- **API Gateway (FastAPI):** Exposes REST and WebSocket endpoints for the trading terminal and integration clients.
- **Event Store:** Captures all market data, orders, executions, and system events for replay and auditing.
- **Strategy Engine:** Executes user-defined Python strategies against live or simulated market data streams.
- **Risk Manager:** Enforces pre-trade and post-trade exposure limits dynamically.
- **Frontend Terminal (React):** A Bloomberg/TradingView style interface for operators and researchers.

## Data Flow
Market Data -> Broker Adapters -> Event Bus (Redis/Kafka) -> Strategy Engine -> Execution Service -> Broker Adapters
