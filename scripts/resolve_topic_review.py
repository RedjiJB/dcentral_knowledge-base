#!/usr/bin/env python3
"""
Subject-check pass over the 59 first-pass topic clusters from topic_synthesis.py,
per DC-TOPIC-SYNTH-STD-001 SS4's calibration test: can you write one honest 2-4
sentence abstract for this cluster without "and" joining two unrelated ideas?

Every cluster was read (titles + spot-checked content) and given one of four
verdicts, same discipline as the Stage 4 dedup review resolution:

  - CONFIRM (rename only): cluster is coherent, gets a real name instead of
    the placeholder keyword-join.
  - SPLIT: cluster silently merged two unrelated subjects via shared
    vocabulary (e.g. CivicMesh's own registry docs got merged with an
    unrelated Local-Fediverse academic-platform cluster; Open-Secure sector
    overviews got merged with an unrelated "Iron Horse" ecosystem cluster).
  - MERGE: several small clusters were actually one topic split by a
    superficial difference (four separate "presentation deck" clusters by
    audience, when audience isn't a different subject).
  - DEMOTE: a single doc inside an otherwise-coherent cluster didn't
    actually belong (e.g. a broad "Master Strategy" doc pulled into a
    narrow "B2B vehicle programme" cluster by shared vocabulary) -- moved
    to ungrouped rather than force-fit.

Full reasoning per verdict: registry/dedup-review/../TOPIC-RESOLUTION.md
(written by this script). This REPLACES the topic: field and _topics.md
output from topic_synthesis.py's first pass -- it does not layer on top.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_DIR = REPO_ROOT / "knowledge-base"

# category -> { topic_slug: [relative paths within category dir] }
FINAL_TOPICS = {
    "academic-training": {
        "comptia-a-learning-platform": [
            "Comptia-A/Comptia-A-Master-Platform.md",
            "Comptia-A/marketing-site-html.md",
        ],
    },
    "ai-ml-research": {
        "federation-sovereignty-cooperative-platforms": [
            "Federated-Learning-Platform/comprehensive-educational-sovereignty-md.md",
            "Federated-Learning-Platform/Enhanced-Educational-Sovereignty-Framework-Complete-Technical-Integration-md.md",
            "Federated-Learning-Platform/Integrated-Community-Sovereignty-Platform-16-Sector-Integration-md.md",
            "Federated-Learning-Platform/Universal-TDP-and-Derivative-Markets-Framework-md.md",
            "Federated-System-Integration/comprehensive-government-public-sector-analysis-md.md",
            "Federated-System-Integration/comprehensive-professional-cooperative-analysis-md.md",
            "IHOSE/IHOSE-Complete-Technical-Specification-Combined-md.md",
            "IHOSE/IHOSE-Federation-Ecosystem-Framework-md.md",
            "IHOSE/IMPROVEMENT-RECOMMENDATIONS-md.md",
            "IHOSE/Iron-Horse-IHOSE-Complete-Technical-Specification-docx.md",
            "IHOSE/IronHorse-md.md",
        ],
        "ihose-architecture-deployment": [
            "IHOSE/01-OpenVision-Architecture-docx.md",
            "IHOSE/03-Technical-Architecture-md.md",
            "IHOSE/DEPLOYMENT-GUIDE-md.md",
            "IHOSE/enterprise-md.md",
            "IHOSE/IHOSE-C4-Architecture-Models-md.md",
            "IHOSE/IHOSE-C4-Architecture-Models-Part2-md.md",
            "IHOSE/overview-md.md",
            "IHOSE/TECHNICAL-ARCHITECTURE-md.md",
        ],
        "blockchain-education-federation": [
            "Federated-Learning-Platform/blockchain-adoption-barriers-md.md",
            "Federated-Learning-Platform/blockchain-education-architecture-md.md",
            "Federated-Learning-Platform/blockchain-risks-community-integration-md.md",
            "Federated-Learning-Platform/blockchain-solutions-roadmap-md.md",
            "Federated-Learning-Platform/emerging-tech-integration-md.md",
            "Federated-Learning-Platform/haiti-education-federation-md.md",
        ],
        "ihose-business-summaries": [
            "IHOSE/01-Executive-Summary-md.md",
            "IHOSE/BUSINESS-PRESENTATION-md.md",
            "IHOSE/DELIVERY-SUMMARY-md.md",
            "IHOSE/EXECUTIVE-SUMMARY-md.md",
            "IHOSE/PROJECT-SUMMARY-md.md",
        ],
        "ihose-hardware-bom": [
            "IHOSE/02-Hardware-Specifications-docx.md",
            "IHOSE/05-Hardware-Specifications-md.md",
            "IHOSE/bom-enterprise-md.md",
            "IHOSE/HARDWARE-BOM-md.md",
        ],
        "ihose-deployment-infrastructure": [
            "IHOSE/04-docker-compose-yml.md",
            "IHOSE/04-Enterprise-Deployment-md.md",
            "IHOSE/05-kubernetes-manifests-yml.md",
            "IHOSE/06-Complete-Deployment-Guide-docx.md",
        ],
        "ihose-quickstart-install": [
            "IHOSE/00-Quick-Start-Guide-md.md",
            "IHOSE/install-sh.md",
            "IHOSE/QUICK-START-md.md",
        ],
        "ihose-use-cases-business-models": [
            "IHOSE/07-Use-Cases-Integration-md.md",
            "IHOSE/08-Ecosystem-Business-Models-md.md",
        ],
        "ihose-module-development": [
            "IHOSE/03-Module-Development-Guide-docx.md",
            "IHOSE/development-md.md",
        ],
    },
    "dcentral-ecosystem": {
        "dcentral-core-narrative-analysis": [
            "D-Central/D-Central-MVP-Technology-Stack-Recommendation-pdf.md",
            "D-Central-Hardware-Software-Tech-Stack/Comprehensive-Mesh-Network-Tech-Stack-for-Business-Integration-Ecosystem-md.md",
            "D-Central-V1/D-Central-Complete-Analysis-md.md",
            "D-Central-V1/D-Central-Master-Explanation-Document-html.md",
            "D-Central-V1/D-Central-Master-Explanation-md.md",
            "D-Central-V1/D-Central-Technical-Documentation-md.md",
            "D-Central-v2/chatgpt-md.md",
            "D-Central-v2/chatgpt-organized-md.md",
            "D-Central-v2/D-Central-Complete-Fractal-DAO-Governance-Architecture-md-7edde1e7.md",
            "D-Central-v2/D-Central-Edge-Distribution-Computation-Deep-Dive-md-4aa82ecd.md",
            "D-Central-v2/D-Social-Ecosystem-Expanded-Implementation-Guide-md.md",
            "D-Central-v2/dcentral-sales-ecosystem-critical-analysis-md.md",
            "D-Central-v2/dcentral-whole-of-life-mesh-critical-analysis-md.md",
        ],
        "livestream-overlay-chatbot-system": [
            "D-Central-Live-Development/chatbot-integration-system-ts.md",
            "D-Central-Live-Development/overlay-websocket-server-ts.md",
            "D-Central-Live-Development/streaming-overlay-system-tsx.md",
        ],
        "mesh-cooperative-business-models": [
            "D-Central-Business-User-Application/Innovative-Cooperative-Business-Models-for-the-Mesh-Economy-md.md",
            "D-Central-x-OBCC/mesh-cooperative-infrastructure-md.md",
        ],
        "dcentral-networking-architecture": [
            "D-Central/dcm-blueprint-comprehensive-md.md",
            "D-Central-v2/D-Central-Networking-Architecture-Complete-md.md",
        ],
        "dcentral-iot-integration-blueprint": [
            "D-Central-v2/d-central-iot-blueprint-txt.md",
            "D-Central-v2/dcentral-complete-integration-md.md",
        ],
        "dcentral-economic-model-critiques": [
            "D-Central-v2/dcentral-creator-economy-telecom-critical-analysis-md.md",
            "D-Central-v2/dcentral-workforce-commerce-mlm-critical-analysis-md.md",
        ],
        "dcentral-obcc-sector-implementation": [
            "D-Central/D-Central-x-OBCC-Complete-Master-Implementation-Plan-md.md",
            "D-Central-x-OBCC/dcentral-sectors-comprehensive-md.md",
        ],
    },
    "haiti-initiative": {
        "haiti-cooperative-resilience-framework": [
            "Haiti-open-framework/complete-enhanced-haiti-framework-md.md",
            "Haiti-open-framework/Complete-Enhanced-Open-Source-Cooperative-Resilience-Framework-for-Haiti-md-fa474e23.md",
            "Haiti-open-framework/complete-merged-haiti-framework-txt.md",
            "Haiti-Project-1/haiti-mesh-plan-txt.md",
        ],
        "haiti-graphrag-graphql-system": [
            "Haiti-open-framework/Complete-HCCC-GraphRAG-GraphQL-System-Implementation-Guide-md.md",
            "Haiti-open-framework/Comprehensive-GraphRAG-GraphQL-System-Design-Document-md.md",
        ],
    },
    "infrastructure-mesh": {
        "digital-community-participation-platforms": [
            "CivicMesh/Chat-Context-A.md",
            "CivicMesh/Chat-Context-B.md",
            "CivicMesh/DC-CM-REG-001-CivicMesh-Document-Registry-v1-1-docx.md",
            "CivicMesh/DC-MASTER-DOC-001-Master-Documentation-Registry-v1-1-docx.md",
            "Local-Fediverse/Academic-Excellence-Module-Comprehensive-University-Features-md.md",
            "Local-Fediverse/Academic-Institution-Specific-ROI-Value-Propositions-md.md",
            "Local-Fediverse/cultural-food-ecosystem-design-md.md",
            "Local-Fediverse/decentralized-tools-equipment-platform-md.md",
            "Local-Fediverse/decentralized-trades-training-platform-md.md",
            "Local-Fediverse/Enhanced-Academic-Institutional-Onboarding-Activation-Platform-md.md",
            "Local-Fediverse/Enhanced-Value-Added-Services-for-Academic-Institutions-md.md",
            "Local-Fediverse/FediFlow-Academic-Ecosystem-Comprehensive-Community-Services-Use-Cases-md.md",
            "Local-Fediverse/FediFlow-Enterprise-Complete-Ecosystem-Architecture-Strategy-md.md",
            "Local-Fediverse/FediFlow-Enterprise-Comprehensive-Technical-Design-Document-md.md",
            "Local-Fediverse/FediFlow-Institutional-Fediverse-Platform-Business-Plan-md.md",
            "Local-Fediverse/Riverside-University-FediFlow-Academic-Platform-User-Story-md.md",
        ],
        "commercial-b2b-vehicle-fleet-programme": [
            "CivicMesh/DC-CM-B2B-001-Commercial-Vehicle-Network-Programme-v1-docx.md",
            "CivicMesh/DC-CM-B2B-002-Fleet-Operator-Agreement-Template-v1-docx.md",
            "CivicMesh/DC-CM-B2B-003-Platform-Driver-Programme-Specification-v1-docx.md",
            "CivicMesh/DC-CM-B2B-006-Commercial-Platform-API-Integration-Spec-v1-docx.md",
        ],
        "civicmesh-federation-noc-municipal-deployment": [
            "CivicMesh/DC-CM-FED-001-CivicMesh-Federation-Protocol-v1-docx.md",
            "CivicMesh/DC-CM-NOC-001-NOC-Dashboard-Specification-v1-docx.md",
            "CivicMesh/DC-MP-FED-001-MeshPlate-Federation-Protocol-v1-docx.md",
            "CivicMesh/DEPLOY-MP-001-MeshPlate-Municipal-Deployment-Package-v1-docx.md",
            "CivicMesh/LEGAL-CM-011-Municipal-Data-Federation-Agreement-v1-docx.md",
        ],
        "trafficmesh-insurance-integration-revenue": [
            "CivicMesh/DC-CM-INS-001-Insurance-Integration-Specification-v1-docx.md",
            "CivicMesh/FIN-TM-001-TrafficMesh-Revenue-Model-v1-docx.md",
            "CivicMesh/MKT-INS-001-Insurance-Partner-Pitch-Deck-Narrative-v1-docx.md",
            "CivicMesh/MKT-INS-002-Insurance-Data-Product-Catalogue-v1-docx.md",
            "CivicMesh/OS-PATROL-TM-INS-001-TrafficMesh-Insurance-Integration-v1-docx.md",
        ],
        "civicmesh-trafficmesh-grant-funding-applications": [
            "CivicMesh/IRAP-TM-001-NRC-IRAP-Application-TrafficMesh-v1-docx.md",
            "CivicMesh/SRED-CM-001-SR-ED-Project-Ledger-CivicMesh-v1-docx.md",
            "CivicMesh/SRED-TM-001-SR-ED-Project-Ledger-TrafficMesh-v1-docx.md",
        ],
        "dcentral-presentation-decks": [
            "CivicMesh/INV-001-D-Central-Seed-Pre-Seed-Pitch-Deck-v1-docx.md",
            "CivicMesh/INV-002-CivicMesh-Deep-Dive-Investor-Deck-v1-docx.md",
            "CivicMesh/INV-003-D-Central-Group-One-Pager-v1-docx.md",
            "CivicMesh/MKT-TM-GOV-002-OC-Transpo-Pitch-Deck-Narrative-v1-docx.md",
            "CivicMesh/PPTX-CONF-002-CivicMesh-Conference-Talk-Smart-Cities-v1-docx.md",
            "CivicMesh/PPTX-CONF-003-D-Central-Cooperative-Economy-Talk-v1-docx.md",
            "CivicMesh/PPTX-INV-003-D-Central-Cooperative-Economy-Thesis-Deck-v1-docx.md",
            "CivicMesh/PPTX-GOV-001-TrafficMesh-OC-Transpo-Pilot-Presentation-v1-docx.md",
            "CivicMesh/PPTX-GOV-002-TrafficMesh-City-of-Ottawa-Council-Presentation-v1-docx.md",
            "CivicMesh/PPTX-INV-002-CivicMesh-Deep-Dive-Deck-v1-docx.md",
            "CivicMesh/PPTX-MSSP-001-CivicMesh-MSSP-Partner-Recruitment-Deck-v1-docx.md",
        ],
        "communityshield-residential-deployment": [
            "CivicMesh/DEPLOY-CS-001-CommunityShield-HOA-Condo-Deployment-v1-docx.md",
            "CivicMesh/DEPLOY-CS-002-CommunityShield-Apartment-Complex-Deployment-v1-docx.md",
            "CivicMesh/LEGAL-CM-012-HOA-Condo-Participation-Agreement-v1-docx.md",
            "CivicMesh/MKT-CCSC-003-Public-Consultation-Toolkit-v1-docx.md",
        ],
        "dcentral-competitive-strategy-analysis": [
            "CivicMesh/DC-STRAT-005-Competitive-Moat-Analysis-v1-docx.md",
            "CivicMesh/INV-005-CivicMesh-Competitive-Analysis-v1-docx.md",
            "CivicMesh/INV-006-D-Central-Cooperative-Economy-Investor-Thesis-v1-docx.md",
        ],
        "trafficmesh-city-fleet-deployment": [
            "CivicMesh/DEPLOY-TM-002-City-Fleet-Expansion-Plan-v1-docx.md",
            "CivicMesh/MKT-TM-GOV-003-City-of-Ottawa-Pitch-Deck-Narrative-v1-docx.md",
            "CivicMesh/OS-PATROL-TM-FLEET-001-TrafficMesh-Fleet-Node-Specification-v1-docx.md",
        ],
        "trafficmesh-legal-regulatory-compliance": [
            "CivicMesh/OS-PATROL-TM-EV-001-TrafficMesh-Evidence-Legal-Framework-v1-docx.md",
            "CivicMesh/REG-TM-001-TrafficMesh-Ontario-HTA-Compliance-Analysis-v1-docx.md",
            "CivicMesh/REG-TM-002-TrafficMesh-Provincial-Variation-Matrix-v1-docx.md",
        ],
        "civicmesh-officer-portal-municipal-training": [
            "CivicMesh/DC-CM-APP-008-CivicMesh-Officer-Portal-v1-docx.md",
            "CivicMesh/OPS-TM-002-Officer-Review-Portal-SOP-v1-docx.md",
            "CivicMesh/TRAIN-006-Track5-Municipal-Partner-Curriculum-v1-docx.md",
        ],
        "civicmesh-security-response-ops-training": [
            "CivicMesh/OPS-GUARD-001-CivicMesh-Security-Response-SOP-v1-docx.md",
            "CivicMesh/TRAIN-005-Track4-Security-Response-Curriculum-v1-docx.md",
        ],
        "civicmesh-cooperative-legal-structures": [
            "CivicMesh/LEGAL-GUARD-COOP-001-CivicMesh-Guard-Cooperative-v1-docx.md",
            "CivicMesh/LEGAL-MSSP-COOP-001-CivicMesh-MSSP-Cooperative-v1-docx.md",
        ],
        "civicmesh-governance-audit-transparency": [
            "CivicMesh/DC-CM-GOV-002-Community-Audit-Framework-v1-docx.md",
            "CivicMesh/DC-CM-GOV-003-Transparency-Reporting-Standard-v1-docx.md",
        ],
        "civicmesh-financial-unit-economics": [
            "CivicMesh/FIN-CM-002-CivicMesh-Unit-Economics-Model-v1-docx.md",
            "CivicMesh/FIN-CM-005-MSSP-Cooperative-Revenue-Model-v1-docx.md",
        ],
        "civicmesh-isc-loan-application": [
            "CivicMesh/LOAN-CM-001-ISC-Phase1-Application-Framework-v1-docx.md",
            "CivicMesh/LOAN-CM-002-ISC-Phase2-Application-Framework-v1-docx.md",
        ],
        "meshnav-architecture-data-pipeline": [
            "CivicMesh/DC-MN-ARCH-001-MeshNav-Architecture-v1-docx.md",
            "CivicMesh/DC-MN-DATA-001-MeshNav-Data-Pipeline-v1-docx.md",
        ],
        "civicmesh-cooperative-finance-regulatory": [
            "CivicMesh/FIN-COOP-001-Cooperative-Patronage-Distribution-Model-v1-docx.md",
            "CivicMesh/REG-COOP-001-Cooperative-Regulatory-Compliance-Matrix-v1-docx.md",
        ],
        "civicmesh-mitacs-accelerate-applications": [
            "CivicMesh/LOAN-CM-003-Mitacs-Accelerate-University-Research-v1-docx.md",
            "CivicMesh/LOAN-CM-004-Mitacs-Accelerate-Entrepreneur-v1-docx.md",
        ],
        "civicmesh-partner-incentive-programmes": [
            "CivicMesh/MKT-CM-GOV-003-Government-Incentive-Programme-Brief-v1-docx.md",
            "CivicMesh/MKT-MSSP-001-MSSP-Partner-Programme-Prospectus-v1-docx.md",
        ],
        "civicmesh-technician-certification-training": [
            "CivicMesh/DC-CM-CERT-001-Technician-Certification-Programme-v1-docx.md",
            "CivicMesh/TRAIN-002-Track1-Node-Technician-Curriculum-v1-docx.md",
        ],
    },
    "security-identity": {
        "security-ecosystem-sector-platforms": [
            "Open-Secure/Comprehensive-OS-CONCIERGE-Sectors-md.md",
            "Open-Secure/Comprehensive-OS-GUARDIAN-Sectors-md.md",
            "Open-Secure/Comprehensive-OS-PATROL-Sectors-md.md",
            "Open-Secure/Comprehensive-OS-SENTINEL-Sectors-md.md",
            "Open-Secure/OS-PACS-v2-md.md",
            "Security-Ecosystem/iron-horse-distributed-ecosystem-md.md",
            "Security-Ecosystem/iron-horse-workspace-suite-md.md",
            "Security-Ecosystem/museum-agriculture-use-case-md.md",
        ],
        "opensecure-provincial-security-network": [
            "Open-Secure/Provincial-Autonomous-Security-Systems-Network-md.md",
            "Open-Secure/Provincial-Body-Camera-Evidence-Network-md.md",
            "Open-Secure/Provincial-PIV-Infrastructure-Integration-md.md",
            "Open-Secure/Provincial-Security-Guard-Universal-Credential-System-md.md",
            "Open-Secure/Provincial-Security-Vehicle-Network-md.md",
            "Open-Secure/Provincial-Security-Video-Network-md.md",
        ],
        "opensecure-openpiv-subsystem": [
            "Open-Secure/OpenPIV-Implementation-Roadmap-md.md",
            "Open-Secure/OpenPIV-OS-PACS-Integration-Guide-md.md",
            "Open-Secure/OpenPIV-Project-Organization-md.md",
            "Open-Secure/OpenPIV-Quick-Start-Guide-md.md",
            "Open-Secure/OpenPIV-Technical-Architecture-md.md",
        ],
        "opensecure-os-drone-subsystem": [
            "Open-Secure/OS-DRONE-Implementation-Guide-md.md",
            "Open-Secure/OS-DRONE-Logical-Topology-md.md",
            "Open-Secure/OS-DRONE-Network-Topology-md.md",
            "Open-Secure/OS-DRONE-Technical-Architecture-md.md",
        ],
        "opensecure-patrol-sentinel-implementation": [
            "Open-Secure/OS-PATROL-Implementation-Guide-md.md",
            "Open-Secure/OS-SENTINEL-Implementation-Guide-md.md",
        ],
        "opensecure-guardian-sentinel-topology": [
            "Open-Secure/OS-GUARDIAN-Network-Topology-md.md",
            "Open-Secure/OS-SENTINEL-Network-Topology-md.md",
        ],
        "opensecure-os-drone-advanced-capabilities": [
            "Open-Secure/OS-DRONE-Advanced-Visual-Intelligence-md.md",
            "Open-Secure/OS-DRONE-Federation-3D-Spatial-md.md",
        ],
        "opensecure-os-concierge-topology": [
            "Open-Secure/OS-CONCIERGE-Logical-Topology-md.md",
            "Open-Secure/OS-CONCIERGE-Network-Topology-md.md",
        ],
        "opensecure-guardian-sentinel-architecture": [
            "Open-Secure/OS-GUARDIAN-Technical-Architecture-md.md",
            "Open-Secure/OS-SENTINEL-Technical-Architecture-md.md",
        ],
    },
    "verticals-products": {
        "chopshop-project-documentation": [
            "CHOPSHOP/ARCHITECTURE-md.md",
            "CHOPSHOP/chopshop-development-guide-md.md",
            "CHOPSHOP/chopshop-phase1-plan-md.md",
            "CHOPSHOP/chopshop-roadmap-md.md",
            "CHOPSHOP/chopshop-technical-architecture-md.md",
            "CHOPSHOP/chopshop-testing-strategy-md.md",
            "CHOPSHOP/CIPHER-MODULE-GUIDE-md.md",
            "CHOPSHOP/CONTRIBUTING-1-md.md",
            "CHOPSHOP/DAY1-QUICKSTART-md.md",
            "CHOPSHOP/EXECUTIVE-SUMMARY-md.md",
            "CHOPSHOP/PHASE1-SPECIFICATION-md.md",
            "CHOPSHOP/PROJECT-CHARTER-md.md",
            "CHOPSHOP/QUICK-START-md.md",
            "CHOPSHOP/README-DOCUMENTATION-md.md",
            "CHOPSHOP/ROADMAP-md.md",
            "CHOPSHOP/DOCUMENTATION-SUMMARY-md.md",
            "CHOPSHOP/README-2-md.md",
        ],
        "haiti-integration-platforms": [
            "Drone-Zoe/Comprehensive-Democratized-Development-Framework-for-Haiti-md-735f60aa.md",
            "Drone-Zoe/Drone-Zoe-Haiti-Complete-Platform-md.md",
            "Drone-Zoe/Drone-Zoe-Haiti-Decentralized-Open-Credentialing-System-md.md",
            "Drone-Zoe/Drone-Zoe-Haiti-Monetization-Strategy-Revenue-Streams-md.md",
            "Drone-Zoe/Enterprise-Partnerships.md",
            "Drone-Zoe/expanded-monetization-guide-md.md",
            "Drone-Zoe/haiti-drone-cooperative-framework-md-ec202f4d.md",
            "Drone-Zoe/haiti-drone-expanded-strategy-md-eb50bcaa.md",
            "Drone-Zoe/micro-credential-system-md.md",
            "Drone-Zoe/Multi-Sector-Development.md",
            "VDI-Solutions/D-Central-Ecosystem-Haiti-Integration-Framework-md-53dbf869.md",
            "VDI-Solutions/D-Central-Ecosystem-Haiti-Integration-Framework-md.md",
        ],
        "dion-platform-technical-architecture": [
            "Bounty/DION-Platform-Complete-Technical-Architecture-Continuation-md.md",
            "Bounty/DION-Platform-Complete-Technical-Architecture-Implementation-Guide-md.md",
            "Bounty/DION-Platform-Complete-Technical-Architecture-md.md",
            "Bounty/DION-Platform-Development-Setup-Configuration-txt.md",
        ],
        "dion-operator-deployment-credentialing": [
            "Bounty/Dynamic-Operator-Deployment-System-for-D-Central-Intelligence-Workflows-md.md",
            "Bounty/Operator-Credentialing-System-for-D-Central-Intelligence-Network-md.md",
        ],
        "drone-zoe-hardware-selection-guides": [
            "Drone-Zoe/drone-selection-guide2-md-f756780a.md",
            "Drone-Zoe/updated-drone-guide-md-1780e328.md",
        ],
        "dion-platform-expansion-explanation": [
            "Bounty/decentralized-ints-expansion-md.md",
            "Bounty/platform-explanation-md.md",
        ],
    },
}

# docs demoted out of a first-pass cluster into ungrouped, with why
DEMOTIONS = {
    "ai-ml-research": [
        ("Federated-Learning-Platform/security-email-md.md",
         "Pulled into the IHOSE/education-sovereignty cluster by shared generic vocabulary; "
         "it's a standalone email doc, not a technical or sovereignty-framework artifact."),
    ],
    "infrastructure-mesh": [
        ("CivicMesh/DC-STRAT-001-D-Central-Master-Strategy-v1-docx.md",
         "A company-wide master strategy doc, not specifically about the B2B vehicle/fleet "
         "programme -- pulled in by shared strategic vocabulary."),
        ("CivicMesh/OS-PATROL-TM-001-TrafficMesh-Technical-Architecture-v1-docx.md",
         "A technical architecture doc mixed into a cluster of grant/funding-ledger applications "
         "(IRAP, SR&ED) -- different subject, no natural single abstract with the other three."),
    ],
    "security-identity": [
        ("Security-Ecosystem/Previous-Chat.md",
         "A scratch/context file, not a subject-bearing artifact -- pulled into the sector-overviews "
         "cluster by incidental vocabulary overlap."),
    ],
    "verticals-products": [
        ("Bounty/The-Future-of-Community-Intelligence-A-Platform-for-Democratic-Safety-and-Prospe.md",
         "About a community-intelligence/DION platform concept, not Haiti drone or VDI integration "
         "specifically -- pulled into the Haiti/credentialing cluster by shared 'platform' vocabulary."),
    ],
}

RESOLUTION_NOTES = """# Stage 5 Topic Clusters — Subject-Check Resolution

