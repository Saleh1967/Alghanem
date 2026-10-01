#!/usr/bin/env python3
"""منفّذُ قاموس مصطلحات النحو — يُخرِج السجلَّ والتقرير من بايتاتٍ مختومة.

    python tools/lexicon_extract.py            # يكتب الوديعتَين
    python tools/lexicon_extract.py --check    # يُصادم الوديعتَين بالقرص
    python tools/lexicon_extract.py --stdout   # يطبع السجلّ ولا يكتب

والمادّتان النحويّتان ليستا في هذه الشجرة؛ يُحَلّ مسارُهما بمتغيّرَين مسمَّيَين:

    export ALGHANEM_MUGHNI_PATH=/absolute/path/to/mughni-labib
    export ALGHANEM_SIBAWAYH_PATH=/absolute/path/to/kitab-sibawayhi

ومن لا بايتاتِ عنده لا يخرج له بندٌ ولا رقم: الغيابُ رفضُ إخراجٍ لا قيمةٌ
افتراضيّة، والختمُ يُقابَل قبل أوّل قراءة.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))

from alghanem.arabic.nahw_lexicon import (  # noqa: E402
    THE_DEFERRED_LINE,
    report_markdown,
    report_rows,
    seal_readings,
)

LEDGER_PATH = REPOSITORY_ROOT / "exhibits" / "nahw-lexicon" / "nahw_lexicon.jsonl"
REPORT_PATH = REPOSITORY_ROOT / "exhibits" / "nahw-lexicon" / "LEXICON-REPORT.md"


def render_ledger() -> str:
    """نصُّ `nahw_lexicon.jsonl` كاملًا: بندٌ في كلّ سطرٍ، بترتيبِ استخراجه."""

    lines = [
        json.dumps(row, ensure_ascii=False, sort_keys=True) for row in report_rows()
    ]
    return "\n".join(lines) + "\n" if lines else ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="يُصادم الوديعتَين بما يُولَّد الآن ولا يكتب شيئًا",
    )
    parser.add_argument(
        "--stdout", action="store_true", help="يطبع السجلّ ولا يكتب وديعةً"
    )
    arguments = parser.parse_args()

    for reading in seal_readings():
        print(
            f"[ختم] {reading.material.key}: {reading.standing.value}",
            file=sys.stderr,
        )

    ledger = render_ledger()
    report = report_markdown()

    if arguments.stdout:
        print(ledger, end="")
        return 0

    if arguments.check:
        drifted = False
        for path, generated in ((LEDGER_PATH, ledger), (REPORT_PATH, report)):
            deposited = path.read_text(encoding="utf-8") if path.is_file() else ""
            if deposited != generated:
                drifted = True
                print(f"[انحراف] {path.relative_to(REPOSITORY_ROOT)}", file=sys.stderr)
        if drifted:
            return 1
        print("[سليم] الوديعتان تطابقان ما يُولَّد الآن.", file=sys.stderr)
        return 0

    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    LEDGER_PATH.write_text(ledger, encoding="utf-8")
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"[كُتِب] {LEDGER_PATH.relative_to(REPOSITORY_ROOT)}", file=sys.stderr)
    print(f"[كُتِب] {REPORT_PATH.relative_to(REPOSITORY_ROOT)}", file=sys.stderr)
    print(THE_DEFERRED_LINE, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
