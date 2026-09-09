<div align="center">
  <img src="assets/logo.svg" width="100%" alt="Kaggriculture autonomous farming agent" />

  [![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
  [![Tests](https://img.shields.io/badge/tests-80%20passing-2ea44f?logo=pytest&logoColor=white)](#verified-current-strategy)
  [![Submission](https://img.shields.io/badge/V17-COMPLETE-2ea44f?logo=kaggle&logoColor=white)](#submission)
  [![Policy](https://img.shields.io/badge/policy-safe%20residual%20KNN-7B61FF)](#strategy)

  **A deterministic public-state farm agent for Kaggle's 720-state economic simulation.**
</div>

## Overview

This repository contains the self-contained V17 agent for the
[Kaggriculture competition](https://www.kaggle.com/competitions/kaggriculture).
V17 keeps V16 as the baseline and adds a deterministic, once-per-episode,
SELL-only residual learned from counterfactual round-2/3 data.

```text
V16 baseline action
  ├─ day not in {16, 27}       → return unchanged
  ├─ residual already used     → return unchanged
  ├─ estimated advantage ≤ 0   → return unchanged
  └─ estimated advantage > 0   → apply one bounded SELL-only intervention
```

The Kaggle entrypoint is [`main.py`](main.py). It has no runtime dependency on
training files, PyTorch, the local training package, absolute paths, or network
access.

## Strategy

- V16 remains the default controller on every turn.
- The residual uses `k=5`, distance weighting `beta=1.0`, and a strictly
  positive estimated-advantage threshold over 384 embedded counterfactual
  records.
- At most one intervention can occur, only on day 16 or 27, and only market
  `SELL` orders may change.
- Farmer actions, hand actions, and purchase orders always remain controlled by
  the baseline.
- Baseline metadata and action caches are synchronized after an intervention.

## Verified current strategy

The V17 `main.py` SHA-256 is
`4b9745ebc26f51b776598ad4326d8ce9b8fdb1c9ea789724db98fb91fd404042`.
The repository has 80 passing tests. Starter and random smoke matches each
reached 720 states with `DONE/DONE` and a win.

The independent round-4 frozen confirmation completed 120 games over 60 seeds
and both seats with mean paired margin `+152.892` and paired confidence interval
`[+31.62, +324.34]` versus V16. Combining both frozen panels gives 200 games
over 100 seeds, mean paired margin `+112.405`, confidence interval
`[+34.99, +218.42]`, and 36 positive, 50 tied, and 14 negative seeds.

A source-string execution smoke completed 8/8 games without stderr. Regression
checks won 8/8 games against `main_hybrid.py` and 8/8 against `rule_agent.py`.
These are local frozen comparisons, not a guarantee against hidden or changing
opponents. Exact scope and claim limits are in
[`docs/v17-strategy.md`](docs/v17-strategy.md).

The repository-local environment still reports three missing optional
`kaggle-environments` transitive packages (`gymnax`, `litellm`, and
`transformers`). Kaggriculture 1.32.7 imports successfully and all applicable
checks above ran.

## Quick start

Prerequisites: Git and the CPython version recorded in [`.python-version`](.python-version).

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
python -m pytest -q
```

Run local matches and build the minimal archive:

```bash
python scripts/run_local_match.py --opponent starter --seed 20260805
python scripts/run_local_match.py --opponent random --seed 20260805
python scripts/package_submission.py
tar -tzf dist/submission.tar.gz
```

## Submission

V17 submission `56126261`, message `v17 safe residual knn 1277bdb`, reached
`COMPLETE`. The uploaded `main.py` maps to public Git commit
[`1277bdb`](https://github.com/ggmljs/Kaggriculture/commit/1277bdba4440edffdb062519c7ecd66a9a937243),
which was pushed to `origin/feature/safe-residual-knn` before the Kaggle upload.

The reviewed archive is 135,892 bytes with SHA-256
`c285227a85f0a2f91468e924720b72bc51107222031089af25d30aaea820977a`.
Kaggle recorded it at `2026-09-09T15:25:15.680Z`; validation completed with an
initial dynamic public score of **600.0**. A new simulation submission begins
its own rating trajectory, so this is a delivery snapshot rather than a final
strength estimate.

The package contains only:

```text
submission-residual-knn.tar.gz
├── main.py
├── LICENSE-APACHE-2.0.txt
└── THIRD_PARTY_NOTICES.txt
```

## Project layout

```text
.
├── main.py                       # self-contained V17 Kaggle agent
├── scripts/                      # local evaluation and packaging utilities
├── docs/v17-strategy.md          # current strategy and evidence boundary
├── tests/                        # deterministic unit and smoke tests
├── THIRD_PARTY_NOTICES.md        # route provenance and modifications
├── AGENTS.md                     # chronological strategy history and rules
└── requirements*.txt             # portable dependency inputs and lockfile
```

## Development gates

1. Run `python -m pip check` and `python -m pytest -q`.
2. Complete 720-state starter and random matches.
3. Evaluate both seats on frozen seeds and report regressions as well as means.
4. Rebuild the archive and verify its contents, import, and hash.
5. Distinguish local frozen evidence, remote validation, and dynamic scores.
6. Stage only explicit paths; never commit credentials or generated training data.

Repository-specific contribution and delivery rules live in
[`AGENTS.md`](AGENTS.md).