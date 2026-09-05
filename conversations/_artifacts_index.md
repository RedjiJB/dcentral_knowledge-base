# Conversation-Artifact Extraction (Stage 2 gap-fill)

Scanned all 743 conversations' `create_file` tool-use blocks for DC-*-NNN/OS-*-NNN-pattern document filenames -- artifacts created inline in a conversation and never uploaded to any Project's knowledge base, so Stage 2's original project-KB extraction (`extract_project_docs.py`) had no way to find them.

**44 new documents extracted** to `conversations/artifacts/`. 3 already present in `docs/` (skipped, not re-extracted). 0 matched the naming pattern but had empty content (skipped).

| Doc ID | Filename | Conversation | Created |
|---|---|---|---|
| DC-AGD-001 | `DC-AGD-001_open_gunshot_detector.md` | Modern police | 2026-06-20 |
| DC-AGD-002 | `DC-AGD-002_governance_data_sdk_network-effects.md` | Modern police | 2026-06-20 |
| DC-AGD-003 | `DC-AGD-003_skyledger_DFR_integration.md` | Modern police | 2026-06-20 |
| DC-AGENT-001 | `DC-AGENT-001-Architecture-Memory-Orchestration.md` | Coworker sessions context | 2026-08-16 |
| DC-B2B-001 | `DC-B2B-001_v1.0_B2BExpansion.md` | Fixing operational visibility in decentralized construction | 2026-06-10 |
| DC-CAMPUS-001 | `DC-CAMPUS-001_Neighbourhood_Campus_Master_Spec.md` | Mobile SOC center setup options | 2026-07-22 |
| DC-COMPUTE-001 | `DC-COMPUTE-001_nvidia_capability_revenue_network-effects.md` | Modern police | 2026-06-20 |
| DC-COOP-001 | `DC-COOP-001_v1.0_SodBoys_FullRebuild.md` | Fixing operational visibility in decentralized construction | 2026-06-10 |
| DC-COOP-001 | `DC-COOP-001_v2.0_SodBoys_FullExpansion.md` | Fixing operational visibility in decentralized construction | 2026-06-10 |
| DC-DEV-001 | `DC-DEV-001_Mesh_Native_Developer_Platform.md` | Mobile SOC center setup options | 2026-07-22 |
| DC-ENTERPRISE-001 | `DC-ENTERPRISE-001_v1.0_WhiteLabel.md` | Fixing operational visibility in decentralized construction | 2026-06-10 |
| DC-FOS-001 | `DC-FOS-001_v1.0_SodBoys.md` | Fixing operational visibility in decentralized construction | 2026-06-10 |
| DC-FRACTAL-001 | `DC-FRACTAL-001_Fractal_Cell_Architecture.md` | Mobile SOC center setup options | 2026-07-22 |
| DC-GOV-002 | `DC-GOV-002_Conglomerate_Governance_Architecture.md` | Mobile SOC center setup options | 2026-07-22 |
| DC-INFRA-001 | `DC-INFRA-001_Infrastructure_Map_v1.0.md` | SkyLedger and XaaS model recall | 2026-06-10 |
| DC-LIC-001 | `DC-LIC-001_Regulated_Licensing_Pathway.md` | Mobile SOC center setup options | 2026-07-22 |
| DC-LKF-001 | `DC-LKF-001_Lakou_Fraternity_Network.md` | Creating third places for men | 2026-07-28 |
| DC-MOGUL-001 | `DC-MOGUL-001_Principal_Track_Protocol.md` | Mobile SOC center setup options | 2026-07-22 |
| DC-MONETARY-001 | `DC-MONETARY-001_Multi_Tier_Currency_Architecture.md` | Mesh Home | 2026-05-07 |
| DC-MSOC-001 | `DC-MSOC-001_Mobile_SOC_Specification.md` | Mobile SOC center setup options | 2026-07-22 |
| DC-NETINFRA-001 | `DC-NETINFRA-001_v1.0_NetworkInfrastructure.md` | Fixing operational visibility in decentralized construction | 2026-06-10 |
| DC-OS-001 | `DC-OS-001_Ecosystem_Operating_System.md` | Mobile SOC center setup options | 2026-07-22 |
| DC-OS-002 | `DC-OS-002_Interoperability_Protocol.md` | Mobile SOC center setup options | 2026-07-22 |
| DC-PROCUREMENT-001 | `DC-PROCUREMENT-001.md` | Building projects from documentation to implementation | 2026-07-06 |
| DC-REG-001 | `DC-REG-001-Master-Registry-v0.2.md` | Processing conversation exports and registry setup | 2026-08-23 |
| DC-REG-001 | `DC-REG-001-Master-Registry.md` | D-Central ISP implementation in Haiti | 2026-08-13 |
| DC-REINVEST-001 | `DC-REINVEST-001-Corporate-Procurement-Plan.md` | Coworker sessions context | 2026-08-16 |
| DC-REINVEST-002 | `DC-REINVEST-002-Full-Immediate-Buildout.md` | Coworker sessions context | 2026-08-16 |
| DC-REINVEST-003 | `DC-REINVEST-003-Master-Procurement-Plan.md` | Coworker sessions context | 2026-08-16 |
| DC-SCOUT-001 | `DC-SCOUT-001_v1.0_ZonePricing.md` | Fixing operational visibility in decentralized construction | 2026-06-10 |
| DC-SHELL-001 | `DC-SHELL-001_open_civic-art_enclosure_gadyen.md` | Modern police | 2026-06-20 |
| DC-SIM-000 | `DC-SIM-000-Index.md` | 💬 I have an idea for the dcentra… | 2026-08-08 |
| DC-SIM-001 | `DC-SIM-001-Fidelity-Reference.md` | 💬 I have an idea for the dcentra… | 2026-08-08 |
| DC-SIM-002 | `DC-SIM-002-Topology-Build-Spec.md` | 💬 I have an idea for the dcentra… | 2026-08-08 |
| DC-SIM-003 | `DC-SIM-003-DCOS-Build-Spec.md` | 💬 I have an idea for the dcentra… | 2026-08-08 |
| DC-SIM-004 | `DC-SIM-004-Test-Scenario-Catalogue.md` | 💬 I have an idea for the dcentra… | 2026-08-08 |
| DC-SIM-005 | `DC-SIM-005-Cloud-Bridge-External-Integration.md` | 💬 I have an idea for the dcentra… | 2026-08-08 |
| DC-SIM-006 | `DC-SIM-006-Hardware-Integration-Roadmap.md` | 💬 I have an idea for the dcentra… | 2026-08-08 |
| DC-SIM-007 | `DC-SIM-007-DAO-Governance-Simulation.md` | 💬 I have an idea for the dcentra… | 2026-08-08 |
| DC-SIM-008 | `DC-SIM-008-Open-Architecture-Decisions.md` | 💬 I have an idea for the dcentra… | 2026-08-08 |
| DC-SIM-009 | `DC-SIM-009-Architecture-Decision-Records.md` | 💬 I have an idea for the dcentra… | 2026-08-08 |
| DC-SKY-001 | `DC-SKY-001_SkyLedger_v1.0.md` | SkyLedger and XaaS model recall | 2026-06-10 |
| DC-TPL-000 | `DC-TPL-000_Template_Standard.md` | Mobile SOC center setup options | 2026-07-22 |
| DC-VENTURE-001 | `DC-VENTURE-001_Venture_Sequencing_Registry.md` | Mobile SOC center setup options | 2026-07-22 |

## Already extracted (skipped)

- DC-LKB-001 (`DC-LKB-001_Lakou_Family_Banking_Protocol.md`) -- already in `docs/`
- DC-LKB-002 (`DC-LKB-002_Lakou_Technical_Specification.md`) -- already in `docs/`
- DC-LKB-003 (`DC-LKB-003_Lakou_Protocol_v2_Universal_Banking_OS.md`) -- already in `docs/`
