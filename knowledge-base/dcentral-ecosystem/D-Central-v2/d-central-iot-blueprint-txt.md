---
source_project: D Central v2
source_project_uuid: 0199df04-2107-76ac-8919-203857b7a6c9
doc_uuid: c0beb3e3-19ea-4c4b-910f-93c4d8bd3cee
original_filename: d-central-iot-blueprint.txt
created_at: 2025-10-13T19:26:30.642609+00:00
content_hash: 2335bb4238ec
---

## 1) Comprehensive Device Catalog (Nothing Left Behind)

### **A) CLIMATE & ENVIRONMENT**

**HVAC & Comfort**
* Smart thermostats (multi-zone, heat pump, radiant, forced-air, mini-splits)
* Smart vents & dampers (per-room balancing, automated zoning)
* Ceiling fans & ventilation (speed control, occupancy-linked)
* Portable heaters & AC units (smart plugs + temp sensors)
* Humidifiers & dehumidifiers (whole-house + room units)
* Air purifiers & filters (HEPA, UV-C, filter-life tracking)
* ERV/HRV fresh-air exchangers (indoor air quality optimization)
* Heated floors & radiant panels (zone controllers)

**Lighting**
* Smart bulbs (color, tunable white, dimming)
* Smart switches & dimmers (0-10V, DALI, TRIAC, PoE lighting)
* Occupancy-linked fixtures (ceiling, cabinet, closet)
* Outdoor landscape lighting (path, accent, security)
* Emergency/exit lighting (battery-backed, self-test)
* Circadian-rhythm controllers (sunrise/sunset simulation)
* Architectural lighting (cove, facade, decorative DMX)

**Air Quality & Sensors**
* Multi-gas sensors (CO, COâ‚‚, PM2.5, PM10, VOC, NOâ‚‚, radon, formaldehyde)
* Temperature & humidity sensors (indoor/outdoor, per-room)
* Barometric pressure (weather station integration)
* Allergen & pollen monitors
* Mold/moisture sensors (wall cavities, basements)

---

### **B) ENERGY & POWER**

**Metering & Management**
* Whole-home/building energy monitors (CT clamps, Rogowski coils)
* Circuit-level sub-meters (per-breaker monitoring)
* Smart breakers (remote trip, arc-fault detection)
* Smart plugs & outlets (per-device kWh, scheduling)
* Metered PDUs & rack power (enterprise/data-center per-outlet)
* Power quality monitors (voltage sag/swell, harmonics, power factor)
* Generator monitors & ATS (automatic transfer switches)
* UPS systems (battery health, runtime, load tracking)

**Renewables & Storage**
* Solar inverters & optimizers (string, micro, hybrid)
* Battery storage systems (BMS integration, SOC/SOH)
* Charge controllers (MPPT for off-grid)
* Production meters (PV generation, net metering)
* EV chargers / EVSE (Level 1/2/DC fast, OCPP, load balancing)
* V2H/V2G bidirectional chargers (vehicle-to-home/grid)
* Wind turbines & micro-hydro (small-scale DER)

**Grid & Demand Response**
* Smart meters (gas, water, electric utility interface)
* Grid-interactive devices (OpenADR clients, DERMS endpoints)
* Load-shedding relays (DR-triggered breaker control)
* Time-of-use controllers (shift HVAC, EV, pool pumps)

---

### **C) WATER & FLUID SYSTEMS**

* Smart water meters (ultrasonic, electromagnetic, whole-home + fixture-level)
* Leak detectors (floor sensors, inline flow monitors, acoustic)
* Motorized shut-off valves (main line, per-zone, appliance-specific)
* Hot water recirculation pumps (on-demand, schedule)
* Water heaters (tank, tankless, heat-pump controllers)
* Sump pumps & ejector pumps (level sensors, backup battery alerts)
* Well pumps & pressure tanks (cycle counting, dry-run protection)
* Irrigation & sprinkler controllers (smart timers, soil moisture, weather-linked)
* Drip irrigation valves (per-zone, per-plant precision)
* Rainwater harvesting (tank level, pump control)
* Greywater systems (treatment monitoring, reuse valves)
* Pool & spa controllers (pumps, heaters, chemical dosing, pH/ORP/chlorine)
* Hot tub covers & bubblers (automated, freeze protection)
* Water softeners & filters (regeneration tracking, salt level)
* Sewage/septic monitors (tank level, pump health)

