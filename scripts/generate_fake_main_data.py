#!/usr/bin/env python3
"""Generate synthetic oTree `main` app CSV rows for mock analysis."""

from __future__ import annotations

import argparse
import csv
import random
import string
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path


NUM_ROUNDS = 16

# Fallback round effects by movie type:
# left-leaning movies push down, right-leaning push up, controls stay near neutral.
FALLBACK_ROUND_EFFECTS = [
    0.0,   # The Watchers (neutral political)
    -1.2,  # Under Cover
    -1.1,  # Silicon Circus
    1.2,   # Glory Before Dawn
    1.0,   # Divided We Stand
    -1.0,  # Broken Care
    -1.1,  # Workers' Strike
    1.1,   # Take Back the Streets
    1.0,   # Publicly Cancelled
    0.0,   # Outsmarted (neutral political)
    0.0,   # Controls below
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create a synthetic CSV with the same schema as an oTree main-app export, "
            "simulating many participants across 16 movie rounds."
        )
    )
    parser.add_argument(
        "--template-csv",
        type=Path,
        required=True,
        help="Path to an existing main-app export CSV used for header/schema template.",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        required=True,
        help="Path where synthetic CSV should be written.",
    )
    parser.add_argument(
        "--n-participants",
        type=int,
        default=500,
        help="How many synthetic participants to generate (default: 500).",
    )
    parser.add_argument(
        "--completion-rate",
        type=float,
        default=0.95,
        help="Probability a participant completes all 16 rounds (default: 0.95).",
    )
    parser.add_argument(
        "--complete-page-name",
        type=str,
        default="FinalForProlific",
        choices=["FinalForProlific", "Completion"],
        help="participant._current_page_name for completed participants (default: FinalForProlific).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducible generation (default: 42).",
    )
    parser.add_argument(
        "--id-start",
        type=int,
        default=1,
        help="Starting value for participant.id_in_session (default: 1).",
    )
    parser.add_argument(
        "--session-code",
        type=str,
        default="",
        help="Optional session.code override. If omitted, value from template is reused.",
    )
    parser.add_argument(
        "--start-time-utc",
        type=str,
        default="",
        help=(
            "Optional start time in 'YYYY-MM-DD HH:MM:SS.ffffff'. "
            "If omitted, template min timestamp is reused."
        ),
    )
    return parser.parse_args()


def clip_likert(value: float) -> int:
    return min(7, max(1, int(round(value))))


def random_code(rng: random.Random, existing: set[str], length: int = 8) -> str:
    alphabet = string.ascii_lowercase + string.digits
    while True:
        code = "".join(rng.choice(alphabet) for _ in range(length))
        if code not in existing:
            existing.add(code)
            return code


