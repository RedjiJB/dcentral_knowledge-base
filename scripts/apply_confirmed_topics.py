#!/usr/bin/env python3
"""
Stage 5 confirm step for the `security` and `business-legal` categories --
writes topic: front matter ONLY for clusters that survived an actual human/
agent subject-check read of scripts/topic_candidates.py's lexical output
(conversations/_scratch/security_topic_candidates.md and
business_legal_topic_candidates.md), per DC-TOPIC-SYNTH-STD-001 SS4.

Several lexical candidates were split, merged, or rejected outright after
reading the actual docs -- see PLAN.md for the reasoning on each. This
script only encodes the FINAL verdicts, never the raw lexical clusters.

Usage: python3 scripts/apply_confirmed_topics.py
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)

# name -> list of repo-relative paths
TOPICS = {
    # ---------------- security ----------------
    "ihose-openvision-documentation-package": [
        "knowledge-base/d-central/security/IHOSE/00-Quick-Start-Guide-md.md",
        "knowledge-base/d-central/security/IHOSE/01-Executive-Summary-md.md",
        "knowledge-base/d-central/security/IHOSE/01-OpenVision-Architecture-docx.md",
        "knowledge-base/d-central/security/IHOSE/03-Module-Development-Guide-docx.md",
        "knowledge-base/d-central/security/IHOSE/03-Technical-Architecture-md.md",
        "knowledge-base/d-central/security/IHOSE/04-docker-compose-yml.md",
        "knowledge-base/d-central/security/IHOSE/04-Enterprise-Deployment-md.md",
        "knowledge-base/d-central/security/IHOSE/05-kubernetes-manifests-yml.md",
        "knowledge-base/d-central/security/IHOSE/06-Complete-Deployment-Guide-docx.md",
        "knowledge-base/d-central/security/IHOSE/07-Use-Cases-Integration-md.md",
        "knowledge-base/d-central/security/IHOSE/core-stack-yml.md",
        "knowledge-base/d-central/security/IHOSE/DEPLOYMENT-GUIDE-md.md",
        "knowledge-base/d-central/security/IHOSE/development-md.md",
        "knowledge-base/d-central/security/IHOSE/enterprise-md.md",
        "knowledge-base/d-central/security/IHOSE/EXECUTIVE-SUMMARY-md.md",
        "knowledge-base/d-central/security/IHOSE/IHOSE-DataFlow-API-DevSecOps-Specification-md.md",
        "knowledge-base/d-central/security/IHOSE/install-sh.md",
        "knowledge-base/d-central/security/IHOSE/overview-md.md",
        "knowledge-base/d-central/security/IHOSE/README-md.md",
        "knowledge-base/d-central/security/IHOSE/TECHNICAL-ARCHITECTURE-md.md",
    ],
    "opensecure-topology-documentation-suite": [
        "knowledge-base/d-central/security/Open-Secure/OpenSecure-Hub-Network-Topology-md.md",
        "knowledge-base/d-central/security/Open-Secure/OpenSecure-Hub-Logical-Topology-md.md",
        "knowledge-base/d-central/security/Open-Secure/OpenSecure-Hub-Implementation-Guide-md.md",
        "knowledge-base/d-central/security/Open-Secure/OS-DRONE-Logical-Topology-md.md",
        "knowledge-base/d-central/security/Open-Secure/OS-DRONE-Network-Topology-md.md",
        "knowledge-base/d-central/security/Open-Secure/OS-DRONE-Technical-Architecture-md.md",
        "knowledge-base/d-central/security/Open-Secure/OS-GUARDIAN-Technical-Architecture-md.md",
        "knowledge-base/d-central/security/Open-Secure/OS-GUARDIAN-Logical-Topology-md.md",
        "knowledge-base/d-central/security/Open-Secure/OS-GUARDIAN-Network-Topology-md.md",
        "knowledge-base/d-central/security/Open-Secure/OS-SENTINEL-Technical-Architecture-md.md",
        "knowledge-base/d-central/security/Open-Secure/OS-SENTINEL-Logical-Topology-md.md",
        "knowledge-base/d-central/security/Open-Secure/OS-SENTINEL-Network-Topology-md.md",
        "knowledge-base/d-central/security/Open-Secure/OS-PATROL-Network-Topology-md.md",
        "knowledge-base/d-central/security/Open-Secure/OS-PATROL-Logical-Topology-md.md",
        "knowledge-base/d-central/security/Open-Secure/OpenSecure-Digital-Twin-Integration-md.md",
    ],
    "opensecure-per-service-implementation-guides": [
        "knowledge-base/d-central/security/Open-Secure/OS-CONCIERGE-Implementation-Guide-md.md",
        "knowledge-base/d-central/security/Open-Secure/OS-DRONE-Implementation-Guide-md.md",
        "knowledge-base/d-central/security/Open-Secure/OS-GUARDIAN-Implementation-Guide-md.md",
        "knowledge-base/d-central/security/Open-Secure/OS-PATROL-Implementation-Guide-md.md",
        "knowledge-base/d-central/security/Open-Secure/OS-SENTINEL-Implementation-Guide-md.md",
    ],
    "opensecure-sector-use-case-analyses": [
        "knowledge-base/d-central/security/Open-Secure/Comprehensive-OS-CONCIERGE-Sectors-md.md",
        "knowledge-base/d-central/security/Open-Secure/Comprehensive-OS-DRONE-Sectors-md.md",
        "knowledge-base/d-central/security/Open-Secure/Comprehensive-OS-GUARDIAN-Sectors-md.md",
        "knowledge-base/d-central/security/Open-Secure/Comprehensive-OS-PATROL-Sectors-md.md",
        "knowledge-base/d-central/security/Open-Secure/Comprehensive-OS-SENTINEL-Sectors-md.md",
    ],
    "provincial-security-network-programs": [
        "knowledge-base/d-central/security/Open-Secure/Provincial-Autonomous-Security-Systems-Network-md.md",
        "knowledge-base/d-central/security/Open-Secure/Provincial-Body-Camera-Evidence-Network-md.md",
        "knowledge-base/d-central/security/Open-Secure/Provincial-Security-Reserve-Forces-Integration-md.md",
        "knowledge-base/d-central/security/Open-Secure/Provincial-Security-Vehicle-Network-md.md",
        "knowledge-base/d-central/security/Open-Secure/Provincial-Security-Video-Network-md.md",
    ],
    "openpiv-pacs-integration-suite": [
        "knowledge-base/d-central/security/Open-Secure/OpenPIV-Implementation-Roadmap-md.md",
        "knowledge-base/d-central/security/Open-Secure/OpenPIV-OS-PACS-Deployment-Checklist-md.md",
        "knowledge-base/d-central/security/Open-Secure/OpenPIV-OS-PACS-Integration-Guide-md.md",
        "knowledge-base/d-central/security/Open-Secure/OpenPIV-Quick-Start-Guide-md.md",
    ],
    "os-drone-advanced-capabilities": [
        "knowledge-base/d-central/security/Open-Secure/OS-DRONE-Advanced-Visual-Intelligence-md.md",
        "knowledge-base/d-central/security/Open-Secure/OS-DRONE-Federation-3D-Spatial-md.md",
    ],
    "meshplate-federation-privacy-compliance": [
        "knowledge-base/d-central/security/CivicMesh/DC-MP-FED-001-MeshPlate-Federation-Protocol-v1-docx.md",
        "knowledge-base/d-central/security/CivicMesh/MKT-CCSC-004-CivicMesh-Privacy-Promise-v1-docx.md",
        "knowledge-base/d-central/security/CivicMesh/REG-CM-001-CivicMesh-PIPEDA-Compliance-Framework-v1-docx.md",
        "knowledge-base/d-central/security/CivicMesh/REG-CS-001-CommunityShield-Surveillance-Regulatory-Analysis-v1-docx.md",
    ],
    "civicmesh-security-response-training": [
        "knowledge-base/d-central/security/CivicMesh/OPS-GUARD-001-CivicMesh-Security-Response-SOP-v1-docx.md",
        "knowledge-base/d-central/security/CivicMesh/TRAIN-005-Track4-Security-Response-Curriculum-v1-docx.md",
    ],

    # ---------------- business-legal ----------------
    "ihose-business-strategy-documents": [
        "knowledge-base/d-central/business-legal/IHOSE/06-Implementation-Roadmap-md.md",
        "knowledge-base/d-central/business-legal/IHOSE/08-Ecosystem-Business-Models-md.md",
        "knowledge-base/d-central/business-legal/IHOSE/BUSINESS-PRESENTATION-md.md",
        "knowledge-base/d-central/business-legal/IHOSE/IMPROVEMENT-RECOMMENDATIONS-md.md",
    ],
    "mesh-cooperative-business-model-framework": [
        "knowledge-base/d-central/business-legal/D-Central/D-Central-x-OBCC-Complete-Master-Implementation-Plan-md.md",
        "knowledge-base/d-central/business-legal/D-Central-Business-User-Application/Innovative-Cooperative-Business-Models-for-the-Mesh-Economy-md.md",
        "knowledge-base/d-central/business-legal/D-Central-Business-User-Application/Mesh-Network-Business-Onboarding-Playbook-90-Day-Value-Capture-Guide-md.md",
        "knowledge-base/d-central/business-legal/D-Central-x-OBCC/mesh-cooperative-infrastructure-md.md",
        "knowledge-base/d-central/business-legal/conversation-artifacts/DC-COOP-001_v1.0_SodBoys_FullRebuild.md",
        "knowledge-base/d-central/business-legal/conversation-artifacts/DC-COOP-001_v2.0_SodBoys_FullExpansion.md",
    ],
    "mesh-food-economy-business-models": [
        "knowledge-base/d-central/business-legal/D-Central-Business-User-Application/Decentralized-Community-Funding-Model-for-Local-Food-Mesh-Network-md.md",
        "knowledge-base/d-central/business-legal/D-Central-Business-User-Application/Restaurant-Mesh-Transformation-Complete-Cost-Analysis-Revenue-Generation-md.md",
        "knowledge-base/d-central/business-legal/D-Central-x-OBCC/dcentral-sectors-comprehensive-md.md",
        "knowledge-base/d-central/business-legal/D-Central-x-OBCC/local-food-mesh-template-md.md",
    ],
    "communityshield-hoa-deployment-package": [
        "knowledge-base/d-central/business-legal/CivicMesh/DEPLOY-CS-001-CommunityShield-HOA-Condo-Deployment-v1-docx.md",
        "knowledge-base/d-central/business-legal/CivicMesh/DEPLOY-CS-002-CommunityShield-Apartment-Complex-Deployment-v1-docx.md",
        "knowledge-base/d-central/business-legal/CivicMesh/LEGAL-CM-012-HOA-Condo-Participation-Agreement-v1-docx.md",
        "knowledge-base/d-central/business-legal/CivicMesh/MKT-CCSC-003-Public-Consultation-Toolkit-v1-docx.md",
    ],
    "civicmesh-investor-pitch-decks": [
        "knowledge-base/d-central/business-legal/CivicMesh/INV-001-D-Central-Seed-Pre-Seed-Pitch-Deck-v1-docx.md",
        "knowledge-base/d-central/business-legal/CivicMesh/INV-002-CivicMesh-Deep-Dive-Investor-Deck-v1-docx.md",
        "knowledge-base/d-central/business-legal/CivicMesh/INV-003-D-Central-Group-One-Pager-v1-docx.md",
        "knowledge-base/d-central/business-legal/CivicMesh/MKT-TM-GOV-002-OC-Transpo-Pitch-Deck-Narrative-v1-docx.md",
    ],
    "civicmesh-government-funding-applications": [
        "knowledge-base/d-central/business-legal/CivicMesh/IRAP-TM-001-NRC-IRAP-Application-TrafficMesh-v1-docx.md",
        "knowledge-base/d-central/business-legal/CivicMesh/LOAN-CM-001-ISC-Phase1-Application-Framework-v1-docx.md",
        "knowledge-base/d-central/business-legal/CivicMesh/SRED-CM-001-SR-ED-Project-Ledger-CivicMesh-v1-docx.md",
        "knowledge-base/d-central/business-legal/CivicMesh/SRED-TM-001-SR-ED-Project-Ledger-TrafficMesh-v1-docx.md",
    ],
    "dcentral-reinvestment-procurement-plans": [
        "knowledge-base/d-central/business-legal/conversation-artifacts/DC-REINVEST-001-Corporate-Procurement-Plan.md",
        "knowledge-base/d-central/business-legal/conversation-artifacts/DC-REINVEST-002-Full-Immediate-Buildout.md",
        "knowledge-base/d-central/business-legal/conversation-artifacts/DC-REINVEST-003-Master-Procurement-Plan.md",
    ],
    "civicmesh-competitive-analysis": [
        "knowledge-base/d-central/business-legal/CivicMesh/DC-STRAT-005-Competitive-Moat-Analysis-v1-docx.md",
        "knowledge-base/d-central/business-legal/CivicMesh/INV-005-CivicMesh-Competitive-Analysis-v1-docx.md",
    ],
    "civicmesh-cooperative-legal-structures": [
        "knowledge-base/d-central/business-legal/CivicMesh/LEGAL-GUARD-COOP-001-CivicMesh-Guard-Cooperative-v1-docx.md",
        "knowledge-base/d-central/business-legal/CivicMesh/LEGAL-MSSP-COOP-001-CivicMesh-MSSP-Cooperative-v1-docx.md",
    ],
    "mitacs-accelerate-applications": [
        "knowledge-base/d-central/business-legal/CivicMesh/LOAN-CM-003-Mitacs-Accelerate-University-Research-v1-docx.md",
        "knowledge-base/d-central/business-legal/CivicMesh/LOAN-CM-004-Mitacs-Accelerate-Entrepreneur-v1-docx.md",
    ],
    "civicmesh-trafficmesh-articles-of-incorporation": [
        "knowledge-base/d-central/business-legal/CivicMesh/LEGAL-CM-001-CivicMesh-Inc-Articles-v1-docx.md",
        "knowledge-base/d-central/business-legal/CivicMesh/LEGAL-TM-001-TrafficMesh-Technologies-Articles-v1-docx.md",
    ],
    "fediverse-academic-institution-services": [
        "knowledge-base/d-central/business-legal/Local-Fediverse/Academic-Institution-Specific-ROI-Value-Propositions-md.md",
        "knowledge-base/d-central/business-legal/Local-Fediverse/Enhanced-Value-Added-Services-for-Academic-Institutions-md.md",
    ],
    "trafficmesh-ottawa-government-engagement": [
        "knowledge-base/d-central/business-legal/CivicMesh/PPTX-GOV-001-TrafficMesh-OC-Transpo-Pilot-Presentation-v1-docx.md",
        "knowledge-base/d-central/business-legal/CivicMesh/PPTX-GOV-002-TrafficMesh-City-of-Ottawa-Council-Presentation-v1-docx.md",
        "knowledge-base/d-central/business-legal/CivicMesh/DEPLOY-TM-002-City-Fleet-Expansion-Plan-v1-docx.md",
        "knowledge-base/d-central/business-legal/CivicMesh/MKT-TM-GOV-003-City-of-Ottawa-Pitch-Deck-Narrative-v1-docx.md",
    ],
    "trafficmesh-ontario-regulatory-compliance": [
        "knowledge-base/d-central/business-legal/CivicMesh/REG-TM-001-TrafficMesh-Ontario-HTA-Compliance-Analysis-v1-docx.md",
        "knowledge-base/d-central/business-legal/CivicMesh/REG-TM-002-TrafficMesh-Provincial-Variation-Matrix-v1-docx.md",
    ],

    # ---------------- core (round 2 -- remaining 7 categories) ----------------
    "dcentral-venture-governance-protocol-suite": [
        "knowledge-base/d-central/core/governance/conversation-artifacts/DC-FRACTAL-001_Fractal_Cell_Architecture.md",
        "knowledge-base/d-central/core/governance/conversation-artifacts/DC-GOV-002_Conglomerate_Governance_Architecture.md",
        "knowledge-base/d-central/core/governance/conversation-artifacts/DC-MOGUL-001_Principal_Track_Protocol.md",
        "knowledge-base/d-central/core/governance/conversation-artifacts/DC-TPL-000_Template_Standard.md",
        "knowledge-base/d-central/core/governance/conversation-artifacts/DC-VENTURE-001_Venture_Sequencing_Registry.md",
    ],
    "civicmesh-noc-manager-dashboard-specifications": [
        "knowledge-base/d-central/core/governance/CivicMesh/DC-CM-APP-009-CivicMesh-Manager-Dashboard-v1-docx.md",
        "knowledge-base/d-central/core/observability/CivicMesh/DC-CM-APP-003-CivicMesh-NOC-Console-v1-docx.md",
        "knowledge-base/d-central/core/observability/CivicMesh/DC-CM-NOC-001-NOC-Dashboard-Specification-v1-docx.md",
    ],

    # ---------------- haiti-diaspora ----------------
    "haiti-security-framework-outreach": [
        "knowledge-base/d-central/haiti-diaspora/Federated-Learning-Platform/security-email-md.md",
        "knowledge-base/d-central/haiti-diaspora/Haiti-open-framework/haiti-security-proposal-md.md",
    ],

    # ---------------- mesh-services ----------------
    "dion-platform-api-backend-architecture": [
        "knowledge-base/d-central/mesh-services/ai/Bounty/api-integration-architecture-md.md",
        "knowledge-base/d-central/mesh-services/ai/Bounty/DION-Platform-API-Completion-of-OpenAPI-Specification-md.md",
        "knowledge-base/d-central/mesh-services/ai/Bounty/DION-Platform-Backend-Services-Implementation-txt.md",
        "knowledge-base/d-central/mesh-services/ai/Bounty/federated-hybrid-integration-md.md",
    ],

    # ---------------- meta ----------------
    "dcentral-developer-ecosystem-os-specs": [
        "knowledge-base/d-central/meta/platform-scaffolding/conversation-artifacts/DC-DEV-001_Mesh_Native_Developer_Platform.md",
        "knowledge-base/d-central/meta/platform-scaffolding/conversation-artifacts/DC-OS-001_Ecosystem_Operating_System.md",
    ],
    "dcentral-simulation-lab-programme": [
        "knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-000-Index.md",
        "knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-001-Fidelity-Reference.md",
        "knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-002-Topology-Build-Spec.md",
        "knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-003-DCOS-Build-Spec.md",
        "knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-004-Test-Scenario-Catalogue.md",
        "knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-005-Cloud-Bridge-External-Integration.md",
        "knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-006-Hardware-Integration-Roadmap.md",
        "knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-007-DAO-Governance-Simulation.md",
        "knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-008-Open-Architecture-Decisions.md",
        "knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-009-Architecture-Decision-Records.md",
    ],
}

# Docs that already carry a DIFFERENT confirmed topic from an earlier pass, but
# also genuinely belong to one more -- topic: is multi-valued, so these ADD a
# second tag rather than overwriting. Every entry here was verified by reading
# the doc, not inferred from the lexical candidate grouping alone.
ADDITIONAL_TOPIC_TAGS = {
    "dion-operator-deployment-credentialing": [
        "knowledge-base/d-central/core/governance/Bounty/The-Future-of-Community-Intelligence-A-Platform-for-Democratic-Safety-and-Prospe.md",
        "knowledge-base/d-central/meta/platform-scaffolding/Bounty/D-Central-Intelligence-Operator-Network-Complete-Platform-Blueprint-md.md",
    ],
    "commercial-b2b-vehicle-fleet-programme": [
        "knowledge-base/d-central/core/identity/CivicMesh/DC-CM-B2B-005-Commercial-Driver-VC-Schema-v1-docx.md",
    ],
    "ihose-architecture-deployment": [
        "knowledge-base/d-central/meta/platform-scaffolding/IHOSE/Iron-Horse-IHOSE-Technical-Specification-v2-docx.md",
    ],
    "opensecure-topology-documentation-suite": [
        "knowledge-base/d-central/meta/status-tracking/Open-Secure/TOPOLOGY-SUITE-SUMMARY-md.md",
    ],
    "dion-platform-technical-architecture": [
        "knowledge-base/d-central/meta/platform-scaffolding/Bounty/DION-Platform-Frontend-Components-Structure-txt.md",
    ],
    "dion-platform-expansion-explanation": [
        "knowledge-base/d-central/meta/platform-scaffolding/Bounty/Simple-Platform-Explanation-with-D-Central-Integration-md.md",
    ],
    "digital-community-participation-platforms": [
        "knowledge-base/d-central/meta/status-tracking/CivicMesh/DC-CM-REG-001-AMD-001-B2B-Registry-Addendum-v1-docx.md",
    ],
    "comptia-a-learning-platform": [
        "knowledge-base/d-central/academic-personal/Comptia-A/Game-Suite.md",
    ],
}


def add_topic(path: Path, topic: str):
    text = path.read_text(encoding="utf-8", errors="replace")
    m = FRONTMATTER_RE.match(text)
    if not m:
        print(f"SKIP (no front matter): {path}")
        return
    fm_lines = m.group(1).splitlines()
    if any(l.strip() in (f'topic: "{topic}"', f"topic: {topic}") for l in fm_lines):
        return  # already tagged -- safe to re-run this script
    fm_lines.append(f'topic: "{topic}"')
    new_text = "---\n" + "\n".join(fm_lines) + "\n---\n" + m.group(2)
    path.write_text(new_text, encoding="utf-8")


def main():
    total = 0
    for topic, rel_paths in TOPICS.items():
        for rel in rel_paths:
            path = REPO_ROOT / rel
            if not path.exists():
                print(f"MISSING: {rel}")
                continue
            add_topic(path, topic)
            total += 1
    print(f"\nTagged {total} docs across {len(TOPICS)} confirmed topics.")

    extra = 0
    for topic, rel_paths in ADDITIONAL_TOPIC_TAGS.items():
        for rel in rel_paths:
            path = REPO_ROOT / rel
            if not path.exists():
                print(f"MISSING: {rel}")
                continue
            add_topic(path, topic)
            extra += 1
    print(f"Added {extra} additional (second) topic tags to already-tagged docs.")


if __name__ == "__main__":
    main()
