---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: e8ce77ac-4220-4b44-b4c1-faee52b6fea3
original_filename: OpenSecure_Hub_Network_Topology.md
created_at: 2026-03-04T20:36:32.675043+00:00
content_hash: 48197ec1fe07
status: "duplicate"
duplicate_of: "knowledge-base/d-central/security/Open-Secure/OpenSecure-Hub-Network-Topology-md.md"
duplicate_reason: "exact body-hash match within the same category, resolved during Stage 5 topic-synthesis prep (never went through Stage 4 exact-hash dedup, which only covered the original 428 docs before this fine-grained reclassification)"
---

# OpenSecure Hub Network Topology
## Unified Management Platform Network Architecture

**Document Type**: Network Topology Specification  
**Version**: 1.0  
**Date**: December 2024  
**Classification**: Technical Documentation  
**Audience**: Enterprise Architects, Network Engineers, CISOs

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Hub Architecture Philosophy](#hub-architecture-philosophy)
3. [Global Network Architecture](#global-network-architecture)
4. [Hub Infrastructure](#hub-infrastructure)
5. [Service Integration Network](#service-integration-network)
6. [Multi-Tenant Architecture](#multi-tenant-architecture)
7. [Security Architecture](#security-architecture)
8. [High Availability & Disaster Recovery](#high-availability--disaster-recovery)
9. [Monitoring & Operations](#monitoring--operations)
10. [Deployment Scenarios](#deployment-scenarios)

---

## Executive Summary

### What is OpenSecure Hub?

The **OpenSecure Hub** is the central nervous system of the OpenSecure ecosystem - a unified management platform that connects, coordinates, and orchestrates all five OpenSecure services:

- **OS-PACS** (Physical Access Control)
- **OS-PATROL** (Fleet Management & Mobile Patrol)
- **OS-CONCIERGE** (Intelligent Concierge Services)
- **OS-GUARDIAN** (Security Personnel & Body Cameras)
- **OS-SENTINEL** (AI-Powered Surveillance)

### Hub Value Proposition

| Capability | Without Hub | With Hub |
|------------|-------------|----------|
| **Management** | 5 separate interfaces | Single unified dashboard |
| **Authentication** | 5 separate logins | Single Sign-On (SSO) |
| **Reporting** | 5 disconnected reports | Unified cross-service analytics |
| **Alerts** | 5 alert systems | Consolidated alert correlation |
| **API Access** | 5 different APIs | Unified API gateway |
| **User Management** | 5 user databases | Centralized identity management |
| **Billing** | 5 separate invoices | Unified usage tracking |

### Network Architecture Summary

```
┌────────────────────────────────────────────────────────────────┐
│                    OPENSECURE HUB                               │
│               (Central Cloud Platform)                          │
│                                                                 │
│  Single Pane of Glass for All Security Operations             │
│  • Unified Dashboard                                           │
│  • Cross-Service Analytics                                     │
│  • Centralized Identity & Access Management                    │
│  • Unified API Gateway                                         │
│  • Consolidated Monitoring & Alerting                          │
└─────────────────────┬──────────────────────────────────────────┘
                      │
                      │ Hub Network: 10.0.0.0/8
                      │
        ┌─────────────┼─────────────┬──────────────┬─────────────┐
        │             │             │              │             │
   ┌────▼────┐   ┌────▼────┐   ┌───▼──────┐  ┌───▼──────┐  ┌───▼──────┐
   │OS-PACS  │   │OS-PATROL│   │OS-       │  │OS-       │  │OS-       │
   │Network  │   │Network  │   │CONCIERGE │  │GUARDIAN  │  │SENTINEL  │
   │10.100.  │   │10.110.  │   │10.120.   │  │10.130.   │  │10.140.   │
   │0.0/16   │   │0.0/16   │   │0.0/16    │  │0.0/16    │  │0.0/16    │
   └─────────┘   └─────────┘   └──────────┘  └──────────┘  └──────────┘
```

---

## Hub Architecture Philosophy

### Design Principles

1. **Unified Experience**: Single interface for all security operations
2. **Service Independence**: Each service can operate standalone or integrated
3. **Federated Identity**: Centralized user management with service-level permissions
4. **Data Sovereignty**: Customer data stays in customer's chosen region
5. **API-First**: All features accessible via unified API
6. **Event-Driven**: Real-time cross-service correlation
7. **Multi-Tenant**: Isolated environments for each customer
8. **Cloud-Agnostic**: Deploy on AWS, Azure, GCP, or on-premises

### Hub Core Functions

```
┌──────────────────────────────────────────────────────────────┐
│                   OPENSECURE HUB CORE                         │
└──────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 1. IDENTITY & ACCESS MANAGEMENT (IAM)                       │
│    • Single Sign-On (SSO) - SAML, OAuth2, OIDC             │
│    • Multi-Factor Authentication (MFA)                      │
│    • Role-Based Access Control (RBAC)                       │
│    • Service-Level Permissions                              │
│    • Audit Logging                                          │
│    Tech: Keycloak, LDAP, Active Directory integration       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 2. UNIFIED API GATEWAY                                      │
│    • Single endpoint: api.opensecure.com                    │
│    • Rate limiting: 10,000 req/hour per tenant             │
│    • Service routing: /pacs/*, /patrol/*, /sentinel/*      │
│    • Request transformation & validation                    │
│    • API versioning (v1, v2)                               │
│    Tech: Kong, Apache APISIX, NGINX                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 3. EVENT CORRELATION ENGINE                                 │
│    • Cross-service event matching                           │
│    • Real-time alert correlation                           │
│    • Automated incident creation                           │
│    • SLA tracking & escalation                             │
│    Example: Access denied (PACS) + loitering (SENTINEL)    │
│             = Security threat escalation                    │
│    Tech: Apache Kafka, Elasticsearch, Logstash             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 4. UNIFIED ANALYTICS & REPORTING                            │
│    • Cross-service dashboards                              │
│    • Custom report builder                                 │
│    • Scheduled reports (daily/weekly/monthly)              │
│    • Export: PDF, Excel, CSV                               │
│    • Real-time metrics aggregation                         │
│    Tech: Grafana, Metabase, Apache Superset               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 5. CENTRALIZED CONFIGURATION MANAGEMENT                     │
│    • Service configuration versioning                       │
│    • Configuration templates                                │
│    • Multi-site configuration sync                          │
│    • Change approval workflows                              │
│    • Rollback capabilities                                  │
│    Tech: Consul, etcd, Git-based configs                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 6. MONITORING & OBSERVABILITY                               │
│    • Service health dashboards                             │
│    • Resource utilization tracking                          │
│    • Performance metrics (latency, throughput)             │
│    • Log aggregation & search                              │
│    • Distributed tracing                                    │
│    Tech: Prometheus, Grafana, ELK Stack, Jaeger            │
└─────────────────────────────────────────────────────────────┘
```

---

## Global Network Architecture

### Three-Tier Hub Network Design

```
┌──────────────────────────────────────────────────────────────────┐
│                    TIER 1: EDGE NETWORK                           │
│                    (Customer Entry Point)                         │
└──────────────────────────────────────────────────────────────────┘

                        Internet
                            │
                            │ Global Anycast IPs
                            │ • Web: 203.0.113.10
                            │ • API: 203.0.113.20
                            │
                    ┌───────▼────────┐
                    │   CloudFlare   │
                    │   CDN + WAF    │
                    │                │
                    │ • DDoS Protect │
                    │ • TLS 1.3      │
                    │ • Edge Caching │
                    └───────┬────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼─────┐       ┌─────▼────┐       ┌─────▼────┐
   │  Region  │       │ Region   │       │ Region   │
   │US-East-1 │       │EU-West-1 │       │AP-South-1│
   │(Primary) │       │(Secondary│       │(Secondary│
   └────┬─────┘       └─────┬────┘       └─────┬────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
┌───────────────────────────▼───────────────────────────────────────┐
│                    TIER 2: APPLICATION NETWORK                     │
│                    (Hub Services - 10.0.0.0/16)                   │
└───────────────────────────────────────────────────────────────────┘

            ┌───────────────────────────────┐
            │  Application Load Balancer    │
            │  (Layer 7)                    │
            │  VIP: 10.0.0.5                │
            └───────┬───────────────────────┘
                    │
        ┌───────────┼───────────┬───────────┐
        │           │           │           │
   ┌────▼────┐ ┌────▼────┐ ┌───▼─────┐ ┌───▼─────┐
   │  VLAN   │ │  VLAN   │ │  VLAN   │ │  VLAN   │
   │   10    │ │   20    │ │   30    │ │   40    │
   │   Web   │ │   API   │ │  Data   │ │  Mgmt   │
   │10.0.10. │ │10.0.20. │ │10.0.30. │ │10.0.40. │
   │  0/24   │ │  0/24   │ │  0/24   │ │  0/24   │
   └─────────┘ └─────────┘ └─────────┘ └─────────┘

┌───────────────────────────▼───────────────────────────────────────┐
│                    TIER 3: SERVICE NETWORK                         │
│              (Integration with 5 Services)                        │
└───────────────────────────────────────────────────────────────────┘

   ┌──────────────────────────────────────────────────────────┐
   │         Service Mesh (Istio / Linkerd)                   │
   │         • mTLS between services                          │
   │         • Traffic routing & load balancing               │
   │         • Circuit breakers & retries                     │
   │         • Observability (metrics, traces)                │
   └──────────┬───────────────────────────────────────────────┘
              │
        ┌─────┴─────┬─────────┬──────────┬──────────┐
        │           │         │          │          │
   ┌────▼────┐ ┌────▼────┐ ┌─▼──────┐ ┌─▼──────┐ ┌─▼──────┐
   │OS-PACS  │ │OS-PATROL│ │OS-     │ │OS-     │ │OS-     │
   │Service  │ │Service  │ │CONCIERGE││GUARDIAN│ │SENTINEL│
   │Network  │ │Network  │ │Service │ │Service │ │Service │
   │         │ │         │ │Network │ │Network │ │Network │
   └─────────┘ └─────────┘ └────────┘ └────────┘ └────────┘
```

---

## Hub Infrastructure

### Kubernetes Cluster Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│              OPENSECURE HUB KUBERNETES CLUSTER                    │
│                     (EKS / AKS / GKE)                             │
└──────────────────────────────────────────────────────────────────┘

Control Plane (Managed)
├── API Server: api.k8s.hub.internal
├── etcd: Distributed config store
├── Scheduler: Pod placement
└── Controller Manager: Maintain desired state

Worker Nodes (3 Availability Zones)
┌──────────────────┬──────────────────┬──────────────────┐
│   AZ-1 (us-e-1a) │   AZ-2 (us-e-1b) │   AZ-3 (us-e-1c) │
├──────────────────┼──────────────────┼──────────────────┤
│ Node Pool: WEB   │ Node Pool: WEB   │ Node Pool: WEB   │
│ • 3 nodes        │ • 3 nodes        │ • 3 nodes        │
│ • m5.xlarge      │ • m5.xlarge      │ • m5.xlarge      │
│ • 4 vCPU, 16GB   │ • 4 vCPU, 16GB   │ • 4 vCPU, 16GB   │
├──────────────────┼──────────────────┼──────────────────┤
│ Node Pool: API   │ Node Pool: API   │ Node Pool: API   │
│ • 3 nodes        │ • 3 nodes        │ • 3 nodes        │
│ • m5.2xlarge     │ • m5.2xlarge     │ • m5.2xlarge     │
│ • 8 vCPU, 32GB   │ • 8 vCPU, 32GB   │ • 8 vCPU, 32GB   │
├──────────────────┼──────────────────┼──────────────────┤
│ Node Pool: DATA  │ Node Pool: DATA  │ Node Pool: DATA  │
│ • 2 nodes        │ • 2 nodes        │ • 2 nodes        │
│ • r5.2xlarge     │ • r5.2xlarge     │ • r5.2xlarge     │
│ • 8 vCPU, 64GB   │ • 8 vCPU, 64GB   │ • 8 vCPU, 64GB   │
└──────────────────┴──────────────────┴──────────────────┘

Total Capacity:
├── 27 nodes across 3 AZs
├── 162 vCPUs
├── 648 GB RAM
└── Can scale to 100+ nodes

Pod Distribution (Namespace: opensecure-hub)
┌────────────────────────────────────────────────────┐
│ Deployment: hub-web (6 replicas)                   │
│ • React frontend                                   │
│ • Resource: 0.5 CPU, 1GB RAM per pod              │
│ • AntiAffinity: Spread across AZs                 │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│ Deployment: hub-api (9 replicas)                   │
│ • Node.js / FastAPI backend                        │
│ • Resource: 1 CPU, 2GB RAM per pod                │
│ • HPA: Scale 9-30 based on CPU > 70%              │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│ StatefulSet: keycloak (3 replicas)                 │
│ • Identity & Access Management                     │
│ • Resource: 2 CPU, 4GB RAM per pod                │
│ • Persistent: 20GB per pod                         │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│ StatefulSet: kafka (3 replicas)                    │
│ • Event streaming                                  │
│ • Resource: 2 CPU, 8GB RAM per pod                │
│ • Persistent: 100GB per pod                        │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│ StatefulSet: elasticsearch (3 replicas)            │
│ • Log aggregation & search                         │
│ • Resource: 4 CPU, 16GB RAM per pod               │
│ • Persistent: 500GB per pod                        │
└────────────────────────────────────────────────────┘
```

### IP Addressing Scheme (Hub Network)

```
HUB PRIMARY NETWORK: 10.0.0.0/16

VLAN 10 - Web Tier (10.0.10.0/24)
├── Load Balancer VIP: 10.0.10.5
├── Web Pods: 10.0.10.10-10.0.10.50
├── CDN Origin Shield: 10.0.10.100
└── Gateway: 10.0.10.1

VLAN 20 - API Tier (10.0.20.0/24)
├── API Gateway: 10.0.20.5
├── API Pods: 10.0.20.10-10.0.20.100
├── WebSocket Server: 10.0.20.200
└── Gateway: 10.0.20.1

VLAN 30 - Data Tier (10.0.30.0/24)
├── PostgreSQL Primary: 10.0.30.10
├── PostgreSQL Replicas: 10.0.30.11-10.0.30.13
├── Redis Cluster: 10.0.30.20-10.0.30.25
├── Kafka Brokers: 10.0.30.30-10.0.30.32
├── Elasticsearch: 10.0.30.40-10.0.30.42
└── Gateway: 10.0.30.1

VLAN 40 - Management (10.0.40.0/24)
├── Bastion Host: 10.0.40.10
├── Prometheus: 10.0.40.20
├── Grafana: 10.0.40.21
├── GitLab Runner: 10.0.40.30
└── Gateway: 10.0.40.1

VLAN 50 - Service Integration (10.0.50.0/24)
├── OS-PACS Gateway: 10.0.50.10
├── OS-PATROL Gateway: 10.0.50.11
├── OS-CONCIERGE Gateway: 10.0.50.12
├── OS-GUARDIAN Gateway: 10.0.50.13
├── OS-SENTINEL Gateway: 10.0.50.14
└── Gateway: 10.0.50.1

SERVICE NETWORKS (Each service has /16)
├── OS-PACS: 10.100.0.0/16
├── OS-PATROL: 10.110.0.0/16
├── OS-CONCIERGE: 10.120.0.0/16
├── OS-GUARDIAN: 10.130.0.0/16
└── OS-SENTINEL: 10.140.0.0/16
```

---

## Service Integration Network

### Hub-to-Service Communication

```
┌──────────────────────────────────────────────────────────────┐
│         SERVICE INTEGRATION ARCHITECTURE                      │
└──────────────────────────────────────────────────────────────┘

OpenSecure Hub (10.0.0.0/16)
        │
        │ Service Mesh (mTLS)
        │
        ├─────────────────────────────────────────┐
        │                                         │
   ┌────▼────────────────┐             ┌─────────▼──────────┐
   │ Hub API Gateway     │             │ Event Router       │
   │ (Kong / APISIX)     │             │ (Kafka Connect)    │
   │ 10.0.20.5           │             │ 10.0.30.30         │
   └────┬────────────────┘             └─────────┬──────────┘
        │                                        │
        │ REST / gRPC                            │ Event Streaming
        │                                        │
        ├──────────┬──────────┬──────────┬──────┴─────┐
        │          │          │          │            │
   ┌────▼───┐ ┌───▼────┐ ┌───▼────┐ ┌──▼─────┐ ┌────▼─────┐
   │OS-PACS │ │OS-     │ │OS-     │ │OS-     │ │OS-       │
   │API     │ │PATROL  │ │CONCIERGE││GUARDIAN│ │SENTINEL  │
   │        │ │API     │ │API     │ │API     │ │API       │
   │10.100. │ │10.110. │ │10.120. │ │10.130. │ │10.140.   │
   │0.10    │ │0.10    │ │0.10    │ │0.10    │ │0.10      │
   └────────┘ └────────┘ └────────┘ └────────┘ └──────────┘

Communication Patterns:

1. SYNCHRONOUS (REST API)
   Hub → Service API Request
   ├── Authentication: JWT token (issued by Hub Keycloak)
   ├── Authorization: Service validates token
   ├── Request: POST /api/v1/users
   ├── Response: 201 Created
   └── Timeout: 30 seconds

2. ASYNCHRONOUS (Event Streaming)
   Service → Kafka → Hub Event Consumer
   ├── Topic: opensecure.pacs.access_granted
   ├── Payload: {user_id, door_id, timestamp, ...}
   ├── Hub processes: Update analytics, trigger correlations
   └── Latency: <500ms

3. REAL-TIME (WebSocket)
   Hub Dashboard ← WebSocket ← Service Events
   ├── Connection: wss://hub.opensecure.com/ws
   ├── Subscribe: /events/pacs/*, /events/patrol/*
   ├── Push: Real-time event updates
   └── Heartbeat: Every 30 seconds

Network Policies (Kubernetes NetworkPolicy)
┌──────────────────────────────────────────────────┐
│ FROM: hub-api pods (10.0.20.0/24)                │
│ TO: os-pacs-api.pacs.svc.cluster.local:8080     │
│ ALLOW: TCP 8080, 8443                            │
│ PROTOCOL: HTTPS only (mTLS)                      │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│ FROM: os-pacs-kafka-producer                     │
│ TO: hub-kafka.hub.svc.cluster.local:9092        │
│ ALLOW: TCP 9092 (Kafka)                          │
│ PROTOCOL: SASL_SSL                               │
└──────────────────────────────────────────────────┘
```

### Cross-Service Event Correlation

```python
# Hub Event Correlation Engine

class EventCorrelationEngine:
    def __init__(self):
        self.kafka_consumer = KafkaConsumer([
            'opensecure.pacs.*',
            'opensecure.patrol.*',
            'opensecure.sentinel.*',
            'opensecure.concierge.*',
            'opensecure.guardian.*'
        ])
        
        self.correlation_rules = self.load_correlation_rules()
    
    def process_event(self, event):
        """Process incoming event and check for correlations"""
        
        # Store event in time-series database
        self.store_event(event)
        
        # Check correlation rules
        for rule in self.correlation_rules:
            if self.matches_rule(event, rule):
                self.trigger_correlation(event, rule)
    
    def load_correlation_rules(self):
        """Load correlation rules from configuration"""
        return [
            {
                'name': 'Unauthorized Access + Loitering',
                'conditions': [
                    {
                        'service': 'OS-PACS',
                        'event_type': 'access_denied',
                        'time_window': '5m'
                    },
                    {
                        'service': 'OS-SENTINEL',
                        'event_type': 'person_loitering',
                        'location': 'same_zone',
                        'time_window': '5m'
                    }
                ],
                'action': {
                    'create_incident': True,
                    'severity': 'HIGH',
                    'notify': ['security_team'],
                    'dispatch': 'nearest_patrol_unit'
                }
            },
            {
                'name': 'Stolen Vehicle + Parking Entry',
                'conditions': [
                    {
                        'service': 'OS-PATROL',
                        'event_type': 'lpr_hot_list_match',
                        'reason': 'stolen_vehicle'
                    },
                    {
                        'service': 'OS-SENTINEL',
                        'event_type': 'vehicle_entered',
                        'location': 'parking_lot',
                        'time_window': '2m'
                    }
                ],
                'action': {
                    'create_incident': True,
                    'severity': 'CRITICAL',
                    'notify': ['security_team', 'law_enforcement'],
                    'lock_barriers': True  # OS-PACS integration
                }
            },
            {
                'name': 'Visitor + Access Request',
                'conditions': [
                    {
                        'service': 'OS-CONCIERGE',
                        'event_type': 'visitor_checked_in',
                        'time_window': '10m'
                    },
                    {
                        'service': 'OS-PACS',
                        'event_type': 'access_request',
                        'credential_type': 'visitor_badge'
                    }
                ],
                'action': {
                    'auto_grant_access': True,
                    'notify_host': True,
                    'log_visit': True
                }
            }
        ]

# Example correlation flow:

# Event 1 arrives (from OS-PACS):
{
    "service": "OS-PACS",
    "event_type": "access_denied",
    "timestamp": "2024-12-08T14:23:45Z",
    "door_id": "DOOR_123",
    "user_id": "unknown",
    "zone": "RESTRICTED_AREA_A",
    "credential": "1234567890"
}

# Event 2 arrives 3 minutes later (from OS-SENTINEL):
{
    "service": "OS-SENTINEL",
    "event_type": "person_loitering",
    "timestamp": "2024-12-08T14:26:15Z",
    "camera_id": "CAM_045",
    "zone": "RESTRICTED_AREA_A",
    "duration": 120,  # seconds
    "person_id": "track_98765"
}

# Hub correlates:
# ✓ Same zone (RESTRICTED_AREA_A)
# ✓ Within 5-minute window
# ✓ Suspicious pattern: access denied + loitering

# Hub creates unified incident:
{
    "incident_id": "INC-2024-12-08-001",
    "severity": "HIGH",
    "title": "Unauthorized Access Attempt + Loitering",
    "description": "Person denied access to restricted area, then observed loitering nearby",
    "events": [
        {"service": "OS-PACS", "event_id": "..."},
        {"service": "OS-SENTINEL", "event_id": "..."}
    ],
    "actions_taken": [
        "Notified security team",
        "Dispatched patrol unit #12 (ETA: 2 minutes)",
        "Locked down adjacent doors"
    ],
    "assigned_to": "security_officer_jane"
}
```

---

## Multi-Tenant Architecture

### Tenant Isolation Strategy

```
┌──────────────────────────────────────────────────────────────┐
│              MULTI-TENANT ISOLATION MODEL                     │
└──────────────────────────────────────────────────────────────┘

Tenant 1: Acme Corp
├── Tenant ID: tenant_acme_001
├── Subdomain: acme.hub.opensecure.com
├── Kubernetes Namespace: tenant-acme-001
├── Database: acme_opensecure (PostgreSQL schema)
├── Object Storage: s3://opensecure-tenant-acme/
├── Network Isolation: Calico NetworkPolicy
└── Services Enabled: OS-PACS, OS-SENTINEL, OS-CONCIERGE

Tenant 2: GlobalTech Inc
├── Tenant ID: tenant_globaltech_002
├── Subdomain: globaltech.hub.opensecure.com
├── Kubernetes Namespace: tenant-globaltech-002
├── Database: globaltech_opensecure (PostgreSQL schema)
├── Object Storage: s3://opensecure-tenant-globaltech/
├── Network Isolation: Calico NetworkPolicy
└── Services Enabled: All 5 services

Tenant 3: SecureBuildings LLC
├── Tenant ID: tenant_securebuildings_003
├── Subdomain: securebuildings.hub.opensecure.com
├── Kubernetes Namespace: tenant-securebuildings-003
├── Database: securebuildings_opensecure (PostgreSQL schema)
├── Object Storage: s3://opensecure-tenant-securebuildings/
├── Network Isolation: Calico NetworkPolicy
└── Services Enabled: OS-PACS, OS-PATROL

Data Isolation (PostgreSQL):
┌──────────────────────────────────────────────────┐
│ CREATE SCHEMA tenant_acme_001;                   │
│ CREATE SCHEMA tenant_globaltech_002;             │
│ CREATE SCHEMA tenant_securebuildings_003;        │
│                                                  │
│ SET search_path = tenant_acme_001;               │
│ -- All queries now scoped to tenant schema      │
│                                                  │
│ Row-Level Security (RLS):                        │
│ ALTER TABLE users ENABLE ROW LEVEL SECURITY;     │
│ CREATE POLICY tenant_isolation ON users         │
│   USING (tenant_id = current_setting('app.tenant_id')); │
└──────────────────────────────────────────────────┘

Network Isolation (Kubernetes NetworkPolicy):
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: tenant-acme-isolation
  namespace: tenant-acme-001
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          tenant: acme-001
    - podSelector: {}
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: opensecure-hub  # Allow hub access
    - podSelector: {}

Resource Quotas (per tenant):
apiVersion: v1
kind: ResourceQuota
metadata:
  name: tenant-acme-quota
  namespace: tenant-acme-001
spec:
  hard:
    requests.cpu: "20"      # 20 vCPUs
    requests.memory: 64Gi   # 64 GB RAM
    persistentvolumeclaims: "10"
    pods: "100"
    services.loadbalancers: "2"
```

---

## Security Architecture

### Defense-in-Depth Security Model

```
┌──────────────────────────────────────────────────────────────┐
│                  SECURITY LAYERS                              │
└──────────────────────────────────────────────────────────────┘

Layer 1: Edge Security (Internet → Hub)
├── DDoS Protection: CloudFlare (100 Gbps mitigation)
├── WAF: OWASP Top 10 protection
├── TLS 1.3: Perfect forward secrecy
├── Certificate Pinning: Prevent MITM
└── Rate Limiting: 1000 req/min per IP

Layer 2: Network Security (Hub Infrastructure)
├── VPC: Private subnets (10.0.0.0/16)
├── Security Groups: Stateful firewall rules
├── NACLs: Stateless subnet-level filtering
├── VPN: WireGuard for service-to-service
└── Zero Trust: All traffic authenticated

Layer 3: Application Security (Services)
├── Authentication: OAuth2 + JWT tokens
├── Authorization: RBAC with least privilege
├── MFA: Required for admin access
├── Session Management: 1-hour token expiry
└── API Security: Request signing, replay protection

Layer 4: Data Security (At Rest & In Transit)
├── Encryption at Rest: AES-256 (all databases)
├── Encryption in Transit: TLS 1.3 (all connections)
├── Key Management: AWS KMS / HashiCorp Vault
├── Data Masking: PII redaction in logs
└── Backup Encryption: GPG encrypted backups

Layer 5: Monitoring & Response
├── SIEM: Elasticsearch + Kibana
├── Intrusion Detection: Suricata IDS
├── Log Aggregation: Fluentd → Elasticsearch
├── Anomaly Detection: ML-based behavioral analysis
└── Incident Response: 24/7 SOC

Firewall Rules (Security Groups):

Hub Web Tier (SG-HUB-WEB):
┌──────────────────────────────────────────────────┐
│ INBOUND:                                         │
│ • 443 (HTTPS) from 0.0.0.0/0 (CloudFlare IPs)   │
│ • 80 (HTTP) from 0.0.0.0/0 → redirect to 443    │
│                                                  │
│ OUTBOUND:                                        │
│ • All traffic to 10.0.20.0/24 (API tier)        │
│ • 443 to 0.0.0.0/0 (external APIs)              │
└──────────────────────────────────────────────────┘

Hub API Tier (SG-HUB-API):
┌──────────────────────────────────────────────────┐
│ INBOUND:                                         │
│ • 8080 from 10.0.10.0/24 (Web tier)             │
│ • 8443 from 10.0.50.0/24 (Service integration)  │
│                                                  │
│ OUTBOUND:                                        │
│ • 5432 to 10.0.30.0/24 (Database)               │
│ • 6379 to 10.0.30.0/24 (Redis)                  │
│ • 9092 to 10.0.30.0/24 (Kafka)                  │
│ • 8080-8443 to 10.100-140.0.0/16 (Services)     │
└──────────────────────────────────────────────────┘

Hub Data Tier (SG-HUB-DATA):
┌──────────────────────────────────────────────────┐
│ INBOUND:                                         │
│ • 5432 (PostgreSQL) from 10.0.20.0/24 only      │
│ • 6379 (Redis) from 10.0.20.0/24 only           │
│ • 9092 (Kafka) from 10.0.20.0/24, 10.0.50.0/24  │
│                                                  │
│ OUTBOUND:                                        │
│ • DENY all (data tier should not initiate)      │
└──────────────────────────────────────────────────┘
```

---

## High Availability & Disaster Recovery

### HA Architecture

```
┌──────────────────────────────────────────────────────────────┐
│         HIGH AVAILABILITY CONFIGURATION                       │
└──────────────────────────────────────────────────────────────┘

Multi-AZ Deployment (Active-Active)
Region: us-east-1
├── AZ-1 (us-east-1a): Primary
│   ├── Web Pods: 2 replicas
│   ├── API Pods: 3 replicas
│   ├── PostgreSQL: Primary
│   └── Kafka: Broker 1
├── AZ-2 (us-east-1b): Secondary
│   ├── Web Pods: 2 replicas
│   ├── API Pods: 3 replicas
│   ├── PostgreSQL: Sync Replica
│   └── Kafka: Broker 2
└── AZ-3 (us-east-1c): Tertiary
    ├── Web Pods: 2 replicas
    ├── API Pods: 3 replicas
    ├── PostgreSQL: Async Replica
    └── Kafka: Broker 3

Load Balancer Health Checks:
├── Interval: 10 seconds
├── Timeout: 5 seconds
├── Unhealthy Threshold: 2 consecutive failures
├── Healthy Threshold: 2 consecutive successes
└── Endpoint: GET /health (returns 200 OK)

Database Failover (PostgreSQL + Patroni):
├── Detection: Patroni health check every 10s
├── Failover Time: <30 seconds
├── Promotion: Synchronous replica → Primary
├── Connection String: VIP (10.0.30.5) follows primary
└── Zero Data Loss: Synchronous replication

Kubernetes Pod Disruption Budgets:
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: hub-api-pdb
spec:
  minAvailable: 6  # Always keep 6/9 API pods
  selector:
    matchLabels:
      app: hub-api

RTO (Recovery Time Objective): 15 minutes
RPO (Recovery Point Objective): 5 minutes (async replication lag)
```

### Disaster Recovery

```
┌──────────────────────────────────────────────────────────────┐
│         DISASTER RECOVERY ARCHITECTURE                        │
└──────────────────────────────────────────────────────────────┘

Primary Region: us-east-1 (N. Virginia)
Secondary Region: us-west-2 (Oregon)

Cross-Region Replication:
├── Database: Streaming replication (lag: <5 minutes)
├── Object Storage: S3 cross-region replication (minutes)
├── Configuration: Git-based, replicated via GitOps
└── Container Images: Multi-region ECR replication

Disaster Scenarios:

Scenario 1: Single AZ Failure
├── Impact: 33% capacity reduction
├── Auto-healing: Pods reschedule to healthy AZs
├── User Impact: None (remaining AZs handle load)
└── Recovery: Automatic (5-10 minutes)

Scenario 2: Entire Region Failure
├── Impact: Complete primary region outage
├── Activation: DNS failover to us-west-2 (TTL: 60s)
├── User Impact: 2-5 minute service interruption
├── Data Loss: Up to 5 minutes (RPO)
└── Recovery: Manual activation of DR site

DR Activation Procedure:
1. Declare disaster (P1 incident)
2. Promote DR database to primary
3. Update DNS: hub.opensecure.com → us-west-2 ALB
4. Scale up DR Kubernetes cluster (30 mins)
5. Verify service health
6. Notify customers (status page)

DR Testing:
├── Frequency: Quarterly
├── Type: Simulated failover (non-production)
├── Duration: 4 hours
└── Success Criteria: RTO <15 min, RPO <5 min
```

---

## Monitoring & Operations

### Observability Stack

```
┌──────────────────────────────────────────────────────────────┐
│              MONITORING & OBSERVABILITY                       │
└──────────────────────────────────────────────────────────────┘

Metrics (Prometheus + Grafana)
├── Prometheus: Time-series metrics database
│   ├── Scrape Interval: 15 seconds
│   ├── Retention: 30 days
│   ├── Storage: 500 GB
│   └── Targets: 200+ (all pods, nodes, services)
├── Grafana: Visualization & dashboards
│   ├── Dashboards: 50+ pre-built
│   ├── Alerts: 100+ alert rules
│   └── Users: LDAP integration

Key Metrics Monitored:
├── Hub API Response Time (p50, p95, p99)
├── Request Rate (req/sec per service)
├── Error Rate (% of 5xx responses)
├── Database Connection Pool Utilization
├── Kafka Consumer Lag
├── Pod CPU & Memory Usage
├── Node Disk I/O
└── Network Throughput

Logging (ELK Stack)
├── Fluentd: Log collection from all pods
├── Elasticsearch: Log storage & search
│   ├── Index: daily (opensecure-YYYY-MM-DD)
│   ├── Retention: 90 days
│   ├── Storage: 2 TB
├── Kibana: Log visualization & analysis
│   ├── Saved Searches: 30+
│   ├── Dashboards: 20+

Distributed Tracing (Jaeger)
├── Trace Sampling: 10% of requests
├── Retention: 7 days
├── Use Case: Debug cross-service latency
└── Integration: Automatic via Istio sidecar

Alerting (Prometheus Alertmanager)
┌──────────────────────────────────────────────────┐
│ Alert: HighAPIErrorRate                          │
│ Condition: error_rate > 5% for 5 minutes        │
│ Severity: Critical                               │
│ Action: Page on-call engineer                    │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│ Alert: DatabaseReplicationLag                    │
│ Condition: lag > 1 minute for 10 minutes        │
│ Severity: Warning                                │
│ Action: Email DBA team                           │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│ Alert: KafkaConsumerLag                          │
│ Condition: lag > 10,000 messages for 15 minutes │
│ Severity: Warning                                │
│ Action: Slack #ops-alerts                        │
└──────────────────────────────────────────────────┘
```

---

## Deployment Scenarios

### Small Enterprise (50-500 Users)

```
Infrastructure:
├── Kubernetes: Single region, 2 AZs
├── Nodes: 9 nodes (3 per AZ)
├── Database: 1 primary + 1 replica
├── Object Storage: 1 TB
└── Monthly Cost: $5,000

Capacity:
├── Users: 500 concurrent
├── API Requests: 10,000/hour
├── Events: 100,000/day
└── Services: All 5 enabled
```

### Mid-Market (500-5,000 Users)

```
Infrastructure:
├── Kubernetes: Single region, 3 AZs
├── Nodes: 27 nodes (9 per AZ)
├── Database: 1 primary + 2 replicas
├── Object Storage: 10 TB
└── Monthly Cost: $25,000

Capacity:
├── Users: 5,000 concurrent
├── API Requests: 100,000/hour
├── Events: 1,000,000/day
└── Services: All 5 enabled
```

### Enterprise (5,000+ Users)

```
Infrastructure:
├── Kubernetes: Multi-region (us-east + us-west)
├── Nodes: 100+ nodes
├── Database: Clustered (Patroni + Citus sharding)
├── Object Storage: 100+ TB
└── Monthly Cost: $150,000+

Capacity:
├── Users: 50,000+ concurrent
├── API Requests: 1,000,000/hour
├── Events: 10,000,000/day
└── Services: All 5 enabled, custom integrations
```

---

## Appendix

### Network Equipment BOM (Hub Infrastructure)

| Component | Purpose | Quantity | Unit Price | Total |
|-----------|---------|----------|------------|-------|
| AWS EKS Cluster | Kubernetes control plane | 1 | $73/mo | $73/mo |
| m5.xlarge nodes | Web tier | 9 | $140/mo | $1,260/mo |
| m5.2xlarge nodes | API tier | 9 | $280/mo | $2,520/mo |
| r5.2xlarge nodes | Data tier | 6 | $365/mo | $2,190/mo |
| Application Load Balancer | Traffic distribution | 2 | $23/mo | $46/mo |
| NAT Gateway | Outbound connectivity | 3 | $33/mo | $99/mo |
| RDS PostgreSQL (r5.2xlarge) | Primary database | 1 | $550/mo | $550/mo |
| RDS Read Replica | Database replicas | 2 | $550/mo | $1,100/mo |
| ElastiCache Redis | Caching layer | 3 nodes | $85/mo | $255/mo |
| S3 Storage | Object storage | 10 TB | $23/TB | $230/mo |
| CloudFront CDN | Content delivery | 1 | $200/mo | $200/mo |
| Route 53 | DNS management | 1 | $1/mo | $1/mo |
| **TOTAL** | | | | **$8,524/mo** |

### Key Performance Indicators

| Metric | Target | Measurement |
|--------|--------|-------------|
| Uptime SLA | 99.9% | Monthly |
| API Response Time (p95) | <500ms | Real-time |
| Event Processing Latency | <2s | Real-time |
| Database Query Time (p95) | <100ms | Real-time |
| Incident Response Time | <15min | Per incident |
| Mean Time to Recovery (MTTR) | <30min | Per incident |

---

**Document Version**: 1.0  
**Last Updated**: December 2024  
**Next Document**: [OpenSecure Hub Logical Topology](./OpenSecure_Hub_Logical_Topology.md)

**Related Documents**:
- [OS-PACS Network Topology](./OS-PACS_Network_Topology.md)
- [OS-PATROL Network Topology](./OS-PATROL_Network_Topology.md)
- [OS-CONCIERGE Network Topology](./OS-CONCIERGE_Network_Topology.md)
- [OS-GUARDIAN Network Topology](./OS-GUARDIAN_Network_Topology.md)
- [OS-SENTINEL Network Topology](./OS-SENTINEL_Network_Topology.md)
