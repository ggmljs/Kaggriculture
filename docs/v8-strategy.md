# V8 strategy: divergence-gated third-Yarn milk routing

V8 keeps V7's ten route tapes and recovery-aware execution controller. Its
only behavioral change repairs a conflict in the V7 route priority: when Yarn
was the third unlocked shop, V7 always chose 6C/8S even if one of the first two
shops exposed milk demand. V8 uses the two farms' public production layouts at
that shared-prefix boundary to decide whether the third-Yarn case should stay
on 6C/8S or use the existing 10C/4S expert.

The frozen candidate is self-contained in `main.py` with SHA-256
`faf57412e2c56dcc669043865a185324bab9952d865abccc2203284e854eceb3`.
Its selector reads only public shops and public farm tiles. It does not read an
opponent identity, episode ID, submission ID, random seed, hidden inventory,
future action tape, or replay lookup table.

## Latest remote snapshot and failure set

The latest official snapshot retrieved at `2026-08-23T15:45:18Z` placed
`ziliangCok` at rank 53 of 6,021 with V7 score `2626.4`. The downloaded
leaderboard archive SHA-256 was
`78b56f62fa43ff2f97604a9c6e856b6de64092eb24ded5a1c22f368cd18dea74`.
Leaderboard ratings and ranks are dynamic; this timestamped observation is not
an immutable score or a claim about the strength of a local artifact.

Kaggle exposed 200 completed V7 public episodes: 140 wins, 59 losses, and one
tie. All 200 replay files were downloaded. The 59 losses had mean margin
`-5721.831`, median `-2597`, and worst margin `-35604`; all finished with
`DONE/DONE`, so termination and invalid-action crashes were not the dominant
failure mode.

The route-level loss split was:

| Effective V7 route | Losses | Mean margin | Worst margin |
|---|---:|---:|---:|
| current 10C/4S | 26 | -4841.731 | -18169 |
| current 6C/8S | 15 | -11790.067 | -35604 |
| current 8C/6S | 7 | -2377.143 | -6373 |
| current second-Yarn 6C/12S | 5 | -1905.200 | -3576 |
| current first-Yarn 6C/12S | 4 | -1365.750 | -3433 |
| legacy 10C/4S | 2 | -1611.500 | -2109 |

The unusually deep 6C/8S group contained repeated third-Yarn prefixes with an
earlier milk-support shop. Several opponents visibly developed toward a
10C/4S-like farm while V7 remained on 6C/8S, producing large late milk and
market-cadence deficits. This is an observational cluster, not by itself a
causal proof.

The final frozen-V7 replay audit covered all 200 public games. Raw replay JSON
was byte-for-byte equivalent on 187/200. The thirteen exceptions differed only
in Kaggle's nondeterministic `remainingOverageTime` runtime-budget field; after
excluding that field, all 200 had the same gameplay observations, V7 actions,
rewards, 720 states, `DONE/DONE`, metadata, and balanced market cashflow.

## Hypothesis screening

A blanket rule that sent every third-Yarn plus milk-support prefix to 10C/4S
was rejected. It improved several losses but changed a near-mirror control from
a V7 win to a loss. The distinguishing public signal was not the shop prefix
alone; it was whether the two farms had already committed to measurably
different production layouts when the third shop became observable.

V8 therefore computes a public L1 distance over six tile counts:

```text
D = |cow_ours - cow_opp|
  + |sheep_ours - sheep_opp|
  + |wheat_ours - wheat_opp|
  + |melon_ours - melon_opp|
  + |strawberry_ours - strawberry_opp|
  + |empty_pasture_ours - empty_pasture_opp|
```

Animal or crop tiles count toward their animal or crop dimension; only a
pasture without a recognized animal contributes to `empty_pasture`. The
selector uses a deliberately small, fixed threshold of three tiles. It does
not fit weights or memorize episode-specific vectors.

## Route decision

The per-seat selector applies this order:

| Observable signal | V8 route |
|---|---|
| first shop is `YARN_STORE` | first-Yarn 6C/12S |
| Yarn appears in the first two shops | second-Yarn 6C/12S |
| Yarn is third and neither first-two shop supports milk | 6C/8S |
| Yarn is third, first-two milk support, and `D >= 3` | 10C/4S |
| Yarn is third, first-two milk support, and `D < 3` | 6C/8S |
| no first-three Yarn but an early milk-support shop | 10C/4S |
| no earlier signal | 8C/6S |

Milk-support shops are `PIZZA_SHOP`, `ICE_CREAM_SHOP`, and
`SMOOTHIE_SHOP`. The third-Yarn decision is sticky for the rest of the episode,
isolated by seat, and cleared when an episode resets or the observed step
rewinds. First-Yarn, second-Yarn, non-milk third-Yarn, ordinary milk, default,
and legacy-opening decisions are unchanged from V7.

The decision is made at the shared-prefix boundary. The 6C/8S and 10C/4S
experts have the same actions before the third-shop observation becomes
usable, so V8 does not pretend that it can rewrite already executed actions.
It switches both the route tape and its derived sale schedule atomically.

## Retained execution controller

V8 retains V7's independently maintained execution controls:

