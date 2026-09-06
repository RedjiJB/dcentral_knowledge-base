---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: 172d2f51-948a-4401-a40c-a040bf413394
original_filename: Provincial_Security_Vehicle_Network.md
created_at: 2026-03-04T20:38:03.426976+00:00
content_hash: 70dbd571efe0
topic: opensecure-provincial-security-network
topic: "provincial-security-network-programs"
consolidated_into: [docs/DC-OPENSECURE-PROVINCIAL-PIV-CREDENTIAL-RECONCILED-001.md, docs/DC-PROVINCIAL-SECURITY-NETWORK-RECONCILED-001.md]
---

# Provincial Security Vehicle Network (PSVN-Fleet)
## Universal Fleet Management & Mobile Patrol Coordination Platform

**Project Name**: Provincial Security Vehicle Network - Fleet (PSVN-Fleet)  
**Version**: 1.0  
**Date**: December 2025  
**Classification**: Fleet & Patrol Infrastructure  
**Scope**: Province-wide vehicle coordination

---

## Executive Summary

### Vision Statement

Create a **federated patrol vehicle network** where every security vehicle and patrol unit in the province operates on a standardized, interoperable platform, enabling **real-time vehicle sharing**, **cross-agency coordination**, and **automated suspect tracking** using PIV credentials to unlock unprecedented cooperation in mobile security operations.

### The Revolutionary Concept

**"Vehicles Follow Credentials, Jurisdiction Follows Authority"**

```
┌─────────────────────────────────────────────────────────────────┐
│  Traditional Model (Isolated Fleets)                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Police Agency A → 50 patrol cars → Own tracking system        │
│  Security Company B → 30 vehicles → Different GPS system       │
│  Security Company C → 20 vehicles → Paper logs                 │
│  University Campus → 15 patrol cars → Standalone system        │
│                                                                  │
│  Problems:                                                       │
│  • No visibility across organizations                           │
│  • Suspect pursuit = stops at boundary                          │
│  • Duplicate patrols in same area                              │
│  • No vehicle sharing (waste)                                   │
│  • Cannot coordinate multi-agency response                      │
│  • License plate databases isolated                            │
│  • Vehicle histories fragmented                                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  PSVN-Fleet Model (Federated Network)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│         ┌──────────────────────────────────────┐               │
│         │  Provincial Vehicle Federation Hub   │               │
│         │  (Ministry of Public Safety)         │               │
│         │  • Real-time vehicle registry        │               │
│         │  • License plate database (pooled)   │               │
│         │  • Cross-agency dispatch             │               │
│         │  • Suspect tracking coordination     │               │
│         └────────────┬─────────────────────────┘               │
│                      │                                          │
│         ┌────────────┼────────────┬────────────┐               │
│         │            │            │            │               │
│         ▼            ▼            ▼            ▼               │
│    Police Dept  Sheriff Dept  Security Co  Campus Sec         │
│    (50 vehicles)(30 vehicles)(100 vehicles)(15 vehicles)       │
│                                                                  │
│  ANY authorized officer/guard with PIV card can:               │
│  • View location of nearby patrol units (all agencies)         │
│  • Request backup from nearest available unit                  │
│  • Track suspect across jurisdictional boundaries              │
│  • Access pooled license plate database                        │
│  • Share real-time alerts (BOLO, stolen vehicles)             │
│  • Coordinate multi-agency operations                          │
│  • Use vehicles across organizations (with authorization)      │
│                                                                  │
│  All vehicle access controlled by:                             │
│  ✓ PIV certificate validation                                  │
│  ✓ Vehicle authorization grants                                │
│  ✓ Role-based permissions                                      │
│  ✓ Location-based access                                       │
│  ✓ Complete audit logging                                      │
└─────────────────────────────────────────────────────────────────┘
```

### Network Effects & Collective Intelligence

**The Power of Pooled Vehicle Data:**

```
Single Organization:
├─ 20 patrol vehicles
├─ 10,000 license plates scanned/day
├─ Coverage: 1 jurisdiction
├─ Response time: 15 minutes average
└─ Value: Baseline

10 Organizations (PSVN-Fleet):
├─ 200 patrol vehicles
├─ 100,000 license plates scanned/day
├─ Coverage: Regional
├─ Response time: 5 minutes (nearest available)
├─ Suspect tracking across boundaries
└─ Value: 20x baseline

100 Organizations (PSVN-Fleet):
├─ 2,000 patrol vehicles
├─ 1,000,000 license plates scanned/day
├─ Coverage: Province-wide
├─ Response time: 2 minutes
├─ Real-time suspect tracking anywhere
├─ Predictive patrol optimization
└─ Value: 500x baseline

Benefits of Scale:
✓ License plate seen by 50 cameras/day (vs 2)
✓ Stolen vehicle detected within minutes (vs days/never)
✓ Nearest unit always available (cross-agency)
✓ Hot spots identified automatically
✓ Patrol routes optimized collectively
✓ Emergency response coordinated seamlessly
```

### The Problem Being Solved

**Current State - Isolated Vehicle Operations:**

1. **No Cross-Agency Visibility** - Can't see where other agencies are patrolling
2. **Jurisdictional Barriers** - Pursuit stops at boundary, suspect escapes
3. **Duplicate Coverage** - Multiple agencies patrolling same area (waste)
4. **Inefficient Response** - Can't dispatch nearest available unit
5. **Fragmented LPR Data** - Each agency scans plates, none share data
6. **No Vehicle Sharing** - Vehicles sit idle while others are overworked
7. **Limited Coordination** - Multi-agency operations require radio/phone

**PSVN-Fleet Solution - Connected Fleet:**

