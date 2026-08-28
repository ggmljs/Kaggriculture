<div align="center">
  <img src="assets/logo.svg" width="100%" alt="Kaggriculture autonomous farming agent" />

  <br />

  [![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
  [![Kaggle Environment](https://img.shields.io/badge/Kaggle-Environment-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com/competitions/kaggriculture)
  [![Tests](https://img.shields.io/badge/tests-77%20passing-2ea44f?logo=pytest&logoColor=white)](#-verified-current-strategy)
  [![Submission status](https://img.shields.io/badge/V10%20submission-COMPLETE-2ea44f?logo=kaggle&logoColor=white)](#-submission)
  [![Policy](https://img.shields.io/badge/policy-V10%20fail--closed%20recovery-7B61FF)](#-strategy)

  **A deterministic public-state farm agent for Kaggle's 720-state economic simulation.**
</div>

## 🌾 Overview

This repository contains the self-contained V10 agent for the
[Kaggriculture competition](https://www.kaggle.com/competitions/kaggriculture).
V10 keeps V9 as the default and adds one fail-closed opening recovery branch
at the first safe route divergence. It uses only observable current-game state
and never routes on identity, episode ID, submission ID, random seed,
opponent-private inventory, replay lookup, or future actions.

```text
step 72 public opening
  ├─ complete recovery signature
  │    ├─ Yarn appears by step 168 → frozen V5 high 6C/12S route
  │    └─ otherwise                → frozen V5 low 10C/4S route
  └─ missing, malformed, or other  → unchanged V9 selector and routes

all paths
  ├─ V9 recovery-aware execution controls
  └─ step 718 projected-shed terminal liquidation
```

The Kaggle entrypoint is [`main.py`](main.py). It is self-contained, returns
JSON-safe actions, and has no runtime dependency on the rest of this
repository.

## 🧠 Strategy

- The recovery gate is evaluated only at step 72. It requires first shop
  `BAKERY` or `PIZZA_SHOP`, an opponent public farm with exactly 1 cow,
  4 sheep, 5 wheat, and 4–5 melon, plus lower public cash on our side.
- Cash must be explicitly present and finite. Shop and tile structures must
  match the public schema. Any missing or malformed feature closes the gate.
- The decision is sticky, seat-isolated, reset-safe, and cannot open after the
  decision step. All V9 routes and the recovery route share the first 72
  actions, so the switch occurs before behavior diverges.
- A matched game uses the frozen V5 low route, then selects the frozen high
  route at step 168 if Yarn demand appears. Route provenance is documented in
  [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
- Non-matching games retain V9's five current routes, five legacy routes,
  third-Yarn milk selector, seed and weed recovery, animal reconciliation,
  premium repayment, executable SELL ranking, retry-safe action cache, and
  malformed-observation protection.
- Step 718 still projects the same-turn shed, preserves sufficient existing
  SELL orders, and only tops up uncovered sellable stock within the ten-order
  cap.

## ✅ Verified current strategy

The submitted V10 `main.py` SHA-256 is
`56831f3c43c9727d90016b7a7a8d4eb51d1a4c08c1120d58f061d9176e8bc109`.
The repository has 77 passing tests, and `python -m pip check` reports no
broken requirements. Starter and random matches from both seats each reached
720 states with `DONE/DONE`, no stderr, and a win.

The release hash was run against three calibrated public replay corpora:

| Fixed opponent-action corpus | Games | V9 W/T/L | V10 W/T/L | Improved | Identical | Regressed |
|:---|---:|:---:|:---:|---:|---:|---:|
| V7 control | 333 | 169/2/162 | 169/2/162 | 2 | 331 | 0 |
| V8 control | 177 | 110/1/66 | 111/1/65 | 2 | 175 | 0 |
| latest V9 | 87 | 57/0/30 | 59/0/28 | 3 | 84 | 0 |
| **Combined** | **597** | **336/3/258** | **339/3/255** | **7** | **590** | **0** |

V10 preserved all 336 known V9 wins. Every game reached 720 states with
`DONE/DONE` and empty stderr. Combined mean margin moved from `+1171.886` to
`+1266.020`.

Three public V9 episodes retrieved only after the gate was frozen were
action- and margin-identical between V9 and V10. A separate fresh 80-game
closed-loop panel against five hash-pinned opponents was also identical on all
80 rows at 68 wins and mean margin `+2515.8125`.

The recovery gate did not trigger in those fresh games. They verify that V10
fails closed without drifting from V9; they do not prove fresh generalization
of the recovery branch. The seven improvements are fixed recorded-opponent
action counterfactuals, not live rematches or leaderboard forecasts. Exact
hashes, rejected candidates, and claim limits are in
[`docs/evidence/v10-failure-analysis.json`](docs/evidence/v10-failure-analysis.json)
and [`docs/v10-strategy.md`](docs/v10-strategy.md).

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

V10 submission `55848408`, message
`v10 fail-closed opening recovery 5c1ffa4`, reached `COMPLETE`. The uploaded
`main.py` maps to public Git commit
[`5c1ffa4`](https://github.com/COK-ZhangZiliang/Kaggriculture/commit/5c1ffa466e8755857a87936e0a24b2d4461aa61b),
which was pushed to `origin/main` before upload.

The deterministic reviewed archive is 122,013 bytes with SHA-256
`4b759b53b7e7ae81b7a1334208db82aacc8a0e1062546dab974843066648d8bb`.
Kaggle recorded it at `2026-08-28T16:08:13.067Z`; validation was observed at
`2026-08-28T16:10:25Z` with initial dynamic public score **600.0**.

The operating target is `2600+`, but it has not yet been observed for V10. A
new simulation submission begins its own dynamic rating trajectory, so the
initial score is a delivery snapshot rather than a strength estimate.

The package contains only:

```text
submission.tar.gz
├── main.py
├── LICENSE-APACHE-2.0.txt
└── THIRD_PARTY_NOTICES.txt
```

## 🗂️ Project layout

```text
.
├── main.py                       # self-contained V10 Kaggle agent
├── scripts/                      # local evaluation and packaging utilities
├── docs/v10-strategy.md          # current strategy and evidence boundary
├── docs/evidence/v10-failure-analysis.json
├── tests/                        # deterministic unit and smoke tests
├── THIRD_PARTY_NOTICES.md        # route provenance and modifications
├── AGENTS.md                     # chronological strategy history and rules
└── requirements*.txt             # portable dependency inputs and lockfile
```

## 🧭 Development gates

Before changing or submitting the agent:

1. Run `python -m pip check` and `python -m pytest -q`.
2. Complete 720-state starter and random matches from both seats.
3. Require zero per-game margin regression and preserve every known win.
4. Rebuild the archive and verify its exact contents, import, and hash.
5. Distinguish fixed tapes, closed-loop panels, remote validation, and dynamic
   leaderboard scoring.
6. Stage only explicit paths and keep secrets and generated artifacts out of
   every commit.

Repository-specific contribution and delivery rules live in
[`AGENTS.md`](AGENTS.md).

---

<div align="center">
  Fail closed, preserve every known win, then improve. 🌱
</div>
