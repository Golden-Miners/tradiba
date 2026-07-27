# Database Failure Runbook

## Symptoms
- API returns HTTP 500 across most endpoints.
- Read/Write timeout errors in application logs.
- Dashboards fail to load historical data.

## Diagnosis
1. Check database CPU and memory utilization on monitoring dashboard.
2. Verify if connection pool is exhausted (`PoolTimeoutError`).
3. Attempt a manual connection to the database instance using a CLI client.

## Recovery Steps
1. **Restart Application Pool:** If it's a connection exhaustion issue, restart the API container to reset connection pools.
2. **Database Failover:** If the primary database node is unresponsive, trigger a manual failover to the standby replica.
3. **Restore from Backup:** If data corruption is detected, invoke `scripts/restore_db.py` using the latest verified backup from `operations/backups`.

## Escalation
- Immediate escalation to `Database Administrator (DBA)` and `Infrastructure Lead`.

## Validation Checklist
- [ ] Read queries execute successfully.
- [ ] Write queries execute successfully.
- [ ] Data integrity check passes.
- [ ] Application health check endpoint reports healthy.
