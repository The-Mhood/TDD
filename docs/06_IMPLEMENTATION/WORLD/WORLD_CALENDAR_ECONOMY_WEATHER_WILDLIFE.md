# TDD — World Calendar, Economy, Weather & Wildlife

**Document ID:** TDD-IMPL-WORLD-003 · **Version:** 1.0 · **Date:** 2026-11-21
**Companion to:** `WORLD_SCALE_AND_LIVING_WORLD_BLUEPRINT.md` (TDD-IMPL-WORLD-001), `WORLD_GEOGRAPHY_SETTLEMENTS_POPULATION.md` (TDD-IMPL-WORLD-002)
**Owner:** PM, with Research (calendar/climate/economy evidence) and Engineering (systems).

---

## 1. The world calendar — Ọgụàfọ̀ (Igbo calendar)

**Source (documented):** The traditional Igbo calendar has **13 months (afọ)** in a year, **7 weeks (izu)** in a month, **4 days (ubochi)** in a week — the four market days **Eke, Orie, Afo, Nkwo** — plus an intercalary day in the final month. The calendar is **neither universal nor synchronized**: communities run at different stages, but the 4/8-day cycle synchronises inter-village market days. (Wikipedia "Igbo calendar"; Oblong Media "NDIGBO: Market Days in Igbo Theosophy"; dibianwangwuuchendu "Ògụ́àfọ̀: The Igbo Calendar".)

### 1.1 Calendar structure

| Unit | Igbo name | Value |
|---|---|---|
| Day (market day) | **Ubochi** | Eke · Orie · Afo · Nkwo (4-day week) |
| Week | **Izu** | 4 market days |
| Month (moon) | **Ọnwa** | 7 izu = 28 days |
| Year | **Afọ** | 13 Ọnwa = 13 months, + 1 intercalary day |

**Months (Ọnwa)**: Ọnwa Mbụ, Ọnwa Abụọ, Ọnwa Ife Eke, Ọnwa Anọ, Ọnwa Agwụ, Ọnwa Ise, Ọnwa Isii, Ọnwa Isii, Ọnwa Asaa, Ọnwa Ise (continuing through to the final intercalary month). *(Full ordered month list per source — see register.)*

### 1.2 Market-day meanings (documented, with cultural nuance)

| Day | Association | Note (source) |
|---|---|---|
| **Eke** | East; creation; **most sacred**; big trading day | Often the largest/most important trading day; sacred — full-grown people not normally buried on Eke |
| **Orie** | West; water; social exchange | Farm work commonly done on Orie |
| **Afo** | North; earth; farming, justice | Influences preparation of goods for market |
| **Nkwo** | South; air; trade, intellect | Often a busy market day |

**Important caveat (documented):** the four days come in **alternating "major" and "minor" cycles, giving an 8-day cycle**. Market days are **not identical schedules across Igboland** — each community holds its main market on its own day. The Ọmà Ala follows this: **different settlements host markets on different days**, so the player travels between settlements to catch different markets.

### 1.3 The 8-day cycle

```
Eke(1) Orie(2) Afo(3) Nkwo(4)  |  Eke(5) Orie(6) Afo(7) Nkwo(8)
└──────── first 4-day week ────────┘ └─────── second 4-day week ───────┘
   (major cycle)                    (minor cycle)
```

The game's clock runs on this cycle. Each `ubochi` is a distinct gameplay day: ordinary day vs market day vs rest day vs story event.

---

## 2. Market system & schedules

### 2.1 Market network (regional differentiation)

Each market settlement hosts its **main market on its assigned day**, with daily stalls on the other days. The player travels to whichever market is busy on the current day.

| Market | Settlement | Main day | Products / identity | Attendees / traders |
|---|---|---|---|---|
| **Ọmà Ukwu Grand Market (Ahịa Ọmà Ukwu)** | Ọmà Ukwu | **Eke** | The region's largest; everything — yams, palm oil, fish, iron tools, pottery, cloth, baskets, beads | Regional traders, all villages, long-distance traders |
| **Ọnịcha Fish & Palm Market** | Ọnịcha | **Orie** | River fish (fresh/dried), palm oil/kernels, palm-oil products, cloth | River-traders, fishers, weavers |
| **Ọba Cassava & Grain Market** | Ọba | **Afo** | Cassava, cocoyam, grains, reed/raffia products | Farmers, wetland crafters |
| **Ịbe Hill Market** | Ịbe | **Eke** (minor) | Yams, stone/clay goods, iron tools (smithing), hill produce | Hill farmers, smiths |

