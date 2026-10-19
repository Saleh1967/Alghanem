"""قارئٌ لتوسيع المجتمع: أين تختفي العلامةُ عن تعداد العلامات.

python examples/arabic/read_hidden_mark_population.py
"""

from __future__ import annotations

import unicodedata

from alghanem.arabic.fath_ayah_source_text import FATH_AYAH_SOURCE_TEXT
from alghanem.arabic.fatiha_source_text import FATIHA_LINES
from alghanem.arabic.hidden_mark_population import (
    HAMZA_ABOVE,
    arabic_letters,
    classes_are_pairwise_distinct,
    combining_classes_of,
    foreign_decomposables,
    fused_bases,
    fused_letters,
    fusion_is_order_indifferent,
    fusion_passes_through,
    hidden_marks,
    letter_named_marks,
    normalization_delta,
    order_bearing_pairs,
    read_invisibility,
    the_identity_holds_on,
)
from alghanem.arabic.hidden_mark_population import (
    HIDDEN_MARK_NAMED_RESIDUALS as RESIDUALS,
)
from alghanem.arabic.mark_pair_census import THE_NINE_MARKS
from alghanem.arabic.written_haraka_mark import arabic_combining_marks


def main() -> None:
    """يعرض المجتمعَ الموسَّع، ثمّ العمى، ثمّ نقضَ قاعدة الترتيب."""

    letters = arabic_letters()
    fused = fused_letters()
    print("المجتمعُ الموسَّع:")
    print(f"  حروفُ `Lo` في كتل العربيّة: {len(letters)}")
    print(f"  علاماتُ `Mn` فيها:         {len(arabic_combining_marks())}")
    print(f"  حروفٌ مُلحَمة:              {len(fused)} ({len(fused) / len(letters):.3%})")

    print()
    print("الحروفُ المُلحَمةُ وعلاماتُها المخفيّة:")
    for letter in fused:
        carrier, mark = unicodedata.normalize("NFD", letter)
        print(
            f"  {letter} U+{ord(letter):04X}  =  {carrier} U+{ord(carrier):04X}"
            f"  +  U+{ord(mark):04X} {unicodedata.name(mark)}"
        )

    print()
    print("حواملُها:", "  ".join(f"{base}×{count}" for base, count in fused_bases()))

    print()
    print("العلاماتُ المخفيّةُ الثلاث:")
    for mark in hidden_marks():
        inside = "نعم" if mark in THE_NINE_MARKS else "لا"
        print(
            f"  U+{ord(mark):04X}  صنف {unicodedata.combining(mark):>3}"
            f"  ضمن التسع: {inside}  {unicodedata.name(mark)}"
        )

    print()
    print("العمى، مقيسًا على المُودَعَين:")
    print(f"  {'النطاق':<10}{'ظاهرة':>8}{'مخفيّة':>9}{'مكتوبة':>9}{'يراها التعداد':>16}")
    for scope, text in (
        ("الفاتحة", "\n".join(FATIHA_LINES)),
        ("الفتح ٢٩", FATH_AYAH_SOURCE_TEXT),
    ):
        reading = read_invisibility(text, scope)
        print(
            f"  {scope:<10}{reading.standalone:>8}{reading.hidden:>9}"
            f"{reading.written:>9}{reading.seen_by_a_mark_census:>16}"
        )

    print()
    print("نقضُ قاعدة الترتيب:")
    print(
        f"  التسع: أصنافٌ {combining_classes_of(THE_NINE_MARKS)}"
        f" متمايزة={classes_are_pairwise_distinct(THE_NINE_MARKS)}"
    )
    print(
        f"  الثلاث: أصنافٌ {combining_classes_of(hidden_marks())}"
        f" متمايزة={classes_are_pairwise_distinct(hidden_marks())}"
    )
    bearing = order_bearing_pairs(hidden_marks())
    print(
        "  مزدوجاتٌ يحمل ترتيبُها خبرًا:",
        " ".join("+".join(f"U+{ord(m):04X}" for m in pair) for pair in bearing) or "—",
    )

    print()
    print("التسويةُ تُلحِم عبرَ الحركة:")
    fatha = "\u064e"
    composed = unicodedata.normalize("NFC", f"\u0627{fatha}{HAMZA_ABOVE}")
    print(f"  ا + فتحة + همزة  →  {composed}  ({fusion_passes_through(fatha)})")
    print(f"  والترتيبان سواء: {fusion_is_order_indifferent(fatha)}")

    print()
    print("هُويّةُ التسوية:")
    for scope, text in (
        ("الفاتحة", "\n".join(FATIHA_LINES)),
        ("الفتح ٢٩", FATH_AYAH_SOURCE_TEXT),
    ):
        reading = read_invisibility(text, scope)
        print(
            f"  {scope:<10} حوامل {reading.hidden:>3} = فرقُ التسوية"
            f" {normalization_delta(text):>3}  ({the_identity_holds_on(text)})"
            f"  دخيلٌ متفكّك: {foreign_decomposables(text)}"
        )

    named = letter_named_marks()
    print()
    print(f"من `Mn` المئةِ والخمس، ما يسمّيه الجدولُ حرفًا: {len(named)}")
    for mark in named:
        print(f"  U+{ord(mark):04X}  {unicodedata.name(mark)}")

    print()
    print("البقايا المسمّاة:")
    for text in RESIDUALS.values():
        print(f"  - {text}")


if __name__ == "__main__":
    main()
