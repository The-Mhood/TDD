# TDD — World Geography, Settlements & Population Atlas

**Document ID:** TDD-IMPL-WORLD-002 · **Version:** 1.0 · **Date:** 2026-11-21
**Companion to:** `WORLD_SCALE_AND_LIVING_WORLD_BLUEPRINT.md` (TDD-IMPL-WORLD-001)
**Owner:** PM (world-production), with Design (maps/layouts) and Research (evidence).
**Canon sources:** `docs/02_PRODUCTION/AGENT2/WORLD_ARCHITECTURE.md`, `WORLD_ASSESSMENT.md`, `SCENE_CAPTURE_W2M2.md`; `docs/06_IMPLEMENTATION/CHARACTER_IDENTITY_RECORDS.md`, `ST05_ST07_APPROVAL_RECORD.md`, Drive `LOCATION_MASTER_REGISTER.md` v2.9 / `SCENE_AND_MICROLOCATION_MASTER_REGISTER.md` v1.9.

> **Terminology (researched, Igbo — see source register):**
> - **Ala** — earth, land. **Ọmà** — the region's principal river. **Ọmà Ala** — the land of the Ọmà.
> - **Ama** — village; public meeting-square. **Obodo** — village-group / town. **Ogbe** — village. **Ehi/Ibe** — town. **Obi** — the head-of-house's hut/compound; the central house of a family compound. **Ezi** — family compound (cluster of huts around an open space). **Ilo** — a hut/dwelling unit within a compound.
> - **Ụmụnna** — sons/brotherhood of a common ancestor; a kindred. **Okpara** — the senior son/heir; head of a compound/kindred. **Ofo** — a title-holder; the council of elders' seat.
> - **Ahịa** — market. **Ubochi/Ubochi ahịa** — a day of the market week. **Eke / Orie / Afo / Nkwo** — the four market days.

---

## 1. The Ọmà Ala — region overview

The Ọmà Ala is a ~**250 km²** river-valley region in the forest–savanna transition of the pre-colonial Igbo homeland. It is crossed by the **Ọmà River** (flowing south to north into a wider waterway) and its two tributaries — the **Ụmụ River** (east) and the **Nkwụ Stream** (west) — and is bounded by the **Ahioma hills** to the east and the **Ezi-na-Oke forest** to the southwest.

The geography is deliberately varied to serve every gameplay and story need: a navigable river for transport and fishing; fertile alluvial and upland farmland for yam, cassava, cocoyam and palm; forest for wood, fibre and medicine; hills for defence and visibility; and wetlands/riversides for fishing and seasonal flood-refugia. Settlements cluster where farmland meets water and where the periodic markets can be held.

**Environmental zones (see also `WORLD_CALENDAR_ECONOMY_WEATHER_WILDLIFE.md` §6):**

| Zone | Coverage | Character |
|---|---|---|
| Riverine wetlands (Ọmà, Ụmụ, Nkwụ banks) | ~12% | Fishing, rice-plots, flood-season swell, reed-beds |
| Farmland (yam/cassava/palm intercrop) | ~28% | Terraced plots, sheds, dry/dry-farm rhythms |
| Secondary & river-edge forest | ~30% | Wood, fibre, medicine, honey, hunting, dangerous |
| Dense high forest (Ezi-na-Oke) | ~18% | Deep forest; resources & danger; masquerade/spirit sites |
| Grassland / derived savanna | ~6% | Grazing, palm-oil hamlets |
| Low hills (Ahioma) | ~4% | Quarries, defence, shrines on ridge-tops |
| Settlement footprint (towns, villages, compounds) | ~2% | Built environment, marketplaces, public squares |

---

## 2. The regional map

**(See `WORLD_GEOGRAPHY_SETTLEMENTS_POPULATION.md` diagrams and the production master map in `docs/04_PLANNING/` produced by Design. The map below is the canonical placement.)**

**Coordinate frame (Unreal-facing, see Engineering spec):** the regional map is authored in a world-space grid with origin at the Ọmà River crossing below Ahanwụ. Every settlement and landmark has fixed world coordinates (x east, z north, y = elevation). Distances in the table below are in-game traversal kilometres, computed from route distance (not straight line).

### 2.1 Settlement placements (regional map)

