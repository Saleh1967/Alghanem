"""أعِد اشتقاقَ قياسِ الخطّ على جذور المقاييس المُودَعة، ولا تقرأه من سطرٍ مكتوب.

بايتاتُ `maqayis_by_root_csv_999.csv` في هذه الشجرة ومُبصَّمة، فهذا التشغيلُ
لا ينتظر ملفًّا ولا متغيّرَ بيئة::

    python examples/arabic/measure_maqayis_root_round_trip.py

يُشتَقّ المجتمعُ من البايتات بقاعدة عدِّ الإيداع نفسِها — `root_full`
المتمايزةُ من صفوف «ثلاثي» — ثمّ تُشغَّل عليه الطبقاتُ الستُّ نفسُها التي
شُغِّلت على إيداع الفاتحة، ويُطبع الجدولُ بموضع توقّفه وأمثلةٍ من صنف توقّفه.
ويفشل التشغيلُ إن خالف `figures_digest` المُجمَّدَ في الشجرة.

**ما يُقرأ هنا موضعُ الوقوف لا النسبة**: السلاسلُ غيرُ مشكولة، فتبلغ الحامل
والحالةَ كاملةً وتقف عند المقطع بعلّةٍ واحدةٍ مُسمّاة. وذلك حدٌّ على دالّة
التقطيع في هذه الشجرة، لا دعوًى على العربية غيرِ المشكولة، ولا على عدد الجذور
فيها: العددُ عددٌ في هذا الملفّ تحت قاعدة عدِّه وعلى رسمِه.

هذا المثالُ مرجعٌ لا جزءٌ من النواة: لا يُولّد كائنًا، ولا يرخّص انتقالًا، ولا
يُصدر شهادة، ولا يستورد من `alghanem.kernel`.
"""

from __future__ import annotations

import sys
from typing import Final

from alghanem.arabic.arabic_round_trip_v1 import (
    LayerOutcome,
    measure_round_trip,
    render_table,
)
from alghanem.arabic.maqayis_root_round_trip import (
    MAQAYIS_TRILATERAL_ROOT_ROUND_TRIP,
    TRILATERAL_ROOT_ORDERING_RULE,
    measure_trilateral_roots,
    trilateral_root_tokens,
)
from alghanem.arabic.maqayis_root_table_deposit import (
    FROZEN_ROOT_TABLE,
    TRILATERAL_ROOT_COUNTING_RULE,
    MaqayisRootTableError,
)

_EXAMPLES_PER_CLASS: Final[int] = 5


def main() -> int:
    try:
        tokens = trilateral_root_tokens()
        measurement = measure_trilateral_roots()
    except MaqayisRootTableError as refused:
        print(f"بايتاتُ جدول الجذور غيرُ مقروءة: {refused}", file=sys.stderr)
        return 2

    print(f"source: {FROZEN_ROOT_TABLE.source_name}")
    print(f"sha256: {FROZEN_ROOT_TABLE.sha256_hex}")
    print(f"counting rule: {TRILATERAL_ROOT_COUNTING_RULE}")
    print(f"ordering rule: {TRILATERAL_ROOT_ORDERING_RULE}")
    print()

    table = measure_round_trip(tokens)
    print(render_table(table))
    for halt in table.halt_profile:
        reason = "" if halt.refusal is None else f"/{halt.refusal.value}"
        print(f"  {halt.layer.value}/{halt.outcome.value}{reason}: {halt.count}")
    shown: list[str] = []
    for trace in table.traces:
        if trace.outcome is LayerOutcome.RECONSTRUCTED:
            continue
        if len(shown) >= _EXAMPLES_PER_CLASS:
            break
        shown.append(tokens[trace.token_index].decode("utf-8", errors="replace"))
    if shown:
        print(f"  examples of the halting class: {' '.join(shown)}")
    print(
        f"  end-to-end reconstructed: {measurement.end_to_end_reconstructed}"
        f"/{measurement.token_total}"
    )
    print(f"  figures digest: {measurement.figures_digest}")
    print()

    if not measurement.agrees_in_figures_with(MAQAYIS_TRILATERAL_ROOT_ROUND_TRIP):
        print(
            "انحرفت الأرقامُ عن المُجمَّد في الشجرة؛ والانحرافُ يُوقِف التشغيل",
            file=sys.stderr,
        )
        return 1
    print("الأرقامُ أُعيد اشتقاقُها كما جُمِّدت، ولا رقمَ منها مقروءٌ من سطر.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