1. **Real-Time Visibility** - See all authorized patrol units on one map
2. **Seamless Coordination** - Track suspects across jurisdictions automatically
3. **Optimized Deployment** - AI suggests patrol routes to avoid overlap
4. **Smart Dispatch** - Nearest available unit responds (any agency)
5. **Pooled Intelligence** - 10M+ license plates scanned daily, searchable
6. **Fleet Optimization** - Share vehicles, reduce waste by 30%+
7. **Instant Coordination** - Push alerts, real-time chat, synchronized response

---

## System Architecture

### Three-Tier Federation Model

#### Tier 1: Provincial Vehicle Hub (Ministry)

**Role**: Fleet registry, coordination center, intelligence aggregation

```
┌───────────────────────────────────────────────────────────────┐
│  Ministry of Public Safety - Provincial Vehicle Hub          │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Real-Time Vehicle Registry                            │  │
│  │  • Live location of all 10,000+ patrol vehicles       │  │
│  │  • Status: Available, En Route, On Scene, Off Duty    │  │
│  │  • Assigned officer (PIV ID linked)                   │  │
│  │  • Vehicle capabilities (K9, supervisor, equipment)   │  │
│  │  • Update frequency: 5 seconds                        │  │
│  │  • Historical tracks: 90 days                         │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Provincial License Plate Database                     │  │
│  │  • Aggregated from all agencies                       │  │
│  │  • 1M+ plates scanned daily                           │  │
│  │  • Real-time hot-list matching:                       │  │
│  │    - Stolen vehicles                                   │  │
│  │    - Amber alerts                                      │  │
│  │    - Wanted persons                                    │  │
│  │    - Unpaid fines                                      │  │
│  │    - Suspended licenses                                │  │
│  │  • Search interface (PIV-authenticated)                │  │
│  │  • Automated alerts to nearest units                  │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Intelligent Dispatch & Coordination                   │  │
│  │  • Cross-agency incident routing                       │  │
│  │  • Nearest available unit algorithm                    │  │
│  │  • Multi-agency backup coordination                    │  │
│  │  • Pursuit coordination across jurisdictions           │  │
│  │  • Emergency alerts to all nearby units                │  │
│  │  • Patrol optimization suggestions                     │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Analytics & Intelligence                              │  │
│  │  • Crime pattern analysis                              │  │
│  │  • Hot spot identification                             │  │
│  │  • Predictive patrol routing                           │  │
│  │  • Vehicle utilization analytics                       │  │
│  │  • Cross-agency collaboration metrics                  │  │
│  │  • Cost savings reports                                │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

**Provincial Vehicle APIs:**

```yaml
openapi: 3.0.0
info:
  title: Provincial Security Vehicle Network API
  version: 1.0.0
  description: |
    Federated fleet management API for real-time vehicle coordination
    and license plate intelligence sharing using PIV credentials.

servers:
  - url: https://vehicles.securityguard.gov.on.ca/api/v1
    description: Provincial Vehicle Federation Hub

paths:
  /vehicles/nearby:
    get:
      summary: Get nearby patrol units (cross-agency)
      security:
        - piv_certificate: []
      parameters:
        - name: latitude
          in: query
          required: true
          schema:
            type: number
        - name: longitude
          in: query
          required: true
          schema:
            type: number
        - name: radius_km
          in: query
          schema:
            type: number
            default: 5
        - name: include_agencies
          in: query
          schema:
            type: array
            items:
              type: string
          description: Filter by specific agencies, or all if omitted
        - name: status
          in: query
          schema:
            type: array
            items:
              type: string
              enum: [available, en_route, on_scene, off_duty]
      responses:
        '200':
          description: List of nearby patrol units
          content:
            application/json:
              schema:
                type: object
                properties:
                  units:
                    type: array
                    items:
                      type: object
                      properties:
                        unit_id:
                          type: string
                          example: "UNIT-ACME-045"
                        call_sign:
                          type: string
                          example: "Alpha-12"
                        organization:
                          type: string
                        location:
                          type: object
                          properties:
                            latitude: number
                            longitude: number
                            heading: number (degrees)
                            speed: number (km/h)
                            last_update: string (ISO 8601)
                        status:
                          type: string
                          enum: [available, en_route, on_scene, off_duty]
                        officer:
                          type: object
                          properties:
                            id: string (PIV ID)
                            name: string (if authorized to see)
                            certification: string
                        capabilities:
                          type: array
                          items:
                            type: string
                          example: ["k9", "supervisor", "first_aid"]
                        distance_km:
                          type: number
                        eta_minutes:
                          type: number

  /vehicles/{unit_id}/request_backup:
    post:
      summary: Request backup from specific unit
      security:
        - piv_certificate: []
      parameters:
        - name: unit_id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                requesting_unit:
                  type: string
                requesting_officer:
                  type: string (PIV ID)
                incident_type:
                  type: string
                  enum: [traffic_stop, disturbance, pursuit, medical, fire, other]
                urgency:
                  type: string
                  enum: [routine, priority, emergency]
                location:
                  type: object
                  properties:
                    latitude: number
                    longitude: number
                notes:
                  type: string
      responses:
        '201':
          description: Backup request sent
          content:
            application/json:
              schema:
                type: object
                properties:
                  request_id: string
                  status: string (sent, acknowledged, declined)
                  eta_minutes: number

  /lpr/search:
    post:
      summary: Search provincial license plate database
      security:
        - piv_certificate: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                plate_number:
                  type: string
                  example: "ABC 1234"
                jurisdiction:
                  type: string
                  example: "ON"
                  description: Province/state code
                time_range:
                  type: object
                  properties:
                    start: string (ISO 8601)
                    end: string (ISO 8601)
                location:
                  type: object
                  properties:
                    center:
                      type: object
                      properties:
                        lat: number
                        lon: number
                    radius_km: number
                reason:
                  type: string
                  description: Required for audit
                  example: "Traffic stop investigation"
      responses:
        '200':
          description: License plate sightings
          content:
            application/json:
              schema:
                type: object
                properties:
                  plate: string
                  vehicle_info:
                    type: object
                    properties:
                      make: string
                      model: string
                      year: integer
                      color: string
                      registered_owner: string (redacted for privacy)
                  hot_list_status:
                    type: object
                    properties:
                      stolen: boolean
                      amber_alert: boolean
                      wanted: boolean
                      suspended_license: boolean
                      unpaid_fines: boolean
                  sightings:
                    type: array
                    items:
                      type: object
                      properties:
                        timestamp: string
                        location:
                          type: object
                          properties:
                            lat: number
                            lon: number
                            address: string
                        scanning_unit: string
                        organization: string
                        confidence: number
                        image_url: string (if authorized)

  /lpr/hotlist:
    post:
      summary: Add vehicle to hot-list (BOLO)
      security:
        - piv_certificate: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                plate_number: string
                jurisdiction: string
                reason:
                  type: string
                  enum: [stolen, amber_alert, wanted, investigation]
                description: string
                case_number: string
                priority:
                  type: string
                  enum: [low, medium, high, critical]
                alert_radius_km:
                  type: number
                  description: Alert units within this radius on sighting
                expires_at:
                  type: string
                  format: date-time
      responses:
        '201':
          description: Hot-list entry created
          content:
            application/json:
              schema:
                type: object
                properties:
                  hotlist_id: string
                  status: string (active, expired)
                  broadcast_sent: boolean

  /dispatch/incident:
    post:
      summary: Create cross-agency incident
      security:
        - piv_certificate: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                incident_type:
                  type: string
                  enum: [traffic, theft, assault, medical, fire, other]
                location:
                  type: object
                  properties:
                    latitude: number
                    longitude: number
                    address: string
                priority:
                  type: string
                  enum: [low, medium, high, emergency]
                description: string
                requesting_agency: string
                estimated_units_needed: integer
                special_requirements:
                  type: array
                  items:
                    type: string
                  example: ["k9", "supervisor", "medical"]
      responses:
        '201':
          description: Incident created, units notified
          content:
            application/json:
              schema:
                type: object
                properties:
                  incident_id: string
                  responding_units:
                    type: array
                    items:
                      type: object
                      properties:
                        unit_id: string
                        organization: string
                        eta_minutes: number

