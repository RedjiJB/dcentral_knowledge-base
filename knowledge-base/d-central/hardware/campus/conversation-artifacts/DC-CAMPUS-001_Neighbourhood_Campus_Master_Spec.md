---
source_conversation_uuid: 702c2d45-c80d-429a-a545-2850a38a6543
conversation_title: 'Mobile SOC center setup options'
created_at: 2026-07-22T11:23:34.845895Z
doc_id: DC-CAMPUS-001
description: 'DC-CAMPUS-001: consolidated campus master spec pulling together existing campus work plus build requirements, population threshold, and civil planning'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
---

# DC-CAMPUS-001 — D-Central Neighbourhood Campus Master Specification

## Consolidated Standard · Revision 1.0 · What It Is, What It Takes, and How It's Planned

| Field | Value |
|---|---|
| **Document ID** | DC-CAMPUS-001 |
| **Revision** | 1.0 (consolidates prior campus design work into one canonical spec) |
| **Author** | Toussaint — D-Central Group Inc. |
| **Status** | Design — far-horizon execution (Phase 5, ~2036–2038); micro-campus prototype Phase 4 |
| **Consolidates** | The DEPLOY-CAMPUS series (001–014), the Civic Spine spec, the DCLT/DHC/DECU financing architecture, DCOT transit, and the district production-ecosystem model, all from prior D-Central sessions |
| **Related** | DC-SHI-SPEC-001/002 (Tier 5 anchor), DC-VENTURE-001 (Phase 4–5), DC-FRACTAL-001 (cluster/regional hub), DC-TPL-HOME, DC-DEV-001, DC-OS-001/002, DC-LKB-001…003, DC-MOGUL-001, DC-SENSE-SERVICE-001, DC-IMPACT-001 |

---

## 1. What the campus is

The D-Central Neighbourhood Campus is not a collection of buildings; it is a **planned neighbourhood of SHI-equipped homes organized into functional districts**, all interconnected through one D-Central mesh — same network, same energy grid, same sensing mesh, same home OS, same learning platform. It is the concentrated (hub) topology of the same architecture the household nodes deploy in distributed (spoke) form. Its reference models are not student residences but Oxford, Marinaleda, and the kibbutz — communities where people arrive as students and age into homeowners, parents, and community anchors within one integrated social and economic structure.

In the fractal (DC-FRACTAL-001), the campus is the **cluster/regional anchor**: the physical commons the surrounding distributed household nodes orbit. It is the SHI Tier 5 site — the only deployment class running maximum compute, full spatial sensing (Levels 4–5), and mesh coordination for everything downstream.

## 2. Physical structure — the districts

The campus is composed of eight functional districts plus a Civic Spine, with a residential integration perimeter.

**The eight districts** (each 8–15 SHI-equipped homes, each home specialized for its district function while keeping full residential capability):

- **District A — Technology, Security & Networking.** The operational heart; runs the infrastructure everything else depends on. Homes carry Tier 4–5 SHI plus extra rack space, specialized networking, and lab VLANs. Writes the navigation software for campus vehicles.
- **District B — Health & Wellness.** Clinical-grade environmental monitoring, accessible design, medical equipment storage. Hosts the regulated clinical facilities the distributed home model can't.
- **District C — Trades & Engineering.** Mechanical fabrication, welding, chassis building, construction, with apprenticeship integration. Fabricates what District A designs.
- **District D — Business, Finance & Law.** The professional-service cells (accounting, HR, ops, legal) and vault administration.
- **District E — Arts, Design & Media / Studios.** Studio-grade lighting, acoustic treatment, expanded GPU for rendering and generative AI. Styles what District C builds.
- **District F — Research, Science & Innovation.** With lab classification tiers.
- **District G — Community Services & Commons.**
- **District H — Agriculture & Food Production.** With aquaponics; supplies the dining commons and hospitality cells.

**The Civic Spine** is the physical and digital backbone — a shared corridor of mixed-use structures housing what serves all districts: the Tier 5 Academy/compute node (maximum compute), the community health clinic, the cooperative dining commons, the shared fabrication lab, the community governance hall, and the D-Central NOC. It is the campus's quad and administration building and a working service environment at once.

**Interdependence by design:** District C fabricates what District A designs; District E styles what District C builds; District H feeds the commons. The campus is a production ecosystem, not a layout.

## 3. What the campus can handle from the ecosystem

Per the specs, the campus handles precisely what the distributed household nodes structurally cannot:

**Heavy compute & hosting (DC-DEV-001):** the campus server is a first-class mesh "region" hosting cell apps, classIQ classroom/cell deployments, NOC/monitoring services, vault infrastructure, and the cluster's mesh-hosted sites. Households run light; the campus carries the load.

