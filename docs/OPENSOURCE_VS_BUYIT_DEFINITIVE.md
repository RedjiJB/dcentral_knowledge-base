# 100% OPENSOURCE vs. MUST-BUY: Complete Breakdown
## What Can Be DIY, What Must Be Commercial, & Cheapest International Alternatives

**Last Updated:** September 2026 | **Classification:** Technical Specification

---

## PART 1: HARDWARE BREAKDOWN

### HARDWARE YOU CAN BUILD 100% OPEN-SOURCE (NO COMPROMISE)

#### ✓ 1. Environmental Monitoring & Telemetry (COMPLETE FREEDOM)

**Components:**
- Temperature sensors: Dallas DS18B20 (OneWire), PT100/PT1000 (RTD)
- Humidity: DHT22, BME680
- Pressure (differential, for room airflow): MPXV7002DP
- Microcontroller: ESP32 (costs $8–15)
- Firmware: ESPHome (Python-based, open-source)
- Message broker: Mosquitto (MQTT, open-source)
- Time-series DB: InfluxDB (open-source version available)
- Visualization: Grafana (open-source version)

**Open-Source Stack:**
```
ESPHome (firmware) 
  ↓ (publishes via MQTT)
Mosquitto (message broker)
  ↓ (subscribes and stores)
InfluxDB (time-series database)
  ↓ (REST API)
Grafana (dashboards)
```

**Regulatory Compliance:**
- ✓ ISO 17025 Cl. 6.3 requires environmental monitoring
- ✓ Each **physical sensor** needs annual NIST/NRC calibration certificate
- ✓ The **software** is fully auditable (open-source)
- ✓ Audit trails automatic (InfluxDB + Grafana logs all writes)

**Cost:**
- ESP32 + sensors + wiring: $100–300 per monitoring station
- Mosquitto + InfluxDB + Grafana: Free (self-hosted)
- NIST calibration per sensor: $150–300/year per probe
- **Total for 10 monitoring points:** $1,500–3,000 initial + $1,500–3,000/year for recalibration

**Auditor View:**
> "Show me calibration certificates for your temperature probes."  
> (You show NIST letter from accredited calibration lab)  
> ✓ PASS. "The firmware is open-source?" Yes. ✓ PASS. "Audit logs?" Yes, here. ✓ PASS.

---

#### ✓ 2. Precision Balances (Analytical & Top-Loading)

**Can be DIY?** Mostly no (load cell nonlinearity), but:
- **Buy commercial balances** (~$1,200–3,000)
- Calibrate annually with NIST-traceable calibration weights (~$200–300/year)
- Integrate weight readout via RS-232 or Modbus to LIMS

**Why not DIY:** Load cell calibration curves are highly nonlinear; achieving ±0.01 g accuracy requires factory calibration.

**Best approach:**
- Buy cheap international balance (Gram, Ooni, etc.) with RS-232
- Connect to Python script that logs weights to SENAITE
- Recalibrate annually with NIST weights

**Cost:** $1,500–2,000 (balance + weights + integration)

---

#### ✓ 3. Benchtop Centrifuges (Slow-Speed, ~5,000 rpm max)

**Can be DIY?** Theoretically yes, but:
- Need DC brushless motor (~$100–200)
- Stepper motor controller (Arduino-based, ~$50)
- Custom-machined aluminum rotor (CNC job, ~$500–1,500)
- Vibration damping (elastomeric mounts, ~$200)
- Encoder for RPM feedback (~$50)

**Problems with DIY:**
- Rotor imbalance causes vibration → cross-contamination
- Hard to achieve consistent RCF (relative centrifugal force)
- Cannot perform ISO 3930 balance validation (requires factory calibration)

**Realistic option:**
- **Buy low-cost centrifuge** (~$2,500–4,000 from Eppendorf, Hettich, or Chinese OEMs)
- Integrate tachometer feedback to log RPM
- Validate RCF annually

**Cost:** $3,000–5,000 (commercial unit + integration)

---

#### ✓ 4. Circulating Water Baths (±0.2°C Stability)

**Can be DIY?** Yes, with PID controller:

```python
# Arduino/ESP32 PID-controlled water bath
import machine
from machine import Pin, ADC
from simple_pid import PID

# Temperature sensor (DS18B20)
# Heating element (1500W submersible heater)
# Relay (to switch heater on/off)

target_temp = 42.0  # 42°C for Salmonella enrichment
pid = PID(Kp=10, Ki=0.5, Kd=2, setpoint=target_temp)

heater_relay = Pin(14, Pin.OUT)
temp_sensor = ADC(Pin(34))

while True:
    current_temp = read_ds18b20()
    
    # PID calculation
    control_signal = pid(current_temp)
    
    # Relay control (bang-bang or PWM)
    if control_signal > 0:
        heater_relay.on()
    else:
        heater_relay.off()
    
    # Log to LIMS
    send_to_mqtt(f"waterbath/temp/{current_temp}")
    time.sleep(10)
```

**Components:**
- Glass flask or stainless container (~$100–200)
- Submersible heater element (1500W, ~$30)
- DS18B20 temperature sensor (~$5)
- Relay module (SSR, ~$20)
- PID controller board (Arduino/ESP32, ~$20)
- Pump (optional, for circulation, ~$50)

**Auditor View:**
- ✓ "Show me temperature logs." (MQTT logs show ±0.1°C stability)
- ✓ "Is the sensor calibrated?" (Show NIST certificate)
- ✓ PASS

**Cost:** $400–700 for DIY; $2,000–3,500 for commercial  
**Verdict:** DIY is viable and saves 70%

---

#### ✓ 5. Microbiological Incubators (35°C, 41.5°C, 42°C, ±0.5°C tolerance)

**Can be DIY?** Yes, with solid engineering:

**Build a custom incubator:**
```
┌─────────────────────────────────────┐
│ Insulated Box (Styrofoam/polycarbonate)
│                                     │
│  ┌──────────────────────────────┐  │
│  │ Heating element (500W)       │  │
│  │ Thermostat (DS18B20 + PID)   │  │
│  │ Air circulation fan (24V DC) │  │
│  │ Temperature data logger      │  │
│  └──────────────────────────────┘  │
│                                     │
│  Dimensions: 50cm × 50cm × 40cm    │
└─────────────────────────────────────┘
```

