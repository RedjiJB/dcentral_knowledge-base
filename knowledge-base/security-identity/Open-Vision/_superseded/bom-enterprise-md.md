---
source_project: Open Vision
source_project_uuid: 019adc89-3095-77fb-a6f8-3f599d84699a
doc_uuid: 640fb278-3099-4b6e-a1fd-89fb5964f5d2
original_filename: bom-enterprise.md
created_at: 2025-12-02T00:49:42.050784+00:00
content_hash: 7bee1bc34cb4status: duplicate
duplicate_of: "ai-ml-research/IHOSE/bom-enterprise-md.md"
duplicate_reason: "exact content_hash match, different category (same doc uploaded to multiple Claude Projects)"
---

# Enterprise Hardware Bill of Materials (BOM)

## Deployment Specs
- **Scale**: 500 cameras across 20 sites
- **Retention**: 90 days for events, 30 days for continuous
- **Analytics**: Real-time AI on all cameras
- **Availability**: 99.9% uptime (high availability)

---

## Central Cloud Infrastructure

### Kubernetes Cluster

#### Control Plane Nodes (3x for HA)

**Option A: System76 Thelio Major (Recommended - Open Hardware)**
| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| CPU | AMD Threadripper PRO 5975WX (32-core) | 3 | $2,400 | $7,200 |
| Motherboard | ASUS Pro WS WRX80E-SAGE SE WIFI | 3 | $800 | $2,400 |
| RAM | 128GB DDR4 ECC (8x16GB) | 3 | $450 | $1,350 |
| Boot SSD | 1TB NVMe Samsung 990 PRO | 3 | $100 | $300 |
| Network | Dual 10GbE Intel X710 | 3 | $250 | $750 |
| Power Supply | 1200W 80+ Platinum | 3 | $200 | $600 |
| Case | System76 Thelio Major | 3 | $300 | $900 |
| **Subtotal** | | | | **$13,500** |

**Option B: Commercial Server**
| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| Server | Dell PowerEdge R750 | 3 | $4,500 | $13,500 |
| - CPU | Dual Intel Xeon Silver 4314 | Included | - | - |
| - RAM | 128GB DDR4 ECC | Included | - | - |
| - Storage | 2x 960GB SSD RAID 1 | Included | - | - |
| - Network | Dual 10GbE | Included | - | - |
| **Subtotal** | | | | **$13,500** |

#### Worker Nodes (5x, scalable)

**Option A: Open Hardware Build**
| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| CPU | AMD Ryzen 9 7950X (16-core) | 5 | $550 | $2,750 |
| Motherboard | ASUS Pro WS X670E-ACE | 5 | $500 | $2,500 |
| RAM | 64GB DDR5 (2x32GB) | 5 | $180 | $900 |
| Boot SSD | 1TB NVMe WD Black SN850X | 5 | $120 | $600 |
| GPU (Optional) | NVIDIA T4 16GB (ML training) | 2 | $2,000 | $4,000 |
| Network | Dual 10GbE Intel X710 | 5 | $250 | $1,250 |
| Power Supply | 850W 80+ Gold | 5 | $150 | $750 |
| Case | Fractal Design Define 7 XL | 5 | $200 | $1,000 |
| **Subtotal** | | | | **$13,750** |

**Option B: RISC-V (Fully Open ISA) - Future-proof**
| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| Server | Milk-V Pioneer (64-core RISC-V) | 5 | $1,500 | $7,500 |
| RAM Upgrade | Additional 64GB (128GB total) | 5 | $300 | $1,500 |
| Network | 10GbE PCIe adapter | 5 | $150 | $750 |
| **Subtotal** | | | | **$9,750** |

### Storage Cluster (Ceph)

#### Storage Nodes (6x for distributed storage)

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| CPU | AMD EPYC 7313P (16-core) | 6 | $900 | $5,400 |
| Motherboard | Supermicro H12SSL-i | 6 | $400 | $2,400 |
| RAM | 64GB DDR4 ECC (4x16GB) | 6 | $280 | $1,680 |
| Boot SSD | 500GB NVMe | 6 | $60 | $360 |
| Cache SSD | 2x 1TB NVMe (metadata/cache) | 6 | $200 | $1,200 |
| Data HDDs | 12x 18TB Seagate Exos X18 | 6 | $3,600 | $21,600 |
| HBA | LSI 9305-16i (SAS controller) | 6 | $350 | $2,100 |
| Network | Dual 25GbE Mellanox ConnectX-5 | 6 | $400 | $2,400 |
| Power Supply | 1000W 80+ Platinum | 6 | $180 | $1,080 |
| Case | Supermicro 4U 24-bay chassis | 6 | $800 | $4,800 |
| **Subtotal** | | | | **$43,020** |