Every one of the 59 first-pass clusters from `topic_synthesis.py` was read (titles plus
spot-checked content) and given a real verdict against DC-TOPIC-SYNTH-STD-001 SS4's calibration
test: can you write one honest 2-4 sentence abstract without "and" joining two unrelated ideas?

**Correction applied after user feedback:** an initial pass split several clusters apart on the
assumption that "different Claude Project = different subject." That assumption is wrong for this
corpus -- D-Central deliberately reuses the same concepts (community/participation platforms,
federation, credentialing, Haiti integration) across many verticals on purpose, so cross-project
overlap here is often the real topic, not noise. Those splits were reverted:

- **`digital-community-participation-platforms`** (infrastructure-mesh, 16 docs): CivicMesh's
  registry/context docs kept together WITH Local-Fediverse's FediFlow academic-platform docs --
  both are community/participation platform concepts, not two unrelated projects.
- **`federation-sovereignty-cooperative-platforms`** (ai-ml-research, 11 docs): Federated-Learning-
  Platform + Federated-System-Integration's sovereignty/cooperative docs kept together WITH IHOSE's
  federation-ecosystem docs -- same underlying federation/sovereignty concept across platforms.
- **`security-ecosystem-sector-platforms`** (security-identity, 8 docs): Open-Secure's sector
  overviews kept together WITH Security-Ecosystem's "Iron Horse" ecosystem docs -- same sector-based
  security-ecosystem concept.
