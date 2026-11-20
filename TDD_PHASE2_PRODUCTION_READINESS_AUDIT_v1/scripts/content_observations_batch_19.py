#!/usr/bin/env python3
from inspection_ledger import add
R = [('1nNFdXOcJYpojq1PYmRsOuZTn5wBRBIq8',
  'Adanna FRONT V003 whole board: full-height long indigo wrap/bandeau, sandals, high braided knot, left-temple '
  'beads/scar/upper-arm coil and diagonal baldric; small pendant/cord; no weapon. Sidebar seven corrections and no automatic '
  'approval.',
  'Superseded front to V004/V005 limited-study lineage, not a production pass. No body scale/topology from printed alignment. '
  'Preserve current V003 side/back and exact later cord-only scope; CQ9/RQ10-1/U11 remain.'),
 ('1nYt7Tvoyn7Q5179ITrgJhCjY5gb4MmyY',
  'Adanna THREE_QUARTER V003: full figure, long indigo wrap and sandals, near/far shoulder silhouette and small pendant, correct '
  'printed left identifiers and plate4, no blade. Complete source/chrome read.',
  'Superseded by V004/V005 history; labels not technical approval. No near-side mirroring or new anatomy/costume changes. '
  'Cord/upper-arm prior corrections and selected internal tier remain exact, no re-review of settled endpoints.'),
 ('1SLxYu-Fez5qGeo1gpZbILWXy_Y_9WHco',
  'CH01ST01 Dawn V001: elevated empty square among circular huts/compound walls, large tiered palace gate at rear, blue '
  'bands/panels and small finials/markers, cool mist/orange horizon, no people.',
  'REPLACED / SUPERSEDED — superseded creative evidence only, no independent release. Do NOT transfer the later version’s '
  'limited use to this exact ID. B03 / 1Rxo6My76m13XUAEVS00M3-bVzMVIxQgb (CH01-SET-001-ST01_V002.jpg) alone has its own recorded '
  'tier: RETAIN AS REFERENCE / REVIEW AID; Lighting/weather reference only; not a locked settlement kit or historical '
  'architecture.'),
 ('1xSJ6QJBwA2eQsatcYgM_hHBrhEAvz_5d',
  'CH01ST02 Midday V001: high wide view of round huts around open square, palace/gateway rear, regular fields/forest horizon, '
  'central narrow marker-like objects and carved/blue gate motifs. Overcast-to-day naturalistic light.',
  'REPLACED / SUPERSEDED — superseded creative evidence only, no independent release. Do NOT transfer the later version’s '
  'limited use to this exact ID. B05 / 1hldnXwv2_grB2Q6YWvQFRPdcIs3dR_h3 (CH01-SET-001-ST02_V002.jpg) alone has its own recorded '
  'tier: APPROVED WITH DEFINED CONDITIONS; Internal fictional midday layout/composition study; not approved settlement design.'),
 ('1YJqo7pZRuq1hOHpfsiBp9Amiv8SHGJQp',
  'CH01ST03 Dusk V001: orange sunset/cool-shadow empty settlement square, round huts/earth compounds and new rear-palace '
  'silhouette, blue gate bands/pointed posts and farm stakes.',
  'REPLACED / SUPERSEDED — superseded creative evidence only, no independent release. Do NOT transfer the later version’s '
  'limited use to this exact ID. B07 / 1j03tjjtHXt6s5iHJfgJS3M_j17aNmiMg (CH01-SET-001-ST03_V002.jpg) alone has its own recorded '
  'tier: RETAIN AS REFERENCE / REVIEW AID; Lighting/weather reference only; not a locked settlement kit or historical '
  'architecture.'),
 ('1r5SIMNFxa1CRTgFnA-4yugnvykBBch4F',
  'CH01ST04 Night V001: dark blue starry settlement, tall multi-tier central tower/gate versus surrounding round huts, warm door '
  'pinpoints, fences/fields and empty square.',
  'Distinct history, not continuous-state geometry or production authority. Do not invent sacred meaning from tower/markers or '
  'accept all source architecture solely to make a night render.'),
 ('1YF2yq80Bxzz9wGOn7C4GzkzaFgApJqe-',
  'CH01ST04 Night V002: different simpler rear-house/compound plan, dense trees/fields, moon above, round huts and open square '
  'with a central low stone-like ring. Dark blue scene.',
  'Distinct generation from V001/V003, not surveyed common scene. Ring function remains unknown; neither sacred/hearth/ritual '
  'identity is established by appearance. No unrequested niche/speck/branch removals.'),
 ('1IhgfuIFZ5wOj4Wb0KpTrYQcyj57nT9Pz',
  'CH01ST04 Night V003 entire raster: moonlit plan related to V002, centre square now open without ring, round thatch huts/blue '
  'doorway cloths and forest/fields; some junction/lighting softness.',
  'REPLACED / SUPERSEDED — superseded creative evidence only, no independent release. Do NOT transfer the later version’s '
  'limited use to this exact ID. B11 / 1npYn0kJB2FFjTxPyGdACAsCqKk8ZbDPq (CH01-SET-001-ST04_V004.jpg) alone has its own recorded '
  'tier: APPROVED WITH DEFINED CONDITIONS; Night concept review at delivered concept scale only. This V003 is actually1264x843; '
  'accepted B11 is a DIFFERENT V0041536x1024, not this payload. No resize, ring/niche/speck/branch removal or source change is '
  'authorized.'),
 ('1KyoNo4wBHp6GG_2Ad2MdYew-cKLYHpaz',
  'CH01ST05 Rain V001: wet reflective empty square under heavy slant rain and sky shafts, round huts/earth walls, dramatically '
  'different central palace/gateway, blue strips and finite fields/forest.',
  'REPLACED / SUPERSEDED — superseded creative evidence only, no independent release. Do NOT transfer the later version’s '
  'limited use to this exact ID. B13 / 1X-eO-Svbzo46ozPXbsE-JpT4SEfWMgOw (CH01-SET-001-ST05_V002.jpg) alone has its own recorded '
  'tier: RETAIN AS REFERENCE / REVIEW AID; Lighting/weather reference only; not a locked settlement kit or historical '
  'architecture.'),
 ('1cKZa4flUbjidGKo5dHZECfJF9hf75RdW',
  'CH01ST06 V001: dense contemporary-looking market with collared shirts/plain tops/patterned wraps, produce/cloth/metal wares, '
  'fabric/tarpaulin stalls and corrugated-looking roofs beneath large tree.',
  'REPLACED / SUPERSEDED — superseded creative evidence only, no independent release. Do NOT transfer the later version’s '
  'limited use to this exact ID. B15 / 1TBXHgJlUmmbMWcMhG9PQn0eS07bdbum9 (CH01-SET-001-ST06_V002.jpg) alone has its own recorded '
  'tier: APPROVED WITH DEFINED CONDITIONS; Internal contemporary-context fictional market study only; not ethnography, ritual '
  'evidence or cross-asset NPC costume authority.'),
 ('1sixVQ4I9wsgJbEOSfssCVsXRcrIG3x7R',
  'CH01ST07 V001: contemporary-looking ordinary assembly seated on plain benches/stools beneath tree, collared '
  'shirts/tops/wrappers and metal-roof-looking houses; small background onlookers.',
  'REPLACED / SUPERSEDED — superseded creative evidence only, no independent release. Do NOT transfer the later version’s '
  'limited use to this exact ID. B17 / 1_Lw07vpd0aOo0XnI7-xrbWZTWhypg7vU (CH01-SET-001-ST07_V002.jpg) alone has its own recorded '
  'tier: APPROVED WITH DEFINED CONDITIONS; Internal contemporary-context fictional ordinary assembly study only; not '
  'ethnography, ritual evidence or cross-asset NPC costume authority.'),
 ('18RHdPeQM-WUSA9N0dvliTi4WWqsfcFVX',
  'CH03 Forgotten Kitchen V001: masonry-like stove/arched fireboxes with cold wood, pots/herb bundles, mill-like round stones, '
  'bright broken wall, plank counter and doorway to another room.',
  'Superseded/rejected version, not current three-stone/earth-room authority or real milling/forging process. No new '
  'event/ruin/weather claim from debris. Current selected E46V003 firewood study remains limited and accepted, not failed.'),
 ('16yJsFYZRa3iE1VAtAqhBTAI3JLuUdCmT',
  'CH03 Forgotten Kitchen V002: grey earth room/cold pot on three stones with ash, dry bundles hung from beam, '
  'mortar/pestle/bowl right, light openleftdoor and dark internal door. No clear discrete stacked woodpile at authorized '
  'back-left patch area.',
  'Original retained and bounded E46V003 selected firewood addition already completed. This read is not a new patch/relight '
  'order; cold remains cold, no source/frame changes. Native scene/geometry not present in still.'),
 ('1xxQFlOkqg045hnmWm-wJY428u0xSV3-K',
  'Sleeping Room V001: warm directional sun from large shuttered/barred-looking window, simple timber '
  'sleepingplatform/wovenmat/foldedpaddedcloth, side table with handled jar/bowl, pale plaster and niche.',
  'Superseded/rejected submitted chapter use; not glass proof, country identification or final design. Accepted V002 grey '
  'doorway-framed visual endpoint remains unaffected; no new re-review or repair order.'),
 ('10Apn34FkRedH1E5NXGCa9KSZ1Dh42SJK',
  'Residential Courtyard V001: warm sunlit brick/plaster enclosure, central tree in raised rectangular brick bed, blue cloth '
  'line, jar, plank/louvre doorway and metal-tap-looking basin fixture right.',
  'Superseded/rejected chapter proposal; no actual material or plumbing engineering inferred. Not authority for ash-grey current '
  'environment or E48 clay-toy decision. No foreign location/authenticity claim from visual style.'),
 ('1RcEkIjAlMqO6cvKhwALy9gveVL07gOCK',
  'Back Plots V001: overgrown masonry allotment-like yards/sheds with blue/pink cloth on line, broken walls and overturned large '
  'pot; row of pitched-roof/chimney houses across horizon, green crops instead of grey ash plots.',
  'Superseded/rejected chapter use, not specific foreign geography identification or approved urban kit. Accepted V002 visual '
  'correction and dead-plot direction retained. No automatic plant-species or weather simulation claim.'),
 ('1DtT7wfMJt63S_oGN-cIKuzR__7oDAqRG',
  'Narrow Passages V001: warm amber narrow masonry alley with arched niches/grilles, overhead sagging cloth, '
  'paved/stepped-looking ground and bright distance.',
  'Superseded/rejected, not grey ash/earth current authority. No generic ban on materials derived here; current V003 internal '
  'footprint endpoint/handworked-wall artistic read remains selected, no actual concrete claim or automatic redesign.'),
 ('1Slo9WE8ezx6yDe-zS-moGTItO-f1dQ_t',
  'Failed E53 Canoe Shed V003 entire raster re-read: original three dugout hulls/unfinished adze/chips/post/thatch setup '
  'remains, desaturated/softened grade but directional highlights/shadows still evident.',
  'FAILED relight / NOT a replacement. Correctly distinct from accepted E46 Kitchen local firewood correction. Preserve failed '
  'attempt and original; native nondestructive lighting proof required after separate film/design authorization, no full-frame '
  'generation.'),
 ('1lrjAnGZRQ7srJxZMTg7Gs7wxZUlDEm_H',
  'Failed E54 Landing V003 entire raster re-read: two houses/canoes/earth landing/cold hanging-fish rack preserved, lowered '
  'warmth/contrast yet directional sunny impression persists.',
  'FAILED relight / NOT replacement. Side-set freestanding rack is accepted fictional cold/unlit staging intent, not process '
  'authentication. No fire/smoke/count/house changes. Native lighting rather than repeated full-frame generative restaging after '
  'authorization.')]
for i,o,l in R:add(i,'visual','entire actual raster',o,l)
