"""قارئُ الولادة العمياء: المُعلَنُ ينقطع عند الحدود، والمقيسُ يعبُرها.

python examples/arabic/read_blind_skeleton_transport.py
"""

from __future__ import annotations

from alghanem.arabic.blind_skeleton_transport import (
    SKELETON_TRANSPORT_NAMED_RESIDUALS as RESIDUALS,
)
from alghanem.arabic.blind_skeleton_transport import (
    THE_DEPOSITS_READ,
    blind_sample_of,
    classes_that_transport,
    declared_classes_of,
    description_length_of,
    fused_alef_class_in,
    geometric_classes_of,
    the_canonical_fusion_is_realized_in,
)
from alghanem.arabic.font_deposit import AMIRI, SCHEHERAZADE, load_font
from alghanem.arabic.hidden_mark_population import fused_letters


def _render(classes: tuple[frozenset[str], ...]) -> str:
    return "  ".join(
        "".join(sorted(letters)) for letters in sorted(classes, key=lambda c: -len(c))
    )


def main() -> None:
    """يعرض ما يعلنه كلُّ خطّ، ثمّ ما يُقاس منه، ثمّ ما ينتقل بينها."""

    print("العيّنةُ العمياء: أرقامُ رسومٍ لا حروف")
    for filename in THE_DEPOSITS_READ:
        sample = blind_sample_of(filename)
        print(f"  {filename:<28}{len(sample):>4} رسمًا، أوّلُها {sample[:6]}")

    print()
    print("المُعلَنُ مقابلَ المقيس:")
    print(f"  {'الملفّ':<28}{'مُعلَن':>7}{'مقيس':>7}{'الخطّ كلُّه':>12}")
    for filename in THE_DEPOSITS_READ:
        print(
            f"  {filename:<28}{len(declared_classes_of(filename)):>7}"
            f"{len(geometric_classes_of(filename)):>7}"
            f"{len(geometric_classes_of(filename, True)):>12}"
        )

    print()
    print("ما يعلنه كلُّ خطّ:")
    for filename in THE_DEPOSITS_READ:
        print(f"  {filename:<28}{_render(declared_classes_of(filename))}")

    print()
    print("ما يُقاس من كلّ خطّ:")
    for filename in THE_DEPOSITS_READ:
        print(f"  {filename:<28}{_render(geometric_classes_of(filename))}")

    print()
    declared = classes_that_transport(declared=True)
    measured = classes_that_transport()
    print(f"ينتقل من المُعلَن إلى الثلاثة: {len(declared)}  {_render(declared) or '—'}")
    print(f"ينتقل من المقيس إلى الثلاثة: {len(measured)}  {_render(measured)}")

    print()
    print("الانتقالُ ثنائيًّا:")
    for first in THE_DEPOSITS_READ:
        for second in THE_DEPOSITS_READ:
            if first >= second:
                continue
            pair = (first, second)
            print(
                f"  {first[:12]:<13}∩ {second[:12]:<13}"
                f" مُعلَن {len(classes_that_transport(pair, declared=True)):>3}"
                f"   مقيس {len(classes_that_transport(pair)):>3}"
            )

    print()
    print("طولُ الوصف: كلُّ رسمٍ مستقلًّا مقابلَ كنتوراتٍ تُشارَك")
    print(f"  {'الملفّ':<28}{'M0':>8}{'M1':>8}{'إحالات':>8}{'التوفير':>10}")
    for filename in THE_DEPOSITS_READ:
        measure = description_length_of(filename)
        print(
            f"  {filename:<28}{measure.independent_points:>8}"
            f"{measure.shared_points:>8}{measure.references:>8}{measure.saving:>9.3f}%"
        )

    print()
    print("الجسرُ إلى الحروف المُلحَمة: هل تظهر بنيةُ الجدول هندسةً؟")
    print(f"  الجدولُ يُلحِم: {' '.join(fused_letters())}")
    for filename in THE_DEPOSITS_READ:
        found = "".join(sorted(fused_alef_class_in(filename)))
        realized = the_canonical_fusion_is_realized_in(filename)
        print(f"  {filename:<28}{found:<8} مطابقٌ للجدول: {'نعم' if realized else 'لا'}")

    amiri = load_font(AMIRI)
    hamza_above = amiri.glyph_for("\u0623")
    print()
    print("وتفصيلُ الخلاف، من البتات:")
    print(f"  Amiri  أ = {amiri.components_of(hamza_above)}")
    print("  أي جسمُ الألف نفسُه مزاحًا، لا صفرًا: إزاحةٌ غيرُ صفريّة هي الخبرُ الجديد.")
    scheherazade = load_font(SCHEHERAZADE)
    other = scheherazade.components_of(scheherazade.glyph_for("\u0623"))
    print(f"  Scheherazade أ = {other}")

    print()
    print("المتبقّياتُ المسمّاة:")
    for text in RESIDUALS.values():
        print(f"  - {text}")


if __name__ == "__main__":
    main()