```
                        Ahioma hills (E)
                             ⛰
                 Ịbe ──────────────────────────────────────  (north)
                  ◖                  ◗
        Nkwụ ─── Ọmà Ukwu ─── Ahanwụ ─── Ihiala ──── river
        Stream   (town)      (village) (village)      (south)
         ◖         ◖◗        ◖◗        ◖◗
   Ọba ─── Ụmụ ─── Ọnịcha ── Ụkwụ ──── Ezimmiri ────────────
   (market)   River   (market)  (village) (pottery village)
              ◖
            Ezi-na-Oke forest (SW)
```

**Legend:** rivers/watercourses (───/◖), settlements (top: towns, ○ villages, ⚪ compounds), forests/hills. Routes are footpaths; river is navigable by canoe.

### 2.2 Geographical features

| Feature | Type | Position | World significance |
|---|---|---|---|
| **Ọmà River** | Major river | Runs north through the region's centre | Transport spine; fishing; flood seasonality; river crossing below Ahanwụ; canoe trade |
| **Ụmụ River** | Tributary | East, joining the Ọmà north of Ihiala | Eastern boundary of farmland; fishing; secondary crossing |
| **Nkwụ Stream** | Tributary | West, joining the Ọmà south of Ọba | Western boundary; reed/wetland; water access for Ọba |
| **Ahioma hills** | Low hills | Eastern edge | Visibility; defence; stone/clay; ridge-top shrines (access-restricted, evidence-backed) |
| **Ezi-na-Oke forest** | Dense high forest | Southwest | Deep forest resources & danger; masquerade/spirit sites |
| **Ọmà floodplain** | Wetland | Along the Ọmà | Rice-plots, seasonal flooding, fishing refugia |

---

## 3. The geographical reference atlas

A reference atlas mapping each location to: ID (TDD-WORLD prefix), world coords, elevation, biome, access, neighbours, story-location status, and references to Drive registers. **Every existing chapter location from the Drive `LOCATION_MASTER_REGISTER.md` v2.9 is to be mapped here** — this atlas is the bridge from canon to geography.

| Atlas ID | Name | Type | Elevation | Biome | Access | Neighbours | Story link |
|---|---|---|---|---|---|---|---|
| W-G01 | Ọmà River | Water | 18 m | Riverine | Canoe; footpath | Ahanwụ, Ọmà Ukwu, Ịbe | Chapter water routes |
| W-G02 | Ahanwụ Crossing | Crossing | 20 m | Riverine | Footpath/canoe | Ahanwụ, Ọmà Ukwu | ST05/ST06 access |
| W-G03 | Ahioma Ridge | Hill | 220 m | Grassland/hill | Footpath | Ịbe, Ịbe-Ezimmiri | Defence / viewpoints |
| W-G04 | Ezi-na-Oke | Forest | 40 m | High forest | Path | Ihiala, Ezimmiri | Forest chapters |
| W-G05 | Ụmụ–Ọmà Confluence | Water | 17 m | Riverine | Canoe | Ọmà Ukwu, Ihiala | Trade route |
| W-G06 | Nkwụ Reed-beds | Wetland | 16 m | Wetland | Footpath | Ọba | Fishing/weaving |

