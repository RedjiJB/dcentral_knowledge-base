# DC-DION-PLATFORM-TECHNICAL-ARCHITECTURE-RECONCILED-001 — DION Platform Technical Architecture & Scaffolding, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `dion-platform-technical-architecture` (5 docs).

## Current understanding

Five documents specifying how to actually build the DION platform's codebase — repo scaffolding, dev
environment, CI/CD, infrastructure-as-code, database schema, API spec, testing, security, monitoring,
and frontend components. Two of the five (the Implementation Guide and the Complete Technical
Architecture doc) are alternate, independently-drafted scaffolds for the same monorepo that disagree on
several concrete technology choices; the other three add genuinely new, non-overlapping detail
(dev-environment config files, testing/security/monitoring depth, and actual frontend component code).

**DION Platform: Complete Technical Architecture & Implementation Guide (incorporated):** the most
detailed of the two scaffolds — an Nx monorepo layout (apps/services/ai-services/edge-software/
infrastructure/libs/tools/docs/tests), a technology-stack table with stated rationale per choice
(Node.js/TypeScript backend, Python for AI/ML, Rust for performance-critical/edge code, PostgreSQL 15+/
Redis/Neo4j/Elasticsearch/ClickHouse/MinIO/IPFS for storage, Kubernetes/Istio/Kong/NATS/Prometheus for
infra), webpack as the web-dashboard's build tool, GitLab CI + ArgoCD for CI/CD, and Terraform/Helm for
IaC [Architecture Overview, Technology Stack, Repository Structure]. A full local-development Docker
Compose stack, a GitLab CI pipeline (lint → test → build → security-scan → deploy-staging →
integration-tests → deploy-production, with blue-green production deployment), a detailed Terraform GKE
configuration (3-tier node pools including a tainted GPU pool), a complete PostgreSQL schema (users,
nodes, operators, intelligence, tasks, task_assignments, task_submissions, emergency_alerts,
emergency_mobilizations, blockchain_transactions, performance_metrics, audit_logs, with full index and
trigger definitions), and a complete OpenAPI 3.0.3 specification for the intelligence/operator/task/
emergency endpoint families [Development Environment through API Design].

**DION Platform - Complete Technical Architecture (incorporated):** an alternate, less detailed scaffold
for the same platform, specifying **Vite** (not webpack) as the build tool, **Redux Toolkit + RTK
Query** for state management, **Tailwind CSS + Headless UI** for styling, **GitHub Actions** (not
GitLab CI) for CI/CD, and Express.js + Fastify explicitly named as the backend framework pairing
[Technology Stack]. Gives a shorter, less-indexed version of the same repository structure and
PostgreSQL schema as the Implementation Guide (matching table names and core columns, omitting most
indexes and the six additional tables the Implementation Guide includes), a condensed REST/GraphQL/
WebSocket API surface, DID-auth and data-privacy-level service sketches, and a shorter Kubernetes/
monitoring section [Repository Structure through Deployment Architecture].