---

### **D) PERIMETER & ACCESS CONTROL**

**Entry & Locks**
* Smart door locks (deadbolts, levers, mortise, keypad, BLE/NFC, fingerprint)
* Smart garage door openers (tilt sensors, camera integration)
* Gate operators (sliding, swing, vehicle/pedestrian)
* Automatic doors (ADA, commercial vestibules)
* Turnstiles & barriers (pedestrian, vehicle, parking)
* Elevator access control (floor restriction, call buttons)

**Sensors & Monitoring**
* Door/window sensors (reed, magnetic, shock/vibration)
* Glass-break detectors (acoustic, shock)
* Motion sensors (PIR, mmWave radar, dual-tech)
* Driveway/perimeter sensors (beam, buried cable, pressure mat)
* Mailbox/package sensors (delivery notifications)
* Fence line sensors (cut/climb detection)

**Identification & Badges**
* Card readers (RFID, NFC, Wiegand, OSDP)
* Biometric scanners (fingerprint, face, iris, palm vein)
* License plate recognition (LPR cameras)
* Visitor management kiosks (sign-in, badge printing)
* Wristbands & proximity tags (events, healthcare, hospitality)

---

### **E) VIDEO, AUDIO & COMMUNICATIONS**

**Cameras & Surveillance**
* Fixed cameras (indoor/outdoor, dome, bullet, turret, PTZ)
* Panoramic/360Â° cameras (fisheye, multi-sensor)
* License plate/ANPR cameras (vehicle identification)
* Thermal/infrared cameras (heat detection, night vision)
* Body-worn cameras (lone-worker, security personnel)
* Doorbell cameras (visitor identification, package monitoring)
* Baby monitors & pet cameras (two-way audio, treat dispensers)
* NVR/DVR systems (on-prem recording, edge analytics)
* Video management systems (VMS for enterprise)

**Intercom & Paging**
* Video intercoms (entrance stations, room stations)
* Audio-only intercoms (apartment buildings, offices)
* PA/paging systems (emergency announcements, background music)
* Two-way radios & repeaters (site communications)

**Audio & Entertainment**
* Multi-room audio (Sonos-style, ceiling speakers, outdoor)
* Smart speakers & displays (voice assistants, visual dashboards)
* Smart TVs & projectors (display signage, digital directories)
* Conference room audio/video (cameras, mics, DSPs, codecs)

---

### **F) SAFETY & EMERGENCY**

**Fire & Life Safety**
* Smoke detectors (photoelectric, ionization, dual-sensor)
* Carbon monoxide detectors
* Natural gas/propane detectors
* Heat detectors (fixed-temp, rate-of-rise)
* Flame detectors (UV/IR, industrial)
* Water-mist & sprinkler flow switches
* Fire alarm panels & annunciators (networked, addressable)
* Emergency lighting (battery-backed, exit signs, path-marking)
* Evacuation voice systems (EVACS, mass notification)
* Fire extinguisher monitors (pressure, tamper, use-tracking)

**Safety Devices**
* Panic buttons (fixed, wearable, mobile app)
* Lone-worker check-in devices (man-down alarms)
* Fall detectors (elderly care, industrial)
* Duress codes (silent alarm triggers on locks/keypads)
* Emergency call boxes (outdoor, parking garages)
* AEDs (automated external defibrillators with connectivity)

**Hazard Monitoring**
* Radiation detectors (Geiger counters for labs, industrial)
* Chemical sensors (Hâ‚‚S, ammonia, chlorine, Oâ‚‚ deficiency)
* Explosion-proof devices (Class I/II/III Div 1/2 environments)
* Lightning detection (storm proximity, grounding monitors)
* Seismic sensors (earthquake early warning)

---

### **G) APPLIANCES & HOME COMFORT**

**Kitchen**
* Smart refrigerators (inventory, cameras, temp monitoring)
* Smart ovens & ranges (preheat, remote monitoring, auto-shutoff)
* Dishwashers (cycle status, detergent alerts)
* Coffee makers & kettles (schedule, voice control)
* Sous vide & slow cookers
* Wine coolers & beverage fridges
* Trash compactors & smart waste bins (fill-level sensors)
* Garbage disposals (jam detection, remote control)
* Range hoods (auto-activation on smoke/heat)