*(Full register to be expanded with all 142 canon locations; each maps to world coords and a settlement's catchment. Design owns the production master map; this atlas fixes the canonical placement.)*

---

## 4. Settlement hierarchy (researched)

Pre-colonial Igbo political/settlement organization (source: GRIN "The Colonial Interlude and the Igbo Judicial Systems"; Bscholarly "Pre-colonial Administration of the Igbo Society"; Grokipedia "Igbo culture"; Project MUSE "Traditional Igbo Architecture"):

**Household → Compound (Ezi/Obi) → Kindred (Ụmụnna) → Ward/Quarter → Village (Ama/Ogbe) → Village-group/Town (Obodo)**

Each level has distinct population scale, governance, and economic role. The Ọmà Ala follows this hierarchy.

- **Household (Ilo):** one family unit within a compound; the head (Okpara) represents it to the kindred.
- **Compound (Ezi):** clustered huts around a central open space/`obi`; the head-of-house (`obi`) presides. Multiple families.
- **Kindred (Ụmụnna):** a group of related compounds descended from a common ancestor; holds land rights.
- **Ward/Quarter (Ahịa mmiri / quarter):** a cluster of kindreds within a village.
- **Village (Ama/Ogbe):** a group of kindreds/quarters with a meeting-square (`ama`), a council of elders (`Oha`), and its own market-day.
- **Village-group/Town (Obodo):** several villages sharing a wider identity, commerce and market network; a `town` is the largest pre-colonial political unit.

---

## 5. World scale & explorable boundaries

**Playable world footprint:** **~18 km east–west × ~14 km north–south (~250 km²)**, bounded by:
- North: Ahioma hills / Ịbe farmland edge
- South: Ọmà floodplain / Ezi-na-Oke forest boundary
- East: Ụmụ River + Ihiala farmland
- West: Nkwụ Stream + Ọba farmland

**Believable distances** (traversal, not straight-line):

| Journey | Distance | Traversal time | Mode |
|---|---|---|---|
| Ahanwụ → Ọmà Ukwu (town) | ~4 km | ~50–70 min | Foot / canoe |
| Ahanwụ → Ihiala (village) | ~3 km | ~40–55 min | Foot |
| Ọmà Ukwu → Ịbe (town-out) | ~7 km | ~90–120 min | Foot / canoe |
| Ọmà Ukwu → Ọba (market) | ~6 km | ~80–105 min | Foot / canoe |
| Ọnịcha → Ụkwụ (river) | ~5 km | ~60–85 min | Canoe / foot |
| Cross-region (worst case) | ~12 km | ~2.5–3.5 h | Foot / canoe |

**Why this scale:** every destination is a genuine journey with a reason — a market day, a relative, a craft, a route. It is not "every place 2 minutes away." The region is large enough to feel like a world and small enough to be fully hand-crafted at HIGH quality within the budget. **Phasing never shrinks this footprint; the full region is the target.**

---

## 6. Settlements & landmark register

### 6.1 The towns and villages

| Settlement | Type | World position | Market day | Identity / economy | Est. pop. | Key landmarks |
|---|---|---|---|---|---|---|
| **Ọmà Ukwu** (Town) | Regional town | Centre, on Ọmà River | Eke (main) + daily stalls | Regional commercial hub; river port; largest market; crossroads of trade | ~2,200 | Grand market (Eke), river port/dock, craft quarter, town square (ama), head-of-town's `obi` |
| **Ịbe** (Town) | Town | Northeast, near Ahioma hills | Orie | Hill town; stone & clay; ridge defence; hill-farming; yam-rich | ~1,400 | Ahioma ridge path, clay/stone workings, hill-top square, Eke/Orie trader hostel |
| **Ahanwụ** (Village) | Village | Centre-south, near crossing | Afo | Story village — home of Adanna's family compound; subsistence farming + palm | ~900 | Adanna's family compound (ezi), ama square, well, shrine-grove (access-restricted) |
| **Ihiala** (Village) | Village | East, between Ọmà & Ụmụ | Nkwo | Farm village; fishers & palm; gateway to forest | ~750 | River-edge fishers' hamlet, farm plots, forest path |
| **Ụkwụ** (Village) | Village | East, on Ụmụ River | — (no major market) | Riverine village; fishing, reeds, rice-plots | ~500 | Canoe docks, fish-drying sheds, reed-beds |
| **Ezimmiri** (Village) | Village | Southwest, forest edge | — (no major market) | Pottery-specialised; clay from forest-edge pits; also forest products | ~600 | Pottery quarter, clay pits, forest trailhead |
| **Ọnịcha** (Market town) | Market settlement | West, on Ọmà | Orie | Fish & palm-oil market; river traders; weaving | ~1,100 | River fish market, palm-oil press sheds, trader hostel, weaving compound |
| **Ọba** (Market settlement) | Market settlement | Northwest, near Nkwụ | Afo | Cassava/cocoyam & grain market; wetland products; raffia | ~800 | Cassava/grain stalls, reed-craft, raffia sheds, crossroads |

### 6.2 Dispersed compounds & hamlets

Beyond the named towns/villages, the world contains **dispersed kindred compounds and hamlets** along the farmland/water interface — each a few households (ezi) with an `obi`, a cooking area, a granary, a small shrine-grove, and farm plots. These are the background population of the world and are placed at intervals across the farmland, forest edge, and river banks. **They are the source of the "people live here" feel** and are streamed in as background tiers.

**Compound typology (researched — Project MUSE "Traditional Igbo Architecture"; Grokipedia "Igbo culture"):**
- **Ezi** — family compound: clustered huts (`ilo`) around an open central space, enclosed by a low red-earth wall; the head's `obi` sits near the gate; separate huts for wives; barns, goat-sheds, hen-attachments; a small shrine-grove.
- **Obi** — the head-of-house's central hut and reception space; the seat of the compound's authority.
- **Ama** — the village public square for assemblies, dances, and markets.

### 6.3 Landmarks & special places

| Landmark | Type | Position | Access | Significance / note |
|---|---|---|---|---|
| **Ahanwụ Shrine-grove** | Sacred grove | Ahanwụ, beyond the compound | **Access-restricted** (specific rules; evidence-backed) | Ancestral/community shrine; specific restrictions need Research + cultural review — **not invented** |
| **Ahioma Ridge shrines** | Sacred sites | Ahioma hills | Restricted by tradition | Ridge-top sacred places; access rules evidence-backed, cultural review required |
| **Ọmà River Port** | Commerce | Ọmà Ukwu | Open | Canoe transport hub; river trade |
| **Ezimmiri Clay Pits** | Resource | Ezimmiri forest edge | Open | Pottery clay source |
| **Ahioma Stone Workings** | Resource | Ahioma hills | Open | Stone/clay for building & craft |
| **Ezi-na-Oke Forest Path** | Wilderness | SW forest | Open | Resource & danger; masquerade/spirit sites (narrative) |

> **Sacred-place handling:** No sacred feature, deity or ritual is invented for visual interest. The shrine-groves and ridge shrines follow **regionally documented** practice (sacred groves, ancestral shrines, access restrictions) and every specific restriction requires **evidence + cultural review** before it is authored. The **Ancestral Realm retains its established narrative status** and is **not** repurposed into an ordinary-world location; it is a distinct narrative space. (See `WORLD_SOURCE_AND_EVIDENCE_REGISTER.md`.)

---

## 7. Travel, routes & exploration

**Routes are the connective tissue of the world.** Each settlement is connected by footpaths (and where water allows, canoe routes), forming a traversable network:

- **Main north–south river route:** Ụkwụ → Ihiala → Ahanwụ → Ọmà Ukwu → Ọnịcha (canoe-capable; the "trade spine").
- **East–west foot routes:** Ọmà Ukwu → Ahanwụ → Ezimmiri; Ịbe → Ọmà Ukwu; Ọba → Ọnịcha.
- **Cross-country farm paths:** link dispersed compounds and hamlets to their villages and market town.

**Travel system design:**
- Journeys are real (distances in §5). Travel is a choice with reasons — market day timing, weather, a quest, a relative to visit, a craft to obtain.
- Weather affects travel: heavy rain muddies paths, raises the Ọmà (breaking crossings → canoe needed), lowers visibility; dry season opens routes and dries the floodplain.
- Routes have ambient life: farmers with loads, traders with carts, hunters, children — the journey itself is part of the world.
- **Fast travel is NOT instant teleport** between settlements; where used, it respects route distance and weather. (No "2-minute world." The full region is traversed on its real scale.)

**Player reasons to explore:** market-day schedules (different markets on different days), craft specialisation (Awka-style smithing at Ịbe, pottery at Ezimmiri, weaving at Ọnịcha), story locations, seasonal/agricultural events, relatives and relationships, and the journey's own encounters.

---

## 8. Population atlas

### 8.1 Regional population estimate

| Level | Settlement(s) | Combined est. population |
|---|---|---|
| Regional town | Ọmà Ukwu (2,200) + Ịbe (1,400) | 3,600 |
| Market settlements | Ọnịcha (1,100) + Ọba (800) | 1,900 |
| Villages | Ahanwụ (900) + Ihiala (750) + Ụkwụ (500) + Ezimmiri (600) | 2,750 |
| Dispersed compounds & hamlets | ~30 compounds × ~15–25 people | ~600 |
| **Regional total** | | **~8,850** |

**Population is NOT a fixed render count.** The persistent population is simulated; market-day and event surges add temporary attendees. The full regional population of ~8,850 is distributed across the **three NPC tiers** (named / crowd / background), with the bulk in background and crowd tiers and a curated set of named actors. This is the "genuinely populated" requirement — solved by simulation, not by hand-placing 8,850 full-AI actors.

### 8.2 NPC categories (researched — pre-colonial Igbo occupations)

The world populates with **occupation-based NPC categories**, each with homes, routines and destinations:

| Category | Igbo-grounded | Where they live / work | Routines & destinations |
|---|---|---|---|
| **Farmers** | Men cultivate yams (prestige crop); women cultivate cassava, cocoyam, vegetables, palm | Farmland, compounds, village granaries | Field work by season; yam harvest; market delivery |
| **Traders** | Women prominent in trade; market networks | Market towns, trader hostels | Market-day stalls; inter-town travel; goods transport |
| **Artisans — smiths** | Awka-style ironworking (regionally documented) | Ịbe (smithing quarter), market towns | Tool-making; market sales; repair |
| **Artisans — potters** | Women-led pottery (Ishiagu, Afikpo, Nsukka, etc.) | Ezimmiri (pottery quarter) | Clay extraction; firing; market sales |
| **Artisans — weavers** | Women's weaving centres (Nsukka, Akwete, etc.) | Ọnịcha, market towns | Fibre prep; mat/cloth weaving; market sales |
| **Artisans — woodworkers** | Woodcarving (masks, figures) | Forest-edge workshops | Timber; carving; ritual/market work |
| **Hunters** | Hunting + trapping | Forest edge, Ezi-na-Oke | Hunt cycles; game delivery to market |
| **Fishers** | Riverine fishing | Ụkwụ, Ọnịcha, Ọmà banks | Daily fishing; drying; market |
| **Builders** | Compound/house construction | Villages, town | Building, repairs, construction cycles |
| **Children** | — | Compounds, ama squares | Play, chores, schooling/age-grade activities |
| **Older residents** | Elders, title-holders, council | Compounds, ama square | Council, mediation, ritual, craft wisdom |
| **Leaders** | Okpara, Obi, Oha council, title-holders | Compound `obi`, ama square | Governance, meetings, ceremonies |
| **Travellers / traders** | Long-distance traders, traders' hosts | Trader hostels, routes | Inter-town movement; market attendance |

**Dialect & naming:** all names from the approved `docs/IGBO_NAME_CATALOGUE.md` / Drive `CHARACTER_DESIGN_REGISTER.md`; no invented native names (see source register). Occupational and place terms use the researched Igbo vocabulary above with dialect variation where appropriate.

### 8.3 Population distribution — residential / economic / public

**Residential:** the bulk of the population lives in compounds across all settlements and dispersed hamlets; each settlement's residential population is its base, persistent tier.
**Economic:** occupation-driven NPCs concentrate where their work happens — farmers on farmland, smiths in the Ịbe quarter, potters in Ezimmiri, fishers on the river, traders in market towns. This gives each settlement a distinct economic identity.
**Public/community:** the `ama` squares, markets, shrine-groves, and town-square host public life — assemblies, dances, council, and events. Population surges here on market days, festivals, and story events.

**Settlement identity differentiation (acceptance):** entering Ọmà Ukwu reads as a busy commercial river town; Ịbe as a hill-farming smithing town; Ahanwụ as a farming/story village; Ụkwụ as a river-fishing village; Ezimmiri as a pottery village; Ọnịcha as a fish/palm-oil market town; Ọba as a cassava/grain market. Each has its own scale, economy and activity.

---

## 9. Open questions / items needing confirmation

1. **Canon placement of all 142 Drive locations** — confirm the exact world coordinates and settlement catchment for each existing chapter location (this atlas fixes the canonical frame; Design maps them).
2. **Sacred-place specifics** — exact rules/access for Ahanwụ shrine-grove and Ahioma ridge shrines need Research evidence + cultural review before authoring.
3. **Ancestral Realm integration** — its narrative status is fixed; how it's represented in world space (if at all) is a Story decision.
4. **Market-day assignments** — the Eke/Orie/Afo/Nkwo assignment above is the proposed regional arrangement; verify against any canon that fixes Ahanwụ/Ọmà Ukwu's market day.
5. **Population final figures** — estimates above are planning figures; final numbers approved with Design/owner.

*End of TDD-IMPL-WORLD-002.*
