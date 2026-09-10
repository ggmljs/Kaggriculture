# AGENTS.md

These instructions apply to the entire repository.

## Project Mission

Build, test, and submit reliable autonomous agents for the Kaggle
Kaggriculture simulation. The first milestone is a deterministic baseline that
completes a 720-turn local episode, produces a replay, and passes Kaggle's
submission validation.

## Repository Map

- `main.py`: Kaggle submission entrypoint. It must expose `agent(obs)` and stay
  self-contained unless the submission archive explicitly includes helpers.
- `scripts/`: local evaluation and packaging utilities.
- `tests/`: deterministic unit and environment smoke tests.
- `assets/`: README and project branding assets only.
- `replays/`, `logs/`, `runs/`, `data/`, `datasets/`: local-only generated or
  downloaded artifacts; never commit them.

## Runtime and Development Rules

- Use the CPython version recorded in `.python-version` and a repository-local
  `.venv`.
- Treat `requirements.txt` and `requirements-dev.txt` as the portable top-level
  dependency inputs. `requirements.lock` is the exact development snapshot for
  the Python, operating system, and architecture documented in its header.
- Do not treat `requirements.lock` as cross-platform. It intentionally excludes
  `pip`, `setuptools`, and `wheel`; recreate it from a clean matching environment
  when a top-level dependency changes, then run `python -m pip check` and the
  applicable tests.
- Keep the submission policy deterministic and lightweight enough for Kaggle's
  per-turn execution limit.
- Treat observations as untrusted mappings: use defensive lookups where doing
  so does not hide schema errors.
- Return only actions accepted by the current Kaggriculture action schema.
- Invalid actions are often silent no-ops; add tests for position, tile state,
  inventory, seeds, and end-of-season liquidation logic.
- Do not depend on network access, local absolute paths, environment secrets,
  or files outside the submission bundle.
- Keep credentials outside the repository. Never print, copy, stage, or commit
  Kaggle or GitHub tokens.
- Keep README commands runnable from the repository root and update README
  evidence whenever the verified runtime or submission state changes.

## Documentation Rules

- `README.md` must describe only the currently promoted agent strategy, its
  current verification evidence, and its current Kaggle delivery.
- Do not retain superseded strategy descriptions, prior submission tables, or
  version-to-version evolution narratives in `README.md`.
- Record the chronological strategy evolution only in the `Strategy Evolution
  Log` section of this file. When a new strategy is promoted, replace the
  strategy and delivery content in `README.md` and append one concise history
  entry here in the same documentation change.
- Keep detailed reproducibility evidence in `docs/` when needed; the evolution
  log should summarize and link to evidence rather than duplicate raw results.

## Strategy Evolution Log

### V1: deterministic carrot baseline — 2026-08-05

- Used the north-west quadrant as a carrot field, hired four hands daily,
  assigned units by row, replenished seeds, and liquidated at the end.
- Established the first complete 720-state local, packaging, Kaggle validation,
  and public-GitHub delivery path.
- Kaggle submission `55268182`, message `baseline-v1 deterministic carrot
  planner`, reached `COMPLETE`; code commit `ec8bdba50701653e4c3b884cce65897e6fc68f3e`,
  archive SHA-256
  `d3781fb452c1ec3c85579c9c22f8dac860c307c3d4b57701eaef796c58d9f448`.
- Its public score was observed at 471.3 on `2026-08-05T11:25:21Z`; simulation
  ratings are dynamic, so this is only a historical snapshot.

### V2: market-aware mixed farm — 2026-08-06

- Replaced the single-crop planner with a three-quadrant wheat, melon,
  strawberry, cow, and sheep supply chain.
- Added worker alignment, actor-local weed recovery, projected-stock sell
  clipping, sustained mirror detection, premium-sale front-running,
  collision-aware order sorting, and step-718 liquidation.
- Frozen holdout evidence: 38 wins in 40 both-seat games, all 720 states and
  `DONE/DONE`, with a positive mean margin against every evaluated public
  policy artifact. See `docs/evidence/v2-holdout.json`.
- Kaggle submission `55292510`, message `v2 market-aware mixed-farm route
  c587ec5`, reached `COMPLETE`; code commit
  `c587ec54eb5e46e560f21797507b1e759ba7ccf6`, archive SHA-256
  `3967ea31aa2da69e0be8b5af0dc07b70d9f5f5384c3f8a1ae74ffa12173ca3ef`.
- Its public score was observed at 1,531.5 on `2026-08-13T13:26Z`; simulation
  ratings are dynamic, so this is only a historical snapshot.

### V3A: observable-state execution control — 2026-08-13

- Preserved the V2 production route while adding actor-ordered field and shed
  shadow execution, atomic-plant repair, conservative market-flow inference,
  evidence-gated H1–H5 premium-sale timing, and capacity-safe terminal recovery.
- Final local candidate SHA-256
  `541d6a13e6d10ca61c00ffe5c46fd3722ea29f22b5b8ea8de6dd550f8f61a001`
  passed 40 automated tests, both required 720-state smoke matches, and
  deterministic three-file archive verification.
- In a fixed four-seed, both-seat paired diagnostic, it improved the margin in
  all 8 games against Kaito v27 and all 8 against Breaking Tie, but still lost
  every game; this is an execution-hardening result, not evidence of a large
  leaderboard gain. The V3A evidence was superseded by the V3B evidence file.
- V3A has not been uploaded to Kaggle or committed to GitHub. The current remote
  delivery remains V2 until a later explicitly authorized delivery cycle.

### V3B: adaptive 8C/4S market counter — 2026-08-13

- Replaced the V2/V3A economic tape with an 8-cow/4-sheep route reconstructed
  by majority vote from three public episodes, while retaining bounded weed and
  cow-placement recovery.
- Extended quantity-conserving one-turn sale leads to all scheduled products
  and added an evidence-gated second-order premium counter for observed H4
  market opponents.
- The frozen `main.py` candidate SHA-256
  `257d74f613f80607fba6fa68482e9db1eb07cb98618add47d45415b4f9079f54`
  swept 80/80 local games against four hash-pinned public strong artifacts,
  using unseen deterministic seeds, both seats, 720 states, and `DONE/DONE`.
  See `docs/v3b-strategy.md` and `docs/evidence/v3b-strong-holdout.json`.
- This is a fixed local artifact-panel result, not proof against future or
  hidden opponents and not a Kaggle score.
- Kaggle submission `55484203`, message
  `v3b adaptive 8c4s market counter 9bd601c`, reached `COMPLETE`; the uploaded
  `main.py` maps to Git commit
  `9bd601cb60150192986313049ce2a609644243e1`, and the archive SHA-256 is
  `b60f48ab876480c850821398ea52486ffc7e7da1a67faba657cbd665de1d67e0`.
- Its initial public score was observed at 600.0 on `2026-08-13T13:30Z`;
  simulation ratings are dynamic, so this is only a delivery snapshot.

### V3C: failure-driven execution and H7 repayment — 2026-08-14

- Reproduced all 17 captured V3B online losses exactly with engine `1.32.6`,
  then separated production-route deficits, market mirrors, and a cash-starved
  partial-purchase cascade. See `docs/v3c-strategy.md` and
  `docs/evidence/v3c-failure-analysis.json`.
- Kept the 8C/4S route; added first-day seed-surplus clipping, observable cow
  purchase reconciliation, a tightly gated ninth cow, and a seven-turn premium
  prepayment whose exact quantity is excluded from H1 and removed from the
  original sale.
- The final local `main.py` SHA-256 is
  `d9e26d7e45a944dd4e46adc28f66f7d9ae5c6974e71755debe6b291029aa79e0`.
  On fixed opponent tapes it improved 9 of 17 historical losses, left 8
  unchanged, regressed none, and flipped 3; this is an open-loop diagnostic,
  not a policy rematch.
- A final-hash fresh closed-loop holdout swept 64/64 both-seat games against
  four hash-pinned public artifacts, all 720 states and `DONE/DONE`, with a
  minimum margin of +116. The seeds do not overlap the V3B holdout.
- Kaggle submission `55500863`, message
  `v3c failure-driven h7 recovery 6aadc96`, reached `COMPLETE`; the uploaded
  `main.py` maps to Git commit
  `6aadc968f3cb0e81839532ff7f1ec0499b061f81`, and the archive SHA-256 is
  `90c800d2d51705a8662ed5d33d60f2953180f192f8091f2ab20d4886b29d13ef`.
- Its initial public score was observed at 600.0 on `2026-08-14T07:54:14Z`.
  The later official snapshot at `2026-08-17T02:36:22Z` showed 2,444.7 at
  rank 371/4,818; simulation ratings and ranks are dynamic.

### V4: public-demand-routed two-expert policy — 2026-08-17

- Reproduced all 111 captured V3C public losses exactly with their recorded
  engine versions, then reconstructed public-behavior majority routes for a
  low 10C/4S expert and a high expert that requests and places 6C/12S
  cumulatively but finishes at a stable 6C/8S herd.
- Added a per-seat, sticky step-168 selector over public unlocked shops:
  observed yarn demand chooses the high expert except for the exact early
  `ICE_CREAM_SHOP`, `YARN_STORE` dominated prefix; no identity, episode, or
  seed routing is used.
- Final local `main.py` SHA-256
  `ff50c792a8e2dbe23c8b9855cfe63074885a22ea381883af463012513a956f70`
  passed 40 tests and low/high 720-state `DONE/DONE` smokes. On fixed opponent
  tapes it won 97/111 captured losses, but that is open-loop counterfactual
  evidence rather than a policy rematch.
- A pre-frozen 32-game public-win control retained only 27 wins, so its strict
  preservation gate failed. The opened 128-row development panel and 80-game
  legacy panel evaluated pre-final hash `38838d46…`, not the final candidate.
- A final-hash fresh closed-loop paired panel produced 101/128 V4 wins versus
  45/128 for V3C and improved mean margin by 8,762.203, but failed the all-wins
  and positive-mean-versus-every-opponent gates. See `docs/v4-strategy.md` and
  `docs/evidence/v4-failure-analysis.json` for hashes and claim limits.
- Kaggle submission `55569567`, message
  `v4 demand-routed mixed farm ea61ae0`, reached `COMPLETE`; the uploaded
  `main.py` maps to Git commit
  `ea61ae044eb481b145ca9741df552e7dd1f0b422`, and the 31,624-byte archive
  SHA-256 is
  `796b1b29abf0b53186b3e3c56a6c19bbb5d47d06e6e98533c05531a11a634a8c`.
- Its initial public score was 600.0 at `2026-08-17T03:35:34Z`; this is a
  dynamic starting snapshot, not a strength estimate or final rank.

### V5: recovery-aware execution and executable-market ranking — 2026-08-17

- Kept the V4 public-shop two-expert selector and added failure-driven fixes:
  day-boundary clearing for in-flight weed transactions, route-prefix seed
  feasibility with atomic same-crop planting semantics, executable same-turn
  shed projection for SELL ranking, terminal wheat-seed pruning, and retry-safe
  per-seat action caching.
- Current `main.py` SHA-256 is
  `9390f7a9136f7c724376107fa3b2f464d871b0d725ac2039503c1cc312f6bc5b` and the
  repository has 56 passing tests. Starter/random both-seat terminal smokes
  completed 720 states with `DONE/DONE` and no stderr.
- The current-hash opened 16-seed, four-opponent, both-seat regression panel
  completed 128/128 wins, mean margin `+6321.125`, and worst margin `+181`.
  The separate RC1 diagnostic panel was 123/128; its five near-mirror losses
  remain an explicit evidence boundary rather than an identity/seed gate.
- Detailed current strategy and raw result hashes are in
  `docs/v5-strategy.md` and `docs/evidence/v5-failure-analysis.json`.
- Kaggle submission `55574866`, message `v5 recovery-aware executable-market
  controller cd5e81b`, reached `COMPLETE`; the uploaded `main.py` maps to Git
  commit `cd5e81b1cc9d6ef38422aa5d47c7f76e64c866fc`, and the reviewed archive
  SHA-256 is
  `9baa7fd9783bab1391fa7293497a174abf5772e0e0beae2b8259aabf9447f1b1`.
- Its initial public score was `600.0` at `2026-08-17T08:58:58Z`; leaderboard
  ratings are dynamic and this is only a delivery snapshot.

### V6: observable behavior-routed counter expert — 2026-08-18

- Retrieved the real V5 public score of `2735.4` and evaluated 97 captured
  public games under engine `1.32.7`: V5 won 73/97, with all 24 losses reaching
  `DONE/DONE`; the repeated weakness was later market cadence rather than
  crashes or invalid termination.
- Kept V5 as the default and added a third public-replay majority route behind
  a conservative step-72 public-state gate: exact opponent `$49`, zero hands,
  2 cows, 2 sheep, 12 melon, 7 wheat, 5 pasture, and first shop `BAKERY` or
  `PIZZA_SHOP`. A repeated first-two-shop prefix falls back to V5.
- The evaluated candidate improved the public panel to 78/97 wins and retained
  all 73 historical win outcomes. It swept the available three-opponent
  16-seed both-seat panel 96/96, then reached 47/48 on a fresh 8-seed panel;
  the lone `-448` row was also V5's only loss on that panel.
- The current repository `main.py` SHA-256 is
  `888115e1a4c48a52f28eeac60ce6fb8ede5dd67db360fee5df004ffa0613885e`.
  Detailed hashes, seeds, results, and claim limits are in
  `docs/v6-strategy.md` and `docs/evidence/v6-failure-analysis.json`.
- Kaggle submission `55596752`, message `v6 behavior-routed counter 2ba26b7`,
  reached `COMPLETE`; the uploaded `main.py` maps to Git commit
  `2ba26b7ff3bc6df55000625df248c91f531c00d3`, and the 44,336-byte archive
  SHA-256 is
  `e9dbd91bcd7b3ce1d98d29ed7e331d43432e9c3fef450797d5996d5fd063b64f`.
- Its initial public score was `600.0` at `2026-08-18T08:50:00.573Z`.
  Immediately before upload, V5's dynamic score was `2730.6`; ratings change
  as episodes run. V6 was later observed at `909.1` on
  `2026-08-18T09:06:26Z`; these are delivery snapshots rather than strength
  estimates.

### V7: public-shop five-route controller — 2026-08-20

- Pulled the latest V6 remote snapshot (`2416.6` at
  `2026-08-20T04:01:34Z`) and analyzed 126 captured public games: V6 won 75
  and lost 51, with all games reaching `DONE/DONE`. The dominant failure
  clusters were late market cadence plus strawberry, wool, wheat, and milk
  revenue deficits. These are dynamic online snapshots and replay diagnostics,
  not fixed leaderboard strength claims.
- Replaced the single V6 public-state counter choice with five observable
  current routes: first-shop Yarn selects first-Yarn 6C/12S, second-shop Yarn
  selects second-Yarn 6C/12S, third-shop Yarn selects 6C/8S, an early
  milk-support pattern selects 10C/4S, and otherwise 8C/6S. A step-24–71
  observable legacy-opening gate selects matching legacy tapes. No identity,
  episode, submission, or seed routing is used.
- Retained V6 execution controls for seed feasibility, day-boundary weed
  recovery, cow reconciliation, bounded premium repayment, executable SELL
  ranking, terminal seed pruning, retry-safe action caching, and malformed
  observation protection. Route data are modified, normalized, compressed
  derivatives of the Apache-2.0 artifact documented in
  `THIRD_PARTY_NOTICES.md`.
- Frozen V7 `main.py` SHA-256 is
  `7ce060d8551cf3e7a20a800c1eea2e18ece63d6d6eab8e21199b65f9b78e4794`.
  The repository has 61 passing tests; starter and random both-seat smokes
  each complete 720 states with `DONE/DONE` and no stderr.
- On the fixed 126-game public replay tape, V7 scored 99/126, mean margin
  `+7401.508`, improving 72 and regressing 54; this is open-loop
  counterfactual evidence. A fresh closed-loop 64-game panel against four
  hash-pinned artifacts scored 56/64, with per-opponent positive mean margins
  and all 64 episodes at 720 states and `DONE/DONE`. A pre-final behavior
  candidate scored 65/96 on an older panel versus V6's 96/96; it was not
  rerun after unused constants were removed and is retained as an explicit
  pre-final regression boundary. See `docs/v7-strategy.md` and
  `docs/evidence/v7-failure-analysis.json`.
- The reviewed 99,523-byte archive has SHA-256
  `03c99a672bee741591d7224781865efd20cb3a26ea775193eadade4ac28f5c4a`.
  Kaggle submission `55638354`, message `v7 public-shop five-route 77c271f`,
  reached `COMPLETE`; the uploaded `main.py` maps to public Git commit
  `77c271f600b09b2dc070bc6b406240356bcb5616`. Kaggle recorded it at
  `2026-08-20T04:56:38.653Z`; validation was observed complete at
  `2026-08-20T05:02:19Z` with an initial dynamic public score of `600.0`. V7
  was later observed at `681.7` on `2026-08-20T05:05:16Z`.

### V8: divergence-gated third-Yarn milk routing — 2026-08-24

- Pulled the latest V7 remote snapshot at `2026-08-23T15:45:18Z`: submission
  `55638354` remained `COMPLETE` at dynamic score `2626.4`, while the
  leaderboard placed `ziliangCok` at rank 53/6,021. Retrieved all 200 public
  episodes: 140 wins, 59 losses, and one tie, all terminal `DONE/DONE`.
- The dominant deep-loss route was current 6C/8S: 15 losses with mean margin
  `-11790.067` and worst margin `-35604`. The repeated actionable subcluster
  was third-shop Yarn after an earlier milk-support shop, where V7's Yarn
  priority suppressed the existing 10C/4S milk expert.
- Kept all ten V7 tapes and execution controls. For current, non-legacy
  third-Yarn plus first-two milk support only, V8 computes an L1 distance over
  the two public farms' cow, sheep, wheat, melon, strawberry, and empty-pasture
  counts. Distance at least three selects 10C/4S; otherwise 6C/8S remains.
  The decision is sticky, per-seat, reset-safe, and uses no identity, episode,
  submission, seed, private inventory, or future-action feature.
- Frozen `main.py` SHA-256 is
  `faf57412e2c56dcc669043865a185324bab9952d865abccc2203284e854eceb3`.
  The repository has 66 passing tests. Starter and random both-seat smokes each
  completed 720 states with `DONE/DONE` and no stderr.
- A calibrated 200-game fixed-opponent-tape gate retained all 140 V7 wins,
  improved nine rows, regressed zero, and flipped five losses. V8 scored
  145 wins, one tie, and 54 losses with mean margin `+4058.725`, versus V7's
  140/1/59 and `+3236.640`. This is open-loop counterfactual evidence.
- A final-hash targeted closed-loop panel improved from V7's 56/88 to V8's
  84/88, with 28 improved and 60 identical rows, zero regressions, and all
  games cleanly terminal. A separate fresh six-opponent, eight-seed, both-seat
  panel was margin-identical to V7 on all 96 rows at 82/96 wins, with a
  positive mean versus every opponent. See `docs/v8-strategy.md` and
  `docs/evidence/v8-failure-analysis.json` for hashes, seeds, and claim limits.
- Kaggle submission `55719179`, message
  `v8 divergence-gated third-yarn milk 779caae`, reached `COMPLETE`; the
  uploaded `main.py` maps to public Git commit
  `779caaec88a441345871e2d62eb5de93606b7b52`. The reviewed 99,945-byte
  archive SHA-256 is
  `5c410ffb2a3637ce8840274c7eab70813c270209cbcbb79e735eb2c547a4b35d`.
  Kaggle recorded it at `2026-08-23T15:57:38.490Z`; validation was observed at
  `2026-08-23T16:02:22Z` with initial dynamic score `600.0`. V7 remained
  `COMPLETE / 2626.4` at that observation, so the prior remote baseline was not
  overwritten while V8 began its own dynamic rating trajectory.

### V9: fail-closed terminal inventory reconciliation — 2026-08-27

- Pulled the current remote snapshot at `2026-08-27T10:25:18Z`: V8 submission
  `55719179` remained `COMPLETE` at dynamic score `1848.0`, while V7 was
  `COMPLETE / 2201.6`. The `2026-08-27T10:23:25Z` public leaderboard placed
  `ziliangCok` at rank 256/6,569 using the team's best score. These are dynamic
  observations and do not causally identify the V8 selector as the decline.
- Retrieved and exactly calibrated all 177 exposed V8 public episodes: 108
  wins, one tie, and 68 losses, all 720 states and `DONE/DONE` under engine
  `1.32.7`. Thirty-two games stranded 1,025 sellable terminal units, dominated
  by 1,020 wool; this was route-schedule drift, not a crash.
- Kept all V8 routes and selectors. On step 718 only, V9 projects the shed after
  same-turn unit actions and tops up or appends SELL orders when actual stock
  exceeds the existing requested quantity. It never removes or reduces an
  order and remains within the ten-order schema cap.
- On the calibrated 177-game V8 tapes, V9 improved 32 rows, left 145 unchanged,
  regressed zero, retained all 108 wins, and flipped two losses, moving to
  110/1/66 with mean-margin delta `+259.825`. The 32 changed games finished
  with zero sellable stock across shed and unit inventories.
- A second 333-game V7 control corpus calibrated exactly at 157/3/173. V9
  improved 85, left 248 unchanged, regressed zero, retained all 157 V7 wins,
  and flipped 12 non-wins. The three-way decomposition found zero regressions
  both for V8 versus V7 (18 improved) and for V9 versus V8 (68 improved). The
  133-game post-V8-design time slice also had zero regression. These are
  fixed-opponent-action counterfactuals, not live rematches or leaderboard
  forecasts.
- Final local `main.py` SHA-256 is
  `dc4ee0a23285ef9f1dd2ba9b9b8f39feb434e363859b60f82d3f793505edb88f`.
  The repository has 71 passing tests; starter and random both-seat smokes each
  reached 720 states and `DONE/DONE`. The reviewed 100,234-byte local archive
  SHA-256 is
  `0a188e825eada95009902566432246f07667688c2280578a81864c73f37c3735`.
  See `docs/v9-strategy.md` and
  `docs/evidence/v9-failure-analysis.json` for exact manifests and limits.
- Code commit `3f918431de637717b6a43b00a099eea662811243` was pushed to
  `origin/main` before upload. Kaggle submission `55817164`, message
  `v9 fail-closed terminal liquidation 3f91843`, reached `COMPLETE`; the
  reviewed archive SHA-256 is
  `0a188e825eada95009902566432246f07667688c2280578a81864c73f37c3735`.
  Kaggle recorded it at `2026-08-27T11:31:53.823Z`; validation was observed at
  `2026-08-27T11:36:45Z` with initial dynamic public score `600.0`. This is a
  delivery snapshot, not a strength estimate or final rank.

### V10: fail-closed opening recovery — 2026-08-29 (current)

- Pulled the pre-V10 submission snapshot at `2026-08-28T15:54:29Z`: V8 was
  `COMPLETE / 1809.5`, V9 was `COMPLETE / 1677.2`, and the historically
  stronger V4/V5 submissions still displayed `2656.6 / 2656.4` but no longer
  occupied either active simulation slot. The decline audit separated active
  slot replacement, replay-derived route specialization, margin-versus-win
  objective mismatch, and dynamic-opponent confounding.
- Retrieved 90 exposed V9 public episodes, including three that appeared only
  after the V10 gate was frozen. V9 reproduced all recorded actions, all games
  reached 720 states and `DONE/DONE`, and terminal sellable stock remained
  reconciled. The online decline was not a recurrence of V9's terminal bug.
- Kept V9 as the default. At step 72 only, a finite seat-relative gate selects
  the frozen V5 recovery route when the first shop is Bakery/Pizza, the
  opponent public farm is exactly 1C/4S/5W/4–5M, and our public cash trails.
  Missing, malformed, late, or mismatched features close the gate. The route
  decision is sticky, per-seat, retry-safe, and uses no identity, episode,
  submission, seed, opponent-private state, replay lookup, or future actions.
- The final `main.py` SHA-256 is
  `56831f3c43c9727d90016b7a7a8d4eb51d1a4c08c1120d58f061d9176e8bc109`.
  Across the final-hash V7/V8/V9 corpora, V10 improved 7 of 597 games, left
  590 identical, regressed zero, preserved all 336 V9 known wins, and moved
  from 336/3/258 to 339/3/255. All games were 720-state `DONE/DONE` with empty
  stderr. These are fixed-opponent-action counterfactuals, not live rematches.
- The three post-freeze public episodes were action- and margin-identical to
  V9. A fresh five-opponent, eight-seed, both-seat closed-loop panel was also
  identical on all 80 games at 68/80 wins. Neither fresh set triggered the
  gate, so it proves fail-closed identity rather than fresh recovery-branch
  generalization. See `docs/v10-strategy.md` and
  `docs/evidence/v10-failure-analysis.json` for exact hashes and boundaries.
- Rejected aggregate-positive candidates that violated the strict gate: a
  blanket V5 rollback regressed 288/597 and lost 117 V9 wins; late seed
  clipping improved 329/333 but regressed four and lost a known win; broader
  step-72 rules and market-formula changes each retained per-game regressions.
  An earlier absolute-seat audit error hid two regressions and its candidate
  evidence was withdrawn before release.
- The repository has 77 passing tests. Starter and random both-seat smokes
  reached 720 states and `DONE/DONE`; `pip check`, archive compile/import, and
  deterministic rebuild checks passed. The reviewed 122,013-byte archive
  SHA-256 is
  `4b759b53b7e7ae81b7a1334208db82aacc8a0e1062546dab974843066648d8bb`.
- Code commit `5c1ffa466e8755857a87936e0a24b2d4461aa61b` was pushed to
  `origin/main` before upload. Kaggle submission `55848408`, message
  `v10 fail-closed opening recovery 5c1ffa4`, reached `COMPLETE`; Kaggle
  recorded it at `2026-08-28T16:08:13.067Z`, and validation was observed at
  `2026-08-28T16:10:25Z` with initial dynamic score `600.0`. The `2600+`
  target has not yet been observed and remains a live-rating objective.

## Verification Gates

Before treating a baseline change as complete, run all applicable checks:

1. `python -m pip check`
2. `python -m pytest -q`
3. `python scripts/run_local_match.py --opponent starter --seed 20260805`
4. `python scripts/run_local_match.py --opponent random --seed 20260805`
5. `python scripts/package_submission.py`
6. Import and syntax checks for every file included in the submission.

For documentation changes, check formatting, links, and example commands. If an
applicable check cannot be run, record the reason in the commit body, pull
request description, or delivery note.

The full 720-turn episode must end with both agents in a terminal status. A
Kaggle upload is only "submitted" until the remote submission status confirms
validation; a local win or successful upload is not evidence of a scored bot.

## Kaggle Submission Rules

- `main.py` must be at the submission root and expose `agent(obs)`.
- Keep the archive below the competition's 100 MiB submission limit.
- Review the exact archive contents before upload.
- Do not include replays, datasets, logs, caches, credentials, or the virtual
  environment.
- Use descriptive submission messages such as `baseline-v1 deterministic
  carrot planner`.
- Record the submission ID, timestamp, message, and remote status in the
  delivery evidence, but do not fabricate a score or validation result.
- Every code revision submitted to Kaggle must also be committed and pushed to
  GitHub in the same delivery cycle. Record the Kaggle submission ID together
  with the corresponding Git commit SHA so the uploaded `main.py` is traceable
  to the public repository.

## Git Rules

The rules below are adapted from
[`COK-ZhangZiliang/Git-Rules`](https://github.com/COK-ZhangZiliang/Git-Rules/blob/ae0e80bb4a18a40c60ca514f0ce9d8f2a4c338af/README.md)
at commit `ae0e80bb4a18a40c60ca514f0ce9d8f2a4c338af`.

- Create commits only when explicitly requested by the user or maintainer.
- Each commit must contain one logical, testable change. Split unrelated
  features, fixes, refactors, tests, and documentation changes.
- Do not bypass checks with `--no-verify` and do not rewrite shared history.
- Prefer topic branches such as `codex/<topic>`, `feature/<topic>`,
  `fix/<topic>`, or `docs/<topic>`, with an English kebab-case topic.
- Use Conventional Commits: `<type>(<scope>): <subject>`, or omit the scope for
  repository-wide changes.
- Recommended common types are `feat`, `fix`, `refactor`, `test`, `docs`, `chore`,
  and `perf`.
- Write the subject in English, imperative mood, lowercase, without a trailing
  period, and at most 72 characters when practical.
- Behavioral, schema, data-format, or compatibility-sensitive commits need a
  body covering motivation, implementation, impact, verification, and
  rollback.
- Stage files by explicit path. Never use `git add -A` or `git add .`.
- Before committing, inspect `git status --short` and `git diff --cached`, then
  run verification matching the change scope.
- Never stage credentials, `.env` files, caches, local experiment outputs,
  model weights, datasets, or large generated artifacts.
- Before the first commit, inspect repository-local author configuration. If
  either value is absent, use only the repository-local fallback:

  ```bash
  git config --local user.name "ziliang"
  git config --local user.email "ziliangzhangcok@gmail.com"
  ```

- Do not change global Git identity unless explicitly requested.
- Push user-requested commits to the verified remote unless the user asks to
  keep them local. Do not push when no remote is available. Confirm the branch
  and remote before pushing.
- Pull request descriptions, when requested, must cover background, solution,
  compatibility or data impact, test results, safety/privacy/cost impact, and
  rollback.
- Keep pull requests focused; do not combine unrelated topics in one pull
  request.

### V11: fail-closed market-curve adaptation — 2026-09-08

- Preserved V10's official-default actions while accepting only complete, public, valid custom market curves for SELL-order ranking; malformed or absent curves fail closed to V10 defaults.
- Added an open-loop, both-seat replay regression gate for future candidate screening. It is a regression screen, not a live-score forecast.

### V16: leader-aware conservative market queue — 2026-09-09

- Rejected the initial interpretation of unsupported cross-product
  `BUY_PRODUCT` requests after interpreter inspection and frame-by-frame state
  differences proved they are silent no-ops. The promoted queue therefore
  front-loads executable sales but leaves legal restocking in place and never
  inserts unsupported padding by default.
- Added a fail-closed, public-tile opening profile that redirects the vulnerable
  10C/4S route against the cow-heavy leader layout unless early Pizza demand
  supports milk. Malformed rows now return no match rather than raising.
- The final `main.py` SHA-256 is
  `e3df9435cffe67a75ae908a1c888240b30546e4a1a86cba62904fe34e2cb4f2f`.
  Eighty tests passed; starter and random smokes reached 720 states and
  `DONE/DONE`. A 40-game five-opponent closed-loop panel was clean, and 12
  both-seat top-six replay comparisons had zero margin regression. See
  `docs/v16-strategy.md` for evidence boundaries.
- Code commit `85aae5c042b23d9da45a0f5c4a57e6b2e24c2016` was pushed to
  `origin/main` before upload. Kaggle submission `56103627`, message
  `v16 leader-aware conservative queue 85aae5c`, reached `COMPLETE`. The
  125,637-byte archive SHA-256 is
  `78ecfb3e3938117bdad1109eccc0a3f47f5666178c22889b2126b7cb2decc289`;
  its initial dynamic score was `600.0`.

### V17: safe residual KNN policy — 2026-09-09

- Kept V16 as the default controller and added a deterministic, at-most-once,
  SELL-only residual restricted to day 16 or day 27. The residual uses `k=5`,
  `beta=1.0`, a positive advantage threshold, and 384 embedded round-2/3
  counterfactual records; it does not change farmer, hand, or purchase actions.
- The final self-contained `main.py` SHA-256 is
  `4b9745ebc26f51b776598ad4326d8ce9b8fdb1c9ea789724db98fb91fd404042`.
  Eighty tests passed; starter and random smokes reached 720 states and
  `DONE/DONE`. The combined frozen comparison covered 100 seeds and 200 games,
  with mean paired margin `+112.405` and confidence interval
  `[+34.99, +218.42]` versus V16. This is local evidence, not a leaderboard
  guarantee.
- Code commit `1277bdba4440edffdb062519c7ecd66a9a937243` was pushed to
  `origin/feature/safe-residual-knn` before upload. Kaggle submission `56126261`,
  message `v17 safe residual knn 1277bdb`, reached `COMPLETE`; the 135,892-byte
  archive SHA-256 is
  `c285227a85f0a2f91468e924720b72bc51107222031089af25d30aaea820977a`.
  Its initial dynamic score was `600.0`.
### V18: online-safe residual KNN policy — 2026-09-10 (current)

- Used V17 public outcomes to identify a reproducible day-27 regression caused
  by rebuilding the sell list and evicting a baseline FERTILIZER order. The
  safe liquidation shield now preserves and tops up baseline sales, and uses
  only free order slots for additional high-value inventory.
- Collected a new 24-seed, both-seat counterfactual round under the corrected
  action semantics, excluded incompatible legacy liquidation labels, and
  retrained the gate on 480 compatible rows. Leave-one-seed-out selection plus
  the public-action-tape safety constraint retained `k=5`, `beta=0.5`, and
  threshold `150`; repeated initial BAKERY shops fail closed to V16.
- Final `main.py` SHA-256 is
  `71246b225b6ab2cd7ce1bd9ae0f26a0a62972226fa4addb7dc4b7130a250b94b`.
  A fresh 60-seed, 120-game both-seat panel had mean margin `+58.958` and paired
  bootstrap 95% interval `[+19.258, +103.142]`. Sixteen public-opponent tape
  comparisons had zero regression. These are local diagnostics, not a live
  leaderboard guarantee.
- Code commit `467d26d881c6d0232c46152f5c09d3ad2d24fc56` was pushed to
  `origin/feature/v18-online-safe-residual` before upload. Kaggle submission
  `56128972`, message `v18 online-safe residual knn 467d26d`, reached
  `COMPLETE`; the 139,406-byte archive SHA-256 is
  `c0b00b1ed1f5e430e183bf8ae4beb7aa71e2bd49b841372233a47450a66eddf9`.
  Its initial dynamic score was `600.0`.
### V29: official-strong production reset — 2026-09-10 (current)

- Rejected V19 after a wider official-replay gate exposed severe route
  overfitting, then evaluated the six V18 route families against four public
  episodes per available top leaderboard team in both seats. The old families
  won only 17/80 rows with mean margin `-12,520.5625`.
- Reconstructed four consistent 8-cow/6-sheep/3-goose production routes from
  public `cooked` episodes and selected episode `107301740` in a route league.
  V29 uses that complete route as the default without runtime identity, replay,
  episode, seed, or future-action lookup.
- On the same official 80-row gate V29 won 35, improved 60 paired rows, and
  raised mean margin to `-1,189.05`; the paired mean delta was `+11,331.5125`.
  It beat several leading teams on mean margin but remained 0/8 with mean
  `-39,784.625` against Otter Vibe, an explicit unresolved weakness.
- A fresh twelve-seed both-seat closed-loop league swept V18 24/24 at mean
  margin `+18,323.292`; all games reached 720 states and `DONE/DONE` with empty
  stderr. See `docs/v29-strategy.md` and
  `docs/evidence/v29-official-strong-gate.json` for scope and claim limits.
- Frozen `main.py` SHA-256 is
  `68c81d9efbd27807340ad575a4e92d12aff151561185be22823ebd5ebf1597eb`.
  Eighty-one tests passed; starter and random smokes reached 720 states and
  `DONE/DONE`. The reproducible 181,451-byte archive SHA-256 is
  `b9caf78699c65cd4c4e69bd14d6c8ae09e7285eb1c0af8ec36e71dd020b4843c`.
- Code commit `d95fc6b590a466cf1622326872681f9053e25772` was pushed to
  `origin/feature/v29-official-strong-default` before upload. Kaggle submission
  `56137699`, message `v29 official-strong default d95fc6b`, reached
  `COMPLETE`; its initial dynamic score was `600.0`.