components:
  securitySchemes:
    piv_certificate:
      type: mutualTLS
      description: PIV certificate authentication
```

#### Tier 2: Organization Fleet Management (Police/Security)

**Role**: Operate vehicles, contribute data, coordinate locally

```
┌───────────────────────────────────────────────────────────────┐
│  Organization Fleet Management (OS-PATROL)                    │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Vehicle Fleet (Hardware)                              │  │
│  │  • 10-500 patrol vehicles                             │  │
│  │  • GPS trackers (Teltonika, Queclink, etc.)          │  │
│  │  • Dashcams (forward + interior)                      │  │
│  │  • License Plate Recognition cameras (Raspberry Pi)   │  │
│  │  • OBD-II adapters (vehicle diagnostics)             │  │
│  │  • PIV card readers (driver authentication)          │  │
│  │  • Mobile data terminals (MDT)                        │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Local Fleet Server (OS-PATROL/Traccar)               │  │
│  │  • Real-time GPS tracking (all vehicles)              │  │
│  │  • Geofencing (patrol zones, restricted areas)        │  │
│  │  • Dashcam video storage (MinIO)                      │  │
│  │  • LPR database (local cache + sync to hub)          │  │
│  │  • Driver behavior analytics                          │  │
│  │  • Maintenance scheduling                             │  │
│  │  • Fuel tracking                                       │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Federation Client                                      │  │
│  │  • Register vehicles with provincial hub              │  │
│  │  • Share location with authorized agencies            │  │
│  │  • Upload LPR scans to pooled database               │  │
│  │  • Receive cross-agency alerts                        │  │
│  │  • Coordinate multi-agency incidents                  │  │
│  │  • Define sharing policies:                           │  │
│  │    - Which vehicles visible to other agencies        │  │
│  │    - What data shared (location, status, LPR)        │  │
│  │    - Emergency override (all data shared)             │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

**Vehicle Configuration with PIV:**

