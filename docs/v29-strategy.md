# V29 official-strong default

## Decision

V29 replaces V18's default production tape with a deterministic 8-cow,
6-sheep, 3-goose route reconstructed from four public Kaggriculture episodes
of the leaderboard team `cooked`. The four observed action sequences agreed on
86.3% of their steps. A route league selected episode `107301740` as the
default before the final gate was opened.

This is a production-route reset, not a claim that the submitted policy is an
end-to-end neural policy. CTDE, DAgger, and league tooling were used to produce
and screen candidate behavior; the Kaggle artifact remains deterministic and
self-contained.

## Official replay gate

The gate used four public episodes per available leaderboard team, both seats,
and the 2026-09-10 leaderboard snapshot. Shared ranks yielded 80 total games
across eleven displayed teams. Every game completed 720 states with
`DONE/DONE` and empty stderr.

| Policy | Wins | Losses | Mean margin |
| --- | ---: | ---: | ---: |
| V18 | 17 | 63 | -12,520.5625 |
| V29 | 35 | 45 | -1,189.05 |

On the exact 80 paired `(team, episode, seat)` rows, V29 improved 60 and
regressed 20. Mean paired improvement was `+11,331.5125`, median improvement
was `+21,415.5`, and worst regression was `-78,282`.

Selected team results for V29 were:

| Public opponent | Wins/games | Mean margin |
| --- | ---: | ---: |
| SpaTaro | 6/8 | +17,097.25 |
| Himanshu Kumar | 5/8 | +813.75 |
| Mengfei Li | 8/8 | +20,202.125 |
| cooked | 4/8 | +1,635.375 |
| binghua | 6/8 | +2,785.25 |
| Otter Vibe | 0/8 | -39,784.625 |

The Otter Vibe result is an explicit known weakness. Multiple complete routes
reconstructed from the other top-ten teams and several market-only hybrids
failed to improve it without larger regressions, so no opponent-identity gate
was added.

## Fresh closed-loop control

V29 then played V18 on twelve new deterministic seeds in both seats. It won
all 24 games. All games completed 720 states with `DONE/DONE` and empty
stderr. Mean margin was `+18,323.292`; the three separately executed batches
had means of `+17,911`, `+18,069.125`, and `+18,989.75`.

## Evidence boundary

Public replay action-tape evaluation fixes the opponent's actions and is not a
live rematch. The fresh V18 control is closed-loop but does not represent the
current leaderboard distribution. These gates establish a large, reproducible
improvement over V18 and useful coverage of official strong behavior; they do
not guarantee a Kaggle rating or rank.

The frozen `main.py` SHA-256 is
`68c81d9efbd27807340ad575a4e92d12aff151561185be22823ebd5ebf1597eb`.
