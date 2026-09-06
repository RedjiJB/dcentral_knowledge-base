---
source_project: Bounty
source_project_uuid: 0198b52e-0516-768e-b6d4-182ebfca6ef0
doc_uuid: 2f9f74d3-4d27-479a-be34-3ede80300b20
original_filename: DION Platform: Complete Technical Architecture & Implementation Guide.md
created_at: 2025-08-23T15:21:06.987967+00:00
content_hash: 7b56011ad3ee
topic: dion-platform-technical-architecture
consolidated_into: docs/DC-DION-PLATFORM-TECHNICAL-ARCHITECTURE-RECONCILED-001.md
---

# DION Platform: Complete Technical Architecture & Implementation Guide

## Architecture Overview

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ 🌐 FRONTEND LAYER                                               │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │   Web App   │ │ Mobile App  │ │ Operator    │ │ Admin       │ │
│ │  (React)    │ │(React Nat.) │ │ Dashboard   │ │ Portal      │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│ 🔗 API GATEWAY LAYER                                           │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Kong API Gateway + GraphQL Federation + WebSocket Hub      │ │
│ │ Rate Limiting • Auth • Monitoring • Load Balancing         │ │
│ └─────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│ 🚀 APPLICATION SERVICES LAYER                                  │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │Intelligence │ │  Operator   │ │ Emergency   │ │   User      │ │
│ │   Service   │ │   Service   │ │  Response   │ │  Service    │ │
│ │  (Node.js)  │ │  (Node.js)  │ │ (Node.js)   │ │ (Node.js)   │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ Notification│ │   Training  │ │ Blockchain  │ │   AI/ML     │ │
│ │   Service   │ │   Service   │ │   Service   │ │  Service    │ │
│ │  (Node.js)  │ │  (Node.js)  │ │ (Rust/Go)   │ │  (Python)   │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│ 🧠 AI & PROCESSING LAYER                                       │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │   GraphRAG  │ │  Federated  │ │Multi-INT    │ │  Real-time  │ │
│ │   Engine    │ │  Learning   │ │ Correlation │ │ Processing  │ │
│ │  (Python)   │ │  (Python)   │ │  (Python)   │ │   (Rust)    │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│ 🔐 DATA & STORAGE LAYER                                        │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ PostgreSQL  │ │   Redis     │ │    Neo4j    │ │    IPFS     │ │
│ │  (Primary)  │ │   (Cache)   │ │   (Graph)   │ │ (Content)   │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ ClickHouse  │ │ Elasticsearch│ │   MinIO     │ │ Blockchain  │ │
│ │ (Analytics) │ │   (Search)   │ │ (Objects)   │ │  (State)    │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│ 🌐 INFRASTRUCTURE LAYER                                        │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ Kubernetes  │ │    NATS     │ │ Prometheus  │ │   Istio     │ │
│ │Orchestration│ │ (Messaging) │ │(Monitoring) │ │ (Service    │ │
│ │             │ │             │ │             │ │   Mesh)     │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Technology Stack Selection

### Core Technologies with Rationale

```yaml
primary_languages:
  backend_services: "Node.js (TypeScript)"
  rationale: "Excellent async I/O, large ecosystem, team familiarity"
  
  ai_ml_services: "Python"
  rationale: "Best ML ecosystem, extensive libraries, research compatibility"
  
  blockchain_smart_contracts: "Solidity + Rust"
  rationale: "Solidity for Ethereum compatibility, Rust for performance-critical components"
  
  high_performance_services: "Rust"
  rationale: "Memory safety, performance for real-time processing"
  
  frontend: "TypeScript + React"
  rationale: "Type safety, component reusability, large talent pool"

databases_storage:
  primary_database: "PostgreSQL 15+"
  rationale: "ACID compliance, JSON support, spatial extensions, mature"
  
  cache_session: "Redis 7+"
  rationale: "High performance, pub/sub, stream processing"
  
  graph_database: "Neo4j"
  rationale: "Intelligence correlation analysis, relationship queries"
  
  search_engine: "Elasticsearch 8+"
  rationale: "Full-text search, real-time analytics, scalability"
  
  time_series: "ClickHouse"
  rationale: "Analytics, monitoring data, high-performance aggregations"
  
  object_storage: "MinIO (S3-compatible)"
  rationale: "Self-hosted, compatible with cloud providers"
  
  content_addressing: "IPFS"
  rationale: "Decentralized storage, content verification"

infrastructure_orchestration:
  container_orchestration: "Kubernetes"
  rationale: "Industry standard, multi-cloud, extensive ecosystem"
  
  service_mesh: "Istio"
  rationale: "Traffic management, security, observability"
  
  api_gateway: "Kong"
  rationale: "Performance, plugins, enterprise features"
  
  message_queue: "NATS"
  rationale: "High performance, built-in clustering, simplicity"
  
  monitoring: "Prometheus + Grafana"
  rationale: "Cloud-native standard, extensive integrations"

development_tools:
  version_control: "Git + GitLab"
  rationale: "Distributed development, integrated CI/CD, self-hosted option"
  
  ci_cd: "GitLab CI + ArgoCD"
  rationale: "GitOps workflow, automated deployments"
  
  infrastructure_as_code: "Terraform + Helm"
  rationale: "Multi-cloud support, Kubernetes integration"
  
  package_management: "npm/yarn (Node.js), pip/poetry (Python), cargo (Rust)"
  rationale: "Standard tools for each ecosystem"
```

## Repository Structure

### Monorepo Architecture with Nx

