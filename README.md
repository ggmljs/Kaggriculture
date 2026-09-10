<div align="center">
  <img src="assets/logo.svg" width="100%" alt="Kaggriculture autonomous farming agent" />

  [![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
  [![Tests](https://img.shields.io/badge/tests-81%20passing-2ea44f?logo=pytest&logoColor=white)](#verified-current-strategy)
  [![Submission](https://img.shields.io/badge/V29-COMPLETE-2ea44f?logo=kaggle&logoColor=white)](#submission)
  [![Policy](https://img.shields.io/badge/policy-official--strong%20default-7B61FF)](#strategy)

  **A deterministic public-state farm agent for Kaggle's 720-state economic simulation.**
</div>

## Overview

This repository contains the self-contained V29 candidate for the
[Kaggriculture competition](https://www.kaggle.com/competitions/kaggriculture).
V29 resets the default production plan to a league-selected 8-cow, 6-sheep,
3-goose route reconstructed from consistent public leaderboard behavior while
retaining the defensive execution and liquidation controls.

```text
official public replay routes
  ├─ reconstruct complete deterministic production experts
  ├─ screen every route against top leaderboard action tapes
  ├─ select cooked episode 107301740 as the default expert
  └─ retain fail-closed execution and terminal liquidation controls
```

The Kaggle entrypoint is [`main.py`](main.py). It has no runtime dependency on
training files, PyTorch, local packages, absolute paths, or network access.

## Strategy

- The default expert builds toward 8 cows, 6 sheep, and 3 geese with larger
  wheat and strawberry production than V18's route family.
- Route selection was frozen before the final official-replay gate was opened.
- Public identity, episode ID, seed, and future actions are not used at runtime.
- Existing weed recovery, purchase reconciliation, market-order safety,
  terminal liquidation, malformed-observation protection, and retry-safe
  action caching remain active.

## Verified current strategy

The final `main.py` SHA-256 is
`68c81d9efbd27807340ad575a4e92d12aff151561185be22823ebd5ebf1597eb`.

The official-replay gate covered 80 both-seat games from the 2026-09-10 top
leaderboard snapshot. V29 moved from V18's 17/80 wins and `-12,520.5625` mean
margin to 35/80 wins and `-1,189.05`; 60/80 paired rows improved, with mean
paired delta `+11,331.5125`.

On twelve new seeds in both seats, V29 beat V18 in all 24 closed-loop games at
mean margin `+18,323.292`. All gate games completed 720 states with
`DONE/DONE` and empty stderr. V29 still lost 0/8 against `Otter Vibe`; this is
recorded as a known weakness, not hidden by an aggregate. Exact scope is in
[`docs/v29-strategy.md`](docs/v29-strategy.md).

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

V29 submission `56137699`, message `v29 official-strong default d95fc6b`,
reached `COMPLETE`. The uploaded `main.py` maps to public Git commit
[`d95fc6b`](https://github.com/ggmljs/Kaggriculture/commit/d95fc6b590a466cf1622326872681f9053e25772),
which was pushed to `origin/feature/v29-official-strong-default` before upload.
Kaggle recorded it at `2026-09-10T05:10:42.403Z` with initial dynamic score
`600.0`; this is a starting snapshot, not a strength estimate.

The deterministic reviewed archive is 181,451 bytes with SHA-256
`b9caf78699c65cd4c4e69bd14d6c8ae09e7285eb1c0af8ec36e71dd020b4843c`.

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
├── main.py                       # self-contained V29 Kaggle agent
├── scripts/                      # evaluation and packaging utilities
├── docs/v29-strategy.md          # current strategy and evidence boundary
├── tests/                        # deterministic tests and smoke checks
├── THIRD_PARTY_NOTICES.md        # provenance and modifications
├── AGENTS.md                     # chronological strategy history and rules
└── requirements*.txt             # dependency inputs and lockfile
```

Repository-specific contribution and delivery rules live in
[`AGENTS.md`](AGENTS.md).