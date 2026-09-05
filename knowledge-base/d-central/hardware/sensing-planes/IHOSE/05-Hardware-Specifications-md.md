---
source_project: IHOSE
source_project_uuid: 019a6ba2-1cf8-703d-b379-bb50cd7fad34
doc_uuid: bfbee8eb-513e-4e92-8f67-aa9a513804d9
original_filename: 05-Hardware-Specifications.md
created_at: 2025-12-02T00:47:55.747409+00:00
content_hash: e2febd8569a7
topic: ihose-hardware-bom
---

# OpenVision Platform
## Hardware Specifications & Bill of Materials

**Version:** 1.0  
**Audience:** Procurement, IT Infrastructure, Finance  
**Purpose:** Hardware selection and purchasing guide

---

## Table of Contents
1. [Executive Hardware Summary](#executive-hardware-summary)
2. [Enterprise Deployment BOM](#enterprise-deployment-bom)
3. [SMB Deployment BOM](#smb-deployment-bom)
4. [Household Deployment BOM](#household-deployment-bom)
5. [Open Hardware Options](#open-hardware-options)
6. [Vendor Matrix](#vendor-matrix)
7. [Cost Comparison](#cost-comparison)

---

## Executive Hardware Summary

### Deployment Tiers

| Tier | Scale | Hardware Cost | Use Case |
|------|-------|---------------|----------|
| **Household** | 1-5 cameras | $300 | Residential security |
| **SMB** | 10-50 cameras | $5,000 | Small office, retail |
| **Enterprise** | 500+ cameras | $294,000 | Corporate, industrial |

### Hardware Strategy

**Open Hardware First:**
- Orange Pi / Raspberry Pi for edge compute
- RISC-V servers for future-proofing
- OpenIPC camera firmware
- Commodity x86 servers

**Pragmatic Proprietary:**
- NVIDIA Jetson for AI acceleration (5x performance advantage)
- Enterprise HDDs (no open alternative)
- Commercial cameras for mission-critical areas

---

## Enterprise Deployment BOM

### Scenario: 500 Cameras, 20 Sites

#### Central Cloud Infrastructure

**Kubernetes Control Plane (3 nodes)**

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| **CPU** | AMD EPYC 7313P (16-core, 3.0GHz) | 3 | $900 | $2,700 |
| **Motherboard** | Supermicro H12SSL-i | 3 | $400 | $1,200 |
| **RAM** | 128GB DDR4 ECC (8×16GB) | 3 | $450 | $1,350 |
| **Boot SSD** | 500GB NVMe Samsung 980 PRO | 3 | $80 | $240 |
| **Network** | Dual 10GbE Intel X710 | 3 | $250 | $750 |
| **PSU** | 1000W 80+ Platinum | 3 | $180 | $540 |
| **Case** | 2U Rackmount chassis | 3 | $200 | $600 |
| **Subtotal** | | | | **$7,380** |

**Kubernetes Worker Nodes (5 nodes)**

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| **CPU** | AMD Ryzen 9 7950X (16-core, 4.5GHz) | 5 | $550 | $2,750 |
| **Motherboard** | ASUS Pro WS X670E-ACE | 5 | $500 | $2,500 |
| **RAM** | 64GB DDR5 (2×32GB) | 5 | $200 | $1,000 |
| **NVMe SSD** | 2TB WD Black SN850X | 5 | $180 | $900 |
| **GPU (Optional)** | NVIDIA T4 16GB | 2 | $2,000 | $4,000 |
| **Network** | Dual 10GbE Intel X710 | 5 | $250 | $1,250 |
| **PSU** | 850W 80+ Gold | 5 | $150 | $750 |
| **Case** | 4U Rackmount chassis | 5 | $250 | $1,250 |
| **Subtotal** | | | | **$14,400** |

**Ceph Storage Cluster (6 nodes)**

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| **CPU** | AMD EPYC 7313P (16-core) | 6 | $900 | $5,400 |
| **Motherboard** | Supermicro H12SSL-i | 6 | $400 | $2,400 |
| **RAM** | 64GB DDR4 ECC (4×16GB) | 6 | $280 | $1,680 |
| **Boot SSD** | 500GB NVMe | 6 | $70 | $420 |
| **Cache SSD** | 2×1TB NVMe (metadata/cache) | 6 | $200 | $1,200 |
| **Data HDD** | 12×18TB Seagate Exos X18 | 6 | $3,600 | $21,600 |
| **HBA** | LSI 9305-16i (SAS controller) | 6 | $350 | $2,100 |
| **Network (10GbE)** | Intel X710 dual port | 6 | $250 | $1,500 |
| **Network (25GbE)** | Mellanox ConnectX-5 dual | 6 | $400 | $2,400 |
| **PSU** | 1000W 80+ Platinum | 6 | $180 | $1,080 |
| **Case** | 4U 24-bay chassis | 6 | $800 | $4,800 |
| **Subtotal** | | | | **$44,580** |

**Storage Capacity:** 1,296TB raw = 432TB usable (3x replication)

**PostgreSQL HA Cluster (3 nodes)**

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| **CPU** | AMD Ryzen 9 7900X (12-core) | 3 | $400 | $1,200 |
| **Motherboard** | ASUS Pro WS X670E-ACE | 3 | $500 | $1,500 |
| **RAM** | 128GB DDR5 (4×32GB) | 3 | $450 | $1,350 |
| **NVMe SSD** | 2×4TB Samsung 990 PRO (RAID 1) | 3 | $800 | $2,400 |
| **Network** | Dual 10GbE Intel X710 | 3 | $250 | $750 |
| **PSU** | 850W 80+ Gold | 3 | $150 | $450 |
| **Case** | 2U Rackmount | 3 | $200 | $600 |
| **Subtotal** | | | | **$8,250** |

**Networking Equipment**

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| **Core Switch** | 48-port 10GbE Arista 7050SX3 | 2 | $8,000 | $16,000 |
| **Storage Switch** | 24-port 25GbE Mellanox SN2700 | 2 | $5,000 | $10,000 |
| **Load Balancer** | F5 BIG-IP Virtual Edition or HAProxy | 2 | $3,000 | $6,000 |
| **Firewall** | Netgate 8200 (pfSense) | 2 | $2,500 | $5,000 |
| **SFP+ Modules** | 10GbE transceivers | 80 | $50 | $4,000 |
| **DAC Cables** | 10GbE 3m copper | 60 | $30 | $1,800 |
| **Fiber Cables** | 25GbE 10m | 30 | $50 | $1,500 |
| **Rack** | 42U server rack with PDU | 2 | $1,500 | $3,000 |
| **UPS** | 10KVA UPS (3-hour runtime) | 2 | $5,000 | $10,000 |
| **Subtotal** | | | | **$57,300** |

**Central Cloud Total:** $131,910

---

#### Edge Site Hardware (Per Site × 20)

**Compute Nodes (2 per site for HA)**

**Option A: Budget (Orange Pi 5 Plus)**

| Component | Specification | Qty/Site | Unit Price | Site Total | 20 Sites |
|-----------|--------------|----------|------------|------------|----------|
| SBC | Orange Pi 5 Plus 16GB | 2 | $150 | $300 | $6,000 |
| AI Accelerator | Hailo-8 M.2 (26 TOPS) | 2 | $70 | $140 | $2,800 |
| Storage | 2TB NVMe SSD | 2 | $150 | $300 | $6,000 |
| Case | Metal case with fan | 2 | $30 | $60 | $1,200 |
| PSU | USB-C PD 65W | 2 | $25 | $50 | $1,000 |
| **Subtotal** | | | | **$850** | **$17,000** |

**Option B: Performance (NVIDIA Jetson Orin Nano) - RECOMMENDED**

| Component | Specification | Qty/Site | Unit Price | Site Total | 20 Sites |
|-----------|--------------|----------|------------|------------|----------|
| Computer | Jetson Orin Nano 8GB | 2 | $500 | $1,000 | $20,000 |
| Storage | 2TB NVMe SSD | 2 | $150 | $300 | $6,000 |
| Case | Industrial enclosure | 2 | $40 | $80 | $1,600 |
| **Subtotal** | | | | **$1,380** | **$27,600** |

**Option C: High-Performance (NVIDIA Jetson Orin NX)**

| Component | Specification | Qty/Site | Unit Price | Site Total | 20 Sites |
|-----------|--------------|----------|------------|------------|----------|
| Computer | Jetson Orin NX 16GB | 2 | $800 | $1,600 | $32,000 |
| Storage | 2TB NVMe SSD | 2 | $150 | $300 | $6,000 |
| Case | Industrial enclosure | 2 | $50 | $100 | $2,000 |
| **Subtotal** | | | | **$2,000** | **$40,000** |

**Local Storage (per site)**

| Component | Specification | Qty/Site | Unit Price | Site Total | 20 Sites |
|-----------|--------------|----------|------------|------------|----------|
| NAS | Synology DS923+ (4-bay) | 1 | $600 | $600 | $12,000 |
| HDDs | 4×8TB WD Red Plus | 1 set | $800 | $800 | $16,000 |
| **Subtotal** | | | | **$1,400** | **$28,000** |

**Network Equipment (per site)**

| Component | Specification | Qty/Site | Unit Price | Site Total | 20 Sites |
|-----------|--------------|----------|------------|------------|----------|
| PoE Switch | 48-port Gigabit PoE+ (802.3at) | 1 | $500 | $500 | $10,000 |
| Router | Ubiquiti EdgeRouter 6P | 1 | $150 | $150 | $3,000 |
| Firewall | Netgate 2100 (pfSense) | 1 | $200 | $200 | $4,000 |
| UPS | 1500VA (1-hour runtime) | 1 | $300 | $300 | $6,000 |
| **Subtotal** | | | | **$1,150** | **$23,000** |

**Cameras (25 per site)**

**Option A: Budget OpenIPC**

| Component | Specification | Qty/Site | Unit Price | Site Total | 20 Sites |
|-----------|--------------|----------|------------|------------|----------|
| IP Camera | 4MP OpenIPC compatible | 25 | $40 | $1,000 | $20,000 |
| Mounts | Wall/ceiling mount | 25 | $15 | $375 | $7,500 |
| Cables | Cat6 50ft PoE | 25 | $10 | $250 | $5,000 |
| **Subtotal** | | | | **$1,625** | **$32,500** |

**Option B: Commercial Quality - RECOMMENDED**

| Component | Specification | Qty/Site | Unit Price | Site Total | 20 Sites |
|-----------|--------------|----------|------------|------------|----------|
| Fixed Camera | Hikvision 4MP ColorVu (H.265) | 20 | $120 | $2,400 | $48,000 |
| PTZ Camera | Hikvision 4MP PTZ | 5 | $400 | $2,000 | $40,000 |
| Mounts | Professional mounts | 25 | $20 | $500 | $10,000 |
| Cables | Cat6 50ft PoE | 25 | $10 | $250 | $5,000 |
| **Subtotal** | | | | **$5,150** | **$103,000** |

**Option C: High-End Axis**

| Component | Specification | Qty/Site | Unit Price | Site Total | 20 Sites |
|-----------|--------------|----------|------------|------------|----------|
| Fixed Camera | Axis P3245-LVE 4K | 20 | $500 | $10,000 | $200,000 |
| PTZ Camera | Axis Q6128-E 4K PTZ | 5 | $3,000 | $15,000 | $300,000 |
| Mounts | Axis mounts | 25 | $50 | $1,250 | $25,000 |
| Cables | Cat6 50ft PoE | 25 | $10 | $250 | $5,000 |
| **Subtotal** | | | | **$26,500** | **$530,000** |

---

### Enterprise Deployment Totals

**Configuration 1: Budget**
- Central Cloud: $131,910
- 20 Edge Sites (Orange Pi + OpenIPC): $94,500
- **Total: $226,410**

**Configuration 2: Standard (RECOMMENDED)**
- Central Cloud: $131,910
- 20 Edge Sites (Jetson Nano + Commercial): $162,200
- **Total: $294,110**

**Configuration 3: Premium**
- Central Cloud: $131,910
- 20 Edge Sites (Jetson NX + Axis): $641,000
- **Total: $772,910**

---

## SMB Deployment BOM

### Scenario: 50 Cameras, Single Location

**Server (All-in-One)**

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| **CPU** | AMD Ryzen 9 7950X | 1 | $550 | $550 |
| **Motherboard** | ASUS Pro WS X670E | 1 | $500 | $500 |
| **RAM** | 64GB DDR5 (2×32GB) | 1 | $200 | $200 |
| **NVMe SSD** | 2TB (OS + Apps) | 1 | $180 | $180 |
| **Data HDD** | 4×8TB WD Red Plus (RAID 10) | 1 set | $800 | $800 |
| **GPU** | NVIDIA RTX 3060 12GB (Analytics) | 1 | $300 | $300 |
| **Network** | 10GbE NIC | 1 | $150 | $150 |
| **PSU** | 850W 80+ Gold | 1 | $150 | $150 |
| **Case** | Tower case | 1 | $150 | $150 |
| **Subtotal** | | | | **$2,980** |

**Network Equipment**

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| PoE Switch | 48-port Gigabit PoE+ | 2 | $500 | $1,000 |
| Router | Ubiquiti EdgeRouter | 1 | $150 | $150 |
| UPS | 1500VA | 1 | $300 | $300 |
| **Subtotal** | | | | **$1,450** |

**Cameras (50 total)**

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| IP Camera | Hikvision 4MP | 50 | $120 | $6,000 |
| Mounts | Wall mount | 50 | $20 | $1,000 |
| Cables | Cat6 PoE | 50 | $10 | $500 |
| **Subtotal** | | | | **$7,500** |

**SMB Total: $11,930**

---

## Household Deployment BOM

### Scenario: 4 Cameras, Residential

**Compute**

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| SBC | Raspberry Pi 5 8GB | 1 | $80 | $80 |
| AI Accelerator | Google Coral USB | 1 | $60 | $60 |
| Storage | 512GB microSD | 1 | $40 | $40 |
| Case | Official case + fan | 1 | $15 | $15 |
| Power | USB-C 27W power supply | 1 | $12 | $12 |
| **Subtotal** | | | | **$207** |

**Network**

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| PoE Switch | 8-port Gigabit PoE+ | 1 | $80 | $80 |
| **Subtotal** | | | | **$80** |

**Cameras**

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| IP Camera | Reolink 5MP PoE | 4 | $50 | $200 |
| Mounts | Basic mount | 4 | $10 | $40 |
| Cables | Cat6 25ft | 4 | $8 | $32 |
| **Subtotal** | | | | **$272** |

**Household Total: $559**

---

## Open Hardware Options

### Fully Open Hardware Components

**Single Board Computers:**
- **Orange Pi 5 Plus** ($150) - ARM Cortex-A76/A55, 16GB RAM, PCIe
- **Rock 5B** ($180) - RK3588, 16GB RAM, NPU for AI
- **PINE64 ROCKPro64** ($80) - Budget option
- **Raspberry Pi 5** ($80) - Most popular, best support

**RISC-V Servers (Fully Open ISA):**
- **Milk-V Pioneer** ($1,500) - 64-core RISC-V server
- **StarFive VisionFive 2** ($70) - Development board
- **Pine64 Star64** ($70) - Entry-level

**Open Firmware Cameras:**
- **OpenIPC** compatible cameras ($30-50)
- **ESP32-CAM** modules ($10-15) - DIY option

**Networking:**
- **OpenWrt** compatible routers (TP-Link, Ubiquiti)
- **OCP switches** (enterprise, Open Compute Project)

### Pragmatic Proprietary (Performance Justifies Cost)

**AI Acceleration:**
- **NVIDIA Jetson Orin Nano** ($500) - 40 TOPS, best software support
- **NVIDIA Jetson Orin NX** ($800) - 100 TOPS
- **Google Coral Edge TPU** ($60) - Budget option, 4 TOPS

**Why Jetson?** 5x better performance than alternatives, mature software stack, TensorRT optimization

---

## Vendor Matrix

### Recommended Vendors

**SBCs & Edge Compute:**
| Vendor | Products | Website |
|--------|----------|---------|
| Orange Pi | SBCs | orangepi.org |
| Raspberry Pi | Pi 4/5 | raspberrypi.com |
| NVIDIA | Jetson series | nvidia.com |
| Seeed Studio | Coral adapters | seeedstudio.com |

**Servers:**
| Vendor | Products | Website |
|--------|----------|---------|
| Supermicro | Rack servers | supermicro.com |
| System76 | Workstations | system76.com |
| Dell | PowerEdge | dell.com |

**Storage:**
| Vendor | Products | Website |
|--------|----------|---------|
| Seagate | Exos enterprise HDDs | seagate.com |
| WD | Red/Gold drives | westerndigital.com |
| Samsung | NVMe SSDs | samsung.com |

**Networking:**
| Vendor | Products | Website |
|--------|----------|---------|
| Ubiquiti | EdgeRouter, switches | ui.com |
| Arista | 10GbE switches | arista.com |
| Mellanox/NVIDIA | High-speed NICs | nvidia.com/networking |

**Cameras:**
| Vendor | Products | Website |
|--------|----------|---------|
| Hikvision | Commercial IP cameras | hikvision.com |
| Dahua | Commercial IP cameras | dahuasecurity.com |
| Axis | Premium IP cameras | axis.com |
| Reolink | Consumer IP cameras | reolink.com |

### Lead Times

| Category | Lead Time |
|----------|-----------|
| SBCs | 2-4 weeks |
| Servers | 4-8 weeks |
| Storage drives | 1-2 weeks |
| Cameras | 2-6 weeks |
| Networking | 2-4 weeks |

**Critical Path:** Order servers and switches first (longest lead time)

---

## Cost Comparison

### 3-Year TCO by Configuration

**Enterprise (500 cameras):**

| Configuration | Initial | Annual OpEx | 3-Year Total |
|---------------|---------|-------------|--------------|
| Budget | $226,410 | $160,000 | $706,410 |
| **Standard** | **$294,110** | **$175,000** | **$819,110** |
| Premium | $772,910 | $200,000 | $1,372,910 |

**SMB (50 cameras):**

| Configuration | Initial | Annual OpEx | 3-Year Total |
|---------------|---------|-------------|--------------|
| **Standard** | **$11,930** | **$10,000** | **$41,930** |

**Household (4 cameras):**

| Configuration | Initial | Annual OpEx | 3-Year Total |
|---------------|---------|-------------|--------------|
| **Standard** | **$559** | **$120** | **$919** |

### vs. Commercial Solutions

**Enterprise (500 cameras, 3 years):**
- OpenVision Standard: $819,110
- Genetec: $1,015,000
- **Savings: $195,890 (19%)**

Plus unlimited customization and no vendor lock-in.

---

## Procurement Checklist

- [ ] Review hardware BOMs
- [ ] Select appropriate configuration tier
- [ ] Get quotes from vendors
- [ ] Validate lead times
- [ ] Approve budget
- [ ] Place orders (servers and network first)
- [ ] Plan delivery and staging
- [ ] Schedule installation team
- [ ] Verify warranty coverage
- [ ] Document asset inventory

---

**Prepared by:** Infrastructure Team  
**Last Updated:** November 2025  
**Next Review:** Quarterly

**For Questions:** hardware@openvision.io
