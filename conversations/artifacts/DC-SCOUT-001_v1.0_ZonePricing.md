---
source_conversation_uuid: 7963735d-a671-4b42-806e-651377fd29b2
conversation_title: 'Fixing operational visibility in decentralized construction'
created_at: 2026-06-10T01:34:30.970459Z
doc_id: DC-SCOUT-001
description: 'D-SCOUT architecture document - drone survey, proximity pricing, and zone campaign system'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
---

# DC-SCOUT-001 v1.0: D-SCOUT — Drone Survey, Condition Assessment & Unified Targeting
## D-Central Field Operations Intelligence System
**Registry ID:** DC-SCOUT-001 v1.0  
**Parent Documents:** DC-COOP-001 v2.0, DC-FOS-001, DC-DRONE (Tier 12)  
**Status:** Architecture Draft v1.0  
**Date:** 2026-06-09  

---

## System Overview

D-SCOUT is the operational intelligence backbone of the D-Central field enterprise. While crews work a job site, a drone surveys the surrounding neighborhood. The resulting data flows through a photogrammetry pipeline, a condition scoring model, and a proximity pricing engine to generate a **Zone Campaign** — a prioritized, priced, and routed set of leads that keeps the crew working within a compact geographic area rather than being scattered across the city.

The core economic insight is this: **the cost of a job to a client is partially a function of where the crew already is.** When the crew is already on the street, there is no equipment transit cost, no crew carpool overhead, and no deadhead drive time. That efficiency has a dollar value — and D-SCOUT passes it to the client as a pricing incentive, creating alignment between client savings, crew productivity, and cooperative revenue.

**What D-SCOUT produces:**
- Property-level aerial imagery and condition scores for all properties within the survey radius
- Accurate lot and landscapeable area measurements (replacing manual estimation)
- D-RECORD entries for every surveyed property (permanent property intelligence)
- D-LEADS entries for all high-opportunity properties
- Dynamic zone pricing per property (adjusting as nearby bookings accumulate)
- An ordered Zone Campaign: which properties to contact, in what sequence, to fill the cluster most efficiently
- Drone footage for D-CONTENT marketing output

---

## The Zone Pricing Mechanism

This is the commercial core of D-SCOUT. Everything else serves this.

### Why standard pricing is wrong

Standard pricing treats every job as isolated. The quote for a property in Orleans assumes the crew drives from the yard, works the job, and drives back. That is an accurate cost model for an isolated job. But when three other jobs are booked within 500m, the marginal cost of that fourth job drops dramatically:

- No additional equipment transit (machine is already on site or a 200m move)
- No additional crew carpool (crew already in the area)
- Reduced machine setup time (repeat site layout, same soil conditions)
- Scheduling certainty (weather-related delays affect the whole cluster, not individual jobs)

Standard pricing ignores this. The owner charges the same rate regardless of job proximity. The client has no incentive to care when they book. The result: a schedule that looks like a random scatter plot across Ottawa.

### Zone Pricing Model

```
FINAL PRICE = BASE QUOTE × (1 − PROXIMITY DISCOUNT − CLUSTER BONUS)

BASE QUOTE:
  = Landscapeable area (sq ft) × Service rate ($/sq ft)
  + Material cost (from D-SUPPLY current pricing)
  + Labor estimate (hours × rate × site complexity multiplier)

PROXIMITY DISCOUNT (distance to nearest booked job or active site):
  ≤ 500m   → 12%
  500–1km  → 8%
  1–2km    → 4%
  > 2km    →  0% (standard pricing)

CLUSTER BONUS (booked jobs within 2km of this property):
  5+ nearby booked jobs → 8% additional
  3–4 nearby booked jobs → 5% additional
  1–2 nearby booked jobs → 2% additional
  0 nearby booked jobs → 0%

MAXIMUM ZONE DISCOUNT: 18% (proximity + cluster combined)
FLOOR: standard price (no penalty for isolated jobs, ever)
```

### The cascade effect

Zone pricing is self-reinforcing:
1. Crew is working Site A in Orleans
2. D-SCOUT surveys 500m radius → identifies 18 opportunity properties
3. D-LEADS sends outreach to high-condition-score properties with zone pricing offer
4. Property B books → Properties C, D, E near B now have a larger cluster → their prices drop
5. Properties C, D, E see the improved discount → more convert
6. Cluster fills to 6 jobs → Crew works in Orleans for 2 full days → zero equipment transit → maximum utilization

The client is incentivized to book soon because:
- The zone discount only applies when scheduled in the cluster window
- Once the cluster window fills, standard pricing resumes
- Adjacent clients benefit from each other's bookings

### Cooperative transparency of pricing