```yaml
# /etc/os-patrol/vehicle-001.yml
# Configuration for patrol vehicle integration with PSVN-Fleet

vehicle:
  id: "VEH-ACME-001"
  call_sign: "Alpha-12"
  organization: "Acme Security Services"
  type: "patrol_sedan"
  
  # Vehicle details
  details:
    make: "Ford"
    model: "Explorer"
    year: 2024
    vin: "1FM5K8D84RGA12345"
    license_plate: "XYZ 789"
    color: "white"
  
  # Capabilities
  capabilities:
    - "patrol"
    - "first_aid"
    - "fire_extinguisher"
    - "emergency_lights"
  
  # PIV Integration
  piv_authentication:
    enabled: true
    reader_type: "nfc"  # NFC reader in vehicle
    
    # Vehicle only starts when PIV card tapped
    ignition_lock: true
    
    # Link vehicle to driver
    auto_assign_driver: true  # Driver's PIV ID becomes vehicle operator
    
    # Require PIV for:
    require_piv_for:
      - ignition_start
      - equipment_access
      - sensitive_areas_entry
      - evidence_upload
  
  # GPS Tracking
  gps:
    device_model: "Teltonika FMB920"
    device_id: "352094080000123"
    update_interval_seconds: 5
    
    # High-precision tracking
    accuracy_required: "3 meters"
    
    # Protocols
    protocol: "osmand"  # or gt06, h02, etc.
    server_url: "https://fleet.acmesecurity.com:5055"
  
  # Dashcams
  dashcams:
    - camera_id: "DASH-VEH-001-FRONT"
      position: "front"
      resolution: "1920x1080"
      fps: 30
      recording_mode: "continuous"
      storage_days: 30
      
      # Auto-upload triggers
      upload_triggers:
        - "g_sensor_event"  # Hard braking, collision
        - "button_press"  # Manual trigger
        - "geofence_entry"  # Entering specific area
        - "hot_list_match"  # LPR detects wanted vehicle
    
    - camera_id: "DASH-VEH-001-INTERIOR"
      position: "interior"
      resolution: "1280x720"
      recording_mode: "on_demand"  # Privacy-preserving
      
      # Only record when:
      record_when:
        - "arrest_made"
        - "transport_prisoner"
        - "complaint_expected"
  
  # License Plate Recognition
  lpr:
    enabled: true
    
    # Edge processing (Raspberry Pi in vehicle)
    device: "Raspberry Pi 4"
    camera_model: "Raspberry Pi Camera Module v3"
    
    # Processing
    engine: "OpenALPR"
    processing_location: "edge"  # Process in vehicle, not cloud
    
    # Scan settings
    scan_interval_seconds: 0.5  # Scan every 0.5 seconds
    confidence_threshold: 0.85
    
    # Hot-list checking
    hot_list:
      enabled: true
      check_against:
        - "provincial_stolen_vehicles"
        - "provincial_amber_alerts"
        - "provincial_wanted_persons"
        - "local_parking_violations"
      
      alert_on_match:
        immediate: true
        notify:
          - "driver"
          - "dispatch"
          - "provincial_hub"
          - "nearby_units"
    
    # Upload to provincial database
    upload_scans:
      enabled: true
      upload_interval: "real-time"  # Every scan immediately
      anonymize: true  # Remove vehicle location for privacy
  
  # OBD-II Diagnostics
  obd2:
    enabled: true
    adapter: "ELM327 WiFi"
    
    # Monitor
    metrics:
      - "speed"
      - "rpm"
      - "fuel_level"
      - "engine_temp"
      - "check_engine_light"
      - "odometer"
    
    # Alerts
    alerts:
      - metric: "check_engine_light"
        condition: "on"
        action: "notify_maintenance"
      
      - metric: "speed"
        condition: "> 120 km/h"
        action: "log_speeding_event"
  
  # Geofencing
  geofences:
    - name: "Patrol Zone A"
      type: "polygon"
      coordinates: [[43.65, -79.38], [43.66, -79.38], [43.66, -79.37], [43.65, -79.37]]
      alerts:
        on_entry: false
        on_exit: true  # Alert if vehicle leaves assigned zone
    
    - name: "Restricted Area (Civilian Property)"
      type: "polygon"
      coordinates: [[43.70, -79.40], [43.71, -79.40], [43.71, -79.39], [43.70, -79.39]]
      alerts:
        on_entry: true  # Unauthorized entry
        on_exit: false
  
  # Federation Sharing
  federation:
    enabled: true
    
    # Share with provincial hub
    share_location: true
    share_status: true
    share_lpr_scans: true
    
    # Visibility policy
    visible_to:
      - organization: "own"
        data: ["location", "status", "lpr", "dashcam"]
      
      - organization: "police_*"  # All police agencies
        data: ["location", "status"]
        conditions:
          - "within_10km"  # Only if within 10km
      
      - organization: "security_*"  # Other security companies
        data: ["location"]
        conditions:
          - "within_5km"
          - "priority_emergency"  # Only during emergencies
    
    # Emergency override
    emergency_sharing:
      enabled: true
      trigger_keywords: ["officer down", "pursuit", "emergency"]
      share_all_data: true  # Location, dashcam, LPR, everything
      notify_all_nearby: true
  
  # Integration with other provincial systems
  integrations:
    pbcen:
      enabled: true
      # Link dashcam to body camera evidence
      link_evidence: true
    
    psvn:
      enabled: true
      # Correlate with fixed cameras
      correlate_with_fixed_cameras: true
    
    os_pacs:
      enabled: true
      # Vehicle gate access
      auto_open_gates: true
```

**Vehicle Physical Setup:**

```
┌─────────────────────────────────────────────────────────────┐
│  Provincial Standard Patrol Vehicle Setup                   │
└─────────────────────────────────────────────────────────────┘

Equipment Installation:

1. GPS Tracker (Teltonika FMB920)
   ├─ Location: Under dash (hidden)
   ├─ Power: Hardwired to vehicle battery
   ├─ Antenna: Roof-mounted (discrete)
   ├─ Backup battery: 24 hours
   └─ Cost: $120

2. Dashcam - Front (Viofo A229 Pro)
   ├─ Location: Windshield, behind mirror
   ├─ Resolution: 1920x1080 @ 60 FPS
   ├─ Storage: 256GB SD card (local)
   ├─ GPS: Integrated
   └─ Cost: $250

3. Dashcam - Interior (optional, privacy-aware)
   ├─ Location: Overhead, facing rear seats
   ├─ Recording: On-demand only
   └─ Cost: $150

4. License Plate Recognition System
   ├─ Raspberry Pi 4 (8GB)
   ├─ Raspberry Pi Camera Module v3
   ├─ Processing: OpenALPR
   ├─ Location: Dashboard, angled 45° down
   ├─ Reads plates: Forward (moving or stationary)
   ├─ Storage: 128GB SD + upload to server
   └─ Cost: $150

5. PIV Card Reader
   ├─ NFC reader (ISO 14443A/B)
   ├─ Location: Dashboard, near ignition
   ├─ Function: Driver authentication
   └─ Cost: $50

6. Mobile Data Terminal (MDT)
   ├─ 10" tablet (rugged, Android)
   ├─ Mounted: Center console
   ├─ Apps: OS-PATROL app, mapping, CAD
   ├─ Connectivity: 4G LTE + WiFi
   └─ Cost: $400

7. OBD-II Adapter
   ├─ ELM327 WiFi
   ├─ Location: OBD-II port
   ├─ Function: Vehicle diagnostics
   └─ Cost: $30

8. Emergency Lights & Siren
   ├─ Integrated with vehicle
   └─ Cost: $800

Total Equipment Cost: $1,950 per vehicle
Installation Labor: $500
Grand Total: $2,450 per vehicle

Compare to proprietary systems: $5,000-8,000 per vehicle
Savings: 51-69%
```