```
dion-platform/                                 # Root monorepo
├── .github/                                   # GitHub workflows and templates
│   ├── workflows/                            # CI/CD workflows
│   │   ├── ci.yml                           # Continuous integration
│   │   ├── cd-staging.yml                   # Staging deployment
│   │   ├── cd-production.yml               # Production deployment
│   │   └── security-scan.yml               # Security scanning
│   ├── ISSUE_TEMPLATE/                      # Issue templates
│   └── pull_request_template.md            # PR template
│
├── apps/                                      # Applications
│   ├── web-dashboard/                        # Main web application
│   │   ├── src/
│   │   │   ├── components/                  # Reusable UI components
│   │   │   │   ├── intelligence/           # Intelligence-specific components
│   │   │   │   ├── operators/              # Operator management components
│   │   │   │   ├── emergency/              # Emergency response components
│   │   │   │   └── common/                 # Shared components
│   │   │   ├── pages/                      # Page components
│   │   │   ├── hooks/                      # Custom React hooks
│   │   │   ├── services/                   # API clients
│   │   │   ├── utils/                      # Utility functions
│   │   │   ├── types/                      # TypeScript type definitions
│   │   │   └── constants/                  # Application constants
│   │   ├── public/                         # Static assets
│   │   ├── package.json
│   │   └── webpack.config.js
│   │
│   ├── mobile-operator/                      # React Native operator app
│   │   ├── src/
│   │   │   ├── screens/                    # App screens
│   │   │   ├── components/                 # Mobile components
│   │   │   ├── navigation/                 # Navigation configuration
│   │   │   ├── services/                   # API and background services
│   │   │   ├── hooks/                      # Custom hooks
│   │   │   ├── utils/                      # Utility functions
│   │   │   └── types/                      # TypeScript types
│   │   ├── android/                        # Android-specific code
│   │   ├── ios/                           # iOS-specific code
│   │   └── package.json
│   │
│   ├── admin-portal/                        # Administrative interface
│   │   ├── src/
│   │   │   ├── modules/                    # Feature modules
│   │   │   │   ├── user-management/
│   │   │   │   ├── system-monitoring/
│   │   │   │   ├── content-moderation/
│   │   │   │   └── analytics/
│   │   │   └── shared/                     # Shared admin components
│   │   └── package.json
│   │
│   └── edge-node-interface/                 # Edge node management UI
│       ├── src/
│       │   ├── components/
│       │   └── services/
│       └── package.json
│
├── services/                                 # Backend microservices
│   ├── intelligence-service/               # Intelligence processing
│   │   ├── src/
│   │   │   ├── controllers/               # HTTP controllers
│   │   │   │   ├── intelligence.controller.ts
│   │   │   │   ├── verification.controller.ts
│   │   │   │   └── correlation.controller.ts
│   │   │   ├── services/                  # Business logic
│   │   │   │   ├── intelligence/
│   │   │   │   │   ├── osint.service.ts
│   │   │   │   │   ├── imint.service.ts
│   │   │   │   │   ├── sigint.service.ts
│   │   │   │   │   └── correlation.service.ts
│   │   │   │   ├── verification.service.ts
│   │   │   │   └── quality.service.ts
│   │   │   ├── models/                    # Data models
│   │   │   │   ├── intelligence.model.ts
│   │   │   │   ├── source.model.ts
│   │   │   │   └── verification.model.ts
│   │   │   ├── middleware/                # Express middleware
│   │   │   ├── utils/                     # Utility functions
│   │   │   ├── config/                    # Configuration
│   │   │   └── types/                     # TypeScript types
│   │   ├── tests/                         # Unit and integration tests
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   └── package.json
│   │
│   ├── operator-service/                   # Operator management
│   │   ├── src/
│   │   │   ├── controllers/
│   │   │   │   ├── registration.controller.ts
│   │   │   │   ├── deployment.controller.ts
│   │   │   │   ├── training.controller.ts
│   │   │   │   └── performance.controller.ts
│   │   │   ├── services/
│   │   │   │   ├── matching/              # Task-operator matching
│   │   │   │   ├── deployment/            # Dynamic deployment
│   │   │   │   ├── training/              # Training management
│   │   │   │   └── performance/           # Performance tracking
│   │   │   ├── models/
│   │   │   └── utils/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── package.json
│   │
│   ├── emergency-response-service/         # Emergency coordination
│   │   ├── src/
│   │   │   ├── controllers/
│   │   │   │   ├── alerts.controller.ts
│   │   │   │   ├── mobilization.controller.ts
│   │   │   │   └── coordination.controller.ts
│   │   │   ├── services/
│   │   │   │   ├── alert-processing/
│   │   │   │   ├── resource-mobilization/
│   │   │   │   ├── real-time-coordination/
│   │   │   │   └── external-integration/
│   │   │   └── models/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── package.json
│   │
│   ├── user-service/                       # User authentication & authorization
│   │   ├── src/
│   │   │   ├── controllers/
│   │   │   │   ├── auth.controller.ts
│   │   │   │   ├── profile.controller.ts
│   │   │   │   └── permissions.controller.ts
│   │   │   ├── services/
│   │   │   │   ├── authentication/
│   │   │   │   ├── authorization/
│   │   │   │   ├── did-management/
│   │   │   │   └── credential-verification/
│   │   │   └── models/
│   │   └── package.json
│   │
│   ├── notification-service/               # Real-time notifications
│   │   ├── src/
│   │   │   ├── controllers/
│   │   │   ├── services/
│   │   │   │   ├── websocket/
│   │   │   │   ├── push-notifications/
│   │   │   │   ├── email/
│   │   │   │   └── sms/
│   │   │   └── models/
│   │   └── package.json
│   │
│   ├── blockchain-service/                 # Blockchain integration
│   │   ├── src/
│   │   │   ├── controllers/
│   │   │   ├── services/
│   │   │   │   ├── smart-contracts/
│   │   │   │   ├── token-management/
│   │   │   │   ├── reputation-system/
│   │   │   │   └── dao-governance/
│   │   │   └── contracts/                 # Smart contract source code
│   │   │       ├── Registry.sol
│   │   │       ├── BountySystem.sol
│   │   │       ├── Governance.sol
│   │   │       └── TokenEconomics.sol
│   │   └── package.json
│   │
│   └── training-service/                   # Training and certification
│       ├── src/
│       │   ├── controllers/
│       │   ├── services/
│       │   │   ├── curriculum/
│       │   │   ├── assessment/
│       │   │   ├── certification/
│       │   │   └── adaptive-learning/
│       │   └── models/
│       └── package.json
│
├── ai-services/                             # AI and ML services (Python)
│   ├── graphrag-engine/                    # GraphRAG implementation
│   │   ├── src/
│   │   │   ├── api/                       # FastAPI application
│   │   │   │   ├── routes/
│   │   │   │   │   ├── query.py
│   │   │   │   │   ├── knowledge_graph.py
│   │   │   │   │   └── reasoning.py
│   │   │   │   └── main.py
│   │   │   ├── services/
│   │   │   │   ├── graph_construction/
│   │   │   │   │   ├── entity_extraction.py
│   │   │   │   │   ├── relationship_extraction.py
│   │   │   │   │   └── graph_builder.py
│   │   │   │   ├── query_processing/
│   │   │   │   │   ├── query_planner.py
│   │   │   │   │   ├── graph_traversal.py
│   │   │   │   │   └── semantic_search.py
│   │   │   │   └── reasoning/
│   │   │   │       ├── llm_integration.py
│   │   │   │       ├── answer_synthesis.py
│   │   │   │       └── confidence_scoring.py
│   │   │   ├── models/
│   │   │   │   ├── graph_models.py
│   │   │   │   ├── nlp_models.py
│   │   │   │   └── reasoning_models.py
│   │   │   ├── utils/
│   │   │   └── config/
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   │
│   ├── federated-learning/                 # Federated learning system
│   │   ├── src/
│   │   │   ├── api/
│   │   │   ├── services/
│   │   │   │   ├── aggregation/
│   │   │   │   ├── model_distribution/
│   │   │   │   ├── privacy_preservation/
│   │   │   │   └── performance_monitoring/
│   │   │   ├── models/
│   │   │   └── algorithms/
│   │   └── requirements.txt
│   │
│   ├── multi-int-processor/               # Multi-INT correlation
│   │   ├── src/
│   │   │   ├── api/
│   │   │   ├── processors/
│   │   │   │   ├── osint_processor.py
│   │   │   │   ├── imint_processor.py
│   │   │   │   ├── sigint_processor.py
│   │   │   │   └── correlation_engine.py
│   │   │   ├── models/
│   │   │   └── utils/
│   │   └── requirements.txt
│   │
│   └── real-time-processor/               # Real-time data processing (Rust)
│       ├── src/
│       │   ├── main.rs
│       │   ├── processors/
│       │   ├── models/
│       │   └── utils/
│       ├── Cargo.toml
│       └── Dockerfile
│
├── edge-software/                          # Edge node software
│   ├── edge-coordinator/                   # Main edge node coordinator
│   │   ├── src/
│   │   │   ├── main.rs
│   │   │   ├── collectors/                # Data collection modules
│   │   │   │   ├── camera.rs
│   │   │   │   ├── radio.rs
│   │   │   │   ├── environmental.rs
│   │   │   │   └── network.rs
│   │   │   ├── processors/               # On-device processing
│   │   │   │   ├── privacy.rs
│   │   │   │   ├── ai_inference.rs
│   │   │   │   └── compression.rs
│   │   │   ├── communication/            # Mesh networking
│   │   │   │   ├── mesh_protocol.rs
│   │   │   │   ├── sync.rs
│   │   │   │   └── security.rs
│   │   │   ├── storage/                  # Local storage
│   │   │   └── config/                   # Configuration management
│   │   ├── Cargo.toml
│   │   └── cross-compile.sh             # Cross-compilation scripts
│   │
│   ├── edge-installer/                     # Installation and setup tools
│   │   ├── install.sh                    # Installation script
│   │   ├── config/                       # Default configurations
│   │   └── systemd/                      # System service files
│   │
│   └── edge-updater/                      # OTA update system
│       ├── src/
│       └── update-scripts/
│
├── infrastructure/                         # Infrastructure as Code
│   ├── terraform/                          # Terraform configurations
│   │   ├── modules/                       # Reusable modules
│   │   │   ├── kubernetes-cluster/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   ├── database/
│   │   │   ├── storage/
│   │   │   ├── networking/
│   │   │   └── monitoring/
│   │   ├── environments/                  # Environment-specific configs
│   │   │   ├── development/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── terraform.tfvars
│   │   │   ├── staging/
│   │   │   └── production/
│   │   └── global/                        # Global resources
│   │
│   ├── kubernetes/                         # Kubernetes manifests
│   │   ├── base/                          # Base configurations
│   │   │   ├── namespaces/
│   │   │   ├── services/
│   │   │   │   ├── intelligence-service/
│   │   │   │   │   ├── deployment.yaml
│   │   │   │   │   ├── service.yaml
│   │   │   │   │   ├── configmap.yaml
│   │   │   │   │   └── secret.yaml
│   │   │   │   ├── operator-service/
│   │   │   │   └── emergency-response-service/
│   │   │   ├── databases/
│   │   │   │   ├── postgresql/
│   │   │   │   │   ├── statefulset.yaml
│   │   │   │   │   ├── service.yaml
│   │   │   │   │   ├── configmap.yaml
│   │   │   │   │   └── pvc.yaml
│   │   │   │   ├── redis/
│   │   │   │   ├── neo4j/
│   │   │   │   └── elasticsearch/
│   │   │   ├── monitoring/
│   │   │   │   ├── prometheus/
│   │   │   │   ├── grafana/
│   │   │   │   └── alertmanager/
│   │   │   └── ingress/
│   │   │       ├── api-gateway.yaml
│   │   │       └── web-ingress.yaml
│   │   ├── overlays/                      # Kustomize overlays
│   │   │   ├── development/
│   │   │   │   ├── kustomization.yaml
│   │   │   │   └── patches/
│   │   │   ├── staging/
│   │   │   └── production/
│   │   └── helm-charts/                   # Custom Helm charts
│   │       ├── dion-platform/
│   │       │   ├── Chart.yaml
│   │       │   ├── values.yaml
│   │       │   ├── templates/
│   │       │   └── charts/
│   │       └── edge-coordinator/
│   │
│   ├── docker/                            # Docker configurations
│   │   ├── base-images/                   # Base Docker images
│   │   │   ├── node-base/
│   │   │   │   └── Dockerfile
│   │   │   ├── python-base/
│   │   │   │   └── Dockerfile
│   │   │   └── rust-base/
│   │   │       └── Dockerfile
│   │   └── docker-compose/                # Local development
│   │       ├── development.yml
│   │       ├── testing.yml
│   │       └── monitoring.yml
│   │
│   ├── scripts/                           # Automation scripts
│   │   ├── setup/
│   │   │   ├── local-development.sh
│   │   │   ├── kubernetes-setup.sh
│   │   │   └── database-migration.sh
│   │   ├── deployment/
│   │   │   ├── deploy.sh
│   │   │   ├── rollback.sh
│   │   │   └── health-check.sh
│   │   ├── monitoring/
│   │   │   ├── backup.sh
│   │   │   └── performance-test.sh
│   │   └── security/
│   │       ├── security-scan.sh
│   │       └── certificate-renewal.sh
│   │
│   └── monitoring/                        # Monitoring configurations
│       ├── prometheus/
│       │   ├── prometheus.yml
│       │   ├── rules/
│       │   │   ├── intelligence.yml
│       │   │   ├── operators.yml
│       │   │   └── emergency.yml
│       │   └── alerts/
│       ├── grafana/
│       │   ├── dashboards/
│       │   │   ├── platform-overview.json
│       │   │   ├── intelligence-metrics.json
│       │   │   ├── operator-performance.json
│       │   │   └── system-health.json
│       │   └── datasources/
│       ├── jaeger/                        # Distributed tracing
│       │   └── jaeger-config.yml
│       └── logging/
│           ├── fluentd/
│           └── elasticsearch/
│
├── libs/                                   # Shared libraries
│   ├── shared-types/                      # TypeScript type definitions
│   │   ├── src/
│   │   │   ├── intelligence.types.ts
│   │   │   ├── operator.types.ts
│   │   │   ├── emergency.types.ts
│   │   │   ├── user.types.ts
│   │   │   └── api.types.ts
│   │   └── package.json
│   │
│   ├── shared-utils/                      # Common utilities
│   │   ├── src/
│   │   │   ├── validation/
│   │   │   ├── encryption/
│   │   │   ├── formatting/
│   │   │   └── constants/
│   │   └── package.json
│   │
│   ├── api-client/                        # API client library
│   │   ├── src/
│   │   │   ├── clients/
│   │   │   │   ├── intelligence.client.ts
│   │   │   │   ├── operator.client.ts
│   │   │   │   └── emergency.client.ts
│   │   │   ├── hooks/                     # React hooks for API calls
│   │   │   └── utils/
│   │   └── package.json
│   │
│   ├── ui-components/                     # Shared UI components
│   │   ├── src/
│   │   │   ├── components/
│   │   │   │   ├── forms/
│   │   │   │   ├── charts/
│   │   │   │   ├── maps/
│   │   │   │   └── layout/
│   │   │   ├── styles/
│   │   │   └── themes/
│   │   └── package.json
│   │
│   └── blockchain-integration/            # Blockchain utilities
│       ├── src/
│       │   ├── contracts/                 # Contract ABIs and interfaces
│       │   ├── providers/                 # Blockchain providers
│       │   └── utils/                     # Web3 utilities
│       └── package.json
│
├── tools/                                 # Development tools
│   ├── code-generators/                   # Code generation tools
│   │   ├── api-generator/                 # Generate API clients from OpenAPI
│   │   ├── type-generator/                # Generate types from schemas
│   │   └── component-generator/           # Generate React components
│   │
│   ├── testing/                           # Testing utilities
│   │   ├── test-data/                     # Test data generators
│   │   ├── mocks/                         # Mock services
│   │   └── fixtures/                      # Test fixtures
│   │
│   ├── deployment/                        # Deployment tools
│   │   ├── environment-sync/              # Environment synchronization
│   │   ├── database-migration/            # Database migration tools
│   │   └── config-management/             # Configuration management
│   │
│   └── monitoring/                        # Monitoring tools
│       ├── performance-testing/           # Load testing tools
│       ├── security-scanning/             # Security analysis tools
│       └── log-analysis/                  # Log analysis utilities
│
├── docs/                                  # Documentation
│   ├── architecture/                      # Architecture documentation
│   │   ├── system-design.md
│   │   ├── api-design.md
│   │   ├── database-schema.md
│   │   └── security-model.md
│   ├── deployment/                        # Deployment guides
│   │   ├── local-development.md
│   │   ├── staging-deployment.md
│   │   ├── production-deployment.md
│   │   └── edge-node-deployment.md
│   ├── api/                               # API documentation
│   │   ├── openapi.yaml
│   │   ├── graphql-schema.graphql
│   │   └── webhook-specs.md
│   ├── user-guides/                       # User documentation
│   │   ├── operator-guide.md
│   │   ├── admin-guide.md
│   │   └── integration-guide.md
│   └── development/                       # Development guides
│       ├── getting-started.md
│       ├── coding-standards.md
│       ├── testing-guidelines.md
│       └── contribution-guide.md
│
├── tests/                                 # End-to-end tests
│   ├── e2e/                               # End-to-end tests
│   │   ├── specs/
│   │   │   ├── intelligence-workflow.spec.ts
│   │   │   ├── operator-deployment.spec.ts
│   │   │   └── emergency-response.spec.ts
│   │   ├── fixtures/
│   │   └── support/
│   ├── integration/                       # Integration tests
│   │   ├── api-integration.test.ts
│   │   ├── database-integration.test.ts
│   │   └── blockchain-integration.test.ts
│   ├── performance/                       # Performance tests
│   │   ├── load-tests/
│   │   ├── stress-tests/
│   │   └── scalability-tests/
│   └── security/                          # Security tests
│       ├── penetration-tests/
│       ├── vulnerability-scans/
│       └── compliance-tests/
│
├── config/                                # Configuration files
│   ├── nx.json                           # Nx workspace configuration
│   ├── package.json                      # Root package.json
│   ├── tsconfig.base.json                # Base TypeScript configuration
│   ├── jest.config.js                    # Jest testing configuration
│   ├── eslint.config.js                  # ESLint configuration
│   ├── prettier.config.js                # Prettier configuration
│   └── docker-compose.yml                # Local development Docker Compose
│
├── scripts/                              # Root-level scripts
│   ├── setup-workspace.sh               # Initial workspace setup
│   ├── generate-certs.sh                # SSL certificate generation
│   ├── backup.sh                        # Backup scripts
│   └── health-check.sh                  # Health check scripts
│
├── .env.example                          # Environment variables template
├── .gitignore                           # Git ignore rules
├── .dockerignore                        # Docker ignore rules
├── README.md                            # Project documentation
├── CONTRIBUTING.md                      # Contribution guidelines
├── LICENSE                              # License file
├── SECURITY.md                          # Security policy
└── CHANGELOG.md                         # Change log
```

