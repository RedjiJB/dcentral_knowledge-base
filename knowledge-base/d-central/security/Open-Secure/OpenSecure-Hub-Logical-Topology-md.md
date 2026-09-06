---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: f5509eaf-4038-4527-830f-a4eb30897180
original_filename: OpenSecure_Hub_Logical_Topology.md
created_at: 2026-03-04T20:34:32.742894+00:00
content_hash: 05d06b1b5704
topic: "opensecure-topology-documentation-suite"
consolidated_into: docs/DC-OPENSECURE-TOPOLOGY-DOCUMENTATION-SUITE-RECONCILED-001.md
---

# OpenSecure Hub Logical Topology
## Unified Management Platform System Architecture & Integration Logic

**Document Type**: Logical Architecture Specification  
**Version**: 1.0  
**Date**: December 2024  
**Classification**: Technical Documentation  
**Audience**: Solution Architects, Integration Engineers, Platform Engineers

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Logical Architecture Overview](#logical-architecture-overview)
3. [Identity & Access Management](#identity--access-management)
4. [Unified API Gateway](#unified-api-gateway)
5. [Event Correlation Engine](#event-correlation-engine)
6. [Cross-Service Analytics](#cross-service-analytics)
7. [Data Flow Patterns](#data-flow-patterns)
8. [State Management](#state-management)
9. [Integration Patterns](#integration-patterns)
10. [API Architecture](#api-architecture)

---

## Executive Summary

### Architectural Philosophy

The OpenSecure Hub implements a **federation architecture** that provides unified management while preserving service autonomy. Core principles:

- **Single Pane of Glass**: One dashboard for all security operations
- **Federated Identity**: Centralized authentication, distributed authorization
- **Event-Driven**: Real-time cross-service correlation
- **Service Autonomy**: Each service operates independently
- **Unified API**: Single endpoint for all operations
- **Multi-Tenant**: Isolated customer environments

### Hub Value Through Integration

| Without Hub | With Hub | Improvement |
|-------------|----------|-------------|
| 5 separate logins | 1 SSO login | 80% time savings |
| Manual correlation | Automated AI correlation | 95% faster incident detection |
| 5 disparate reports | Unified analytics | 10× better insights |
| Siloed data | Cross-service data lake | Complete operational picture |
| Manual workflows | Automated workflows | 70% efficiency gain |

---

## Logical Architecture Overview

### Hub Logical Layers

```
┌────────────────────────────────────────────────────────────────┐
│                 LAYER 5: EXPERIENCE LAYER                       │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │           Unified Dashboard (React)                      │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │  │
│  │  │ Command  │  │Analytics │  │  Alerts  │  │Reports │ │  │
│  │  │ Center   │  │Dashboard │  │  Feed    │  │Builder │ │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └────────┘ │  │
│  └─────────────────────────────────────────────────────────┘  │
└────────────────────────────┬───────────────────────────────────┘
                             │ HTTPS / WebSocket
┌────────────────────────────▼───────────────────────────────────┐
│                 LAYER 4: ORCHESTRATION LAYER                    │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              Workflow Automation Engine                   │ │
│  │  • Cross-service workflows                               │ │
│  │  • Event-triggered actions                               │ │
│  │  • Approval processes                                    │ │
│  │  • SLA management                                        │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────┬───────────────────────────────────┘
                             │
┌────────────────────────────▼───────────────────────────────────┐
│                 LAYER 3: INTEGRATION LAYER                      │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │   IAM    │  │   API    │  │  Event   │  │Analytics │     │
│  │Federation│  │ Gateway  │  │Correlation│  │  Engine  │     │
│  │(Keycloak)│  │ (Kong)   │  │ (Kafka)  │  │(Grafana) │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
└────────────────────────────┬───────────────────────────────────┘
                             │
┌────────────────────────────▼───────────────────────────────────┐
│                 LAYER 2: DATA LAYER                             │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │            Unified Data Lake                              │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │ │
│  │  │PostgreSQL│  │ClickHouse│  │  MinIO   │              │ │
│  │  │(OLTP)    │  │ (OLAP)   │  │ (Objects)│              │ │
│  │  └──────────┘  └──────────┘  └──────────┘              │ │
│  │                                                          │ │
│  │  Data Models:                                           │ │
│  │  • Unified user directory                               │ │
│  │  • Cross-service events                                 │ │
│  │  • Correlation graph                                    │ │
│  │  • Aggregated analytics                                 │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────┬───────────────────────────────────┘
                             │
┌────────────────────────────▼───────────────────────────────────┐
│                 LAYER 1: SERVICE LAYER                          │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ OS-PACS  │  │OS-PATROL │  │OS-       │  │OS-       │     │
│  │          │  │          │  │CONCIERGE │  │GUARDIAN  │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
│  ┌──────────┐                                                 │
│  │OS-       │                                                 │
│  │SENTINEL  │                                                 │
│  └──────────┘                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Identity & Access Management

### Federated Identity Architecture

```
┌──────────────────────────────────────────────────────────────┐
│           FEDERATED IDENTITY MANAGEMENT                       │
└──────────────────────────────────────────────────────────────┘

Keycloak (Hub Identity Provider)
        │
        │ Users authenticate once
        │
        ▼
┌─────────────────────────┐
│ User Login               │
│ • Username/Email        │
│ • Password              │
│ • MFA (TOTP/SMS)        │
└──────────┬──────────────┘
           │
           │ Authentication successful
           │
           ▼
┌─────────────────────────┐
│ JWT Token Issued        │
│ {                       │
│   "sub": "user_12345",  │
│   "email": "john@acme", │
│   "tenant": "acme_001", │
│   "roles": [            │
│     "hub:admin",        │
│     "pacs:operator",    │
│     "sentinel:viewer"   │
│   ],                    │
│   "exp": 1735689825     │
│ }                       │
└──────────┬──────────────┘
           │
           │ User accesses service
           │
           ▼
┌─────────────────────────────────────────────┐
│ Token Validation (at each service)          │
│                                             │
│ Service receives token                      │
│ ↓                                           │
│ Verify signature (RS256)                    │
│ ↓                                           │
│ Check expiration                            │
│ ↓                                           │
│ Validate tenant_id matches request          │
│ ↓                                           │
│ Check service-specific roles:               │
│ • "pacs:operator" → Can view, cannot edit  │
│ • "sentinel:viewer" → Read-only access     │
│ ↓                                           │
│ Grant/Deny access                           │
└─────────────────────────────────────────────┘

Role-Based Access Control (RBAC) Model:

Hub Roles:
├── hub:super_admin (Full access to everything)
├── hub:admin (Tenant administration)
├── hub:operator (Day-to-day operations)
├── hub:viewer (Read-only access)
└── hub:auditor (Audit log access only)

Service-Specific Roles:
├── pacs:admin (Full OS-PACS management)
├── pacs:operator (Grant/deny access, view events)
├── pacs:viewer (View-only)
├── patrol:admin (Fleet management)
├── patrol:dispatcher (Assign vehicles, view locations)
├── patrol:viewer (View-only)
├── sentinel:admin (Camera management, configure analytics)
├── sentinel:operator (View live streams, search recordings)
├── sentinel:viewer (View-only)
├── concierge:admin (Property management)
├── concierge:operator (Check-in visitors, manage packages)
├── guardian:admin (Evidence management, policies)
└── guardian:officer (Record footage, upload evidence)

Permission Matrix Example:

Action: "Create new user in OS-PACS"
Required Roles: hub:admin OR pacs:admin

Action: "View live camera stream in OS-SENTINEL"
Required Roles: hub:operator OR sentinel:operator OR sentinel:viewer

Action: "Dispatch patrol vehicle"
Required Roles: hub:operator OR patrol:dispatcher OR patrol:admin

Action: "Download body camera footage"
Required Roles: hub:admin OR guardian:admin (with case # reference)
```

### Single Sign-On (SSO) Integration

```python
class SSOIntegration:
    """Hub SSO integration with external identity providers"""
    
    def __init__(self):
        self.keycloak = KeycloakClient(
            server_url='https://auth.opensecure.com',
            realm='opensecure'
        )
    
    def configure_saml_idp(self, tenant_id, idp_config):
        """Configure SAML 2.0 identity provider"""
        
        # Example: Integrate with Okta, Azure AD, Google Workspace
        
        realm = self.keycloak.get_realm(tenant_id)
        
        realm.add_identity_provider({
            'alias': idp_config['name'],
            'providerId': 'saml',
            'enabled': True,
            'config': {
                'singleSignOnServiceUrl': idp_config['sso_url'],
                'signingCertificate': idp_config['certificate'],
                'nameIDPolicyFormat': 'urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress',
                'wantAuthnRequestsSigned': 'true'
            }
        })
        
        # Map IdP attributes to Hub roles
        realm.add_identity_provider_mapper({
            'name': 'role-mapper',
            'identityProviderAlias': idp_config['name'],
            'identityProviderMapper': 'saml-role-idp-mapper',
            'config': {
                'attribute.name': 'Role',
                'attribute.friendly.name': 'Role',
                'role': 'hub:admin'
            }
        })
    
    def configure_oidc_idp(self, tenant_id, idp_config):
        """Configure OpenID Connect identity provider"""
        
        realm = self.keycloak.get_realm(tenant_id)
        
        realm.add_identity_provider({
            'alias': idp_config['name'],
            'providerId': 'oidc',
            'enabled': True,
            'config': {
                'clientId': idp_config['client_id'],
                'clientSecret': idp_config['client_secret'],
                'authorizationUrl': idp_config['auth_url'],
                'tokenUrl': idp_config['token_url'],
                'userInfoUrl': idp_config['userinfo_url'],
                'jwksUrl': idp_config['jwks_url']
            }
        })

# Usage:
sso = SSOIntegration()

# Example: Integrate with Azure AD
sso.configure_saml_idp('tenant_acme_001', {
    'name': 'azure-ad',
    'sso_url': 'https://login.microsoftonline.com/...',
    'certificate': '...'
})

# Example: Integrate with Okta
sso.configure_oidc_idp('tenant_acme_001', {
    'name': 'okta',
    'client_id': 'abc123',
    'client_secret': '...',
    'auth_url': 'https://acme.okta.com/oauth2/v1/authorize',
    'token_url': 'https://acme.okta.com/oauth2/v1/token',
    'userinfo_url': 'https://acme.okta.com/oauth2/v1/userinfo',
    'jwks_url': 'https://acme.okta.com/oauth2/v1/keys'
})
```

---

## Unified API Gateway

### API Routing Architecture

```
┌──────────────────────────────────────────────────────────────┐
│              UNIFIED API GATEWAY (Kong)                       │
└──────────────────────────────────────────────────────────────┘

Client Request: 
GET https://api.opensecure.com/pacs/v1/doors

        │
        │ 1. Request arrives at API Gateway
        ▼
┌─────────────────────────┐
│ Request Validation      │
│ • Check API key         │
│ • Verify JWT token      │
│ • Rate limit check      │
│ • Schema validation     │
└──────────┬──────────────┘
           │
           │ 2. Authentication
           ▼
┌─────────────────────────┐
│ JWT Token Decode        │
│ Extract:                │
│ • tenant_id: acme_001   │
│ • user_id: user_12345   │
│ • roles: [pacs:admin]   │
└──────────┬──────────────┘
           │
           │ 3. Service Routing
           ▼
┌─────────────────────────────────────┐
│ Route to OS-PACS Service            │
│                                     │
│ URL: /pacs/v1/doors                 │
│ → Forward to: pacs.svc:8080/v1/doors│
│                                     │
│ Add Headers:                        │
│ • X-Tenant-ID: acme_001             │
│ • X-User-ID: user_12345             │
│ • X-User-Roles: pacs:admin          │
└──────────┬────────────────────────────┘
           │
           │ 4. Service processes request
           ▼
┌─────────────────────────┐
│ OS-PACS Service         │
│ • Validates tenant_id   │
│ • Checks authorization  │
│ • Executes query        │
│ • Returns response      │
└──────────┬──────────────┘
           │
           │ 5. Response transformation
           ▼
┌─────────────────────────┐
│ API Gateway             │
│ • Log request/response  │
│ • Transform if needed   │
│ • Add correlation ID    │
│ • Return to client      │
└──────────┬──────────────┘
           │
           ▼
Client receives:
{
  "doors": [
    {"id": 1, "name": "Main Entrance", ...},
    {"id": 2, "name": "Parking Gate", ...}
  ],
  "total": 2,
  "correlation_id": "abc-123-def"
}

API Gateway Plugins (Kong):

1. Authentication Plugins:
   ├── JWT (RS256 signature verification)
   ├── API Key (for service-to-service)
   └── OAuth 2.0 (for third-party integrations)

2. Traffic Control:
   ├── Rate Limiting (per tenant, per user)
   ├── Request Size Limiting (10 MB max)
   └── Response Caching (Redis)

3. Security:
   ├── IP Restriction (whitelist/blacklist)
   ├── CORS (cross-origin policy)
   └── Bot Detection (challenge suspicious traffic)

4. Transformation:
   ├── Request/Response transformation
   ├── GraphQL to REST proxy
   └── Protocol upgrade (HTTP → gRPC)

5. Observability:
   ├── Logging (all requests)
   ├── Metrics (Prometheus)
   └── Distributed Tracing (Jaeger)
```

### API Versioning Strategy

```
API Version Management:

Current Version: v1
Legacy Support: v1 (supported), v0 (deprecated, EOL: 2025-06-01)
Next Version: v2 (beta, available at /beta/*)

Version Routing:
├── /pacs/v1/* → OS-PACS service (stable)
├── /pacs/v2/* → OS-PACS service v2 (new features)
├── /patrol/v1/* → OS-PATROL service
└── /sentinel/v1/* → OS-SENTINEL service

Backward Compatibility:
├── /v0/* → Transform to v1 format internally
├── /v1/* → Native format
└── /v2/* → Extended format (superset of v1)

Deprecation Process:
1. Announce deprecation (6 months notice)
2. Add deprecation warnings to responses
3. Monitor usage (Grafana dashboard)
4. Migrate customers to new version
5. Sunset old version after 6 months
```

---

## Event Correlation Engine

### Real-Time Event Processing

```
┌──────────────────────────────────────────────────────────────┐
│           EVENT CORRELATION ARCHITECTURE                      │
└──────────────────────────────────────────────────────────────┘

Service Events → Kafka Topics → Correlation Engine → Unified Incidents

Step 1: Event Ingestion
Services publish events to Kafka:

OS-PACS → Topic: opensecure.pacs.events
{
  "event_type": "access_denied",
  "timestamp": "2024-12-08T14:23:45Z",
  "tenant_id": "acme_001",
  "door_id": "DOOR_123",
  "credential_id": "BADGE_456",
  "user_id": "unknown",
  "zone": "RESTRICTED_A"
}

OS-SENTINEL → Topic: opensecure.sentinel.events
{
  "event_type": "person_detected",
  "timestamp": "2024-12-08T14:24:00Z",
  "tenant_id": "acme_001",
  "camera_id": "CAM_789",
  "zone": "RESTRICTED_A",
  "person_id": "track_12345",
  "behavior": "loitering"
}

Step 2: Event Stream Processing (Kafka Streams)

class EventCorrelator:
    def __init__(self):
        # Time window for correlation: 5 minutes
        self.window_size = timedelta(minutes=5)
        
        # Event cache for correlation
        self.event_cache = {}  # zone → [events]
    
    def process_event(self, event):
        """Process incoming event and check for correlations"""
        
        zone = event['zone']
        timestamp = event['timestamp']
        
        # Add to cache
        if zone not in self.event_cache:
            self.event_cache[zone] = []
        
        self.event_cache[zone].append(event)
        
        # Get events in time window
        window_events = [
            e for e in self.event_cache[zone]
            if timestamp - e['timestamp'] < self.window_size
        ]
        
        # Check correlation rules
        self.check_correlations(window_events)
        
        # Cleanup old events
        self.cleanup_cache(zone, timestamp)
    
    def check_correlations(self, events):
        """Check if events match any correlation patterns"""
        
        # Pattern 1: Access Denied + Loitering
        access_denied = [e for e in events if e['event_type'] == 'access_denied']
        loitering = [e for e in events if e.get('behavior') == 'loitering']
        
        if access_denied and loitering:
            self.create_correlated_incident(
                events=[access_denied[0], loitering[0]],
                pattern='unauthorized_access_attempt',
                severity='HIGH',
                title='Unauthorized Access Attempt + Suspicious Behavior'
            )
        
        # Pattern 2: Multiple Failed Access Attempts
        if len(access_denied) >= 3:
            self.create_correlated_incident(
                events=access_denied,
                pattern='brute_force_attempt',
                severity='CRITICAL',
                title='Multiple Failed Access Attempts (Possible Brute Force)'
            )

Step 3: Incident Creation

Unified Incident Created:
{
  "incident_id": "INC-2024-12-08-00123",
  "tenant_id": "acme_001",
  "pattern": "unauthorized_access_attempt",
  "severity": "HIGH",
  "title": "Unauthorized Access Attempt + Suspicious Behavior",
  "description": "Person attempted access at DOOR_123 (denied), then observed loitering nearby for 45 seconds",
  "created_at": "2024-12-08T14:24:15Z",
  "zone": "RESTRICTED_A",
  "correlated_events": [
    {
      "service": "OS-PACS",
      "event_id": "evt_pacs_789",
      "event_type": "access_denied"
    },
    {
      "service": "OS-SENTINEL",
      "event_id": "evt_sentinel_456",
      "event_type": "person_detected",
      "behavior": "loitering"
    }
  ],
  "recommended_actions": [
    "Review camera footage",
    "Dispatch security patrol",
    "Interview person if still present"
  ],
  "assigned_to": null,
  "status": "open"
}

Step 4: Automated Response

Workflow Engine executes:
1. Send alert to security team (email + SMS)
2. Display incident on Command Center dashboard
3. If OS-PATROL available: Dispatch nearest unit
4. If OS-GUARDIAN available: Alert nearby officers
5. Log incident for compliance
```

### Correlation Patterns Library

```
Built-in Correlation Patterns:

1. Tailgating Detection
   ├── Events: 2× badge swipes within 3 seconds at same door
   ├── Condition: Only 1 authorized credential
   ├── Severity: MEDIUM
   └── Action: Alert security, review footage

2. Stolen Vehicle in Parking Lot
   ├── Events: LPR hot-list match + Vehicle enters parking
   ├── Condition: Within 2 minutes
   ├── Severity: CRITICAL
   └── Action: Lock barriers, alert law enforcement

3. VIP Arrival Preparation
   ├── Events: Visitor check-in (OS-CONCIERGE) + VIP guest
   ├── Condition: VIP flag = true
   ├── Severity: INFO
   └── Action: Pre-condition HVAC, notify host, grant temporary access

4. After-Hours Intrusion
   ├── Events: Motion detected (OS-SENTINEL) + Outside business hours
   ├── Condition: Zone = restricted, Time: 22:00-06:00
   ├── Severity: HIGH
   └── Action: Alert security, dispatch patrol, start recording

5. Officer Safety Alert
   ├── Events: Body camera activated + GPS speed >80 mph
   ├── Condition: Pursuit flag = true
   ├── Severity: CRITICAL
   └── Action: Alert dispatch, track location, notify backup units

Custom Pattern Creation:
Users can create custom correlation patterns via UI:

Pattern Builder:
┌────────────────────────────────────────┐
│ Pattern Name: [________________]       │
│                                        │
│ Trigger Events:                        │
│ [+] Add Event Condition                │
│   Service: [OS-PACS ▼]                 │
│   Event Type: [access_denied ▼]        │
│   Time Window: [5] minutes             │
│                                        │
│ [+] Add Event Condition                │
│   Service: [OS-SENTINEL ▼]             │
│   Event Type: [person_detected ▼]      │
│   Additional: behavior = loitering     │
│                                        │
│ Match Conditions:                      │
│ ☑ Same tenant                          │
│ ☑ Same zone/location                   │
│ ☐ Same person                          │
│                                        │
│ Actions:                               │
│ ☑ Create incident                      │
│ ☑ Send notification to: [Security ▼]  │
│ ☑ Dispatch patrol unit                │
│ ☐ Lock doors in zone                  │
│                                        │
│ Severity: [HIGH ▼]                     │
│                                        │
│ [Save Pattern]  [Test Pattern]         │
└────────────────────────────────────────┘
```

---

## Cross-Service Analytics

### Unified Data Warehouse

```
┌──────────────────────────────────────────────────────────────┐
│          UNIFIED ANALYTICS ARCHITECTURE                       │
└──────────────────────────────────────────────────────────────┘

Data Pipeline:

Service Databases → ETL → Data Warehouse → Analytics/Reporting

Step 1: Data Extraction
Each service maintains its own operational database:
├── OS-PACS PostgreSQL (access events)
├── OS-PATROL PostgreSQL (GPS tracks, LPR scans)
├── OS-SENTINEL MinIO (videos) + PostgreSQL (detections)
├── OS-CONCIERGE PostgreSQL (visitors, packages)
└── OS-GUARDIAN MinIO (evidence) + PostgreSQL (metadata)

Step 2: ETL (Extract, Transform, Load)
Apache Airflow orchestrates nightly ETL:

DAG: hub_analytics_etl (runs at 2 AM daily)
├── Task 1: Extract from OS-PACS
│   SELECT * FROM access_events WHERE date = yesterday
├── Task 2: Extract from OS-PATROL
│   SELECT * FROM gps_tracks WHERE date = yesterday
├── Task 3: Extract from OS-SENTINEL
│   SELECT * FROM detection_events WHERE date = yesterday
├── Task 4: Extract from OS-CONCIERGE
│   SELECT * FROM visitor_checkins WHERE date = yesterday
├── Task 5: Extract from OS-GUARDIAN
│   SELECT * FROM evidence_uploads WHERE date = yesterday
├── Task 6: Transform & Normalize
│   • Standardize timestamps (UTC)
│   • Normalize user IDs across services
│   • Geocode locations
│   • Join with dimension tables
├── Task 7: Load into ClickHouse
│   INSERT INTO unified_events (...)
└── Task 8: Update aggregates
    • Refresh materialized views
    • Update summary tables

Step 3: Data Warehouse (ClickHouse)
Unified event table:

CREATE TABLE unified_events (
    tenant_id String,
    event_id String,
    service LowCardinality(String),  -- pacs, patrol, sentinel, ...
    event_type LowCardinality(String),
    timestamp DateTime64(3),
    user_id Nullable(String),
    location Tuple(lat Float64, lon Float64),
    zone String,
    metadata String,  -- JSON blob
    
    INDEX idx_tenant tenant_id TYPE bloom_filter GRANULARITY 1,
    INDEX idx_service service TYPE set(0) GRANULARITY 1
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (tenant_id, service, timestamp);

Aggregation tables:

-- Daily summary by service
CREATE MATERIALIZED VIEW daily_summary_by_service
ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (tenant_id, service, date)
AS SELECT
    tenant_id,
    service,
    toDate(timestamp) AS date,
    count() AS event_count,
    uniq(user_id) AS unique_users,
    sum(CASE WHEN event_type LIKE '%denied%' THEN 1 ELSE 0 END) AS denied_count
FROM unified_events
GROUP BY tenant_id, service, date;

Step 4: Analytics & Reporting
Grafana connects to ClickHouse:

Dashboard: "Executive Summary"
├── Panel 1: Events by Service (last 30 days)
│   SELECT service, count() FROM unified_events
│   WHERE tenant_id = $tenant AND timestamp >= now() - INTERVAL 30 DAY
│   GROUP BY service
├── Panel 2: Top 10 Active Users
│   SELECT user_id, count() AS activity_count
│   FROM unified_events
│   WHERE tenant_id = $tenant AND timestamp >= now() - INTERVAL 7 DAY
│   GROUP BY user_id ORDER BY activity_count DESC LIMIT 10
├── Panel 3: Geographic Heatmap (access events)
│   SELECT location FROM unified_events
│   WHERE tenant_id = $tenant AND service = 'pacs'
├── Panel 4: Incident Severity Trend
│   SELECT toDate(timestamp) AS date, severity, count()
│   FROM incidents
│   WHERE tenant_id = $tenant
│   GROUP BY date, severity
└── Panel 5: System Health (service uptime)
    SELECT service, avg(uptime_seconds) / 3600 AS uptime_hours
    FROM service_health
    WHERE timestamp >= now() - INTERVAL 24 HOUR
    GROUP BY service
```

### Cross-Service Reports

```
Report: "Daily Operations Summary"

Generated: 2024-12-08 (Yesterday)
Tenant: Acme Corporation

═══════════════════════════════════════════════════════════
SECTION 1: ACCESS CONTROL (OS-PACS)
═══════════════════════════════════════════════════════════
Total Access Events: 12,456
├── Granted: 12,234 (98.2%)
├── Denied: 222 (1.8%)
└── Peak Hour: 08:00-09:00 (2,345 events)

Top Doors by Activity:
1. Main Entrance: 3,456 events
2. Parking Gate: 2,890 events
3. Employee Entrance: 2,123 events

Denied Access Analysis:
├── Expired Credentials: 145 (65%)
├── Wrong Zone: 58 (26%)
├── After-Hours: 19 (9%)

═══════════════════════════════════════════════════════════
SECTION 2: FLEET OPERATIONS (OS-PATROL)
═══════════════════════════════════════════════════════════
Total Fleet: 25 vehicles
Active Today: 22 vehicles (88%)
Offline: 3 vehicles (maintenance)

Mileage:
├── Total: 2,345 miles
├── Average per vehicle: 106 miles
├── Longest trip: Vehicle #12 (245 miles)

LPR Scans:
├── Total: 1,234 plates scanned
├── Hot-List Matches: 2 (0.16%)
└── Top Scanner: Vehicle #7 (189 plates)

═══════════════════════════════════════════════════════════
SECTION 3: VIDEO SURVEILLANCE (OS-SENTINEL)
═══════════════════════════════════════════════════════════
Cameras Online: 98/100 (98%)
Offline Cameras: CAM_045, CAM_078

Detection Events: 45,678
├── Person: 34,567 (76%)
├── Vehicle: 8,901 (19%)
├── Other: 2,210 (5%)

Top Activity Zones:
1. Main Lobby: 8,456 detections
2. Parking Lot: 6,789 detections
3. Warehouse: 4,321 detections

AI Alerts Generated: 23
├── Loitering: 12
├── Unauthorized Zone: 8
├── Tailgating: 3

═══════════════════════════════════════════════════════════
SECTION 4: VISITOR MANAGEMENT (OS-CONCIERGE)
═══════════════════════════════════════════════════════════
Total Visitors: 234
├── Pre-registered: 189 (81%)
├── Walk-in: 45 (19%)
└── Average check-in time: 42 seconds

Packages:
├── Received: 67 packages
├── Picked up: 59 packages (88%)
└── Awaiting pickup: 8 packages

═══════════════════════════════════════════════════════════
SECTION 5: PERSONNEL (OS-GUARDIAN)
═══════════════════════════════════════════════════════════
Officers on Duty: 15
Body Camera Usage:
├── Total Recording Time: 89 hours
├── Average per officer: 5.9 hours
├── Evidence Uploads: 12 clips (3.2 GB)

Incidents Documented: 8
├── Property theft: 3
├── Trespassing: 2
├── Altercation: 2
├── Medical emergency: 1

═══════════════════════════════════════════════════════════
CROSS-SERVICE CORRELATIONS
═══════════════════════════════════════════════════════════
Correlated Incidents: 3
1. INC-00123: Unauthorized access + loitering (RESOLVED)
2. INC-00124: Stolen vehicle detected in parking (IN PROGRESS)
3. INC-00125: After-hours intrusion + patrol dispatch (RESOLVED)

Workflow Automations Triggered: 15
├── Auto-dispatch: 5 times
├── Auto-lock: 3 times
├── VIP preparation: 7 times

═══════════════════════════════════════════════════════════
SYSTEM HEALTH
═══════════════════════════════════════════════════════════
Uptime (24h average):
├── OS-PACS: 99.98%
├── OS-PATROL: 99.95%
├── OS-SENTINEL: 99.89%
├── OS-CONCIERGE: 99.99%
└── OS-GUARDIAN: 99.97%

Performance:
├── API Response Time (p95): 145 ms
├── Event Processing Latency: 1.2 seconds
└── Database Query Time (p95): 78 ms
```

---

## API Architecture

### Unified API Endpoints

```
BASE URL: https://api.opensecure.com/

HUB MANAGEMENT
├── POST   /auth/login                    User authentication
├── POST   /auth/refresh                  Refresh JWT token
├── POST   /auth/logout                   Invalidate token
├── GET    /auth/user                     Get current user
├── GET    /tenants                       List tenants (super admin)
├── GET    /tenants/{id}                  Get tenant details
├── POST   /tenants                       Create tenant
├── GET    /users                         List users
├── POST   /users                         Create user
├── PUT    /users/{id}                    Update user
├── DELETE /users/{id}                    Delete user
└── GET    /roles                         List available roles

UNIFIED DASHBOARDS
├── GET    /dashboard/summary             Executive summary
├── GET    /dashboard/incidents           Recent incidents
├── GET    /dashboard/alerts              Active alerts
├── GET    /dashboard/map                 Unified map view
└── GET    /dashboard/analytics           Analytics overview

CROSS-SERVICE SEARCH
├── POST   /search                        Global search
│          {"query": "john doe", "services": ["pacs", "sentinel"]}
├── GET    /search/users                  Search users across services
├── GET    /search/events                 Search events across services
└── GET    /search/locations              Search locations/zones

INCIDENTS & CORRELATION
├── GET    /incidents                     List correlated incidents
├── GET    /incidents/{id}                Get incident details
├── POST   /incidents                     Create manual incident
├── PUT    /incidents/{id}                Update incident
├── POST   /incidents/{id}/assign         Assign incident
└── POST   /incidents/{id}/resolve        Resolve incident

WORKFLOWS & AUTOMATION
├── GET    /workflows                     List workflows
├── POST   /workflows                     Create workflow
├── PUT    /workflows/{id}                Update workflow
├── DELETE /workflows/{id}                Delete workflow
├── POST   /workflows/{id}/trigger        Manual trigger
└── GET    /workflows/history             Workflow execution history

REPORTING
├── GET    /reports                       List available reports
├── POST   /reports/generate              Generate custom report
├── GET    /reports/{id}                  Download report
└── POST   /reports/schedule              Schedule recurring report

SERVICE PROXIES (Unified access to individual services)
├── /pacs/*                               Proxy to OS-PACS API
├── /patrol/*                             Proxy to OS-PATROL API
├── /concierge/*                          Proxy to OS-CONCIERGE API
├── /guardian/*                           Proxy to OS-GUARDIAN API
└── /sentinel/*                           Proxy to OS-SENTINEL API
```

---

## Integration Patterns

### Hub-to-Service Integration Models

```
Pattern 1: SYNCHRONOUS (REST API Calls)
Use Case: User initiates action requiring immediate response

Example: User grants access via Hub dashboard
Hub → OS-PACS: POST /api/v1/access/grant
{
  "user_id": "user_123",
  "door_id": "door_456",
  "start_time": "2024-12-08T00:00:00Z",
  "end_time": "2024-12-09T23:59:59Z"
}

OS-PACS ← Response (200 OK):
{
  "access_id": "acc_789",
  "status": "granted"
}

Pattern 2: ASYNCHRONOUS (Event-Driven)
Use Case: Service event notification to Hub

Example: Access event occurs in OS-PACS
OS-PACS → Kafka Topic: opensecure.pacs.events
Hub subscribes and processes event in background

Pattern 3: BATCH (Scheduled ETL)
Use Case: Daily analytics aggregation

Example: Nightly data sync
Hub ETL Job (2 AM):
├── Extract data from all services
├── Transform & normalize
├── Load into data warehouse
└── Update analytics dashboards

Pattern 4: WEBHOOK (Push Notifications)
Use Case: Third-party system integration

Example: When incident created, notify external SIEM
Hub → External System: POST https://siem.company.com/webhook
{
  "event": "incident_created",
  "incident_id": "INC-123",
  "severity": "HIGH",
  "timestamp": "2024-12-08T14:23:45Z"
}
```

---

**Document Version**: 1.0  
**Last Updated**: December 2024  
**Related Documents**:
- [OpenSecure Hub Network Topology](./OpenSecure_Hub_Network_Topology.md)
- [OS-PACS Logical Topology](./OS-PACS_Logical_Topology.md)
- [OS-PATROL Logical Topology](./OS-PATROL_Logical_Topology.md)
- [OS-CONCIERGE Logical Topology](./OS-CONCIERGE_Logical_Topology.md)
- [OS-GUARDIAN Logical Topology](./OS-GUARDIAN_Logical_Topology.md)
- [OS-SENTINEL Logical Topology](./OS-SENTINEL_Logical_Topology.md)

**Completion Status**: OpenSecure Hub documentation suite complete (Network + Logical Topology).
