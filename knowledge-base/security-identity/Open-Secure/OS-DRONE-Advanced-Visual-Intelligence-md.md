---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: ee787db4-d5b0-4111-859a-9d68945c413f
original_filename: OS-DRONE_Advanced_Visual_Intelligence.md
created_at: 2026-03-05T00:33:47.287133+00:00
content_hash: 3f7dfdb02d0b
---

# OS-DRONE Advanced Visual Intelligence System
## Full-Spectrum Imaging, Sensor Fusion, Night Vision, AR Overlay & Surveying

**Document Type**: Advanced Capabilities Specification
**Version**: 1.0
**Date**: March 2026
**Classification**: Technical Documentation
**Audience**: System Architects, UAS Engineers, Computer Vision Engineers, Operations Leads

---

## Table of Contents

1. [Design Philosophy: The Intelligent Payload Bus](#design-philosophy-the-intelligent-payload-bus)
2. [Full-Spectrum Imaging Stack](#full-spectrum-imaging-stack)
3. [Advanced Night Vision & Fusion](#advanced-night-vision--fusion)
4. [Sensor Fusion Engine](#sensor-fusion-engine)
5. [Augmented Reality (AR) Overlay System](#augmented-reality-ar-overlay-system)
6. [LiDAR & 3D Mapping](#lidar--3d-mapping)
7. [Multispectral & Hyperspectral](#multispectral--hyperspectral)
8. [Surveying & Photogrammetry Engine](#surveying--photogrammetry-engine)
9. [Payload Configuration Profiles](#payload-configuration-profiles)
10. [On-Board Processing Architecture](#on-board-processing-architecture)
11. [Fleet Ops Visual Intelligence Dashboard](#fleet-ops-visual-intelligence-dashboard)
12. [Integration with OpenSecure Ecosystem](#integration-with-opensecure-ecosystem)
13. [Hardware BOM by Capability Tier](#hardware-bom-by-capability-tier)

---

## Design Philosophy: The Intelligent Payload Bus

The most intelligent architecture for drone visual capabilities is **not** to bolt on individual sensors — it is to build a **modular payload bus** that treats every sensor as a hot-swappable data source feeding a single **unified sensor fusion engine** running on the Jetson Orin NX.

Think of it like this: every sensor produces a stream of raw data. The Jetson is the brain that fuses all those streams into a single **unified situational picture** — enriched with AI, georeferenced on a live map, and streamed to operators with AR overlays on top.

```
┌──────────────────────────────────────────────────────────────────┐
│              THE OS-DRONE INTELLIGENT PAYLOAD BUS                │
└──────────────────────────────────────────────────────────────────┘

┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│ EO/RGB  │  │Thermal  │  │  SWIR   │  │  LiDAR  │  │ Hyper-  │
│  4K     │  │  FLIR   │  │  cam    │  │  360°   │  │spectral │
│  60fps  │  │ Boson   │  │         │  │         │  │         │
└────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘
     │             │             │             │             │
     └─────────────┴─────────────┴─────────────┴─────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  SENSOR FUSION ENGINE   │
                    │  (NVIDIA Jetson Orin NX)│
                    │                         │
                    │  • Pixel-level fusion   │
                    │  • AI inference         │
                    │  • Geolocation          │
                    │  • AR rendering         │
                    │  • Evidence recording   │
                    └────────────┬────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
    ┌─────────▼──────┐  ┌────────▼───────┐  ┌──────▼───────┐
    │  AR Overlay    │  │  Live Stream   │  │  3D Survey   │
    │  (operator HUD)│  │  (Fleet Ops)   │  │  (point cloud│
    └────────────────┘  └────────────────┘  └──────────────┘
```

**Core principle**: One Jetson. One fusion pipeline. Many sensors. The operator always sees a **single enhanced view** — not four separate windows.

---

## Full-Spectrum Imaging Stack

### The Electromagnetic Spectrum — What Each Band Reveals

```
WAVELENGTH   BAND          SENSOR              WHAT YOU SEE
──────────────────────────────────────────────────────────────────
350–700 nm   Visible (EO)  Sony IMX577 4K      Normal colour video
700–1000 nm  Near-IR (NIR) Modified EO +       Vegetation health,
                           NIR filter          concealed suspects
                                               in foliage, fake ID
1000–1700 nm SWIR          Sensors Unlimited   See through smoke,
                           640C (InGaAs)       haze, glass, thin
                                               plastics, wet surfaces
3–5 μm       Mid-IR (MWIR) FLIR Neutrino LC    High-contrast heat —
                           (cooled MCT)        best for vehicles,
                                               engine heat, weapons
8–14 μm      Long-IR (LWIR)FLIR Boson 640+     Human body heat,
                           (uncooled VOx)      warm ground, heat
                                               footprints on pavement
1–100 GHz    Radar / SAR   Echodyne EchoGuard  See through walls,
                                               foliage, in the rain
```

### Recommended Sensor Stack Per Use Case

```
TIER 1 — STANDARD SECURITY (most deployments)
├── EO: Sony IMX577 4K (main camera, 3-axis gimbal)
└── LWIR: FLIR Boson 640+ (thermal, co-boresighted)
    Cost premium: +$4,000 | Weight: +320g | Use: Night patrol, people detection

TIER 2 — ADVANCED SECURITY (high-value sites, law enforcement)
├── EO: Sony IMX577 4K + 30× optical zoom
├── LWIR: FLIR Boson 640+ (thermal)
└── SWIR: Sensors Unlimited 640C (see through smoke/glass)
    Cost premium: +$18,000 | Weight: +600g | Use: Industrial fires, pursuits

TIER 3 — INTELLIGENCE / CRITICAL INFRASTRUCTURE
├── EO: Sony IMX577 4K
├── MWIR: FLIR Neutrino LC (cooled, high sensitivity)
├── SWIR: Sensors Unlimited 640C
└── Radar: Echodyne EchoGuard (see through walls and rain)
    Cost premium: +$60,000 | Weight: +1.2 kg | Use: Nuclear, military, CBRN

TIER 4 — SURVEY / INSPECTION / AGRICULTURE
├── EO: Sony IMX577 4K
├── LWIR: FLIR Boson 640+
├── Multispectral: MicaSense RedEdge-P (5-band)
└── LiDAR: DJI Zenmuse L2 (240,000 pts/s)
    Cost premium: +$22,000 | Weight: +850g | Use: Mapping, crop health, inspection
```

---

## Advanced Night Vision & Fusion

### The Problem with Simple Night Vision

Standard night vision (image intensification) is a single approach — it amplifies available light. This fails in complete darkness, in smoke, or when subjects are camouflaged against the environment. The intelligent solution is **multi-mode night vision with AI-driven fusion**.

### Mode 1: Low-Light EO (Starlight Camera)

```
Hardware: Sony IMX585 Starvis 2 (or Sony IMX492)
├── Sensitivity: 0.0001 lux (true starlight performance)
├── Resolution: 4K
├── Frame rate: 60fps full res, 120fps @ 1080p
├── Technology: Back-illuminated CMOS (BSI), large pixels (2.9μm)
└── Result: Usable colour video in near-zero ambient light

Deployment: Replace standard IMX577 with IMX585 for night-primary sites
Software: GStreamer ISP pipeline tuned for low-light
          (gain: adaptive, noise reduction: temporal NR enabled)
```

### Mode 2: Thermal LWIR (Primary Night Mode)

```
Hardware: FLIR Boson 640+ (uncooled, VOx microbolometer)
├── Resolution: 640×512
├── Sensitivity: <35mK NETD (detects 0.035°C temperature difference)
├── Spectral band: 8–14 μm
├── Frame rate: 60Hz (NTSC) or 50Hz (PAL)
├── FOV: 18° × 14° (standard) — matches EO camera FOV for fusion
├── Interface: USB3 / MIPI (direct to Jetson)
└── Cost: ~$4,000

What you gain at night:
├── Person standing on warm asphalt: clearly visible
├── Vehicle driven recently: engine glows, exhaust trail visible
├── Footprints on cool pavement: visible for 5-10 minutes
├── Subject hidden in bushes: body heat visible through foliage
└── Downed/injured person: visible even if unconscious and motionless
```

### Mode 3: SWIR (Smoke & Glass Penetration)

```
Hardware: Sensors Unlimited 640CSX (InGaAs, cooled)
├── Spectral band: 0.9–1.7 μm (near/short-wave infrared)
├── Resolution: 640×512
├── Key property: Active illumination with 940nm laser illuminator
└── Cost: ~$14,000

When SWIR beats everything else:
├── Smoke: SWIR wavelengths penetrate smoke that blocks visible and thermal
├── Glass: See THROUGH tinted windows into vehicles
├── Haze / fog: Much better contrast than EO in foggy conditions
├── Wet surfaces: Wet ground absorbs SWIR → dry paths visible
└── Silicon detection: Counterfeit materials, circuit boards visible
```

### Mode 4: Sensor Fusion Night Vision (The Intelligent Approach)

This is the key insight. No single sensor is best in all conditions. The fusion engine selects and blends the best channels dynamically:

```python
# OS-DRONE Fusion Engine — Night Vision Pipeline
# Running on Jetson Orin NX (CUDA)

class NightVisionFusionEngine:

    def fuse(self, eo_frame, lwir_frame, swir_frame=None, conditions=None):
        """
        Intelligently fuse available sensor channels.
        Output: single enhanced frame for streaming + recording.
        """

        # Step 1: Geometric alignment (all sensors pre-calibrated)
        eo_aligned    = self.warp(eo_frame, self.eo_to_ref_homography)
        lwir_aligned  = self.warp(lwir_frame, self.lwir_to_ref_homography)
        lwir_upscaled = cv2.resize(lwir_aligned, eo_aligned.shape[:2][::-1],
                                   interpolation=cv2.INTER_CUBIC)

        # Step 2: Select fusion mode based on conditions
        mode = self.select_mode(conditions, eo_aligned, lwir_upscaled)

        if mode == "THERMAL_ONLY":
            # Complete darkness: thermal is sole source
            output = self.colorize_thermal(lwir_upscaled, palette="iron")

        elif mode == "FUSION_EQUAL":
            # Twilight: equal weight, laplacian pyramid blend
            output = self.pyramid_blend(eo_aligned, lwir_upscaled, alpha=0.5)

        elif mode == "FUSION_THERMAL_DOMINANT":
            # Low light, strong thermal signal
            # Keep EO for colour/texture, overlay thermal heat in orange/red
            output = self.guided_filter_fusion(eo_aligned, lwir_upscaled,
                                               thermal_weight=0.7)

        elif mode == "EO_DOMINANT":
            # Daytime / well-lit: EO primary, thermal as AI aid only
            output = eo_aligned  # Thermal used by AI, not composited

        elif mode == "SWIR_PENETRATION":
            # Smoke/fire/fog: SWIR penetrates obscurants
            swir_aligned = self.warp(swir_frame, self.swir_to_ref_homography)
            output = self.pyramid_blend(swir_aligned, lwir_upscaled, alpha=0.6)

        # Step 3: AI detection on fused frame
        detections = self.yolo_inference(output)

        # Step 4: AR overlay (see AR section)
        output_with_ar = self.ar_overlay(output, detections)

        return output_with_ar

    def select_mode(self, conditions, eo_frame, lwir_frame):
        lux   = conditions.get("lux", self.estimate_lux(eo_frame))
        smoke = conditions.get("smoke_density", 0)
        rain  = conditions.get("rain_mm_hr", 0)

        if smoke > 0.5:       return "SWIR_PENETRATION"
        if lux < 0.01:        return "THERMAL_ONLY"
        if lux < 1.0:         return "FUSION_THERMAL_DOMINANT"
        if lux < 10.0:        return "FUSION_EQUAL"
        return "EO_DOMINANT"
```

### Fusion Output Visualization Modes (Operator-Selectable)

```
MODE NAME           DESCRIPTION                           USE CASE
────────────────────────────────────────────────────────────────────
COLOUR EO           Standard 4K colour video              Daytime
IRON THERMAL        False-colour LWIR (classic)           Night patrol
WHITEHOT            Bright = hot, dark = cold             Tactical
BLACKHOT            Inverted thermal (many prefer this)   User preference
FUSION OVERLAY      EO + thermal blended (see-thru)       Twilight
RAINBOW             Full spectrum thermal colouring       Analytics
SWIR MONO           Greyscale SWIR                        Smoke/fog
SWIR+THERMAL FUSE   SWIR structure + thermal heat         Fire scenes
```

---

## Sensor Fusion Engine

### Architecture: The Single Unified Picture

All sensors connect to the Jetson via a **payload hub** — a custom PCB that aggregates USB3, MIPI CSI, UART, and Ethernet interfaces into a single board managed by the Jetson.

```
┌──────────────────────────────────────────────────────────────────┐
│              PAYLOAD HUB (Custom PCB on Drone)                   │
└──────────────────────────────────────────────────────────────────┘

INPUTS:
├── MIPI CSI-2 (×4 lanes): EO main camera
├── USB3.1 Gen2: FLIR Boson thermal
├── USB3.1 Gen2: SWIR camera (if equipped)
├── USB3.1 Gen2: LiDAR unit (if equipped)
├── USB3.1 Gen2: Hyperspectral (if equipped)
├── I2C: IMU (VectorNav VN-100, 200Hz)
├── UART: Pixhawk MAVLink (position, attitude)
├── UART: GPS RTK (u-blox F9P, 2cm accuracy)
└── SPI: Environmental sensor (temp, humidity, pressure)

OUTPUTS TO JETSON:
└── PCIe Gen4: Aggregated sensor bus (single high-bandwidth link)

JETSON INTERNAL PIPELINE:
sensor_data → GStreamer source elements (per sensor)
           → Hardware decode (NVDEC)
           → Cuda memory (zero-copy, NVMM buffers)
           → Fusion kernel (CUDA custom shader)
           → YOLOv8 TensorRT inference
           → AR composition
           → NVENC hardware encode (output stream)

LATENCY BUDGET:
├── Sensor capture:        0 ms (reference)
├── Hardware decode:       5 ms
├── Fusion kernel:        10 ms
├── YOLOv8 inference:     15 ms
├── AR composition:        5 ms
├── Hardware encode:      10 ms
└── Total pipeline:      ~45 ms glass-to-encode
```

### IMU & GPS Tight Coupling (Stabilisation + Geolocation)

The fusion engine is **tightly coupled** with the IMU (200Hz) and GPS/RTK (10Hz). This means:

```
1. GIMBAL ATTITUDE: At every frame, the exact gimbal pitch/roll/yaw
   is recorded. This means every pixel in the frame can be
   georeferenced precisely.

2. VIBRATION COMPENSATION: IMU at 200Hz feeds the digital stabilisation
   pipeline, removing high-frequency jitter that mechanical gimbals miss.

3. DETECTION GEOLOCATION: When YOLOv8 detects "person" in the frame,
   the system instantly computes the GPS coordinates of that detection:

   detected_pixel (u, v)
   + gimbal_angles (pitch, roll, yaw)
   + drone_position (lat, lon, alt)
   + terrain_elevation (DEM lookup)
   ────────────────────────────────
   = detection_gps (lat, lon) ± 3m accuracy

4. FORENSIC ANNOTATION: Every recorded frame stores metadata:
   {frame_id, timestamp, drone_lat, drone_lon, drone_alt,
    gimbal_pitch, gimbal_roll, gimbal_yaw, sensor_mode}
   This allows post-flight reconstruction of exactly what the
   drone was looking at for any given second.
```

---

## Augmented Reality (AR) Overlay System

### Architecture: Two Layers of AR

OS-DRONE implements AR at **two levels**:

- **Level 1: On-Stream AR** — baked into the video stream itself (HUD overlay rendered by Jetson, anyone watching the stream sees it)
- **Level 2: Operator AR** — rendered client-side in the Fleet Ops dashboard or on AR glasses; contains interactive elements, linked to live data

### Level 1: On-Stream HUD Overlay

```
What gets rendered onto the live video stream by the Jetson:

┌──────────────────────────────────────────────────────────────────┐
│  DRONE-07  ●REC  BAT:72%  ALT:80m  SPD:0.0m/s  GPS:OK  ●LIVE  │
│                                                                  │
│                                                                  │
│         ┌─────────────────┐                                     │
│         │  PERSON         │  ← YOLOv8 detection bbox           │
│         │  ID: TRK-0042   │    with persistent track ID        │
│         │  DWELL: 4:23    │    and dwell time counter          │
│         └─────────────────┘                                     │
│                    ↑                                             │
│                 45.421°N  75.697°W                              │
│                 (auto-geoloc of detection)                      │
│                                                                  │
│  ◄────────────────────────────────────────────────────────────►│
│  N                                   COMPASS                  N │
│                                                                  │
│  THERMAL: OFF  │  FUSION: EO  │  ZOOM: 1×  │  MODE: PATROL    │
└──────────────────────────────────────────────────────────────────┘

HUD Elements:
├── Top bar: Drone ID, recording status, battery, altitude, speed, GPS
├── Detection boxes: colour-coded by class (red=person, blue=vehicle)
├── Track ID: persistent identifier across frames (DeepSORT)
├── Dwell time: how long this track has been in frame/zone
├── Geolocation: GPS coords of each detection, displayed below bbox
├── Compass rose: always-visible heading indicator
├── Sensor mode: current fusion mode, zoom level, mission mode
├── Geofence boundary: thin red line rendered at fence boundary
├── Scale bar: distance indicator calibrated to current altitude
└── Mini-map: inset showing drone position on site map
```

```python
# AR HUD Compositor — running on Jetson CUDA

class ARHUDCompositor:

    def render(self, fused_frame, detections, telemetry, geofence):
        # All rendering via GPU (OpenGL ES or CUDA surface)
        canvas = CUDASurface(fused_frame)

        # 1. Detection bounding boxes + labels
        for det in detections:
            color  = self.class_colors[det.class_name]
            canvas.draw_box(det.bbox, color, thickness=2)
            canvas.draw_label(det.bbox.top_left,
                f"{det.class_name} | TRK-{det.track_id:04d} | "
                f"{det.dwell_time:.0f}s | "
                f"{det.gps_lat:.5f}°N {det.gps_lon:.5f}°W",
                font_size=14, color=color)

        # 2. Top status bar
        canvas.draw_status_bar(
            drone_id   = telemetry.drone_id,
            recording  = telemetry.recording,
            battery    = telemetry.battery_pct,
            altitude   = telemetry.altitude_m,
            speed      = telemetry.speed_ms,
            sensor_mode= telemetry.sensor_mode
        )

        # 3. Geofence overlay (project 3D fence to image plane)
        geofence_pixels = self.project_geofence_to_image(
            geofence, telemetry.position, telemetry.gimbal_angles
        )
        canvas.draw_polygon(geofence_pixels, color=(255,0,0), thickness=2)

        # 4. Compass rose (top-right corner)
        canvas.draw_compass(telemetry.heading, position="top-right")

        # 5. Mini-map (bottom-right)
        canvas.draw_minimap(telemetry.lat, telemetry.lon,
                            detections, position="bottom-right")

        # 6. Scale bar (bottom-left)
        canvas.draw_scalebar(telemetry.altitude_m, telemetry.camera_fov)

        return canvas.encode_h265(bitrate=4_000_000)
```

### Level 2: Operator AR — Fleet Ops Interactive Dashboard

The Fleet Ops web dashboard renders **fully interactive AR** on top of the drone video feed, using WebGL and live data from the Fleet Ops API:

```
INTERACTIVE AR ELEMENTS (not burned into stream, interactive in browser):

1. PERSISTENT TRACK TRAILS
   Each tracked person/vehicle has a trajectory line drawn behind them
   on the map and on the video feed. Operator can click any trail to
   see: first seen timestamp, total distance travelled, predicted path.

2. ZONES & VIRTUAL TRIPWIRES
   Operator draws zones directly on the video (polygons, lines).
   System triggers when tracked objects cross the tripwire.
   Zones appear as semi-transparent overlays on video.

3. MEASUREMENT TOOL
   Operator clicks two points on video → system calculates real-world
   distance between them (using drone altitude + camera FOV + GPS).
   "That crowd is 45m from the entrance."

4. LINKED CAMERA OVERLAY
   When drone is flying over an area covered by OS-SENTINEL fixed cameras,
   those camera FOVs are projected onto the drone's aerial view as
   coloured cones — operator sees exactly what each camera covers from above.

5. ASSET OVERLAY
   OS-PATROL vehicles and OS-GUARDIAN officers with active body cams
   appear as labelled icons on the drone's aerial view in real time.
   "Unit 7 is 200m south. Officer Chen is at the east entrance."

6. HISTORICAL HEATMAP
   Toggle on: shows detection heatmap overlay (last 24h / 7 days)
   on the live video. Operator sees exactly which zones have had
   the most activity — without leaving the video view.
```

### AR Glasses Integration (Field Operator)

For field security officers, the AR stream can feed directly into **smart glasses** (Microsoft HoloLens 2, Magic Leap 2, or Rokid Max):

```
FIELD AR VIEW (on operator's AR glasses):

What the security officer sees in their glasses:
├── Arrow: "Drone DRONE-07 is 80m above, northeast"
├── Live drone thumbnail (corner of vision)
├── Alert icon: "Drone detected 2 persons at Gate C"
│   └── Arrow pointing toward Gate C
├── Mini-map: site map with drone position + detections
├── Waypoint marker: "Investigation point — 45m, heading 270°"
└── Person outline: when detected person comes into officer's
    own FOV, AR outlines them in orange
    (drone feeds coordinates → glasses project AR marker)

Technology Stack:
├── Glasses: HoloLens 2 (preferred) or Rokid Max (lower cost)
├── App: Custom Unity app on HoloLens / React Native on Rokid
├── Data: Fleet Ops WebSocket → glasses app (same WS feed)
├── Video: Drone RTSP stream → HLS → glasses video player
└── AR anchoring: Azure Spatial Anchors (HoloLens)
                  or GPS-based for outdoor (Rokid)
```

---

## LiDAR & 3D Mapping

### What LiDAR Adds

LiDAR is not just for surveying — it provides **geometric intelligence** that cameras alone cannot:

```
SECURITY USE CASES FOR LIDAR:
├── Volumetric occupancy: Is this building actually empty? LiDAR
│   detects objects/people by geometry, not heat or light.
├── 3D geofencing: Vertical geofence — alert if anything enters
│   a 3D volume (under a bridge, inside a perimeter, above a roof)
├── Change detection: Compare today's 3D scan to yesterday's.
│   Any object that appeared or moved is instantly flagged.
├── Structural inspection: Detect cracks, deformation,
│   settlement in structures — mm-level accuracy from air.
└── Smoke-penetrating 3D: LiDAR penetrates smoke better than cameras.
    Lidar + thermal = locate people in burning buildings.

SURVEYING USE CASES:
├── Topographic mapping: True-elevation terrain models (DTM/DSM)
├── Stockpile volume: Measure aggregate, gravel, coal volumes
│   from air in minutes — replaces days of manual survey
├── As-built verification: Compare construction to BIM model
└── Corridor mapping: Linear infrastructure (roads, pipelines)
```

### Recommended LiDAR Module

```
PRIMARY: DJI Zenmuse L2 (best-in-class for drone, integrated)
├── Laser: 240,000 points/second (5-return, 100m range)
├── Accuracy: 4cm horizontal, 2cm vertical (RTK-corrected)
├── IMU: VectorNav VN-200 integrated (tightly coupled)
├── Interface: DJI Payload SDK (or custom via UART/Ethernet)
├── Weight: 905g
└── Cost: ~$14,000

OPEN-SOURCE ALTERNATIVE: Livox Mid-360 + custom mount
├── Laser: 200,000 points/second, 360° horizontal FOV
├── Range: 40m (practical at drone altitude)
├── Interface: Ethernet (ROS2 driver available)
├── Weight: 265g
├── Cost: ~$1,200
└── Note: Requires custom IMU tight-coupling for accurate mapping

POINT CLOUD PIPELINE:
LiDAR → Livox ROS2 driver
      → LIO-SAM (LiDAR-Inertial Odometry)
      → PointPillars AI (3D object detection in point cloud)
      → PCL (change detection vs. reference scan)
      → Open3D (3D visualisation, served to Fleet Ops dashboard)
      → CloudCompare (offline analysis, survey deliverables)
```

### Change Detection for Security

```python
# Automated site change detection using LiDAR
# Runs nightly as a background task on Fleet Ops server

def nightly_change_detection(site_id, new_scan_path, baseline_scan_path):
    """
    Compare today's LiDAR scan against baseline.
    Returns: list of changes with GPS coordinates and severity.
    """
    baseline = load_point_cloud(baseline_scan_path)
    today    = load_point_cloud(new_scan_path)

    # Register (align) scans using ICP
    transformation = icp_align(today, baseline)
    today_aligned  = today.transform(transformation)

    # Compute difference
    distances = compute_nearest_neighbor_distances(today_aligned, baseline)

    # Threshold: changes > 0.3m are significant
    changed_points = today_aligned.points[distances > 0.30]

    # Cluster changes into discrete objects
    clusters = dbscan_cluster(changed_points, eps=0.5, min_pts=10)

    changes = []
    for cluster in clusters:
        centroid_gps = drone_lidar_to_gps(cluster.centroid)
        volume_m3    = cluster.convex_hull_volume()
        changes.append({
            "gps":      centroid_gps,
            "volume":   volume_m3,
            "severity": "HIGH" if volume_m3 > 1.0 else "LOW",
            "category": classify_change(cluster)  # "vehicle", "debris", "person"
        })

    # Publish to Hub as drone.change_detection events
    publish_to_hub("drone.change_detection", {"site_id": site_id, "changes": changes})
    return changes
```

---

## Multispectral & Hyperspectral

### When You Need More Than Visible + Thermal

For applications like agriculture, environmental monitoring, and infrastructure inspection, you need to **quantify** what you're seeing — not just see it.

```
MULTISPECTRAL (5-10 discrete bands):
Hardware: MicaSense RedEdge-P
├── Bands: Blue(475nm), Green(560nm), Red(668nm),
│          Red Edge(717nm), NIR(842nm) — 5 bands
├── Resolution: 21 MP panchromatic + 3.2 MP per band
├── Capture: GPS-triggered, synchronized with drone position
├── Output: Calibrated reflectance maps
└── Cost: ~$7,000

Applications:
├── NDVI maps: (NIR - Red) / (NIR + Red) — vegetation health index
├── Crop stress detection: disease/drought 2-3 weeks before visible
├── Solar panel efficiency: IR absorption anomalies
├── Roof membrane inspection: moisture ingress (invisible to EO)
└── Environmental: algae bloom, illegal dumping, wetland mapping

HYPERSPECTRAL (100-200+ continuous bands):
Hardware: Specim AFX10 or Headwall Photonics
├── Bands: 400–1000nm continuous (visible + NIR)
├── Spectral resolution: 5nm (fingerprint-level specificity)
├── Output: 3D datacube (x, y, wavelength)
└── Cost: $40,000–$80,000

Applications (where you need spectral fingerprinting):
├── Material identification: detect specific chemicals, minerals
├── Counterfeit detection: verify material authenticity from air
├── Pollution source tracing: identify chemical composition of spills
└── Illegal crop detection: cannabis, coca — unique spectral signature
```

### NDVI Pipeline (Agriculture Example)

```python
# Automated NDVI analysis pipeline (Fleet Ops background worker)

def compute_ndvi_map(mission_id, red_band_path, nir_band_path):
    """
    Compute Normalized Difference Vegetation Index from multispectral flight.
    NDVI = (NIR - Red) / (NIR + Red)
    Range: -1 (water/bare) to +1 (dense healthy vegetation)
    Threshold alerts: <0.3 = stressed crop
    """
    red = load_reflectance_band(red_band_path)  # Calibrated 0.0–1.0
    nir = load_reflectance_band(nir_band_path)

    ndvi = (nir - red) / (nir + red + 1e-8)  # Avoid div/0

    # Classify health zones
    health_map = numpy.zeros_like(ndvi, dtype=numpy.uint8)
    health_map[ndvi < 0.2]  = BARE_SOIL      # Brown
    health_map[ndvi < 0.4]  = STRESSED       # Yellow
    health_map[ndvi >= 0.4] = HEALTHY        # Green

    # Generate GeoTIFF (georeferenced for GIS)
    save_geotiff(f"ndvi_{mission_id}.tif", ndvi, crs="EPSG:4326")

    # Find stressed areas, generate GPS-tagged alerts
    stressed_zones = find_contiguous_zones(health_map, STRESSED, min_area_ha=0.1)
    for zone in stressed_zones:
        publish_alert("drone.ndvi.stressed", {
            "mission_id": mission_id,
            "area_ha": zone.area_ha,
            "centroid_gps": zone.centroid_gps,
            "severity": "HIGH" if zone.area_ha > 1.0 else "MEDIUM"
        })

    return ndvi, health_map
```

---

## Surveying & Photogrammetry Engine

### Autonomous Survey Missions

The surveying system is built on top of the standard OS-DRONE mission engine — it's just a specific mission type with structured waypoints and post-processing pipelines.

```
SURVEY MISSION TYPES:

1. ORTHOMOSAIC MAPPING (aerial photography → georeferenced map)
   ├── Waypoint pattern: lawnmower grid at constant altitude
   ├── Trigger: GPS-triggered photo every N metres
   ├── Overlap: 80% front, 70% side (configurable)
   ├── Output: Stitched orthomosaic GeoTIFF (1-5 cm/pixel GSD)
   └── Software: OpenDroneMap (ODM) — open source, on-premise

2. 3D RECONSTRUCTION (photogrammetry → 3D model)
   ├── Same as orthomosaic but with oblique photos added
   ├── Output: Dense point cloud, mesh, textured 3D model
   └── Software: OpenDroneMap (Structure from Motion)

3. LIDAR MAPPING (LiDAR → point cloud → DTM/DSM)
   ├── Slower, lower altitude (50–100m AGL), tighter lines
   ├── Output: Classified point cloud, DTM, DSM, contours
   └── Software: PDAL + CloudCompare + LAStools (open source)

4. INSPECTION ROUTE (structure-following, close-range)
   ├── Drone follows structure at constant offset distance
   ├── High-resolution camera captures every face
   ├── AI flags anomalies in real time
   └── Software: Pix4D Inspection (or OpenDroneMap)

5. CORRIDOR MAPPING (linear infrastructure)
   ├── Drone follows GPS-defined line (road, pipeline, powerline)
   ├── Left/right cameras + nadir camera
   └── Output: Linear feature map with anomaly tags
```

### Open-Source Photogrammetry Stack

```
POST-PROCESSING PIPELINE (runs on Fleet Ops GPU server):

1. Image collection: all photos from mission → MinIO bucket
                     {site_id}/surveys/{mission_id}/raw/

2. OpenDroneMap processing (Docker container on GPU server):
   odm --project-path /data/{mission_id}
       --feature-type sift
       --matcher-type flann
       --sfm-algorithm incremental
       --mesh-size 200000
       --orthophoto-resolution 2.0       ← 2cm/pixel
       --use-3dmesh true
       --pc-quality ultra
       --gps-accuracy 0.10               ← RTK GPS precision
       --time

3. Outputs to MinIO:
   {site_id}/surveys/{mission_id}/products/
   ├── odm_orthophoto/odm_orthophoto.tif  (georeferenced map)
   ├── odm_dem/dsm.tif                    (surface model)
   ├── odm_dem/dtm.tif                    (terrain model)
   ├── odm_pointcloud/cloud.laz           (3D point cloud)
   ├── odm_texturemesh/                   (3D textured model)
   └── report.pdf                         (processing report)

4. Web viewer:
   ├── Potree viewer (3D point cloud in browser — open source)
   └── OpenLayers (orthomosaic tile serving — open source)
   Both served from Fleet Ops dashboard, accessible from Hub.

PROCESSING TIME (on 2× RTX 4090):
├── 100 photos,  10 acres:   15 min
├── 500 photos,  50 acres:   45 min
└── 2000 photos, 200 acres: 2.5 hours
```

---

## Payload Configuration Profiles

### 60-Second Profile Switching

Just as OS-GUARDIAN allows 60-second profile switching for different deployment contexts, OS-DRONE implements **payload profiles** — pre-defined sensor mode combinations that the operator can activate instantly:

```
PROFILE: NIGHT_SECURITY
├── Primary stream: FUSION_THERMAL_DOMINANT
├── AI models: Person detection, vehicle detection (thermal-tuned)
├── HUD: WHITEHOT palette, dwell time counters prominent
├── Recording: Full thermal + EO raw (dual-stream)
└── Alerts: Low confidence threshold (0.55) — catch everything

PROFILE: DAYTIME_PATROL
├── Primary stream: EO 4K
├── AI models: Full suite (person, vehicle, face, LPR)
├── HUD: Standard colour overlay
├── Recording: 4K EO, thumbnail AI events
└── Alerts: Standard threshold (0.7)

PROFILE: SMOKE_FIRE
├── Primary stream: SWIR+THERMAL FUSION
├── AI models: Person detection (thermal dominant), fire/smoke detection
├── HUD: SWIR primary, thermal heat overlay
├── Recording: Both SWIR and thermal raw streams + fused
└── Alerts: Lowest threshold (0.45) — assume reduced visibility

PROFILE: SURVEY_MAPPING
├── Primary stream: EO 4K nadir (downward-facing)
├── Multispectral: 5-band capture (GPS-triggered)
├── AI models: OFF (saves compute for mapping)
├── Recording: Raw photos (not video) for ODM processing
└── Mission type: Lawnmower grid at configured altitude

PROFILE: INSPECTION
├── Primary stream: EO 4K + LWIR dual-stream
├── AI models: Crack detection, thermal anomaly detection
├── HUD: Split-screen EO/thermal side by side
├── Recording: Maximum quality (4K + full thermal)
└── GPS: RTK-corrected (centimetre accuracy for annotation)

PROFILE: INCIDENT_RESPONSE
├── Primary stream: FUSION_EQUAL (automatic day/night selection)
├── AI models: All active (max alert sensitivity)
├── HUD: All tracks visible, geoloc on all detections
├── Recording: Continuous + event clips + thumbnails every 10s
└── Streaming: Push to all Hub operators simultaneously
```

---

## On-Board Processing Architecture

### How the Jetson Orin NX Handles It All

The key to making all of this work without adding external compute is **pipeline parallelism** — the Jetson's CPU, GPU, NVENC, NVDEC, DLA (deep learning accelerator), and ISP all run simultaneously on different tasks.

```
JETSON ORIN NX HARDWARE ALLOCATION:

ISP (Image Signal Processor):
└── Task: Raw camera demosaicing, tone mapping, noise reduction

NVDEC (Video Decoder):
└── Task: Decode incoming thermal/SWIR video streams

DLA (Deep Learning Accelerator, 2× DLA cores):
└── Task: Run YOLOv8-nano continuously at 30fps (always-on detection)
         Low power, high throughput — frees GPU for fusion

CUDA GPU (1024 Ampere cores):
└── Tasks:
    ├── Sensor fusion kernel (frame alignment + blending)
    ├── YOLOv8-small inference (higher accuracy when needed)
    ├── DeepSORT tracking
    ├── AR HUD compositor (OpenGL ES)
    └── LiDAR point processing (if equipped)

NVENC (Video Encoder, 2× engines):
└── Tasks:
    ├── Encoder 1: Fused + AR stream → H.265 4 Mbps (live stream)
    └── Encoder 2: Raw EO 4K → H.265 12 Mbps (local record)

CPU (6× Arm Cortex-A78AE):
└── Tasks:
    ├── OS-DRONE agent (Python asyncio, MAVLink, MQTT)
    ├── WireGuard VPN
    ├── RTSP server (GStreamer)
    ├── LiDAR driver (ROS2 node)
    └── System management (temp monitoring, failsafe watchdog)

POWER BUDGET (Jetson Orin NX @ full load):
├── Module:              25W (15W idle)
├── All cameras:         8W
├── LiDAR (Livox):       9W
├── 4G modem:            3W
├── C2 radio:            2W
└── Total companion:    ~47W (well within 6S drone power budget)
```

---

## Fleet Ops Visual Intelligence Dashboard

### The Operator View

The Fleet Ops dashboard is upgraded with a **Visual Intelligence Panel** for each drone:

```
DASHBOARD LAYOUT (per drone panel):

┌─────────────────────────────────────────────────────────────────┐
│  DRONE-07 ● LIVE  BAT:72%  ALT:80m  MISSION: INCIDENT_RESPONSE │
├──────────────────────────────┬──────────────────────────────────┤
│                              │  SENSOR SELECT                  │
│    FUSED VIDEO FEED          │  ○ EO Colour                    │
│    (AR overlay active)       │  ● Fusion (EO+Thermal)          │
│                              │  ○ Thermal Only                  │
│    [live video panel]        │  ○ SWIR                          │
│                              │                                  │
│    ← Person TRK-0042        │  ZOOM: [────●────────] 4×       │
│       4:23 dwell             │                                  │
│       45.4215°N 75.6972°W   │  FUSION WEIGHT:                 │
│                              │  EO  [──●─────────] 40%        │
│    ← Vehicle TRK-0017       │  IR  [─────●──────] 60%        │
│       MOVING: 8 km/h N      │                                  │
│       ABC-1234 (HOT LIST)   │  NIGHT MODE: ● AUTO             │
│                              │                                  │
├──────────────────────────────┤  AR LAYERS:                     │
│  SITE MAP (aerial)           │  ☑ Detection boxes              │
│  [drone position + tracks]   │  ☑ Track trails                 │
│  [OS-PATROL vehicles]        │  ☑ Geolocation labels          │
│  [OS-GUARDIAN officers]      │  ☑ Geofence boundary           │
│  [detection heatmap overlay] │  ☑ Asset positions             │
│                              │  ☑ Fixed camera FOVs           │
│                              │  ☑ Measurement tool             │
├──────────────────────────────┴──────────────────────────────────┤
│  ACTIVE TRACKS: 2 persons, 1 vehicle                            │
│  ALERTS: [HIGH] Vehicle ABC-1234 — STOLEN — dispatching patrol  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Integration with OpenSecure Ecosystem

### Visual Intelligence Data Flow

```
OS-DRONE visual intelligence enriches every other OpenSecure service:

OS-DRONE → OS-SENTINEL:
├── Drone detection (lat, lon) + track → PTZ camera auto-slews to target
├── Drone orthomosaic → updates SENTINEL camera coverage map
└── Drone 3D change detection → identifies where new cameras needed

OS-DRONE → OS-PATROL:
├── Aerial vehicle track (GPS) → feeds PATROL live vehicle tracking map
├── Drone LPR hit → PATROL unit dispatched with aerial escort active
└── Aerial heatmap → PATROL route optimization (patrol where incidents occur)

OS-DRONE → OS-GUARDIAN:
├── Drone overhead video + officer body cam = two-angle evidence package
├── GPS: drone can tell officer: "suspect is 30m northeast of you"
└── AR: officer's glasses show drone-derived location of threat

OS-DRONE → OS-PACS:
├── Drone detects tailgating → PACS sends lockdown signal to zone
├── Drone 3D map → PACS knows exact 3D location of every access point
└── Drone change detection → PACS detects new paths/holes in perimeter

OS-DRONE → Digital Twin:
├── Orthomosaic → updates base map in digital twin
├── 3D model → updates 3D building/site model
├── Real-time positions → live drone position in 3D twin
└── Heatmaps → incident density overlay in twin
```

---

## Hardware BOM by Capability Tier

| Sensor | Model | Interface | Cost | Weight | Use Case |
|--------|-------|-----------|------|--------|----------|
| EO Main | Sony IMX577 4K, 3-axis gimbal | MIPI CSI-2 | $1,800 | 320g | All missions |
| EO Low-Light | Sony IMX585 Starvis 2 | MIPI CSI-2 | $2,500 | 320g | Night primary sites |
| LWIR Thermal | FLIR Boson 640+ | USB3 | $4,000 | 75g | Night, person detection |
| LWIR Advanced | FLIR Neutrino LC (MWIR, cooled) | USB3/LVDS | $22,000 | 400g | Critical infrastructure |
| SWIR | Sensors Unlimited 640CSX | USB3 | $14,000 | 280g | Smoke, glass, haze |
| LiDAR (entry) | Livox Mid-360 | Ethernet | $1,200 | 265g | 3D mapping, change detection |
| LiDAR (pro) | DJI Zenmuse L2 | DJI SDK | $14,000 | 905g | Survey-grade mapping |
| Multispectral | MicaSense RedEdge-P (5-band) | USB3 | $7,000 | 355g | Agri, solar, roof |
| Hyperspectral | Specim AFX10 | GigE | $42,000 | 1.3 kg | Chemical, material ID |
| AR Glasses | Microsoft HoloLens 2 | WiFi/BLE | $3,500 | 566g | Field AR operator |
| AR Glasses (budget) | Rokid Max | USB-C | $500 | 75g | Fleet Ops AR viewer |
| Spotlight | Acebeam X75 (drone-mount) | PWM | $400 | 380g | Night illumination |
| Speaker | Autel EVO Max speaker payload | UART | $600 | 290g | Warning broadcast |
| Radar | Echodyne EchoGuard | Ethernet | $35,000 | 620g | Through-wall, rain |

**Practical Recommendation for Most Security Deployments:**

Start with **EO + LWIR (Tier 1)** at $5,800 per drone above the base airframe. This covers 90% of security use cases. Add SWIR only if you have smoke/fire risk. Add LiDAR only if surveying is a requirement. The fusion engine is already in the base software stack — adding a sensor is a hardware connection and a software driver.

---

**Document Version**: 1.0
**Platform**: OS-DRONE v1.0
**Companion Documents**: OS-DRONE_Technical_Architecture.md, OS-DRONE_Network_Topology.md