**Components:**
- Polycarbonate or acrylic box: $150–300
- Heating element (500W immersion or ceramic): $40–100
- Thermostat IC (NTC thermistor 10kΩ or DS18B20): $5–20
- PID controller (Arduino-based): $30–80
- 24V DC power supply: $50–100
- Silicone seals and insulation: $100–200
- Optional: Humidity control (wet bulb method): $50

**Total DIY cost:** $425–800 per incubator

**Commercial equivalent:** $3,000–5,000

**Auditor View:**
- ✓ "Can you verify ±0.5°C accuracy?" (Show calibration log over 24 hours)
- ✓ "Sensor calibrated?" (Show NIST certificate)
- ✓ "Is the design documented?" (Show schematics + build notes)
- ✓ PASS

**Verdict:** DIY saves 75%, fully auditable, no regulatory barrier

**Build Reference:** See https://github.com/BiohackAcademy/BioCoder (open-source incubator designs)

---

#### ✓ 6. Automated Liquid Handling (Opentrons OT-2 / Flex)

**Already open-source:**
- Hardware schematics: GitHub (opentrons/opentrons)
- Firmware: Python-based, fully customizable
- Python Protocol API: Create any extraction/dilution workflow
- HTTP server: Interface with LIMS via REST

**Cost:**
- **OT-2:** $35,000–45,000 (purchase, not DIY—mechanical precision too high)
- **Custom extraction protocol:** You write it (free, open-source)

**Can you build an Opentrons alternative?**
- Theoretically: Open-source gantry system exists (OpenPnP, Jubilee)
- Practically: Mechanical tolerances (±0.5mm) for 96-well plates is hard
- **Better option:** Buy Opentrons OT-2 used (~$15k–25k), or buy compatible OEM

**Auditor View:**
- ✓ "Is the liquid handling validated?" (Show calibration data: aspirate/dispense accuracy)
- ✓ "Is the protocol documented?" (Show Python code)
- ✓ PASS

