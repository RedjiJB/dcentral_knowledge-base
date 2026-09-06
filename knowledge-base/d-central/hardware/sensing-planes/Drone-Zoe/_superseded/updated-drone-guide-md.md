---
source_project: Drone Zoe
source_project_uuid: 0197e6d0-e935-724d-8916-5cbbdf9646ab
doc_uuid: 7b6a018e-3cbe-4afd-b4b7-00b4f1e43f94
original_filename: updated_drone_guide.md
created_at: 2025-07-07T21:36:14.580266+00:00
content_hash: 2919590a8dd8
status: superseded
superseded_by: "updated-drone-guide-md-1780e328.md [unresolved during reconciliation -- old path, target not found in new tree]"
supersession_reason: Same title re-uploaded 6 weeks later, near-identical size (22234 vs 22228 chars).
---

# Haiti Drone Cooperative: Open Source Modular Sensor Platform System - Updated

## 1. COMPLETE DRONE PLATFORM MATRIX WITH OPEN SOURCE OPTIONS

### **TIER 1: MICRO DRONES (50-250g)**

#### **Platform A1: "SkyMite" - Indoor/Confined Space Specialist**
**Size**: 90mm diagonal, <250g | **Flight Time**: 8-12 minutes | **Range**: 500m-1km

**Open Source Platform Options:**

