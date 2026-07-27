# Security Incident Runbook

## Symptoms
- Multiple authentication failures from single IP.
- Unauthorized access attempts logged in audit trails.
- Unexpected configuration changes.
- Rate limit triggers across multiple endpoints simultaneously.

## Diagnosis
1. Check WAF (Web Application Firewall) logs for blocked requests.
2. Review active sessions in the Admin Console.
3. Check `logs/security.log` for unusual activity patterns.

## Recovery Steps
1. **Isolate Affected Tenant/User:** Use Admin Console to suspend compromised accounts.
2. **Revoke API Keys:** Invalidate active API keys and JWT tokens for affected entities.
3. **Block IP:** Add malicious IP addresses to the WAF blocklist.
4. **Trigger Incident Response:** Create a SEV1 incident in the Incident Management system.

## Escalation
- Immediate escalation to `Security Officer (CISO)` and `Operations Lead`.

## Validation Checklist
- [ ] Unauthorized access is blocked.
- [ ] No further malicious activity in logs.
- [ ] Postmortem report drafted in `operations/incidents`.