**Verdict:** Buy Opentrons (it's already open-source); write custom protocols (free)

---

#### ✓ 7. Real-Time qPCR for Food Testing (Chai Open qPCR)

**Can be open-source?** Yes, Chai exists:
- Hardware: Open schematics on GitHub
- Firmware: Python-based
- Cost: $3,000–5,000 (DIY kit from Chai, or build from schematics)
- Optical precision: Good enough for food testing (Ct ±0.5 acceptable)

**Limitations:**
- ✗ **NOT FDA-cleared** (research-grade)
- ✓ **IS ISO 17025 validatable** (if you do in-house LoD/LoQ studies)
- ✗ **NOT for clinical reporting** without LDT pathway ($20k–50k)

**Build option:**
```python
# Chai qPCR uses Python directly
from chai_openqpcr.thermal_cycler import QuantificationCycle

protocol = [
    QuantificationCycle(
        stage="exponential",
        fluor_channel="FAM",  # Salmonella stx gene
        hold_time=60,
        target_temp=60
    ),
    QuantificationCycle(
        stage="exponential",
        fluor_channel="VIC",  # E. coli eae gene
        hold_time=60,
        target_temp=58
    ),
]
```

**Cost:** $3,500–5,000 DIY vs. $12,000–18,000 commercial (Tianlong)

**Auditor View (Food Testing):**
- ✓ "Where are your LoD/LoQ validation studies?" (Show data for Salmonella, STEC, Norovirus)
- ✓ "Plate compatibility?" (Show 96-well plate validation)
- ✓ PASS (ISO 17025)

**Auditor View (Clinical):**
- ✗ "Is this FDA-cleared?" No. ✗ FAIL (cannot report clinical results)
- → Need LDT pathway or use FDA-cleared instrument

**Verdict:** Perfect for food testing; not suitable for clinical without LDT

---

#### ✓ 8. Automated Plate Washers & Readers (with caveats)

**Can you DIY a plate washer?**
- Theoretically: Solenoid valves + peristaltic pump + Arduino
- Problem: Uniform wash across 96 wells is mechanically hard
- Reality: DIY washers leak and fail QC

**Better option:**
- Buy used BioTek 405 TS (~$2,000–3,000 refurbished)
- Or buy cheap Chinese equivalent with CE mark (~$1,500–2,000)

**Plate Reader:**
- Can DIY: Fiber-coupled LEDs (wavelength filters) + CCD camera + Arduino
- Problem: Cannot achieve certified neutral density linearity (CLSI requirement)
- Reality: IO Rodeo spectrophotometer (~$2,000) is best DIY option; still not ELISA-grade

**Auditor View:**
- Refurbished BioTek: ✓ PASS (if calibration certificates current)
- DIY IO Rodeo: ⚠ PASS for food assays, ✗ FAIL for clinical ELISA

**Verdict:** Buy commercial (used is fine); DIY plate reader is research-only

---

### HARDWARE YOU CANNOT BUILD OPEN-SOURCE (MUST BUY)

#### ✗ 1. STEAM AUTOCLAVES (Pressure Vessels)

**Why impossible:**
- ASME Boiler & Pressure Vessel Code (§ VIII) is **federal law**
- Requires certified manufacturer stamp ("U" or "H")
- Insurance voids coverage on uncertified units
- Municipal building code violation

**What to buy instead:**

| Manufacturer | Model | Capacity | Certification | Price |
|---|---|---|---|---|
| **Gemmy (Taiwan)** | SA-Series 30L | 30L | ASME "U" stamp | $4,000–6,000 |
| **Zealway (China)** | GI54 Deluxe | 54L | ASME "U" + ISO 13485 | $5,000–7,500 |
| **Hirayama (Japan)** | HA-600IIIS | 600L | ASME "U" stamp | $8,000–12,000 |
| **Priorclave (UK)** | LG120 | 120L | ASME "U" + CE mark | $12,000–15,000 |

**Where to source:**
- **Direct from Taiwan/China manufacturers** (via Alibaba, Global Sources)
  - Gemmy: contact@gemmy.com.tw
  - Zealway: export@zealway.com
- **US/Canada distributor** (pays import duties but handles compliance)
  - Lab Alliance (distributor for Gemmy/Zealway/Hirayama)

**What to verify BEFORE buying:**
```
MANDATORY CHECKLIST:
☐ ASME "U" stamp (North America) OR PED 2014/68/EU (EU/Canada)
☐ ISO 13485 factory audit certificate
☐ Pressure vessel inspection certificate (hydrostatic test)
☐ Manual includes SOP for biological indicator validation
☐ Seller provides certificate of conformity (CoC)
☐ Optional: Seller pre-certifies for your jurisdiction
```

**Cost breakdown:**
- Equipment: $4,000–7,500
- Shipping + import duties (if applicable): $500–2,000
- Local pressure vessel inspection: $200–500
- Biological indicator test kit (annual): $100–200/year
- **Total first year:** $4,800–10,200

**Audit Trail:**
- ASME certificate: Kept on file
- Annual bio-indicator validation: Logged in LIMS
- Temperature/pressure charts: PDF archived

**Auditor view:**
- ✓ "Show pressure vessel certification." (ASME stamp photo)
- ✓ "Annual biological indicator results?" (FilePath: /audit/autoclave/bio_indicator_2026.pdf)
- ✓ PASS

---

#### ✗ 2. CLASS II BIOSAFETY CABINETS (NSF/ANSI 49 or EN 12469)

**Why impossible:**
- NSF International will **not certify DIY cabinets**
- Annual DOP/PAO aerosol smoke test is mandatory
- Third-party certifier's liability insurance excludes uncertified units
- Lab insurance voids coverage

**What to buy instead:**

| Manufacturer | Model | Width | Certification | Price |
|---|---|---|---|---|
| **Biobase (China)** | BSC-1100IIA2-X | 1.1m | NSF/ANSI 49 listed | $5,500–7,000 |
| **Esco Lifesciences (Singapore)** | A2 Series | 1.0m–1.5m | NSF/ANSI 49 listed | $7,000–10,000 |
| **Heal Force (China)** | HR1650-IIA2 | 1.65m | EN 12469 certified | $6,000–8,000 |
| **Labconco (USA)** | Purifier (used) | 1.2m | NSF/ANSI 49 | $3,000–5,000 refurbished |
| **Thermo Fisher (USA)** | Herasafe (used) | 1.2m | NSF/ANSI 49 | $2,500–4,500 refurbished |

**Sourcing strategy:**

**Option A: New international**
- Contact Biobase or Esco directly
- Request NSF certificate for specific model
- Verify model in NSF directory (nsf.org/certified-products)
- Cost: $5,000–8,000
- Shipping: 4–8 weeks

**Option B: Used North American (Safer bet)**
- LabX.com, EquipNet, Biosurplus (lab resale marketplaces)
- Buy certified Thermo/Baker/Labconco unit
- Cost: $2,500–5,000
- Install new HEPA filter (~$600) + field certification (~$800)
- Shipping: 1–2 weeks

**What to verify BEFORE buying:**
```
MANDATORY CHECKLIST:
☐ NSF/ANSI 49 certificate (or EN 12469 if EU/Canada)
☐ DOP test report (HEPA filter integrity)
☐ Airflow velocity certification (100 ft/min ±20%)
☐ Downflow/inflow balance sheet
☐ Certificate of Conformity (CoC)
☐ Pressure decay test (annual maintenance schedule)
```

**Cost breakdown:**
- Equipment: $3,000–8,000 (depending on new vs. used)
- Shipping + installation: $500–2,000
- HEPA filter replacement (if used): $400–800
- Annual field certification (DOP/PAO test): $700–1,200/year
- **Total first year:** $4,600–12,000

**Annual compliance:**
- DOP/PAO aerosol smoke test: $700–1,200
- Pressure decay test: $300–500
- Certification report: Filed in LIMS
- **Total/year:** $1,000–1,700

**Auditor view:**
- ✓ "Show NSF certification." (Certificate on wall)
- ✓ "Annual DOP/PAO results?" (Show report from certified contractor)
- ✓ PASS

---

#### ✗ 3. SYNDROMIC MULTIPLEX CARTRIDGES (for clinical diagnostics)

**Why impossible:**
- Patents (Cepheid, BioFire, Sansure): 200+ US/EU/CN patents
- Manufacturing: ±10 μm tolerance injection molding (DIY: ±200 μm best case)
- IVD clearance: FDA, Health Canada, CE mark required for clinical use

**What to buy instead:**

| Manufacturer | Device | Targets (count) | IVD Clearance | Price/Test | Unit Cost |
|---|---|---|---|---|---|
| **Sansure Biotech (China)** | iPonatic III POCT | 22-plex GI | CE-IVD | $25–35 | $8,000–12,000 |
| **Coyote Bioscience (China)** | Flash20 System | 20-plex GI | CE-IVD | $30–40 | $10,000–14,000 |
| **BioFire (USA, Meridian)** | FilmArray 2.0 | 22-plex GI | FDA 510k | $150–200 | $45,000 |
| **Cepheid (USA, Danaher)** | GeneXpert Xpress MTB/RIF | Tuberculosis | FDA 510k | $80–120 | $20,000+ |

**Why international is better:**
- Sansure/Coyote: CE-IVD approved (Europe, Canada); not FDA-cleared (US clinical use needs LDT)
- Cost: 70% cheaper than BioFire/Cepheid
- Consumables: $25–40/test vs. $150–200/test (FilmArray)

**Sourcing:**

**Option A: If you need CLINICAL reporting (US)**
- Must use FDA-cleared system (BioFire, GeneXpert, etc.)
- Cost: $45,000+ instrument + $100–200/test consumable
- Verify: FDA 510k clearance on FDA.gov (Device List)

**Option B: If you operate in Canada/EU (or do food testing)**
- Can use CE-IVD marked system (Sansure, Coyote)
- Cost: $8,000–14,000 instrument + $25–40/test
- Verify: CE-IVD certificate + Notified Body approval

**Option C: If you want FOOD testing only**
- Don't need IVD clearance
- Can use any qPCR system (Chai Open, Tianlong, even DIY)
- Cost: $3,000–15,000 instrument
- Verify: ISO 17025 matrix validation (in-house study)

**Where to source Sansure/Coyote:**
- Direct: contact@sansure.com.cn / contact@coyotebio.com
- Distributor: Global Sources, Alibaba Global
- US/Canada import: Requires regulatory pathway (LDT or CE-IVD mutual recognition)

**What to verify BEFORE buying:**
```
MANDATORY CHECKLIST (CE-IVD):
☐ CE-IVD certificate from Notified Body
☐ List of targets (22-plex should include Salmonella, STEC, Campylobacter, Norovirus, etc.)
☐ Analytical sensitivity/specificity data (≥95% both)
☐ Internal Control validation
☐ Reagent stability (shelf-life)
☐ Quality of reagent supply chain (ISO 9001, ISO 13485)
☐ Software updates: How does manufacturer push updates? (Over-the-network? Firmware card?)

MANDATORY CHECKLIST (Clinical LDT pathway):
☐ Clinical accuracy study (500+ patient samples)
☐ Sensitivity/specificity verification in your lab
☐ Cross-reactivity testing (interference panel)
☐ Medical director sign-off
☐ CAP/CLIA certified lab required
```

**Cost breakdown:**
- Sansure instrument: $8,000–12,000
- Shipping + import duties: $500–2,000
- Reagent consumables (1,000 tests/year @ $30): $30,000/year
- LDT validation (if clinical use): $20,000–50,000 (one-time)
- **Total first year:** $38,500–64,000 (or $8,500–14,000 if food testing)

**Auditor view (Food):**
- ✓ "Is this validated for your matrix?" (Show in-house LoD/LoQ studies)
- ✓ PASS

**Auditor view (Clinical, US):**
- ⚠ "Is this FDA-cleared?" If using Sansure: No. → Need LDT pathway
- ✓ "Do you have LDT documentation?" (Show validation package)
- ✓ PASS (if LDT complete)

---

#### ✗ 4. IMMUNOASSAY ANALYZERS (for clinical serology)

**Why can't DIY:** Chemiluminescence/ELISA requires:
- Multi-wavelength optical detection (450 nm, 630 nm, etc.)
- Precise temperature control (37°C water jacket)
- Automated microplate handling + wash cycle precision
- Reagent bar-code reading (to match reagent lot to test)

**What to buy instead:**

| Manufacturer | Model | Test Types | IVD Clearance | Price |
|---|---|---|---|---|
| **Snibe Diagnostic (China)** | Maglumi 600 Plus | Chemiluminescence (Hep A IgM, etc.) | CE-IVD | $12,000–16,000 |
| **Mindray (China)** | CL-2200i | Chemiluminescence | CE-IVD | $14,000–18,000 |
| **Roche (Switzerland)** | cobas e411 | Chemiluminescence | FDA + CE-IVD | $35,000–50,000 |
| **bioMérieux (France)** | VIDAS 3 | ELISA | FDA + CE-IVD | $30,000–45,000 |

**Sourcing strategy:**

**Option A: If you need FDA clearance (US clinical)**
- Use Roche cobas or bioMérieux VIDAS
- Cost: $30,000–50,000
- Verify: FDA database (mddb.fda.gov)

**Option B: If CE-IVD OK (Canada, EU, or food)**
- Use Snibe or Mindray
- Cost: $12,000–18,000
- 60% savings vs. Roche
- Verify: CE-IVD certificate + Notified Body

**Where to source:**
- Direct: contact@snibe.com.cn / contact@mindray.com
- Distributor: Alibaba, Global Sources
- US/Canada: Requires import regulatory pathway

**What to verify:**
```
MANDATORY CHECKLIST:
☐ CE-IVD certificate (or FDA 510k if US)
☐ Assay menu: Does it include Anti-HAV IgM, Enterotoxins, etc.?
☐ Test throughput: ~60–100 tests/hour (appropriate scale)
☐ Reagent availability: 24-month shelf-life minimum
☐ QC materials: Provided by manufacturer (3-level controls)
☐ Software updates: How frequently? (Monthly patches?)
☐ Service & support: Technical hotline? Spare parts availability?
```

**Cost breakdown:**
- Instrument: $12,000–18,000
- Shipping + installation: $1,000–3,000
- Reagents (500 tests/year @ $30): $15,000/year
- QC materials (reagent pack/month): $1,200/year
- Annual service contract: $1,000–2,000/year
- **Total first year:** $30,200–41,000

**Auditor view:**
- ✓ "Is this FDA-cleared or CE-marked?" (Show certificate)
- ✓ "QC results?" (Show daily 3-level control logs)
- ✓ PASS

---

#### ✗ 5. WHOLE GENOME SEQUENCERS (NGS)

**Why can't DIY:** Sequencing chemistry is proprietary (patents + process know-how)

**Options:**
- **Illumina MiSeq:** $100k new, $40k–60k used (industry standard)
- **Oxford Nanopore GridION:** $70k new, $30k–50k used (long-read alternative)
- **Ion Torrent PGM:** $35k new, $15k–25k used (deprecated but works)

**Sourcing:**
- New: Contact manufacturer directly
- Used: LabX.com, EquipNet, BiodagUS
- Cost: Buy 5–10 years old (still functional; sequencing chemistry updates via reagent purchase)

**For phylogenetics (food/clinical outbreak tracking):**
- **Recommended:** Oxford Nanopore Flongle ($8,000 instrument + $100/flow cell)
  - Real-time sequencing (in-lab results <4 hours)
  - Much cheaper than full GridION
  - Sufficient for MLST/WGS phylogenetic typing

**Auditor view:**
- ✓ "How do you validate WGS results?" (Show Snippy SNP pipeline validation; comparison to reference)
- ✓ PASS

**Cost:** $30,000–60,000 used MiSeq (one-time) + $50–100/sample reagents

---

## PART 2: COMPLETE OPEN-SOURCE SOFTWARE STACK

### ✓ 100% OPEN-SOURCE SOFTWARE (FULL FREEDOM, ALL FUNCTIONS)

#### 1. LIMS (Laboratory Information Management System)

**SENAITE (GPL-2.0)**
```
GitHub: https://github.com/senaite/senaite.core
License: GNU General Public License v2.0
Built on: Plone CMS (Python/Zope)
Database: PostgreSQL
```

**Features:**
- Sample intake & barcode tracking
- Dual-stream workflows (Food | Clinical)
- Automatic QC result flagging (Ct > 35 = negative, Ct < 30 = presumptive positive)
- Chain-of-custody audit trails (ALCOA+ compliance)
- Certificate of Analysis generation (PDF export)
- Proficiency testing (PT) matrix management
- Electronic signature (OIDC + Keycloak)
- REST API (senaite.jsonapi) for instrument integration
- Role-based access control (Food Manager, Clinical Tech, Admin)

**Customization (you write it):**
```python
# senaite.foodsafety (custom egg)
# Custom Python module extending SENAITE

from senaite.core.catalog import CATALOG
from senaite.core.workflow import WORKFLOW

class RecallManagement:
    """Lot tracking & recall workflow"""
    
    def flag_lot_contaminated(self, lot_id, pathogen):
        lot = self.catalog.get(lot_id)
        lot.setState("Contaminated")
        
        # Automatic notification
        emails = self.get_retail_contacts()
        for email in emails:
            self.send_recall_notice(email, lot_id, pathogen)

class ChefClearanceWorkflow:
    """Worker test-of-cure tracking"""
    
    def schedule_retest(self, worker_id):
        """Schedule 2nd stool sample, >24hrs after 1st negative"""
        worker = self.get_worker(worker_id)
        test1_date = worker.get_last_negative_test()
        retest_date = test1_date + timedelta(days=2)
        
        worker.setState("AwaitingRetestSample")
        self.send_notification(worker.email, f"Please collect 2nd sample by {retest_date}")
```

**Cost:** Free (open-source) + hosting costs ($100–300/month self-hosted or $500–1,000/month managed)

**Auditor view:** ✓ PASS (ISO 17025 / ISO 15189 validated)

---

#### 2. Instrument Data Ingestion (Custom Python Daemons)

**Framework:** Python 3.10+ + Watchdog + Requests

```python
# instrument_watcher.py (runs in Docker container)

import os
import json
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests

class QPCRWatcher(FileSystemEventHandler):
    """Parse qPCR output files and ingest to SENAITE"""
    
    def __init__(self, lims_url, api_key):
        self.lims_url = lims_url
        self.api_key = api_key
    
    def on_created(self, event):
        if not event.src_path.endswith(".csv"):
            return
        
        # Parse Tianlong Gentier CSV
        results = self.parse_qpcr_csv(event.src_path)
        
        # Post to SENAITE
        self.post_to_lims(results)
    
    def parse_qpcr_csv(self, filepath):
        """
        Expected format:
        Well, Target, Ct, Tm, DeltaRn
        A1, stx1_FAM, 18.5, 82.3, 0.95
        """
        with open(filepath, "r") as f:
            lines = f.readlines()
        
        results = {}
        for line in lines[1:]:
            well, target, ct, tm, deltarn = line.strip().split(",")
            results[well] = {
                "Target": target,
                "Ct": float(ct) if ct != "N/A" else None,
                "Result": "Negative" if float(ct) > 35 else "Presumptive Positive"
            }
        
        return results
    
    def post_to_lims(self, results):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        # Batch update in SENAITE
        for well, data in results.items():
            payload = {
                "portal_type": "AnalysisResult",
                "Result": data["Ct"],
                "Remarks": f"Auto-ingested: {data['Target']}"
            }
            
            requests.post(
                f"{self.lims_url}/senaite/@@API/v1/update/qpcr_{well}",
                json=payload,
                headers=headers
            )

# Main
if __name__ == "__main__":
    observer = Observer()
    watcher = QPCRWatcher(
        lims_url=os.getenv("LIMS_URL"),
        api_key=os.getenv("LIMS_API_KEY")
    )
    
    observer.schedule(watcher, "/mnt/instruments/qpcr_output", recursive=False)
    observer.start()
```

**Cost:** Free (open-source) + development time (1–2 weeks)

---

#### 3. Robotic Automation (Opentrons OT-2/Flex + Python API)

**Framework:** Opentrons Protocol API (Python)

```python
# magnetic_bead_extraction.py (Opentrons protocol)

from opentrons import protocol_api

metadata = {
    "apiLevel": "2.15",
    "protocolName": "Magnetic Bead RNA Extraction",
}

def run(protocol: protocol_api.ProtocolContext):
    
    # Load hardware
    mag_mod = protocol.load_module("magnetic module gen2", 1)
    sample_plate = mag_mod.load_labware("nest_96_deepwell_2ml")
    elution_plate = protocol.load_labware("nest_96_wellplate_200ul", 2)
    tips = protocol.load_labware("opentrons_96_filtertiprack_200ul", 3)
    
    pipette = protocol.load_instrument("p300_single_gen2", "right", tip_racks=[tips])
    
    # Step 1: Bind RNA to magnetic beads
    for well in sample_plate.wells():
        pipette.pick_up_tip()
        pipette.mix(3, 150, well)  # Mix sample
        pipette.drop_tip()
    
    # Step 2: Magnetic separation (move beads to side)
    mag_mod.engage(height_from_base=4.5)
    protocol.delay(minutes=5)
    
    # Step 3: Remove supernatant
    for well in sample_plate.wells():
        pipette.pick_up_tip()
        pipette.aspirate(180, well.bottom(1))
        pipette.dispense(180, protocol.fixed_trash)
        pipette.drop_tip()
    
    # Step 4: Wash (ethanol)
    mag_mod.disengage()
    for i in range(2):
        # Add ethanol...
        mag_mod.engage()
        protocol.delay(minutes=2)
        # Remove supernatant...
    
    # Step 5: Elute RNA
    mag_mod.disengage()
    for i, (src, dst) in enumerate(zip(sample_plate.wells(), elution_plate.wells())):
        pipette.pick_up_tip()
        pipette.aspirate(50, src.bottom(1))
        pipette.dispense(50, dst)
        pipette.drop_tip()
    
    protocol.comment("Extraction complete!")
```

**Features:**
- Upload protocol via HTTP API (OT's built-in server, port 31950)
- Python fully customizable
- No proprietary consumables; uses standard 96-well plates
- Integrate with LIMS (poll for pending samples, run extraction)

**Cost:** $35,000–45,000 (purchase) + Free (protocols are open-source Python)

---

#### 4. Bioinformatics Pipeline (Nextflow + Snippy + Nextstrain)

**SNP Analysis & Phylogenetics:**

```nextflow
// wgs_pipeline.nf

params {
    fastq_dir = "/data/sequencer_output"
    ref_genome = "/data/reference/salmonella_lt2.fasta"
}

process quality_control {
    container "quay.io/biocontainers/fastp:latest"
    
    input:
    tuple val(sample_id), path(r1), path(r2)
    
    output:
    tuple val(sample_id), path("${sample_id}_trimmed_R1.fastq.gz"), path("${sample_id}_trimmed_R2.fastq.gz")
    
    script:
    """
    fastp -i ${r1} -I ${r2} \
          -o ${sample_id}_trimmed_R1.fastq.gz \
          -O ${sample_id}_trimmed_R2.fastq.gz \
          --qualified_quality_phred 20
    """
}

process variant_calling {
    container "quay.io/biocontainers/snippy:latest"
    
    input:
    tuple val(sample_id), path(r1), path(r2)
    
    output:
    tuple val(sample_id), path("${sample_id}.vcf"), path("${sample_id}.fa")
    
    script:
    """
    snippy --r ${params.ref_genome} \
           --pe1 ${r1} --pe2 ${r2} \
           --outdir snippy_out
    cp snippy_out/snps.vcf ${sample_id}.vcf
    cp snippy_out/core.aln ${sample_id}.fa
    """
}

process phylogenetics {
    container "quay.io/biocontainers/augur:latest"
    publishDir "results"
    
    input:
    path(all_fastas)
    
    output:
    path("phylo_tree.json"), path("tree.nwk")
    
    script:
    """
    augur align --sequences ${all_fastas} --output aligned.fasta
    augur tree --alignment aligned.fasta --output tree.nwk
    augur refine --tree tree.nwk --alignment aligned.fasta --output-tree tree_refined.nwk
    augur export v2 --tree tree_refined.nwk --output phylo_tree.json
    """
}

workflow {
    fastqs = Channel
        .fromFilePairs("${params.fastq_dir}/*_{R1,R2}.fastq.gz")
        .map { sample, reads -> tuple(sample, reads[0], reads[1]) }
    
    quality_control(fastqs)
    variant_calling(quality_control.out)
    
    all_fas = variant_calling.out.map { id, vcf, fa -> fa }.collect()
    phylogenetics(all_fas)
}
```

**Visualization (Nextstrain Auspice):**

```bash
# Auspice web frontend (runs locally)
auspice view --dataDir results/

# Browse phylogenetic tree interactively
# Hover over branches to see outbreak links
# Export to publication-ready SVG
```

**Cost:** Free (all open-source) + compute resources (~$500–1,000/month cloud, or free if on-premises)

---

#### 5. Environmental Telemetry (InfluxDB + Grafana + Mosquitto)

**Docker Compose Stack:**

```yaml
version: '3.8'

services:
  mosquitto:
    image: eclipse-mosquitto:latest
    ports:
      - "1883:1883"
    volumes:
      - ./mosquitto.conf:/mosquitto/config/mosquitto.conf

  influxdb:
    image: influxdb:2.7
    environment:
      INFLUXDB_DB: lab_telemetry
      INFLUXDB_ADMIN_USER: admin
      INFLUXDB_ADMIN_PASSWORD: ${INFLUX_PASS}
    ports:
      - "8086:8086"
    volumes:
      - influxdb_data:/var/lib/influxdb2

  grafana:
    image: grafana/grafana:latest
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASS}
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
```

**Alerts (Grafana AlertManager):**

```yaml
# grafana-alert-rules.yaml

- title: "Incubator Temperature Out of Range"
  condition: "temp_35c_room1 > 36.5 OR temp_35c_room1 < 33.5"
  actions:
    - type: "email"
      email: "lab-manager@lab.com"
      message: "Incubator temperature abnormal!"
    - type: "sms"
      number: "+1-555-0123"
    - type: "slack"
      channel: "#lab-alerts"
```

**Cost:** Free (open-source) + hosting ($50–200/month)

---

#### 6. Identity & Access Management (Keycloak)

**SSO Configuration:**

```yaml
# keycloak-docker-compose.yaml

version: '3.8'

services:
  keycloak:
    image: quay.io/keycloak/keycloak:latest
    environment:
      KC_DB: postgres
      KC_DB_URL: jdbc:postgresql://postgres:5432/keycloak
      KC_DB_USERNAME: keycloak
      KC_DB_PASSWORD: ${KEYCLOAK_DB_PASS}
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: ${KEYCLOAK_ADMIN_PASS}
    ports:
      - "8080:8080"
    command: start-dev  # Production: use 'start'

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: keycloak
      POSTGRES_USER: keycloak
      POSTGRES_PASSWORD: ${KEYCLOAK_DB_PASS}
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

**OIDC Integration (SENAITE + Grafana + Nextflow):**

```python
# senaite_oidc_config.py

OIDC_PROVIDER = "https://auth.lab.internal/auth/realms/lab-production"
OIDC_CLIENT_ID = "senaite-lims"
OIDC_CLIENT_SECRET = "${OIDC_SECRET}"

# All three apps use same Keycloak realm
# Single sign-on across platform
# Audit logs: Keycloak logs all login/logout events
```

**Cost:** Free (open-source) + hosting ($100–300/month)

---

#### 7. Data Integration & Orchestration (FastAPI + Celery + Redis)

**LIMS API Gateway:**

```python
# api_gateway.py (FastAPI)

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer
import httpx

app = FastAPI(title="Lab API Gateway")
security = HTTPBearer()

@app.post("/api/v1/samples")
async def create_sample(sample_data: dict, credentials = Depends(security)):
    """
    Create new sample in SENAITE via REST API
    """
    token = credentials.credentials
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://senaite.lab.internal/senaite/@@API/v1/create",
            json=sample_data,
            headers={"Authorization": f"Bearer {token}"}
        )
    
    return response.json()

@app.get("/api/v1/samples/{sample_id}/status")
async def get_sample_status(sample_id: str):
    """
    Poll sample analysis status
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://senaite.lab.internal/senaite/@@API/v1/get/{sample_id}"
        )
    
    return response.json()
```

**Task Queue (Celery + Redis):**

```python
# tasks.py

from celery import Celery

app = Celery("lab_tasks")
app.conf.broker_url = "redis://redis:6379/0"

@app.task
def process_qpcr_batch(run_id):
    """
    Async task: Process all qPCR results from a run
    """
    results = parse_qpcr_file(run_id)
    
    for well, data in results.items():
        update_lims(well, data)

@app.task
def trigger_wgs_analysis(sample_id):
    """
    Async task: Launch Nextflow WGS pipeline
    """
    import subprocess
    subprocess.run([
        "nextflow", "run", "wgs_pipeline.nf",
        "-resume",
        f"--sample_id={sample_id}"
    ])
```

**Cost:** Free (open-source) + infrastructure ($200–500/month)

---

#### 8. Reporting & Visualization (Custom Python PDF Generation)

**Certificate of Analysis Generation:**

```python
# certificate_generator.py (ReportLab)

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer
from datetime import datetime

def generate_certificate(sample_data):
    """
    Generate PDF Certificate of Analysis
    """
    
    doc = SimpleDocTemplate("COA.pdf", pagesize=letter)
    elements = []
    
    # Header
    title = Paragraph(f"<b>CERTIFICATE OF ANALYSIS</b>", getSampleStyleSheet()['Heading1'])
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Sample info table
    data = [
        ["Lot #", sample_data['lot_id']],
        ["Product", sample_data['product']],
        ["Date Tested", datetime.now().strftime("%Y-%m-%d")],
        ["Result", sample_data['result']],  # "PASSED" or "FAILED"
    ]
    
    table = Table(data)
    elements.append(table)
    
    # Build PDF
    doc.build(elements)
    
    return "COA.pdf"
```

**Cost:** Free (ReportLab open-source)

---

### SUMMARY: COMPLETE OPEN-SOURCE SOFTWARE STACK

| Function | Tool | License | Cost |
|----------|------|---------|------|
| **LIMS** | SENAITE | GPL-2.0 | Free + $100–300/mo hosting |
| **Instrument Integration** | Custom Python (Watchdog) | MIT | Free (dev time) |
| **Robotics** | Opentrons Protocol API | Apache 2.0 | Free (instrument: $35k–45k) |
| **Bioinformatics** | Nextflow + Snippy + Augur | MIT / GPL-3.0 | Free (compute: $500–1k/mo) |
| **Telemetry** | InfluxDB + Grafana + Mosquitto | AGPL / MIT | Free + $50–200/mo hosting |
| **Identity** | Keycloak | Apache 2.0 | Free + $100–300/mo hosting |
| **API Gateway** | FastAPI | BSD-3 | Free |
| **Task Queue** | Celery + Redis | BSD / 3-Clause | Free |
| **Reporting** | ReportLab | AGPL-3.0 | Free |
| **Lab Notebook** | Jupyter + JupyterHub | BSD-3 | Free + $200/mo hosting |
| **Version Control** | Gitea (self-hosted) | MIT | Free + $100/mo hosting |
| **Container Registry** | Gitea (integrated) | MIT | Free |
| **Container Orchestration** | Kubernetes (k3s lightweight) | Apache 2.0 | Free ($500/mo infrastructure) |

**Total Software Cost (excluding infrastructure):** $0 (all open-source)

**Total Hosting/Infrastructure Cost:** ~$1,500–3,000/month

**Cost Comparison vs. Proprietary Stack:**
- Proprietary LIMS (LabWare, STARLIMS): $50,000–150,000/year
- Proprietary bioinformatics (BioNumerics): $5,000–15,000/year
- **Open-source equivalent:** $18,000–36,000/year (hosting only)

**Savings:** 60–75% annually

---

## PART 3: COMPLETE PROCUREMENT CHECKLIST

### Hardware to BUY (with verification points)

```
PRESSURE VESSEL (Autoclave)
☐ Purchase: Gemmy SA-Series 30L or Zealway GI54 Deluxe
☐ Verify: ASME "U" stamp certificate (PDF/photo)
☐ Verify: ISO 13485 factory audit certificate
☐ Verify: Shipping includes pressure vessel inspection certificate
☐ Install: Register with local municipal building department
☐ Annual: Biological indicator spore test (Bacillus atrophaeus)
☐ Cost: $4,000–8,000 + $200–500/year maintenance

CLASS II BIOSAFETY CABINET
☐ Option A (New): Order from Biobase/Esco with NSF certificate
☐ Option B (Used): Buy from LabX/EquipNet; verify NSF listing
☐ Verify: Model listed in NSF directory (nsf.org/certified-products)
☐ Verify: DOP/PAO test report (HEPA integrity)
☐ Verify: Airflow velocity ≥100 ft/min
☐ Install: Schedule field certification with NSF-approved contractor
☐ Annual: DOP/PAO aerosol smoke test ($700–1,200)
☐ Cost: $5,000–8,000 + $1,000–1,700/year maintenance

SYNDROMIC MULTIPLEX SYSTEM (if clinical)
☐ Option A (FDA cleared): BioFire FilmArray 2.0 (~$45k)
☐ Option B (CE-IVD): Sansure iPonatic III (~$8k–12k) [requires LDT if US]
☐ Verify: CE-IVD certificate OR FDA 510k clearance
☐ Verify: Assay menu includes your targets (Salmonella, STEC, etc.)
☐ Verify: Reagent supply chain (24-month shelf life minimum)
☐ Cost: $8,000–45,000 + $25–200/test consumables

IMMUNOASSAY ANALYZER (if serology)
☐ Option A (FDA): Roche cobas e411 (~$35k–50k)
☐ Option B (CE-IVD): Snibe Maglumi 600 (~$12k–16k)
☐ Verify: CE-IVD OR FDA 510k clearance
☐ Verify: QC materials supplied (3-level controls)
☐ Cost: $12,000–50,000 + $20–40/test reagents

SEQUENCER (for WGS phylogenetics)
☐ Buy used: Illumina MiSeq ($40k–60k) OR Oxford Nanopore Flongle ($8k)
☐ Verify: Manufacturer warranty (5-year standard)
☐ Verify: Sequencing reagents in stock for purchase
☐ Cost: $8,000–60,000 (one-time) + $50–100/sample

INCUBATORS (you CAN DIY these)
☐ Buy commercial OR build DIY with PID controller
☐ If DIY: Temperature calibration certificate (NIST) [$150–300/yr per unit]
☐ Verify: ±0.5°C stability over 24 hours
☐ Cost: DIY $400–800 OR commercial $3,000–5,000

WATER BATHS (you CAN DIY these)
☐ Buy commercial OR build DIY PID-controlled
☐ If DIY: Temperature probe calibration (NIST) [$150–300/yr]
☐ Verify: ±0.2°C stability
☐ Cost: DIY $400–700 OR commercial $2,000–3,500

CENTRIFUGES (buy commercial, low-cost OK)
☐ Buy used Eppendorf or cheap Chinese brand
☐ Verify: Electrical safety (CSA/UL)
☐ Verify: Tachometer calibration (NIST) [$150–300/yr]
☐ Cost: $2,500–5,000

OPENTRONS ROBOT
☐ Buy new OT-2 or Flex (only manufacturer: Opentrons)
☐ Verify: Python API documentation (GitHub)
☐ Verify: Community protocols (nextstrain.org)
☐ Cost: $35,000–45,000 (one-time)

QPC CYCLER
☐ Option A (Food): Chai Open qPCR DIY kit ($3k–5k) [requires ISO 17025 validation]
☐ Option B (Food): Tianlong Gentier 96E ($12k–16k) [CE-IVD, plug-and-play]
☐ Option C (Clinical): Only use FDA-cleared (Roche, Bio-Rad, Applied Bio) [$35k+]
☐ Cost: $3,000–35,000
```

---

## PART 4: FINAL COST COMPARISON

### SCENARIO A: Food Testing Lab (No Clinical Diagnostics)

| Category | Open-Source DIY | Commercial Budget | Savings |
|----------|-----------------|-------------------|---------|
| **Instrumentation** | | | |
| Autoclave (mandatory) | N/A (buy Gemmy) | $5,000–8,000 | -- |
| BSC (mandatory) | N/A (buy Biobase) | $6,000–8,000 | -- |
| Incubators (3×) | $1,200–2,400 (DIY) | $9,000–15,000 | $6,600–12,600 |
| Water baths (2×) | $800–1,400 (DIY) | $4,000–7,000 | $2,600–5,600 |
| Centrifuges (2×) | $5,000–8,000 (buy used) | $6,000–10,000 | $0–5,000 |
| Opentrons OT-2 | $35,000–45,000 | $35,000–45,000 | -- |
| qPCR (Chai or Tianlong) | $3,000–16,000 | $12,000–35,000 | $0–19,000 |
| Sequencer (Nanopore) | $8,000–12,000 | $8,000–12,000 | -- |
| Misc. (balances, pipettes, etc.) | $5,000–8,000 | $8,000–15,000 | $0–7,000 |
| **SUBTOTAL HARDWARE** | **$63,000–100,800** | **$87,000–155,000** | **$9,600–55,200** |
| **Software** | | | |
| LIMS (SENAITE) | Free | $50,000–150,000 | $50,000–150,000 |
| Bioinformatics (Nextstrain, etc.) | Free | $5,000–15,000 | $5,000–15,000 |
| Monitoring/Telemetry | Free + hosting | $20,000–50,000 | $20,000–50,000 |
| **SUBTOTAL SOFTWARE** | **Free + $1,500–3,000/mo** | **$75,000–215,000** | **$75,000–215,000** |
| **FACILITY** | | | |
| Building renovation (HVAC, electrical) | $200,000–400,000 | $200,000–400,000 | -- |
| **TOTAL YEAR 1** | **$263,000–503,800** | **$362,000–770,000** | **$84,600–306,200** |
| **ANNUAL MAINTENANCE** | $50,000–80,000 | $100,000–150,000 | $20,000–100,000 |

**Savings:** 23–60% with open-source stack

---

### SCENARIO B: Food + Clinical Testing Lab (Dual-Purpose)

| Category | Open-Source DIY | Commercial Budget | Savings |
|----------|-----------------|-------------------|---------|
| **All Food Equipment** | (as above) | (as above) | (as above) |
| **Clinical Add-On** | | | |
| Syndromic POCT (Sansure) | $8,000–12,000 | $45,000 (FilmArray) | $33,000–37,000 |
| Immunoassay (Snibe) | $12,000–16,000 | $35,000–50,000 | $19,000–38,000 |
| **TOTAL CLINICAL** | **$20,000–28,000** | **$80,000–95,000** | **$52,000–75,000** |
| **TOTAL YEAR 1** | **$283,000–531,800** | **$442,000–865,000** | **$136,600–381,200** |

**Savings:** 31–57% with open-source stack + international hardware

---

## CONCLUSION: RECOMMENDED ARCHITECTURE

### ✓ BUILD COMPLETELY OPEN-SOURCE (Software)

1. **LIMS:** SENAITE (GPL-2.0, fully customizable)
2. **Instrument Integration:** Custom Python watchdog daemons
3. **Robotics:** Opentrons Protocol API (already open-source)
4. **Bioinformatics:** Nextflow + Snippy + Nextstrain (publication-ready)
5. **Telemetry:** InfluxDB + Grafana + Mosquitto (enterprise-grade)
6. **Identity:** Keycloak (SSO across all apps)

**Cost:** $0 (all open-source) + $1,500–3,000/month hosting

### ✓ BUILD DIY (Hardware Where Possible)

1. **Incubators:** Custom ESP32 + DS18B20 + PID controller ($400–800 each)
2. **Water baths:** DIY PID-controlled ($400–700 each)
3. **Environmental monitoring:** ESPHome sensors + InfluxDB ($100–300 per station)

**Savings:** $6,000–15,000 vs. commercial

### ✓ BUY CERTIFIED INTERNATIONAL (Hardware You Can't DIY)

1. **Autoclave:** Gemmy SA-Series ($4,000–8,000) with ASME stamp
2. **BSC:** Biobase/Esco ($5,000–8,000) with NSF listing
3. **Syndromic POCT:** Sansure iPonatic ($8,000–12,000) with CE-IVD
4. **Immunoassay:** Snibe Maglumi ($12,000–16,000) with CE-IVD
5. **qPCR:** Tianlong Gentier ($12,000–16,000) with CE-IVD
6. **Sequencer:** Oxford Nanopore Flongle ($8,000) or used Illumina MiSeq ($40k–60k)

**Savings:** 60–70% vs. Western brands (Thermo, Roche, Bio-Rad)

### BOTTOM LINE

**Total Investment (Food + Clinical Lab):**
- Hardware: $280,000–530,000 (open-source DIY + international certified)
- Software: $0 (all open-source)
- Facility: $200,000–400,000 (building renovation)
- **TOTAL YEAR 1:** $480,000–930,000

**vs. Proprietary Stack:**
- **Total:** $900,000–1,600,000

**Savings:** $170,000–670,000 (18–42% reduction)

**Annual Operating Costs:**
- Open-source: $50,000–80,000/year
- Proprietary: $150,000–250,000/year
- **Savings:** $70,000–200,000/year

**Payback Period:** 1–3 years on capital investment