#### Tier 3: Officer/Guard Access (PIV Card)

**Role**: Operate vehicles, coordinate patrols, access network

```
┌───────────────────────────────────────────────────────────────┐
│  Officer/Guard Vehicle Interface                              │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Start of Shift:                                              │
│  1. Tap PIV card on vehicle reader                           │
│  2. Vehicle authenticates certificate                         │
│  3. Displays: "AUTHORIZED - SMITH, JOHN (SG-ON-123456)"     │
│  4. Ignition unlocks                                          │
│  5. Vehicle assigned to officer in system                     │
│  6. All equipment activated (dashcam, GPS, LPR)              │
│                                                               │
│  Mobile App (Tablet/Phone):                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ PSVN-Fleet Mobile Interface                          │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │                                                       │   │
│  │  🚗 My Vehicle: Alpha-12 (VEH-ACME-001)              │   │
│  │     Status: On Patrol                                │   │
│  │     Location: King St & Bay St                       │   │
│  │     Fuel: 67% | Speed: 45 km/h                      │   │
│  │                                                       │   │
│  │  📍 Map View:                                        │   │
│  │  [Interactive map showing:]                          │   │
│  │  • Your vehicle (blue)                               │   │
│  │  • Nearby units - own org (green)                    │   │
│  │  • Nearby units - other agencies (yellow)            │   │
│  │  • Incidents (red pins)                              │   │
│  │  • Hot-list vehicles detected (orange)               │   │
│  │                                                       │   │
│  │  🚨 Alerts:                                          │   │
│  │  ⚠️ HOT-LIST MATCH                                   │   │
│  │     Plate: ABC 1234 (Stolen Vehicle)                │   │
│  │     Location: 200m ahead on Queen St                │   │
│  │     Last seen: 30 seconds ago                        │   │
│  │     [View Details] [Request Backup]                  │   │
│  │                                                       │   │
│  │  👥 Nearby Units (5km radius):                       │   │
│  │  • Bravo-7 (Police) - 1.2km, 3 min                  │   │
│  │  • Charlie-3 (Sheriff) - 2.8km, 5 min               │   │
│  │  • Delta-9 (Campus Security) - 4.1km, 8 min         │   │
│  │  [Request Backup] [Send Message]                     │   │
│  │                                                       │   │
│  │  🔍 License Plate Search:                           │   │
│  │  [_______________] [Search Provincial Database]      │   │
│  │                                                       │   │
│  │  [Dispatch] [Chat] [Evidence] [Reports]             │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

---

## Data Flow: Complete Vehicle Operations

### Scenario 1: Routine Patrol with Automatic LPR

```
┌────────────────────────────────────────────────────────────────┐
│  STEP 1: Officer Starts Shift                                 │
└────────────────────────────────────────────────────────────────┘

Officer JOHN SMITH (SG-ON-123456) arrives at vehicle
    ↓
Taps PIV card on NFC reader in vehicle
    ↓
Vehicle system validates certificate (offline cache):
    • Certificate signed by ministry CA ✓
    • Not expired ✓
    • Not revoked (cached OCSP) ✓
    ↓
Vehicle system displays on MDT:
    "✓ AUTHORIZED
     SMITH, JOHN (SG-ON-123456)
     Acme Security Services
     
     Vehicle: Alpha-12 (VEH-ACME-001)
     Fuel: 67%
     Mileage: 45,234 km
     Status: Ready
     
     [START PATROL]"
    ↓
Officer presses START PATROL
    ↓
System activates:
    1. Ignition unlocked
    2. GPS tracking starts (5-second updates)
    3. Dashcam recording starts
    4. LPR system activates
    5. OBD-II monitoring begins
    6. Location shared with:
       - Own dispatch center
       - Provincial hub (federated)
       - Nearby authorized units
    ↓
Officer begins patrol

┌────────────────────────────────────────────────────────────────┐
│  STEP 2: Automatic License Plate Recognition                  │
└────────────────────────────────────────────────────────────────┘

Vehicle driving at 50 km/h on Main Street
    ↓
LPR camera continuously scanning:
    • 2 scans per second
    • Reads plates: forward, parked cars, oncoming
    ↓
10:15:32 - Plate detected: "ABC 1234"
    ↓
Raspberry Pi processes with OpenALPR:
    • Confidence: 96%
    • Jurisdiction: Ontario
    ↓