**Top-tier sensing (DC-SHI/DC-SENSE-SERVICE-001):** the only site running T4/T5 and spatial Levels 4–5 (LiDAR point clouds, splatting) — the residential ceiling is T3/Level 3.

**Regulated facilities (DC-LIC-001 Regulated Entity Pattern):** the licensed commercial kitchen the home micro-kitchen graduates to, the clinic where telehealth's hands-on half happens, the AGCO-licensed venue, the in-person classrooms, the licensed-trade staging yard, the gym/athletic complex. Each keeps its named accountable licensed human; the DAO allocates space and capital, never regulated operations.

**Cluster governance & vault hub (DC-FRACTAL-001 Layers 1–2):** the shared NOC, shared professional back-office cells, cluster vault, and governance assemblies physically sit here — the lakou's shared yard.

**Training engine made physical (classIQ / DC-FLUENT / DC-MOGUL-001):** in-person cohorts, apprenticeships, the judgment-work pool coordination, and the venture studio where new stewards launch cells.

**Community resilience (DC-MSOC-001 / energy specs):** campus-scale solar/battery/generator, Starlink/mast fallback connectivity, and the mobile SOC trailer's home base — the community's backstop when a household node or the grid fails.

**Support infrastructure (DEPLOY-CAMPUS 011–014):** family housing district (Stage 4 CLT homes), athletic complex (gym, pool, courts, arena), a bond-financed multi-use stadium, and the D-Central Sports Network broadcast infrastructure.

**Campus transit (DCOT):** the D-Pod (2-passenger autonomous electric pod, ~$4,500–7,000/unit vs. $45–80K commercial, 8 km/h cap, Isaac ROS 2 over WiFi 6 mesh) and the D-Bus (20-passenger modular electric, configurable passenger/cargo/medical/school variants). Vehicles operating entirely on private campus paths fall under the golf-cart regulatory category — no public-road certification required — and the campus fleet is the test environment for the commercial D-Central Ride product.

**What it cannot be** (three refused departments, at every scale): not a surveillance hub, not an enforcement/military base, not a private force beyond the PSISA-licensed protection service. The campus hosts protection, not enforcement.

## 4. What it takes to build — the honest requirements

**4.1 Land.** A campus of eight districts at 8–15 homes each plus Civic Spine, support infrastructure, agriculture, and transit paths implies roughly **100–150 dwelling units** on a walkable footprint. In an Ontario neighbourhood-density context that is on the order of **15–40 acres** for a compact, mixed-use, walkable plan (denser than suburban tract, deliberately). The Haiti-corridor campuses in prior planning were sketched far larger (4–8 km²) because they bundled regional service areas; the Ottawa reference campus is a walkable neighbourhood, not a territory.

**4.2 Capital.** Prior financing architecture modelled a **$50M infrastructure bond** at the strategic-investor layer plus a CMHC MLI Select mortgage (4.5%, 50-year, up to 95% loan-to-cost) funding construction — implying a total build in the low-to-mid **hundreds of millions** for the full campus. This is a real-estate development at institutional scale, not a venture expense. It is Phase 5 precisely because it requires the property equity, vault cycles, and track record of Phases 0–4 to underwrite.

**4.3 The financing loop (DCLT + DHC + DECU + bond/REIT).** The model closes a loop rather than relying on any single source: strategic investors (a **Campus Infrastructure Bond ~6.25%**, a **Campus REIT**, FinDev Canada for the international corridor) own the physical infrastructure and take first-priority waterfall payment; a **CMHC MLI Select** mortgage funds construction at low debt service; the **D-Central Housing Cooperative** holds the master lease and keeps housing charges low (~$700/month modelled); residents work through the **Work Cooperative** (gig platform, patronage returns); income services **Education Credit Union** loans (~3% cooperative student loans); repaid loans become credit-union investment shares that fund the next cohort. Land is held permanently by a **Community Land Trust** (partnering with the existing Ottawa Community Land Trust rather than founding a competitor) on 99-year ground leases — taking land off the speculative market permanently.

**4.4 The ownership spectrum (five stages).** Residents are not locked into one tenure: arrive as a **renter/student**, become a **cooperative member** (first equity from membership, not a down payment), transition to **LEHC member** (accumulating share equity), then **CLT equity homeowner** (buy the improvements ~$269K on a modelled ~$300K improvements value, DCLT retains land, DECU issues the ground-lease mortgage), through to long-term **community anchor**. Appreciation on resale is shared between homeowner and the trust — the anti-speculation mechanism. This is what makes the campus a permanent community rather than a housing complex.

**4.5 Time.** ~10+ years out (Phase 5, ~2036–2038), gated behind: incorporation, first revenue, the property holdco (DC-TPL-PROP), and — critically — the **micro-campus prototype**.

