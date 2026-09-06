---
source_project: Open Vision
source_project_uuid: 019adc89-3095-77fb-a6f8-3f599d84699a
doc_uuid: 92514048-effd-48a0-b944-094d0dbd3b7b
original_filename: 02-Hardware-Specifications.docx
created_at: 2025-12-02T00:49:43.372478+00:00
content_hash: 4abbe80d440f
status: duplicate
duplicate_of: "knowledge-base/d-central/hardware/sensing-planes/IHOSE/02-Hardware-Specifications-docx.md"
duplicate_reason: exact content_hash match, different category (same doc uploaded to multiple Claude Projects)
---

OpenVision Platform

**Hardware Specifications & Bill of Materials**

Open Hardware & Hybrid Architecture Guide

Version 1.0

Hardware Philosophy

OpenVision Platform is designed to operate on diverse hardware
platforms, from fully open RISC-V systems to pragmatic hybrid
configurations incorporating proprietary components where performance
justifies the investment. This document provides comprehensive hardware
specifications, Bill of Materials, and deployment recommendations for
various scales and use cases.

Open vs. Proprietary Trade-offs

  -----------------------------------------------------------------------
  **Component**     **Open Hardware Option**   **Pragmatic Proprietary**
  ----------------- -------------------------- --------------------------
  **CPU             RISC-V (StarFive, Milk-V)  AMD x86 (better
  Architecture**                               performance)

  **Edge Compute**  Orange Pi 5, Rock 5B       Raspberry Pi 5 (best
                                               support)

  **AI              Coral TPU (\$60)           NVIDIA Jetson (5-10x
  Accelerator**                                faster)

  **Cameras**       OpenIPC firmware (\$30)    Hikvision/Axis
                                               (reliability)

  **Storage         No open alternative        Enterprise HDD required
  Drives**                                     
  -----------------------------------------------------------------------

Small Deployment (5-20 Cameras)

Ideal for small businesses, branch offices, or residential properties.
Single-node deployment with optional edge processing.

Configuration A: Maximum Open Hardware

  -----------------------------------------------------------------------
  **Component**           **Model**         **Qty**     **Price**
  ----------------------- ----------------- ----------- -----------------
  **Compute Node**        Orange Pi 5 Plus  1           \$150
                          (16GB)                        

  AI Accelerator          Google Coral TPU  1           \$60
                          (USB)                         

  Storage                 2x 4TB WD Red HDD 2           \$200

  NVMe SSD (OS)           512GB M.2 NVMe    1           \$50

  IP Cameras              OpenIPC           10          \$300
                          compatible 1080p              

  Network Switch          16-port Gigabit   1           \$120
                          PoE                           

  Router                  OpenWrt           1           \$60
                          compatible                    

  **TOTAL**                                             **\$940**
  -----------------------------------------------------------------------

**Specifications:**

-   Handles 10-20 cameras @ 1080p with motion detection

-   30-day video retention on 8TB storage

-   Real-time object detection on 2-4 streams via Coral TPU

-   90% open hardware components

Configuration B: Pragmatic Performance

  -----------------------------------------------------------------------
  **Component**           **Model**         **Qty**     **Price**
  ----------------------- ----------------- ----------- -----------------
  **Compute Node**        Intel NUC i5/16GB 1           \$500

  AI Accelerator          NVIDIA Jetson     1           \$500
                          Orin Nano                     

  Storage                 2x 4TB Seagate    2           \$240
                          Exos                          

  NVMe SSD                512GB Samsung 980 1           \$70
                          Pro                           

  IP Cameras              Hikvision 4MP     15          \$1,200
                          (mix)                         

  Network Switch          24-port Gigabit   1           \$180
                          PoE                           

  **TOTAL**                                             **\$2,690**
  -----------------------------------------------------------------------

**Specifications:**

-   Handles 20-30 cameras @ 4MP with continuous recording

-   Real-time AI on 10+ streams simultaneously (Jetson Orin)

-   Superior camera image quality and low-light performance

-   3x performance of Configuration A

Medium Deployment (50-100 Cameras)

Multi-site deployment with edge processing at each location and central
management server. Typical for retail chains, manufacturing facilities,
or campus environments.

Per-Site Edge Node Configuration

  -----------------------------------------------------------------------
  **Component**           **Model**         **Qty**     **Price**
  ----------------------- ----------------- ----------- -----------------
  **Edge Server**         Radxa ROCK 5 ITX  1           \$200

  AI Accelerator          NVIDIA Jetson     1           \$800
                          Orin NX                       

  Local Storage           2TB NVMe SSD      1           \$150

  IP Cameras              Hikvision 4MP     20          \$1,600

  Network Switch          24-port PoE       1           \$200
                          managed                       

  **TOTAL PER SITE**                                    **\$2,950**
  -----------------------------------------------------------------------

Each edge node handles 15-25 cameras with local recording, AI analytics,
and IoT integration. Operates independently for 7+ days without
connectivity to central server.

