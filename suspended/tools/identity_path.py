"""أداةُ إعادة تشغيل مسار الهويّة: تُخرِج الأثرَ ملفًّا، ولا تكتب في الشجرة.

الاستعمال:

    python tools/identity_path.py --output identity-traces

تُنتِج `identity-traces/run.jsonl` و`identity-traces/trace.txt`؛ والمجلّدُ
خارجَ الشجرة المُتابَعة إن شئت. والأداةُ **لا تُودِع** شيئًا ولا تُصادِم رقمًا.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for entry in (ROOT, ROOT / "src"):
    if str(entry) not in sys.path:
        sys.path.insert(0, str(entry))

from alghanem.arabic.identity_path_run import full_run  # noqa: E402


def rows() -> list[dict[str, object]]:
    """صفوفُ الأثر: محطّةٌ محطّة، كلٌّ بمخرجها لا بخلاصتها."""

    outcome = full_run(ROOT)
    found: list[dict[str, object]] = [
        {"stage": "representation_witness", **witness.as_canonical_content()}
        for witness in outcome.witnesses
    ]
    found.extend(
        {"stage": "canonical_reading", **reading.as_canonical_content()}
        for reading in outcome.readings
    )
    found.extend(
        {"stage": "naming_candidate", **candidate.as_canonical_content()}
        for candidate in outcome.zayd_candidates
    )
    found.append(
        {
            "stage": "identity_revision",
            "city_names": list(outcome.city_names),
            "linked_before": list(outcome.linked_before),
            "linked_after_link": list(outcome.linked_after_link),
            "linked_after_retraction": list(outcome.linked_after_retraction),
            "arrival_before_link": outcome.arrival_before_link,
            "arrival_after_link": outcome.arrival_after_link,
            "arrival_after_retraction": outcome.arrival_after_retraction,
            "arrival_after_independent": outcome.arrival_after_independent,
            "suspended_by_policy": list(outcome.suspended_by_policy),
        }
    )
    return found


def main(argv: list[str] | None = None) -> int:
    """اكتب الأثرَ في المجلّد المطلوب، وأعد صفرًا إن تمّ."""

    parser = argparse.ArgumentParser(description="إعادةُ تشغيل مسار الهويّة")
    parser.add_argument("--output", required=True, help="مجلّدُ الأثر")
    arguments = parser.parse_args(argv)
    destination = Path(arguments.output)
    destination.mkdir(parents=True, exist_ok=True)
    found = rows()
    (destination / "run.jsonl").write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in found)
        + "\n",
        encoding="utf-8",
    )
    outcome = full_run(ROOT)
    (destination / "trace.txt").write_text(
        "\n".join(outcome.trace) + "\n", encoding="utf-8"
    )
    for line in outcome.trace:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
