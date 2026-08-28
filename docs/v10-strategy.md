# V10 strategy: fail-closed opening recovery

V10 keeps the complete V9 controller as its default policy and introduces one
seat-relative recovery branch at the first safe route divergence. The branch
recognizes a repeated public opening family that V9 handled poorly and reuses
the frozen V5 low/high route for that family. Every incomplete, malformed, or
non-matching observation remains on V9.

Returning to a public score of `2600+` is the operating target, not a verified
result. Simulation ratings start a new trajectory for every submission and
change as games are sampled. V10 must therefore be described as delivered only
after Kaggle validation, and as having reached the target only after a live
score at or above 2600 is observed.

## Latest remote snapshot before V10

The submission API snapshot at `2026-08-28T15:54:29Z` was:

| Version | Submission | Status | Dynamic score |
|:---|---:|:---:|---:|
| V4 | 55569567 | COMPLETE | 2656.6 |
| V5 | 55574866 | COMPLETE | 2656.4 |
| V6 | 55596752 | COMPLETE | 2343.2 |
| V7 | 55638354 | COMPLETE | 2192.2 |
| V8 | 55719179 | COMPLETE | 1809.5 |
| V9 | 55817164 | COMPLETE | 1677.2 |

Only V8 and V9 occupied the team's two active simulation slots. The older
V4/V5 scores remain visible in submission history but no longer supplied the
team's active rating. The earlier leaderboard archive at
`2026-08-28T14:23:49Z` placed `ziliangCok` at rank 765 of 6,735 with score
1801.9 and `SubmissionCount=2`.

These values are dynamic observations, not controlled head-to-head results.

## Why the later versions became weaker online

The failure audit found no single terminal or schema defect that explains the
decline. Five effects accumulated:

1. **Active-slot replacement.** Both historically stronger V4/V5 rating
   trajectories were displaced by later policies from the same specialized
   lineage.
2. **Replay-derived route specialization.** V6 through V8 added increasingly
   specific routes and observable gates. A fixed opponent-action tape does not
   model how a live opponent reacts to the changed policy.
3. **Objective mismatch.** Development often emphasized aggregate or mean
   margin, while the public rating is driven by wins and losses. Large positive
   outliers can hide losing more individual games.
4. **Dynamic-opponent confounding.** Each submission faced a different sampled
   population and rating trajectory. Remote score gaps alone cannot identify a
   selector as the sole causal failure.
5. **V9's terminal repair is not the regression source.** All 90 currently
   exposed V9 public episodes reached 720 states and `DONE/DONE`. V9 actions
   replayed exactly, including the three episodes retrieved after the V10 gate
   was preregistered, and terminal sellable stock remained reconciled.

The practical lesson is to require per-game zero regression and known-win
preservation before promotion. Aggregate improvement is supporting evidence,
not the release gate.

## Recovery branch

At step 72, V10 reads only public, current-game state. It selects the recovery
route when all conditions hold:

- the first unlocked shop is `BAKERY` or `PIZZA_SHOP`;
- the opponent public farm has exactly 1 cow, 4 sheep, 5 wheat, and either 4
  or 5 melon;
- the candidate's public cash is lower than the opponent's public cash.

Cash must be explicitly present, finite, and non-boolean. Shop and tile
structures must have the expected public schema. Missing or malformed values
close the gate. The decision is sticky, seat-isolated, retry-safe, reset on a
new game, and cannot open after step 72.

All ten V9 current/legacy tapes and the V5 low route have an identical action
prefix through step 71, so the decision occurs before behavior diverges. If
the gate opens, V10 retains the V5 step-168 public-shop decision: a later Yarn
shop selects the high 6C/12S route; otherwise it keeps the low 10C/4S route.
V9's execution controls and step-718 projected-shed liquidation remain active
for both paths.

The gate uses no identity, episode ID, submission ID, seed, opponent-private
state, replay lookup, or future action.

## Final-hash anti-regression evidence

The release candidate `main.py` SHA-256 is
`56831f3c43c9727d90016b7a7a8d4eb51d1a4c08c1120d58f061d9176e8bc109`.
The final hash was executed against three calibrated public replay corpora:

| Corpus | Games | V9 W/T/L | V10 W/T/L | Improved | Identical | Regressed | V9 wins preserved |
|:---|---:|:---:|:---:|---:|---:|---:|---:|
| V7 public control | 333 | 169/2/162 | 169/2/162 | 2 | 331 | 0 | 169/169 |
| V8 public control | 177 | 110/1/66 | 111/1/65 | 2 | 175 | 0 | 110/110 |
| latest V9 public | 87 | 57/0/30 | 59/0/28 | 3 | 84 | 0 | 57/57 |
| **Combined** | **597** | **336/3/258** | **339/3/255** | **7** | **590** | **0** | **336/336** |

The combined mean margin moved from `+1171.886` to `+1266.020`. Every run
completed 720 states with `DONE/DONE` and empty stderr. The seven changed rows
all improved and three losses became wins.

These are fixed recorded-opponent-action counterfactuals. They enforce exact
per-game safety under the recorded tapes but are not closed-loop rematches or
leaderboard forecasts.

After the gate was frozen, three newly exposed V9 public episodes were pulled.
The gate matched none; final-hash V10 and V9 produced identical actions and
margins in all three. A separate 80-game closed-loop panel against five
hash-pinned opponents was also identical to V9 on every row at 68/80 wins and
mean margin `+2515.8125`.

The recovery branch did not trigger in that fresh 80-game panel or in the
larger 512-game public-opening scan. This proves fail-closed identity on fresh
non-matching games, not fresh generalization of the recovery branch. Its
positive evidence is limited to the seven historical matched tapes.

## Rejected changes

Several apparently strong aggregate improvements were rejected:

- blanket V5 rollback: 309 improved and 288 regressed margins across the 597
  games, losing 117 V9 known wins;
- late V5 splice: 2 improved and 25 regressed among 27 matches;
- market-formula parity: 13 improved and 6 regressed on the V8 corpus;
- three broader step-72 rules: each retained at least one regression, and the
  Pet Cafe rule also lost a known win;
- late multi-crop seed clipping: 329 improved but 4 regressed on the V7 corpus,
  including a known win moving from `+121` to `-105`;
- the first candidate gate: an absolute-seat indexing error hid two large
  seat-relative regressions, so the gate and its evidence were withdrawn;
- further terminal pruning: no remaining terminal purchase orders or stranded
  sellable inventory were found.

Exact hashes and counterexamples are in
[`evidence/v10-failure-analysis.json`](evidence/v10-failure-analysis.json).

## Delivery boundary

Code commit `5c1ffa466e8755857a87936e0a24b2d4461aa61b` was pushed to
`origin/main` before upload. The deterministic 122,013-byte archive has
SHA-256
`4b759b53b7e7ae81b7a1334208db82aacc8a0e1062546dab974843066648d8bb`.

Kaggle submission `55848408`, message
`v10 fail-closed opening recovery 5c1ffa4`, was recorded at
`2026-08-28T16:08:13.067Z` and observed `COMPLETE` at
`2026-08-28T16:10:25Z` with initial dynamic score `600.0`. `COMPLETE` proves
remote validation; it does not prove a final strength estimate. The `2600+`
target remains pending until a live snapshot actually reaches it.
