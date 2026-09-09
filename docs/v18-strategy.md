# V18 online-safe residual KNN policy

## Promoted behavior

V18 keeps the V16 controller as the baseline and retains the at-most-once,
SELL-only residual action space on day 16 or day 27. It adds two safety layers
learned from V17 public outcomes and a new counterfactual round:

- `LIQUIDATE_SHED` preserves every executable baseline sale, tops up those
  quantities to observable shed inventory, and uses only genuinely free order
  slots for omitted inventory ranked by current gross value. It no longer
  rebuilds the sell list in enum order or evicts a baseline FERTILIZER sale.
- The residual fails closed when the first two public shops are both BAKERY,
  the repeated-shop regime that produced the reproducible V17 online-tape
  regression. Missing or malformed shop data also falls back to V16.

The final gate uses 480 semantically compatible counterfactual rows: unchanged
HALVE_SALES/SELL_AVAILABLE rows from rounds 2 and 3 plus all three deployed
modes from the new safe round 4. Old LIQUIDATE_SHED labels are excluded because
they describe the superseded action semantics.

## Hyperparameter selection

Leave-one-seed-out selection over 48 seeds and 192 contexts retained `k=5`,
`beta=0.5`, and threshold `150`. Its realized mean advantage was `+78.448`,
with worst context `-290`. Threshold 100 had a slightly larger development
mean but reproduced a `-243` regression from each seat on a V17 public opponent
action tape, so it was rejected before release.

## Verification

- Final `main.py` SHA-256:
  `71246b225b6ab2cd7ce1bd9ae0f26a0a62972226fa4addb7dc4b7130a250b94b`.
- Round 4 counterfactual collection completed 48 baseline games and 288
  intervention games at `DONE/DONE`; 62 interventions had positive terminal
  advantage.
- The final independent closed-loop panel used 60 fresh seeds and both seats:
  120/120 games reached `DONE/DONE`, mean margin was `+58.958`, and the paired
  bootstrap 95% interval was `[+19.258, +103.142]`. Thirteen seeds were
  positive, 42 tied, and five negative; bootstrap positive-mean probability
  was 99.912%.
- On eight latest V17 public opponents, both seats produced 16/16 clean fixed
  action-tape comparisons with zero regression versus V16. This is an
  open-loop safety screen, not an adaptive rematch.
- A final 24-game, three-opponent, both-seat league was clean. Mean margins were
  `+78.75` versus V16, `+81.0` versus the frozen V10 reference, and
  `+149,778.25` versus Wheat.
- The self-contained source compiles without PyTorch or training files.

These are local frozen comparisons and public-action-tape diagnostics. They do
not guarantee a live leaderboard score or performance against hidden and
changing opponents.

## Delivery

The deterministic 139,406-byte archive has SHA-256
`c0b00b1ed1f5e430e183bf8ae4beb7aa71e2bd49b841372233a47450a66eddf9`
and contains only `main.py`, `LICENSE-APACHE-2.0.txt`, and
`THIRD_PARTY_NOTICES.txt`. Git commit, Kaggle submission ID, validation status,
and observed dynamic score are recorded after the corresponding remote
operations complete.