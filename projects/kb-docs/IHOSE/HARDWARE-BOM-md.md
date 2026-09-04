---
source_project: IHOSE
source_project_uuid: 019a6ba2-1cf8-703d-b379-bb50cd7fad34
doc_uuid: 7ce13798-93bb-4ddc-83e0-1caf8d204c9d
original_filename: HARDWARE_BOM.md
created_at: 2025-12-02T00:47:54.958277+00:00
content_hash: bce30b2bc93d
---

# OpenVision Platform - Hardware Bill of Materials

**Document Type**: Hardware Specifications & Procurement Guide  
**Version**: 1.0  
**Audience**: Procurement Teams, Technical Planners, Budget Planners

---

## Table of Contents

1. [Enterprise Deployment (500 cameras, 20 sites)](#enterprise-deployment-bom)
2. [SMB Deployment (10-50 cameras)](#smb-deployment-bom)
3. [Household Deployment (1-5 cameras)](#household-deployment-bom)
4. [Hardware Selection Guide](#hardware-selection-guide)
5. [Vendor Directory](#vendor-directory)
6. [Lead Times & Procurement](#lead-times-and-procurement)

---

## Enterprise Deployment BOM

### Configuration: 500 cameras across 20 sites

**Total Investment**: $294,430 (standard tier)

---

### Central Cloud Infrastructure

#### Kubernetes Control Plane (3 nodes for HA)

**Option A: Open Hardware Build** (Recommended)

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| CPU | AMD Threadripper PRO 5975WX (32-core, 3.6GHz) | 3 | $2,400 | $7,200 |
| Motherboard | ASUS Pro WS WRX80E-SAGE SE WIFI | 3 | $800 | $2,400 |
| RAM | 128GB DDR4 ECC (8×16GB, 3200MHz) | 3 | $450 | $1,350 |
| Boot SSD | 1TB NVMe Samsung 990 PRO | 3 | $100 | $300 |
| Network Card | Dual 10GbE Intel X710-DA2 | 3 | $250 | $750 |
| Power Supply | 1200W 80+ Platinum Modular | 3 | $200 | $600 |
| Case | System76 Thelio Major or equivalent | 3 | $300 | $900 |
| **Subtotal** | | | | **$13,500** |

**Option B: Commercial Servers**

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| Server | Dell PowerEdge R750 or HP ProLiant DL380 | 3 | $4,500 | $13,500 |
| - Includes: Dual Xeon Silver 4314, 128GB RAM, Dual 960GB SSD, Dual 10GbE | | | | |
| **Subtotal** | | | | **$13,500** |

#### Worker Nodes (5 nodes, scalable to 20+)

**Standard Configuration**

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| CPU | AMD Ryzen 9 7950X (16-core, 4.5GHz) | 5 | $550 | $2,750 |
| Motherboard | ASUS Pro WS X670E-ACE | 5 | $500 | $2,500 |
| RAM | 64GB DDR5 (2×32GB, 5200MHz) | 5 | $180 | $900 |
| Boot SSD | 1TB NVMe WD Black SN850X | 5 | $120 | $600 |
| GPU (Optional) | NVIDIA T4 16GB (for ML training) | 2 | $2,000 | $4,000 |
| Network Card | Dual 10GbE Intel X710-DA2 | 5 | $250 | $1,250 |
| Power Supply | 850W 80+ Gold Modular | 5 | $150 | $750 |
| Case | Fractal Design Define 7 XL | 5 | $200 | $1,000 |
| **Subtotal** | | | | **$13,750** |

#### Ceph Storage Cluster (6 nodes)

**High-Capacity Configuration**

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| CPU | AMD EPYC 7313P (16-core, 3.0GHz) | 6 | $900 | $5,400 |
| Motherboard | Supermicro H12SSL-i | 6 | $400 | $2,400 |
| RAM | 64GB DDR4 ECC (4×16GB, 3200MHz) | 6 | $280 | $1,680 |
| Boot SSD | 500GB NVMe Samsung 980 | 6 | $60 | $360 |
| Cache SSD | 2×1TB NVMe Samsung 980 PRO (RAID 1) | 6 | $200 | $1,200 |
| Data HDDs | 12×18TB Seagate Exos X18 7200RPM | 6 | $3,600 | $21,600 |
| HBA Card | LSI 9305-16i PCIe 3.0 HBA | 6 | $350 | $2,100 |
| Network Card | Dual 25GbE Mellanox ConnectX-5 | 6 | $400 | $2,400 |
| Power Supply | 1000W 80+ Platinum | 6 | $180 | $1,080 |
| Case | Supermicro 4U 24-bay chassis | 6 | $800 | $4,800 |
| **Subtotal** | | | | **$43,020** |

**Storage Capacity**: 1,296TB raw = 432TB usable (3× replication)  
**Estimated costs per TB**: $99.58/TB usable

#### PostgreSQL HA Cluster (3 nodes)

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| CPU | AMD Ryzen 9 7900X (12-core, 4.7GHz) | 3 | $400 | $1,200 |
| Motherboard | ASUS Pro WS X670E-ACE | 3 | $500 | $1,500 |
| RAM | 128GB DDR5 (4×32GB, 5200MHz) | 3 | $350 | $1,050 |
| NVMe SSD | 2×4TB Samsung 990 PRO (RAID 1) | 3 | $700 | $2,100 |
| Network Card | Dual 10GbE Intel X710-DA2 | 3 | $250 | $750 |
| Power Supply | 850W 80+ Gold | 3 | $150 | $450 |
| Case | Fractal Design Define 7 | 3 | $170 | $510 |
| **Subtotal** | | | | **$7,560** |

#### Central Networking

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| Core Switch | 48-port 10GbE + 4×100GbE uplinks | 2 | $8,000 | $16,000 |
| Storage Switch | 24-port 25GbE (Ceph backend) | 2 | $4,000 | $8,000 |
| Load Balancer | HA pair (HAProxy appliance or VMs) | 2 | $3,000 | $6,000 |
| Firewall | pfSense appliance or Netgate 8200 | 2 | $2,500 | $5,000 |
| Cables | SFP+ DAC 10GbE (1m, 3m), SFP28 25GbE | 100 | $30 | $3,000 |
| Rack | 42U server rack with PDU and cable mgmt | 2 | $1,500 | $3,000 |
| **Subtotal** | | | | **$41,000** |

**Central Cloud Total: $118,830**

---

### Edge Sites (20 sites × 25 cameras each)

#### Per-Site Compute Nodes (2× per site for HA)

**Option A: Budget (Orange Pi 5 Plus + Hailo-8)**

| Component | Specification | Qty/Site | Unit Price | Site Total | 20 Sites |
|-----------|--------------|----------|------------|------------|----------|
| SBC | Orange Pi 5 Plus 16GB | 2 | $150 | $300 | $6,000 |
| AI Accelerator | Hailo-8 M.2 (26 TOPS) | 2 | $70 | $140 | $2,800 |
| Storage | 2TB NVMe SSD | 2 | $150 | $300 | $6,000 |
| Case | Metal case with cooling | 2 | $30 | $60 | $1,200 |
| Power Supply | USB-C PD 65W | 2 | $25 | $50 | $1,000 |
| **Subtotal** | | | | **$850** | **$17,000** |

**Option B: Performance (NVIDIA Jetson Orin Nano)** (Recommended)

| Component | Specification | Qty/Site | Unit Price | Site Total | 20 Sites |
|-----------|--------------|----------|------------|------------|----------|
| Computer | NVIDIA Jetson Orin Nano Dev Kit (8GB) | 2 | $500 | $1,000 | $20,000 |
| Storage | 2TB NVMe SSD Samsung 980 | 2 | $150 | $300 | $6,000 |
| Case | Industrial enclosure with cooling | 2 | $40 | $80 | $1,600 |
| **Subtotal** | | | | **$1,380** | **$27,600** |

**Option C: High-Performance (NVIDIA Jetson Orin NX)**

| Component | Specification | Qty/Site | Unit Price | Site Total | 20 Sites |
|-----------|--------------|----------|------------|------------|----------|
| Computer | NVIDIA Jetson Orin NX 16GB | 2 | $800 | $1,600 | $32,000 |
| Storage | 2TB NVMe SSD Samsung 990 PRO | 2 | $150 | $300 | $6,000 |
| Case | Industrial enclosure | 2 | $50 | $100 | $2,000 |
| **Subtotal** | | | | **$2,000** | **$40,000** |

#### Per-Site Local Storage

| Component | Specification | Qty/Site | Unit Price | Site Total | 20 Sites |
|-----------|--------------|----------|------------|------------|----------|
| NAS | Synology DS923+ 4-bay or equivalent | 1 | $600 | $600 | $12,000 |
| HDDs | 4×8TB WD Red Plus (RAID 10) | 1 | $800 | $800 | $16,000 |
| **Subtotal** | | | | **$1,400** | **$28,000** |

**Effective storage per site**: 16TB (RAID 10) = 8TB usable

#### Per-Site Networking

| Component | Specification | Qty/Site | Unit Price | Site Total | 20 Sites |
|-----------|--------------|----------|------------|------------|----------|
| PoE Switch | 48-port Gigabit PoE+ (802.3at, 370W) | 1 | $500 | $500 | $10,000 |
| Router | OpenWrt-compatible (Ubiquiti EdgeRouter 4) | 1 | $150 | $150 | $3,000 |
| VPN Gateway | WireGuard appliance or pfSense VM | 1 | $200 | $200 | $4,000 |
| **Subtotal** | | | | **$850** | **$17,000** |

#### Cameras (25 per site)

**Option A: Budget (OpenIPC Firmware)**

| Component | Specification | Qty/Site | Unit Price | Site Total | 20 Sites |
|-----------|--------------|----------|------------|------------|----------|
| IP Camera | 4MP with HiSilicon chip (OpenIPC compatible) | 25 | $40 | $1,000 | $20,000 |
| Mounts | Universal wall/ceiling mount | 25 | $15 | $375 | $7,500 |
| Cables | Cat6 50ft PoE cable | 25 | $10 | $250 | $5,000 |
| **Subtotal** | | | | **$1,625** | **$32,500** |

**Option B: Commercial Quality** (Recommended)

| Component | Specification | Qty/Site | Unit Price | Site Total | 20 Sites |
|-----------|--------------|----------|------------|------------|----------|
| Fixed Camera | Hikvision 4MP ColorVu (H.265, 80m IR) | 20 | $120 | $2,400 | $48,000 |
| PTZ Camera | Hikvision 4MP PTZ (25× zoom, 150m IR) | 5 | $400 | $2,000 | $40,000 |
| Mounts | Professional mounts with junction boxes | 25 | $20 | $500 | $10,000 |
| Cables | Cat6 50ft outdoor-rated PoE cable | 25 | $10 | $250 | $5,000 |
| **Subtotal** | | | | **$5,150** | **$103,000** |

**Option C: Premium (Axis Communications)**

| Component | Specification | Qty/Site | Unit Price | Site Total | 20 Sites |
|-----------|--------------|----------|------------|------------|----------|
| Fixed Camera | Axis P3245-LVE 4K (Forensic WDR, Zipstream) | 20 | $500 | $10,000 | $200,000 |
| PTZ Camera | Axis Q6128-E 4K PTZ (31× zoom, 250m IR) | 5 | $3,000 | $15,000 | $300,000 |
| Mounts | Axis mounts and outdoor housings | 25 | $50 | $1,250 | $25,000 |
| Cables | Cat6 50ft shielded PoE cable | 25 | $10 | $250 | $5,000 |
| **Subtotal** | | | | **$26,500** | **$530,000** |

---

### Configuration Summaries

#### Budget Configuration
**Total**: $213,330
- Central Cloud: $118,830
- Edge (Orange Pi + OpenIPC): $94,500

#### Standard Configuration (Recommended)
**Total**: $294,430
- Central Cloud: $118,830
- Edge (Jetson Nano + Commercial cams): $175,600

#### Premium Configuration
**Total**: $733,830
- Central Cloud: $118,830
- Edge (Jetson NX + Axis cams): $615,000

---

## SMB Deployment BOM

### Configuration: 10-50 cameras, single site

**Total Investment**: $5,000-15,000

### Option A: On-Premise Server

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| **Server** | Dell PowerEdge T340 or equivalent | 1 | $2,500 | $2,500 |
| - CPU | Intel Xeon E-2234 (4-core, 3.6GHz) | Included | - | - |
| - RAM | 32GB DDR4 ECC | Included | - | - |
| - Storage | 2×4TB HDD (RAID 1) | Included | - | - |
| - Boot | 500GB SSD | Included | - | - |
| **Network** | 24-port PoE+ switch (Ubiquiti USW-24-POE) | 1 | $500 | $500 |
| **UPS** | 1500VA UPS with AVR | 1 | $300 | $300 |
| **Cameras** | 20× 4MP IP cameras (Hikvision DS-2CD2343G2-I) | 20 | $100 | $2,000 |
| **Cabling** | Cat6 cables, mounts, installation labor | - | - | $1,500 |
| **Total** | | | | **$6,800** |

### Option B: Cloud Deployment

| Component | Specification | Monthly | Annual (×12) | 3-Year |
|-----------|--------------|---------|--------------|--------|
| **Compute** | 4 vCPU, 16GB RAM (AWS, GCP, or Azure) | $80 | $960 | $2,880 |
| **Storage** | 2TB SSD block storage | $200 | $2,400 | $7,200 |
| **Bandwidth** | 5TB egress | $50 | $600 | $1,800 |
| **Backup** | 500GB snapshot backup | $25 | $300 | $900 |
| **Total** | | **$355/mo** | **$4,260/yr** | **$12,780** |

Plus cameras: $2,000 (one-time)  
**3-Year TCO**: $14,780

**Recommendation**: On-premise for 3+ year deployments

---

## Household Deployment BOM

### Configuration: 1-5 cameras

**Total Investment**: $300-500

### Recommended Setup

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| **Compute** | Raspberry Pi 4 (8GB) | 1 | $75 | $75 |
| **AI** | Google Coral USB TPU Accelerator | 1 | $60 | $60 |
| **Storage** | 500GB External SSD (USB 3.0) | 1 | $60 | $60 |
| **Power** | Official Raspberry Pi Power Supply | 1 | $10 | $10 |
| **Case** | Aluminum case with fan | 1 | $15 | $15 |
| **Cameras** | 1080p IP cameras (OpenIPC compatible) | 3 | $40 | $120 |
| **Network** | Cat6 cables (50ft × 3), PoE injectors | - | - | $60 |
| **Total** | | | | **$400** |

### Budget Alternative

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| **Compute** | Raspberry Pi 4 (4GB) | 1 | $55 | $55 |
| **Storage** | 256GB microSD card (Class 10) | 1 | $25 | $25 |
| **Cameras** | 720p IP cameras (generic) | 2 | $30 | $60 |
| **Network** | Cat6 cables, PoE injectors | - | - | $40 |
| **Total** | | | | **$180** |

### Premium Alternative

| Component | Specification | Qty | Unit Price | Total |
|-----------|--------------|-----|------------|-------|
| **Compute** | NVIDIA Jetson Nano 4GB | 1 | $150 | $150 |
| **Storage** | 1TB NVMe SSD with adapter | 1 | $120 | $120 |
| **Cameras** | 4K IP cameras (Hikvision) | 3 | $150 | $450 |
| **Network** | Cat6 cables, PoE switch (5-port) | - | - | $80 |
| **Total** | | | | **$800** |

---

## Hardware Selection Guide

### CPU Selection

**For Central Cloud**:
- **AMD Threadripper PRO**: Best performance, PCIe lanes
- **AMD EPYC**: Server-grade, massive core counts
- **Intel Xeon Scalable**: Good compatibility, mature platform

**For Edge Nodes**:
- **Orange Pi 5**: Budget, ARM, good performance
- **NVIDIA Jetson**: Best for AI, proven platform
- **RISC-V (Milk-V)**: Fully open, emerging platform

### AI Accelerator Selection

| Accelerator | TOPS | Price | Use Case |
|-------------|------|-------|----------|
| **Google Coral USB** | 4 | $60 | Household, light workload |
| **Hailo-8** | 26 | $70 | SMB, moderate workload |
| **NVIDIA Jetson Nano** | 472 GFLOPS | $150 | Good all-around |
| **NVIDIA Jetson Orin Nano** | 40 | $500 | Edge enterprise |
| **NVIDIA Jetson Orin NX** | 100 | $800 | Heavy analytics |
| **NVIDIA T4** | 65 | $2,000 | Data center training |

### Storage Selection

**Hot Storage** (0-7 days):
- NVMe SSD (Samsung 980 PRO, WD Black)
- Target: 500+ MB/s sustained write

**Warm Storage** (7-30 days):
- Enterprise HDD (Seagate Exos, WD Gold)
- 7200 RPM minimum
- 256MB+ cache

**Cold Storage** (30+ days):
- Ceph distributed storage
- Object storage (MinIO)
- Lower-cost HDDs acceptable

### Network Equipment

**For SMB**:
- Ubiquiti UniFi switches (good value)
- TP-Link managed switches (budget)
- Netgear M4250 (prosumer)

**For Enterprise**:
- Cisco Catalyst 9000 series
- Arista switches
- Mellanox/NVIDIA for high-speed storage network

---

## Vendor Directory

### Compute Hardware

**Systems Integrators**:
- System76 (open hardware, coreboot): https://system76.com
- Supermicro: https://www.supermicro.com
- Dell: https://www.dell.com/servers
- HP: https://www.hpe.com/servers

**DIY Components**:
- Newegg: https://www.newegg.com
- Amazon Business: https://business.amazon.com
- B&H Photo: https://www.bhphotovideo.com

### Edge Compute

**SBCs**:
- Raspberry Pi: https://www.raspberrypi.com
- Orange Pi: http://www.orangepi.org (via AliExpress)
- NVIDIA Jetson: https://www.nvidia.com/jetson
- Milk-V (RISC-V): https://milkv.io

**AI Accelerators**:
- Google Coral: https://coral.ai
- Hailo: https://hailo.ai
- NVIDIA: https://www.nvidia.com

### Storage

**Enterprise HDDs**:
- Seagate (direct): https://www.seagate.com
- Western Digital: https://www.westerndigital.com
- Amazon: https://www.amazon.com/drives

**SSDs**:
- Samsung: https://www.samsung.com/ssd
- Western Digital: https://www.westerndigital.com/ssd
- Crucial: https://www.crucial.com

### Networking

**Switches & Routers**:
- Ubiquiti: https://ui.com
- TP-Link: https://www.tp-link.com/business
- Cisco: https://www.cisco.com (via resellers)
- Netgear: https://www.netgear.com/business

**NICs**:
- Intel: https://www.intel.com/network-adapters
- Mellanox (NVIDIA): https://www.nvidia.com/networking

### Cameras

**Commercial Cameras**:
- Hikvision: https://www.hikvision.com
- Dahua: https://www.dahuasecurity.com
- Axis Communications: https://www.axis.com
- Hanwha (Samsung): https://www.hanwhasecurity.com

**Open Hardware Cameras**:
- OpenIPC compatible (search AliExpress/Amazon)
- ESP32-CAM modules (DIY)

---

## Lead Times and Procurement

### Typical Lead Times

| Category | Lead Time | Notes |
|----------|-----------|-------|
| **Standard PCs/Servers** | 1-2 weeks | In-stock items |
| **Custom Servers** | 4-8 weeks | Build-to-order |
| **SBCs (Pi, Orange Pi)** | 2-4 weeks | Stock varies |
| **NVIDIA Jetson** | 2-6 weeks | Often backordered |
| **Enterprise HDDs** | 1-2 weeks | Usually in stock |
| **SSDs** | 1 week | Commodity item |
| **Cameras (Hikvision)** | 2-4 weeks | Via distributor |
| **Cameras (Axis)** | 4-8 weeks | Premium brand |
| **Network Equipment** | 2-4 weeks | Varies by model |

### Procurement Tips

1. **Order early**: Some items (Jetson) often have long lead times
2. **Buy from authorized distributors**: Especially for cameras
3. **Consider alternatives**: Have backup options for each component
4. **Bulk discounts**: 20+ cameras often get 10-20% discount
5. **Warranty**: Enterprise drives worth the premium
6. **Support contracts**: Consider for network equipment

### Budget Planning

**Add 15-20% contingency** for:
- Price fluctuations
- Shipping costs
- Import duties (if applicable)
- Installation labor
- Miscellaneous (cables, mounts, tools)

### Financing Options

**Leasing**: 
- 3-year lease typical for enterprise
- ~30% higher TCO but preserves capital
- Includes refresh cycle

**Vendor Financing**:
- Dell, HP offer 0% for 12-24 months
- Good for managing cash flow

---

## Cost Comparison

### 3-Year Total Cost of Ownership

#### Enterprise (500 cameras)

**OpenVision Standard**: $774,430
- Hardware: $294,430
- Personnel (2 engineers): $480,000
- Power/cooling: Included
- No licensing fees

**Commercial VMS (Genetec)**: $1,120,000
- Licensing: $150,000
- Hardware: $250,000
- Maintenance: $90,000 (20%/year × 3)
- Personnel: $480,000
- Customization: $150,000 (limited)

**Savings**: $345,570 (31%)

#### SMB (20 cameras)

**OpenVision On-Premise**: $10,400
- Hardware: $6,800
- 3-year power: $600
- Part-time IT: $3,000

**Cloud VMS (Verkada)**: $22,800
- Cameras: $3,000 (proprietary required)
- Subscription: $40/cam/month × 20 × 36 = $28,800
- Less: Hardware savings: -$9,000

**Savings**: $12,400 (54%)

---

## Next Steps

1. **Review configurations** and select appropriate tier
2. **Get quotes** from vendors (use this as RFQ)
3. **Plan installation** timeline
4. **Order long-lead items** first (Jetson, cameras)
5. **Prepare infrastructure** (network, power)

---

**Document Version**: 1.0  
**Last Updated**: November 2024  
**Maintained By**: Procurement Team

**Questions?**
- Technical: architecture@openvision.io
- Procurement: procurement@openvision.io
- Sales quotes: sales@openvision.io