## Development Environment Setup

### Local Development Stack

```yaml
# docker-compose.yml for local development
version: '3.8'
services:
  # Databases
  postgresql:
    image: postgres:15
    environment:
      POSTGRES_DB: dion_platform
      POSTGRES_USER: dion_user
      POSTGRES_PASSWORD: dion_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/db-init:/docker-entrypoint-initdb.d
    
  redis:
    image: redis:7
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    
  neo4j:
    image: neo4j:5
    environment:
      NEO4J_AUTH: neo4j/password
      NEO4J_PLUGINS: '["graph-data-science"]'
    ports:
      - "7474:7474"
      - "7687:7687"
    volumes:
      - neo4j_data:/data
    
  elasticsearch:
    image: elasticsearch:8.8.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    
  # Message Queue
  nats:
    image: nats:2.9
    ports:
      - "4222:4222"
      - "6222:6222"
      - "8222:8222"
    command: ["--cluster_name", "dion", "--jetstream"]
    
  # Monitoring
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./infrastructure/monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
      - ./infrastructure/monitoring/grafana/dashboards:/var/lib/grafana/dashboards
    
  # Object Storage
  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    command: server /data --console-address ":9001"
    volumes:
      - minio_data:/data

volumes:
  postgres_data:
  redis_data:
  neo4j_data:
  elasticsearch_data:
  prometheus_data:
  grafana_data:
  minio_data:
```

