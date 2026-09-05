---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: 1119f649-2df8-4b90-98d8-0fb978ca5026
original_filename: OS-DRONE_Decentralized_Identity_VC.md
created_at: 2026-03-05T13:50:31.677323+00:00
content_hash: 34fab2cb6a12
status: "duplicate"
duplicate_of: "knowledge-base/d-central/core/identity/Open-Secure/OS-DRONE-Decentralized-Identity-VC-md.md"
duplicate_reason: "exact body-hash match within the same category, resolved during Stage 5 topic-synthesis prep (never went through Stage 4 exact-hash dedup, which only covered the original 428 docs before this fine-grained reclassification)"
---

# OS-DRONE Decentralized Identity & Verifiable Credentials
## W3C DID, Verifiable Credentials, and Decentralized Trust for Autonomous Aerial Systems

**Document Type**: Identity Architecture Specification
**Version**: 1.0
**Date**: March 2026
**Classification**: Technical Documentation
**Audience**: Identity Architects, Security Engineers, UAS Operations, Compliance Teams

---

## Table of Contents

1. [The Core Problem: Identity in Autonomous Airspace](#the-core-problem)
2. [Architecture Philosophy: Decentralized by Design](#architecture-philosophy)
3. [W3C DID for Drones — Drone Decentralized Identifiers](#w3c-did-for-drones)
4. [Verifiable Credentials Ecosystem](#verifiable-credentials-ecosystem)
5. [Drone Credential Schema Library](#drone-credential-schema-library)
6. [Operator Authorization via Verifiable Credentials](#operator-authorization)
7. [Mission Authorization Tokens (Decentralized)](#mission-authorization-tokens)
8. [Evidence as Verifiable Presentations](#evidence-as-verifiable-presentations)
9. [Trust Registry & Federation](#trust-registry--federation)
10. [Zero-Knowledge Proofs for Privacy-Preserving Compliance](#zero-knowledge-proofs)
11. [Cross-Organization Drone Sharing](#cross-organization-drone-sharing)
12. [Blockchain Anchoring Strategy](#blockchain-anchoring-strategy)
13. [OpenSecure PIV + DID Bridge](#opensecure-piv--did-bridge)
14. [Implementation Stack](#implementation-stack)
15. [Security Threat Model](#security-threat-model)
16. [API Reference](#api-reference)

---

## The Core Problem

Every other device in the OpenSecure ecosystem has a clear owner and a clear physical boundary. A door reader stays at a door. A body camera stays on an officer. But a drone is different:

- It **moves across organizational boundaries** — flying over multiple properties, jurisdictions, agencies
- It **acts autonomously** — making decisions and taking actions without a human in the loop
- It **represents authority** — operators, organizations, and regulators all delegate different permissions to it
- It **generates legal evidence** — video that needs cryptographic proof of authenticity and provenance
- It **interacts with other drones** — swarm coordination requires peer-to-peer trust without a central broker

Traditional PKI and centralized identity systems are inadequate for this. They assume a central authority that all parties trust, a stable network connection, and a human in every decision loop. Drones in the field have none of these guarantees.

**The solution is a decentralized identity architecture where:**
- The drone itself has a self-sovereign identity (W3C DID)
- Every authorization is a cryptographically signed Verifiable Credential
- Evidence is a Verifiable Presentation that proves its own authenticity
- Trust is established through a federated Trust Registry, not a single CA
- The drone can verify and issue credentials even when offline

This integrates seamlessly with the OpenPIV / PIV infrastructure already in the ecosystem — the PIV credential becomes a **DID anchor** and a **VC issuer**, not a replacement.

---

## Architecture Philosophy

### Decentralized vs. Centralized — When to Use Each

The ecosystem already uses centralized PKI (OpenPIV / Dogtag) for human identity. The question is not "replace PKI with DIDs" — it is "what does each technology do best?"

```
CENTRALIZED PKI (OpenPIV / Dogtag)     DECENTRALIZED (W3C DID / VC)
─────────────────────────────────────────────────────────────────────
Human identity (guard, officer,          Machine identity (drone,
  pilot, admin)                            sensor, ground station)

Long-lived credentials (years)           Short-lived tokens (minutes
                                           to hours for mission auth)

Always-online OCSP revocation            Offline-capable revocation
                                           (status list 2021)

Single organizational trust anchor       Multi-org federated trust
                                           (no single point of failure)

Physical smart card                      Embedded hardware wallet
                                           (TPM on Jetson)

Audit trail in central DB                Audit trail on distributed
                                           ledger (tamper-evident)

Door access (binary allow/deny)          Rich capability assertions
                                           ("authorized to fly BVLOS
                                           over Zone 3 until 18:00")
```

### The Unified Model

```
┌──────────────────────────────────────────────────────────────────┐
│              OPENSECURE DECENTRALIZED IDENTITY LAYER             │
└──────────────────────────────────────────────────────────────────┘

HUMAN LAYER (OpenPIV + DID Bridge):
  Guard/Pilot PIV card
  └─► PIV cert serial → resolves to → did:opensecure:piv:{serial}
      └─► DID Document contains PIV cert as verification method
      └─► Operator can issue VCs using PIV signing key
      └─► Operator VCs stored in mobile wallet (iOS/Android)

MACHINE LAYER (W3C DID for Devices):
  Drone TPM chip
  └─► Generates did:opensecure:drone:{uuid} at provisioning
      └─► DID Document anchored on Hyperledger Fabric
      └─► Public key in DID Doc = WireGuard identity key
      └─► Drone signs all evidence, telemetry, events with DID key

CREDENTIAL LAYER (Verifiable Credentials):
  OpenPIV CA issues:         Regulator issues:          Operator issues:
  └─ OperatorCredential      └─ FlightLicenseVC          └─ MissionAuthVC
  └─ DroneRegistrationVC     └─ AirspaceAuthVC           └─ EvidenceVC (scene)
  └─ MaintenanceVC           └─ BVLOSPermitVC            └─ ChainOfCustodyVC

TRUST LAYER (Federated Trust Registry):
  Ministry (Transport Canada / FAA)
  └─► Trusted issuer list: who can issue FlightLicenseVC, AirspaceAuthVC
  OpenSecure Hub
  └─► Trusted issuer list: who can issue DroneRegistrationVC, OperatorVC
  Customer Organization
  └─► Trusted issuer list: who can issue MissionAuthVC for their site
```

---

## W3C DID for Drones — Drone Decentralized Identifiers

### DID Method: `did:opensecure`

We define a new DID method `did:opensecure` that supports three sub-types:

```
did:opensecure:drone:{uuid}       — Drone hardware identity
did:opensecure:piv:{serial}       — PIV card holder (bridge from OpenPIV)
did:opensecure:org:{org_id}       — Organization identity (issuer)
```

### Drone DID Document

Every drone has a DID Document stored on Hyperledger Fabric (the same network used for evidence chain-of-custody in OS-GUARDIAN). This document is created at provisioning and updated whenever keys are rotated:

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://w3id.org/security/suites/ed25519-2020/v1",
    "https://opensecure.io/ns/drone/v1"
  ],
  "id": "did:opensecure:drone:f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "controller": "did:opensecure:org:acme-security-corp",

  "verificationMethod": [
    {
      "id": "did:opensecure:drone:f47ac10b#primary-key",
      "type": "Ed25519VerificationKey2020",
      "controller": "did:opensecure:drone:f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "publicKeyMultibase": "z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK"
      // Private key: TPM chip, never leaves hardware
    },
    {
      "id": "did:opensecure:drone:f47ac10b#wireguard-key",
      "type": "X25519KeyAgreementKey2020",
      "controller": "did:opensecure:drone:f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "publicKeyMultibase": "z6LSbysY2xFMRpGMhb7tFTLMpeuPRaqaWM1yECx2AtzE3KCc"
      // Same key as WireGuard peer key — cryptographic binding
    }
  ],

  "authentication": [
    "did:opensecure:drone:f47ac10b#primary-key"
  ],
  "assertionMethod": [
    "did:opensecure:drone:f47ac10b#primary-key"
    // Used to sign evidence VCs
  ],
  "keyAgreement": [
    "did:opensecure:drone:f47ac10b#wireguard-key"
    // Used for encrypted comms (VPN)
  ],

  "service": [
    {
      "id": "did:opensecure:drone:f47ac10b#telemetry",
      "type": "DroneTelemtryEndpoint",
      "serviceEndpoint": "wss://fleet.opensecure.local/drone/f47ac10b/telemetry"
    },
    {
      "id": "did:opensecure:drone:f47ac10b#rtsp",
      "type": "DroneVideoEndpoint",
      "serviceEndpoint": "rtsp://10.9.42.1:8554/live"
    },
    {
      "id": "did:opensecure:drone:f47ac10b#status",
      "type": "DroneStatusList2021",
      "serviceEndpoint": "https://registry.opensecure.local/status/drone/f47ac10b"
    }
  ],

  "opensecure:droneMetadata": {
    "serialNumber": "DRONE-ACME-007",
    "model": "Custom Hexacopter",
    "manufacturer": "OpenSecure Builds",
    "registrationNumber": "C-DRNE-789012",
    "registrationAuthority": "Transport Canada",
    "maxAltitudeAGL": 400,
    "maxSpeedMs": 20,
    "payloadCapabilites": ["EO", "LWIR", "LiDAR"],
    "remoteIdBroadcast": true,
    "laancEnabled": true
  },

  "created": "2026-03-04T09:00:00Z",
  "updated": "2026-03-04T09:00:00Z",
  "proof": {
    "type": "Ed25519Signature2020",
    "created": "2026-03-04T09:00:00Z",
    "verificationMethod": "did:opensecure:org:acme-security-corp#signing-key",
    "proofPurpose": "assertionMethod",
    "proofValue": "z58DAdFfa9SkqZMVPxAkpfoQcbkC..."
    // Signed by the ORGANIZATION at provisioning
  }
}
```

### DID Resolution

```python
# DID Resolver — resolves did:opensecure:drone:* from Hyperledger Fabric

class OpenSecureDIDResolver:

    async def resolve(self, did: str) -> DIDDocument:
        """
        Resolve a DID to its DID Document.
        Supports: did:opensecure:drone:*, did:opensecure:piv:*, did:opensecure:org:*
        """
        method, sub_type, identifier = self.parse_did(did)

        if sub_type == "drone":
            # Fetch from Hyperledger Fabric ledger
            return await self.fabric_client.query_chaincode(
                channel="identity-channel",
                chaincode="did-registry",
                function="resolve",
                args=[did]
            )

        elif sub_type == "piv":
            # Bridge: resolve from OpenPIV / Dogtag PKI
            serial = identifier
            cert = await self.dogtag_client.get_certificate(serial)
            return self.piv_cert_to_did_document(cert, did)

        elif sub_type == "org":
            # Fetch from Hub organization registry
            return await self.hub_client.get_org_did_document(identifier)

    def piv_cert_to_did_document(self, piv_cert, did) -> DIDDocument:
        """
        Convert an OpenPIV X.509 certificate into a DID Document.
        This is the bridge between the existing PIV infrastructure and W3C DID.
        The PIV cert's public key becomes the DID's verification method.
        """
        return {
            "@context": ["https://www.w3.org/ns/did/v1"],
            "id": did,
            "verificationMethod": [{
                "id": f"{did}#piv-auth-key",
                "type": "EcdsaSecp256r1VerificationKey2019",  # P-256 = PIV standard
                "controller": did,
                "publicKeyPem": piv_cert.public_key_pem
            }],
            "authentication": [f"{did}#piv-auth-key"],
            "assertionMethod": [f"{did}#piv-auth-key"]
        }
```

---

## Verifiable Credentials Ecosystem

### The Credential Web

```
ISSUERS                         CREDENTIALS                    HOLDERS
──────────────────────────────────────────────────────────────────────

Transport Canada / FAA          FlightLicenseVC                Pilot (DID)
                                BVLOSPermitVC
                                AirspaceAuthVC

OpenSecure CA (OpenPIV)         DroneRegistrationVC            Drone (DID)
                                OperatorCertificationVC        Operator (DID)
                                MaintenanceComplianceVC        Drone (DID)
                                InsuranceVC                    Org (DID)

Customer Organization           MissionAuthorizationVC         Drone (DID)
                                SiteAccessVC                   Drone (DID)
                                EvidenceRequestVC              Investigator (DID)

Drone (self-issued, signed)     EvidenceVC                     Fleet Ops
                                TelemetryAttestation           Fleet Ops
                                RemoteIDAttestation            Regulator

Maintenance Shop                InspectionPassVC               Drone (DID)
                                AirworthinessVC                Drone (DID)
```

### Credential Lifecycle

```
1. ISSUANCE:
   Issuer signs credential with their DID key
   Credential stored: holder's wallet (mobile / TPM)
   Anchored: status entry on Hyperledger Fabric

2. PRESENTATION:
   Holder presents credential (or selective disclosure)
   Verifier resolves issuer's DID → gets public key
   Verifier checks: signature, expiry, revocation status

3. REVOCATION:
   Issuer updates StatusList2021 (bitstring, off-chain)
   Status list URL is in the credential itself
   Drone checks status on preflight (online) or uses
   cached list (offline, max 24h stale)

4. OFFLINE OPERATION:
   Drone caches all needed VCs locally on NVMe
   Pre-flight: validates all cached VCs online
   In-flight: verifies against cached status lists
   On-dock: syncs new VCs, updated status lists
```

---

## Drone Credential Schema Library

### DroneRegistrationVC

Issued by OpenSecure CA at provisioning. The drone's birth certificate.

```json
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://opensecure.io/ns/drone-credentials/v1"
  ],
  "id": "urn:uuid:3978344f-8596-4c3c-a978-2fcf9fda487e",
  "type": ["VerifiableCredential", "DroneRegistrationCredential"],
  "issuer": "did:opensecure:org:opensecure-ca",
  "issuanceDate": "2026-03-04T09:00:00Z",
  "expirationDate": "2028-03-04T09:00:00Z",

  "credentialSubject": {
    "id": "did:opensecure:drone:f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "serialNumber": "DRONE-ACME-007",
    "model": "Custom Hexacopter v2",
    "manufacturer": "OpenSecure Builds",
    "ownerDID": "did:opensecure:org:acme-security-corp",
    "regulatoryRegistration": {
      "authority": "Transport Canada",
      "registrationNumber": "C-DRNE-789012",
      "registrationDate": "2026-03-01",
      "remoteIdCompliant": true
    },
    "capabilities": {
      "maxAltitudeAGL_m": 400,
      "maxSpeedMs": 20,
      "flightTime_min": 42,
      "payloads": ["EO_4K", "LWIR_Thermal", "LiDAR"],
      "bvlosCapable": false,
      "nightOperationsCapable": true
    },
    "hardwareSecurity": {
      "tpmPresent": true,
      "tpmVersion": "2.0",
      "secureBootEnabled": true,
      "firmwareSignatureVerified": true
    }
  },

  "credentialStatus": {
    "id": "https://registry.opensecure.local/status/drones/1#42",
    "type": "StatusList2021Entry",
    "statusPurpose": "revocation",
    "statusListIndex": "42",
    "statusListCredential": "https://registry.opensecure.local/status/drones/1"
  },

  "proof": {
    "type": "Ed25519Signature2020",
    "created": "2026-03-04T09:00:00Z",
    "verificationMethod": "did:opensecure:org:opensecure-ca#signing-key-2026",
    "proofPurpose": "assertionMethod",
    "proofValue": "z3FXQjecWufY4qRQKHrtfeXXyz..."
  }
}
```

### MaintenanceComplianceVC

Issued by a certified maintenance shop after each inspection. Drone cannot fly if this is expired or revoked.

```json
{
  "type": ["VerifiableCredential", "MaintenanceComplianceCredential"],
  "issuer": "did:opensecure:org:certified-drone-maintenance-inc",
  "issuanceDate": "2026-03-01T00:00:00Z",
  "expirationDate": "2026-09-01T00:00:00Z",

  "credentialSubject": {
    "id": "did:opensecure:drone:f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "inspectionDate": "2026-02-28",
    "inspectorDID": "did:opensecure:piv:7F3A9C21B4E86D50",
    "inspectorCertificationNumber": "UAV-MAINT-ON-4421",
    "cyclesSinceLastInspection": 187,
    "flightHoursSinceLastInspection": 46.3,
    "findings": {
      "motorsStatus": "PASS",
      "propsStatus": "PASS",
      "batteryHealthPercent": 94,
      "gpsStatus": "PASS",
      "cameraGimbalStatus": "PASS",
      "firmwareVersion": "4.2.1",
      "firmwareUpToDate": true
    },
    "airworthyCertificate": "AWC-2026-DRONE-007-0301",
    "nextInspectionDue": "2026-09-01",
    "clearanceLevel": "STANDARD_OPS"
  }
}
```

### FlightLicenseVC

Issued by the regulatory authority (Transport Canada / FAA) to the pilot/operator.

```json
{
  "type": ["VerifiableCredential", "FlightLicenseCredential"],
  "issuer": "did:opensecure:org:transport-canada",
  "issuanceDate": "2025-01-15T00:00:00Z",
  "expirationDate": "2027-01-15T00:00:00Z",

  "credentialSubject": {
    "id": "did:opensecure:piv:7F3A9C21B4E86D50",
    "licenseType": "Advanced_Operations_Certificate",
    "licenseNumber": "RPAS-ADV-ON-88421",
    "licenseAuthority": "Transport Canada",
    "authorizedOperations": [
      "VLOS",
      "VLOS_NightOps",
      "BVLOS_WithATCApproval"
    ],
    "authorizedAircraftClasses": ["25kg_or_less"],
    "biometricBinding": {
      "fingerprint_hash": "sha256:a3f9c2...",
      // Bound to the same biometric in OpenPIV — prevents credential sharing
      "binding_method": "OpenPIV_Biometric_Hash"
    }
  }
}
```

### MissionAuthorizationVC

Short-lived credential issued by the organization (or auto-issued by Fleet Ops MCS) for a specific mission. This is the "go/no-go" credential the drone checks before arming.

```json
{
  "type": ["VerifiableCredential", "MissionAuthorizationCredential"],
  "issuer": "did:opensecure:org:acme-security-corp",
  "issuanceDate": "2026-03-04T22:00:00Z",
  "expirationDate": "2026-03-04T23:00:00Z",
  // Valid for 1 hour — not transferable, not reusable after expiry

  "credentialSubject": {
    "id": "did:opensecure:drone:f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "missionId": "MSN-2026-0304-0042",
    "missionType": "INCIDENT_RESPONSE",
    "authorizedPilotDID": "did:opensecure:piv:7F3A9C21B4E86D50",
    // If autonomous: "authorizedPilotDID": "did:opensecure:org:acme-security-corp#autopilot"

    "geofence": {
      "type": "Polygon",
      "coordinates": [[[-75.70, 45.42], [-75.68, 45.42], [-75.68, 45.40], [-75.70, 45.40]]],
      "maxAltitudeAGL_m": 120,
      "minAltitudeAGL_m": 30,
      "hard_limit": true
      // Drone firmware enforces this — CANNOT be overridden by software command
    },

    "laancAuthorization": {
      "authorizationNumber": "LAANC-2026-0304-98712",
      "ceiling_ft": 400,
      "validFrom": "2026-03-04T22:00:00Z",
      "validTo": "2026-03-04T23:00:00Z",
      "authorizedBy": "did:opensecure:org:airmap-uss"
    },

    "hubEventContext": {
      "triggerEventId": "evt_9f2a3c4d",
      "triggerService": "OS-SENTINEL",
      "triggerDescription": "Motion detected at Gate C after hours"
    },

    "restrictions": {
      "maxSpeedMs": 12,
      "lightingRequired": false,
      "videoRecordingMandatory": true,
      "chainOfCustodyRequired": true
    }
  }
}
```

---

## Operator Authorization via Verifiable Credentials

### The Preflight Authorization Flow

Before any drone arms its motors, it executes a **VC-based preflight authorization check**. This works whether online or offline (using cached credentials).

```python
# Drone-side preflight authorization engine
# Runs on Jetson Orin NX before every flight

class PreflightVCAuthorizationEngine:

    async def authorize_flight(self, mission_vc: VC, operator_did: str) -> AuthResult:
        """
        Execute full VC-based preflight check.
        Returns: AUTHORIZED or DENIED with specific reason.
        All results logged to blockchain COC.
        """

        checks = []

        # 1. DRONE REGISTRATION — is this drone legally registered?
        reg_vc = self.wallet.get_vc("DroneRegistrationCredential")
        checks.append(await self.verify_vc(reg_vc, expected_subject=self.drone_did))

        # 2. MAINTENANCE COMPLIANCE — is maintenance current?
        maint_vc = self.wallet.get_vc("MaintenanceComplianceCredential")
        checks.append(await self.verify_vc(maint_vc, expected_subject=self.drone_did))
        if maint_vc.expired():
            return AuthResult.DENIED("MaintenanceVC expired. Drone grounded.")

        # 3. OPERATOR FLIGHT LICENSE — does the operator hold a valid license?
        license_vc = await self.resolve_vc(operator_did, "FlightLicenseCredential")
        checks.append(await self.verify_vc(license_vc, expected_subject=operator_did))
        if not self.license_covers_mission(license_vc, mission_vc):
            return AuthResult.DENIED(f"Operator not licensed for {mission_vc.missionType}")

        # 4. MISSION AUTHORIZATION — is this specific mission authorized?
        checks.append(await self.verify_vc(mission_vc, expected_subject=self.drone_did))
        if mission_vc.expired():
            return AuthResult.DENIED("MissionVC expired — request new mission.")

        # 5. AIRSPACE AUTHORIZATION — LAANC clearance inside MissionVC
        laanc = mission_vc.laancAuthorization
        if not self.is_laanc_valid(laanc):
            return AuthResult.DENIED("LAANC authorization invalid or expired.")

        # 6. REVOCATION CHECK — check StatusList2021 for all VCs
        for vc in [reg_vc, maint_vc, license_vc, mission_vc]:
            is_revoked = await self.check_status_list(vc)
            if is_revoked:
                return AuthResult.DENIED(f"VC {vc.id} has been revoked.")

        # 7. GEOFENCE UPLOAD — load geofence from MissionVC into firmware
        await self.upload_geofence_to_pixhawk(mission_vc.geofence)
        # Hard-coded in firmware — software commands CANNOT override

        # 8. LOG TO BLOCKCHAIN
        await self.record_authorization_on_chain({
            "drone_did": self.drone_did,
            "operator_did": operator_did,
            "mission_id": mission_vc.missionId,
            "all_checks_passed": all(c.passed for c in checks),
            "timestamp": utcnow(),
            "drone_signature": self.tpm.sign(str(checks))
        })

        if all(c.passed for c in checks):
            return AuthResult.AUTHORIZED(checks)
        else:
            failed = [c for c in checks if not c.passed]
            return AuthResult.DENIED(f"Failed: {[c.reason for c in failed]}")
```

### Autonomous Mission Authorization (No Human Pilot)

When Fleet Ops dispatches a drone automatically (e.g., triggered by an OS-SENTINEL alert), the Mission Control Server acts as an automated VC issuer:

```python
# MCS auto-issues MissionAuthorizationVC for autonomous dispatch

class AutoDispatchVCIssuer:

    async def issue_autonomous_mission_vc(
        self,
        drone_did: str,
        hub_event: HubEvent,
        laanc_auth: LAAnCAuthorization
    ) -> MissionAuthorizationVC:

        # MCS acts as the authorized issuer on behalf of the organization
        # MCS's signing key is itself a DID: did:opensecure:org:acme#mcs-autopilot
        issuer_did = f"did:opensecure:org:{self.org_id}#mcs-autopilot"

        # Generate mission VC
        vc = MissionAuthorizationVC(
            issuer=issuer_did,
            subject_id=drone_did,
            missionId=generate_mission_id(),
            missionType=self.classify_mission(hub_event),
            authorizedPilotDID=issuer_did,
            # ↑ Autonomous: the MCS IS the authorized "pilot"

            geofence=self.compute_geofence(hub_event.location),
            laancAuthorization=laanc_auth,
            validFor=timedelta(hours=1),

            # Trace back to the triggering event
            hubEventContext={
                "triggerEventId": hub_event.id,
                "triggerService": hub_event.source_service,
                "triggerDescription": hub_event.description
            }
        )

        # Sign with MCS key (stored in HSM on Fleet Ops server)
        signed_vc = await self.hsm.sign_vc(vc, issuer_did)

        # Push to drone's VC wallet via VPN
        await self.push_vc_to_drone(drone_did, signed_vc)

        # Record issuance on blockchain
        await self.record_vc_issuance(signed_vc)

        return signed_vc
```

---

## Evidence as Verifiable Presentations

### Every Piece of Evidence is Self-Proving

The most powerful application of VCs in OS-DRONE is making **video evidence self-authenticating**. Instead of relying on a central server to prove "this video is genuine", the drone produces a Verifiable Presentation that cryptographically proves:

1. Which drone captured it (DID)
2. Which operator authorized the mission (DID)
3. What the GPS location and timestamp were (signed at capture)
4. That the video file has not been tampered with (SHA256 + signature)
5. The chain of every person who accessed it (Verifiable Presentations)

```json
{
  "@context": ["https://www.w3.org/2018/credentials/v1",
               "https://opensecure.io/ns/drone-evidence/v1"],
  "type": ["VerifiablePresentation", "DroneEvidencePresentation"],

  "holder": "did:opensecure:drone:f47ac10b-58cc-4372-a567-0e02b2c3d479",

  "verifiableCredential": [

    // CREDENTIAL 1: Prove the drone is registered and legitimate
    { /* DroneRegistrationVC — included inline */ },

    // CREDENTIAL 2: Prove the mission was authorized
    { /* MissionAuthorizationVC — proves operator, geofence, LAANC */ },

    // CREDENTIAL 3: The evidence record itself
    {
      "type": ["VerifiableCredential", "DroneEvidenceCredential"],
      "issuer": "did:opensecure:drone:f47ac10b-58cc-4372-a567-0e02b2c3d479",
      // Self-issued by the DRONE — the drone attests to its own capture

      "credentialSubject": {
        "id": "urn:evidence:drone:f47ac10b:2026-03-04T22:17:05Z",

        "capturedBy": "did:opensecure:drone:f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "missionId": "MSN-2026-0304-0042",
        "authorizedBy": "did:opensecure:piv:7F3A9C21B4E86D50",

        "captureMetadata": {
          "startTime": "2026-03-04T22:17:05Z",
          "endTime": "2026-03-04T22:22:05Z",
          "duration_s": 300,
          "gps_start": {"lat": 45.4215, "lon": -75.6972, "alt_m": 80},
          "gps_end": {"lat": 45.4220, "lon": -75.6965, "alt_m": 80},
          "sensorMode": "FUSION_THERMAL_DOMINANT",
          "firmwareVersion": "4.2.1"
        },

        "fileIntegrity": {
          "filename": "DRONE-ACME-007_2026-03-04T22-17-05Z.mp4",
          "sha256": "a3f9c2b1d4e7f8a0c1b2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4",
          "size_bytes": 524288000,
          "hash_computed_at": "2026-03-04T22:22:06Z",
          // Hash computed IMMEDIATELY after recording stops, before any upload
          "hash_computed_by": "did:opensecure:drone:f47ac10b#primary-key"
        },

        "storageLocation": {
          "minioUri": "s3://drone-evidence/acme/DRONE-007/2026-03-04/...",
          "blockchainTxHash": "0x7f3a9c21b4e8..."
        }
      },

      "proof": {
        "type": "Ed25519Signature2020",
        "verificationMethod": "did:opensecure:drone:f47ac10b#primary-key",
        "proofPurpose": "assertionMethod",
        "proofValue": "zABCDEFG..."
        // SIGNED BY THE DRONE'S TPM — unforgeble without physical access to drone
      }
    }
  ],

  // The presentation itself is signed by the drone's DID
  "proof": {
    "type": "Ed25519Signature2020",
    "created": "2026-03-04T22:22:10Z",
    "verificationMethod": "did:opensecure:drone:f47ac10b#primary-key",
    "proofPurpose": "authentication",
    "proofValue": "zXYZABC..."
  }
}
```

### Evidence Chain of Custody as VC Chain

Every access to evidence generates a new VC that extends the chain:

```
INITIAL EVIDENCE VC         FIRST ACCESS VC             EXPORT VC
(signed by drone)           (signed by investigator)    (signed by evidence mgr)
      │                           │                            │
      └──── references ───────────┤                            │
                                  └──── references ────────────┘
                                        (entire chain provable)

Python:
def create_access_vc(evidence_vc_id, accessor_did, purpose):
    return VC(
        type="EvidenceAccessCredential",
        issuer=accessor_did,
        subject={
            "evidenceVCId": evidence_vc_id,
            "accessedBy": accessor_did,
            "accessTime": utcnow(),
            "purpose": purpose,  # "investigation", "court", "review"
            "actions": ["VIEW"],  # or ["VIEW", "DOWNLOAD", "EXPORT"]
        }
    ).sign(accessor_private_key)
```

---

## Trust Registry & Federation

### Decentralized Trust Registry on Hyperledger Fabric

The Trust Registry answers one question: **"Is this issuer trusted to issue this type of credential?"**

```json
// Trust Registry Entry (on-chain)
{
  "issuerDID": "did:opensecure:org:transport-canada",
  "trustedFor": [
    "FlightLicenseCredential",
    "BVLOSPermitCredential",
    "AirspaceAuthorizationCredential"
  ],
  "trustLevel": "REGULATORY_AUTHORITY",
  "addedBy": "did:opensecure:org:opensecure-root",
  "addedAt": "2026-01-01T00:00:00Z",
  "governanceFramework": "https://tc.canada.ca/drone-vc-governance-v1.json"
}

{
  "issuerDID": "did:opensecure:org:opensecure-ca",
  "trustedFor": [
    "DroneRegistrationCredential",
    "OperatorCertificationCredential",
    "MaintenanceComplianceCredential"
  ],
  "trustLevel": "PLATFORM_AUTHORITY",
  "addedBy": "did:opensecure:org:opensecure-root",
  "addedAt": "2026-01-01T00:00:00Z"
}

{
  "issuerDID": "did:opensecure:org:acme-security-corp",
  "trustedFor": [
    "MissionAuthorizationCredential",
    "SiteAccessCredential"
  ],
  "trustLevel": "CUSTOMER_ORGANIZATION",
  // Customer orgs can only issue mission-level VCs — not regulatory ones
  "addedBy": "did:opensecure:org:opensecure-ca",
  "addedAt": "2026-03-01T00:00:00Z"
}
```

### Multi-Level Trust Hierarchy

```
LEVEL 0: ROOT OF TRUST
  did:opensecure:org:opensecure-root
  └── Anchored on multiple blockchains (Hyperledger + Ethereum)
  └── Controls who can be a "PLATFORM_AUTHORITY"

LEVEL 1: REGULATORY AUTHORITIES (government-endorsed)
  did:opensecure:org:transport-canada
  did:opensecure:org:faa
  did:opensecure:org:easa
  └── Issue: FlightLicenseVC, BVLOSPermitVC, AirspaceAuthVC

LEVEL 2: PLATFORM AUTHORITIES (OpenSecure-endorsed)
  did:opensecure:org:opensecure-ca     (main CA)
  did:opensecure:org:certified-maintenance-inc  (maintenance shops)
  └── Issue: DroneRegistrationVC, MaintenanceVC, OperatorVC

LEVEL 3: CUSTOMER ORGANIZATIONS
  did:opensecure:org:acme-security-corp
  did:opensecure:org:city-of-ottawa-police
  └── Issue: MissionAuthVC, SiteAccessVC, EvidenceRequestVC

LEVEL 4: DEVICES (self-attesting, within issued scope)
  did:opensecure:drone:f47ac10b-...
  └── Issue: EvidenceVC (self-signed, verifiable against DroneRegistrationVC)
             TelemetryAttestationVC
             RemoteIDAttestationVC
```

---

## Zero-Knowledge Proofs for Privacy-Preserving Compliance

### Proving Compliance Without Revealing Data

Some compliance scenarios require the drone to prove a fact **without revealing the underlying data**. ZKPs enable this:

```
SCENARIO 1: Operator Privacy During Cross-Org Sharing
  Problem:
    Org B wants to borrow a drone from Org A.
    Org B needs to verify the operator is licensed.
    But Org A doesn't want to reveal the operator's full identity.

  ZKP Solution:
    Prove: "The pilot holds a valid FlightLicenseVC issued by Transport Canada
            AND the license covers VLOS night operations
            AND the license has not expired"
    WITHOUT revealing: pilot's name, DID, license number, biometric

  Implementation:
    Using: BBS+ Signatures (W3C standard, supports selective disclosure)
    Operator selects: reveal only licenseType and authorizedOperations
    Org B verifies: signature chain from Transport Canada → valid
    Org B does NOT see: operatorDID, name, personal details

SCENARIO 2: Proving a Drone is Compliant Without Exposing Fleet Data
  Regulatory audit: Prove all drones in fleet have current MaintenanceVC
  WITHOUT revealing: individual drone serials, flight hours, findings

  ZKP: "I have N drones. All N have MaintenanceVCs issued by a certified shop
        in the last 6 months. No drone has a FAIL finding."
  Proves compliance. Auditor cannot derive drone count, serial numbers, or
  the maintenance shops used (competitive intelligence).

SCENARIO 3: Age/Time Attestation for Evidence
  Court needs to know: was this video captured before the incident was reported?
  WITHOUT revealing: exact timestamp, drone route, mission details

  ZKP: "Video was captured between T1 and T2, before T_report"
  Using: Range proof over timestamp values (Bulletproofs)
```

```python
# BBS+ Selective Disclosure — Operator shows only what's needed
from bbs_bls12381 import BbsSignature

class SelectiveDisclosureProver:

    def prove_license_without_identity(
        self, license_vc: FlightLicenseVC, required_fields: list
    ) -> SelectiveDisclosureProof:
        """
        Create a ZKP that reveals only the required fields of a VC.
        Verifier can confirm signature validity without seeing hidden fields.
        """
        # Reveal only: licenseType, authorizedOperations, expirationDate
        # Hide: id (operator DID), licenseNumber, biometricBinding, issuanceDate
        revealed_indices = [
            license_vc.field_index("licenseType"),
            license_vc.field_index("authorizedOperations"),
            license_vc.field_index("expirationDate")
        ]

        proof = BbsSignature.create_proof(
            messages=license_vc.signed_messages,
            signature=license_vc.bbs_signature,
            revealed_indices=revealed_indices,
            nonce=os.urandom(32)  # Prevents replay attacks
        )

        return SelectiveDisclosureProof(
            disclosed_messages={
                "licenseType": license_vc.licenseType,
                "authorizedOperations": license_vc.authorizedOperations,
                "expirationDate": license_vc.expirationDate
            },
            proof=proof,
            issuer_did=license_vc.issuer
            # Verifier can verify TC's signature covers all fields,
            # including the hidden ones, without seeing them
        )
```

---

## Cross-Organization Drone Sharing

### The Decentralized Borrowing Protocol

This mirrors the Provincial PIV cross-organization model, but for drones. An organization can authorize another organization to use their drones without requiring a central broker — just VC exchange.

```
SCENARIO: City Police wants to borrow Acme Security's drone for a BOLO

TRADITIONAL (centralized):
  Police call Acme → Acme admin logs in → creates account for officer →
  officer logs in → admin assigns drone → 20-30 minutes
  Problem: requires Acme's staff to be available, creates Acme account for police

DECENTRALIZED (VC-based):
  Police officer presents: FlightLicenseVC + PoliceAuthorizationVC (< 2 min)
  Acme's Fleet Ops verifies VCs → issues CrossOrgMissionAuthVC → drone ready
  No Acme staff intervention. No police account in Acme's system.
```

```python
# Cross-Org Drone Authorization Protocol

class CrossOrgDroneAuthorizationProtocol:

    async def handle_borrow_request(
        self,
        requester_org_did: str,
        requester_operator_did: str,
        presented_vcs: list[VC],
        requested_drone_did: str,
        requested_duration: timedelta
    ) -> CrossOrgMissionAuthVC:

        # Step 1: Verify requester organization is in Trust Registry
        trust_entry = await self.trust_registry.lookup(requester_org_did)
        if not trust_entry or trust_entry.level < TrustLevel.VERIFIED_ORG:
            raise AuthorizationError("Requester org not in Trust Registry")

        # Step 2: Verify operator's FlightLicenseVC (from regulator)
        license_vc = self.find_vc(presented_vcs, "FlightLicenseCredential")
        await self.verify_vc(license_vc)  # Checks TC/FAA DID signature

        # Step 3: Verify operator's authorization from THEIR org
        # (Police must have police dept VC — not just a personal license)
        org_auth_vc = self.find_vc(presented_vcs, "OperatorOrganizationCredential")
        await self.verify_vc(org_auth_vc)

        # Step 4: Check our org's policy — are we open to sharing with requester?
        sharing_policy = await self.get_sharing_policy(
            our_org=self.org_did,
            requester_org=requester_org_did
        )
        if not sharing_policy.allows_sharing():
            raise AuthorizationError("Sharing policy denies this request")

        # Step 5: Apply restrictions from sharing policy
        # e.g., Police can only use our drones for 2h, in our geofence, no BVLOS
        restrictions = sharing_policy.get_restrictions(
            license_vc.authorizedOperations
        )

        # Step 6: Issue CrossOrgMissionAuthVC (OUR org signs it)
        cross_vc = CrossOrgMissionAuthVC(
            issuer=self.org_did,
            subject=requested_drone_did,
            authorizedOperatorDID=requester_operator_did,
            authorizedOrganizationDID=requester_org_did,
            validFor=min(requested_duration, timedelta(hours=4)),
            geofence=restrictions.geofence,
            maxAltitude=restrictions.max_altitude,
            evidenceSharingAgreement={
                "videoRetentionDays": 30,
                "accessibleBy": [requester_org_did, self.org_did],
                "evidenceOwnership": "JOINT"
            }
        )
        signed_vc = await self.sign_vc(cross_vc)

        # Step 7: Record borrowing event on blockchain
        await self.record_cross_org_loan(signed_vc)

        # Step 8: Push VC to drone wallet via VPN
        await self.push_vc_to_drone(requested_drone_did, signed_vc)

        return signed_vc
```

---

## Blockchain Anchoring Strategy

### What Goes On-Chain vs. Off-Chain

Not everything belongs on the blockchain. The design follows the principle: **anchor only what needs to be universally verifiable and immutable**.

```
ON-CHAIN (Hyperledger Fabric — existing OS-GUARDIAN network):

  DID Registry:
    ├── DID Documents for all drones, orgs (public keys, service endpoints)
    └── DID updates (key rotation events)

  Trust Registry:
    ├── Trusted issuer entries
    └── Governance framework references

  Credential Status (StatusList2021):
    ├── Revocation bitstrings (one bit per credential — not the credentials)
    └── Suspension bitstrings

  Evidence Attestations:
    ├── SHA256 of evidence VCs (not the VCs themselves — saves space)
    └── Evidence access log (who accessed what, when)

  Cross-Org Authorizations:
    ├── Drone borrowing events (org A loaned drone X to org B, mission Y)
    └── Authorization grants/revocations

OFF-CHAIN (IPFS + MinIO):

  Full DID Documents:
    └── Content-addressed on IPFS (hash = DID resolution endpoint)

  Full Verifiable Credentials:
    └── Stored in holder's wallet (drone TPM / officer mobile app)

  Full Verifiable Presentations:
    └── Stored in Fleet Ops MinIO (evidence bucket — same as today)

  Status List Credentials:
    └── Served from Fleet Ops HTTPS endpoint
        (URL is in every credential — quick to check)
```

### Smart Contract (Hyperledger Chaincode) — Key Functions

```go
// did-registry chaincode (Go)

// Register a new DID Document
func (s *DIDRegistry) RegisterDID(ctx contractapi.TransactionContextInterface,
    did string, didDocumentJSON string, signature string) error {

    // Verify the caller has authority to register this DID
    // (org must sign new drone DIDs)
    err := s.verifyRegistrationAuthority(ctx, did, signature)
    if err != nil { return err }

    // Store DID Document
    return ctx.GetStub().PutState(did, []byte(didDocumentJSON))
}

// Revoke a credential (update status list bit)
func (s *DIDRegistry) RevokeCredential(ctx contractapi.TransactionContextInterface,
    credentialId string, statusListIndex int, revokerDID string) error {

    // Only the issuer of the credential can revoke it
    credential := s.getCredentialRecord(ctx, credentialId)
    if credential.IssuerDID != revokerDID {
        return fmt.Errorf("only issuer can revoke")
    }

    return s.updateStatusBit(ctx, statusListIndex, true)
}

// Record evidence attestation (immutable)
func (s *DIDRegistry) RecordEvidence(ctx contractapi.TransactionContextInterface,
    evidenceId string, sha256 string, droneDID string,
    missionId string, timestamp string, droneSignature string) error {

    // Verify drone signature (same as OS-GUARDIAN's existing COC logic)
    err := s.verifyDIDSignature(ctx, droneDID, sha256, droneSignature)
    if err != nil { return fmt.Errorf("invalid drone signature: %v", err) }

    record := EvidenceRecord{
        EvidenceId: evidenceId, SHA256: sha256,
        DroneDID: droneDID, MissionId: missionId,
        Timestamp: timestamp, Immutable: true
    }
    return ctx.GetStub().PutState(evidenceId, record.ToJSON())
}
```

---

## OpenSecure PIV + DID Bridge

### Unifying the Two Identity Systems

The PIV infrastructure (OpenPIV, Dogtag, FIPS 201) and the W3C DID system are complementary, not competing. The bridge makes them interoperable:

```
                    OPENSECURE IDENTITY BRIDGE
                    ─────────────────────────

Human PIV Card                          W3C DID Ecosystem
─────────────────                       ─────────────────────────
Card serial: 7F3A9C21B4E86D50           did:opensecure:piv:7F3A9C21B4E86D50
PIV Auth cert (9A): ECC P-256           Verification method: same P-256 key
CHUID: on card                          DID Document: on Hyperledger Fabric
OCSP revocation: Dogtag                 VC StatusList2021: Fleet Ops HTTPS
Card holder: John Doe                   DID Subject: same person
Issuer: OpenPIV CA                      VC Issuer: did:opensecure:org:openpiv-ca

HOW BRIDGE WORKS:
  1. At PIV enrollment, OpenPIV CA creates BOTH:
     a. X.509 certificate (for FIPS 201 / OS-PACS / smart card systems)
     b. DID Document (for W3C VC ecosystem)
     → Same key pair, two representations

  2. PIV card can sign W3C VCs:
     Guard taps PIV → signature request to card → card signs with 9C key
     → Result is a valid W3C VC proof (EcdsaSecp256r1 = FIPS P-256)

  3. Any system that accepts PIV certs ALSO accepts VC proofs from PIV
  4. Any system that accepts W3C VCs ALSO accepts PIV-signed credentials
```

```python
# PIV-DID Bridge — the enrollment step that creates both representations

class PIVDIDBridge:

    async def enroll_with_dual_representation(
        self,
        person_info: PersonInfo,
        piv_card: PIVCard
    ) -> tuple[X509Certificate, DIDDocument]:

        # Step 1: Standard OpenPIV enrollment (existing flow)
        piv_cert = await self.openpiv_ca.issue_piv_cert(person_info, piv_card)

        # Step 2: Create DID from the PIV certificate
        did = f"did:opensecure:piv:{piv_cert.serial_number_hex}"

        did_document = DIDDocument(
            id=did,
            verificationMethod=[{
                "id": f"{did}#piv-auth-key",
                "type": "EcdsaSecp256r1VerificationKey2019",
                "controller": did,
                "publicKeyPem": piv_cert.subject_public_key_pem
                # SAME KEY as PIV certificate — zero overhead, one key pair
            }],
            authentication=[f"{did}#piv-auth-key"],
            assertionMethod=[f"{did}#piv-auth-key"],
            service=[{
                "id": f"{did}#vc-wallet",
                "type": "LinkedVerifiableCredentialWallet",
                "serviceEndpoint": f"https://wallet.opensecure.local/{piv_cert.serial_number_hex}"
            }, {
                "id": f"{did}#piv-status",
                "type": "PIVCertificateStatus",
                "serviceEndpoint": f"https://ocsp.opensecure.local/piv"
                # Points to existing Dogtag OCSP — existing revocation reused
            }]
        )

        # Sign DID Document with OpenPIV CA (same CA as PIV cert)
        signed_did_document = await self.openpiv_ca.sign_did_document(did_document)

        # Anchor on Hyperledger Fabric
        await self.fabric_client.register_did(did, signed_did_document)

        # Step 3: Issue initial OperatorCertificationVC to this person
        operator_vc = await self.issue_operator_vc(did, person_info, piv_cert)

        return piv_cert, did_document, operator_vc
```

---

## Implementation Stack

### Complete Technology Stack

| Layer | Component | Technology | Notes |
|-------|-----------|-----------|-------|
| DID Method | `did:opensecure` resolver | Python (FastAPI) | Custom resolver, open spec |
| DID Storage | DID Document registry | Hyperledger Fabric | Same network as OS-GUARDIAN COC |
| VC Issuance | Credential issuer service | SpruceID `didkit` (Rust) | Open-source W3C compliant |
| VC Verification | Verifier service | SpruceID `didkit` | Same library |
| VC Wallet (drone) | Hardware wallet | TPM 2.0 + custom agent | Private keys never leave TPM |
| VC Wallet (operator) | Mobile wallet | SpruceID `credible` app | iOS/Android, open source |
| ZKP (selective disclosure) | BBS+ proofs | `bbs-signatures` (Rust) | W3C LD-Proofs compatible |
| Trust Registry | On-chain registry | Hyperledger Fabric chaincode | Same network as DID docs |
| Status List | Revocation | StatusList2021 | HTTPS-served bitstring |
| PIV Bridge | DID ↔ X.509 bridge | Custom Python service | Links OpenPIV to W3C DID |
| Blockchain | Anchoring | Hyperledger Fabric | Shared with OS-GUARDIAN |
| Key Storage (MCS) | Signing keys | HashiCorp Vault + HSM | Existing infrastructure |
| Key Storage (drone) | Signing keys | TPM 2.0 chip on Jetson | Provisioned at manufacture |

### New Services Added to Fleet Ops

```yaml
# docker-compose additions for DID/VC infrastructure

services:

  did-resolver:
    image: opensecure/did-resolver:1.0
    ports: ["8550:8550"]
    environment:
      FABRIC_PEER_URL: "grpc://fabric-peer:7051"
      DOGTAG_OCSP_URL: "https://ocsp.opensecure.local"
    # Resolves did:opensecure:* → DID Documents
    # Bridges did:opensecure:piv:* → OpenPIV certs

  vc-issuer:
    image: opensecure/vc-issuer:1.0
    ports: ["8551:8551"]
    environment:
      HSM_URL: "pkcs11:..."
      TRUST_REGISTRY_URL: "grpc://fabric-peer:7051"
    # Issues, signs all VCs for Fleet Ops
    # MCS calls this to issue MissionAuthorizationVCs

  vc-verifier:
    image: opensecure/vc-verifier:1.0
    ports: ["8552:8552"]
    # Verifies presented VCs, checks Trust Registry, StatusList2021

  trust-registry:
    # Runs as Hyperledger Fabric chaincode (no separate container)
    # Accessed via fabric-peer

  status-list-server:
    image: opensecure/status-list:1.0
    ports: ["8553:8553"]
    # Serves StatusList2021 bitstrings for revocation checking
    # Drone caches these for offline operation (24h TTL)
```

---

## Security Threat Model

| Threat | Attack | Mitigation |
|--------|--------|-----------|
| Credential theft | Steal operator's VC wallet | TPM binding — VC unusable without TPM. Biometric binding from PIV. |
| Forged MissionVC | Attacker issues fake mission auth | Trust Registry — only org DIDs in registry can issue MissionVCs |
| Replay attack | Reuse expired MissionVC | Expiry enforced in drone firmware. Nonce in each presentation. |
| Drone impersonation | Claim another drone's DID | DID proof requires TPM private key — physically impossible to forge |
| Evidence tampering | Modify video after capture | SHA256 in self-signed drone EvidenceVC. On-chain hash. Detectable. |
| VC revocation delay | Use revoked VC during offline window | Max 24h cache. Preflight requires fresh status check (online). |
| Trust Registry poisoning | Add malicious org as trusted issuer | Registry entries require multi-sig from Root of Trust (threshold 2-of-3) |
| Cross-org abuse | Org A uses borrowed drone outside policy | Geofence in MissionVC is loaded into firmware — hardware-enforced |
| Regulatory spoofing | Fake TC/FAA VC | Trust Registry only accepts DIDs endorsed by government e-government frameworks |

---

## API Reference

### New Fleet Ops API Endpoints (DID/VC Layer)

```
BASE: https://api.opensecure.com/drone/v1/

IDENTITY
GET    /identity/{drone_id}/did              Drone's DID Document
GET    /identity/{drone_id}/credentials      Drone's credential wallet (summary)
POST   /identity/{drone_id}/credentials      Push new VC to drone wallet
DELETE /identity/{drone_id}/credentials/{id} Revoke a credential

MISSION AUTHORIZATION
POST   /missions/{mission_id}/auth-vc        Issue MissionAuthorizationVC
GET    /missions/{mission_id}/auth-vc        Get current MissionAuthorizationVC
DELETE /missions/{mission_id}/auth-vc        Revoke mission auth (abort)

EVIDENCE
GET    /evidence/{id}/vp                     Full Verifiable Presentation (court-ready)
GET    /evidence/{id}/verify                 Verify VP signature chain
POST   /evidence/{id}/access-vc             Issue EvidenceAccessVC (log access)
POST   /evidence/{id}/share                 Create ShareAuthorizationVC (cross-org)

TRUST REGISTRY
GET    /trust/issuers                        List all trusted VC issuers
POST   /trust/issuers                        Propose new trusted issuer
GET    /trust/verify/{vc_id}                 Verify a VC against Trust Registry
GET    /trust/status/{status_list_id}        Get StatusList2021 bitstring

CROSS-ORG
POST   /cross-org/request                    Request to borrow drone (submit VCs)
GET    /cross-org/loans                      Active cross-org authorizations
DELETE /cross-org/loans/{id}                 Revoke cross-org authorization
```

---

**Document Version**: 1.0
**Platform**: OS-DRONE v1.0
**Standards**: W3C DID Core 1.0, W3C VC Data Model 2.0, StatusList2021,
              BBS+ LD-Proofs, FIPS 201-3 (PIV), Hyperledger Fabric 2.x
**Companion Documents**: OS-DRONE_Technical_Architecture.md,
                        OpenPIV_Technical_Architecture.md,
                        Provincial_PIV_Infrastructure_Integration.md
