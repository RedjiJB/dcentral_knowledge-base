# Running Neo4j on a Raspberry Pi, for this repo's graph layer

This is the setup guide for Stage 8's Neo4j track. It gets you a running Neo4j instance on a
Raspberry Pi and loads the artifacts `scripts/build_neo4j_load.py` generates in `registry/graph/`.
Not covered here: the Obsidian track (Track A), which needs no server at all — see
`scripts/build_obsidian_graph.py` and just point an Obsidian vault at this repo's root.

## 1. Hardware and OS baseline

- **Raspberry Pi 4 or 5, 4GB RAM minimum, 8GB recommended.** Neo4j's JVM heap and page cache both
  want headroom; 4GB works for this repo's small graph (472 Document nodes, ~1,400 edges total) but
  will feel tight once you're also running other services on the same Pi.
- **A 64-bit OS is required.** Neo4j 5.x ships no 32-bit ARM build. Use Raspberry Pi OS (64-bit) or
  Ubuntu Server 22.04+ (arm64).
- **SSD/USB3 storage strongly recommended over SD card** — Neo4j does a lot of small random I/O, and
  an SD card will bottleneck both the initial CSV load and later query performance.

## 2. Two ways to run it — pick one

### Option A: Docker (recommended — easiest to upgrade/reset)

```bash
sudo apt update && sudo apt install -y docker.io
sudo systemctl enable --now docker
sudo usermod -aG docker $USER   # log out/in after this, or use sudo below

mkdir -p ~/neo4j/data ~/neo4j/import ~/neo4j/logs

docker run -d \
  --name neo4j \
  --restart unless-stopped \
  -p 7474:7474 -p 7687:7687 \
  -v ~/neo4j/data:/data \
  -v ~/neo4j/import:/var/lib/neo4j/import \
  -v ~/neo4j/logs:/logs \
  -e NEO4J_AUTH=neo4j/changeme \
  neo4j:5-community
```

`arm64` images are published for the `neo4j` official image, so this works unmodified on a Pi. Set a
real password in place of `changeme` before exposing port 7474/7687 beyond localhost.

### Option B: Native install via apt

```bash
curl -fsSL https://debian.neo4j.com/neotechnology.gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/neo4j.gpg
echo "deb [signed-by=/usr/share/keyrings/neo4j.gpg] https://debian.neo4j.com stable 5" | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt update
sudo apt install -y neo4j

sudo systemctl enable --now neo4j
```

Config lives at `/etc/neo4j/neo4j.conf`; data at `/var/lib/neo4j/data`; the import directory Cypher's
`LOAD CSV` reads from is `/var/lib/neo4j/import` by default.

On first native install, set the initial password:
```bash
sudo neo4j-admin dbms set-initial-password 'changeme'
```

## 3. Point it at the outside world (optional)

If you want to reach the Neo4j Browser (port 7474) or Bolt (port 7687) from another machine on your
network, not just `localhost` on the Pi itself:

- Docker: already published via `-p 7474:7474 -p 7687:7687` above — reachable at `http://<pi-ip>:7474`.
- Native: edit `/etc/neo4j/neo4j.conf`, uncomment/set:
  ```
  server.default_listen_address=0.0.0.0
  ```
  then `sudo systemctl restart neo4j`.

Put this behind your router's firewall or a VPN (Tailscale/WireGuard) rather than port-forwarding it
directly to the internet — Neo4j's default auth is a single username/password, not defense-in-depth.

## 4. Load this repo's graph

1. Generate the artifacts (from your regular working machine, inside this repo):
   ```bash
   python3 scripts/build_manifest.py       # if not already run/current
   python3 scripts/build_neo4j_load.py
   ```
   This writes `registry/graph/*.csv` and `registry/graph/load.cypher`.

2. Copy the CSVs onto the Pi's import directory:
   ```bash
   # Docker setup from Option A:
   scp registry/graph/*.csv pi@<pi-ip>:~/neo4j/import/

   # Native install from Option B:
   scp registry/graph/*.csv pi@<pi-ip>:/tmp/
   ssh pi@<pi-ip> 'sudo cp /tmp/*.csv /var/lib/neo4j/import/'
   ```

3. Run the load script. Easiest via `cypher-shell`, available in both Docker and native installs:
   ```bash
   # Docker:
   docker exec -i neo4j cypher-shell -u neo4j -p changeme < registry/graph/load.cypher

   # Native (on the Pi):
   cat registry/graph/load.cypher | cypher-shell -u neo4j -p changeme
   ```

4. Verify:
   ```cypher
   MATCH (n) RETURN count(n);
   ```
   Should return the total node count `build_neo4j_load.py` printed when it ran (Document + Topic +
   ConsolidatedDoc + Project + Category counts summed).

## 5. Re-loading after the corpus changes

`load.cypher` uses plain `CREATE`, not `MERGE` — running it twice duplicates every node and edge. To
refresh after re-running Stage 6/7/8's scripts on updated source material:

```cypher
MATCH (n) DETACH DELETE n;
```
then re-run `load.cypher`. There's no incremental-update path in this version — the graph is treated
as fully regenerated from `materialized-manifest.json`, matching how `registry/graph/` itself is
regenerated wholesale rather than patched.

## 6. What you can query once it's loaded

See `registry/graph/README.md` for three worked example Cypher queries (cross-topic/project rollups,
"everything a consolidated doc absorbed," and supersession-chain tracing). This is the payoff
DC-PIPELINE-STD-001 describes for Stage 8: "show me everything that touches both X and Y" as an actual
query, not a manual cross-reference between `_topics.md` and front-matter fields.


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

*No cross-references detected to/from other docs/*.md files.*

<!-- AUTO-GENERATED RELATED END -->