**Storage Capacity**: 6 nodes × 12 drives × 18TB = 1,296TB raw = ~432TB usable (3x replication)

### PostgreSQL HA Cluster (3x nodes)

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| CPU | AMD Ryzen 9 7900X (12-core) | 3 | $400 | $1,200 |
| Motherboard | ASUS Pro WS X670E-ACE | 3 | $500 | $1,500 |
| RAM | 128GB DDR5 (4x32GB) | 3 | $350 | $1,050 |
| NVMe SSD | 2x 4TB Samsung 990 PRO (RAID 1) | 3 | $700 | $2,100 |
| Network | Dual 10GbE Intel X710 | 3 | $250 | $750 |
| Power Supply | 850W 80+ Gold | 3 | $150 | $450 |
| Case | Fractal Design Define 7 | 3 | $170 | $510 |
| **Subtotal** | | | | **$7,560** |

### Networking

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| Core Switch | 48-port 10GbE + 4x 100GbE uplinks | 2 | $8,000 | $16,000 |
| Storage Switch | 24-port 25GbE (Ceph network) | 2 | $4,000 | $8,000 |
| Load Balancer | HA pair (HAProxy appliance) | 2 | $3,000 | $6,000 |
| Firewall | pfSense appliance or Netgate 8200 | 2 | $2,500 | $5,000 |
| Cables | 10GbE SFP+ DAC, 25GbE cables | 100 | $30 | $3,000 |
| Rack | 42U server rack with PDU | 2 | $1,500 | $3,000 |
| **Subtotal** | | | | **$41,000** |

### Central Cloud Total: **$118,830**

---

## Edge Sites (20 sites, 25 cameras each)

### Per-Site Hardware

#### Edge Compute Nodes (2x per site for HA)

**Option A: Budget (Orange Pi 5 Plus + Hailo-8)**
| Component | Specification | Qty/Site | Unit Price | Total/Site | 20 Sites Total |
|-----------|--------------|----------|------------|------------|----------------|
| SBC | Orange Pi 5 Plus 16GB | 2 | $150 | $300 | $6,000 |
| AI Accelerator | Hailo-8 M.2 module (26 TOPS) | 2 | $70 | $140 | $2,800 |
| Storage | 2TB NVMe SSD | 2 | $150 | $300 | $6,000 |
| Case | Metal case with cooling | 2 | $30 | $60 | $1,200 |
| Power Supply | USB-C PD 65W | 2 | $25 | $50 | $1,000 |
| **Subtotal** | | | | **$850** | **$17,000** |

**Option B: Performance (Jetson Orin Nano)**
| Component | Specification | Qty/Site | Unit Price | Total/Site | 20 Sites Total |
|-----------|--------------|----------|------------|------------|----------------|
| Computer | NVIDIA Jetson Orin Nano Dev Kit | 2 | $500 | $1,000 | $20,000 |
| Storage | 2TB NVMe SSD | 2 | $150 | $300 | $6,000 |
| Case | Metal enclosure | 2 | $40 | $80 | $1,600 |
| **Subtotal** | | | | **$1,380** | **$27,600** |

**Option C: High-End (Jetson Orin NX)**
| Component | Specification | Qty/Site | Unit Price | Total/Site | 20 Sites Total |
|-----------|--------------|----------|------------|------------|----------------|
| Computer | NVIDIA Jetson Orin NX 16GB | 2 | $800 | $1,600 | $32,000 |
| Storage | 2TB NVMe SSD | 2 | $150 | $300 | $6,000 |
| Case | Industrial enclosure | 2 | $50 | $100 | $2,000 |
| **Subtotal** | | | | **$2,000** | **$40,000** |

#### Local Storage (per site)

