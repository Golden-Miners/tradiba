# Broker Outage Runbook

## Symptoms
- Elevated latency on order submissions.
- Websocket disconnection events from broker integrations.
- P&L and Open Positions failing to sync.

## Diagnosis
1. Check the Operational Dashboard for API Latency.
2. Verify broker status on their respective status pages (e.g., status.binance.com).
3. Check `logs/broker_api.log` for HTTP 5xx errors or timeout exceptions.

## Recovery Steps
1. **Pause Strategy Execution:** Disable all active algorithmic trading strategies via the Admin Console to prevent misfired orders.
2. **Switch to Fallback Data Provider:** If market data is affected, failover to the secondary data provider (e.g., switch from MT5 to generic WebSocket feed).
3. **Notify Users:** Broadcast a `warning` level system alert through the Notification Engine.

## Escalation
- If outage exceeds 15 minutes, escalate to the `Operations Lead`.
- If outage exceeds 1 hour, escalate to `Engineering Manager` for failover strategy.

## Validation Checklist
- [ ] Broker API returns HTTP 200 consistently.
- [ ] Test orders execute successfully in paper trading environment.
- [ ] Re-enable algorithmic trading.