**Laundry**
* Smart washers & dryers (cycle alerts, remote start, maintenance)
* Leak pans & overflow detectors (under appliances)
* Lint sensors (dryer vent blockage alerts)

**Cleaning & Maintenance**
* Robot vacuums & mops (scheduled, room-specific)
* Central vacuum systems (run-time tracking)
* Automated pool cleaners (robotic, schedule-linked)

**Garage & Workshop**
* Tool lockers & vending (RFID checkout, inventory)
* Compressors & pneumatic tools (usage tracking, pressure)
* Fume extractors & ventilation (auto-activation)
* Workbench power (remote shutoff for safety)

**Outdoor & Lifestyle**
* Outdoor grills & smokers (temp probes, pellet hoppers)
* Patio heaters & fire pits (automated ignition, safety shutoff)
* Awnings & retractable shades (sun/wind sensors)
* Outdoor furniture sensors (rain detection, cover deployment)

---

### **H) WINDOW TREATMENTS & SHADING**

* Motorized blinds & shades (blackout, solar, privacy)
* Smart curtains (track-mounted, rod-mounted)
* Window actuators (skylight/greenhouse venting)
* Electrochromic/smart glass (tint control, privacy)
* Awnings (retractable, sun/wind-linked)

---

### **I) PERSONAL & WELLNESS**

**Health Monitoring**
* Smart scales (body composition, multi-user)
* Blood pressure monitors (Bluetooth-connected)
* Glucometers (diabetes management)
* Pulse oximeters & heart rate monitors
* Sleep trackers (mattress sensors, wearables)
* Medication dispensers (scheduled, adherence tracking)
* Fall detection wearables (elderly care)
* Telehealth kiosks (remote vitals, video consult)

**Pet Care**
* Smart feeders (scheduled, portion control)
* Pet doors (RFID/collar-triggered, app-controlled)
* Litter boxes (self-cleaning, waste level)
* Pet trackers (GPS, geofencing, activity)
* Aquarium controllers (temp, pH, auto-feeders, lighting)

---

### **J) OFFICE & WORKSPACE (Enterprise)**

**Desk & Meeting Rooms**
* Desk occupancy sensors (hot-desking, booking)
* Meeting room displays (scheduling, check-in/out)
* Conference equipment (cameras, mics, codecs, wireless presentation)
* Smart whiteboards & displays (interactive, annotation)
* Desk power/data hubs (PoE, USB-C, metered outlets)

**Queue & Space Management**
* People-counting sensors (entry/exit, retail traffic)
* Queue management displays (wait times, ticket systems)
* Occupancy heatmaps (utilization analytics)
* Wayfinding kiosks & digital signage

---

### **K) RETAIL & HOSPITALITY (Commercial)**

**Point-of-Sale & Inventory**
* POS terminals & payment kiosks (integrated sensors)
* Shelf sensors (weight, RFID, out-of-stock alerts)
* Electronic shelf labels (dynamic pricing)
* Inventory robots (autonomous scanning)
* Vending machines (cashless, inventory, refrigeration)
* Self-checkout stations (scale, scanner, payment)

**Customer Experience**
* Beacon networks (proximity marketing, wayfinding)
* Digital signage (menu boards, promotions, info displays)
* Interactive mirrors (fitting rooms, product info)
* Customer feedback kiosks (satisfaction surveys)

**Hospitality Specific**
* Room automation (lighting, HVAC, curtains via keycard)
* Mini-bar sensors (RFID, weight-based consumption tracking)
* Towel/linen RFID (inventory, loss prevention)
* Hotel safes (audit trail, remote unlock)
* Laundry chutes (RFID-tagged linen tracking)

---

### **L) HEALTHCARE (Clinical & Senior Living)**

**Patient Monitoring**
* Bed sensors (occupancy, fall prevention, pressure mapping)
* Nurse call systems (pull cords, wireless buttons, voice)
* Wandering prevention (door alarms, wristbands, geofencing)
* Vital sign monitors (networked bedside, wearables)
* Infusion pumps (IV tracking, alerts)
* Oxygen concentrators & ventilators (telemetry)