### Development Scripts

```bash
#!/bin/bash
# scripts/setup-workspace.sh

echo "Setting up DION Platform development environment..."

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

# Install Python dependencies for AI services
echo "Installing Python dependencies..."
cd ai-services/graphrag-engine && pip install -r requirements.txt && cd ../..
cd ai-services/federated-learning && pip install -r requirements.txt && cd ../..
cd ai-services/multi-int-processor && pip install -r requirements.txt && cd ../..

# Install Rust dependencies
echo "Installing Rust dependencies..."
cd ai-services/real-time-processor && cargo build && cd ../..
cd edge-software/edge-coordinator && cargo build && cd ../..

# Set up databases
echo "Starting development databases..."
docker-compose up -d postgresql redis neo4j elasticsearch

# Wait for databases to be ready
echo "Waiting for databases to initialize..."
sleep 30

# Run database migrations
echo "Running database migrations..."
npm run db:migrate

# Generate initial data
echo "Generating development data..."
npm run db:seed

# Start development services
echo "Starting development services..."
npm run dev

echo "Development environment ready!"
echo "Access points:"
echo "- Web Dashboard: http://localhost:3000"
echo "- API Gateway: http://localhost:4000"
echo "- GraphQL Playground: http://localhost:4000/graphql"
echo "- Grafana: http://localhost:3001 (admin/admin)"
echo "- Neo4j Browser: http://localhost:7474"
echo "- Elasticsearch: http://localhost:9200"
```

## CI/CD Pipeline Configuration

### GitLab CI Configuration

```yaml
# .gitlab-ci.yml
stages:
  - lint-and-test
  - build
  - security-scan
  - deploy-staging
  - integration-tests
  - deploy-production

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"
  KUBECONFIG: /tmp/kubeconfig

# Lint and Test Stage
lint-typescript:
  stage: lint-and-test
  image: node:18
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
      - .npm/
  script:
    - npm ci --cache .npm --prefer-offline
    - npm run lint
    - npm run type-check
  rules:
    - changes:
        - "**/*.ts"
        - "**/*.tsx"
        - "**/*.js"
        - "**/*.jsx"

test-services:
  stage: lint-and-test
  image: node:18
  services:
    - postgres:15
    - redis:7
  variables:
    POSTGRES_HOST: postgres
    POSTGRES_DB: test_db
    POSTGRES_USER: test_user
    POSTGRES_PASSWORD: test_password
    REDIS_HOST: redis
  script:
    - npm ci
    - npm run test:unit
    - npm run test:integration
  coverage: '/Coverage: \d+\.\d+%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

test-ai-services:
  stage: lint-and-test
  image: python:3.11
  script:
    - cd ai-services/graphrag-engine
    - pip install -r requirements.txt
    - pip install pytest pytest-cov
    - pytest --cov=src --cov-report=xml
    - cd ../federated-learning
    - pip install -r requirements.txt
    - pytest --cov=src --cov-report=xml

test-edge-software:
  stage: lint-and-test
  image: rust:1.70
  script:
    - cd edge-software/edge-coordinator
    - cargo test
    - cargo clippy -- -D warnings
    - cargo fmt -- --check

# Build Stage
build-services:
  stage: build
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - |
      for service in services/*/; do
        service_name=$(basename "$service")
        echo "Building $service_name..."
        docker build -t $CI_REGISTRY_IMAGE/$service_name:$CI_COMMIT_SHA "$service"
        docker push $CI_REGISTRY_IMAGE/$service_name:$CI_COMMIT_SHA
        docker tag $CI_REGISTRY_IMAGE/$service_name:$CI_COMMIT_SHA $CI_REGISTRY_IMAGE/$service_name:latest
        docker push $CI_REGISTRY_IMAGE/$service_name:latest
      done
  rules:
    - if: $CI_COMMIT_BRANCH == "main" || $CI_COMMIT_BRANCH == "develop"

build-ai-services:
  stage: build
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - |
      for service in ai-services/*/; do
        service_name=$(basename "$service")
        echo "Building AI service $service_name..."
        docker build -t $CI_REGISTRY_IMAGE/ai-$service_name:$CI_COMMIT_SHA "$service"
        docker push $CI_REGISTRY_IMAGE/ai-$service_name:$CI_COMMIT_SHA
      done

build-frontend:
  stage: build
  image: node:18
  script:
    - npm ci
    - npm run build:web-dashboard
    - npm run build:admin-portal
  artifacts:
    paths:
      - apps/web-dashboard/dist
      - apps/admin-portal/dist
    expire_in: 1 hour

# Security Scan Stage
security-scan-containers:
  stage: security-scan
  image: aquasec/trivy:latest
  script:
    - |
      for service in services/*/; do
        service_name=$(basename "$service")
        trivy image --exit-code 0 --no-progress --format template --template "@contrib/sarif.tpl" \
          -o $service_name-security-report.sarif $CI_REGISTRY_IMAGE/$service_name:$CI_COMMIT_SHA
      done
  artifacts:
    reports:
      sast: "*-security-report.sarif"
  allow_failure: true

security-scan-code:
  stage: security-scan
  image: returntocorp/semgrep-agent:v1
  script:
    - semgrep-agent
  rules:
    - if: $CI_MERGE_REQUEST_IID
    - if: $CI_COMMIT_BRANCH == "main"

# Deploy Staging
deploy-staging:
  stage: deploy-staging
  image: bitnami/kubectl:latest
  environment:
    name: staging
    url: https://staging.dion-platform.com
  before_script:
    - echo $KUBE_CONFIG_STAGING | base64 -d > $KUBECONFIG
    - kubectl config use-context staging
  script:
    - kubectl set image deployment/intelligence-service intelligence-service=$CI_REGISTRY_IMAGE/intelligence-service:$CI_COMMIT_SHA
    - kubectl set image deployment/operator-service operator-service=$CI_REGISTRY_IMAGE/operator-service:$CI_COMMIT_SHA
    - kubectl set image deployment/emergency-response-service emergency-response-service=$CI_REGISTRY_IMAGE/emergency-response-service:$CI_COMMIT_SHA
    - kubectl rollout status deployment/intelligence-service
    - kubectl rollout status deployment/operator-service
    - kubectl rollout status deployment/emergency-response-service
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"

# Integration Tests
integration-tests-staging:
  stage: integration-tests
  image: node:18
  environment:
    name: staging
  script:
    - npm ci
    - npm run test:e2e:staging
  artifacts:
    when: always
    reports:
      junit: test-results.xml
    paths:
      - cypress/videos/
      - cypress/screenshots/
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"

# Deploy Production
deploy-production:
  stage: deploy-production
  image: bitnami/kubectl:latest
  environment:
    name: production
    url: https://platform.dion-network.com
  before_script:
    - echo $KUBE_CONFIG_PRODUCTION | base64 -d > $KUBECONFIG
    - kubectl config use-context production
  script:
    - |
      # Blue-Green deployment strategy
      kubectl patch deployment intelligence-service -p '{"spec":{"template":{"spec":{"containers":[{"name":"intelligence-service","image":"'$CI_REGISTRY_IMAGE'/intelligence-service:'$CI_COMMIT_SHA'"}]}}}}'
      kubectl rollout status deployment/intelligence-service --timeout=600s
      
      # Health check
      kubectl get pods -l app=intelligence-service
      
      # If health check passes, continue with other services
      kubectl patch deployment operator-service -p '{"spec":{"template":{"spec":{"containers":[{"name":"operator-service","image":"'$CI_REGISTRY_IMAGE'/operator-service:'$CI_COMMIT_SHA'"}]}}}}'
      kubectl rollout status deployment/operator-service --timeout=600s
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
    - when: manual
```

