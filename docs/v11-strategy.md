# V11 strategy: fail-closed market-curve adaptation

V11 retains every V10 production route and execution repair under the official default market configuration. Its only policy change is in executable SELL ordering: when the public observation explicitly contains a complete, valid market curve, V11 ranks orders using that supplied curve rather than a stale embedded default. Missing, partial, malformed, or unsupported curves fail closed to V10's exact parameters.

This is a robustness release, not a claim of a default-environment margin gain. The official default configuration leaves V11 action-identical to V10. It is promoted because it removes a configuration-sensitivity risk without changing the established route, selector, inventory, or terminal-liquidation behavior.

Release gate: syntax and package checks; both-seat seeded league against Wheat and frozen V10; a replay-tape candidate-versus-baseline gate with no regression in any comparison. The replay gate is open-loop evidence and does not claim a live-rating forecast.
## Delivery

The reviewed archive submission-v11-market-curve.tar.gz has SHA-256 df6a2de3fbc2bb174182069e5252b9e8434bbad963ce2e276c5d75d916986137 and contains only main.py, the Apache-2.0 license, and third-party notices. Its main.py matches Git commit 505f8133ce76abeff18782a02387fd28281770ce. Kaggle submission 56090534, message 11 fail-closed market curve 505f813, was uploaded on 2026-09-08 and is currently PENDING; validation and score are not yet claimed.