- **`haiti-integration-platforms`** (verticals-products, 12 docs): Drone-Zoe's Haiti drone/monetization
  docs kept together WITH VDI-Solutions' Haiti integration docs -- same Haiti-integration concept
  across different verticals.

## Splits that stayed (genuinely different subject, not just a different platform)

## Merges (several small clusters were one topic split by a superficial difference)

- **infrastructure-mesh**: `format-open-ask` + `script-pptx-produce` + `available-script-pptx` +
  `one-show-design` (4 clusters, 11 docs total) merged into one `dcentral-presentation-decks` topic.
  These were split only by audience (investor vs. government vs. conference), not by subject --
  they're all presentation-deck artifacts.
- **verticals-products**: `decoding-cipher-chopshop` + `recursive-focused-best` merged into
  `chopshop-project-documentation` (17 docs) -- the second cluster was just two CHOPSHOP meta/
  summary docs that belong with the rest of that project's documentation set.

## Demotions (one doc inside an otherwise-coherent cluster didn't belong)

See DEMOTIONS in `scripts/resolve_topic_review.py` for the full list and reasoning (4 docs total,
moved to their category's ungrouped list).

## Confirmed as-is (renamed only)

The remaining ~45 clusters were confirmed coherent as first-clustered and given a real name instead
of the placeholder keyword-join (e.g. `sony-firmware-opensecure` -> `opensecure-os-drone-subsystem`).
Several small (2-doc) sibling clusters in security-identity (e.g. OS-GUARDIAN vs OS-SENTINEL topology/
architecture pairs) were deliberately NOT merged despite structural similarity -- they're functionally
different subsystems, and forcing a merge across subsystem boundaries would reduce coherence, not
improve it (DC-TOPIC-SYNTH-STD-001 SS4's sibling-consistency guidance cuts the other way here: these
ARE consistently-grained siblings, so matching granularity means keeping them separate).

See `scripts/resolve_topic_review.py` for the complete final topic membership per category.
"""


def parse_doc(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    if text.startswith("---"):
        end = text.find("\n---", 3)
        return text[3:end], text[end + 4:]
    return "", text


def set_topic_field(path, topic_slug):
    fm_text, body = parse_doc(path)
    lines = [l for l in fm_text.split("\n") if not l.strip().startswith("topic:")]
    fm_text = "\n".join(lines)
    if not fm_text.endswith("\n") and fm_text:
        fm_text += "\n"
    fm_text += f"topic: {topic_slug}\n"
    path.write_text("---" + fm_text + "---" + body, encoding="utf-8")


def clear_topic_field(path):
    fm_text, body = parse_doc(path)
    lines = [l for l in fm_text.split("\n") if not l.strip().startswith("topic:")]
    fm_text = "\n".join(lines)
    path.write_text("---" + fm_text + "---" + body, encoding="utf-8")


def main():
    for category, topics in FINAL_TOPICS.items():
        cat_dir = KB_DIR / category
        all_docs = set(f for f in cat_dir.rglob("*.md")
                        if f.name not in ("_INDEX.md", "_topics.md") and "_superseded" not in f.parts)
        clustered = set()

        for topic_slug, rel_paths in topics.items():
            for rel in rel_paths:
                p = cat_dir / rel
                if not p.exists():
                    print(f"WARNING: missing {p}")
                    continue
                set_topic_field(p, topic_slug)
                clustered.add(p)

        demoted = {cat_dir / rel for rel, _ in DEMOTIONS.get(category, [])}
        for p in demoted:
            if p.exists():
                clear_topic_field(p)

        ungrouped = sorted((all_docs - clustered) | (demoted & all_docs))

        topics_path = cat_dir / "_topics.md"
        with open(topics_path, "w", encoding="utf-8") as f:
            f.write(f"# Topics — {category}\n\n")
            f.write(f"**Subject-checked** — see [../../TOPIC-RESOLUTION.md](../../TOPIC-RESOLUTION.md) "
                    f"for the full reasoning behind every split/merge/demotion applied.\n\n")
            f.write(f"{len(all_docs)} docs. {len(topics)} confirmed topics ({len(clustered)} docs), "
                    f"{len(ungrouped)} ungrouped.\n\n")
            for topic_slug, rel_paths in sorted(topics.items(), key=lambda t: -len(t[1])):
                f.write(f"## {topic_slug} ({len(rel_paths)} docs)\n\n")
                for rel in sorted(rel_paths):
                    f.write(f"- [{rel}](./{rel})\n")
                f.write("\n")
            if ungrouped:
                f.write(f"## Ungrouped ({len(ungrouped)} docs)\n\n")
                for p in ungrouped:
                    rel = p.relative_to(cat_dir).as_posix()
                    f.write(f"- [{rel}](./{rel})\n")

        print(f"{category}: {len(topics)} confirmed topics, {len(clustered)} docs clustered, "
              f"{len(ungrouped)} ungrouped")

    with open(REPO_ROOT / "TOPIC-RESOLUTION.md", "w", encoding="utf-8") as f:
        f.write(RESOLUTION_NOTES)

    total_topics = sum(len(t) for t in FINAL_TOPICS.values())
    total_clustered = sum(len(v) for t in FINAL_TOPICS.values() for v in t.values())
    print(f"\nTotals: {total_topics} confirmed topics, {total_clustered} docs clustered.")
    print("Wrote TOPIC-RESOLUTION.md")


if __name__ == "__main__":
    main()