## Infrastructure as Code

### Terraform Configuration

```hcl
# infrastructure/terraform/environments/production/main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.20"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.10"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 4.70"
    }
  }
  backend "gcs" {
    bucket = "dion-platform-terraform-state"
    prefix = "production"
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

provider "kubernetes" {
  host                   = "https://${module.gke_cluster.endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(module.gke_cluster.ca_certificate)
}

provider "helm" {
  kubernetes {
    host                   = "https://${module.gke_cluster.endpoint}"
    token                  = data.google_client_config.default.access_token
    cluster_ca_certificate = base64decode(module.gke_cluster.ca_certificate)
  }
}

data "google_client_config" "default" {}

# GKE Cluster
module "gke_cluster" {
  source = "../../modules/kubernetes-cluster"
  
  project_id   = var.gcp_project_id
  region       = var.gcp_region
  cluster_name = "dion-production"
  
  node_pools = [
    {
      name         = "system-pool"
      machine_type = "e2-standard-4"
      min_count    = 1
      max_count    = 3
      disk_size_gb = 100
      disk_type    = "pd-ssd"
      preemptible  = false
      
      labels = {
        role = "system"
      }
      
      taints = [
        {
          key    = "role"
          value  = "system"
          effect = "NO_SCHEDULE"
        }
      ]
    },
    {
      name         = "app-pool"
      machine_type = "e2-standard-8"
      min_count    = 3
      max_count    = 20
      disk_size_gb = 200
      disk_type    = "pd-ssd"
      preemptible  = false
      
      labels = {
        role = "application"
      }
    },
    {
      name         = "ai-pool"
      machine_type = "n1-standard-8"
      min_count    = 1
      max_count    = 10
      disk_size_gb = 300
      disk_type    = "pd-ssd"
      preemptible  = true
      accelerator  = {
        type  = "nvidia-tesla-t4"
        count = 1
      }
      
      labels = {
        role = "ai-workloads"
      }
      
      taints = [
        {
          key    = "role"
          value  = "ai-workloads"
          effect = "NO_SCHEDULE"
        }
      ]
    }
  ]
  
  enable_workload_identity = true
  enable_network_policy    = true
  enable_pod_security_policy = true
}

# Database Infrastructure
module "postgresql" {
  source = "../../modules/database"
  
  project_id   = var.gcp_project_id
  region       = var.gcp_region
  
  instance_name = "dion-postgresql"
  database_version = "POSTGRES_15"
  tier = "db-custom-8-32768"
  disk_size = 500
  disk_type = "PD_SSD"
  
  backup_configuration = {
    enabled    = true
    start_time = "02:00"
    point_in_time_recovery_enabled = true
    retained_backups = 30
  }
  
  high_availability = {
    type = "REGIONAL"
  }
  
  databases = [
    {
      name = "dion_platform"
      charset = "UTF8"
      collation = "en_US.UTF8"
    }
  ]
  
  users = [
    {
      name = "dion_user"
      password = var.db_password
    }
  ]
}

# Redis Cluster
module "redis" {
  source = "../../modules/redis"
  
  project_id = var.gcp_project_id
  region     = var.gcp_region
  
  instance_id   = "dion-redis"
  memory_size   = 16
  tier          = "STANDARD_HA"
  redis_version = "REDIS_7_0"
  
  authorized_network = module.gke_cluster.network_name
}

# Storage
module "storage" {
  source = "../../modules/storage"
  
  project_id = var.gcp_project_id
  region     = var.gcp_region
  
  buckets = [
    {
      name = "dion-intelligence-data"
      storage_class = "STANDARD"
      versioning = true
      lifecycle_rules = [
        {
          condition = {
            age = 90
          }
          action = {
            type = "SetStorageClass"
            storage_class = "NEARLINE"
          }
        },
        {
          condition = {
            age = 365
          }
          action = {
            type = "SetStorageClass"
            storage_class = "COLDLINE"
          }
        }
      ]
    },
    {
      name = "dion-model-artifacts"
      storage_class = "STANDARD"
      versioning = true
    }
  ]
}

# Monitoring
module "monitoring" {
  source = "../../modules/monitoring"
  
  project_id = var.gcp_project_id
  
  enable_prometheus = true
  enable_grafana = true
  enable_alertmanager = true
  
  notification_channels = [
    {
      type = "slack"
      labels = {
        channel_name = "#dion-alerts"
        url = var.slack_webhook_url
      }
    },
    {
      type = "email"
      labels = {
        email_address = "alerts@dion-platform.com"
      }
    }
  ]
}

# Helm Charts Deployment
resource "helm_release" "dion_platform" {
  name       = "dion-platform"
  repository = "https://charts.dion-platform.com"
  chart      = "dion-platform"
  version    = var.chart_version
  namespace  = "dion-system"
  
  create_namespace = true
  
  values = [
    templatefile("${path.module}/values.yaml", {
      database_host = module.postgresql.private_ip
      database_name = "dion_platform"
      redis_host    = module.redis.host
      storage_bucket = module.storage.buckets["dion-intelligence-data"].name
      
      # Image tags
      intelligence_service_image = "${var.registry_url}/intelligence-service:${var.image_tag}"
      operator_service_image     = "${var.registry_url}/operator-service:${var.image_tag}"
      emergency_service_image    = "${var.registry_url}/emergency-response-service:${var.image_tag}"
      
      # AI Service images
      graphrag_engine_image = "${var.registry_url}/ai-graphrag-engine:${var.image_tag}"
      federated_learning_image = "${var.registry_url}/ai-federated-learning:${var.image_tag}"
      
      # Scaling configuration
      intelligence_service_replicas = 5
      operator_service_replicas = 3
      emergency_service_replicas = 3
      
      # Resource limits
      intelligence_service_resources = {
        requests = {
          cpu    = "500m"
          memory = "1Gi"
        }
        limits = {
          cpu    = "2"
          memory = "4Gi"
        }
      }
      
      ai_service_resources = {
        requests = {
          cpu    = "1"
          memory = "4Gi"
          nvidia_com_gpu = 1
        }
        limits = {
          cpu    = "4"
          memory = "16Gi"
          nvidia_com_gpu = 1
        }
      }
    })
  ]
  
  depends_on = [
    module.gke_cluster,
    module.postgresql,
    module.redis
  ]
}
```

## Database Schema and Migrations

### Database Migration System

