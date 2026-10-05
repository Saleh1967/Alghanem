"""أعِد اشتقاقَ بصمات الحروف من مدوَّنة جذورٍ، وأخرِج التصادمَ مع خطِّ صفره.

هذا سكربتٌ مرجعيٌّ لا جزءٌ من النواة ولا سلطةٌ في الطبقة العربيّة: لا يُولِّد
شيئًا ولا يُجمِّد ولا يُصدر حكمًا. وهو يُصلح سكربتَ «بصمة الحرف» الأوّل بأن
يُخرِج ما كان يُخفيه:

* التصادماتُ مُسمّاةٌ، ومعها ما هو **لازمٌ من الجدولين المستورَدين** قبل قراءة
  أيّ مدوَّنة (تصادمُ (د، ق) منها).
* عددُ البصمات الفريدة مقرونٌ بخطِّ صفرٍ: كم فريدةً تُنتجها مدوَّناتٌ عشوائيّةٌ
  بنفس الحجم بنفس الخوارزميّة. فالرقمُ وحده لا يفصل البنيةَ عن الصدفة.
* الصفوفُ المستبعَدةُ معدودةٌ بأسبابها، فمدوَّنةٌ نصفُها مرفوضٌ لا تُقرأ صغيرة.

المدوَّنةُ **ليست** مضمَّنةً في المستودع: مرِّر مسارَ ملفِّ `csv` فيه العمودان
`root_full` و`root_type`::

    python examples/letter_fingerprint/measure_letter_fingerprints.py roots.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

from alghanem.arabic.letter_fingerprint import (
    FOUR_DIMENSIONS_ARE_NOT_FOUR_MEASUREMENTS_NOTE,
    LETTER_VOCABULARY,
    UNIQUENESS_WITHOUT_A_NULL_BASELINE_IS_HALF_A_MEASUREMENT_NOTE,
    compute_fingerprint_census,
    read_triliteral_roots,
    structural_collision_classes,
    uniform_null_unique_counts,
)

NULL_BASELINE_TRIALS = 20
NULL_BASELINE_SEED = 17


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("corpus", type=Path, help="مسارُ ملفِّ الجذور بصيغة csv")
    arguments = parser.parse_args()

    reading = read_triliteral_roots(arguments.corpus)
    if not reading.accepted_roots:
        print("لا جذرَ مقبولًا في المدوَّنة؛ لا رقمَ يُذكَر.")
        return 1

    census = compute_fingerprint_census(reading.accepted_roots)
    total = len(LETTER_VOCABULARY)
    unique = census.unique_fingerprint_count

    print(f"صفوفٌ مقروءة: {reading.row_count}، مقبولة: {census.corpus_size}")
    for reason, count in reading.exclusion_counts.items():
        print(f"  مستبعَد [{reason.value}]: {count}")

    print(f"بصماتٌ فريدة: {unique}/{total}")

    baseline = uniform_null_unique_counts(
        corpus_size=census.corpus_size,
        trials=NULL_BASELINE_TRIALS,
        seed=NULL_BASELINE_SEED,
    )
    print(
        "خطُّ الصفر (مدوَّنةٌ عشوائيّةٌ بنفس الحجم): "
        f"من {min(baseline)} إلى {max(baseline)} من {total} "
        f"في {NULL_BASELINE_TRIALS} محاولةً ببذرة {NULL_BASELINE_SEED}"
    )
    print(UNIQUENESS_WITHOUT_A_NULL_BASELINE_IS_HALF_A_MEASUREMENT_NOTE)
    print(FOUR_DIMENSIONS_ARE_NOT_FOUR_MEASUREMENTS_NOTE)

    forced = {key for key, _ in census.structurally_forced_collisions}
    if census.collisions:
        print("تصادماتٌ باقية، مُسمّاةٌ لا مُخفاة:")
        for key, letters in census.collisions:
            mark = "لازمٌ من الجدولين" if key in forced else "رصديّ"
            print(f"  {key}: {list(letters)} [{mark}]")
    else:
        print("صفرُ تصادمٍ في هذه المدوَّنة؛ وهو خاصّيّةُ جدولٍ لا هُويّةُ حرف.")

    print("خاناتُ الجدولين المستورَدين وحدَهما، قبل أيّ مدوَّنة:")
    for (is_ithlaq, role_count), letters in structural_collision_classes():
        if len(letters) > 1:
            print(f"  (ذلاقة={is_ithlaq}، أدوار={role_count}): {''.join(letters)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
