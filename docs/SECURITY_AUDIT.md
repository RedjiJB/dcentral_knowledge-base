# Security Review — dcentral-fieldops

**Method**: direct code review of the cloned repository (identity, auth, MCP, REST façade, SQL layer, secrets handling) plus an independent `npm audit` run. This is not a penetration test and did not include the live production deployment — it covers what's verifiable from source.

The codebase's own `docs/ARCHITECTURE.md` already discloses several gaps candidly (unencrypted private keys, no key rotation, unreviewed sovereignty policy). Those are restated below with severity added, not re-discovered — the point of this review is the things *not* already self-reported, plus independent confirmation of the things that are.

---

## Summary

| # | Finding | Severity | Status |
|---|---|---|---|
| 1 | Webhook target URL has no validation — SSRF risk | **Medium** (High if ever exposed beyond platform admins) | New — not previously flagged |
| 2 | Third-party LLM API keys stored in plaintext in Postgres | **Medium** | New — not previously flagged |
| 3 | Webhook secrets stored in plaintext (by design) | **Low–Medium** | Previously disclosed in code comments, not in ARCHITECTURE.md gaps list |
| 4 | Private key material (`keys.private_jwk`) stored unencrypted at rest | **Medium** | Previously disclosed |
| 5 | No key rotation implemented | **Low** (compounds #4) | Previously disclosed |
| 6 | Sovereignty-tier policy never formally reviewed | **Low** (process gap) | Previously disclosed |
| 7 | No general-purpose rate limiting beyond login | **Low** | New — not previously flagged |
| 8 | No CORS policy defined | **Informational** | New — not previously flagged, not currently exploitable |
| — | Dependency vulnerabilities | **None found** | `npm audit`: 0 vulnerabilities, independently confirmed |

---

## Detailed findings

### 1. SSRF via webhook target registration — Medium (High if scope expands)

`src/domain/webhookTargets.ts`'s `registerWebhookTarget` accepts an arbitrary `url` with no validation whatsoever — no scheme allow-list, no check against private/internal IP ranges. `dispatchToWebhooks` then performs a server-side `fetch(target.url, ...)` against whatever was stored.

This is a textbook Server-Side Request Forgery pattern: a URL like `http://169.254.169.254/latest/meta-data/` (the cloud instance metadata endpoint) or an internal-network address would be fetched directly by the server, from inside your infrastructure's trust boundary.

**Why it's Medium today, not High**: `src/facade/routes/webhookTargets.ts` correctly gates this behind `requireAdminRole` — only a tier-4 admin can register a target. The blast radius today is limited to "a compromised or malicious admin account can pivot into internal infrastructure," which is real but requires an already-serious prior compromise.

**Why this becomes High under the platform/multi-tenant design discussed**: if webhook registration is ever exposed to *tenant* admins (a very natural feature for a platform — "notify our Slack when a job completes" is exactly the kind of thing tenant admins will ask for), this becomes a tenant-to-platform SSRF vector: a malicious or compromised tenant account could probe the platform's internal network or cloud metadata service, potentially extracting credentials for the platform's own cloud infrastructure. This needs fixing *before* webhook configuration is ever extended to tenant-level access.

**Recommended fix**: validate the URL at registration time — resolve the hostname, reject if it resolves to a private/loopback/link-local range (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.0/8`, `169.254.0.0/16`), reject non-`https` schemes, and re-validate at dispatch time too (DNS can change between registration and use — "TOCTOU" for SSRF filters is a known bypass pattern).

### 2. LLM API keys stored in plaintext — Medium

`src/domain/llmSettings.ts` stores `deepseek_api_key`, `anthropic_api_key`, and `openai_api_key` as plain text columns in Postgres, settable from the dashboard's Settings page. No encryption at rest.

A database compromise (or a misconfigured backup, or an overly-broad `SELECT *` bug in a future feature) would directly leak live API keys for three external providers. These keys likely have real cost/quota attached — a leak isn't just a confidentiality issue, it's a potential billing/abuse issue on the provider side.

**Recommended fix**: same remediation family as the already-disclosed private-key gap (#4) — envelope encryption or an external KMS/secrets manager, decrypted only in-memory at the point of use. Worth fixing both together rather than sequentially, since they're the same underlying gap (no secrets-at-rest story) in two different tables.

### 3. Webhook secrets stored in plaintext — Low–Medium, but worth re-flagging

`src/db/migrations/0037_webhook_targets.sql` stores the webhook HMAC secret in cleartext, with a code comment explaining this is deliberate — the secret must be read back at dispatch time to sign outbound requests, and it's never returned to the frontend (only a `has_secret` boolean).

This is a defensible tradeoff as written, not a bug — but it's the same underlying pattern as #2 and the already-known #4: this system currently has **no secrets-at-rest story anywhere**. Three independent instances of "store the plaintext because we need to read it back later" is a pattern worth solving once, systemically (a KMS/envelope-encryption layer that decrypts on read), rather than accepting individually per table.

### 4–6. Previously disclosed gaps (confirmed, not re-discovered)

Restated here with severity for completeness, since a security document should be a complete picture, not just new findings:

- **Private key material unencrypted at rest** (`keys.private_jwk`) — Medium. Confirmed via `src/db/migrations/0005_keys.sql`. A database compromise yields signing keys for every DID in the system, not just credential-check bypass.
- **No key rotation** — Low on its own, but compounds #4: if a key is ever compromised, there's currently no mechanism to rotate it without broader manual intervention.
- **Sovereignty-tier policy never formally reviewed** (`policy/sovereignty_tiers.yaml`) — Low severity, but a process gap worth closing before it's forgotten under platform-scale time pressure.

### 7. No general-purpose rate limiting — Low

`src/domain/loginAttempts.ts` correctly implements account lockout on the login endpoint specifically (5 failed attempts / 15-minute sliding window, tracked by normalized email, generic error responses that don't leak account existence — this is genuinely well done). But no equivalent throttling exists on other façade endpoints. The system currently relies on Cloudflare in front of it for volumetric/IP-based protection, which is a reasonable division of responsibility for a single-tenant deployment, but worth re-examining once the platform has many tenants sharing the same origin — a single tenant's misbehaving integration or bug could affect shared infrastructure others depend on.

### 8. No CORS policy — Informational

No CORS headers are set anywhere in `src/facade/`. This is not currently a vulnerability — same-origin deployment (frontend and API behind the same reverse proxy) means the browser's default same-origin policy already provides protection, and Bearer-token auth (not cookies) means CSRF isn't a relevant risk class here either. Flagged only because the multi-tenant platform design (tenant subdomains, possible third-party integrations) will likely require an explicit, deliberately-scoped CORS policy where today there's implicitly none — worth designing intentionally rather than discovering the need mid-incident.

---

## What's genuinely solid (confirmed by direct review, not just repo claims)

Worth stating plainly, since a security document that only lists problems gives a distorted picture:

- **Password hashing**: `src/identity/passwords.ts` uses Node's native `scrypt` with a per-password random salt and `timingSafeEqual` for comparison — correct, standard, no home-rolled crypto mistakes.
- **Access tokens**: short-lived (15 min), Ed25519-signed, correctly reject expired/malformed/invalid-signature tokens (`src/identity/accessToken.ts`).
- **Authorization re-checked server-side on every request**: `src/facade/auth.ts` re-verifies a standing capability grant against Postgres on every call rather than trusting the JWT's own role claim — a capability revocation takes effect on the *next* request, not after token expiry. This is a materially stronger design than most JWT-based systems.
- **SQL injection**: every dynamic query reviewed (`purchaseOrders.ts`, `users.ts`, `crewMembers.ts`, `telemetry.ts`, and others) uses parameterized queries (`$1`, `$2`, ...) correctly — dynamic `WHERE` clause construction interpolates only static column names, never user-supplied values, into the query string itself. No injection vector found.
- **Path traversal**: `src/domain/documents.ts` deliberately generates random storage filenames rather than deriving them from user-supplied filenames — the comment explicitly notes this closes a path-traversal class of bug.
- **Capability tier comparison logic**: `src/identity/capabilities.ts`'s tier check (`grant.tier < minimumTier → denied`) is correct in both the argument-based and header-based credential paths (`src/mcp/middleware.ts`, `src/mcp/requestContext.ts`) — the HTTP-header fallback credential path still goes through full JWT signature verification, it's not a weaker trust path as might be assumed from the name.
- **Dependencies**: `npm audit` reports 0 vulnerabilities, independently confirmed by installing and auditing in a clean environment.

---

## Priority recommendations, in order

1. **Fix the webhook SSRF (#1) before any work that exposes webhook configuration to tenant-level users.** This is the one finding here that changes severity class (Medium → High) under the platform roadmap already discussed — fix it while it's still cheap, not after tenant self-serve ships.
2. **Design one secrets-at-rest solution and apply it to all three plaintext-secret locations (#2, #3, and the already-known #4) together.** These are one architectural gap, not three separate bugs — solving it once (envelope encryption or a KMS) is cheaper than three point fixes.
3. **Close the sovereignty-policy review (#6)** — cheap, already flagged, easy to keep deferring indefinitely under feature-work pressure.
4. **Revisit rate limiting and CORS (#7, #8) as part of the multi-tenancy work**, not as standalone fixes — both are naturally scoped by "what does tenant isolation require" once that design is finalized.


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

*No cross-references detected to/from other docs/*.md files.*

<!-- AUTO-GENERATED RELATED END -->