**Option 1: Crazyflie 2.1 Based**
- **Source**: [Bitcraze Crazyflie](https://www.bitcraze.io/) - Fully open source hardware & software
- **GitHub**: https://github.com/bitcraze/crazyflie-firmware
- **Specs**: 27g, 7min flight time, STM32F405 processor, 10-DOF sensors
- **Cost**: $180 (complete kit with radio)
- **Advantages**: Professional development platform, extensive documentation, modular expansion decks
- **Community**: Active development community, educational support

**Option 2: OpenRC Quadcopter**
- **Source**: [Daniel Norée's OpenRC Project](https://github.com/openrc)
- **Thingiverse**: https://www.thingiverse.com/thing:793425
- **Description**: 3D printed 450mm frame, designed for DJI 450 Flamewheel electronics
- **Cost**: ~$15 for 3D printed frame + electronics
- **Advantages**: Completely 3D printable, modular design, enclosed electronics

**Option 3: Hovership 3DFLY Micro**
- **Source**: Community designed micro drone frame
- **Thingiverse**: Multiple variants available
- **Specs**: <100g, 100x100mm print bed requirement
- **Cost**: ~$10 frame + $50 electronics
- **Advantages**: Ultra-compact, beginner-friendly

**Option 4: TinyTina 90mm Frame**
- **Source**: Open source mini drone design
- **Specs**: 90mm frame, 1S/2S compatible
- **Cost**: ~$300 complete build
- **Applications**: Indoor/outdoor flying, FPV capable

---

#### **Platform A2: "NanoSpy" - Ultra-Micro Surveillance**
**Size**: 65mm diagonal, <100g | **Flight Time**: 5-8 minutes | **Range**: 200-500m

**Open Source Platform Options:**

**Option 1: Modified Crazyflie Nano**
- **Base**: Crazyflie 2.1 with custom 65mm frame
- **Modifications**: 3D printed micro frame, same electronics
- **Advantages**: Proven flight control, programmable

**Option 2: Tiny Whoop Style DIY**
- **Frame**: 3D printed 65mm brushless frame
- **Electronics**: F4 flight controller, 1S setup
- **GitHub**: Multiple community designs available
- **Cost**: ~$80 complete

---

### **TIER 2: SMALL DRONES (250g-2kg)**

#### **Platform B1: "UrbanHawk" - City Operations Quadcopter**
**Size**: 159×202×55mm, 580g | **Flight Time**: 25-31 minutes | **Range**: 6-10km

**Open Source Platform Options:**

**Option 1: TBS Source One V5**
- **Source**: [Team BlackSheep Open Source](https://github.com/tbs-trappy/source_one)
- **Type**: 5" freestyle/racing frame, X configuration
- **License**: GPL v3, fully open source
- **Frame Cost**: $45-65
- **Advantages**: Wide community support, proven design, multiple size variants
- **GitHub**: Active development, 3D printable accessories
- **Build Guide**: https://oscarliang.com/how-to-build-fpv-drone/

**Option 2: T4 Quadcopter (Brendan22)**
- **Source**: [Thingiverse](https://www.thingiverse.com/thing:32281)
- **Type**: Completely 3D printable quadcopter
- **Features**: No supports required, modular design, GoPro mount
- **Cost**: ~$20 frame + electronics
- **Community**: 51+ makes, 37+ remixes

**Option 3: Crossfire 2**
- **Source**: 3D printed large quadcopter design
- **Features**: Huge frame, fully 3D printable
- **Applications**: Heavy payload, long range

**Option 4: AESIR II Frame**
- **Source**: Modular 3D printed + carbon fiber hybrid
- **Year**: 2021 design
- **Features**: Customizable, professional grade

---

#### **Platform B2: "RangerWing" - Fixed Wing Patrol**
**Size**: 1340mm wingspan, 1.2kg | **Flight Time**: 60-90 minutes | **Range**: 30-50km

**Open Source Platform Options:**

**Option 1: Flightory Pico Talon**
- **Source**: [Flightory](https://flightory.com/product/pico-talon/) - 3D printed FPV wing design
- **Type**: Small FPV wing, compact UAV platform
- **Weight**: 300-400g estimated
- **Features**: ArduPilot compatible, FPV optimized, customizable nose sections
- **Applications**: Short-range surveillance, training platform, urban operations
- **Community**: Active modifications on Cults3D, custom nose designs available
- **Cost**: $12.99 design files + ~$100 electronics

**Option 2: Flightory Mini Plank**
- **Source**: [Flightory](https://flightory.com/product/mini-plank/) - Compact FPV wing
- **Type**: Ultra-efficient flying wing design
- **Features**: Long-range tested, highly customizable, stable flight characteristics
- **Applications**: Extended patrol missions, efficiency-focused operations
- **Weight Range**: 800-1500g
- **Cost**: $22.99 design files + electronics

**Option 3: FOS UAV Platform**
- **Source**: [GitHub - FOS_UAV](https://github.com/rahulsarchive/FOS_UAV)
- **Developer**: ICFOSS (International Center for Free and Open Source Software)
- **Base**: ArduPlane compatible fixed-wing platform
- **Features**: Aerial reconnaissance and mapping, modular payload bay
- **Documentation**: Complete build guide, flight testing results
- **Applications**: Surveillance, mapping, long-range patrol

**Option 4: ArduPlane Compatible Platforms**
- **Software**: [ArduPilot Plane](https://ardupilot.org/plane/)
- **GitHub**: https://github.com/ArduPilot/ardupilot
- **Airframes**: 
  - Modified Bixler variants
  - Skywalker X8 clones
  - EPO foam + carbon rod construction
- **Community**: Large global development community
- **Features**: Full autonomous capability, mission planning

**Option 5: HAWk Modular RC Wing**
- **Source**: 3D printed LW-PLA pusher/puller wing
- **Size**: 1m+ wingspan
- **Year**: 2023 design
- **Features**: Complete BOM + manual documentation

**Option 6: CNR-IRPI-GMG-T1 Style**
- **Source**: Open source fixed-wing UAV design
- **Features**: BVLOS capabilities, modular payload system
- **Applications**: Geohazards monitoring, surveying
- **Base**: V-tail configuration, high-wing design

---

#### **Platform B3: "StealthQuad" - Covert Operations**
**Size**: 220mm diagonal, 850g | **Flight Time**: 35-45 minutes | **Range**: 8-12km

**Open Source Platform Options:**

**Option 1: TBS Source V**
- **Source**: Team BlackSheep ultra-stiff design
- **Features**: Optimized for stealth operations, noise dampening
- **Frame**: Carbon fiber, minimal radar signature

**Option 2: Custom Stealth Frame**
- **Base**: Modified racing frame design
- **Features**: Noise-dampened propellers, dark coating
- **Electronics**: Encrypted communications, low EMI

---

### **TIER 3: MEDIUM DRONES (2-10kg)**

#### **Platform C1: "EnforcerQuad" - Security Specialist**
**Size**: 900mm diagonal, 6.5kg | **Flight Time**: 15-25 minutes | **Range**: 5-8km

**Open Source Platform Options:**

**Option 1: S1000+ Open Source Clone**
- **Base**: DJI S1000+ inspired open source design
- **Frame**: Carbon fiber monocoque, 6-arm configuration
- **GitHub**: Multiple community variants available
- **Features**: Heavy payload capability, modular arms

**Option 2: DIY Heavy Lift Hexacopter**
- **Source**: Community designed heavy lift platform
- **Construction**: Carbon fiber arms + aluminum center plate
- **Payload**: 2-3kg capacity
- **Applications**: Security surveillance, equipment transport

---

#### **Platform C2: "SurveillanceWing" - Long Endurance Fixed Wing**
**Size**: 2120mm wingspan, 4.2kg | **Flight Time**: 3-5 hours | **Range**: 100-200km

**Open Source Platform Options:**

**Option 1: Flightory Stallion**
- **Source**: [Flightory](https://flightory.com/product/stallion/) - 3D printed fixed-wing UAV
- **Type**: Medium fixed-wing platform optimized for performance and versatility
- **Weight Range**: 1500-3000g estimated
- **Features**: ArduPilot compatible, professional applications, autonomous flight capable
- **Applications**: Long-range surveillance, mapping, reconnaissance missions
- **Cost**: $39.99 design files + electronics (~$400-600 total)

**Option 2: Flightory Stork**
- **Source**: [Flightory](https://flightory.com/product/stork/) - Push-prop V-tail design
- **Wingspan**: 1600mm
- **Type**: Classic layout with pusher propeller and V-tail configuration
- **Weight Range**: 1500-2800g 
- **Features**: Very spacious fuselage, accommodates large battery, stable flight characteristics
- **Applications**: Long-range FPV flights, LOS flights, surveying missions
- **Cruise Speed**: 50-60 km/h optimal
- **Build**: LW-PLA construction + regular PLA reinforcements
- **Cost**: $34.99 design files + electronics

**Option 3: Flightory Super Stingray**
- **Source**: [Flightory](https://flightory.com/product/superstingray/) - High-performance fixed-wing
- **Type**: Advanced fixed-wing UAV for demanding applications
- **Weight Range**: 1500-3300g estimated
- **Features**: Optimized aerodynamics, FPV capable, professional grade design
- **Applications**: Advanced surveillance, long-range missions
- **Cost**: $29.99 design files + electronics

**Option 4: Flightory Super Stingray VTOL**
- **Source**: [Flightory](https://flightory.com/product/super-stingray-vtol/) - VTOL variant
- **Type**: 3D printed VTOL aircraft with vertical takeoff/landing capability
- **Features**: FPV optimized, challenging takeoff/landing conditions capable
- **Applications**: Urban operations, confined space missions, versatile deployment
- **Advantages**: No runway required, hover capability + fixed-wing efficiency
- **Weight Range**: 2000-4500g estimated
- **Cost**: $34.99 design files + VTOL electronics

**Option 5: Extended FOS UAV Platform**
- **Base**: Scaled up FOS UAV design
- **Modifications**: Larger wingspan, extended fuel capacity
- **Features**: Long endurance surveillance, communications relay

**Option 6: ArduPlane Long Range Platform**
- **Base**: Custom EPO foam + carbon construction
- **Software**: ArduPilot with advanced mission planning
- **Features**: RTK GPS, redundant systems, BVLOS capability

---

#### **Platform C3: "GuardianHex" - Multi-Mission Platform**
**Size**: 1200mm diagonal, 8.5kg | **Flight Time**: 45-65 minutes | **Range**: 15-25km

**Open Source Platform Options:**

**Option 1: Y-Octocopter Design**
- **Source**: [CNC-Step Y-Octocopter](https://www.cnc-step.com/modelbuilding-multicopter-quadrocopter-hexacopter/)
- **Features**: Y-configuration, 8 motors, aluminum construction
- **Weight**: 700g frame only
- **Advantages**: More space on center plate, modular design

**Option 2: Custom Hexacopter Platform**
- **Construction**: Carbon fiber + aluminum hybrid
- **Configuration**: Coaxial or traditional hex
- **Features**: Modular payload bay, redundant systems

---

### **TIER 4: HEAVY-LIFT DRONES (10-25kg)**

#### **Platform D1: "CargoLifter" - Heavy Transport Octocopter**
**Size**: 1500mm diagonal, 18kg | **Flight Time**: 20-35 minutes | **Range**: 10-15km

**Open Source Platform Options:**

**Option 1: DIY Y-Octocopter (Ultralight Design)**
- **Source**: Austrian CNC-Step design methodology
- **Construction**: CNC milled aluminum components
- **Weight**: 700g frame for 8-motor configuration
- **Features**: Y-configuration for maximum payload space
- **Build Guide**: Complete CAD files and milling instructions

**Option 2: PVC Octocopter Frame**
- **Source**: [Instructables PVC Design](https://www.instructables.com/PVC-Octocopter-Drone-Frame/)
- **Materials**: PVC pipe + 3D printed connectors
- **Size**: 1100mm motor-to-motor spacing
- **Advantages**: Low cost, field repairable, modular arms
- **Payload**: Designed for DSLR cameras + gimbals
- **Cost**: <$100 frame construction

**Option 3: Modular Heavy Lift Platform**
- **Design**: Open source heavy lift frame
- **Features**: Folding arms, quick assembly, transport friendly
- **Construction**: Carbon fiber + aluminum joints
- **Applications**: Cargo delivery, emergency supply drops

**Option 4: ASW HLM Style Open Source**
- **Base**: Heavy Lift Multirotor design principles
- **Features**: Modular arms, high accessibility components
- **Software**: ArduCopter flight stack compatible
- **Payload**: 30+ kg capacity possible

---

#### **Platform D2: "SkySentinel" - Command & Control Platform**
**Size**: 1800mm diagonal, 22kg | **Flight Time**: 60-90 minutes | **Range**: 30-50km

**Open Source Platform Options:**

**Option 1: Extended Y-Octocopter**
- **Base**: Scaled Y-Octocopter design
- **Features**: Extended flight time, command & control systems
- **Payload**: Multiple sensor packages, communications equipment

**Option 2: Coaxial Octocopter Design**
- **Configuration**: X8 coaxial setup
- **Advantages**: Compact footprint, high redundancy
- **Applications**: Command center, communications relay

---

## 2. OPEN SOURCE DEVELOPMENT RESOURCES

### **Flightory Integration - Professional 3D Printed Aircraft**

**Flightory** is a forward-thinking project dedicated to providing accessible unmanned aerial vehicle platforms. They specialize in a diverse range of fixed-wing drone projects with a mission to enhance the capabilities of small UAVs, ensuring they are accessible, cost-effective, and globally available.

**Key Flightory Advantages:**
- **ArduPilot Compatible**: All airplanes are designed to accommodate a flight controller and other components that allow for autonomous flight. They recommend ArduPilot firmware.
- **Professional Design**: Diligent design approach that prioritizes aerodynamic optimization and real-flight testing
- **Customization Ready**: Files provided in STL format, with some files also provided in STEP to facilitate editing and customization for different cameras, antennas, sensors, etc.
- **Community Support**: Active Tech Group on Facebook where users share experiences and experiment with Flightory platforms

**Flightory Platform Summary:**

| Platform | Type | Weight Range | Applications | Cost |
|----------|------|--------------|-------------|------|
| **Pico Talon** | Small FPV Wing | 300-400g | Training, urban ops | $12.99 + electronics |
| **Mini Plank** | Compact Wing | 800-1500g | Efficient patrol | $22.99 + electronics |
| **Stallion** | Medium UAV | 1500-3000g | Professional missions | $39.99 + electronics |
| **Super Stingray** | Advanced Fixed-Wing | 1500-3300g | Surveillance | $29.99 + electronics |
| **Super Stingray VTOL** | VTOL Aircraft | 2000-4500g | Urban/confined ops | $34.99 + electronics |
| **Stork** | Long-Range Platform | 1500-2800g | Extended missions | $34.99 + electronics |

### **Primary Development Platforms**

**Flight Control Software:**
1. **ArduPilot/ArduCopter**
   - GitHub: https://github.com/ArduPilot/ardupilot
   - License: GPL v3
   - Supports: All aircraft types
   - Community: 10+ years active development

2. **PX4 Autopilot**
   - GitHub: https://github.com/PX4/PX4-Autopilot
   - License: BSD 3-Clause
   - Features: Advanced VTOL support
   - Backed by: Dronecode Foundation

3. **Betaflight** (Racing/FPV focus)
   - GitHub: https://github.com/betaflight/betaflight
   - Applications: Racing, acrobatic flight
   - Features: High performance, low latency

4. **iNAV** (Navigation focus)
   - GitHub: https://github.com/iNavFlight/inav
   - Features: Advanced GPS modes, fixed-wing support
   - Applications: Long range, autonomous flight

### **Frame Design Resources**

**3D Printing Repositories:**
- **Thingiverse**: 100+ open source drone designs
- **Cults3D**: Premium 3D printed drone collection
- **GitHub**: Source files for major open source projects
- **GrabCAD**: CAD files for professional designs

**Key Design Communities:**
- **OpenRC Project**: Radio controlled vehicle designs
- **DIY Drones**: Historical community with extensive archives
- **Team BlackSheep**: Open source FPV frame project leader
- **ArduPilot Community**: Flight control and airframe development

### **Hardware Standards**

**Flight Controller Compatibility:**
- **30.5×30.5mm**: Standard for 5"+ quadcopters
- **20×20mm**: Micro/mini quadcopter standard
- **UAVCAN**: Open communication protocol
- **MAVLink**: Standard telemetry protocol

**Frame Materials:**
- **3D Printing**: PLA, PETG, TPU, Carbon fiber filled
- **Carbon Fiber**: Professional grade, high strength
- **Aluminum**: CNC machined, cost effective
- **Hybrid**: 3D printed + carbon/aluminum components

---

## 3. IMPLEMENTATION ROADMAP FOR HAITI - Updated with Flightory Integration

### **Phase 1: Micro Platform + Flightory Entry (Months 1-3)**
**Target**: SkyMite, NanoSpy + Flightory Pico Talon
**Open Source Base**: Crazyflie 2.1 + Flightory entry-level designs
**Investment**: $8,000 for development setup + Flightory licensing
**Deliverables**: 
- 10x functional micro drones
- 5x Pico Talon fixed-wing trainers
- Training materials in Kreyòl
- Local 3D printing setup for Flightory designs

### **Phase 2: Small Platform + Flightory Expansion (Months 4-8)**
**Target**: UrbanHawk, RangerWing + Full Flightory Small Aircraft Line
**Open Source Base**: TBS Source One + Flightory Mini Plank, Pico Talon
**Investment**: $20,000 for expanded capabilities + Flightory platform integration
**Deliverables**:
- 20x small drones across configurations
- 15x Flightory small fixed-wing aircraft
- Flight training program with fixed-wing specialization
- Basic sensor integration for both multirotor and fixed-wing

### **Phase 3: Medium Platform + Flightory Professional (Months 9-15)**
**Target**: EnforcerQuad, SurveillanceWing + Flightory Stallion, Stork, Super Stingray
**Open Source Base**: Custom heavy lift + Flightory professional aircraft
**Investment**: $40,000 for professional capabilities + VTOL development
**Deliverables**:
- 10x medium drones
- 10x Flightory professional aircraft (including VTOL)
- Advanced sensor packages for both platforms
- Mission planning software for autonomous operations

### **Phase 4: Heavy Platform + Flightory VTOL Mastery (Months 16-24)**
**Target**: CargoLifter, SkySentinel + Advanced Flightory Applications
**Open Source Base**: Y-Octocopter + Flightory Super Stingray VTOL
**Investment**: $60,000 for full capability + VTOL specialization
**Deliverables**:
- 5x heavy lift platforms
- 5x advanced VTOL aircraft
- Complete mission capability across all aircraft types
- Training and certification program for all platforms

### **Phase 5: Regional Hub + Flightory Distribution (Months 25-36)**
**Target**: Caribbean market expansion + Flightory design licensing
**Investment**: $100,000 for regional operations
**Deliverables**:
- Regional distribution center for Flightory designs
- Custom modification services for Flightory platforms
- Training centers in Jamaica, Dominican Republic, Puerto Rico
- Haiti as Flightory's Caribbean development hub

### **Manufacturing Strategy**

**Local Production Capabilities:**
- **3D Printing Farm**: 10+ printers for frame production
- **Electronics Assembly**: Partner with technical schools
- **Testing Facility**: Flight test and validation center
- **Training Center**: Pilot and technician certification

**Quality Assurance:**
- **Environmental Testing**: IP65 rating compliance
- **Flight Testing**: Comprehensive performance validation
- **Documentation**: Complete maintenance and operation manuals
- **Certification**: Compliance with Haiti aviation regulations

**Supply Chain Localization:**
- **Haiti Sources**: 3D printing materials, basic electronics
- **Regional Sources**: Motors, sensors, specialized components
- **International Sources**: Flight controllers, advanced sensors
- **Emergency Stock**: Critical spare parts inventory

---

## 4. COST ANALYSIS BY PLATFORM

### **Development Costs (One-time)**

| Platform Tier | Open Source Development | Local Manufacturing Setup | Training Materials | Total Investment |
|---------------|------------------------|---------------------------|-------------------|------------------|
| Micro (A1, A2) | $2,000 | $3,000 | $1,000 | $6,000 |
| Small (B1, B2, B3) | $5,000 | $8,000 | $2,000 | $15,000 |
| Medium (C1, C2, C3) | $8,000 | $15,000 | $5,000 | $28,000 |
| Heavy (D1, D2) | $15,000 | $25,000 | $8,000 | $48,000 |
| **TOTAL** | **$30,000** | **$51,000** | **$16,000** | **$97,000** |

### **Production Costs (Per Unit) - Updated with Flightory Integration**

| Platform | Open Source Cost | Flightory Option | Proprietary Equivalent | Savings | Local Content |
|----------|------------------|------------------|----------------------|---------|---------------|
| SkyMite | $390 | N/A (multirotor only) | $799 (DJI Tello+) | 51% | 40% |
| RangerWing | $1,778 | $113 (Pico Talon) / $123 (Mini Plank) | $4,999 (Parrot Disco Pro) | 94% / 98% | 80% / 85% |
| SurveillanceWing | $2,910 | $440 (Stallion) / $435 (Stork) / $430 (Super Stingray) | $16,000+ (Quantum Trinity) | 97% / 97% / 97% | 75% / 75% / 75% |
| UrbanHawk | $1,208 | N/A (fixed-wing only) | $2,499 (DJI Mini Pro) | 52% | 35% |
| EnforcerQuad | $4,085 | N/A (fixed-wing only) | $8,999 (DJI Matrice 300) | 55% | 25% |
| CargoLifter | $7,700 | N/A (fixed-wing only) | $24,999 (Heavy lift commercial) | 69% | 20% |

**Flightory Cost Advantages:**
- **Ultra-Low Entry Cost**: $13-40 for design files vs $400-16,000 for proprietary alternatives
- **94-98% Cost Savings**: Dramatic reduction in platform costs for fixed-wing aircraft
- **High Local Content**: 75-85% of Flightory builds can be manufactured locally in Haiti
- **Customization Freedom**: STEP files allow unlimited modifications without licensing restrictions
- **No Vendor Lock-in**: Complete design ownership and community support

**Updated Revenue Projections (Annual):**
- **Year 1**: $100,000 (micro/small platforms + Flightory integration)
- **Year 2**: $300,000 (all platforms operational + Flightory export)
- **Year 3**: $500,000 (full production + regional Flightory hub)
- **Year 4**: $750,000 (Caribbean market expansion)

This comprehensive open source approach enables Haiti Drone Cooperative to build world-class capabilities using affordable, locally-manufacturable components while maintaining complete technological independence and unlimited customization potential.

<!-- AUTO-GENERATED RELATED START (scripts/build_obsidian_graph.py) -->

## Related (auto-generated)

**Superseded by:** updated-drone-guide-md-1780e328.md (unresolved path, see registry/materialized-manifest.json)

<!-- AUTO-GENERATED RELATED END -->
