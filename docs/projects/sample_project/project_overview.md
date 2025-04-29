# LedgerFlow – End-to-End Project Description
_A living primer for every Windsurf session – last updated: 2025-04-24_

## 1. Why LedgerFlow Exists
Small-business owners and freelancers juggle banks, credit cards, PDFs and CSVs.  
LedgerFlow ingests **bank statements + receipts**, classifies every payee, and spits out **tax-ready reports** – all on-prem (or self-hosted) so data never leaves the owner’s laptop.

## 2. High-Level Workflow
```mermaid
graph LR
    subgraph Ingestion
        A[PDF / CSV Upload] --> B[Parser Service]
    end
    subgraph Core DB
        C[(PostgreSQL)]
    end
    subgraph Processing
        B --> C
        C --> D[Payee Classifier]
        D --> C
    end
    subgraph Reporting
        C --> E[Tax Report Builder]
        E --> F[PDF / XLSX Export]
    end
    subgraph UI
        B --> G[React Dashboard] <-- C
        D --> G
        E --> G
    end

(see original for numbered description)

3. Tech Stack at a Glance

Layer	Tech	Notes
Containers	Docker Compose (dev + prod)	Wrapper ledger_docker enforces safety
Backend	Python 3.12, Django 5.2, DRF	Hot-reload in dev
DB	PostgreSQL 17.4	Hourly + daily backups, restore-smoke CI
AI/NLP	sentence-transformers, scikit-learn	Local embeddings – no external API calls
Front-end	React + Tailwind + shadcn/ui	Served by Django templates or Vite build
CI/CD	GitHub Actions	Lint → test → build → restore-smoke
Backups	iCloud mount ~/iCloudLedger	Size check > 10 KB, integrity test

Dev vs Prod Config
	•	Dev runs on http://localhost:9001 (make dev, volume mounts, DEBUG on).
	•	Prod container listens on http://localhost:9000 (or behind reverse-proxy); volumes are protected, DEBUG off.
	•	Envs are separated by .env.dev / .env.prod, with gold-copy templates and guard hooks preventing secret leakage.

(rest unchanged – milestones, repos, safety model, PR “definition of done” etc.)

⸻

Company & Environment
	•	Company / client name: LedgerFlow
	•	Production domain / hostnames: currently local-only – http://localhost:9000 (prod) and http://localhost:9001 (dev)
	•	Slack workspace URL: MCP