System checks hot-lists (local + provincial):
    
    1. Local cache (instant):
       ├─ Stolen vehicles
       ├─ Amber alerts
       ├─ Wanted persons
       ├─ Parking violations
       └─ No match
    
    2. Provincial database (via API):
       Query: GET /lpr/check?plate=ABC1234&jurisdiction=ON
       Response: {
           "hot_list_status": {
               "stolen": true,
               "reported": "2025-12-18",
               "case_number": "2025-5678",
               "agency": "City Police Department"
           }
       }
    ↓
🚨 HOT-LIST MATCH DETECTED 🚨
    ↓
System immediately:
    
    1. Alert driver on MDT:
       "⚠️ STOLEN VEHICLE DETECTED
        Plate: ABC 1234
        Location: Main St & 5th Ave (ahead 50m)
        Status: Moving eastbound
        Case: 2025-5678 (City Police)
        [VIEW DETAILS] [REQUEST BACKUP] [PURSUE]"
    
    2. Capture evidence:
       • Photo of plate (high-res)
       • Dashcam video (30 sec before + continuous)
       • GPS location
       • Timestamp
       • Officer PIV ID
    
    3. Upload to provincial hub:
       POST /lpr/sighting
       {
           "plate": "ABC1234",
           "timestamp": "2025-12-20T10:15:32Z",
           "location": {"lat": 43.6532, "lon": -79.3832},
           "scanning_unit": "VEH-ACME-001",
           "officer": "SG-ON-123456",
           "hot_list_match": true,
           "case_number": "2025-5678",
           "confidence": 0.96,
           "image_url": "s3://evidence/lpr/2025-12-20/..."
       }
    
    4. Notify provincial hub:
       Hub broadcasts to all units within 5km:
       "STOLEN VEHICLE SIGHTED
        Plate: ABC 1234
        Location: Main St & 5th Ave, heading east
        Scanning unit: Alpha-12 (Acme Security)
        All units: Be on lookout, do not approach"
    
    5. Notify originating agency (City Police):
       Real-time alert to detective on Case #2025-5678
    ↓
Officer decides to follow at safe distance
    ↓
Dashcam continuously records
LPR continues scanning (every 500ms confirms same vehicle)
GPS tracks vehicle path
    ↓
10:18:45 - Vehicle turns into parking lot
    ↓
Officer presses REQUEST BACKUP on MDT
    ↓
System finds nearest available units:
    
    Nearby Units:
    1. Bravo-7 (City Police) - 1.2km, ETA 3 min
    2. Charlie-3 (Sheriff) - 2.8km, ETA 5 min
    ↓
Backup request sent automatically
    ↓
Bravo-7 acknowledges, en route
    ↓
10:21:30 - Police unit arrives
    ↓
Safe vehicle stop, suspect apprehended
    ↓
All dashcam footage automatically:
    • Bookmarked
    • Uploaded to evidence server
    • Linked to case #2025-5678
    • Blockchain chain-of-custody initiated
    • Available to detective within minutes

Traditional approach:
└─ Officer might not know vehicle was stolen
   Manual BOLO check (if remembered)
   Radio for backup (slower)
   No automatic evidence capture
   Suspect might escape

PSVN-Fleet approach:
└─ Automatic detection (<1 second)
   Instant alerts to all nearby units
   Real-time coordination
   Complete evidence capture
   Successful apprehension
```

### Scenario 2: Cross-Jurisdictional Pursuit

```
┌────────────────────────────────────────────────────────────────┐
│  STEP 1: Pursuit Begins in City A                             │
└────────────────────────────────────────────────────────────────┘

14:30 - City A Police Officer initiates traffic stop
    ↓
Suspect flees, pursuit begins
    ↓
Officer activates PURSUIT mode on MDT:
    • GPS tracking increased to 1-second updates
    • Dashcam switches to high-bitrate recording
    • Emergency lights activated (logged)
    • Provincial hub notified automatically
    ↓
Provincial hub broadcasts PURSUIT ALERT:
    "ACTIVE PURSUIT
     Initiating Unit: Unit-5 (City A Police)
     Vehicle: Black Honda Civic, Plate ABC 1234
     Direction: Heading north on Highway 401
     Speed: 140 km/h
     All agencies: Monitor and prepare to assist"
    ↓
Real-time pursuit map displayed to:
    • City A dispatch
    • Provincial hub
    • All nearby agencies within 50km
    ↓
Every unit sees:
    • Blue icon: Pursuing officer (Unit-5)
    • Red icon: Suspect vehicle (real-time)
    • Green icons: Available backup units

┌────────────────────────────────────────────────────────────────┐
│  STEP 2: Pursuit Crosses into City B Jurisdiction             │
└────────────────────────────────────────────────────────────────┘

14:35 - Suspect crosses city boundary
    ↓
Traditional: City A officer must stop (jurisdiction ends)
            Suspect escapes
    ↓
PSVN-Fleet: Seamless coordination
    ↓
Provincial hub:
    1. Identifies nearest City B units:
       • Unit-12 (City B Police) - 2km ahead
       • Unit-18 (Sheriff) - 5km ahead
    
    2. Automatically sends INTERCEPT request:
       "PURSUIT ENTERING YOUR JURISDICTION
        Suspect: Black Honda Civic, ABC 1234
        ETA: 2 minutes
        Speed: 140 km/h
        Primary pursuit: Unit-5 (City A)
        Request: Position for intercept"
    
    3. City B Unit-12 acknowledges:
       "Unit-12 responding, positioning on Highway 401 exit"
    ↓
City A Unit-5 continues pursuit (authorized cross-jurisdiction)
City B Unit-12 positions ahead
    ↓
Real-time coordination via shared map:
    • All units see each other's positions
    • Predicted suspect path shown (AI)
    • Optimal intercept points suggested
    ↓
14:37 - City B Unit-12 successfully deploys spike strip
    ↓
Suspect vehicle disabled
    ↓
