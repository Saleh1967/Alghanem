"""تشغيلُ جدول الحرف والحركة: سلّمُه، وخلوُّه، وفجوةُ الجشع عن الأمثل.

    python examples/arabic/run_letter_haraka_partition.py

والغرضُ أن يُرى الثلاثةُ في نفَسٍ واحد: كم خليّةً من المئة والاثنتي عشرة تمتلئ
كلّما اتّسع المصدر، وأيُّ الخلايا الخالية خلوُّها ندرةٌ وأيُّها يبقى مستغرَبًا
تحت هامشه، ثمّ كم يُخطئ الدمجُ الجشعُ الأمثلَ المُستقصى حيث يُمكِن الاستقصاء.

ولا يُرفَع ههنا حظرٌ ولا يُفكّ تجميد: بوّابةُ ماركوف على المدوّنة تُفحَص في
آخر الطبع، ويُطبَع أنّها باقيةٌ على حالها.
"""

from __future__ import annotations

from alghanem.arabic.letter_haraka_partition import (
    THE_DECLARED_HARAKAT,
    THE_DECLARED_PROBES,
    THE_HUNDRED_AND_TWELVE,
    THE_PREREGISTERED_GREEDY_CONDITION,
    THE_SURPRISE_FLOOR,
    SourceRung,
    absent_cells,
    bell_number,
    greedy_standing,
    measure_greedy_gap,
    stirling_second_kind,
    table_census,
    the_block_and_the_freeze_are_untouched,
    the_declared_probes,
)

_HARAKA_NAMES = {
    "\u064e": "فتحة",
    "\u064f": "ضمّة",
    "\u0650": "كسرة",
    "\u0652": "سكون",
}


def main() -> None:
    """اطبع السلّمَ، ثمّ الخلوَّ، ثمّ فجوةَ الجشع، ثمّ حالَ البوّابة."""

    print(
        f"عدّةُ الخلايا المُعلَنة: {THE_HUNDRED_AND_TWELVE} = 28 × "
        f"{len(THE_DECLARED_HARAKAT)}"
    )

    print("\n— السلّم —")
    for rung in SourceRung:
        census = table_census(rung)
        print(
            f"{census.rung.value}: {census.realized_cells}/{THE_HUNDRED_AND_TWELVE} "
            f"خليّة، {census.occurrences:,} وقوعًا، "
            f"{census.letters_present}/28 حرفًا"
        )

    print(f"\n— الخلايا الخالية عند أوسع درجة (عتبةُ الاستغراب {THE_SURPRISE_FLOOR}) —")
    for absence in absent_cells():
        print(
            f"{absence.letter} + {_HARAKA_NAMES[absence.haraka]}: "
            f"هامشُ الصفّ {absence.row_total:,}، المتوقَّع {absence.expected:.3f}، "
            f"احتمالُ الصفر {absence.probability_of_zero:.4f} — "
            f"{absence.standing.value}"
        )

    print("\n— فضاءُ القسمات —")
    for classes in (2, 3, 4, 5):
        print(f"S(28, {classes}) = {stirling_second_kind(28, classes):,}")
    print(f"B(28) = {bell_number(28):,}")

    print(f"\n— المسابات المُعلَنة —\n{THE_DECLARED_PROBES}")
    for probe in the_declared_probes():
        print(f"{probe.name}: {' '.join(probe.letters)}")

    print(f"\n— الشرطُ المُودَع —\n{THE_PREREGISTERED_GREEDY_CONDITION}")

    print("\n— الجشعُ في وجه الأمثل —")
    readings = measure_greedy_gap()
    for reading in readings:
        verdict = "بلغ" if reading.reached else "أخفق"
        print(
            f"{reading.probe} عند {reading.classes} أصناف: "
            f"جشع {reading.greedy_criterion:.3f}، أمثل "
            f"{reading.optimal_criterion:.3f}، فجوة {reading.gap:.3f} — {verdict}"
        )
    reached = sum(1 for reading in readings if reading.reached)
    print(f"بلغ في {reached} من {len(readings)} — {greedy_standing(readings).value}")

    print(
        "\nبوّابةُ ماركوف على المدوّنة بعد كلّ ما سبق: "
        f"{'محجوبةٌ كما كانت' if the_block_and_the_freeze_are_untouched() else 'تغيّرت'}"
    )


if __name__ == "__main__":
    main()
