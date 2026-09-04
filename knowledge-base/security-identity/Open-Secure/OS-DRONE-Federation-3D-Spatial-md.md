---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: f2ea6e43-b91b-44d5-9a86-860fb7e98aad
original_filename: OS-DRONE_Federation_3D_Spatial.md
created_at: 2026-03-05T13:49:35.439296+00:00
content_hash: bfd7f88691e2topic: sony-served-construction
topic: opensecure-os-drone-advanced-capabilities
---

# OS-DRONE Federation & 3D Spatial Intelligence
## Secure Ecosystem Federation, Open-Source 3D Reconstruction, and Living Spatial Models

**Document Type**: Integration & Spatial Architecture Specification
**Version**: 1.0
**Date**: March 2026
**Classification**: Technical Documentation
**Audience**: Platform Engineers, GIS/Spatial Architects, Security Operations, DevOps

---

## Table of Contents

1. [The Vision: Drones as the Spatial Intelligence Layer](#the-vision)
2. [Secure Federation Architecture](#secure-federation-architecture)
3. [Per-Service Federation Protocols](#per-service-federation-protocols)
4. [The 3D Spatial Intelligence Pipeline](#the-3d-spatial-intelligence-pipeline)
5. [Open-Source Toolchain: Complete Stack](#open-source-toolchain)
6. [LiDAR Point Cloud Processing](#lidar-point-cloud-processing)
7. [Photogrammetry: Photos to 3D Models](#photogrammetry-photos-to-3d-models)
8. [Living Digital Twin Integration](#living-digital-twin-integration)
9. [Federated 3D Map: Multi-Org Spatial Sharing](#federated-3d-map)
10. [Real-Time 3D Situational Awareness](#real-time-3d-situational-awareness)
11. [3D Change Detection & Anomaly System](#3d-change-detection--anomaly-system)
12. [GIS Integration & Spatial Databases](#gis-integration--spatial-databases)
13. [Web-Based 3D Visualization Stack](#web-based-3d-visualization-stack)
14. [Docker Compose: Full Deployment](#docker-compose-full-deployment)
15. [Kafka Topic Map: Spatial Events](#kafka-topic-map-spatial-events)

---

## The Vision

The OS-DRONE fleet is the only component in the OpenSecure ecosystem that moves across an entire site continuously, looking down. That makes it the **natural spatial intelligence layer** — the system that builds and keeps alive a 3D model of the physical world that every other service operates within.

Without drones, the digital twin is a static import — a CAD file or a point-in-time photogrammetry scan that goes stale the moment something changes. With drones feeding a continuous reconstruction pipeline, the 3D model becomes a **living document** that reflects reality in near-real-time. Every fence that moves, every vehicle that parks permanently, every new construction is captured, processed, and pushed into the digital twin automatically.

At the same time, the drone fleet only reaches its full intelligence potential when it is **deeply federated** with the other services — not just receiving alerts and dispatching, but sharing 3D context, layering evidence from all sensors into a unified spatial picture, and enabling every service to reason about *where* things are happening in three dimensions.

```
┌────────────────────────────────────────────────────────────────────────┐
│              THE OS-DRONE SPATIAL INTELLIGENCE LAYER                   │
│                                                                        │
│  OS-DRONE generates:      Other services consume:                      │
│  ─────────────────────    ─────────────────────────────────────────    │
│  • 3D point clouds        OS-SENTINEL: camera FOV accuracy in 3D      │
│  • Orthomosaic maps        OS-PATROL: route planning on true terrain   │
│  • Change detection        OS-PACS: perimeter model, breach geometry   │
│  • Terrain models          OS-GUARDIAN: georeference body cam footage  │
│  • LiDAR snapshots         OS-CONCIERGE: site wayfinding in AR        │
│  • Thermal heatmaps        Digital Twin: base map always current       │
│  • Multispectral data      All services: incident geolocation in 3D    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Secure Federation Architecture

### Design Principles

Federation between OS-DRONE and other services follows the same principles as the rest of the OpenSecure ecosystem — but with three additional requirements unique to drones:

1. **Drone data is location-sensitive** — all data carries GPS provenance and must be access-controlled by spatial scope (an org can only query drone data from their own site boundary)
2. **3D data is large** — point clouds and orthomosaics are gigabytes, not kilobytes. Federation uses streaming and tiling, not bulk transfer
3. **Real-time + historical** — drones produce both live telemetry (sub-second) and post-processed products (minutes to hours). Each has a different transport path

### The Four Federation Planes

```
PLANE 1: CONTROL PLANE (mTLS gRPC)
  Purpose: Dispatch commands, mission management, configuration
  Transport: gRPC over mTLS (WireGuard tunnel between services)
  Auth: Keycloak JWT + DID Verifiable Credential
  Latency: <100ms
  Who uses it: All services sending dispatch requests to Fleet Ops

PLANE 2: EVENT PLANE (Kafka pub/sub)
  Purpose: Alerts, detections, status changes, telemetry
  Transport: Kafka (SASL_SSL, existing Hub infrastructure)
  Auth: Keycloak service account + Kafka ACLs
  Latency: <500ms
  Who uses it: All services (produce + consume drone events)

PLANE 3: MEDIA PLANE (RTSP/HLS over WireGuard)
  Purpose: Live video streams, thermal feeds, fused video
  Transport: RTSP (push from drone) / HLS (pull from services)
  Auth: Stream tokens (short-lived JWT, issued by Fleet Ops)
  Latency: <500ms glass-to-glass
  Who uses it: OS-SENTINEL (PTZ correlation), OS-GUARDIAN (body cam pairing)

PLANE 4: SPATIAL PLANE (OGC Standards + REST)
  Purpose: 3D models, point clouds, orthomosaics, GIS data
  Transport: OGC API - Features, OGC 3D Tiles, WMTS tiles
  Auth: OAuth2 bearer token (scoped by site geofence)
  Latency: Minutes to hours (processing pipeline) then tile-served
  Who uses it: Digital Twin, OS-PATROL (route planning), all map UIs
```

### Federation Gateway

Every cross-service request passes through a dedicated **Drone Federation Gateway** — a lightweight service that sits between Fleet Ops and the Hub, enforcing:

```
┌──────────────────────────────────────────────────────────────────────┐
│                   DRONE FEDERATION GATEWAY                           │
│                   (fleet-gw.opensecure.local)                        │
└──────────────────────────────────────────────────────────────────────┘

INBOUND (other services → OS-DRONE):
  ┌──────────────┐
  │ OS-SENTINEL  │──dispatch_request──► Kong API GW ──► /drone/v1/* ──►┐
  │ OS-PATROL    │──dispatch_request──► Kong API GW ──► /drone/v1/* ──►┤
  │ OS-PACS      │──dispatch_request──► Kong API GW ──► /drone/v1/* ──►┤
  │ OS-GUARDIAN  │──dispatch_request──► Kong API GW ──► /drone/v1/* ──►┤
  └──────────────┘                                                      │
                                                                        ▼
                                                         ┌────────────────────┐
                                                         │ Federation Gateway │
                                                         │                    │
                                                         │ • Verify JWT       │
                                                         │ • Check DID VC     │
                                                         │ • Spatial scoping  │
                                                         │ • Rate limiting    │
                                                         │ • Audit log        │
                                                         │ • Route to Fleet   │
                                                         └────────────────────┘

OUTBOUND (OS-DRONE → other services):
  Fleet Ops ──kafka_event──► Hub Kafka ──► Consumer per service
  Fleet Ops ──3D_tiles──────► Spatial API ──► /3d/v1/{site_id}/*
  Fleet Ops ──RTSP_stream───► MediaMTX proxy ──► service stream URL
```

### Spatial Scoping — The Critical Access Control Layer

Every request to OS-DRONE data is **spatially scoped**. A service can only access drone data whose geographic footprint intersects with the requesting organization's registered site boundary.

```python
# Spatial scoping middleware — runs on every request to Federation Gateway

class SpatialScopeMiddleware:

    async def check_access(
        self,
        requester_org_did: str,
        request_type: str,         # "live_video", "3d_tiles", "telemetry"
        spatial_context: GeoJSON   # What area does this request cover?
    ) -> ScopingDecision:

        # 1. Load requester org's registered site boundaries from PostGIS
        org_sites = await self.db.query("""
            SELECT site_id, ST_AsGeoJSON(boundary_geom) as boundary
            FROM organization_sites
            WHERE org_did = $1 AND active = true
        """, requester_org_did)

        # 2. Check spatial intersection
        #    Requester can only see data whose footprint overlaps THEIR sites
        authorized_area = unary_union([shape(s.boundary) for s in org_sites])
        request_area    = shape(spatial_context)

        if not authorized_area.intersects(request_area):
            return ScopingDecision.DENIED(
                reason="Requested area does not intersect any authorized site",
                authorized_area=authorized_area.wkt
            )

        # 3. Clip the authorized response to the intersection only
        #    (org can see their piece, not the neighbor's)
        clipped_area = authorized_area.intersection(request_area)

        return ScopingDecision.APPROVED(
            authorized_footprint=clipped_area,
            clip_response_to_footprint=True
        )
```

---

## Per-Service Federation Protocols

### OS-DRONE ↔ OS-SENTINEL

The tightest integration in the ecosystem. Cameras trigger drones, drones enhance cameras.

```
SENTINEL → DRONE (Camera triggers aerial response):

Kafka topic: sentinel.detection.alert
  └─► Fleet Ops MCS consumer
      ├─ Parse alert: {camera_id, detection_class, confidence, bbox, timestamp}
      ├─ Geolocate detection: camera_id + bbox → GPS coordinate (using camera 3D model)
      ├─ Select nearest available drone
      ├─ Auto-issue MissionAuthVC (autonomous dispatch, see DID/VC doc)
      └─ Dispatch: drone airborne in <90 seconds at detection GPS

gRPC call structure:
  sentinel_service → fleet_ops_service: DispatchToCameraAlert {
    camera_id:          "CAM-EAST-042",
    detection_class:    "person",
    confidence:         0.89,
    detection_bbox:     {x:120, y:340, w:80, h:210},
    camera_gps:         {lat:45.4215, lon:-75.6972, alt_m:6.0},
    camera_pitch_deg:   -30,
    priority:           HIGH,
    requesting_service: "os-sentinel",
    requester_jwt:      "eyJhbGc..."
  }

DRONE → SENTINEL (Drone positions PTZ cameras):

Kafka topic: drone.detection.confirmed
  └─► OS-SENTINEL consumer
      ├─ Parse: {drone_id, track_id, detection_gps, heading, speed}
      ├─ Find nearest PTZ camera to detection_gps
      ├─ Calculate: pan/tilt angles to point camera at detection
      └─ Command PTZ: camera auto-slews to track detected object

Kafka topic: drone.3d.update
  └─► OS-SENTINEL consumer
      ├─ New orthomosaic available for site
      ├─ Recalculate all camera FOV polygons in 3D space (using new DEM)
      └─ Update Frigate zone definitions with corrected geometry
```

### OS-DRONE ↔ OS-PATROL

Drones give patrol vehicles aerial context and optimal routing; patrol vehicles give drones ground-level corroboration.

```
PATROL → DRONE (LPR hit triggers aerial follow):

Kafka topic: patrol.lpr.hotlist_hit
  └─► Fleet Ops consumer
      ├─ Extract: {vehicle_gps, plate, direction_heading, speed_kmh}
      ├─ Project vehicle's 15-second future position
      ├─ Dispatch drone to intercept point
      └─ Drone arrives before vehicle, establishes aerial track

DRONE → PATROL (Aerial track feeds vehicle routing):

Kafka topic: drone.track.vehicle
  └─► OS-PATROL consumer
      ├─ Live vehicle position from air (GPS + bearing + speed)
      ├─ Patrol unit's navigation app receives live target waypoint
      └─ "Vehicle last seen: 45.4218°N 75.6955°W, heading NE at 45 km/h"

DRONE → PATROL (Terrain model improves routing):

OGC API:  GET /3d/v1/{site_id}/dtm.tif
  └─► OS-PATROL route planner loads DTM (Digital Terrain Model)
      ├─ Routing engine now knows actual road grades, barriers
      ├─ Patrol routes avoid flooded low spots, steep grades
      └─ Response time calculation uses real terrain, not straight-line
```

### OS-DRONE ↔ OS-PACS

Drones enforce perimeters in 3D; PACS events trigger aerial verification.

```
PACS → DRONE (Door breach or perimeter alarm triggers dispatch):

Kafka topic: pacs.alarm.perimeter_breach
  └─► Fleet Ops consumer
      ├─ Map alarm zone_id to site GPS polygon (from 3D spatial model)
      ├─ Dispatch nearest drone to breach polygon centroid
      └─ Drone arrives, thermal + EO scan, reports back

DRONE → PACS (Aerial perimeter model improves access zones):

REST: POST /pacs/v1/zones/update_geometry
  Body: {
    zone_id: "PERIMETER-NORTH",
    geometry_3d: <GeoJSON Polygon with elevation>,
    source: "lidar_scan_2026-03-04",
    confidence: 0.98
  }
  └─► OS-PACS updates its access zone map with LiDAR-accurate boundary
      ├─ Previously: manually drawn polygon (approximate)
      └─ Now: LiDAR-traced boundary accurate to ±5cm
```

### OS-DRONE ↔ OS-GUARDIAN

Body cameras gain aerial context; drones gain ground-level identity confirmation.

```
GUARDIAN → DRONE (Officer activates body cam → drone assigned overhead):

Kafka topic: guardian.bodycam.activated
  └─► Fleet Ops consumer
      ├─ Parse: {officer_did, officer_gps, incident_type}
      ├─ If incident_type in HIGH_RISK_TYPES:
      │   dispatch nearest drone as aerial overwatch
      └─ Drone loiters overhead, monitoring officer

DRONE → GUARDIAN (Drone GPS enriches body cam evidence):

Kafka topic: drone.evidence.geolocation_service
  └─► OS-GUARDIAN consumer
      ├─ For every body cam recording session:
      │   cross-reference with drone overhead position
      ├─ Attach drone position + bearing to body cam evidence record
      └─ Body cam footage now has precise aerial GPS corroboration
          (officer was at EXACTLY this location, drone confirms)

GUARDIAN → DRONE (Body cam face ID → aerial target lock):

Kafka topic: guardian.recognition.face_confirmed
  └─► Fleet Ops consumer
      ├─ Parse: {person_did OR watchlist_id, officer_gps}
      ├─ Dispatch drone: maintain aerial visual on confirmed individual
      └─ Drone uses DeepSORT track + face match to follow target
```

### OS-DRONE ↔ OS-CONCIERGE

Drones enable wayfinding in dynamic environments; visitor data enables proactive airspace clearance.

```
CONCIERGE → DRONE (VIP arrival pre-clears airspace, requests escort):

Kafka topic: concierge.visitor.vip_arrival_imminent
  └─► Fleet Ops consumer
      ├─ Pre-flight route inspection: drone checks arrival route clear
      ├─ If COVERT mode: drone stands down from arrival area
      └─ If ESCORT mode: drone loiters overhead at safe altitude

DRONE → CONCIERGE (Aerial people count informs concierge queues):

Kafka topic: drone.analytics.crowd_density
  └─► OS-CONCIERGE consumer
      ├─ Aerial head count per zone → concierge predicts wait time
      └─ "Lobby has 34 people, kiosk queue: 8 minutes. Open overflow."
```

---

## The 3D Spatial Intelligence Pipeline

### Architecture Overview

The pipeline transforms raw drone sensor data into spatial products (point clouds, models, maps, tiles) that feed the digital twin and every other service. It is entirely open-source.

```
┌──────────────────────────────────────────────────────────────────────┐
│                  3D SPATIAL INTELLIGENCE PIPELINE                    │
└──────────────────────────────────────────────────────────────────────┘

PHASE 1 — DATA ACQUISITION (on drone, in flight):
  EO Camera (Sony IMX577)
  └─► GPS-triggered photos every 2m forward / 1.5m side overlap
      Stored: NVMe on drone (JPEG + metadata EXIF)
  LiDAR (DJI L2 or Livox Mid-360)
  └─► Continuous point stream (200,000 pts/s)
      Stored: LAS binary on drone NVMe
  IMU (VectorNav VN-100, 200Hz)
  └─► Tight coupling with LiDAR/camera timestamps
  RTK GPS (u-blox F9P)
  └─► 2cm accuracy position in every photo EXIF + every LiDAR return

PHASE 2 — INGEST (on dock, post-flight):
  Drone docks → USB3 sync begins automatically
  Files transferred to: MinIO bucket
    s3://spatial-raw/{site_id}/{date}/{mission_id}/
    ├── photos/         (JPEG + XMP sidecar with GPS/attitude)
    ├── lidar/          (LAS 1.4 files, ~500MB per 20-min flight)
    └── telemetry/      (MAVLink logs, IMU, GPS)

PHASE 3 — PROCESSING (Fleet Ops GPU server):
  Job scheduler: Apache Airflow (DAG per mission type)

  PHOTOGRAMMETRY DAG:
    ingest → validate_gps → run_odm → generate_tiles → publish

  LIDAR DAG:
    ingest → classify_pdal → register_icp → merge_baseline →
    run_change_detection → generate_3dtiles → publish

  MULTISPECTRAL DAG:
    ingest → radiometric_calibration → align_bands →
    compute_ndvi → generate_geotiff → publish

PHASE 4 — PUBLISHING (Spatial API):
  Processed products served via OGC-standard APIs:
  ├── 3D Tiles 1.1:  /3d/{site_id}/tileset.json
  ├── OGC API Features: /features/{site_id}/collections/
  ├── WMTS tiles: /wmts/{site_id}/{layer}/...
  ├── COG GeoTIFF: /cog/{site_id}/ortho_latest.tif
  └── WFS (change events): /wfs/{site_id}/changes

PHASE 5 — CONSUMPTION (downstream services):
  Digital Twin → cesium.js loads 3D Tiles in browser
  OS-PATROL    → OSRM routing engine loads DTM
  OS-SENTINEL  → camera calibration tool loads point cloud
  OS-PACS      → perimeter accuracy tool loads LiDAR boundary
  External GIS → QGIS, ArcGIS connect via OGC standard endpoints
```

---

## Open-Source Toolchain: Complete Stack

### Every Tool, Its Role, and Why It Was Chosen

```
DATA ACQUISITION
  ArduPilot (autopilot firmware, Apache 2.0)
  └─► Survey mission planning: AUTO mode, camera trigger via MAVLink DO_SET_CAM_TRIGG_DIST
  Mission Planner (ground station, GPL)
  └─► Survey grid generation, waypoint upload, GCP target placement
  ROS2 Humble (robot middleware, Apache 2.0)
  └─► LiDAR driver, sensor time synchronization, bag recording

PHOTOGRAMMETRY
  OpenDroneMap / ODM (GPL 3.0)
  └─► Structure-from-Motion (SfM) + MVS = orthomosaic + point cloud + mesh + DSM/DTM
  NodeODM (MIT)
  └─► REST API wrapper for ODM — Fleet Ops submits jobs via HTTP POST
  ClusterODM (LGPL)
  └─► Distribute large ODM jobs across multiple GPU servers
  Why ODM not Pix4D/Metashape? 100% open source, on-premise, no per-flight fees

LIDAR PROCESSING
  PDAL (BSD, Point Data Abstraction Library)
  └─► Classify returns (ground/vegetation/buildings), filter noise, reproject
  LAStools (commercial for large data, but las2las/lasinfo free)
  └─► LAS/LAZ file manipulation, tiling, indexing
  LIO-SAM (BSD, LiDAR-Inertial Odometry Smoothing and Mapping)
  └─► Real-time SLAM: fuse LiDAR + IMU → georeferenced map while flying
  PCL (BSD, Point Cloud Library)
  └─► Change detection: ICP registration, nearest-neighbor difference
  Open3D (MIT)
  └─► 3D mesh reconstruction from point cloud (Poisson surface reconstruction)
  Why these? PCL + Open3D cover 95% of open-source 3D processing needs

3D TILING & SERVING
  py3dtiles (Apache 2.0)
  └─► Convert point clouds / meshes to Cesium 3D Tiles 1.1 format
  pg2b3dm (MIT)
  └─► Convert PostGIS 3D geometry to batched 3D tiles
  Potree Converter (BSD)
  └─► Convert LAZ → Potree format for web point cloud streaming
  Martin (MIT, by MapLibre)
  └─► Vector tile server from PostGIS (for 2D GIS layers)
  GeoServer (LGPL)
  └─► Full OGC stack: WMS, WFS, WMTS, WCS for raster/vector data

SPATIAL DATABASE
  PostgreSQL 15 + PostGIS 3.4 (BSD/GPL)
  └─► Primary spatial database: stores site geometries, change events, GIS layers
  TimescaleDB (Apache 2.0)
  └─► Time-series extension: drone telemetry positions, detection events
  pgRouting (GPL)
  └─► Graph routing on PostGIS: OS-PATROL route optimization on drone-mapped roads

3D VISUALIZATION (WEB)
  CesiumJS (Apache 2.0)
  └─► Primary 3D globe / scene viewer — renders 3D Tiles, terrain, vector data
  Potree (BSD)
  └─► Massive point cloud streaming in browser (handles billion-point clouds)
  MapLibre GL JS (BSD)
  └─► 2D/2.5D map base layer, vector tiles, custom styling
  deck.gl (MIT, by Uber/Foursquare)
  └─► GPU-accelerated data layers on top of map: heatmaps, arcs, scatterplots
  Three.js (MIT)
  └─► Low-level 3D rendering when Cesium is too heavy (in-building views)

PHOTOGRAMMETRY PROCESSING SERVER
  Apache Airflow (Apache 2.0)
  └─► DAG-based job scheduler: triggers ODM/PDAL jobs when new data arrives
  Celery + Redis (MIT/BSD)
  └─► Task queue: parallelizes processing across multiple GPU workers
  NVIDIA CUDA toolkit (proprietary but free)
  └─► GPU acceleration for ODM and point cloud processing

DATA PIPELINE
  Apache Kafka (Apache 2.0) — existing Hub infrastructure
  └─► All spatial events published to kafka.opensecure.drone.spatial.*
  MinIO (AGPL)
  └─► S3-compatible object store: raw photos, LAS files, processed products
  Apache Parquet + DuckDB (Apache 2.0)
  └─► Columnar storage for large telemetry analytics queries
```

---

## LiDAR Point Cloud Processing

### Complete PDAL Pipeline

```python
# PDAL pipeline configuration — Fleet Ops processing worker
# Runs automatically when new LiDAR data arrives from drone

import pdal
import json

# STAGE 1: Classify and clean raw LiDAR
classification_pipeline = {
    "pipeline": [
        {
            "type": "readers.las",
            "filename": "s3://spatial-raw/{site_id}/{date}/{mission_id}/lidar/raw.laz",
            "override_srs": "EPSG:4326"
        },
        {
            "type": "filters.reprojection",
            "out_srs": "EPSG:32618"   # UTM Zone 18N for Ontario — local metric CRS
        },
        {
            "type": "filters.smrf",   # Simple Morphological Filter — ground classification
            "scalar": 1.2,
            "slope": 0.2,
            "threshold": 0.45,
            "window": 16.0
        },
        {
            "type": "filters.hag_nn", # Height Above Ground — compute for each point
            "count": 5
        },
        {
            "type": "filters.ferry",
            "dimensions": "HeightAboveGround=>Z"  # Use HAG as Z for vegetation
        },
        {
            "type": "filters.range",  # Remove outliers
            "limits": "Z[-5:500]"
        },
        {
            "type": "filters.assign",  # Classify by HAG
            "assignment": "Classification[:]=0",
            "condition": "Z > 2.0"
        },
        {
            "type": "writers.las",
            "filename": "s3://spatial-processed/{site_id}/{date}/classified.laz",
            "compression": "laszip",
            "minor_version": 4
        }
    ]
}

# STAGE 2: Generate DTM (Digital Terrain Model) — ground only
dtm_pipeline = {
    "pipeline": [
        {
            "type": "readers.las",
            "filename": "s3://spatial-processed/{site_id}/{date}/classified.laz"
        },
        {
            "type": "filters.range",
            "limits": "Classification[2:2]"  # Ground points only
        },
        {
            "type": "writers.gdal",
            "filename": "s3://spatial-products/{site_id}/dtm_latest.tif",
            "resolution": 0.5,        # 50cm resolution
            "output_type": "mean",
            "gdalopts": "COMPRESS=DEFLATE,TILED=YES,BLOCKXSIZE=256,BLOCKYSIZE=256"
            # Cloud-Optimized GeoTIFF format — efficient streaming
        }
    ]
}

# STAGE 3: Generate DSM (Digital Surface Model) — everything including buildings/trees
dsm_pipeline = {
    "pipeline": [
        {"type": "readers.las",
         "filename": "s3://spatial-processed/{site_id}/{date}/classified.laz"},
        {"type": "filters.range", "limits": "Classification[1:31]"},  # All returns
        {"type": "writers.gdal",
         "filename": "s3://spatial-products/{site_id}/dsm_latest.tif",
         "resolution": 0.25,  # 25cm for surface model
         "output_type": "max"}  # Highest return = top of surface
    ]
}

# Execute all three stages
for pipeline_def in [classification_pipeline, dtm_pipeline, dsm_pipeline]:
    pipeline = pdal.Pipeline(json.dumps(pipeline_def))
    pipeline.execute()

print("LiDAR processing complete. DTM and DSM available in spatial-products bucket.")
```

### 3D Mesh from LiDAR (Open3D)

```python
import open3d as o3d
import numpy as np

def generate_3d_mesh_from_lidar(laz_path: str, output_path: str):
    """
    Convert classified LiDAR point cloud to watertight 3D mesh.
    Output: GLB file (web-compatible, loads in CesiumJS / Three.js)
    """

    # Load classified point cloud (building + structure points)
    pcd = o3d.io.read_point_cloud(laz_path)

    # Estimate surface normals (required for Poisson reconstruction)
    pcd.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.5, max_nn=30)
    )
    pcd.orient_normals_consistent_tangent_plane(k=15)

    # Poisson Surface Reconstruction — generates watertight mesh
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd, depth=12, width=0, scale=1.1, linear_fit=False
    )

    # Remove low-density vertices (artifacts at boundaries)
    vertices_to_remove = densities < np.quantile(densities, 0.05)
    mesh.remove_vertices_by_mask(vertices_to_remove)

    # Simplify mesh for web streaming (reduce triangle count)
    mesh = mesh.simplify_quadric_decimation(target_number_of_triangles=500_000)

    # Clean up
    mesh.remove_degenerate_triangles()
    mesh.remove_duplicated_triangles()
    mesh.compute_triangle_normals()

    # Export as GLB (embedded textures + geometry, single file)
    o3d.io.write_triangle_mesh(output_path, mesh, write_ascii=False)

    # Tile for Cesium 3D Tiles streaming
    generate_3d_tiles(output_path)

    return output_path
```

---

## Photogrammetry: Photos to 3D Models

### Automated ODM Processing via NodeODM API

```python
# Fleet Ops worker: automatically process photos into 3D products
# Triggered by Airflow DAG when new photos arrive in MinIO

import requests
import time
from minio import Minio

class ODMProcessingWorker:

    def __init__(self):
        self.nodeoдm_url = "http://odm-worker:3000"  # NodeODM container
        self.minio       = Minio("minio:9000", ...)

    def process_survey_mission(self, mission_id: str, site_id: str) -> dict:
        """
        Full photogrammetry pipeline: photos → orthomosaic + 3D model + terrain
        """

        # Step 1: List photos from MinIO
        photos = list(self.minio.list_objects(
            "spatial-raw", prefix=f"{site_id}/{mission_id}/photos/"
        ))

        # Step 2: Create NodeODM task
        task_response = requests.post(f"{self.nodeoдm_url}/task/new/init", json={
            "options": [
                {"name": "feature-quality",     "value": "ultra"},
                {"name": "pc-quality",          "value": "ultra"},
                # High quality SfM for point cloud
                {"name": "mesh-size",           "value": 300000},
                # Triangle count target
                {"name": "orthophoto-resolution","value": 2.0},
                # 2 cm/pixel ground sampling distance
                {"name": "dtm",                 "value": True},
                # Generate Digital Terrain Model
                {"name": "dsm",                 "value": True},
                # Generate Digital Surface Model
                {"name": "3d-tiles",            "value": True},
                # Output Cesium 3D Tiles directly
                {"name": "use-3dmesh",          "value": True},
                {"name": "gps-accuracy",        "value": 0.05},
                # 5cm GPS accuracy (RTK)
                {"name": "cog",                 "value": True}
                # Cloud-Optimized GeoTIFF output
            ]
        })
        task_id = task_response.json()["uuid"]

        # Step 3: Upload photos to ODM task
        for photo_obj in photos:
            photo_data = self.minio.get_object("spatial-raw", photo_obj.object_name)
            requests.post(
                f"{self.nodeoдm_url}/task/new/upload/{task_id}",
                files={"images": (photo_obj.object_name, photo_data)}
            )

        # Step 4: Commit task (start processing)
        requests.post(f"{self.nodeoдm_url}/task/new/commit/{task_id}")

        # Step 5: Poll for completion
        while True:
            status = requests.get(f"{self.nodeoдm_url}/task/{task_id}/info").json()
            if status["status"]["code"] == 40:   # COMPLETED
                break
            elif status["status"]["code"] == 30: # FAILED
                raise RuntimeError(f"ODM processing failed: {status}")
            time.sleep(30)

        # Step 6: Download and store products
        products = {
            "orthophoto":   f"{self.nodeoдm_url}/task/{task_id}/download/orthophoto.tif",
            "dsm":          f"{self.nodeoдm_url}/task/{task_id}/download/dsm.tif",
            "dtm":          f"{self.nodeoдm_url}/task/{task_id}/download/dtm.tif",
            "pointcloud":   f"{self.nodeoдm_url}/task/{task_id}/download/georeferenced_model.laz",
            "3d_tiles":     f"{self.nodeoдm_url}/task/{task_id}/download/3d_tiles.zip",
            "report":       f"{self.nodeoдm_url}/task/{task_id}/download/report.pdf"
        }

        for product_name, url in products.items():
            product_bytes = requests.get(url).content
            self.minio.put_object(
                "spatial-products",
                f"{site_id}/latest/{product_name}",
                product_bytes
            )

        # Step 7: Publish spatial update event to Kafka
        self.kafka.produce("drone.spatial.update", {
            "event":    "photogrammetry_complete",
            "site_id":  site_id,
            "mission_id": mission_id,
            "products": list(products.keys()),
            "gsd_cm":   2.0,
            "area_m2":  self.compute_area(site_id),
            "timestamp": utcnow()
        })

        return {"status": "complete", "products": products}
```

### ODM Output Products

```
FROM A SINGLE SURVEY FLIGHT (30 min, ~800 photos, 50-acre site):

orthophoto.tif        — Georeferenced aerial photo mosaic (2cm/pixel, COG format)
dsm.tif               — Digital Surface Model (includes buildings, trees)
dtm.tif               — Digital Terrain Model (bare earth only)
georeferenced_model.laz — Dense 3D point cloud (60-200 million points)
odm_mesh/             — Textured 3D mesh (OBJ + MTL + JPG textures)
3d_tiles/             — Cesium 3D Tiles (ready to load in browser)
report.pdf            — Processing quality report (reprojection error, GCPs)

DERIVED PRODUCTS (generated post-ODM):
contours.geojson      — 1m elevation contours (GDAL)
hillshade.tif         — Shaded relief model (atmospheric lighting)
slope.tif             — Slope angle raster (GDAL DEM tools)
aspect.tif            — Aspect direction raster
ndvi.tif              — Vegetation index (if multispectral equipped)
change_detection.geojson — Objects that appeared/changed since last flight
```

---

## Living Digital Twin Integration

### How Drone Data Becomes the Digital Twin Base Map

The OpenSecure Digital Twin already exists (see `OpenSecure_Digital_Twin_Integration.md`). OS-DRONE upgrades it from a static model to a **continuously updated spatial reality**.

```
BEFORE OS-DRONE:
  Digital Twin base map:
  ├── CAD import (from architect drawings, years old)
  ├── Manual photogrammetry (done once at deployment, never updated)
  └── OpenStreetMap (street-level only, no detail)
  Problem: model diverges from reality every time something changes

WITH OS-DRONE:
  Digital Twin base map:
  ├── Weekly: full-site orthomosaic survey (2cm/pixel)
  ├── After incidents: targeted rescan of affected area
  ├── Nightly: LiDAR change detection scan (automated, 20 min)
  └── Real-time: drone live position + FOV shown in twin
  Result: twin stays accurate to within 1 week of ground truth
```

### Cesium-Based Digital Twin Spatial Stack

```javascript
// Fleet Ops Digital Twin — Cesium.js integration
// Loads all drone-generated 3D products into the scene

import * as Cesium from "cesium";

class DroneDigitalTwin {

    constructor(cesiumViewer) {
        this.viewer  = cesiumViewer;
        this.site_id = getCurrentSiteId();
        this.layers  = {};
    }

    async loadAllSpatialLayers() {

        // 1. TERRAIN: Use drone-generated DTM as terrain provider
        //    (replaces Cesium World Terrain — now we have 2cm accuracy for our site)
        const terrain = await Cesium.CesiumTerrainProvider.fromUrl(
            `/terrain/${this.site_id}/layer.json`
            // Generated by rio-cogeo + Cesium terrain tile format conversion
        );
        this.viewer.terrainProvider = terrain;

        // 2. ORTHOMOSAIC: Latest drone orthophoto as imagery layer
        this.layers.ortho = this.viewer.imageryLayers.addImageryProvider(
            new Cesium.WebMapTileServiceImageryProvider({
                url:    `/wmts/${this.site_id}/ortho/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png`,
                layer:  "orthophoto_latest",
                style:  "default",
                format: "image/webp",   // WebP for bandwidth efficiency
                tileMatrixSetID: "GoogleMapsCompatible"
            })
        );

        // 3. 3D POINT CLOUD: LiDAR scan as Cesium 3D Tiles
        this.layers.pointcloud = await Cesium.Cesium3DTileset.fromUrl(
            `/3d/${this.site_id}/pointcloud/tileset.json`, {
                maximumScreenSpaceError: 4,    // LOD quality
                pointCloudShading: {
                    attenuation: true,
                    maximumAttenuation: 4,
                    geometricErrorScale: 0.5
                }
            }
        );
        this.viewer.scene.primitives.add(this.layers.pointcloud);

        // 4. 3D BUILDINGS: ODM textured mesh as 3D Tiles
        this.layers.buildings = await Cesium.Cesium3DTileset.fromUrl(
            `/3d/${this.site_id}/buildings/tileset.json`, {
                maximumScreenSpaceError: 8
            }
        );
        this.viewer.scene.primitives.add(this.layers.buildings);

        // 5. CHANGE DETECTION OVERLAY: flag changed areas since last scan
        this.layers.changes = new Cesium.GeoJsonDataSource();
        await this.layers.changes.load(
            `/features/${this.site_id}/collections/changes/items?limit=100`
        );
        this.viewer.dataSources.add(this.layers.changes);

        // 6. LIVE DRONE POSITIONS: WebSocket feed of all active drones
        this.subscribeDroneTelemetry();

        // 7. ALL OTHER SERVICES: overlay on 3D terrain
        this.loadSentinelCameraFOVs();   // OS-SENTINEL camera cones in 3D
        this.loadPatrolVehicles();        // OS-PATROL real-time vehicles
        this.loadGuardianOfficers();      // OS-GUARDIAN officer positions
        this.loadPACSZones();             // OS-PACS access zones in 3D
    }

    subscribeDroneTelemetry() {
        const ws = new WebSocket(`wss://fleet.opensecure.local/ws/telemetry`);
        ws.onmessage = (event) => {
            const { drone_id, lat, lon, alt, heading, battery } = JSON.parse(event.data);
            this.updateDronePosition(drone_id, lat, lon, alt, heading);
        };
    }

    loadSentinelCameraFOVs() {
        // Each camera's field of view is a 3D frustum projected onto the terrain
        // Uses: camera GPS position + orientation + FOV angle + ODM terrain model
        // Result: exact coverage polygon on ground (accounts for terrain elevation)
        fetch(`/sentinel/v1/cameras/${this.site_id}/fov_3d`)
            .then(r => r.json())
            .then(cameras => {
                cameras.forEach(cam => {
                    const fov = this.compute3DFOV(
                        cam.position, cam.orientation,
                        cam.fov_horizontal, cam.fov_vertical,
                        this.viewer.terrainProvider   // Uses drone DTM
                    );
                    this.viewer.entities.add({
                        id: `camera-fov-${cam.id}`,
                        polygon: {
                            hierarchy: Cesium.Cartesian3.fromDegreesArrayHeights(fov),
                            material: Cesium.Color.CYAN.withAlpha(0.15),
                            outline: true,
                            outlineColor: Cesium.Color.CYAN
                        }
                    });
                });
            });
    }
}
```

---

## 3D Change Detection & Anomaly System

### Nightly Automated Change Detection Workflow

```python
# Airflow DAG: nightly_change_detection
# Runs every night at 02:00 local time
# Compares today's LiDAR scan to rolling baseline

from airflow import DAG
from airflow.operators.python import PythonOperator
import numpy as np
import open3d as o3d
from sklearn.cluster import DBSCAN

def run_change_detection(site_id: str, today_scan: str, baseline_scan: str):
    """
    Compare today's classified LiDAR to the rolling 7-day baseline.
    Returns: GeoJSON FeatureCollection of significant changes.
    """

    # Load both scans (ground-classified points only for terrain changes)
    baseline = o3d.io.read_point_cloud(baseline_scan)
    today    = o3d.io.read_point_cloud(today_scan)

    # Register scans (align them precisely using ICP)
    # Even with RTK GPS, slight drift exists — ICP corrects it
    threshold = 0.10  # 10cm max correspondence distance
    reg_result = o3d.pipelines.registration.registration_icp(
        today, baseline, threshold,
        estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPoint()
    )
    today_aligned = today.transform(reg_result.transformation)

    # Compute per-point change magnitude
    today_tree = o3d.geometry.KDTreeFlann(baseline)
    changes    = []

    for point in np.asarray(today_aligned.points):
        [k, idx, dist] = today_tree.search_knn_vector_3d(point, 1)
        nearest_dist = np.sqrt(dist[0])
        if nearest_dist > 0.30:   # 30cm threshold = significant change
            changes.append({
                "point":    point.tolist(),
                "distance": float(nearest_dist)
            })

    if not changes:
        return {"site_id": site_id, "changes": [], "timestamp": utcnow()}

    # Cluster changed points into discrete objects
    change_points = np.array([c["point"] for c in changes])
    clustering = DBSCAN(eps=1.0, min_samples=20).fit(change_points)

    features = []
    for label in set(clustering.labels_):
        if label == -1:  # Noise
            continue

        cluster_points = change_points[clustering.labels_ == label]
        centroid   = cluster_points.mean(axis=0)
        bbox_dims  = cluster_points.max(axis=0) - cluster_points.min(axis=0)
        volume_m3  = float(bbox_dims[0] * bbox_dims[1] * bbox_dims[2])

        # Convert UTM centroid to WGS84 GPS
        centroid_gps = utm_to_wgs84(centroid[0], centroid[1])

        # Classify change type using spatial context
        change_class = classify_change(
            bbox_dims, volume_m3,
            context=lookup_zone(centroid_gps)  # What zone is this in?
        )

        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [centroid_gps.lon, centroid_gps.lat, float(centroid[2])]
            },
            "properties": {
                "change_class":  change_class,  # "vehicle", "debris", "construction", "person"
                "volume_m3":     round(volume_m3, 2),
                "footprint_m2":  round(bbox_dims[0] * bbox_dims[1], 2),
                "severity":      "HIGH" if volume_m3 > 2.0 else "MEDIUM",
                "site_id":       site_id,
                "detected_at":   utcnow()
            }
        })

    result = {"type": "FeatureCollection", "features": features}

    # Write to PostGIS for spatial querying
    save_to_postgis(result, table="spatial_changes", site_id=site_id)

    # Publish to Kafka — all services react to changes
    kafka.produce("drone.spatial.change_detected", {
        "site_id":      site_id,
        "change_count": len(features),
        "high_severity": sum(1 for f in features if f["properties"]["severity"] == "HIGH"),
        "geojson":       result
    })

    return result
```

---

## GIS Integration & Spatial Databases

### PostGIS Schema for Spatial Intelligence

```sql
-- Core spatial schema for OS-DRONE intelligence layer
-- PostGIS 3.4 + TimescaleDB

-- Site boundaries (authoritative perimeters for spatial scoping)
CREATE TABLE organization_sites (
    site_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_did        TEXT NOT NULL,                       -- DID of owning org
    name           TEXT NOT NULL,
    boundary_geom  GEOMETRY(Polygon, 4326) NOT NULL,   -- WGS84 polygon
    altitude_min_m FLOAT DEFAULT 0,
    altitude_max_m FLOAT DEFAULT 400,
    created_at     TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX ON organization_sites USING GIST (boundary_geom);

-- Spatial products (maps, models, point clouds)
CREATE TABLE spatial_products (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    site_id        UUID REFERENCES organization_sites,
    mission_id     TEXT NOT NULL,
    product_type   TEXT NOT NULL,  -- 'orthophoto', 'dtm', 'dsm', 'pointcloud', '3dtiles'
    minio_uri      TEXT NOT NULL,
    resolution_cm  FLOAT,
    gsd_cm         FLOAT,
    point_density  FLOAT,          -- points/m² for LiDAR
    coverage_geom  GEOMETRY(Polygon, 4326),
    produced_at    TIMESTAMPTZ DEFAULT NOW(),
    valid_until    TIMESTAMPTZ DEFAULT NOW() + INTERVAL '30 days'
);
CREATE INDEX ON spatial_products USING GIST (coverage_geom);
CREATE INDEX ON spatial_products (site_id, product_type, produced_at DESC);

-- Change detection results (PostGIS queryable)
CREATE TABLE spatial_changes (
    id             BIGSERIAL,
    site_id        UUID REFERENCES organization_sites,
    change_class   TEXT NOT NULL,  -- 'vehicle', 'debris', 'construction', 'vegetation'
    location_geom  GEOMETRY(PointZ, 4326) NOT NULL,    -- 3D point
    footprint_geom GEOMETRY(Polygon, 4326),             -- Ground footprint
    volume_m3      FLOAT,
    severity       TEXT CHECK (severity IN ('LOW','MEDIUM','HIGH','CRITICAL')),
    detected_at    TIMESTAMPTZ NOT NULL,
    resolved_at    TIMESTAMPTZ,                         -- When change disappeared
    mission_id     TEXT
);
SELECT create_hypertable('spatial_changes', 'detected_at');  -- TimescaleDB
CREATE INDEX ON spatial_changes USING GIST (location_geom);

-- Drone detections with full 3D geolocation
CREATE TABLE drone_detections_3d (
    id             BIGSERIAL,
    drone_id       TEXT NOT NULL,
    mission_id     TEXT NOT NULL,
    track_id       INTEGER,                             -- DeepSORT persistent ID
    detection_class TEXT NOT NULL,                     -- 'person', 'vehicle', etc.
    confidence     FLOAT,
    location_geom  GEOMETRY(PointZ, 4326) NOT NULL,   -- GPS-computed location
    location_accuracy_m FLOAT,
    altitude_agl_m FLOAT,                              -- Drone altitude when detected
    sensor_mode    TEXT,
    detected_at    TIMESTAMPTZ NOT NULL
);
SELECT create_hypertable('drone_detections_3d', 'detected_at');
CREATE INDEX ON drone_detections_3d USING GIST (location_geom);
CREATE INDEX ON drone_detections_3d (track_id, detected_at);

-- Track history: full trajectory of every detected object
CREATE TABLE object_tracks (
    id             BIGSERIAL,
    track_id       INTEGER NOT NULL,
    drone_id       TEXT NOT NULL,
    position_geom  GEOMETRY(PointZ, 4326) NOT NULL,
    speed_ms       FLOAT,
    heading_deg    FLOAT,
    tracked_at     TIMESTAMPTZ NOT NULL
);
SELECT create_hypertable('object_tracks', 'tracked_at');
CREATE INDEX ON object_tracks USING GIST (position_geom);
```

### Spatial Query Examples

```sql
-- "How many people were detected in the north parking lot today?"
SELECT COUNT(DISTINCT track_id)
FROM drone_detections_3d d
JOIN organization_sites s ON s.site_id = 'north-lot-uuid'
WHERE d.detection_class = 'person'
  AND ST_Within(d.location_geom::geometry, s.boundary_geom)
  AND d.detected_at >= NOW() - INTERVAL '24 hours';

-- "What changed in the southeast quadrant since last week?"
SELECT change_class, ST_AsGeoJSON(footprint_geom), volume_m3, detected_at
FROM spatial_changes
WHERE ST_Intersects(
    footprint_geom,
    ST_MakeEnvelope(-75.69, 45.42, -75.68, 45.43, 4326)  -- SE quadrant bbox
  )
  AND detected_at >= NOW() - INTERVAL '7 days'
ORDER BY severity DESC, detected_at DESC;

-- "Show the full track of vehicle TRK-0017 from this afternoon"
SELECT ST_MakeLine(position_geom::geometry ORDER BY tracked_at) as trajectory,
       MIN(tracked_at) as first_seen, MAX(tracked_at) as last_seen,
       ST_Length(ST_MakeLine(position_geom::geometry ORDER BY tracked_at)::geography) as distance_m
FROM object_tracks
WHERE track_id = 17
  AND tracked_at BETWEEN '2026-03-04 13:00' AND '2026-03-04 18:00';
```

---

## Kafka Topic Map: Spatial Events

All spatial intelligence data flows through Kafka, making it available to every consuming service in real time.

```
DRONE SPATIAL KAFKA TOPICS
──────────────────────────────────────────────────────────────────────

drone.spatial.update
  Trigger: New spatial product available (orthomosaic, DTM, point cloud)
  Consumers: Digital Twin, OS-SENTINEL (camera calibration), OS-PATROL (routing)
  Payload: {site_id, product_type, minio_uri, coverage_geojson, resolution_cm}

drone.spatial.change_detected
  Trigger: Nightly change detection finds significant differences
  Consumers: OS-PACS (perimeter integrity), OS-PATROL (route update), Digital Twin
  Payload: {site_id, change_count, high_severity_count, geojson_featurecollection}

drone.detection.geolocated
  Trigger: Every AI detection with GPS coordinates computed
  Consumers: All services, Digital Twin, OS-PATROL (dispatch)
  Payload: {drone_id, track_id, class, confidence, gps_lat, gps_lon, gps_alt, timestamp}

drone.track.update
  Trigger: Every 1-second position update for each tracked object
  Consumers: OS-PATROL (vehicle follow), OS-GUARDIAN (officer awareness), Digital Twin
  Payload: {track_id, drone_id, gps_lat, gps_lon, speed_ms, heading_deg, timestamp}

drone.telemetry.position
  Trigger: 5Hz drone position update (while airborne)
  Consumers: Digital Twin (live map), UTM traffic manager, Air Traffic awareness
  Payload: {drone_id, lat, lon, alt_agl, alt_msl, heading, speed, battery}

drone.survey.complete
  Trigger: Survey mission fully processed and products available
  Consumers: All services
  Payload: {site_id, mission_id, products[], area_m2, gsd_cm, processing_time_s}

drone.3d.tile_ready
  Trigger: New 3D tiles published for a site
  Consumers: Digital Twin (reload scene), any 3D viewer
  Payload: {site_id, tileset_url, product_type, timestamp}
```

---

## Docker Compose: Full Deployment

### Complete Spatial Intelligence Stack

```yaml
# docker-compose.spatial.yml
# Extends the base Fleet Ops compose with the full spatial intelligence stack

version: "3.9"

services:

  # ─── PHOTOGRAMMETRY ENGINE ──────────────────────────────────────────

  odm-worker:
    image: opendronemap/nodeodm:latest
    container_name: odm-worker
    ports:
      - "3000:3000"
    volumes:
      - odm_data:/var/www/data
    environment:
      - NODE_TLS_REJECT_UNAUTHORIZED=0
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]   # GPU acceleration for ODM
    restart: unless-stopped

  clusterodm:
    image: opendronemap/clusterodm:latest
    container_name: clusterodm
    ports:
      - "3001:3000"
    depends_on:
      - odm-worker
    command: ["--token", "${CLUSTER_TOKEN}"]
    restart: unless-stopped

  # ─── JOB SCHEDULER ──────────────────────────────────────────────────

  airflow-webserver:
    image: apache/airflow:2.8.1
    container_name: airflow-webserver
    ports:
      - "8080:8080"
    environment:
      - AIRFLOW__CORE__EXECUTOR=CeleryExecutor
      - AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:${AIRFLOW_PASS}@postgres:5432/airflow
      - AIRFLOW__CELERY__BROKER_URL=redis://redis:6379/1
      - AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:${AIRFLOW_PASS}@postgres:5432/airflow
    volumes:
      - ./dags:/opt/airflow/dags            # Survey processing DAGs
      - ./plugins:/opt/airflow/plugins
    depends_on:
      - postgres
      - redis
    command: webserver
    restart: unless-stopped

  airflow-worker:
    image: apache/airflow:2.8.1
    container_name: airflow-worker
    environment:
      - AIRFLOW__CORE__EXECUTOR=CeleryExecutor
      - AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:${AIRFLOW_PASS}@postgres:5432/airflow
      - AIRFLOW__CELERY__BROKER_URL=redis://redis:6379/1
    volumes:
      - ./dags:/opt/airflow/dags
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    command: celery worker
    restart: unless-stopped

  # ─── SPATIAL DATABASE ────────────────────────────────────────────────

  postgis:
    image: postgis/postgis:16-3.4
    container_name: postgis
    environment:
      - POSTGRES_USER=spatial
      - POSTGRES_PASSWORD=${POSTGIS_PASS}
      - POSTGRES_DB=spatial
    volumes:
      - postgis_data:/var/lib/postgresql/data
      - ./sql/spatial_schema.sql:/docker-entrypoint-initdb.d/01-schema.sql
    ports:
      - "5433:5432"   # Separate port from main Fleet Ops postgres
    restart: unless-stopped

  # ─── SPATIAL API SERVERS ─────────────────────────────────────────────

  geoserver:
    image: docker.osgeo.org/geoserver:2.24.1
    container_name: geoserver
    ports:
      - "8600:8080"
    volumes:
      - geoserver_data:/opt/geoserver/data_dir
    environment:
      - JAVA_OPTS=-Xms512m -Xmx2048m
    restart: unless-stopped
    # Serves: WMS, WMTS, WFS, WCS for all raster/vector layers

  martin:
    image: ghcr.io/maplibre/martin:latest
    container_name: martin
    ports:
      - "3003:3000"
    environment:
      - DATABASE_URL=postgresql://spatial:${POSTGIS_PASS}@postgis:5432/spatial
    command: ["--listen-addresses", "0.0.0.0:3000"]
    depends_on:
      - postgis
    restart: unless-stopped
    # Serves: Vector MVT tiles directly from PostGIS

  # ─── 3D TILE SERVER ───────────────────────────────────────────────────

  3dtiles-server:
    image: ghcr.io/cogeo/titiler:latest
    container_name: 3dtiles-server
    ports:
      - "8008:8888"
    environment:
      - AWS_ACCESS_KEY_ID=${MINIO_ACCESS_KEY}
      - AWS_SECRET_ACCESS_KEY=${MINIO_SECRET_KEY}
      - AWS_ENDPOINT_URL=http://minio:9000
      - AWS_S3_FORCE_PATH_STYLE=true
    restart: unless-stopped
    # Serves Cloud-Optimized GeoTIFFs from MinIO as web map tiles

  potree-server:
    image: nginx:alpine
    container_name: potree-server
    ports:
      - "8009:80"
    volumes:
      - potree_data:/usr/share/nginx/html/pointclouds:ro
      - ./nginx/potree.conf:/etc/nginx/conf.d/default.conf
    restart: unless-stopped
    # Serves Potree point cloud tiles for browser viewer

  # ─── SPATIAL WORKER (PDAL + Open3D processing) ───────────────────────

  spatial-worker:
    build:
      context: ./spatial-worker
      dockerfile: Dockerfile
      # Base: ubuntu:22.04 + PDAL + Open3D + GDAL + PyProj + Shapely
    container_name: spatial-worker
    environment:
      - MINIO_URL=http://minio:9000
      - MINIO_ACCESS_KEY=${MINIO_ACCESS_KEY}
      - MINIO_SECRET_KEY=${MINIO_SECRET_KEY}
      - POSTGIS_URL=postgresql://spatial:${POSTGIS_PASS}@postgis:5432/spatial
      - KAFKA_BROKER=kafka:9092
    volumes:
      - ./workers/spatial:/app
      - /tmp/spatial_scratch:/tmp/scratch   # Scratch space for large files
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: unless-stopped

volumes:
  odm_data:
  postgis_data:
  geoserver_data:
  potree_data:

networks:
  default:
    name: opensecure_network
    external: true   # Joins existing Fleet Ops network
```

### Hardware Sizing for Spatial Processing

```
MINIMUM (small site, 1-5 drones, <50 acres):
  Processing server: 1× NVIDIA RTX 4070 (12GB VRAM)
                     32GB RAM, 2TB NVMe SSD
  ODM processing time: ~20 min per 100-photo mission
  Storage: ~500GB/year (raw + products)

RECOMMENDED (medium site, 5-20 drones, 50-500 acres):
  Processing server: 2× NVIDIA RTX 4090 (24GB VRAM each)
                     128GB RAM, 8TB NVMe RAID
  ODM processing time: ~45 min per 500-photo mission
  Storage: ~5TB/year

LARGE SCALE (20+ drones, 500+ acres, multi-site):
  Processing cluster: 4× A100 80GB (or 2× H100)
                      256GB RAM, 32TB NVMe
  ClusterODM: distribute across nodes
  Storage: S3-compatible (MinIO cluster, 50TB+)
  Processing time: 30 min even for 2000-photo missions
```

---

*Document Version*: 1.0 | *Platform*: OS-DRONE v1.0
*Standards*: OGC 3D Tiles 1.1, OGC API Features, COG GeoTIFF, LAS 1.4
*Companion Documents*: OS-DRONE_Technical_Architecture.md,
OpenSecure_Digital_Twin_Integration.md, OS-DRONE_Advanced_Visual_Intelligence.md
