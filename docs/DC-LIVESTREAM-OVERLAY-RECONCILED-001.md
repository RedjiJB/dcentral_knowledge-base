# DC-LIVESTREAM-OVERLAY-RECONCILED-001 — D-Central Live Development Chatbot & Overlay System, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `livestream-overlay-chatbot-system` (3 docs).

## Current understanding

Three tightly-integrated source files for a Twitch livestream development-session overlay system:
`chatbot_integration_system.ts` (the Twitch chat bot), `overlay_websocket_server.ts` (the WebSocket
relay + metrics server), and `streaming_overlay_system.tsx` (the React overlay UI). All three share
the same architecture (bot → WebSocket server on port 3001 → React overlay), but a specific piece of
mock/hardcoded data is inconsistent with the chatbot's own defined business logic (see Unresolved
tensions).

**Chatbot (incorporated):** connects to Twitch chat via tmi.js, parses `!`-prefixed commands, and
integrates with GitHub (Octokit) for issue creation, PR-from-gist, deployment triggering via workflow
dispatch, and test running [Twitch client init, command handlers]. Fifteen named commands include
`!vote`, `!issue`, `!deploy`, `!test`, `!gist`, `!cred`, `!passport` (Gitcoin Passport score lookup),
`!poll`, `!ping-node` (Graph Node health check), and `!query` (GraphQL). A cred/reputation system awards
points per action (issue creation +25, deployment trigger +50, test run +15, code contribution via gist
+40, issue vote +5) and defines exactly five levels by total cred: Observer (0), Amplifier L1 (≥100),
Amplifier L2 (≥500), Chapter Steward (≥2000), Core Contributor (≥5000) [`calculateLevel()`]. Deployment
permission requires mod/subscriber/VIP status or Core Contributor level [`canDeploy()`]. Every command
execution and cred award is relayed to the overlay server via WebSocket (`ws://localhost:3001`).

**Overlay WebSocket server (incorporated):** an Express + `ws` server listening on port 3001, exposing
`/health`, `/metrics`, and three webhook endpoints (`/webhook/deployment`, `/webhook/github`,
`/webhook/twitch`) [setupExpress()]. Maintains a `StreamMetrics` object (live viewers, commits, lines of
code, test coverage, build/deployment status, contributor feed, chapter metrics, cred leaderboard,
4-chain cross-chain status for Ethereum/Polygon/Arbitrum/Base, chat-to-GitHub-issue tracking) updated on
staggered intervals (metrics every 30s, viewer count every 10s, cross-chain status every 15s)
[initializeMetrics, startMetricsUpdates]. Broadcasts updates to all connected WebSocket clients and
exposes public methods (`updateContributor`, `updateChatIssue`, `updateDeploymentProgress`) for the
chatbot to push events into the shared metrics state.

**React overlay UI (incorporated):** renders the on-stream visual overlay consuming (in this file, mock)
the same `StreamMetrics` shape the WebSocket server maintains — build-status indicator, deployment
progress bar, live-viewer count, a live contributor feed, a rotating panel cycling every 8 seconds
between cred leaderboard / chapter map / cross-chain status / chat-issues (`RotatingSection`), a stats
panel, and a scrolling bottom ticker [component structure]. The four cross-chain entries (Ethereum/
Polygon/Arbitrum/Base) and the chat-command reference list (`!vote`/`!issue`/`!deploy`/`!test`/`!cred`)
match the chatbot's and WebSocket server's real chain list and command set exactly.

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Twitch chat command set and GitHub integration | chatbot_integration_system.ts, command handlers | incorporated |
| Cred award amounts per action and 5-tier level thresholds | chatbot_integration_system.ts, `awardCred()`/`calculateLevel()` | incorporated |
| Deployment permission gating | chatbot_integration_system.ts, `canDeploy()` | incorporated |
| WebSocket server endpoints, metrics shape, update cadence | overlay_websocket_server.ts, setupExpress/initializeMetrics/startMetricsUpdates | incorporated |
| Cross-chain monitoring (4 chains) | overlay_websocket_server.ts, `updateCrossChainStatus()` | incorporated (chain list matches UI exactly) |
| React overlay UI structure and rotating panel | streaming_overlay_system.tsx, component structure | incorporated |
| Mock leaderboard/contributor data used for UI development | overlay_websocket_server.ts and streaming_overlay_system.tsx, mock data blocks | incorporated — inconsistent with the chatbot's own level formula, see tension below |

## Unresolved tensions

**Mock cred-leaderboard data in both the WebSocket server and the React overlay assigns a level label
that contradicts the chatbot's own `calculateLevel()` formula.** The chatbot defines Chapter Steward as
≥2,000 cred and Core Contributor as ≥5,000 cred. Both `overlay_websocket_server.ts`'s
`updateContributorStats()` mock data and `streaming_overlay_system.tsx`'s `mockData.credLeaderboard`
list `alice_dev` at 2,840 cred labeled **"Core Contributor"** — but 2,840 falls in the 2,000-4,999 range,
which the chatbot's own formula classifies as **"Chapter Steward,"** not Core Contributor. Attempted
reconciliation: this is very plausibly just stale or hand-authored placeholder/mock data in the two
UI-facing files that was never regenerated to match the chatbot's actual level formula (the mock data
predates or was written independently of the real `calculateLevel()` logic), rather than a deliberate
alternate leveling scheme — no source states a different level formula. Left as an open inconsistency
rather than silently corrected, since fixing it would mean guessing whether the intended fix is the mock
cred number or the mock level label.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/meta/platform-scaffolding/D-Central-Live-Development/chatbot-integration-system-ts.md`
- `knowledge-base/d-central/meta/platform-scaffolding/D-Central-Live-Development/overlay-websocket-server-ts.md`
- `knowledge-base/d-central/meta/platform-scaffolding/D-Central-Live-Development/streaming-overlay-system-tsx.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/meta/platform-scaffolding/D-Central-Live-Development/chatbot-integration-system-ts.md,
  knowledge-base/d-central/meta/platform-scaffolding/D-Central-Live-Development/overlay-websocket-server-ts.md,
  knowledge-base/d-central/meta/platform-scaffolding/D-Central-Live-Development/streaming-overlay-system-tsx.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.