- step-24--71 public legacy-layout compatibility routing;
- day-boundary weed transaction recovery and actor-local weed handling;
- atomic planting and route-prefix seed-feasibility checks;
- observable cow placement and partial animal-purchase reconciliation;
- bounded premium prepayment with quantity-conserving repayment;
- executable same-turn shed projection for SELL ranking;
- terminal wheat-seed pruning and market-order caps;
- per-seat retry-safe action caching and malformed-observation fallback.

The five current and five legacy route tapes remain modified, normalized, and
compressed derivatives of the Apache-2.0 artifact documented in
[`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md). V8 adds no new external
route data.

## Verification and preservation gates

### Full public fixed-tape gate

The fail-closed gate replays all 200 captured public opponent action tapes
against both the frozen V7 file and the candidate. It first requires V7 to
reproduce recorded actions, rewards, statuses, and terminal state exactly;
only then are candidate deltas considered. The promotion condition is:

1. all 140 recorded V7 wins remain candidate wins;
2. at least one recorded non-win flips to a win;
3. total wins and mean margin do not decrease;
4. every replay reaches 720 states, `DONE/DONE`, with no stderr.

Fixed opponent actions make this an open-loop counterfactual preservation
test, not a policy rematch or leaderboard-score guarantee. Final full-tape
results were 140 wins, 59 losses, and one tie for calibrated V7 versus 145
wins, 54 losses, and one tie for V8. V8 improved nine margins, changed no other
row, regressed no row, and flipped five losses. Mean margin increased from
`+3236.640` to `+4058.725`, a delta of `+822.085`. All 140 V7 wins remained
wins. The result JSON SHA-256 is
`179c8e56ed16b577bcb602669f9ed3833b064dd377785c762ed0c85e2a49989e`;
full fields and episode IDs are recorded in
[`docs/evidence/v8-failure-analysis.json`](evidence/v8-failure-analysis.json).

### Targeted closed-loop paired panel

The paired panel uses the 11 third-Yarn seeds found during failure analysis,
four hash-pinned public artifacts, both seats, and the same environment for V7
and V8. Across 88 games, V7 scored 56 wins and 32 losses; V8 scored 84 wins and
4 losses. V8 improved 28 rows, left 60 margins exactly unchanged, regressed no
row, and preserved all 56 V7 wins. Mean margin delta was `+5367.795`.

| Opponent | V7 W-L | V7 mean | V8 W-L | V8 mean |
|---|---:|---:|---:|---:|
| V21 public-state portfolio | 19-3 | +2681.364 | 19-3 | +2681.364 |
| V17 10C/4S | 8-14 | -6570.636 | 22-0 | +4164.955 |
| Tetsu adaptive | 21-1 | +3958.318 | 21-1 | +3958.318 |
| public demand-MoE | 8-14 | -6570.636 | 22-0 | +4164.955 |

All 176 candidate-and-baseline executions reached 720 states, `DONE/DONE`,
with no stderr. V17 and the public demand-MoE are distinct downloaded source
artifacts even though they produced the same results on this targeted panel.
The V7 and final-V8 result JSON SHA-256 values are respectively
`ffbfe44ca7b0a85404499916d0df9001520b2940ea996381a66511d0abf3f5a0`
and `6918e806aeaa1aefa9a095286ad4f0bc2c59633183f3b5fc424f6f2faf9bd33d`.

### General regression and runtime gates

The frozen V7 and V8 files were additionally evaluated on eight fresh seeds,
six deduplicated public artifacts, and both seats. All 96 V8 rows were
margin-identical to V7: both policies scored 82 wins and 14 losses, with no
tie. Every row reached 720 states, `DONE/DONE`, with no stderr, and every
opponent-level mean margin was positive.

| Hash-pinned opponent | Games | V7/V8 W-L | Mean margin |
|---|---:|---:|---:|
| Kaito V42 | 16 | 12-4 | +553.688 |
| Tetsu adaptive | 16 | 16-0 | +2504.938 |
| Tetsu Read the Town | 16 | 16-0 | +2502.313 |
| V21 public-state portfolio | 16 | 8-8 | +2321.313 |
| public demand-MoE | 16 | 15-1 | +6223.063 |
| V17 10C/4S | 16 | 15-1 | +11883.750 |

The frozen V7 and V8 result JSON SHA-256 values are respectively
`f862f0bd37d59d74de5d4e008318a32af8e1670a7323d8ebcdd480d7a48dde07`
and `12abc5fa629645795f67e6f060edaed5e850323a52bb71915ed95e54091d3add`.
Repository tests, both-seat starter/random smokes, dependency checks, import
checks, and deterministic packaging were rerun after the candidate hash was
frozen: `pip check` found no broken requirements, all 66 tests passed, and all
four smoke games reached 720 states with `DONE/DONE`. Two independent package
builds were byte-identical. The 99,945-byte archive SHA-256 is
`5c410ffb2a3637ce8840274c7eab70813c270209cbcbb79e735eb2c547a4b35d`;
it contains only `main.py`, `LICENSE-APACHE-2.0.txt`, and
`THIRD_PARTY_NOTICES.txt`. Exact seeds and opponent hashes are in the evidence
JSON.

## Claim boundary

The preservation gates substantially reduce the known regression risk, but no
finite local panel can guarantee a nondecreasing dynamic Kaggle rating. Public
opponents, matchmaking, and rating updates change over time, and a new
submission starts with its own remote rating trajectory. V7 remains a separate
submitted artifact, while V8 is promoted only after preserving all captured
V7 wins and improving both fixed-tape and closed-loop evidence.
