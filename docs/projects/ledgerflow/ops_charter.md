# LedgerFlow Ops Charter (Windsurf Setup)

## TL;DR

Start lean:
- 4 **core Windsurf sessions** + 1 **"on-demand" Taskforce** slot.
- Everything else spins up temporarily based on backlog needs.
- Existing sessions map neatly into this.

---

## Core Windsurf Sessions

| Slot | Slack Handle | Primary Scope | Why We Need It Day-1 |
|:---|:---|:---|:---|
| 1 | @ledgerflow-pm | • Enforce backup/wrapper rules<br>• Own CI & prod roll-outs<br>• Merge authority | Central command brain. |
| 2 | @ledgerflow-dev | • Django API<br>• React/Tailwind UI<br>• Glue code for parsers/classifier | Unified builder for full stack in small codebase phase. |
| 3 | @ledgerflow-db | • Postgres schema & fixtures<br>• Backup/restore scripts<br>• Performance tuning | Dedicated watchdog to prevent past data loss issues. |
| 4 | @ledgerflow-review | • Automated & manual PR review<br>• Lint/tests/docs gate | Maintain high velocity without sacrificing quality. |
| 5 | @ledgerflow-taskforce | • Temporary specialist focus (PDF/NLP/Reporting/Ops) | Only when large specialist tasks appear. |

---

## Why Trim from 9-Agent Draft?

| Issue | Impact | Lean Model Mitigation |
|:---|:---|:---|
| Coordination overhead (9 IDs × 9 channels) | PM wastes time routing/conflict-resolving. | Only 4 standing channels; clean handoffs. |
| Resource contention (shared files) | Merge conflicts, race conditions. | Single Full-Stack Dev owns code; Reviewer + PM-Guardian catch issues. |
| Premature specialization | Wasted work on unstable foundations. | Taskforce spins up only when feature area is stable. |
| Duplicate authority (merge/deploy) | Confusion over final authority. | Guardian holds prod switch; Reviewer signs off; DB Guardian can veto on data risk. |

---

## Coverage Check

| Capability | Covered by | Notes |
|:---|:---|:---|
| Backups & Volume Safety | DB Guardian ⚙ PM-Guardian | Two-person rule on prod restores. |
| CI/CD & Docker | PM-Guardian | GitHub Actions, bootstrap checks. |
| Application code (API, parsers, UI) | Full-Stack Dev | Makefile workflow; Taskforce for heavy lifts. |
| Code Quality Gate | Reviewer | Linting, secret scan, log smoke-tests required. |
| Specialist spikes (PDF, NLP, reports) | Taskforce slot | Temporary container with limited access. |

---

## Suggested Initial Channel Matrix

| Channel | Purpose | Members |
|:---|:---|:---|
| #ledgerflow-dev | Day-to-day commits, stand-ups | Full-Stack Dev, Reviewer, PM Guardian |
| #ledgerflow-db | Backup alerts, migrations | DB Guardian, PM Guardian |
| #ledgerflow-review | PR notifications, reviews | Reviewer, PM Guardian |
| #ledgerflow-ops | CI status, deploys | PM Guardian, DB Guardian |
| #ledgerflow-taskforce (private) | Specialist work (when needed) | Taskforce + Full-Stack Dev |

---

## Next Steps

1. **Rename existing sessions**:
    - Architect ➔ ledgerflow-pm
    - CoderDev ➔ ledgerflow-dev
    - Reviewer ➔ ledgerflow-review
2. **Create new Windsurf container** for ledgerflow-db.
3. **Prepare Taskforce template** (ledgerflow-taskforce) but keep dormant.
4. **Update Slack user mappings** in PM's Name-ID cache.
5. **Publish this document** as `docs/ops_charter.md` for all AI and humans to follow.

---

# End of Charter 🌐