Central Management Server

  -----------------------------------------------------------------------
  **Component**           **Model**         **Qty**     **Price**
  ----------------------- ----------------- ----------- -----------------
  **Server**              System76 Thelio   1           \$1,800
                          (Ryzen 9)                     

  RAM                     64GB DDR4 ECC     1           Included

  Storage                 6x 8TB Seagate    6           \$1,200
                          Exos                          

  NVMe Cache              2x 2TB Samsung    2           \$400
                          980 Pro                       

  10GbE NIC               Intel X550-T2     1           \$250

  **TOTAL CENTRAL**                                     **\$3,650**
  -----------------------------------------------------------------------

**Total Deployment Cost (4 sites, 80 cameras):**

-   4 Edge Nodes @ \$2,950 = \$11,800

-   1 Central Server = \$3,650

-   **Total: \$15,450**

Large Enterprise (500+ Cameras)

Data center infrastructure with distributed edge nodes, redundant
storage, and high-availability configuration. Kubernetes-based
orchestration across multiple sites.

Kubernetes Cluster Nodes

  -------------------------------------------------------------------------
  **Component**           **Specification**   **Qty**     **Price**
  ----------------------- ------------------- ----------- -----------------
  **Master Nodes**        Dell R640 (Xeon     3           \$12,000
                          Gold)                           

  **Worker Nodes**        Dell R740 (128GB    10          \$50,000
                          RAM)                            

  **GPU Nodes**           4x NVIDIA A100 per  4           \$80,000
                          node                            

  **Storage Cluster**     Ceph 10 nodes, 20TB 10          \$60,000
                          each                            

  Network Infrastructure  10/40GbE switches,  \-          \$30,000
                          cabling                         

  Edge Nodes              Jetson clusters, 25 25          \$50,000
                          sites                           

  Cameras                 Mix Axis/Hikvision  500         \$50,000

  **TOTAL**                                               **\$332,000**
  -------------------------------------------------------------------------

**Specifications:**

-   500-1000 cameras across 25 sites

-   200TB usable storage (with Ceph 3x replication)

-   Real-time AI on 200+ concurrent streams

-   99.9% uptime with HA configuration

-   Edge autonomy: 30+ days per site

Open Hardware Recommendations

RISC-V Processors

RISC-V represents the future of truly open computing with no proprietary
instruction sets or licensing restrictions.

**StarFive VisionFive 2**

-   Quad-core RISC-V 64-bit @ 1.5GHz

-   8GB LPDDR4, PCIe 2.0

-   Best for: Edge nodes, development, light workloads

-   \$75

**Milk-V Pioneer**

-   64-core RISC-V server-grade processor

-   Up to 128GB DDR4, PCIe 4.0

-   Best for: Central servers, full open-source deployments

-   \$1,500

ARM Open Hardware

**Orange Pi 5 Plus**

-   Rockchip RK3588 (8-core ARM)

-   16GB RAM, 6 TOPS NPU, PCIe 3.0

-   Best for: Edge AI nodes, excellent price/performance

-   \$130

**Rock 5B**

-   Same RK3588 chip, better I/O

-   Up to 16GB RAM, M.2 slots

-   Best for: Edge servers with storage needs

-   \$180

AI Accelerators

**Google Coral Edge TPU**

-   4 TOPS, TensorFlow Lite optimized

-   USB or M.2 form factor

-   Best for: Edge inference, low power

-   \$60 (USB), \$25 (M.2)

**Hailo-8 AI Accelerator**

-   26 TOPS, M.2 form factor

-   Better performance than Coral

-   Best for: Multi-camera edge nodes

-   \$70

IP Cameras with Open Firmware

OpenIPC is an open-source firmware that replaces stock firmware on many
inexpensive IP cameras, providing full ONVIF support and RTSP streaming.

**Supported Chipsets:**

-   HiSilicon Hi3516Ev200/300 - Most common, good support

-   Goke GK7205V200 - Budget option

-   Ingenic T31 - Low power, outdoor

**Where to Buy:**

-   AliExpress: Search \'Hi3516Ev300 camera\' (\$30-40)

-   OpenIPC wiki lists compatible models

-   Flash firmware via TFTP (detailed guides available)

Conclusion

OpenVision Platform can be deployed on a spectrum ranging from fully
open RISC-V hardware to pragmatic hybrid configurations. The choice
depends on project priorities: maximum openness, best performance, or
optimal cost.

For most deployments, we recommend a hybrid approach: open hardware for
edge nodes and management infrastructure (Orange Pi, Rock 5B, System76
servers) combined with strategic use of proprietary AI accelerators
(NVIDIA Jetson) where performance justifies the investment. This
balances philosophical commitment to openness with practical performance
requirements.

As the RISC-V ecosystem matures and open AI accelerators improve, fully
open deployments will become increasingly viable for production
workloads. For now, OpenVision Platform provides the flexibility to make
pragmatic trade-offs while maintaining the option to transition to fully
open hardware as it becomes available.


<!-- AUTO-GENERATED RELATED START (scripts/build_obsidian_graph.py) -->

## Related (auto-generated)

**Duplicate of:** [[knowledge-base/d-central/hardware/sensing-planes/IHOSE/02-Hardware-Specifications-docx]]

<!-- AUTO-GENERATED RELATED END -->