Safe apprehension by City B officers
    ↓
City A officer arrives 30 seconds later

┌────────────────────────────────────────────────────────────────┐
│  STEP 3: Evidence Aggregation & Reporting                     │
└────────────────────────────────────────────────────────────────┘

System automatically collects evidence:
    
    1. City A Unit-5 dashcam:
       • Initial traffic stop
       • Pursuit (5 minutes, 12 GB video)
       • Uploaded to PBCEN
    
    2. City B Unit-12 dashcam:
       • Intercept position
       • Spike strip deployment
       • Apprehension
       • Uploaded to PBCEN
    
    3. GPS tracks:
       • Complete pursuit path (both units)
       • Speed data (every second)
       • Exported to KML format
    
    4. LPR scans:
       • 15 different units scanned suspect plate
       • Complete timeline of sightings
       • Proves vehicle movements
    
    5. Radio logs:
       • All communications
       • Timestamps synchronized
    ↓
Evidence package automatically generated:
    • All videos (blockchain-verified)
    • GPS tracks overlaid on map
    • Timeline visualization
    • LPR scan history
    • Officer body cam footage (from PBCEN)
    • Fixed camera footage (from PSVN)
    ↓
Shared with:
    • City A Police (originating agency)
    • City B Police (assisting agency)
    • Prosecutor's office
    • Defense counsel (disclosure)
    ↓
Case file complete within 1 hour of incident
    ↓
Trial preparation time: Reduced from weeks to days

Traditional approach:
└─ Pursuit stops at boundary
   Or: Requires supervisor approval + radio coordination
   Evidence: Fragmented, manual collection
   Report writing: 4-8 hours per officer
   Total time: 2-3 weeks

PSVN-Fleet approach:
└─ Seamless cross-jurisdiction
   Real-time coordination
   Automatic evidence collection
   Report generation: 15 minutes
   Total time: 1 hour
```

### Scenario 3: Multi-Agency Incident Response

```
┌────────────────────────────────────────────────────────────────┐
│  Large-Scale Emergency - Shopping Mall Active Threat          │
└────────────────────────────────────────────────────────────────┘

16:00 - 911 call: Active threat at Westfield Mall
    ↓
Provincial hub creates incident:
    
    POST /dispatch/incident
    {
        "type": "active_threat",
        "location": {"lat": 43.7, "lon": -79.4},
        "priority": "emergency",
        "estimated_units_needed": 15,
        "special_requirements": ["supervisor", "medical", "k9"]
    }
    ↓
Hub automatically identifies all units within 20km:
    • 8 City Police units
    • 5 Sheriff units
    • 12 Security company vehicles
    • 3 Campus security units
    • 2 Fire/EMS units
    
    Total: 30 units available
    ↓
Hub dispatches optimally:
    1. Nearest 10 units: Perimeter establishment
    2. Supervisor units: Command post
    3. K9 units: Building search
    4. Medical: Staging area
    5. Security vehicles: Evacuation support
    ↓
ALL units receive real-time alerts on MDT:
    "🚨 EMERGENCY DISPATCH
     
     Active Threat - Westfield Mall
     123 Mall Road
     
     Your assignment: [specific role]
     Route: [optimal path shown on map]
     ETA: 5 minutes
     
     Incident Commander: Unit-Supervisor-3
     Command Post: Mall north parking lot
     
     Other responding units: [live map]
     
     [ACKNOWLEDGE] [EN ROUTE] [ON SCENE]"
    ↓
Real-time coordination map:
    • All 30 units visible (different colors by agency)
    • Incident location (red pin)
    • Perimeter zones (auto-calculated)
    • Evacuation routes
    • Command post location
    • Medical staging area
    ↓
As units arrive:
    • Auto check-in (GPS confirms on-scene)
    • Status updates: "On perimeter", "Entering building"
    • Body cameras auto-activate (PBCEN)
    • Dashcams bookmark incident time
    ↓
16:45 - Threat neutralized
    ↓
All units:
    • Evidence auto-collected (30 dashcams)
    • Response timeline generated
    • After-action report templates pre-filled
    • Debriefing scheduled automatically
    ↓
Provincial hub analytics:
    • Response time: Average 6.2 minutes
    • Multi-agency coordination: Seamless
    • Evidence collected: 45 GB (all vehicles + body cams)
    • Lessons learned: Documented
    ↓
System continuously improves future responses
```

---

## Privacy & Security

### Vehicle Data Privacy

**What's Tracked:**
- Vehicle location (when on duty)
- Speed, heading
- Driver identity (PIV ID)
- License plates scanned (publicly visible plates)
- Dashcam (forward view - public roads)
- OBD-II diagnostics (vehicle health)

**What's NOT Tracked:**
- Off-duty location
- Personal conversations (no interior audio recording)
- Private property without authorization
- Non-public areas

**Access Controls:**
| Role | View Own Vehicles | View Other Agency | LPR Database | Historical Tracks |
|------|-------------------|-------------------|--------------|-------------------|
| **Officer** | Current shift only | No | Search only | Own vehicle, 24hrs |
| **Supervisor** | All | Nearby (5km) | Full access | All vehicles, 7 days |
| **Dispatch** | All | Authorized agencies | Full access | All vehicles, 30 days |
| **Investigator** | Case-related | Court order | Case-related | Court order |
| **Admin** | All | All (audit) | All (audit) | All, 90 days |

### License Plate Privacy

**Automatic Redaction:**
- Plates scanned on private property: Not uploaded
- Plates of law enforcement vehicles: Redacted
- Residential areas: Optional redaction
- Retention: 90 days for routine scans, 7 years for hot-list matches

**ALPR Best Practices:**
- Only public roadways
- Audit all searches
- Limit retention
- Public transparency reports

---

## Cost Economics

### Per-Vehicle Costs

**Traditional Proprietary Fleet System:**
```
Equipment per vehicle:
├─ GPS tracker: $300
├─ Dashcam: $600
├─ LPR system: $3,000
├─ MDT: $800
├─ Installation: $800
└─ Total Hardware: $5,500