*(Proposed assignment; verify against any canon fixing Ahanwụ/Ọmà Ukwu's market day. The design intent: the player can always find a busy market by travelling, and the choice of *which* market is a meaningful player decision.)*

### 2.2 Market as a gameplay system

A market day is **not just a lighting clock** — it is a functioning system:

- **Traders & customers:** stall-holders arrive and set up at dawn; customers surge through the day; the crowd density follows a daily curve (build-up → peak → dispersal).
- **Stalls & goods:** each market has themed stalls — yam stalls, fish stalls, palm-oil stalls, tool/smith stalls, pottery stalls, cloth/mat stalls, basketry, bead/ornament stalls, food-cooking stalls.
- **Prices & availability:** prices shift with season (post-harvest gluts, lean-season scarcity), weather (rain disrupts supply/prices), and events. Goods differ by market.
- **Information & events:** markets are where news, rumours, story clues and NPC relationships concentrate. Meeting a specific NPC, hearing a lead, or witnessing an event may require being at the right market on the right day.
- **Market identity:** each market has its own smell/sound/layout/product-mix; Ọmà Ukwu is vast and chaotic, Ọnịcha is fishy and riverine, Ọba is grain-and-cassava, Ịbe is tool-and-yam.

### 2.3 Trading relationships & transport

- **Inter-settlement trade:** villages bring surplus (yam, palm, fish, craft) to the market towns; towns redistribute goods and crafted items back out. Traders travel between settlements on footpaths and canoe routes.
- **Transport:** head-loading, carts, and canoe transport along the Ọmà/Ụmụ rivers; market-day caravans move along the main routes.
- **Trader travel distance:** traders from a village walk the 3–7 km to their market town; long-distance traders move between towns over a day or more.

---

## 3. Economy model

The economy is **interconnected and occupation-driven** (researched: pre-colonial Igbo agrarian economy + craft specialisation + trade).

**Production → distribution → consumption:**
- **Farmers** produce yams (men, prestige), cassava/cocoyam/vegetables/palm (women). Surplus enters the market.
- **Smiths** (Ịbe) produce hoes, machetes, knives, gongs — circulated through trade to farms and villages.
- **Potters** (Ezimmiri) produce cooking/storage pots — traded regionally.
- **Weavers** (Ọnịcha) produce mats, cloth, baskets.
- **Fishers** (Ụkwụ, Ọnịcha) produce fresh/dried fish.
- **Traders** move goods between settlements and to the market towns.

**Moneyless exchange with a trade-value system:** the game models goods with trade values (barter/exchange, the pre-colonial norm) rather than a single currency. Player trades, quests and market activity use this value system.

**Regional interdependence:** no settlement is self-sufficient — Ọmà Ukwu needs the farms' yams and the smiths' tools; Ezimmiri's pots reach every settlement; Ụkwụ's fish feeds the towns. This interdependence is the substance of the living economy and gives the player reasons to travel.

---

## 4. Seasonal model

**Source (documented):** the Igbo homeland is in the **tropical rainforest / Guinea-Savanna transition** — a **wet season** and a **dry season** (not a European 4-season model). The Anambra/Igbo region has a tropical climate with distinct wet and dry seasons; the rainy season drives planting/harvest and floods. (naijahistory "Anambra State"; Grokipedia "Igbo culture"; Sankofapedia "Cultures:Igbo".)

### 4.1 The two seasons

| Season | Approx. months | Character |
|---|---|---|
| **Rainy season (Ọkọchasị / wet)** | ~April–October | Heavy rains; rivers swell; floodplain floods; roads/paths turn to mud; dense green growth; farm work peaks |
| **Dry season (Ọkọchasị / dry)** | ~November–March | Dry; rivers fall; floodplain recedes; harvest/dry-farm; smoke/haze; visibility clear; travel easier |

*(The Igbo calendar's 13-month structure maps onto these seasons; the exact month boundaries are researched/adapted — see register.)*

### 4.2 Agricultural cycle

- **Rainy season:** land preparation, planting (yam, cassava, cocoyam, palm), weeding; river fishing declines as floods spread fish into floodplains.
- **Transition:** yams maturing; early harvests.
- **Dry season:** **New Yam Festival (Iri Ji)** — the yam harvest celebration (documented; a major community event); dry-farm crops; river fishing recovers as waters recede; market gluts from harvest.

**The New Yam Festival (Iri Ji)** is the anchor seasonal event — a region-wide celebration at the yam harvest, with feasting, dancing, and masquerade (documented). It is a major world event the player can attend.

---

## 5. Calendar → gameplay mapping

| In-game state | Igbo day / period | World behaviour |
|---|---|---|
| **Ordinary day** | non-market ubochi | Normal routines: farming, craft, household life, travel |
| **Market day** | the settlement's assigned ubochi | Market surge; traders/customers converge; prices/events/info |
| **Festival day** | Iri Ji / masquerade days | Regional celebration; special events, masquerade, feasting |
| **Seasonal phase** | rainy / dry | Weather, farming, travel, water levels change (§6) |

The player's choice of *where to travel and when* is driven by this calendar: catch a market, attend a festival, farm, or seek a story event.

---

## 6. Weather & environmental progression

**Source (documented):** tropical wet/dry climate; rainy-season rainfall, river swelling, floodplain flooding; dry-season haze/low water. The environment must change with time/weather/seasons.

### 6.1 Weather model

**Weather is a functioning system, not a static look.** It drives:

- **Rainfall:** tropical downpours, heavy storms, drizzle. Rain frequency/intensity follows the seasonal curve.
- **Clouds & visibility:** rain-cloud build-ups; dry-season haze.
- **Mud & paths:** rain turns paths and settlement approaches to mud; deep ruts; slippery crossings.
- **Rivers & water:** the Ọmà/Ụmụ/Nkwụ swell and fall with the seasons; floodplain floods; crossings break in high water (canoe required).
- **Vegetation:** rainy = lush, dense, green; dry = drier, browner, leaf-fall, fire-clearing.
- **NPC clothing & activity:** rain → shelter, changed clothing, reduced outdoor activity, market disruptions; dry → full activity, dry-farm, festivals.
- **Agriculture:** rainy = planting/weeding; dry = harvest, drying, storage.

**Market-in-rain ≠ market-in-dry:** the same market on the same day looks and behaves differently — rain-stalls with tarpaulins, fewer customers, slick ground, goods under cover; dry = full open stalls, peak crowd.

### 6.2 Environmental progression (the world must not look identical)

| Phase | Visual / behavioural state |
|---|---|
| **Early rainy** | Fresh green; rivers rising; paths firm→soft |
| **Peak rainy** | Dense lush forest; swollen rivers; flooded floodplain; heavy mud; frequent storms |
| **Late rainy** | Green fading; rivers still high; harvest begins |
| **Dry season** | Drier, browner; low rivers; exposed floodplain; clear visibility; smoke/haze; harvest/festival |
| **Late dry** | Driest; fire-clearing; water scarce; preparation for rains |

Each biome transitions through these phases. **The environment must not look identical on every visit** — the player returns to a changed world.

### 6.3 Weather vs market-day interaction (key acceptance)

Weather is the *envelope*; the market-day cycle is the *pulse*. A market day in peak rainy season is a wet, muddy, covered market with fewer but determined traders; the same market in dry season is a sun-blasted, open, full market. This interaction is part of the acceptance evidence.

---

## 7. Wildlife & vegetation

**Source (documented):** the Igbo forest/savanna ecology supports game, fish, birds, and a rich plant base. Verified Igbo names are used where available; uncertainty is recorded (see source register). **No invented names.**

### 7.1 Animals (grounded in regional ecology)

| Animal | Igbo name (verified/adapted) | Habitat | Role in world |
|---|---|---|---|
| **Yam** (cultivated) | Iji | Farmland | Staple/prestige crop; the agricultural core |
| **Oil palm** | Osisi / mkpuru osisi | Farmland/forest edge | Palm oil, kernels, soap, fibre |
| **Cassava** | Akpụrụ / akpụrụ ọkụ | Farmland | Staple (women's cultivation) |
| **Cocoyam** | Ede | Farmland/wetland | Staple |
| **Plantain** | Ọkwụ / ụkwụ | Farmland | Staple/fruit |
| **Raffia palm** | Ọkụ / akpụrụ ọkụ | Forest edge/wetland | Weaving fibre |
| **Goat** | Ezi / anụ ezi | Compounds/farmland | Livestock, sacrifice |
| **Chicken/hen** | Akpa / ehi | Compounds | Livestock, trade |
| **Dog** | Nwa nkịta / nkịta | Compounds | Companion, hunting |
| **Fish** | Ọsị / anụ ọsị | Rivers/floodplain | Fisher folk's livelihood |
| **Antelope / duiker** | Nkịta ọhịa / enyi | Forest | Hunting |
| **Monkey** | Ọtụ / ọtụ ọhịa | Forest | Forest life |
| **Birds (various)** | various | All | Ambient forest/farm life |

*(Where a name is uncertain, it is marked as adapted and requires Research/cultural confirmation — no invented names are accepted as canon.)*

### 7.2 Plants & materials

- **Yam** (iji), **cassava** (akpụrụ), **cocoyam** (ede), **plantain** (ọkwụ), **oil palm** (osisi), **raffia** (ọkụ) — staple crops and fibres (documented, above).
- **Obeche / mahogany / iroko** (timber, documented) — woodworking/building.
- **Leafy greens, okra, melons, peppers** — women's cultivation and market goods (documented).
- **Medicinal plants** — forest/farm, used by healers (evidence-backed; specific uses need cultural review).

**Wildlife is ambient and seasonal:** fish spawn with the flood cycle; game is more abundant in certain seasons; crops grow and are harvested on the calendar. Wildlife is part of the environment's change.

---

## 8. Acceptance & open items

**Calendar/market acceptance:** travelling to a settlement on its market day yields a genuinely busy market; ordinary days show normal routines; the calendar progresses the world.
**Weather/seasonal acceptance:** the environment visibly changes across rainy/dry and across weather; market-in-rain ≠ market-in-dry; NPC clothing/activities respond.
**Open items:** finalise exact month boundaries; confirm market-day assignments vs canon; verify animal/plant Igbo names with Research/cultural review (record uncertainty, no invented names).

*End of TDD-IMPL-WORLD-003.*