## 5. How many people around it to make it worth it

Two thresholds matter: the **internal** population that makes the campus self-sustaining, and the **surrounding** catchment that makes it viable.

**Internal (residents):** at 100–150 units and ~2.5 persons/unit, the campus houses roughly **250–400 residents**. Prior planning sized district capacity comparably (diaspora + local trainee cohorts in the hundreds). This is the population that operates the districts, staffs the cells, and fills the in-person cohorts. Below ~250 the district production-ecosystem (A designs, C builds, E styles, H feeds) loses the specialization that justifies it; the micro-campus (§6) is the sub-threshold prototype that deliberately doesn't attempt full district specialization.

**Surrounding catchment (the spokes the hub serves):** the campus is a cluster anchor for distributed household nodes, so its viability scales with the member households in its service radius. Cooperative and community-facility economics generally need a **few thousand people** in walkable/short-drive catchment to sustain shared commercial facilities (the venue, clinic, gym, commercial kitchen, market). A reasonable planning threshold: the campus becomes "worth it" when the surrounding cluster reaches on the order of **500–1,000 member households (~1,500–3,000 people)** actively transacting through ecosystem rails — enough to fill the regulated facilities the campus uniquely provides and to justify the shared professional cells. Below that, the distributed model alone (home nodes + cluster shared services without a physical campus) is the correct, cheaper topology.

The sequencing implication: **you do not build the campus to create the community; you build it once the distributed community exists and has outgrown purely virtual shared services.** The campus is demand-pulled by a proven cluster, never supply-pushed.

## 6. The arrangement & civil planning

**6.1 Planning philosophy — walkable, mixed-use, production-integrated.** The campus is planned as a compact walkable neighbourhood, not a zoned-separation suburb. Districts are mixed-use (homes that are also workplaces and learning sites), organized around the Civic Spine as the central shared corridor, with the residential integration perimeter blending the campus into the surrounding neighbourhood rather than walling it off. Transit is internal, low-speed, autonomous-capable, on private paths (the golf-cart regulatory category). Energy, water (aquaponics, rainwater), and food (District H) are partially closed-loop.

**6.2 Zoning & entitlement (the real civil-planning gate).** This is the hardest non-capital constraint. A mixed-use, live-work, higher-density cooperative neighbourhood requires municipal zoning that permits it — in Ottawa's context, this means engaging the city's planning process, likely a community-planning-permit or zoning-bylaw-amendment path, and aligning with intensification and missing-middle policy. The CLT partnership (Ottawa Community Land Trust) matters here beyond finance: it brings established municipal relationships and legal precedent. Live-work and home-based-enterprise permissions (which the whole household-venture model depends on) must be secured at the zoning layer, not assumed.

**6.3 Building standards.** Stage-4 CLT homes are specified in cross-laminated timber (CLT) — the material pun is deliberate and real: mass timber for the sustainability, speed, and carbon profile. SHI infrastructure is built into each home (the ~$420K modelled replacement cost includes construction + SHI stack). District-specialized homes add their fitout (rack space, clinical monitoring, studio treatment) per the DEPLOY-CAMPUS district fitout specs (002–009).

**6.4 Phasing — micro-campus first.** The full campus is not the first build. Per DC-VENTURE-001 Phase 4, the prototype is a **single rehabilitated mixed-use block**: ground-floor gym/venue/commercial, upper-floor offices and a few residential units, SHI nodes throughout, the converged SOC in the basement. This micro-campus proves the arrangement, the live-work zoning, the shared-facility economics, and the financing loop at a scale of one building and a handful of households — de-risking the ~$100M+ full campus. The full eight-district campus is assembled only after the micro-campus validates the model and the surrounding cluster reaches the §5 threshold.

**6.5 Civic & governance layout.** The governance hall in the Civic Spine hosts the cluster and regional DAO assemblies (DC-FRACTAL-001). The NOC and Tier 5 node anchor the mesh. The market and dining commons are the daily-life gravity centre — the lakou yard — deliberately placed central so the community's social life has a physical heart, not just a network.

## 7. Honest status

Every figure here is a planning estimate from design sessions, not a costed development pro forma — the land, capital, and population thresholds need a real feasibility study before any of them is load-bearing. The campus is the ecosystem's most capital-intensive, most regulation-dependent, and most far-horizon element, and it is the one most likely to be over-designed relative to execution (the DC-STATUS-001 pattern at its largest scale). The disciplined path is unchanged: incorporation → revenue → property holdco → micro-campus prototype → (only if the cluster threshold is met) full campus. The community must exist and pull the campus into being; the campus cannot be built to summon a community that isn't there yet.
