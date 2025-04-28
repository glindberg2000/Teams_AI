# LedgerFlow – Project Overview
_Last updated: 2025-04-24_

## Mission
Provide a **self-hosted, safety-first bookkeeping platform** that ingests PDFs & CSVs, classifies payees, and produces tax-ready reports – all running in Docker with bullet-proof backup / restore.

## Milestones (Q2 2025)

| ID | Goal | Target | Owner |
|----|------|--------|-------|
| M-01 | **Prod bootstrap** using image `v20250424`, first backup succeeds | 30 Apr | PM-Guardian |
| M-02 | Hourly backup container & size-check alerting in prod | 05 May | DB Guardian |
| M-03 | Restore-smoke job wired into CI / PR gate | 09 May | Reviewer + DB Guardian |
| M-04 | PDF parser integrated into Django `documents` app | 15 May | Full-Stack Dev |
| M-05 | Payee-classifier baseline accuracy ≥ 75 % | 22 May | Task-force |
| M-06 | Minimal UI dashboard (React + Tailwind) deployed | 31 May | UI Specialist |

> **Definition of done** for every milestone: _code merged → CI green → backup + restore smoke-test pass → docs updated_.

## Repositories

| Repo | Purpose | Default Branch |
|------|---------|----------------|
| **ledgerflow-app** | Django backend, React frontend, domain logic | `main` |
| **ledgerflow-infra** | Dockerfiles, docker-compose, GH Actions, Helm (future) | `main` |
| **ledgerflow-archive** | Long-term backups (iCloud mount) – _not public_ | n/a |

## Non-Code Assets

* **iCloudLedger** → `~/iCloudLedger` symlink (backups & gold-copy envs)  
* Docker volumes  
  * `ledger_dev_db_data` (protected)  
  * `ledger_prod_db_data` (protected)
* Slack workspace **ledgerflow-dev**  
* PagerDuty service **LedgerFlow-Critical** 