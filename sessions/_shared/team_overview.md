# LedgerFlow Windsurf Team

| Slack Handle | Windsurf Session | Role | TZ / Typical Hours |
|--------------|------------------|------|--------------------|
| @ledgerflow-guardian | **pm-guardian** | Release captain, safety gate | PST (08-16) |
| @ledgerflow-dev | **full-stack-dev** | Django + React implementation | EST (09-17) |
| @ledgerflow-db | **db-guardian** | PostgreSQL, backups, migrations | PST (10-18) |
| @ledgerflow-review | **reviewer** | PR audit & CI enforcement | CET (async) |
| @ledgerflow-task | **task-force** | Short-lived spikes / experiments | rotates |

## Escalation

1. **Prod down / data-loss risk** → page **@ledgerflow-guardian**  
2. **DB corruption / backup failure** → **@ledgerflow-db**  
3. **CI red on `main`** → **@ledgerflow-review** + #ledgerflow-ops

## Communication Channels

| Channel | Purpose |
|---------|---------|
| #ledgerflow-ops | Deploys, infra alerts |
| #ledgerflow-dev | Daily dev chatter |
| #ledgerflow-db | Schema / migration discussions |
| #ledgerflow-reviews | PR notifications |
| #ledgerflow-alerts | PagerDuty → Slack sink | 