**Equipment & Facility**
* Medical equipment tracking (RFID, BLE tags on wheelchairs, pumps, carts)
* Medication cabinets (automated dispensing, access control)
* Refrigerator/freezer alarms (vaccine storage, lab samples)
* Sterilization equipment (autoclave cycle tracking)
* Hand-hygiene monitors (compliance tracking)

---

### **M) INDUSTRIAL & MANUFACTURING (OT/IIoT)**

**Process & Control**
* Modbus RTU/TCP sensors & actuators (PLCs, RTUs, field devices)
* BACnet MSTP/IP controllers (building automation)
* OPC UA servers (machine data, historian)
* SCADA endpoints (process visualization, alarming)
* Analog sensors (4-20mA, 0-10V) via I/O modules
* Fieldbus devices (Profibus, DeviceNet, CANopen, EtherCAT)

**Machine & Asset Health**
* Vibration sensors (predictive maintenance)
* Temperature probes (bearing, motor, fluid temps)
* Current/power sensors (motor load, anomaly detection)
* Oil quality sensors (contamination, viscosity)
* Belt tension & alignment sensors

**Facility Equipment**
* Elevators (monitoring, predictive maintenance, emergency comms)
* Escalators & moving walkways
* HVAC air handlers (AHUs, VAVs, FCUs)
* Boilers & chillers (efficiency, safety interlocks)
* Cooling towers (water treatment, fan control)
* Compressed air systems (leaks, pressure, dew point)
* Dock doors & levelers (position, safety sensors)

---

### **N) AGRICULTURE & OUTDOOR**

**Crop Management**
* Soil moisture sensors (tensiometers, capacitance)
* Soil pH, NPK, EC sensors
* Weather stations (temp, humidity, wind, rain, solar radiation)
* Leaf wetness & canopy temperature sensors
* Crop cameras (growth monitoring, pest detection)
* Automated irrigation valves & drip systems

**Livestock & Aquaculture**
* Animal tracking (GPS collars, ear tags, pedometers)
* Feeding systems (scheduled, automated)
* Water trough sensors (level, flow, quality)
* Barn climate control (ventilation, heating, humidity)
* Egg counters & graders (poultry)
* Milk parlor automation (yield tracking, cow ID)
* Aquaculture monitors (DO, pH, temp, salinity, feeders)

**Greenhouse & Controlled Environment**
* Grow lights (spectrum control, PAR sensors)
* COâ‚‚ injection systems
* Automated venting & shade curtains
* Hydroponic/aeroponic controllers (pH, EC, pumps)
* Vertical farming racks (multi-zone climate)

---

### **O) TRANSPORTATION & PARKING**

**Parking Management**
* Parking space sensors (ultrasonic, magnetic, camera-based)
* Parking guidance displays (available spaces, wayfinding)
* Payment kiosks & meters
* License plate recognition gates
* Barrier arms & bollards (automated access control)

**Fleet & Vehicles**
* GPS trackers (vehicles, trailers, equipment)
* Telematics (diagnostics, driver behavior, fuel)
* Dashcams (forward/rear, cabin, AI event detection)
* Tire pressure & temperature sensors
* Asset immobilizers (anti-theft)
* Forklift safety systems (collision avoidance, operator ID)

---

### **P) SMART CITY & PUBLIC INFRASTRUCTURE**

**Traffic & Mobility**
* Traffic signals (adaptive, connected-vehicle ready)
* Pedestrian crossing buttons & countdown timers
* Speed sensors & feedback signs
* V2X roadside units (vehicle-to-infrastructure)
* Bus/transit tracking (GPS, arrival prediction)
* Bike-share & scooter docks (locking, battery, GPS)
* Toll collection (ETC, license plate, RFID)

**Public Safety**
* Gunshot detection (acoustic triangulation)
* Emergency call boxes (SOS, video/audio)
* First-responder mesh networks (disaster comms)
* Street cameras (surveillance, traffic, analytics)
* Smart streetlights (dimming, motion-activation, wireless backhaul)

**Environment & Utilities**
* Air quality stations (city-wide monitoring networks)
* Noise monitoring (acoustic pollution tracking)
* Weather stations (hyperlocal micro-climate)
* Flood sensors (rivers, storm drains, low-lying areas)
* Earthquake/seismic sensors (early warning)
* Smart waste bins (fill-level, compaction, route optimization)
* Manhole covers (intrusion, gas, water ingress)
* Bridge & infrastructure health (strain gauges, accelerometers, corrosion)