| Component | Specification | Qty/Site | Unit Price | Total/Site | 20 Sites Total |
|-----------|--------------|----------|------------|------------|----------------|
| NAS | Synology DS923+ (4-bay) | 1 | $600 | $600 | $12,000 |
| HDDs | 4x 8TB WD Red Plus | 1 | $800 | $800 | $16,000 |
| **Subtotal** | | | | **$1,400** | **$28,000** |

#### Network Equipment (per site)

| Component | Specification | Qty/Site | Unit Price | Total/Site | 20 Sites Total |
|-----------|--------------|----------|------------|------------|----------------|
| PoE Switch | 48-port Gigabit PoE+ (802.3at) | 1 | $500 | $500 | $10,000 |
| Router | OpenWrt-compatible (Ubiquiti EdgeRouter) | 1 | $150 | $150 | $3,000 |
| VPN Gateway | WireGuard appliance or pfSense | 1 | $200 | $200 | $4,000 |
| **Subtotal** | | | | **$850** | **$17,000** |

#### Cameras (25 per site)

**Option A: OpenIPC (Budget)**
| Component | Specification | Qty/Site | Unit Price | Total/Site | 20 Sites Total |
|-----------|--------------|----------|------------|------------|----------------|
| IP Camera | 4MP with OpenIPC firmware | 25 | $40 | $1,000 | $20,000 |
| Mounts | Wall/ceiling mount | 25 | $15 | $375 | $7,500 |
| Cables | Cat6 50ft PoE cable | 25 | $10 | $250 | $5,000 |
| **Subtotal** | | | | **$1,625** | **$32,500** |

**Option B: Quality Commercial**
| Component | Specification | Qty/Site | Unit Price | Total/Site | 20 Sites Total |
|-----------|--------------|----------|------------|------------|----------------|
| IP Camera | Hikvision 4MP ColorVu (H.265) | 20 | $120 | $2,400 | $48,000 |
| PTZ Camera | Hikvision 4MP PTZ (key locations) | 5 | $400 | $2,000 | $40,000 |
| Mounts | Professional mounts | 25 | $20 | $500 | $10,000 |
| Cables | Cat6 50ft PoE cable | 25 | $10 | $250 | $5,000 |
| **Subtotal** | | | | **$5,150** | **$103,000** |

**Option C: High-End (Axis Communications)**
| Component | Specification | Qty/Site | Unit Price | Total/Site | 20 Sites Total |
|-----------|--------------|----------|------------|------------|----------------|
| IP Camera | Axis P3245-LVE 4K | 20 | $500 | $10,000 | $200,000 |
| PTZ Camera | Axis Q6128-E 4K PTZ | 5 | $3,000 | $15,000 | $300,000 |
| Mounts | Axis mounts and housings | 25 | $50 | $1,250 | $25,000 |
| Cables | Cat6 50ft PoE cable | 25 | $10 | $250 | $5,000 |
| **Subtotal** | | | | **$26,500** | **$530,000** |

### Per-Site Totals (Different Configurations)

**Budget Configuration** (Orange Pi + OpenIPC):
- Edge compute: $850
- Storage: $1,400
- Network: $850
- Cameras: $1,625
- **Total per site: $4,725**
- **20 sites: $94,500**

**Standard Configuration** (Jetson Nano + Commercial):
- Edge compute: $1,380
- Storage: $1,400
- Network: $850
- Cameras: $5,150
- **Total per site: $8,780**
- **20 sites: $175,600**

**Premium Configuration** (Jetson NX + Axis):
- Edge compute: $2,000
- Storage: $1,400
- Network: $850
- Cameras: $26,500
- **Total per site: $30,750**
- **20 sites: $615,000**

---

## Complete System Totals

### Budget Deployment
- Central Cloud: $118,830
- 20 Edge Sites: $94,500
- **Grand Total: $213,330**

### Standard Deployment (Recommended)
- Central Cloud: $118,830
- 20 Edge Sites: $175,600
- **Grand Total: $294,430**

### Premium Deployment
- Central Cloud: $118,830
- 20 Edge Sites: $615,000
- **Grand Total: $733,830**

---

## Additional Hardware Considerations

### Uninterruptible Power Supply (UPS)

| Location | Specification | Qty | Unit Price | Total |
|----------|--------------|-----|------------|-------|
| Central Cloud | 10KVA UPS (3-hour runtime) | 2 | $5,000 | $10,000 |
| Edge Sites | 1500VA UPS (1-hour runtime) | 20 | $300 | $6,000 |
| **Subtotal** | | | | **$16,000** |