The pricing logic is disclosed to clients, not hidden:
> *"Our price for your property is lower because our crew will be working in your neighborhood on [date]. We save on equipment transport and pass that directly to you. The zone pricing window closes when the schedule fills."*

This is D-Central's cooperative transparency principle in the pricing layer: clients understand why they pay what they pay, which builds trust and drives urgency to book within the cluster window.

---

## Survey Pipeline

### Phase 1: Mission Planning

Triggered automatically when a job is booked or manually by the site lead through D-MESH.

**Pre-flight checks (integrated into D-JOB pre-roll gate):**
- Airspace authorization: NAV CANADA DroneHub API call → confirm Class G or obtain RPAS Special Flight Operations Certificate for Class C
- Weather: D-WEATHER check → wind < 25 km/h, no precipitation, visibility > 3 statute miles
- Pilot assignment: D-TRAIN credential verification → assigned pilot holds correct certificate for airspace class
- Battery status: D-ASSET battery register → minimum 2 fully charged batteries
- Survey radius: default 500m from job site center; configurable 200m–1km based on pilot's available time
- Privacy filter: confirm imagery processing will exclude identifiable individuals (faces, license plates)

**Ottawa airspace notes:**
- Central Ottawa and areas near YOW require Advanced RPAS Certificate and NOTAM/NAN check
- Orleans, Barrhaven, Kanata fringe areas are predominantly uncontrolled (Class G) → Basic Certificate sufficient
- Gatineau Park edges → special consideration
- D-WEATHER and airspace check must both clear before mission authorization fires

**Flight plan generation:**
- Grid pattern over survey area (parallel north-south passes)
- Altitude: 80m AGL (above ground level) — optimal for GSD (ground sample distance) vs flight time
- Photo overlap: 80% front, 70% side — required for photogrammetry reconstruction
- Estimated flight time: ~15–20 min for 500m radius, ~2 batteries
- Output: KML/GPX flight plan compatible with DJI, Autel, and Skydio flight apps

### Phase 2: Data Collection

Drone executes the grid mission. Crew lead monitors from a designated ground control point.

**Data captured:**
- 200–400 geotagged JPEG images (GPS coordinates embedded in EXIF)
- Altitude and gimbal angle data per photo
- Video log (optional — for D-CONTENT output)
- Total flight logged in D-ASSET (pilot, battery cycles consumed, engine hours)

### Phase 3: Photogrammetry Processing

**Stack: OpenDroneMap (ODM) — free, open source, self-hosted**

ODM runs on the cooperative's VPS or on a dedicated local machine at the yard. Processing begins automatically when photos are uploaded from the drone SD card or synced via D-MESH.

**ODM outputs:**
- Orthophoto (GeoTIFF): georeferenced mosaic, 3–5 cm/pixel resolution
- DSM (Digital Surface Model): height data across the survey area
- Point cloud (LAS): 3D representation of the terrain and structures
- Processing time: 20–45 min for a 500m radius survey on a modern 4-core server

**WebODM:** The browser-based UI for ODM. Site leads access it through D-MESH to review results, annotate properties, and confirm output quality before the pipeline continues.

### Phase 4: Property Identification

**Ottawa Open Data integration:**

The City of Ottawa provides open-access GIS datasets including property parcel boundaries (polygons keyed to civic addresses). This data is loaded into the D-SCOUT GIS layer on first use and updated quarterly.

**Process:**
1. Overlay Ottawa property parcel boundaries (GIS polygon layer) on the ODM orthophoto
2. For each parcel intersecting the survey area: extract the address, lot area (from parcel data), and the portion of the orthophoto corresponding to that property
3. Estimate landscapeable area: lot area − building footprint (derived from DSM height data) − estimated hardscape (driveway, walkway — detected from satellite-level visible spectrum contrast)
4. Store as D-RECORD entry: address, coordinates, lot area, landscapeable area, aerial image tile, survey date

**Result:** Every property within the survey radius now has a D-RECORD entry regardless of whether they are a current client. This is the city-scale property intelligence database that builds over time.

### Phase 5: Lawn Condition Scoring

**Method: RGB vegetation index analysis**

True NDVI requires a near-infrared camera. D-SCOUT uses an RGB proxy that gives 80% of the value at zero additional hardware cost.

**Vegetation proxy index (VPI):**
```
VPI = (G − R) / (G + R + 0.001)

Where:
  G = mean green channel value within the lawn polygon (0–255)
  R = mean red channel value within the lawn polygon (0–255)

Range: −1 (bare soil/pavement) to +1 (dense healthy vegetation)

Condition score mapping:
  VPI > 0.30  → Score 9 (Excellent)
  0.20–0.30   → Score 7–8 (Good)
  0.10–0.20   → Score 5–6 (Fair)
  0.00–0.10   → Score 3–4 (Poor/Struggling)
  < 0.00      → Score 1–2 (Critical — bare, dead, or hardscape)
```

