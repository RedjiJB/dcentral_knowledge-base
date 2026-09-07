# DC-CM-SECURITY-RESPONSE-RECONCILED-001 — CivicMesh Security Response Ops & Training, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `civicmesh-security-response-training` (2 docs).

## Current understanding

OPS-GUARD-001 is the operational SOP for licensed security responders dispatched through CivicMesh;
TRAIN-005 is the certification curriculum that qualifies responders to follow it. The curriculum's five
modules map directly onto the SOP's own section structure.

**SOP (incorporated):** dispatch/response SLAs by event type and tier (e.g., a confirmed gunshot is
"accept: immediate" at every tier and always escalates to 911 regardless of tier; parking enforcement
is accept-30min/on-scene-2hr at Standard) [OPS-GUARD-001 §1]; a scene-safety-first on-scene procedure
with mandatory photo/GPS documentation and credential display [§2]; five incident-type-specific
procedures each pairing an on-scene action with an escalation rule (e.g., trespassing responders may
request departure but must not physically remove; vandalism responders must not physically intervene)
[§3]; evidence-chain obligations — every action is DID-signed and timestamped, corrections must
reference rather than delete the original entry, and body-camera footage is explicitly NOT
auto-uploaded to CivicMesh (managed separately by the responder's employer) [§4]; and rules for
interacting with sworn officers on scene, including that a responder is not required to hand over DID
wallet/credential data to police outside the formal federation-request process [§5].

**Curriculum (incorporated):** a 6-hour, $399, five-module course (Dispatch Integration, Evidence Chain
Obligations, Incident-Type Procedures, Law Enforcement Interaction, Privacy/Anti-Surveillance), each
module directly assessed (practical, written exam, or scenario) and each mapping one-to-one onto a
section of the SOP it exists to operationalize [TRAIN-005 §1]. Prerequisites require a valid Ontario
security guard licence (the curriculum explicitly does not replace licensing) and an enhanced
reliability background check renewed annually [§2].

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Dispatch/response SLAs by event type and tier | OPS-GUARD-001 §1 | incorporated |
| On-scene procedure and documentation requirements | OPS-GUARD-001 §2 | incorporated |
| Incident-type-specific procedures and escalation rules | OPS-GUARD-001 §3 | incorporated |
| Evidence-chain obligations, incl. body-cam handling | OPS-GUARD-001 §4 | incorporated |
| Sworn-officer interaction rules | OPS-GUARD-001 §5 | incorporated |
| 5-module certification curriculum (content + assessment) | TRAIN-005 §1 | incorporated (each module maps to an SOP section) |
| Certification prerequisites | TRAIN-005 §2 | incorporated |

## Unresolved tensions

None identified in this pass — the curriculum is explicitly built to certify responders on the SOP's
own procedures, and no content in either document contradicts the other.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/security/CivicMesh/OPS-GUARD-001-CivicMesh-Security-Response-SOP-v1-docx.md`
- `knowledge-base/d-central/security/CivicMesh/TRAIN-005-Track4-Security-Response-Curriculum-v1-docx.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/security/CivicMesh/OPS-GUARD-001-CivicMesh-Security-Response-SOP-v1-docx.md,
  knowledge-base/d-central/security/CivicMesh/TRAIN-005-Track4-Security-Response-Curriculum-v1-docx.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

Neither source doc is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

*No cross-references detected to/from other docs/*.md files.*

<!-- AUTO-GENERATED RELATED END -->