### Spare Parts & Replacements

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| HDDs | Hot spares for Ceph | 12 | $300 | $3,600 |
| SSDs | Hot spares | 6 | $150 | $900 |
| Cameras | Replacement units | 20 | $120 | $2,400 |
| Network Modules | SFP+ transceivers | 10 | $100 | $1,000 |
| **Subtotal** | | | | **$7,900** |

### Monitoring & Management

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| KVM | Remote KVM over IP | 2 | $500 | $1,000 |
| Environmental | Temperature/humidity sensors | 22 | $50 | $1,100 |
| **Subtotal** | | | | **$2,100** |

---

## Open Hardware Preference Summary

### Fully Open Components Used
- ✅ Orange Pi 5 Plus (ARM SBC, open schematics)
- ✅ RISC-V Milk-V Pioneer (open ISA)
- ✅ AMD CPUs (more open than Intel)
- ✅ System76 hardware (coreboot BIOS)
- ✅ OpenIPC camera firmware
- ✅ pfSense/OpenWrt routers

### Pragmatic Proprietary (Worth the Cost)
- ⚠️ NVIDIA Jetson (AI performance justifies proprietary)
- ⚠️ Commercial cameras (critical areas need reliability)
- ⚠️ Enterprise HDDs (no open alternative)
- ⚠️ 10GbE networking (mature ecosystem)

### Open Source Software (100%)
- All software components are FOSS
- No licensing costs
- Full customization rights

---

## Cost Breakdown by Category

### Standard Configuration ($294,430 total)

| Category | Cost | Percentage |
|----------|------|------------|
| Cameras | $103,000 | 35% |
| Storage Hardware | $43,020 | 14.6% |
| Compute (Cloud) | $34,810 | 11.8% |
| Compute (Edge) | $27,600 | 9.4% |
| Networking | $58,000 | 19.7% |
| Local Storage (Edge) | $28,000 | 9.5% |

---

## 3-Year TCO Analysis

### Hardware
- Initial: $294,430
- Year 1 replacements: $10,000 (drives, cameras)
- Year 2 replacements: $15,000
- Year 3 replacements: $20,000
- **3-year hardware: $339,430**

### Software (OpenVision Platform)
- Licensing: $0 (open source)
- Support: $30,000/year optional
- **3-year software: $90,000 (optional)**

### Personnel
- 2 engineers × $80,000 × 3 years: $480,000

### Infrastructure (if cloud-hosted)
- Hosting: $24,000/year
- Bandwidth: $12,000/year
- **3-year infrastructure: $108,000**

### Total 3-Year TCO
- On-premise: $819,430 (hardware + optional support + personnel)
- Cloud-hosted: $927,430

### vs. Commercial Solutions

**Genetec/Milestone** (commercial VMS):
- Initial licensing: $200/camera × 500 = $100,000
- Annual maintenance: 20% = $20,000/year = $60,000
- Hardware: $250,000 (similar cameras/servers)
- Personnel: $480,000
- **3-year TCO: $890,000**

**OpenVision Advantage**:
- Lower TCO: $819,430 vs $890,000 = **$70,570 savings**
- Full customization (priceless)
- No vendor lock-in
- Community support

---

## Purchasing Guide

### Recommended Vendors

**SBCs & Edge Compute**:
- Orange Pi: amazon.com, aliexpress.com
- NVIDIA Jetson: nvidia.com, arrow.com
- Hailo-8: hailo.ai

**Servers**:
- System76: system76.com
- Supermicro: supermicro.com
- Dell: dell.com

**Storage**:
- HDDs: newegg.com, amazon.com
- SSDs: samsung.com, westerndigital.com

**Networking**:
- Ubiquiti: ui.com
- Intel NICs: intel.com
- Mellanox: nvidia.com/networking

**Cameras**:
- OpenIPC compatible: aliexpress.com
- Hikvision: hikvision.com
- Axis: axis.com

### Lead Times
- SBCs: 2-4 weeks
- Servers: 4-8 weeks
- Storage: 1-2 weeks
- Cameras: 2-6 weeks
- Networking: 2-4 weeks

---

**Next**: [SMB BOM](bom-smb.md) | [Household BOM](bom-household.md)