Software (Annual per vehicle):
├─ Fleet tracking: $400/year
├─ Dashcam platform: $200/year
├─ LPR service: $600/year
└─ Total Software: $1,200/year

5-Year TCO per vehicle:
├─ Hardware: $5,500
├─ Software: $6,000
└─ Total: $11,500
```

**PSVN-Fleet Open Source:**
```
Equipment per vehicle:
├─ GPS tracker: $120
├─ Dashcam: $250
├─ LPR (Raspberry Pi): $150
├─ MDT: $400
├─ PIV reader: $50
├─ Installation: $500
└─ Total Hardware: $1,470

Software (Annual per vehicle):
├─ OS-PATROL license: $0
├─ PSVN-Fleet membership: $100/year
└─ Total Software: $100/year

5-Year TCO per vehicle:
├─ Hardware: $1,470
├─ Software: $500
└─ Total: $1,970

Savings per vehicle: $9,530 (83%)
```

**100 Vehicle Fleet:**
- Traditional: $1,150,000
- PSVN-Fleet: $197,000
- **Savings: $953,000 (83%)**

### Provincial Network ROI

**Ministry Operating Costs:**
```
Annual Budget (1,000 organizations, 10,000 vehicles):

Infrastructure:
├─ Vehicle registry servers: $300,000
├─ LPR database: $400,000
├─ Real-time tracking: $200,000
├─ Analytics platform: $150,000
└─ Total: $1,050,000

Staff:
├─ Technical (5 FTE): $500,000
├─ Dispatch coordination (3 FTE): $300,000
├─ Support (4 FTE): $300,000
└─ Total: $1,100,000

Operations:
├─ Bandwidth: $150,000
├─ Compliance: $100,000
└─ Total: $250,000

Grand Total: $2,400,000/year
```

**Revenue:**
```
Membership Fees:
├─ Small fleets (1-10): $1,000/year × 600 = $600,000
├─ Medium (11-50): $3,000/year × 250 = $750,000
├─ Large (51-200): $10,000/year × 100 = $1,000,000
├─ Enterprise (200+): $25,000/year × 50 = $1,250,000
└─ Total: $3,600,000/year

Surplus: $1,200,000 → Technology R&D
```

**Province-Wide Benefits:**
```
Quantified Annual Savings:

Law Enforcement Efficiency:
├─ Faster response: $50M/year
├─ Cross-jurisdiction coordination: $30M/year
├─ Evidence collection automation: $20M/year
└─ Total: $100M/year

Fleet Optimization:
├─ Vehicle sharing: $40M/year
├─ Fuel savings (route optimization): $25M/year
├─ Maintenance (predictive): $15M/year
└─ Total: $80M/year

Public Safety:
├─ Stolen vehicle recovery: $60M/year
├─ Faster emergency response: Priceless
├─ Crime prevention (LPR deterrence): $40M/year
└─ Total: $100M+/year

Total Annual Benefit: $280M+
Cost: $2.4M
ROI: 11,567%
```

---

## Implementation Roadmap

### Phase 1: Pilot (6 months)

**Scope**: 5 organizations, 100 vehicles

Month 1-2: Infrastructure
├─ Deploy provincial vehicle hub
├─ Set up LPR database
├─ Configure tracking servers

Month 3-4: Vehicle Deployment
├─ Install equipment in 100 vehicles
├─ Train 50 officers/guards
├─ Test cross-agency coordination

Month 5-6: Evaluation
├─ Measure response time improvements
├─ Test LPR accuracy
├─ Gather user feedback
└─ Refine for rollout

**Budget**: $400,000

### Phase 2: Regional (12 months)

**Scope**: 50 organizations, 1,000 vehicles

### Phase 3: Province-Wide (24 months)

**Scope**: 500+ organizations, 10,000 vehicles

---

## Conclusion

**PSVN-Fleet completes the provincial security ecosystem:**

1. **OpenPIV + OS-PACS** → Universal credentials & door access
2. **PSVN** → Universal video surveillance
3. **PBCEN** → Universal body camera evidence
4. **PSVN-Fleet** → Universal vehicle coordination

**Together creating:**
✅ One PIV card controls everything
✅ Real-time cross-agency coordination
✅ Automatic suspect tracking
✅ Evidence automatically aggregated
✅ 80%+ cost savings
✅ Network effects benefiting everyone

**From isolated vehicles → connected fleet → coordinated response → safer province**

---

**Document Version**: 1.0  
**Date**: December 2025  
**Author**: Toussaint Louis  
**Status**: Concept Proposal

**For More Information:**
- tech-fleet@securityguard.gov.on.ca
- https://os-patrol.org


<!-- AUTO-GENERATED RELATED START (scripts/build_obsidian_graph.py) -->

## Related (auto-generated)

**Topics:**
- [[knowledge-base/_topics/opensecure-provincial-security-network|opensecure-provincial-security-network]]
- [[knowledge-base/_topics/provincial-security-network-programs|provincial-security-network-programs]]

**Consolidated into:**
- [[docs/DC-OPENSECURE-PROVINCIAL-PIV-CREDENTIAL-RECONCILED-001]]
- [[docs/DC-PROVINCIAL-SECURITY-NETWORK-RECONCILED-001]]

<!-- AUTO-GENERATED RELATED END -->