**Lighting & Power**
* Smart streetlights (LED, adaptive dimming, outage detection)
* Decorative/festival lighting (DMX/RGB control)
* Public charging stations (EV, e-bike, USB)
* Solar benches & kiosks (off-grid power)

**Public Amenities**
* Smart benches (charging, WiFi, environmental sensors)
* Public WiFi access points (mesh, captive portal)
* Digital kiosks (wayfinding, tourism info, transit schedules)
* Park sensors (trail counters, restroom occupancy, field usage)
* Public fountain controllers (scheduled, water quality)

---

### **Q) EDGE COMPUTE & GATEWAYS**

**Home Edge**
* OpenWRT router (Thread/802.15.4 radio, BLE, VPN gateway)
* PoE switch (managed, 8â€“48 ports, VLAN-capable)
* Thread border router (USB dongle or standalone)
* Zigbee/Z-Wave coordinator
* BLE gateway (beacon scanning, presence detection)

**Enterprise Edge**
* K3s cluster (3+ nodes: NUCs, ARM servers, or rackmount)
* MQTT broker (Mosquitto, EMQX, VerneMQ in HA mode)
* LoRaWAN gateway (8-channel, GPS, backhaul via LTE/fiber)
* BACnet/Modbus protocol gateway (RTU-to-IP, MSTP-to-IP)
* OPC UA gateway (OT/IT bridge)
* OCPP server (EV charge management)
* Video analytics appliance (GPU-accelerated edge AI)
* Time-series database appliance (VictoriaMetrics, InfluxDB)

**Smart City / ISP Edge**
* Fiber aggregation switches (10/25/40GbE uplinks)
* BATMAN-adv / LibreMesh mesh nodes (802.11s, TDMA)
* 5G small cells & private LTE
* LoRaWAN network server (ChirpStack, TTN)
* Edge AI inference servers (NVIDIA Jetson, Coral, Hailo)

---

### **R) SPECIALTY & NICHE**

**Museum & Galleries**
* Vibration sensors (artwork protection)
* UV light sensors (conservation)
* Proximity alarms (theft prevention)
* Climate control (precise temp/humidity for artifacts)

**Data Centers**
* Hot/cold aisle temp sensors (thermal mapping)
* CRAC/CRAH unit monitoring (computer room AC)
* Leak detection cables (under raised floors)
* Rack environmental sensors (per-rack or per-U)
* PDU monitoring (per-outlet power, current imbalance)
* Door access & biometrics (cage/cabinet security)

**Labs & Clean Rooms**
* Differential pressure sensors (room containment)
* Particle counters (ISO cleanliness class)
* Fume hood face-velocity monitors
* Autoclave cycle validation
* Freezer/incubator alarms (sample integrity)
* Chemical inventory (RFID, hazmat tracking)

**Entertainment Venues**
* Stage lighting (DMX, Art-Net, sACN)
* Fog/haze machines (atmospheric effects)
* Pyrotechnics controllers (safety interlocked)
* Sound reinforcement (networked DSPs, amps)
* Projection mapping (multi-projector sync)
* Seat occupancy (event analytics, no-shows)

---

## Device Count Summary (Rough Estimate)

* **Home/Residential:** 50â€“200+ devices (single-family)
* **Enterprise/Campus:** 500â€“50,000+ devices (depends on size)
* **Smart City/District:** 10,000â€“1,000,000+ devices (sensors, streetlights, kiosks, transit)

---

## Next-Level Catalog Management

To keep this manageable at scale, you'll want:

1. **Device Registry / CMDB:** Auto-discovery + manual enrollment; lifecycle tracking (install, warranty, EOL).
2. **Taxonomy / SKU Database:** Vendor, model, protocol(s), power requirements, mounting, certifications.
3. **Templates & Profiles:** Pre-configured twin YAML + OPA policies per device class.
4. **Procurement & Spares:** Track inventory, lead times, compatibility (avoid vendor lock-in).
5. **Interop Testing:** Lab environment to validate new devices before production deployment.

---

### Want me to create:
1. **A searchable device matrix** (protocol/power/mounting/environment by device type)?
2. **Deployment guides** for specific verticals (healthcare, retail, agriculture)?
3. **A device onboarding checklist** (certs, VLAN assignment, twin creation, policy binding)?