**DION Platform - Development Setup & Configuration (incorporated):** concrete configuration files
implementing the scaffold — a Docker Compose file adding ClickHouse and Kong (absent from the other two
docs' compose examples) alongside Postgres/Redis/Neo4j/Elasticsearch/NATS/MinIO/Prometheus/Grafana, a
monorepo root `package.json` with Nx workspace scripts, an `nx.json` **explicitly configuring the React
application generator's bundler as `"vite"`** — confirming this document sides with the Complete
Technical Architecture doc's build-tool choice, not the Implementation Guide's webpack — and a
`tsconfig.base.json` with the monorepo's shared-library path aliases. Its CI/CD section is **GitHub
Actions**, again matching the Complete Technical Architecture doc rather than the Implementation Guide's
GitLab CI.

**DION Platform - Complete Technical Architecture Continuation (incorporated):** additive depth not
present in either scaffold document — a full testing-pyramid specification (80% unit-coverage
threshold, Jest/pytest/cargo test per language, Playwright E2E, k6 load testing at a 10,000 RPS/1,000
concurrent-user target, OWASP ZAP/Nessus/Qualys vulnerability scanning plus a quarterly manual
pentest and bug-bounty programme) with a worked integration-test example [Testing Strategy]. A
zero-trust security architecture (DID + FIDO2/WebAuthn + HSM authentication, 15-minute JWT expiry,
ABAC authorization enforced at four separate points — API gateway, service mesh, PostgreSQL RLS, and
smart-contract modifiers — AES-256-GCM at rest via HashiCorp Vault, TLS 1.3 + mTLS in transit) with a
worked `SecurityMonitor` class implementing threat-intelligence request scoring and data-exfiltration
detection [Security Implementation Details]. A detailed Prometheus scrape configuration (per-service
intervals, Consul service discovery for edge nodes) and custom-metrics implementation sketch
[Monitoring and Observability].

**DION Platform - Frontend Components Structure (incorporated):** actual React component code for the
web dashboard (Dashboard, IntelligenceFeed) built on **Material UI (`@mui/material`)** components (Grid,
Paper, Typography, Chip) and plain `react-redux` (`useSelector`/`useDispatch` against a `RootState`),
**not** the Redux Toolkit + RTK Query state layer or the Tailwind CSS + Headless UI styling stack the
Complete Technical Architecture document's stack list specifies — a third, unreconciled divergence in
the frontend tooling choice across this topic's documents.

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Nx monorepo structure, tech-stack rationale table, webpack/GitLab CI choice | Implementation Guide, Architecture Overview / Technology Stack | incorporated — see tension below |
| Local dev Docker Compose, GitLab CI pipeline, Terraform GKE config | Implementation Guide, Development Environment / CI/CD / Infrastructure as Code | incorporated |
| Full PostgreSQL schema (12 tables, indexes, triggers) | Implementation Guide, Database Schema and Migrations | incorporated (condensed, non-conflicting subset restated in Complete Technical Architecture doc) |
| Complete OpenAPI 3.0.3 specification | Implementation Guide, API Design and Documentation | incorporated |
| Alternate scaffold: Vite/RTK Query/Tailwind+Headless UI/GitHub Actions stack | Complete Technical Architecture doc, Technology Stack | incorporated — see tension below |
| Condensed repo structure, DB schema, API surface, DID-auth/privacy service sketches | Complete Technical Architecture doc, Repository Structure through Security Implementation | incorporated (consistent subset of the Implementation Guide's fuller detail) |
| Docker Compose with ClickHouse/Kong, Nx config confirming Vite bundler, GitHub Actions CI | Development Setup & Configuration | incorporated — confirms the Complete Technical Architecture doc's build-tool/CI choice, contradicting the Implementation Guide |
| tsconfig path aliases and monorepo root package.json | Development Setup & Configuration | incorporated |
| Testing pyramid and worked integration-test example | Continuation doc, Testing Strategy & Implementation | incorporated |
| Zero-trust security architecture and SecurityMonitor implementation | Continuation doc, Security Implementation Details | incorporated |
| Prometheus scrape config and custom metrics | Continuation doc, Monitoring and Observability | incorporated |
| Dashboard and IntelligenceFeed component code (Material UI + plain react-redux) | Frontend Components Structure | incorporated — see tension below |

## Unresolved tensions

**Three of this topic's five documents disagree, pairwise, on core frontend/CI/CD tooling for what is
presented as one platform, with no document acknowledging the others' choices.** (1) Build tool: the
Implementation Guide specifies webpack (`vite.config.ts` is absent; a `webpack.config.js` is listed for
web-dashboard), while both the Complete Technical Architecture doc and the Development Setup &
Configuration doc specify Vite — the latter's `nx.json` explicitly sets `"bundler": "vite"`. (2) CI/CD
system: the Implementation Guide's pipeline is GitLab CI (`.gitlab-ci.yml`, stages including
`deploy-staging`/`deploy-production` against Kubernetes contexts), while the Complete Technical
Architecture doc and the Development Setup & Configuration doc both specify GitHub Actions
(`.github/workflows/ci.yml`). (3) Frontend state/styling stack: the Complete Technical Architecture
doc's own stack list names Redux Toolkit + RTK Query and Tailwind CSS + Headless UI, but the Frontend
Components Structure document's actual component code uses Material UI (`@mui/material`) components and
plain `react-redux` hooks — not RTK Query, not Tailwind. Attempted reconciliation: none of the five
documents cross-references or supersedes another on any of these three points; this reads as
independently-drafted architecture passes that were never reconciled into one canonical stack, rather
than a stated intentional per-environment or per-app variation. Left unresolved rather than picking one
stack as authoritative — a future dedup/architecture-decision pass should determine which (if any) of
these choices is the one actually implemented.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/meta/platform-scaffolding/Bounty/DION-Platform-Complete-Technical-Architecture-Implementation-Guide-md.md`
- `knowledge-base/d-central/meta/platform-scaffolding/Bounty/DION-Platform-Complete-Technical-Architecture-md.md`
- `knowledge-base/d-central/meta/platform-scaffolding/Bounty/DION-Platform-Development-Setup-Configuration-txt.md`
- `knowledge-base/d-central/security/Bounty/DION-Platform-Complete-Technical-Architecture-Continuation-md.md`
- `knowledge-base/d-central/meta/platform-scaffolding/Bounty/DION-Platform-Frontend-Components-Structure-txt.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/meta/platform-scaffolding/Bounty/DION-Platform-Complete-Technical-Architecture-Implementation-Guide-md.md,
  knowledge-base/d-central/meta/platform-scaffolding/Bounty/DION-Platform-Complete-Technical-Architecture-md.md,
  knowledge-base/d-central/meta/platform-scaffolding/Bounty/DION-Platform-Development-Setup-Configuration-txt.md,
  knowledge-base/d-central/security/Bounty/DION-Platform-Complete-Technical-Architecture-Continuation-md.md,
  knowledge-base/d-central/meta/platform-scaffolding/Bounty/DION-Platform-Frontend-Components-Structure-txt.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

**Referenced by:**
- [[DC-IHOSE-ARCHITECTURE-DEPLOYMENT-RECONCILED-001|DC-IHOSE-ARCHITECTURE-DEPLOYMENT-RECONCILED-001 — IHOSE Architecture & OpenVision Deployment, Consolidated (v1, generated 2026-09-05)]]

<!-- AUTO-GENERATED RELATED END -->
