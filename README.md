<div align="center">
  <img src="assets/logo.svg" width="100%" alt="Kaggriculture autonomous farming agent" />

  [![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
  [![Tests](https://img.shields.io/badge/tests-80%20passing-2ea44f?logo=pytest&logoColor=white)](#verified-current-strategy)
  [![Submission](https://img.shields.io/badge/V18-COMPLETE-2ea44f?logo=kaggle&logoColor=white)](#submission)
  [![Policy](https://img.shields.io/badge/policy-online--safe%20residual%20KNN-7B61FF)](#strategy)

  **A deterministic public-state farm agent for Kaggle's 720-state economic simulation.**
</div>

## Overview

This repository contains the self-contained V18 candidate for the
[Kaggriculture competition](https://www.kaggle.com/competitions/kaggriculture).
V18 keeps V16 as the baseline, uses an at-most-once SELL-only residual on day
16 or 27, and retrains its gate on 480 semantically compatible counterfactual
records including a new safe round 4.

```text
V16 baseline action
  ├─ malformed/repeated-Bakery public regime → return unchanged
  ├─ day not in {16, 27} or already used     → return unchanged
  ├─ KNN lower-confidence score ≤ 150        → return unchanged
  └─ score > 150                             → one shielded SELL intervention
```

The Kaggle entrypoint is [`main.py`](main.py). It has no runtime dependency on
training files, PyTorch, local packages, absolute paths, or network access.

## Strategy

- The gate uses `k=5`, uncertainty penalty `beta=0.5`, and threshold `150`.
- Farmer, hand, and purchase actions always remain baseline-controlled.
- `LIQUIDATE_SHED` preserves baseline sell orders, tops up their quantities,
  and spends only free order slots on highest-current-value omitted inventory.
- A repeated initial `BAKERY/BAKERY` public shop prefix fails closed to V16.
- Baseline metadata and action caches remain synchronized after intervention.

## Verified current strategy

The final `main.py` SHA-256 is
`71246b225b6ab2cd7ce1bd9ae0f26a0a62972226fa4addb7dc4b7130a250b94b`.

The independent 60-seed, both-seat panel completed 120/120 games at
`DONE/DONE`, with mean margin `+58.958` versus V16 and paired bootstrap 95%
interval `[+19.258, +103.142]`. Thirteen seeds were positive, 42 tied, and five
negative.

Sixteen both-seat comparisons against eight latest V17 public opponent action
tapes were clean and had zero regression versus V16. A separate 24-game final
league had positive mean margin against V16, frozen V10, and Wheat. These are
local frozen and open-loop diagnostics, not a live-score guarantee. Exact
scope is documented in [`docs/v18-strategy.md`](docs/v18-strategy.md).

## Quick start

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
python -m pytest -q
python scripts/run_local_match.py --opponent starter --seed 20260805
python scripts/package_submission.py
```

## Submission

V18 submission `56128972`, message `v18 online-safe residual knn 467d26d`,
reached `COMPLETE`. The uploaded `main.py` maps to public Git commit
[`467d26d`](https://github.com/ggmljs/Kaggriculture/commit/467d26d881c6d0232c46152f5c09d3ad2d24fc56),
which was pushed to `origin/feature/v18-online-safe-residual` before upload.
Kaggle recorded it at `2026-09-09T18:17:54.090Z` with initial dynamic score
`600.0`; this is a starting snapshot, not a final strength estimate.

The deterministic reviewed archive is 139,406 bytes with SHA-256
`c0b00b1ed1f5e430e183bf8ae4beb7aa71e2bd49b841372233a47450a66eddf9`.

The package contains only:

```text
submission.tar.gz
├── main.py
├── LICENSE-APACHE-2.0.txt
└── THIRD_PARTY_NOTICES.txt
```

## Project layout

```text
.
├── main.py                       # self-contained V18 Kaggle agent
├── scripts/                      # evaluation and packaging utilities
├── docs/v18-strategy.md          # current strategy and evidence boundary
├── tests/                        # deterministic tests and smoke checks
├── THIRD_PARTY_NOTICES.md        # provenance and modifications
├── AGENTS.md                     # chronological strategy history and rules
└── requirements*.txt             # dependency inputs and lockfile
```

Repository-specific contribution and delivery rules live in
[`AGENTS.md`](AGENTS.md).