```sql
-- migrations/001_initial_schema.sql
-- Initial database schema for DION platform

-- Users and Identity
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- Users table with DID integration
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    did TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    profile JSONB DEFAULT '{}',
    roles TEXT[] DEFAULT '{}',
    permissions TEXT[] DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_active TIMESTAMP WITH TIME ZONE
);

-- Create indexes for performance
CREATE INDEX idx_users_did ON users(did);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_roles ON users USING GIN(roles);
CREATE INDEX idx_users_permissions ON users USING GIN(permissions);

-- Nodes table for edge infrastructure
CREATE TABLE nodes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    did TEXT UNIQUE NOT NULL,
    owner_id UUID REFERENCES users(id),
    node_type TEXT NOT NULL CHECK (node_type IN ('community', 'professional', 'command')),
    capabilities INTEGER NOT NULL DEFAULT 0, -- Bitmask
    hardware_spec JSONB DEFAULT '{}',
    location GEOMETRY(POINT, 4326),
    location_hash TEXT, -- For privacy-preserving location queries
    status TEXT NOT NULL DEFAULT 'offline' CHECK (status IN ('online', 'offline', 'maintenance', 'error')),
    reputation DECIMAL(10,2) DEFAULT 1000.0,
    stake_amount DECIMAL(20,8) DEFAULT 0,
    certification_hash TEXT,
    last_heartbeat TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_nodes_did ON nodes(did);
CREATE INDEX idx_nodes_owner ON nodes(owner_id);
CREATE INDEX idx_nodes_type ON nodes(node_type);
CREATE INDEX idx_nodes_location ON nodes USING GIST(location);
CREATE INDEX idx_nodes_location_hash ON nodes(location_hash);
CREATE INDEX idx_nodes_status ON nodes(status);
CREATE INDEX idx_nodes_capabilities ON nodes(capabilities);

-- Operators table for human workforce
CREATE TABLE operators (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    did TEXT UNIQUE NOT NULL,
    level INTEGER NOT NULL CHECK (level BETWEEN 1 AND 4),
    specializations INTEGER[] DEFAULT '{}', -- Array of specialization IDs
    certifications JSONB DEFAULT '[]',
    performance_metrics JSONB DEFAULT '{}',
    availability_config JSONB DEFAULT '{}',
    current_status TEXT DEFAULT 'available' CHECK (current_status IN ('available', 'busy', 'offline', 'training')),
    location GEOMETRY(POINT, 4326),
    reputation DECIMAL(10,2) DEFAULT 1000.0,
    success_rate DECIMAL(5,4) DEFAULT 1.0000,
    total_tasks INTEGER DEFAULT 0,
    total_earnings DECIMAL(20,8) DEFAULT 0,
    stake_amount DECIMAL(20,8) DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_operators_user ON operators(user_id);
CREATE INDEX idx_operators_did ON operators(did);
CREATE INDEX idx_operators_level ON operators(level);
CREATE INDEX idx_operators_specializations ON operators USING GIN(specializations);
CREATE INDEX idx_operators_status ON operators(current_status);
CREATE INDEX idx_operators_location ON operators USING GIST(location);
CREATE INDEX idx_operators_reputation ON operators(reputation DESC);

-- Intelligence data table
CREATE TABLE intelligence (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_hash TEXT UNIQUE NOT NULL,
    intelligence_type TEXT NOT NULL,
    source_node_id UUID REFERENCES nodes(id),
    collector_id UUID, -- Could be node or operator
    location GEOMETRY(POINT, 4326),
    location_hash TEXT,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    confidence DECIMAL(3,2) CHECK (confidence BETWEEN 0.00 AND 1.00),
    verification_status TEXT DEFAULT 'unverified' CHECK (verification_status IN ('unverified', 'single_source', 'multi_source', 'expert_verified', 'disputed')),
    privacy_level TEXT NOT NULL DEFAULT 'public' CHECK (privacy_level IN ('public', 'restricted', 'confidential', 'secret')),
    metadata JSONB DEFAULT '{}',
    tags TEXT[] DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_intelligence_content_hash ON intelligence(content_hash);
CREATE INDEX idx_intelligence_type ON intelligence(intelligence_type);
CREATE INDEX idx_intelligence_source ON intelligence(source_node_id);
CREATE INDEX idx_intelligence_location ON intelligence USING GIST(location);
CREATE INDEX idx_intelligence_timestamp ON intelligence(timestamp DESC);
CREATE INDEX idx_intelligence_verification ON intelligence(verification_status);
CREATE INDEX idx_intelligence_tags ON intelligence USING GIN(tags);
CREATE INDEX idx_intelligence_metadata ON intelligence USING GIN(metadata);

-- Tasks and bounties
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    creator_id UUID REFERENCES users(id),
    task_type TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    requirements JSONB DEFAULT '{}',
    location GEOMETRY(POINT, 4326),
    location_radius DECIMAL(10,2), -- in meters
    reward_amount DECIMAL(20,8) NOT NULL,
    reward_currency TEXT DEFAULT 'INTEL',
    required_capabilities INTEGER DEFAULT 0, -- Bitmask
    required_operator_level INTEGER,
    required_specializations INTEGER[] DEFAULT '{}',
    urgency_level TEXT DEFAULT 'normal' CHECK (urgency_level IN ('low', 'normal', 'high', 'critical', 'emergency')),
    status TEXT DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'submitted', 'verification', 'completed', 'disputed', 'expired', 'cancelled')),
    deadline TIMESTAMP WITH TIME ZONE,
    verification_criteria JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_tasks_creator ON tasks(creator_id);
CREATE INDEX idx_tasks_type ON tasks(task_type);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_urgency ON tasks(urgency_level);
CREATE INDEX idx_tasks_location ON tasks USING GIST(location);
CREATE INDEX idx_tasks_deadline ON tasks(deadline);
CREATE INDEX idx_tasks_reward ON tasks(reward_amount DESC);
CREATE INDEX idx_tasks_capabilities ON tasks(required_capabilities);

-- Task assignments
CREATE TABLE task_assignments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
    operator_id UUID REFERENCES operators(id),
    node_id UUID REFERENCES nodes(id),
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    accepted_at TIMESTAMP WITH TIME ZONE,
    status TEXT DEFAULT 'assigned' CHECK (status IN ('assigned', 'accepted', 'in_progress', 'completed', 'declined', 'cancelled')),
    progress JSONB DEFAULT '{}',
    completed_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(task_id, operator_id)
);

CREATE INDEX idx_task_assignments_task ON task_assignments(task_id);
CREATE INDEX idx_task_assignments_operator ON task_assignments(operator_id);
CREATE INDEX idx_task_assignments_status ON task_assignments(status);

-- Task submissions and results
CREATE TABLE task_submissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id UUID REFERENCES tasks(id),
    assignment_id UUID REFERENCES task_assignments(id),
    submitter_id UUID REFERENCES users(id),
    submission_type TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    quality_score DECIMAL(3,2),
    verification_status TEXT DEFAULT 'pending' CHECK (verification_status IN ('pending', 'verified', 'rejected', 'disputed')),
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    verified_at TIMESTAMP WITH TIME ZONE,
    verified_by UUID REFERENCES users(id)
);

CREATE INDEX idx_task_submissions_task ON task_submissions(task_id);
CREATE INDEX idx_task_submissions_assignment ON task_submissions(assignment_id);
CREATE INDEX idx_task_submissions_submitter ON task_submissions(submitter_id);
CREATE INDEX idx_task_submissions_status ON task_submissions(verification_status);

-- Emergency alerts and responses
CREATE TABLE emergency_alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    alert_type TEXT NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    title TEXT NOT NULL,
    description TEXT,
    location GEOMETRY(POINT, 4326) NOT NULL,
    radius DECIMAL(10,2) NOT NULL, -- Search radius in meters
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'in_progress', 'resolved', 'cancelled')),
    priority INTEGER DEFAULT 5 CHECK (priority BETWEEN 1 AND 10),
    metadata JSONB DEFAULT '{}',
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolution_summary TEXT
);

CREATE INDEX idx_emergency_alerts_type ON emergency_alerts(alert_type);
CREATE INDEX idx_emergency_alerts_severity ON emergency_alerts(severity);
CREATE INDEX idx_emergency_alerts_status ON emergency_alerts(status);
CREATE INDEX idx_emergency_alerts_location ON emergency_alerts USING GIST(location);
CREATE INDEX idx_emergency_alerts_priority ON emergency_alerts(priority DESC);
CREATE INDEX idx_emergency_alerts_created ON emergency_alerts(created_at DESC);

-- Mobilization tracking
CREATE TABLE emergency_mobilizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    alert_id UUID REFERENCES emergency_alerts(id) ON DELETE CASCADE,
    mobilization_type TEXT NOT NULL,
    target_location GEOMETRY(POINT, 4326),
    search_radius DECIMAL(10,2),
    operators_needed INTEGER DEFAULT 0,
    operators_assigned INTEGER DEFAULT 0,
    nodes_activated INTEGER DEFAULT 0,
    resources_deployed JSONB DEFAULT '{}',
    coordination_hub_url TEXT,
    communication_channels JSONB DEFAULT '{}',
    status TEXT DEFAULT 'initiated' CHECK (status IN ('initiated', 'deploying', 'active', 'scaling_down', 'completed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_mobilizations_alert ON emergency_mobilizations(alert_id);
CREATE INDEX idx_mobilizations_status ON emergency_mobilizations(status);
CREATE INDEX idx_mobilizations_location ON emergency_mobilizations USING GIST(target_location);

-- Blockchain transactions tracking
CREATE TABLE blockchain_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    transaction_hash TEXT UNIQUE NOT NULL,
    block_number BIGINT,
    transaction_type TEXT NOT NULL,
    from_address TEXT NOT NULL,
    to_address TEXT,
    value DECIMAL(30,18),
    gas_used BIGINT,
    gas_price DECIMAL(30,18),
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'failed')),
    event_data JSONB DEFAULT '{}',
    related_entity_type TEXT, -- 'task', 'operator', 'node', etc.
    related_entity_id UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    confirmed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_blockchain_tx_hash ON blockchain_transactions(transaction_hash);
CREATE INDEX idx_blockchain_tx_type ON blockchain_transactions(transaction_type);
CREATE INDEX idx_blockchain_tx_status ON blockchain_transactions(status);
CREATE INDEX idx_blockchain_tx_entity ON blockchain_transactions(related_entity_type, related_entity_id);

-- Performance metrics and analytics
CREATE TABLE performance_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_type TEXT NOT NULL, -- 'operator', 'node', 'task', 'system'
    entity_id UUID NOT NULL,
    metric_type TEXT NOT NULL,
    metric_value DECIMAL(20,8),
    metric_metadata JSONB DEFAULT '{}',
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    time_period TEXT -- 'real_time', 'hourly', 'daily', 'weekly', 'monthly'
);

CREATE INDEX idx_performance_metrics_entity ON performance_metrics(entity_type, entity_id);
CREATE INDEX idx_performance_metrics_type ON performance_metrics(metric_type);
CREATE INDEX idx_performance_metrics_recorded ON performance_metrics(recorded_at DESC);
CREATE INDEX idx_performance_metrics_period ON performance_metrics(time_period);

-- Audit logs
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    actor_id UUID REFERENCES users(id),
    actor_type TEXT NOT NULL, -- 'user', 'operator', 'node', 'system'
    action TEXT NOT NULL,
    resource_type TEXT NOT NULL,
    resource_id UUID,
    details JSONB DEFAULT '{}',
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    session_id TEXT
);

CREATE INDEX idx_audit_logs_actor ON audit_logs(actor_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp DESC);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers to relevant tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_nodes_updated_at BEFORE UPDATE ON nodes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_operators_updated_at BEFORE UPDATE ON operators FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

## API Design and Documentation

### OpenAPI Specification

```yaml
# docs/api/openapi.yaml
openapi: 3.0.3
info:
  title: DION Platform API
  description: |
    Decentralized Intelligence & Operator Network Platform API
    
    This API provides access to the DION platform's intelligence collection,
    operator management, emergency response, and community governance features.
  version: 1.0.0
  contact:
    name: DION Platform Team
    email: api-support@dion-platform.com
    url: https://docs.dion-platform.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.dion-platform.com/v1
    description: Production API
  - url: https://staging-api.dion-platform.com/v1  
    description: Staging API
  - url: http://localhost:4000/v1
    description: Local development API

