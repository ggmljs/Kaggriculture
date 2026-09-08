#!/usr/bin/env python3
"""Fail-closed candidate-versus-baseline replay regression gate.

The Kaggriculture replay contains the action chosen for observation ``t`` in
frame ``t + 1``.  This utility turns one player from each recorded replay into
a deterministic, action-tape opponent and runs both a candidate and a frozen
baseline from both seats.  It is deliberately an *open-loop* regression
screen: a taped opponent cannot adapt after either policy diverges, so a pass
does not claim a live leaderboard improvement.  It does guarantee that a
candidate has not made any recorded matchup worse under this fixed corpus.

Replay data stays outside the submission artifact.  The production ``main.py``
is neither imported by Kaggle through this script nor modified by it.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any, Callable

from kaggle_environments import make


ROOT = Path(__file__).resolve().parent


def python_file(value: str) -> Path:
    path = Path(value).expanduser().resolve()
    if not path.is_file() or path.suffix != ".py":
        raise argparse.ArgumentTypeError(f"expected Python file: {value}")
    return path


def replay_file(value: str) -> Path:
    path = Path(value).expanduser().resolve()
    if not path.is_file() or path.suffix != ".json":
        raise argparse.ArgumentTypeError(f"expected replay JSON: {value}")
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=python_file, default=ROOT / "main.py")
    parser.add_argument(
        "--baseline",
        type=python_file,
        required=True,
    )
    parser.add_argument("--replay", type=replay_file, action="append", required=True)
    parser.add_argument(
        "--recorded-team",
        required=True,
        help="team whose recorded actions become the fixed opponent tape",
    )
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_agent(path: Path, label: str) -> Callable[[dict[str, Any]], dict[str, Any]]:
    module_name = f"replay_gate_{label}_{digest(path)[:12]}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    agent = getattr(module, "agent", None)
    if not callable(agent):
        raise RuntimeError(f"{path} does not expose callable agent(obs)")
    return agent


def action_tape(replay: dict[str, Any], team: str) -> tuple[int, list[dict[str, Any]]]:
    teams = list((replay.get("info") or {}).get("TeamNames") or [])
    if teams.count(team) != 1:
        raise ValueError(f"recorded team {team!r} must occur exactly once; got {teams}")
    seat = teams.index(team)
    frames = list(replay.get("steps") or [])
    if len(frames) < 2:
        raise ValueError("replay contains fewer than two frames")
    tape: list[dict[str, Any]] = []
    for step, frame in enumerate(frames[1:]):
        try:
            action = frame[seat].get("action") or {}
        except (IndexError, AttributeError) as error:
            raise ValueError(f"replay action missing at step {step}") from error
        tape.append(json.loads(json.dumps(action)))
    return seat, tape


def taped_agent(tape: list[dict[str, Any]]) -> Callable[[dict[str, Any]], dict[str, Any]]:
    def agent(observation: dict[str, Any]) -> dict[str, Any]:
        try:
            step = max(0, int(observation.get("step", 0) or 0))
        except (AttributeError, TypeError, ValueError):
            step = 0
        if step < len(tape):
            return json.loads(json.dumps(tape[step]))
        return {"farmer": ["PASS"], "hands": [], "market": []}

    return agent


def run_once(
    policy_path: Path,
    label: str,
    tape: list[dict[str, Any]],
    seed: int,
    policy_seat: int,
) -> dict[str, Any]:
    policy = load_agent(policy_path, label)
    players: list[Any] = [policy, taped_agent(tape)]
    if policy_seat == 1:
        players.reverse()
    environment = make(
        "kaggriculture",
        configuration={"episodeSteps": len(tape) + 1, "seed": seed},
        debug=False,
    )
    steps = environment.run(players)
    final = steps[-1]
    statuses = [str(state.status) for state in final]
    rewards = [float(state.reward or 0) for state in final]
    stderr = [
        {"turn": turn, "player": player, "text": log.get("stderr")}
        for turn, logs in enumerate(environment.logs)
        for player, log in enumerate(logs)
        if log.get("stderr")
    ]
    return {
        "reward": rewards[policy_seat],
        "opponent_reward": rewards[1 - policy_seat],
        "margin": rewards[policy_seat] - rewards[1 - policy_seat],
        "states": len(steps),
        "statuses": statuses,
        "stderr": stderr,
        "clean": len(steps) == len(tape) + 1 and statuses == ["DONE", "DONE"] and not stderr,
    }


def main() -> int:
    args = parse_args()
    rows: list[dict[str, Any]] = []
    for replay_path in args.replay:
        replay = json.loads(replay_path.read_text(encoding="utf-8"))
        source_seat, tape = action_tape(replay, args.recorded_team)
        seed = (replay.get("info") or {}).get("seed")
        if isinstance(seed, bool) or not isinstance(seed, int):
            raise ValueError(f"{replay_path}: missing integer info.seed")
        for seat in (0, 1):
            baseline = run_once(args.baseline, "baseline", tape, seed, seat)
            candidate = run_once(args.candidate, "candidate", tape, seed, seat)
            delta = candidate["margin"] - baseline["margin"]
            rows.append(
                {
                    "replay": str(replay_path),
                    "replay_sha256": digest(replay_path),
                    "episode_id": (replay.get("info") or {}).get("EpisodeId"),
                    "recorded_team": args.recorded_team,
                    "recorded_seat": source_seat,
                    "seed": seed,
                    "policy_seat": seat,
                    "baseline": baseline,
                    "candidate": candidate,
                    "margin_delta": delta,
                    "regressed": delta < 0,
                }
            )

    clean = all(row["baseline"]["clean"] and row["candidate"]["clean"] for row in rows)
    regressions = [row for row in rows if row["regressed"]]
    mean_delta = math.fsum(row["margin_delta"] for row in rows) / len(rows)
    result = {
        "manifest": {
            "candidate": str(args.candidate),
            "candidate_sha256": digest(args.candidate),
            "baseline": str(args.baseline),
            "baseline_sha256": digest(args.baseline),
            "recorded_team": args.recorded_team,
            "replays": [str(path) for path in args.replay],
        },
        "summary": {
            "comparisons": len(rows),
            "all_clean": clean,
            "regressions": len(regressions),
            "mean_margin_delta": mean_delta,
            "passed": clean and not regressions and mean_delta >= 0,
        },
        "rows": rows,
    }
    encoded = json.dumps(result, indent=2, sort_keys=True)
    print(encoded)
    if args.output:
        output = args.output if args.output.is_absolute() else Path.cwd() / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(encoded + "\n", encoding="utf-8")
    return 0 if result["summary"]["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
