# DC-TAXONOMY-009: 802.1X as the Unified Access-Authentication Transport
### Extends/refines DC-TAXONOMY-008's dual-radio roaming architecture with a third leg (wired) and clarifies the authentication/roaming relationship

---

## 1. Where 802.1X sits in the stack

Everything discussed through 008 covered *roaming* (how a device stays connected as it moves) and *radio access* (which spectrum carries the signal). 802.1X answers a different, earlier question: **before any of that, how does a device get let onto the network in the first place?**

802.1X is port-based Network Access Control (NAC) — the EAP (Extensible Authentication Protocol) exchange run once, at first association, before a device gets any real network access. It is not WiFi-specific: it gates WiFi association, wired ethernet ports, and (in concept) any access-controlled port. It's the *authentication transport*; `dc-identity` is the *authentication authority* underneath it. This is the piece that was implicit across DC-TAXONOMY-004's campus section and DC-TAXONOMY-008's roaming design but never named directly — it's the mechanism, not a new layer.

## 2. The three legs, unified under one DID

| Access type | Protocol doing the gating | What it checks | Ties to |
|---|---|---|---|
| **WiFi** | 802.1X / EAP-TLS at first association | Device presents a certificate/credential; FreeRADIUS terminates the EAP session | `dc-identity` `vc-verifier` — the certificate check IS a VC check, not a separate CA |
| **Wired ethernet** | 802.1X at the switch port | Identical protocol, same RADIUS backend, same `dc-identity` check | Any gateway node, campus switch, or SHI node ethernet jack should run this — a rogue device plugged into a wall jack gets the same DID-gate a WiFi client does |
| **Cellular (MulteFire)** | eSIM/AKA authentication, run by the EPC/HSS-equivalent | The eSIM profile issued by `dc-identity`'s `esim-provisioner` (DC-TAXONOMY-008 §2) is the credential being checked | Functionally the same job as 802.1X, different protocol family, same underlying credential store |

**The unifying claim:** one DID-linked credential is checked three different ways depending on which physical medium a device is using — 802.1X/EAP-TLS on WiFi, 802.1X again on wired ports, eSIM/AKA on cellular — but it's never three separate identity systems. This is the same "one DID, multiple radio expressions" principle DC-TAXONOMY-008 §3 established for MulteFire+WiFi roaming; this doc adds the wired leg explicitly and names 802.1X as the shared mechanism doing the work on two of the three legs.

## 3. How 802.1X relates to roaming (802.11k/r/v) — not competing, layered

This is worth being precise about since it's easy to conflate: 802.1X and 802.11r are not alternatives, they operate at different moments.

```
Device associates with AP #1 (first time)
   → Full 802.1X / EAP-TLS exchange runs
   → FreeRADIUS calls dc-identity vc-verifier
   → Takes ~1-2+ seconds (cryptographically expensive, thorough)
   → Result: a Pairwise Master Key (PMK) is established and CACHED
              across every AP in the same mobility domain

Device roams to AP #2, #3, ... (same session, moving)
   → 802.11k tells the device which nearby APs exist
   → 802.11v can nudge the device toward a better AP
   → 802.11r reuses the CACHED PMK from the original 802.1X exchange
   → Only an abbreviated 4-way handshake runs — <50ms
   → Full 802.1X is NOT re-run
```

So: **802.1X is the expensive, thorough check done once per session; 802.11r/k/v exist specifically to make repeating that check unnecessary as the device physically moves.** A network design that tries to run full 802.1X on every roam defeats the entire purpose of 802.11r — this is a common real-world misconfiguration worth flagging explicitly in whatever campus deployment spec eventually gets written, since fast roaming silently fails back to slow full re-authentication if the PMK caching isn't configured correctly.

## 4. Revision to DC-TAXONOMY-008's proposed spec name

DC-TAXONOMY-008 §7 named the roaming-unification gap `DC-DUAL-RADIO-ROAMING-001`. Given this addition, that's better renamed and widened:

**`DC-UNIFIED-ACCESS-001`** — covers all three legs (WiFi 802.1X/802.11k/r/v, wired 802.1X, cellular eSIM/AKA) authenticating against one `dc-identity` layer, with the roaming mechanics (008 §3) as a sub-section rather than the whole spec. This is a cleaner name for what's actually being specified: unified network access control, of which fast roaming is one consequence, not the whole point.

## 5. Practical implication for the SHI node / campus hardware spec

Every access point, cellular small cell, and managed switch port in a D-Central deployment should run the identical RADIUS/`dc-identity` chain rather than each network layer inventing its own auth flow:

```
Device (any medium) → 802.1X (wifi/wired) or eSIM-AKA (cellular)
                    → FreeRADIUS (or EPC/HSS-equivalent)
                    → dc-identity: vc-verifier
                    → Pass/fail + entitlement (VLAN, PLMN slice,
                       service access) assigned dynamically per-DID,
                       same mechanism DC-TAXONOMY-004 §2.10 already
                       described for campus WiFi, now explicitly
                       generalized to every access medium
```

No new primitive is required to implement this — it's a naming and consolidation fix, folding wired 802.1X into the same design the WiFi and cellular legs already had, and correcting the earlier spec name to reflect that all three were always meant to be one system.

---

## 6. Updated gap registry addition

42. **DC-UNIFIED-ACCESS-001** (supersedes/renames `DC-DUAL-RADIO-ROAMING-001` from 008 §7) — the full three-leg spec: 802.1X for WiFi and wired access, eSIM/AKA for cellular, all terminating at `dc-identity`'s `vc-verifier`; includes the PMK-caching/802.11r interaction as an explicit configuration note to prevent the common fast-roaming misconfiguration described in §3

---

*DC-TAXONOMY-009 — extends/refines DC-TAXONOMY-008. Names 802.1X as the shared authentication transport underneath both the WiFi and wired access legs (cellular uses eSIM/AKA doing the equivalent job), all three terminating at dc-identity's vc-verifier as the single authority. Clarifies that 802.1X and 802.11r are sequential, not competing — full 802.1X runs once per session, 802.11r/k/v exist to cache and reuse that result during roaming. Renames the prior DC-DUAL-RADIO-ROAMING-001 gap to DC-UNIFIED-ACCESS-001 to reflect the third (wired) leg.*
