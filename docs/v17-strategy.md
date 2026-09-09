# V17 safe residual KNN policy

## Promoted behavior

V17 keeps the V16 controller as the default action source and adds a bounded
residual policy. The residual may alter only the market `SELL` list, at most
once per episode, and only on day 16 or day 27. Farmer actions, hand actions,
purchase orders, and the underlying route remain unchanged.

The residual is a deterministic `k=5` nearest-neighbor policy over 384 embedded
counterfactual training records collected in rounds 2 and 3. It uses
distance-weighted advantage with `beta=1.0` and applies an intervention only
when the estimated advantage is positive. The baseline controller's internal
metadata and action cache are updated after an intervention so later actions
remain synchronized with the action that was actually returned.

The Kaggle entrypoint is a single self-contained `main.py`. It has no runtime
dependency on training files, PyTorch, the local `strong_agent` package,
absolute paths, or `__file__`.

## Verification

- `main.py` SHA-256:
  `4b9745ebc26f51b776598ad4326d8ce9b8fdb1c9ea789724db98fb91fd404042`.
- The independent round-4 frozen confirmation completed 120/120 games at
  `DONE/DONE` over 60 seeds and both seats, with mean paired margin `+152.892`
  and paired confidence interval `[+31.62, +324.34]` versus V16.
- Combining the earlier frozen panel with round 4 gives 200 games over 100
  seeds, mean paired margin `+112.405`, confidence interval
  `[+34.99, +218.42]`, with 36 positive, 50 tied, and 14 negative seeds.
- A source-string execution smoke completed 8/8 games without stderr. A
  separate candidate smoke was 3 wins, 4 ties, and 1 loss with mean margin
  `+20.375`.
- Regression checks won 8/8 games against `main_hybrid.py` and 8/8 against
  `rule_agent.py`.

These results are frozen local comparisons. They do not establish a live
leaderboard score or guarantee performance against hidden and changing
opponents.

## Delivery

The reviewed 135,892-byte archive has SHA-256
`c285227a85f0a2f91468e924720b72bc51107222031089af25d30aaea820977a`
and contains only `main.py`, `LICENSE-APACHE-2.0.txt`, and
`THIRD_PARTY_NOTICES.txt`. Git commit and Kaggle submission identifiers are
recorded after each remote operation completes.