def parse_ts(text: str) -> datetime | None:
    text = text.strip()
    if not text:
        return None
    try:
        return datetime.strptime(text, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        return None


def infer_round_effects(template_rows: list[dict[str, str]]) -> list[float]:
    by_round: dict[int, list[int]] = defaultdict(list)
    for row in template_rows:
        try:
            round_no = int(row.get("subsession.round_number", ""))
        except ValueError:
            continue
        raw = row.get("player.movie_political_vibe", "").strip()
        if raw.isdigit():
            by_round[round_no].append(int(raw))

    effects: list[float] = []
    for idx in range(NUM_ROUNDS):
        round_no = idx + 1
        observed = by_round.get(round_no, [])
        fallback = FALLBACK_ROUND_EFFECTS[idx]
        if not observed:
            effects.append(fallback)
            continue

        mean_vibe = sum(observed) / len(observed)
        observed_effect = mean_vibe - 4.0
        # Small template data can be noisy; shrink toward fallback.
        weight = len(observed) / (len(observed) + 8)
        effects.append(weight * observed_effect + (1 - weight) * fallback)
    return effects


def generate_rows(
    header: list[str],
    template_stub: dict[str, str],
    round_effects: list[float],
    n_participants: int,
    completion_rate: float,
    complete_page_name: str,
    id_start: int,
    session_code: str,
    start_time: datetime,
    rng: random.Random,
    existing_codes: set[str],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    for participant_offset in range(n_participants):
        pid = id_start + participant_offset
        pcode = random_code(rng, existing_codes)

        is_complete = rng.random() < completion_rate
        if is_complete:
            completed_rounds = NUM_ROUNDS
            current_app_name = "post_experimental"
            current_page_name = complete_page_name
            max_page_index = "53"
            index_in_pages = "54" if current_page_name == "FinalForProlific" else "52"
        else:
            completed_rounds = rng.randint(0, NUM_ROUNDS - 1)
            current_app_name = "main"
            current_page_name = "MovieSurvey"
            max_page_index = "53"
            index_in_pages = str(3 + completed_rounds)

        # Participant-level latent traits.
        ideology = rng.gauss(0.0, 0.85)
        guessing_bias = rng.gauss(0.0, 0.30)
        start_ts = start_time + timedelta(seconds=rng.randint(0, n_participants * 25))

        for round_no in range(1, NUM_ROUNDS + 1):
            row = {k: template_stub.get(k, "") for k in header}

            row["participant.id_in_session"] = str(pid)
            row["participant.code"] = pcode
            row["participant._is_bot"] = "0"
            row["participant._index_in_pages"] = index_in_pages
            row["participant._max_page_index"] = max_page_index
            row["participant._current_app_name"] = current_app_name
            row["participant._current_page_name"] = current_page_name
            row["participant.time_started_utc"] = start_ts.strftime("%Y-%m-%d %H:%M:%S.%f")
            row["participant.visited"] = "1"
            row["participant.payoff"] = "0.0"

            row["player.id_in_group"] = "1"
            row["player.role"] = ""
            row["player.payoff"] = "0.0"
            row["group.id_in_subsession"] = "1"
            row["subsession.round_number"] = str(round_no)
            row["session.code"] = session_code

            if round_no <= completed_rounds:
                effect = round_effects[round_no - 1]
                own_mean = 4.0 + effect + ideology + rng.gauss(0.0, 0.20)
                own_vibe = clip_likert(rng.gauss(own_mean, 0.85))

                crowd_mean = 4.0 + effect + guessing_bias + rng.gauss(0.0, 0.20)
                guess_mean = 0.55 * crowd_mean + 0.45 * own_vibe + rng.gauss(0.0, 0.12)
                avg_guess = clip_likert(rng.gauss(guess_mean, 0.70))

                row["player.movie_political_vibe"] = str(own_vibe)
                row["player.average_movie_vibe"] = str(avg_guess)
            else:
                row["player.movie_political_vibe"] = ""
                row["player.average_movie_vibe"] = ""

            rows.append(row)

    return rows


def main() -> None:
    args = parse_args()
    rng = random.Random(args.seed)

    if args.n_participants <= 0:
        raise SystemExit("--n-participants must be > 0")
    if not (0.0 <= args.completion_rate <= 1.0):
        raise SystemExit("--completion-rate must be between 0 and 1")
    if not args.template_csv.exists():
        raise SystemExit(f"Template CSV not found: {args.template_csv}")

    with args.template_csv.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        if not header:
            raise SystemExit("Template CSV has no header.")
        template_rows = list(reader)

    template_stub = {k: "" for k in header}
    if template_rows:
        template_stub.update(template_rows[0])

    round_effects = infer_round_effects(template_rows)
    existing_codes = {r.get("participant.code", "") for r in template_rows if r.get("participant.code")}

    session_code = args.session_code or template_stub.get("session.code", "") or random_code(rng, set(), 8)

    if args.start_time_utc:
        start_time = datetime.strptime(args.start_time_utc, "%Y-%m-%d %H:%M:%S.%f")
    else:
        observed_ts = [parse_ts(r.get("participant.time_started_utc", "")) for r in template_rows]
        observed_ts = [ts for ts in observed_ts if ts is not None]
        start_time = min(observed_ts) if observed_ts else datetime.utcnow()

    synthetic_rows = generate_rows(
        header=header,
        template_stub=template_stub,
        round_effects=round_effects,
        n_participants=args.n_participants,
        completion_rate=args.completion_rate,
        complete_page_name=args.complete_page_name,
        id_start=args.id_start,
        session_code=session_code,
        start_time=start_time,
        rng=rng,
        existing_codes=existing_codes,
    )

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(synthetic_rows)

    completed_rows = sum(1 for r in synthetic_rows if r.get("player.movie_political_vibe"))
    completed_participants = completed_rows / NUM_ROUNDS
    print(f"Wrote {len(synthetic_rows)} rows to {args.output_csv}")
    print(f"Synthetic participants: {args.n_participants}")
    print(f"Participants with full/partial answers (expected): ~{completed_participants:.1f}")


if __name__ == "__main__":
    main()
