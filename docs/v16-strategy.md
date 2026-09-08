# V16 leader-aware conservative market queue

## Promoted behavior

V16 keeps the existing public-shop route controller and adds two bounded
controls. First, a public-tile detector observes the opponent during steps
24–96. A layout with at least four cows, no more than two sheep, and at least
twelve wheat tiles is treated as the cow-heavy leader opening. If the existing
selector chooses 10C/4S, V16 uses 8C/6S instead unless Pizza is present among
the first three shops. Missing or malformed input closes the detector.

Second, executable sales move to the front of the ten-slot market queue while
retaining their relative order. Other orders also retain relative order.
Legal WHEAT/FERTILIZER restocking is not back-loaded and unsupported product
buys are not inserted as padding by default. Nonpositive executable SELL and
BUY_PRODUCT requests are removed.

## Rejected interpretation

Kaggle environment 1.32.7 executes `BUY_PRODUCT` only for WHEAT and
FERTILIZER. Replay requests for CARROT, TOMATO, STRAWBERRY, or MELON do not
change cash, shared market inventory, or private inventory. They are no-ops,
not evidence of cross-product inventory trading. The experimental late-slot
restocking candidate produced only tiny tape gains and a repeatable V10
closed-loop loss, so both late restocking and no-op padding remain disabled.

## Verification

- `main.py` SHA-256:
  `e3df9435cffe67a75ae908a1c888240b30546e4a1a86cba62904fe34e2cb4f2f`.
- 80 repository tests passed.
- Starter and random smoke matches completed 720 states at `DONE/DONE` and
  were wins.
- The four-seed, both-seat frozen panel completed 40 games cleanly against V4,
  V5, V7, V10, and Wheat. V4, V5, and Wheat were unchanged by SELL
  front-loading. V7 and V10 each gained `+2.25` mean margin versus queue-off.
- One representative action tape for each of SpaTaro, Otter Vibe, Mengfei Li,
  binghua, Matthew Huang, and Ad Space Available was run from both seats. All
  12 comparisons had zero margin regression against the frozen pre-queue
  candidate.

The replay checks use fixed recorded opponent actions and cannot demonstrate
adaptive rematch strength. The closed-loop panel contains frozen local
artifacts and cannot guarantee a live leaderboard rank.

The repository-local dependency installation hit the Windows path-length
limit in an optional Orbax fixture. Kaggriculture 1.32.7 imported and every
applicable test and match above ran, but `pip check` retains three missing
optional transitive packages (`gymnax`, `litellm`, and `transformers`).

## Delivery

Git commit `85aae5c042b23d9da45a0f5c4a57e6b2e24c2016` was pushed before
the Kaggle upload. Submission `56103627` reached `COMPLETE`. The submitted
125,637-byte archive has SHA-256
`78ecfb3e3938117bdad1109eccc0a3f47f5666178c22889b2126b7cb2decc289`.
The observed `600.0` public score is the new simulation slot's initial dynamic
rating, not a final strength measurement.