security:
  - BearerAuth: []
  - DIDAuth: []

paths:
  # Intelligence endpoints
  /intelligence:
    get:
      summary: Search intelligence data
      description: Search and filter intelligence data with various criteria
      tags: [Intelligence]
      parameters:
        - name: types
          in: query
          schema:
            type: array
            items:
              type: string
              enum: [OSINT, IMINT, SIGINT, HUMINT, MASINT, GEOINT, CYBINT, FININT, TECHINT, MEDINT]
        - name: location
          in: query
          schema:
            type: object
            properties:
              latitude:
                type: number
                format: double
              longitude:
                type: number
                format: double
              radius:
                type: number
                description: Search radius in meters
        - name: timeRange
          in: query
          schema:
            type: object
            properties:
              start:
                type: string
                format: date-time
              end:
                type: string
                format: date-time
        - name: confidenceThreshold
          in: query
          schema:
            type: number
            minimum: 0
            maximum: 1
        - name: verificationRequired
          in: query
          schema:
            type: boolean
        - name: limit
          in: query
          schema:
            type: integer
            default: 50
            maximum: 1000
        - name: offset
          in: query
          schema:
            type: integer
            default: 0
      responses:
        '200':
          description: Intelligence search results
          content:
            application/json:
              schema:
                type: object
                properties:
                  results:
                    type: array
                    items:
                      $ref: '#/components/schemas/Intelligence'
                  total:
                    type: integer
                  limit:
                    type: integer
                  offset:
                    type: integer
                  hasMore:
                    type: boolean
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'

    post:
      summary: Submit intelligence data
      description: Submit new intelligence data to the platform
      tags: [Intelligence]
      security:
        - BearerAuth: []
        - DIDAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/IntelligenceSubmission'
      responses:
        '201':
          description: Intelligence successfully submitted
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: string
                    format: uuid
                  contentHash:
                    type: string
                  status:
                    type: string
                    enum: [accepted, pending_verification]
                  submittedAt:
                    type: string
                    format: date-time
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '413':
          description: Payload too large
        '429':
          $ref: '#/components/responses/RateLimit'

  /intelligence/{id}:
    get:
      summary: Get specific intelligence data
      tags: [Intelligence]
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Intelligence data
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Intelligence'
        '404':
          $ref: '#/components/responses/NotFound'

  /intelligence/{id}/verify:
    post:
      summary: Verify intelligence data
      description: Submit verification for intelligence data
      tags: [Intelligence]
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                verification:
                  type: string
                  enum: [verified, disputed, false]
                evidence:
                  type: string
                  description: Supporting evidence for verification
                confidence:
                  type: number
                  minimum: 0
                  maximum: 1
              required: [verification]
      responses:
        '200':
          description: Verification submitted
        '400':
          $ref: '#/components/responses/BadRequest'
        '404':
          $ref: '#/components/responses/NotFound'

  # Operator endpoints
  /operators:
    get:
      summary: Find available operators
      tags: [Operators]
      parameters:
        - name: level
          in: query
          schema:
            type: integer
            minimum: 1
            maximum: 4
        - name: specializations
          in: query
          schema:
            type: array
            items:
              type: string
        - name: location
          in: query
          schema:
            $ref: '#/components/schemas/LocationQuery'
        - name: availability
          in: query
          schema:
            type: string
            enum: [available, busy, offline]
            default: available
      responses:
        '200':
          description: Available operators
          content:
            application/json:
              schema:
                type: object
                properties:
                  operators:
                    type: array
                    items:
                      $ref: '#/components/schemas/Operator'

    post:
      summary: Register as operator
      tags: [Operators]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/OperatorRegistration'
      responses:
        '201':
          description: Operator registration successful
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Operator'
        '400':
          $ref: '#/components/responses/BadRequest'

  /operators/{id}/availability:
    put:
      summary: Update operator availability
      tags: [Operators]
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  enum: [available, busy, offline, training]
                location:
                  $ref: '#/components/schemas/Location'
                availableUntil:
                  type: string
                  format: date-time
                maxConcurrentTasks:
                  type: integer
                  minimum: 1
                  maximum: 10
              required: [status]
      responses:
        '200':
          description: Availability updated
        '400':
          $ref: '#/components/responses/BadRequest'
        '404':
          $ref: '#/components/responses/NotFound'

  # Task endpoints
  /tasks:
    get:
      summary: Get available tasks
      tags: [Tasks]
      parameters:
        - name: operatorId
          in: query
          schema:
            type: string
            format: uuid
        - name: taskType
          in: query
          schema:
            type: string
        - name: location
          in: query
          schema:
            $ref: '#/components/schemas/LocationQuery'
        - name: minReward
          in: query
          schema:
            type: number
        - name: urgency
          in: query
          schema:
            type: string
            enum: [low, normal, high, critical, emergency]
        - name: status
          in: query
          schema:
            type: string
            enum: [open, in_progress, verification, completed]
            default: open
      responses:
        '200':
          description: Available tasks
          content:
            application/json:
              schema:
                type: object
                properties:
                  tasks:
                    type: array
                    items:
                      $ref: '#/components/schemas/Task'

    post:
      summary: Create new task
      tags: [Tasks]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskCreation'
      responses:
        '201':
          description: Task created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '400':
          $ref: '#/components/responses/BadRequest'
        '402':
          description: Insufficient funds for task reward

  /tasks/{id}/accept:
    post:
      summary: Accept a task
      tags: [Tasks]
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                operatorId:
                  type: string
                  format: uuid
                estimatedCompletion:
                  type: string
                  format: date-time
                notes:
                  type: string
              required: [operatorId]
      responses:
        '200':
          description: Task accepted
          content:
            application/json:
              schema:
                type: object
                properties:
                  assignmentId:
                    type: string
                    format: uuid
                  status:
                    type: string
                  acceptedAt:
                    type: string
                    format: date-time
        '400':
          $ref: '#/components/responses/BadRequest'
        '409':
          description: Task already assigned or expired

  /tasks/{id}/submit:
    post:
      summary: Submit task completion
      tags: [Tasks]
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                assignmentId:
                  type: string
                  format: uuid
                submissionType:
                  type: string
                  enum: [report, evidence, analysis]
                content:
                  type: string
                  format: binary
                metadata:
                  type: string
                  description: JSON metadata
                signature:
                  type: string
                  description: Digital signature of submission
              required: [assignmentId, submissionType, content, signature]
      responses:
        '201':
          description: Submission successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  submissionId:
                    type: string
                    format: uuid
                  contentHash:
                    type: string
                  status:
                    type: string
                    enum: [pending_verification, verified]
                  submittedAt:
                    type: string
                    format: date-time
        '400':
          $ref: '#/components/responses/BadRequest'
        '404':
          $ref: '#/components/responses/NotFound'

  # Emergency Response endpoints
  /emergency/alerts:
    get:
      summary: Get active emergency alerts
      tags: [Emergency]
      parameters:
        - name: location
          in: query
          schema:
            $ref: '#/components/schemas/LocationQuery'
        - name: severity
          in: query
          schema:
            type: string
            enum: [low, medium, high, critical]
        - name: status
          in: query
          schema:
            type: string
            enum: [active, in_progress, resolved]
            default: active
      responses:
        '200':
          description: Emergency alerts
          content:
            application/json:
              schema:
                type: object
                properties:
                  alerts:
                    type: array
                    items:
                      $ref: '#/components/schemas/EmergencyAlert'

    post:
      summary: Create emergency alert
      tags: [Emergency]
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/EmergencyAlertCreation'
      responses:
        '201':
          description: Emergency alert created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/EmergencyAlert'
        '400':
          $ref: '#/components/responses/BadRequest'
        '403':
          description: Insufficient permissions to create emergency alert

  /emergency/mobilize:
    post:
      summary: Mobilize emergency response
      tags: [Emergency]
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                alertId:
                  type: string
                  format: uuid
                mobilizationType:
                  type: string
                  enum: [search_rescue, disaster_response, medical_emergency, security_threat]
                targetLocation:
                  $ref: '#/components/schemas/Location'
                searchRadius:
                  type: number
                  description: Search radius in meters
                operatorsNeeded:
                  type: integer
                  minimum: 1
                resourceRequirements:
                  type: object
                  properties:
                    drones:
                      type: integer
                    vehicles:
                      type: integer
                    specializedEquipment:
                      type: array
                      items:
                        type: string
              required: [alertId, mobilizationType, targetLocation]
      responses:
        '201':
          description: Mobilization initiated
          content:
            application/json:
              schema:
                type: object
                properties:
                  mobilizationId:
                    type: string
                    format: uuid
                  status:
                    type: string
                    enum: [initiated, deploying, active]
                  estimatedResponseTime:
                    type: integer
                    description: Estimated response time in seconds
                  coordinationHub:
                    type: string
                    format: uri
                    description: URL for real-time coordination
                  activatedNodes:
                    type: integer
                  assignedOperators:
                    type: integer
        '400':
          $ref: '#/components/responses/BadRequest'
        '403':
          $ref: '#/components/responses/Forbidden'

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
    DIDAuth:
      type: apiKey
      in: header
      name: X-DID-Auth
      description: DID-based authentication with signature

  schemas:
    Intelligence:
      type: object
      properties:
        id:
          type: string
          format: uuid
        contentHash:
          type: string
        type:
          type: string
          enum: [OSINT, IMINT, SIGINT, HUMINT, MASINT, GEOINT, CYBINT, FININT, TECHINT, MEDINT]
        timestamp:
          type: string
          format: date-time
        location:
          $ref: '#/components/schemas/Location'
        confidence:
          type: number
          minimum: 0
          maximum: 1
        verificationStatus:
          type: string
          enum: [unverified, single_source, multi_source, expert_verified, disputed]
        privacyLevel:
          type: string
          enum: [public, restricted, confidential]
        sources:
          type: array
          items:
            $ref: '#/components/schemas/IntelligenceSource'
        metadata:
          type: object
        tags:
          type: array
          items:
            type: string
        createdAt:
          type: string
          format: date-time
        expiresAt:
          type: string
          format: date-time

    IntelligenceSource:
      type: object
      properties:
        nodeId:
          type: string
          format: uuid
        nodeDID:
          type: string
        sensorType:
          type: string
        reputation:
          type: number
        attestation:
          type: string

    IntelligenceSubmission:
      type: object
      properties:
        type:
          type: string
          enum: [OSINT, IMINT, SIGINT, HUMINT, MASINT, GEOINT, CYBINT, FININT, TECHINT, MEDINT]
        content:
          type: string
          description: Base64 encoded content or content hash
        location:
          $ref: '#/components/schemas/Location'
        timestamp:
          type: string
          format: date-time
        metadata:
          type: object
        tags:
          type: array
          items:
            type: string
        signature:
          type: string
          description: Digital signature of the submission
        attestation:
          type: string
          description: Hardware attestation or provenance proof
      required: [type, content, timestamp, signature]

    Operator:
      type: object
      properties:
        id:
          type: string
          format: uuid
        did:
          type: string
        level:
          type: integer
          minimum: 1
          maximum: 4
        specializations:
          type: array
          items:
            type: string
        certifications:
          type: array
          items:
            type: object
        reputation:
          type: number
        successRate:
          type: number
          minimum: 0
          maximum: 1
        availability:
          type: object
          properties:
            status:
              type: string
              enum: [available, busy, offline, training]
            location:
              $ref: '#/components/schemas/Location'
            availableUntil:
              type: string
              format: date-time
        performanceMetrics:
          type: object
        totalTasks:
          type: integer
        totalEarnings:
          type: number

    OperatorRegistration:
      type: object
      properties:
        did:
          type: string
        level:
          type: integer
          minimum: 1
          maximum: 4
        specializations:
          type: array
          items:
            type: string
        certificationProofs:
          type: array
          items:
            type: string
        location:
          $ref: '#/components/schemas/Location'
        availabilityConfig:
          type: object
        signature:
          type: string
      required: [did, level, certificationProofs, signature]

    Task:
      type: object
      properties:
        id:
          type: string
          format: uuid
        type:
          type: string
        title:
          type: string
        description:
          type: string
        requirements:
          type: object
        location:
          $ref: '#/components/schemas/Location'
        radius:
          type: number
          description: Task area radius in meters
        reward:
          type: object
          properties:
            amount:
              type: number
            currency:
              type: string
              default: INTEL
        urgencyLevel:
          type: string
          enum: [low, normal, high, critical, emergency]
        status:
          type: string
          enum: [open, in_progress, submitted, verification, completed, disputed, expired, cancelled]
        deadline:
          type: string
          format: date-time
        verificationCriteria:
          type: object
        createdAt:
          type: string
          format: date-time
        assignedOperators:
          type: array
          items:
            type: string
            format: uuid

    TaskCreation:
      type: object
      properties:
        type:
          type: string
        title:
          type: string
        description:
          type: string
        requirements:
          type: object
        location:
          $ref: '#/components/schemas/Location'
        radius:
          type: number
        rewardAmount:
          type: number
        deadline:
          type: string
          format: date-time
        urgencyLevel:
          type: string
          enum: [low, normal, high, critical, emergency]
          default: normal
        verificationCriteria:
          type: object
      required: [type, title, rewardAmount, deadline]

    EmergencyAlert:
      type: object
      properties:
        id:
          type: string
          format: uuid
        type:
          type: string
        severity:
          type: string
          enum: [low, medium, high, critical]
        title:
          type: string
        description:
          type: string
        location:
          $ref: '#/components/schemas/Location'
        radius:
          type: number
        status:
          type: string
          enum: [active, in_progress, resolved, cancelled]
        priority:
          type: integer
          minimum: 1
          maximum: 10
        metadata:
          type: object
        createdAt:
          type: string
          format: date-time
        resolvedAt:
          type: string
          format: date-time

    EmergencyAlertCreation:
      type: object
      properties:
        type:
          type: string
        severity:
          type: string
          enum: [low, medium, high, critical]
        title: