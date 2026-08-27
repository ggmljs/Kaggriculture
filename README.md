<div align="center">
  <img src="assets/logo.svg" width="100%" alt="Kaggriculture autonomous farming agent" />

  <br />

  [![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
  [![Kaggle Environment](https://img.shields.io/badge/Kaggle-Environment-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com/competitions/kaggriculture)
  [![Tests](https://img.shields.io/badge/tests-71%20passing-2ea44f?logo=pytest&logoColor=white)](#-verified-current-strategy)
  [![Submission status](https://img.shields.io/badge/V8%20submission-COMPLETE-2ea44f?logo=kaggle&logoColor=white)](#-submission)
  [![Policy](https://img.shields.io/badge/policy-V9%20terminal--reconciled-7B61FF)](#-strategy)

  **A deterministic public-demand-routed farm agent for Kaggle's 720-state economic simulation.**
</div>

## 🌾 Overview

This repository contains the self-contained V9 local candidate for the
[Kaggriculture competition](https://www.kaggle.com/competitions/kaggriculture).
V9 keeps V8's five observable public-shop experts and recovery-aware execution
controller, then reconciles final sales against the shed that will actually be
available after same-turn unit actions. It does not use identity, episode ID,
submission ID, random seed, opponent-private inventory, or future actions.

```text
public shop prefix
  ├─ first shop is YARN_STORE          → first-Yarn 6C/12S route
  ├─ first two shops end in YARN_STORE → second-Yarn 6C/12S route
  ├─ Yarn is third + early milk support
  │    ├─ public farm distance ≥ 3     → 10C/4S route
  │    └─ public farm distance < 3     → 6C/8S route
  ├─ other third-Yarn prefix           → 6C/8S route
  ├─ early milk-support signal         → 10C/4S route
  └─ otherwise                         → 8C/6S route

step 718 only
  └─ projected sellable stock > scheduled SELL → top up final liquidation
```

The Kaggle entrypoint is [`main.py`](main.py). It is self-contained, returns
JSON-safe actions, and has no runtime dependency on the rest of this repository.

## 🧠 Strategy

- The V8 per-seat selector retains first-Yarn, second-Yarn, ordinary
  third-Yarn, early-milk, and default routes. Only a current third-Yarn prefix
  whose first two shops support milk activates the divergence decision.
- The selector measures the L1 difference in public cow, sheep, wheat, melon,
  strawberry, and empty-pasture counts. A distance of at least three selects
  the existing 10C/4S expert; a near mirror stays on 6C/8S. The decision is
  sticky, seat-isolated, and reset between episodes.
- A step-24–71 legacy-opening gate recognizes the older public opening shape
  and selects its matching legacy tape. The divergence branch never applies
  to a legacy route.
- All five current and five legacy tapes are modified, normalized, compressed
  route data derived from the Apache-2.0 artifact documented in
  [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md). The selector and runtime
  execution controller are independently maintained in this repository.
- Recovery controls remain active: day-boundary weed recovery, observable
  cow-placement and purchase reconciliation, seed-prefix feasibility, bounded
  premium prepayment/repayment, executable same-turn SELL ranking, terminal
  seed pruning, retry-safe per-seat action caching, and malformed-observation
  protection.
- On step 718, V9 projects the same-turn shed, preserves sufficient sales, and
  tops up or appends only uncovered products. Earlier actions and already
  sufficient final orders remain unchanged; market orders stay capped at 10.

## ✅ Verified current strategy

The final local `main.py` SHA-256 is
`dc4ee0a23285ef9f1dd2ba9b9b8f39feb434e363859b60f82d3f793505edb88f`.
The repository has 71 passing tests and `python -m pip check` reports no broken
requirements. With `kaggle-environments==1.32.7`, starter and random matches
from both seats each completed 720 states with `DONE/DONE` and no stderr.

The `2026-08-27T10:25:18Z` submission snapshot showed V8 at dynamic score
**1848.0** and V7 at **2201.6**. The public leaderboard archive at
`2026-08-27T10:23:25Z` placed `ziliangCok` at rank **256/6569** with the team's
best score **2201.6**; that row is not a V8-only score. Ratings and ranks are
dynamic.

All 177 V8 public replays calibrated exactly at 108 wins, one tie, and 68
losses. V9 changed only the final action in the 32 games whose scheduled SELL
orders missed actual terminal stock:

| Fixed opponent tape | Wins | Ties | Losses | Mean margin |
|:---|---:|---:|---:|---:|
| frozen V8 | 108 | 1 | 68 | +2171.271 |
| **V9 terminal reconciliation** | **110** | **1** | **66** | **+2431.096** |

V9 improved all 32 affected rows, left 145 unchanged, regressed zero, retained
all 108 V8 wins, and flipped two losses. The terminal audit reduced 1,025
stranded sellable units to zero.

An additional 333-game V7 control corpus also calibrated exactly. V9 retained
all 157 recorded V7 wins, improved 85 rows, left 248 unchanged, regressed zero,
and moved from 157/3/173 to 169/2/162. Separately, V8 versus V7 had zero
regressions, and V9's terminal change versus V8 also had zero regressions. On
the 133 games created after the V8 design snapshot, V9 improved 29 end-to-end,
left 104 unchanged, regressed zero, and flipped one loss. These are
fixed-opponent-action counterfactuals, not live rematches or leaderboard
estimates. Exact hashes, failure clusters, and claim limits are in
[`docs/evidence/v9-failure-analysis.json`](docs/evidence/v9-failure-analysis.json)
and [`docs/v9-strategy.md`](docs/v9-strategy.md).

## 🚜 Quick start

Prerequisites: Git, CPython 3.12.13, and a POSIX-like shell. The exact Python
version is recorded in [`.python-version`](.python-version).

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
python -m pip check
python -m pytest -q
```

Run full matches and write ignored replays:

```bash
python scripts/run_local_match.py --opponent starter --seed 20260805
python scripts/run_local_match.py --opponent random --seed 20260805 --player 1
```

Build and inspect the minimal Kaggle archive:

```bash
python scripts/package_submission.py
tar -tzf dist/submission.tar.gz
```

## 📦 Submission

The V9 candidate has **not** been committed, pushed, or uploaded. The latest
remote delivery remains V8 submission `55719179`, message
`v8 divergence-gated third-yarn milk 779caae`, reached `COMPLETE`. The uploaded
`main.py` maps to public Git commit
[`779caae`](https://github.com/COK-ZhangZiliang/Kaggriculture/commit/779caaec88a441345871e2d62eb5de93606b7b52).

The reviewed V8 archive is 99,945 bytes with SHA-256
`5c410ffb2a3637ce8840274c7eab70813c270209cbcbb79e735eb2c547a4b35d`.
Kaggle recorded it at `2026-08-23T15:57:38.490Z`; validation was observed at
`2026-08-23T16:02:22Z`. In the latest pulled snapshot it remained `COMPLETE`
at dynamic score **1848.0**, while V7 was `COMPLETE / 2201.6`. These values are
dynamic observations, not final strength estimates.

The reviewed local V9 archive is 100,234 bytes with SHA-256
`0a188e825eada95009902566432246f07667688c2280578a81864c73f37c3735`.
It is a packaging artifact only, not a Kaggle submission.

The package contains only the self-contained entrypoint and the applicable
Apache attribution files:

```text
submission.tar.gz
├── main.py
├── LICENSE-APACHE-2.0.txt
└── THIRD_PARTY_NOTICES.txt
```

## 🗂️ Project layout

```text
.
├── main.py                       # self-contained V9 local candidate
├── scripts/                      # local evaluation and packaging utilities
├── docs/v9-strategy.md           # current strategy and evidence boundary
├── docs/evidence/v9-failure-analysis.json
├── tests/                        # unit and environment smoke tests
├── THIRD_PARTY_NOTICES.md        # route provenance and modifications
├── AGENTS.md                     # strategy history and workflow rules
└── requirements*.txt             # portable dependency inputs and lockfile
```

## 🧭 Development gates

Before changing the agent or submitting a new revision:

1. Run `python -m pip check` and `python -m pytest -q`.
2. Complete 720-state starter and random matches.
3. Rebuild the archive and verify its exact contents and hash.
4. Distinguish replay reproduction, open-loop diagnostics, closed-loop local
   evaluation, remote validation, and leaderboard scoring.
5. Stage only explicit paths and keep secrets and generated artifacts out of
   every commit.

Repository-specific contribution and delivery rules live in
[`AGENTS.md`](AGENTS.md).

---

<div align="center">
  Reconcile what is executable, preserve every known win, then improve. 🌱
</div>