**Secondary indicators (detected via color segmentation):**
- Brown/yellow patch coverage (% of lawn polygon showing stress coloration)
- Bare soil exposure (bare soil has distinctive spectral signature)
- Drainage pooling indicators (DSM low-point analysis — potential drainage issues visible from height data)
- Relative coverage (what % of the lot polygon is green vs impervious)

**Output per property:**
- Condition score (1–9)
- Dominant issue flag: dead / sparse / stressed / weed-dominated / drainage / healthy
- Aerial crop image (stored in D-RECORD, visible in D-LEADS)

### Phase 6: Zone Campaign Generation

With all 200–400 properties in the survey radius scored and priced, D-SCOUT generates the Zone Campaign.

**Zone Campaign output:**

```
ZONE CAMPAIGN: Orleans East — Survey 2026-06-15
Origin job: 481 Portobello Blvd (active site, crew deployed)
Survey radius: 500m | Properties identified: 183 | Opportunity tier: HIGH

Priority 1 — Same-block leads (0–200m, condition score 1–4): 8 properties
  → Immediate zone price applies: 12% proximity + 0-8% cluster
  → Recommended outreach: door hanger + D-LEADS automated message today

Priority 2 — Near-zone leads (200–500m, condition score 1–5): 23 properties
  → Zone price applies on booking: 8–12% combined discount
  → Recommended outreach: D-LEADS automated message + D-CANVAS follow-up tomorrow

Priority 3 — Zone extension leads (500m–1km, condition score 1–4): 41 properties
  → Partial zone price on booking: 4–8% discount
  → Recommended outreach: D-CONTENT neighborhood post + direct D-LEADS message

Existing D-MEMBER clients in zone: 4 (pre-scheduled priority for zone week)

OPTIMAL BOOKING SEQUENCE (to maximize cluster density):
  Book A, B, C first → unlocks cluster bonus for D, E, F
  Book D, E, F → unlocks bonus for G, H, I, J
  Full 10-job cluster → all clients at 15%+ zone pricing, crew in Orleans 3 days

ZONE WEEK REVENUE PROJECTION:
  If 5 jobs booked: $8,200 zone revenue, 68% crew utilization
  If 8 jobs booked: $13,100 zone revenue, 94% crew utilization
  If 10 jobs booked: $16,400 zone revenue, full cluster, 2.3 days in zone
```

**Zone map:** Visual overlay of the neighborhood with properties color-coded by priority tier, existing clients marked, and the optimal booking sequence numbered. Accessible through D-MESH for the site lead and owner.

---

## Integration with D-Central Systems

| System | D-SCOUT Input | D-SCOUT Output |
|--------|--------------|----------------|
| D-DRONE | Flight execution, battery tracking | Survey hours logged, maintenance trigger |
| D-RECORD | Reads existing property data | Creates/updates property entries for all surveyed properties |
| D-LEADS | — | Auto-creates prioritized leads for all high-opportunity properties |
| D-QUOTE | Reads current material/labor rates | Generates pre-priced quotes with zone pricing applied |
| D-ROUTE | — | Zone campaign feeds into weekly schedule clustering |
| D-UTIL | — | Zone fill rate feeds crew utilization projections |
| D-NEIGHBOR | — | Neighborhood penetration map updated with survey coverage |
| D-CANVAS | — | Door hanger deployment list auto-generated by address |
| D-CONTENT | — | Orthophoto → neighborhood map content, before-images for client outreach |
| D-SEO | — | Neighborhood data enriches Ottawa hyperlocal search content |
| D-MAINT | — | Flight hours → battery cycle count → replacement trigger |
| D-MEMBER | Reads existing client locations | Flags existing members in survey area, pre-schedules them into cluster |
| D-SUPPLY | — | Landscapeable area data → pre-calculated material quantities for upcoming zone jobs |

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Drone | DJI Mini 4 Pro / Air 3 or Autel Evo Lite | Survey platform (Advanced RPAS certified) |
| Flight planning | DJI Fly / Litchi / DroneLink | Grid mission planning with overlap settings |
| Photogrammetry | OpenDroneMap (ODM) | Photo → orthophoto, DSM, point cloud (free, self-hosted) |
| ODM UI | WebODM | Browser-based review and quality check |
| GIS / mapping | QGIS (desktop) + Leaflet.js (web) | Property overlay, zone map display |
| Ottawa property data | City of Ottawa Open Data Portal | Parcel boundaries, civic addresses (free) |
| Vegetation scoring | Python (NumPy + Pillow) | Per-property VPI calculation from orthophoto tiles |
| Database | PostgreSQL + PostGIS extension | Geospatial property intelligence storage |
| Zone campaign engine | Node.js | Pricing calculation, cluster optimization, campaign generation |
| Drone field review | D-MESH (PWA) | Site lead views results, confirms leads, launches outreach |
| Airspace | NAV CANADA DroneHub API | Pre-flight authorization (free) |
| Map tiles | OpenStreetMap + Leaflet.js | Base map for zone visualization |

