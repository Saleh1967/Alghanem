"""`maqayis_links.py` — مُخرِجُ السجلّ الموحَّد لمرشَّحات المقاييس وروابطها.

وهذا هو **المستهلِك الفعليُّ** لآلة العشرين: لم تكن للآلة قبلَه قارئةٌ
خارجَ اختباراتها، فكان نجاحُ الربط نجاحًا في معمله لا في مجرى العمل. ومن
هنا يُوصَل الربطُ المستخرَجُ من المتن — بنودُ المصالحة ومعناها المُستخرَج —
بمرشَّحات حقل `semantic_axes` في سجلٍّ واحد، لكلِّ دالٍّ فيه صفُّه:
مرشَّحاتُه، ورابطُه المعتمَد، ورابطُه المعلَّق، وحدودُ تغطيته.

ويُحقَن المودَعُ ههنا لا في الآلة: `maqayis_segment_reconciliation` يستورد
من `maqayis_link_candidates`، فلو استورد الثاني الأوّلَ لدار الاستيراد.
فالمنفِّذُ هو الذي يَصِل الطرفين، وهذا وصلٌ مقصودٌ لا التفاف.

والاستعمال::

    python tools/maqayis_links.py             # يُعرَض الموجزُ ويُكتَب السجلّ
    python tools/maqayis_links.py --check     # يُصادَم المُودَعُ بما يولّده القرصُ
    python tools/maqayis_links.py --stdout    # يُطبَع السجلُّ ولا يُكتَب ملفّ

والمعلَّقُ يُعرَض معلَّقًا بسببه: لا يُطوى، ولا يُقرَأ الرابطُ الواحدُ
المعتمَدُ اعتمادًا لمعاني الدالّ كلِّها.
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

from alghanem.arabic.maqayis_link_candidates import (  # noqa: E402
    LinkCandidate,
    ReviewAttestation,
    SegmentAttribution,
    candidate_counts,
    report_rows,
)
from alghanem.arabic.maqayis_segment_reconciliation import (  # noqa: E402
    THE_ABAT_SEGMENTS,
    extracted_candidate,
    extracted_review,
)

REPORT_RELATIVE_PATH: Final[str] = "exhibits/maqayis-links/links_report.jsonl"


def deposited_links(root: Path | None = None) -> tuple[LinkCandidate, ...]:
    """الروابطُ المستخرَجةُ من المتن، مُعادَ بناؤها من البايتات عند كلّ نداء."""

    return (extracted_candidate(root or REPO_ROOT),)


def deposited_reviews() -> tuple[ReviewAttestation, ...]:
    """شهاداتُ المراجعة المودَعة؛ ومنفِّذُها مُصرَّحٌ بأنّه آليٌّ غيرُ مستقلّ."""

    return (extracted_review(),)


def deposited_segments() -> tuple[SegmentAttribution, ...]:
    """بنودُ المصالحة المودَعة: المحقَّقُ والأجنبيُّ والملتبسُ جميعًا."""

    return THE_ABAT_SEGMENTS


def unified_rows(root: Path | None = None) -> tuple[dict[str, object], ...]:
    """السجلُّ الموحَّد: مرشَّحاتُ الحقل وروابطُ المتن في جدولٍ واحد."""

    return report_rows(
        root or REPO_ROOT,
        links=deposited_links(root),
        reviews=deposited_reviews(),
        segments=deposited_segments(),
    )


def rendered_report(root: Path | None = None) -> str:
    """السجلُّ نصًّا: سطرٌ لكلِّ واقعة، بترميزٍ لا يهرب من العربيّة."""

    lines = [
        json.dumps(row, ensure_ascii=False, sort_keys=True)
        for row in unified_rows(root)
    ]
    return "\n".join(lines) + "\n"


def rendered_summary(root: Path | None = None) -> Iterator[str]:
    """موجزٌ بأعدادٍ مفصولةِ الوحدات؛ والمعلَّقُ يُعرَض ولا يُطوى."""

    counts = candidate_counts(
        root or REPO_ROOT,
        links=deposited_links(root),
        reviews=deposited_reviews(),
        segments=deposited_segments(),
    )
    yield "— السجلُّ الموحَّد لمرشَّحات المقاييس وروابطها —"
    for key, value in counts.items():
        yield f"{key.replace('_', ' ')}: {value}"
    yield (
        "وعددُ الشهادات غيرُ عددِ المعاني: شهادةُ مراجعةٍ واحدةٌ قد تُسنِد "
        "معنًى واحدًا، ولا يُعَدّ وجودُها تصحيحًا لها."
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="السجلُّ الموحَّد: مرشَّحاتُ حقل المحاور وروابطُ المتن"
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
        return 0
    if args.check:
        if not deposit.is_file():
            print(f"السجلُّ المُودَعُ غائب: {REPORT_RELATIVE_PATH}")
            return 1
        if deposit.read_text(encoding="utf-8") != report:
            print(
                "انزياح: السجلُّ المُودَعُ ليس ما يولّده القرصُ الآن — "
                "أعِد التوليد بـ`python tools/maqayis_links.py`"
            )
            return 1
    else:
        deposit.parent.mkdir(parents=True, exist_ok=True)
        deposit.write_text(report, encoding="utf-8")

    for line in rendered_summary(REPO_ROOT):
        print(line)

    if args.check:
        print("لا انزياح: السجلُّ المُودَعُ نابضٌ ببايتات مواده.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
