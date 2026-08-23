<div align="center">
  <img src="assets/logo.svg" width="100%" alt="Kaggriculture autonomous farming agent" />

  <br />

  [![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
  [![Kaggle Environment](https://img.shields.io/badge/Kaggle-Environment-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com/competitions/kaggriculture)
  [![Tests](https://img.shields.io/badge/tests-66%20passing-2ea44f?logo=pytest&logoColor=white)](#-verified-current-strategy)
  [![Submission status](https://img.shields.io/badge/V8%20submission-COMPLETE-2ea44f?logo=kaggle&logoColor=white)](#-submission)
  [![Policy](https://img.shields.io/badge/policy-V8%20divergence--gated-7B61FF)](#-strategy)

  **A deterministic public-demand-routed farm agent for Kaggle's 720-state economic simulation.**
</div>

## 🌾 Overview

This repository contains the self-contained V8 agent for the
[Kaggriculture competition](https://www.kaggle.com/competitions/kaggriculture).
V8 keeps the five observable public-shop experts and the recovery-aware
execution controller. It resolves a third-Yarn route conflict using only the
two farms' visible production layouts; it does not use identity, episode ID,
submission ID, random seed, hidden inventory, or future actions.

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
```

The Kaggle entrypoint is [`main.py`](main.py). It is self-contained, returns
JSON-safe actions, and has no runtime dependency on the rest of this repository.

## 🧠 Strategy

- A per-seat selector retains V7's first-Yarn, second-Yarn, ordinary
  third-Yarn, early-milk, and default routes. Only a current third-Yarn prefix
  whose first two shops support milk activates the V8 decision.
- V8 measures the L1 difference in public cow, sheep, wheat, melon,
  strawberry, and empty-pasture counts. A distance of at least three selects
  the existing 10C/4S expert; a near mirror stays on 6C/8S. The decision is
  sticky, seat-isolated, and reset between episodes.
- A step-24–71 legacy-opening gate recognizes the older public opening shape
  and selects its matching legacy tape. V8 never applies the new branch to a
  legacy route.
- All five current and five legacy tapes are modified, normalized, compressed
  route data derived from the Apache-2.0 artifact documented in
  [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md). The selector and runtime
  execution controller are independently maintained in this repository.
- Recovery controls remain active: day-boundary weed recovery, observable
  cow-placement and purchase reconciliation, seed-prefix feasibility, bounded
  premium prepayment/repayment, executable same-turn SELL ranking, terminal
  seed pruning, retry-safe per-seat action caching, and malformed-observation
  protection.
- Every action is hand-aligned, market orders are capped at 10, and terminal
  liquidation is scheduled from the route tape.

## ✅ Verified current strategy

The frozen V8 `main.py` SHA-256 is
`faf57412e2c56dcc669043865a185324bab9952d865abccc2203284e854eceb3`.
The repository has 66 passing tests. With `kaggle-environments==1.32.7`,
starter and random matches from both seats each completed 720 states with
`DONE/DONE` and no stderr.

The latest official snapshot at `2026-08-23T15:45:18Z` kept V7 at dynamic
score **2626.4** and placed `ziliangCok` at rank **53/6021**. The leaderboard
archive SHA-256 is
`78b56f62fa43ff2f97604a9c6e856b6de64092eb24ded5a1c22f368cd18dea74`.
Ratings and ranks change as public episodes run.

The complete 200-game public fixed-tape gate first calibrated the frozen V7
file exactly. V8 retained all 140 V7 wins, changed no loss into a worse margin,
flipped five losses, and improved the mean margin by `+822.085`:

| Fixed opponent tape | Wins | Ties | Losses | Mean margin |
|:---|---:|---:|---:|---:|
| frozen V7 | 140 | 1 | 59 | +3236.640 |
| **frozen V8** | **145** | **1** | **54** | **+4058.725** |

This is a fail-closed open-loop counterfactual test, not a leaderboard claim.
The targeted closed-loop panel used 11 failure-trigger seeds, four hash-pinned
artifacts, and both seats. V7 scored 56/88; V8 scored 84/88, with 28 improved
rows, 60 identical rows, no regression, and mean delta `+5367.795`.

A separate fresh panel used eight new seeds, six deduplicated public artifacts,
and both seats. V7 and V8 were margin-identical on all 96 games at 82-14; every
opponent-level mean was positive. All fixed-tape and closed-loop matches
completed 720 states, `DONE/DONE`, with no stderr. Exact failure clusters,
seeds, hashes, and claim limits are in
[`docs/evidence/v8-failure-analysis.json`](docs/evidence/v8-failure-analysis.json)
and [`docs/v8-strategy.md`](docs/v8-strategy.md).

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

V8 submission `55719179`, message
`v8 divergence-gated third-yarn milk 779caae`, reached `COMPLETE`. The uploaded
`main.py` maps to public Git commit
[`779caae`](https://github.com/COK-ZhangZiliang/Kaggriculture/commit/779caaec88a441345871e2d62eb5de93606b7b52).

The reviewed archive is 99,945 bytes with SHA-256
`5c410ffb2a3637ce8840274c7eab70813c270209cbcbb79e735eb2c547a4b35d`.
Kaggle recorded it at `2026-08-23T15:57:38.490Z`; validation was observed at
`2026-08-23T16:02:22Z` with initial dynamic public score **600.0**. At that
observation V7 submission `55638354` remained `COMPLETE / 2626.4`, preserving
the existing remote baseline as V8 begins its own rating trajectory. These are
dynamic delivery snapshots, not final strength estimates.

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
├── main.py                       # self-contained V8 Kaggle agent
├── scripts/                      # local evaluation and packaging utilities
├── docs/v8-strategy.md           # current strategy and evidence boundary
├── docs/evidence/v8-failure-analysis.json
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
  Route on public demand, preserve every known win, then improve. 🌱
</div>