**Total additional infrastructure cost for D-SCOUT: $0/month.** All software is free and open source. Runs on the same VPS used for the rest of the D-Field stack.

**One-time hardware cost:**
- DJI Mini 4 Pro (under 250g, reduced regulatory overhead): ~$900 CAD
- Extra batteries (×4): ~$400 CAD
- Carrying case, ND filters, SD cards: ~$150 CAD
- Total: ~$1,450 CAD

**Payback calculation:**
If D-SCOUT generates 3 additional zone-cluster jobs per month (conservative for Ottawa sod season), at average $1,800/job = $5,400 additional monthly revenue. Hardware cost recovered in < 1 month of operation.

---

## Transport Canada Compliance Protocol

**Legal basis:** Canadian Aviation Regulations (CARs), Part IX — Remotely Piloted Aircraft Systems

**Required per flight:**
1. Valid Transport Canada RPAS pilot certificate (Basic or Advanced as required by airspace)
2. Drone registration number displayed on aircraft
3. Pre-flight NOTAM check (NAV CANADA website or DroneHub app)
4. Pre-flight airspace authorization where required (RPAS Portal)
5. Visual line of sight (VLOS) maintained at all times
6. No flight over people without Advanced certificate
7. Flight log maintained (logged automatically in D-DRONE via D-ASSET)

**Privacy compliance (PIPEDA):**
- Survey imagery used for property condition assessment only
- Individual people in imagery: blurred by post-processing before storage
- License plates: blurred by post-processing before storage
- Client aerial imagery shared publicly only with property owner consent
- D-RECORD stores property condition data, not personal information about residents
- Survey disclosure: Sod Boys discloses aerial survey use in its service terms

**Survey scope policy:**
- Survey covers visible exterior property conditions from public airspace
- No directional camera angles into windows or private enclosed spaces
- Flight altitude minimum 50m to ensure survey rather than voyeuristic character
- Any property owner who requests removal from D-RECORD: complied within 10 business days

---

## Economic Impact Model

**Per-season projections (Ottawa sod season: May–October, ~26 weeks):**

| Metric | Without D-SCOUT | With D-SCOUT |
|--------|----------------|-------------|
| Average km driven per job | 18km (cross-city scatter) | 3.2km (zone clusters) |
| Fuel cost per job | ~$12 | ~$2.20 |
| Machine transit per job | 45 min avg | 8 min avg |
| Jobs per crew-day | 1.4 avg | 2.1 avg |
| Lead conversion rate | ~15% (cold outreach) | ~38% (aerial-informed, proximity offer) |
| Revenue per crew-week | ~$5,600 | ~$8,400 |
| Seasonal revenue uplift | baseline | +$73,000 (26 weeks × $2,800/wk delta) |
| Client savings (zone pricing) | $0 | ~$180/job average → passed to clients |
| Quote accuracy | ±20% (manual estimation) | ±4% (aerial measurement) |

**The $73,000 figure is conservative.** It assumes 2.5 additional zone-clustered jobs per week at standard average revenue, driven entirely by the clustering efficiency gain. It does not include the incremental revenue from higher lead conversion rates driven by aerial pre-qualification and condition scoring.

---

## Registry Classification

```
Document ID:     DC-SCOUT-001
Version:         1.0 (Architecture Draft)
Domain:          Field Intelligence & Zone Pricing
System:          D-SCOUT (Drone Survey, Condition Assessment, Unified Targeting)
Parent:          DC-COOP-001 v2.0, DC-FOS-001
Feeds:           D-RECORD, D-LEADS, D-QUOTE, D-ROUTE, D-UTIL, D-NEIGHBOR,
                 D-CANVAS, D-CONTENT, D-SEO, D-SUPPLY, D-MEMBER
Requires:        D-DRONE (Tier 12), D-IoT (GPS tracking), D-MAINT
Upgrade path:    Multi-drone fleet, LiDAR sensor fusion, ML condition model,
                 real-time market pricing integration, D-FRANCHISE network-wide zone coordination
```

---

*The drone is not the product. The product is the cluster. The drone makes the cluster visible before it exists — and the pricing model gives everyone inside it a reason to book.*
