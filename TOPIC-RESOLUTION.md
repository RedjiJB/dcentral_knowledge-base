# Stage 5 Topic Clusters — Subject-Check Resolution

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
