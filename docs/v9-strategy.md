# V9 strategy: fail-closed terminal inventory reconciliation

V9 keeps V8's public-shop selector, all ten route tapes, and the existing
recovery-aware execution controller. Its only policy change is a final-action
reconciliation: on step 718, sell any product that will actually be in the
shed after the same-turn unit actions but is not fully covered by the existing
SELL orders.

The change is deliberately narrower than another route revision. It does not
use identity, episode ID, submission ID, seed, opponent-private state, future
actions, or a replay lookup. Before step 718 it returns the existing action
unchanged.

## Remote snapshot and claim boundary

The Kaggle submission snapshot completed at `2026-08-27T10:25:18Z`:

| Submitted artifact | Submission | Status | Dynamic score |
|:---|---:|:---:|---:|
| V4 | 55569567 | COMPLETE | 2656.6 |
| V5 | 55574866 | COMPLETE | 2656.4 |
| V7 | 55638354 | COMPLETE | 2201.6 |
| V8 | 55719179 | COMPLETE | 1848.0 |

The public leaderboard archive at `2026-08-27T10:23:25Z` placed
`ziliangCok` at rank 256 of 6,569 with score `2201.6`. That row uses the
team's best active submission and is therefore not a V8-only score. Ratings,
ranks, opponent samples, and episode counts are dynamic.

The lower V8 snapshot motivated this audit, but it does not by itself prove
that the V8 selector caused the change. The V7 and V8 submissions saw
different opponent samples. All comparisons below first reproduce the
recorded policy exactly and then hold the opponent action tape fixed; they are
open-loop counterfactuals, not live rematches or leaderboard forecasts.

## Exact V8 public replay audit

The V8 corpus contains all 177 public episodes exposed by the API in the
snapshot: 108 wins, one tie, and 68 losses, spanning
`2026-08-23T16:04:50Z` through `2026-08-27T10:15:37Z`. Every replay uses
`kaggle-environments==1.32.7`, contains 720 states, and ends `DONE/DONE`.
The frozen V8 file reproduced the recorded actions, rewards, statuses, and
opponent tapes in all 177 games.

The audit found a deterministic execution defect rather than a crash:

- 32 games ended with 1,025 sellable units still present: 1,020 wool, three
  wheat, and two strawberry;
- 15 of the affected games were losses and stranded 542 wool;
- 17 were wins and stranded the remaining 483 units;
- current 8C/6S stranded stock in 22 of 22 games (861 units), current 6C/8S
  in eight of eight games (160 units), and two 10C/4S games held four units.

The missing sale was route-specific schedule drift: the static final SELL
quantities no longer matched the shed after recovery controls, animal events,
and same-turn deposits. This made terminal inventory a particularly narrow
target: the policy had no future decision after the affected action.

## Final-action reconciliation

After the existing seed pruning and executable-market ranking, V9:

1. projects the shed from the observed private shed plus the current farmer
   and hand PICKUP, DROP, and PLACE actions;
2. sums the quantity already requested by SELL orders for each sellable
   product;
3. leaves an already sufficient SELL unchanged;
4. tops up the first existing SELL when projected stock is larger, or appends
   one missing SELL while the ten-order market cap has room.

The helper never deletes an order or reduces a requested quantity. In the
captured production path, final market actions contain at most four orders,
so the append path remains below the schema limit. A unit test also fixes the
fail-closed behavior when a synthetic action already contains ten orders.

## Anti-regression gates

### Current V8 corpus

On all 177 calibrated V8 opponent tapes, the candidate changed only the final
action in the 32 deficit games:

| Policy | Wins | Ties | Losses | Mean margin |
|:---|---:|---:|---:|---:|
| frozen V8 | 108 | 1 | 68 | +2171.271 |
| V9 terminal reconciliation | 110 | 1 | 66 | +2431.096 |

V9 improved 32 rows, left 145 exactly unchanged, regressed zero, and retained
all 108 V8 wins. It flipped episodes `98672699` (`-3028` to `+10702`) and
`99646509` (`-234` to `+1013`). The 32 changed games gained a total of
`45,989` margin, and all nine sellable product counts across shed and unit
inventories were zero at terminal.

### V7 control corpus

To avoid repeating a route-development-only gate, V9 was also compared with
the exact frozen V7 policy on all 333 currently exposed V7 public episodes.
They contain 157 wins, three ties, and 173 losses; every baseline action,
reward, status, and opponent tape reproduced exactly. The V7 and V8 replay
episode IDs do not overlap.

The three-way decomposition separates the historical V8 routing change from
the V9 terminal change:

| Policy | Wins | Ties | Losses | Mean margin |
|:---|---:|---:|---:|---:|
| frozen V7 | 157 | 3 | 173 | -1876.255 |
| frozen V8 | 162 | 3 | 168 | -876.354 |
| V9 terminal reconciliation | 169 | 2 | 162 | -520.721 |

V8 versus V7 improved 18 rows, left 315 unchanged, regressed zero, retained
all 157 V7 wins, and flipped five non-wins. V9 versus V8 improved 68 rows,
left 265 unchanged, regressed zero, retained all 162 V8 wins, and flipped seven
more non-wins. End to end, V9 improved 85 rows, left 248 unchanged, and
retained every V7 win.

Of the 333 games, 133 were created after the V8 design snapshot and therefore
did not participate in the V8 route decision. On this time slice, V8 versus
V7 improved nine rows and regressed zero; V9 versus V8 improved 21, left 112
unchanged, regressed zero, retained all 17 V8 wins, and flipped episode
`99797162`. This does not turn the time slice into an unopened holdout, but it
directly checks the behavior on later online cases.

### Local runtime and packaging

The final local candidate uses `kaggle-environments==1.32.7`, passes 71 tests
and `python -m pip check`, and compiles/imports as a self-contained module.
Starter and random opponents from both seats each completed 720 states with
`DONE/DONE` and no stderr. The reviewed package contains only `main.py`,
`LICENSE-APACHE-2.0.txt`, and `THIRD_PARTY_NOTICES.txt`.

## Rejected and deferred changes

- Reverting the 69 V8 non-wins to V7 flipped no game, worsened two, and
  reduced mean margin by `166.696`; the online score gap was not sufficient
  evidence for a blanket rollback.
- V4 and V5 flipped eight and 11 of those non-wins, respectively, but
  regressed 30 and 20 rows. They failed the zero-regression rule.
- A simple second-Yarn guard sees the deciding shop only after the candidate
  tapes have already diverged. A local check lost `21,323` margin, so a future
  version would need a shared-prefix route rather than a late tape switch.
- The official Carrot, Tomato, and Egg scarcity functions are hinge-shaped,
  while the current ranking approximation is not. Correcting that is broader
  than terminal reconciliation and may reorder SELL actions globally; it is
  deferred to an independently gated change.
- The repeated 8C/6S late cow escape suggests a separate wheat-reserve
  recovery experiment. It must first preserve the ten current 8C/6S wins in
  the targeted corpus and is not bundled into V9.

## Delivery state

V9 is a verified local candidate only. It has not been committed, pushed, or
uploaded to Kaggle. The latest remote delivery remains V8 submission
`55719179`, while V7 remains a separate submitted control. A future upload
requires an explicitly authorized commit-and-push delivery cycle and remote
validation before it can be called submitted or scored.

Exact source hashes, corpus manifests, result hashes, time-slice results, and
package evidence are in
[`docs/evidence/v9-failure-analysis.json`](evidence/v9-failure-analysis.json).
