"""`bridge.py` — منفّذُ جسر الدالِّ وحدَه بالمدلول وحدَه، ومُخرِجُ سجلّه.

يُعيد هذا المنفّذُ اشتقاقَ كلِّ رقمٍ في التقرير من البايتات المختومة عند كلّ
تشغيل، ثمّ يكتب `bridge_report.jsonl` سطرًا لكلِّ واقعة. ولا رقمَ ههنا منقولٌ
من نثر: من شغّله على المواد نفسِها أعاد السجلَّ بحروفه.

والاستعمال::

    python tools/bridge.py             # يُعرَض التقريرُ ويُكتَب السجلّ
    python tools/bridge.py --check     # يُصادَم المُودَعُ بما يولّده القرصُ الآن
    python tools/bridge.py --stdout    # يُطبَع السجلُّ ولا يُكتَب ملفّ

والساقطُ يُعرَض ساقطًا: القنواتُ المقفلةُ تُسمّى بشرطها، والصفرُ يُعرَض ومعه
الطريقُ الذي بلغه.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Final

REPO_ROOT: Final[Path] = Path(__file__).resolve().parent.parent
SRC_ROOT: Final[Path] = REPO_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from alghanem.arabic.dal_madlul_bridge import (  # noqa: E402
    THE_DEFERRED_LINE,
    THE_SUSPENSION_SAMPLE_RULE,
    bridge_metrics,
    report_rows,
)

REPORT_RELATIVE_PATH: Final[str] = "exhibits/dal-madlul-bridge/bridge_report.jsonl"


def rendered_report(root: Path | None = None) -> str:
    """السجلُّ نصًّا: سطرٌ لكلِّ واقعة، بترميزٍ لا يهرب من العربيّة."""

    lines = [
        json.dumps(row, ensure_ascii=False, sort_keys=True) for row in report_rows(root)
    ]
    return "\n".join(lines) + "\n"


def rendered_metrics(root: Path | None = None) -> Iterator[str]:
    """تقريرُ المقاييس بأرقامه الخام؛ وغيرُ المقيس يُسمّى غيرَ مقيسٍ لا صفرًا."""

    metrics = bridge_metrics(root)
    yield "— تقريرُ مقاييس جسر الدالّ وحدَه بالمدلول وحدَه —"
    yield f"قاعدةُ العيّنة: {THE_SUSPENSION_SAMPLE_RULE}"
    yield f"الدوالُّ المفحوصة: {metrics.dals_examined}"
    yield f"الأزواجُ المُخرَجة: {metrics.pairs_emitted}"
    yield f"المعلَّقون (صنفٌ أوّل، محفوظون): {metrics.suspended_count}"
    yield (
        "التغطية (دوالٌّ لها مدلولُ مطابقةٍ واحدٌ على الأقلّ): "
        f"{metrics.coverage_numerator}/{metrics.coverage_denominator}"
        + (
            f" = {metrics.coverage:.4f}"
            if metrics.coverage is not None
            else " = غيرُ مقيسة"
        )
    )
    yield (
        "الصدق (عيّنةُ فحص السمع): "
        + (
            f"{metrics.truth_rate:.4f}"
            if metrics.truth_rate is not None
            else f"غيرُ مقيسٍ — حجمُ العيّنة {metrics.audited_sample_size}"
        )
    )
    yield (
        "انضباطُ الأقسام: "
        + (
            f"{metrics.section_discipline:.4f}"
            if metrics.section_discipline is not None
            else "غيرُ مقيسٍ — لا مدلولَ خرج فيُوسَم"
        )
    )
    yield (
        f"الانفصال: أزواجٌ جُمع فيها الدالُّ والمدلولُ مفهومًا = "
        f"{metrics.concept_joins}"
        + (
            " — وهذا صفرٌ بلغه الخلوُّ لا انضباطٌ مُمتحَن"
            if metrics.the_zero_was_reached_by_vacancy
            else ""
        )
    )
    yield THE_DEFERRED_LINE


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="جسرُ الدالِّ وحدَه بالمدلول وحدَه: سجلٌّ ومقاييسُ خام"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="يُخرِج 1 إن خالف السجلُّ المُودَعُ ما يولّده القرصُ الآن",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="يطبع السجلَّ ولا يكتب ملفًّا",
    )
    args = parser.parse_args(argv)

    report = rendered_report(REPO_ROOT)
    deposit = REPO_ROOT / REPORT_RELATIVE_PATH

    if args.stdout:
        sys.stdout.write(report)
    elif args.check:
        if not deposit.is_file():
            print(f"السجلُّ المُودَعُ غائب: {REPORT_RELATIVE_PATH}")
            return 1
        if deposit.read_text(encoding="utf-8") != report:
            print(
                "انزياح: السجلُّ المُودَعُ ليس ما يولّده القرصُ الآن — "
                f"أعِد التوليد بـ`python tools/bridge.py` ({REPORT_RELATIVE_PATH})"
            )
            return 1
    else:
        deposit.parent.mkdir(parents=True, exist_ok=True)
        deposit.write_text(report, encoding="utf-8")

    for line in rendered_metrics(REPO_ROOT):
        print(line)

    if args.check:
        print("لا انزياح: السجلُّ المُودَعُ نابضٌ ببايتات مواده.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
