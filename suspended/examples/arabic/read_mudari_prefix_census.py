"""يشغّل شرطَ حروف المضارعة المختومَ ويعرض تكذيبَه وسببَه المقيس."""

from __future__ import annotations

from alghanem.arabic.mudari_prefix_census import (
    MUDARI_CENSUS_NAMED_RESIDUALS,
    THE_ABSENT_IDENTIFIERS,
    THE_HAND_AUDITED_TOP_TYPES,
    THE_TANWIN_EXCLUDED_TYPES,
    CarrierKey,
    NounFilter,
    SlotReading,
    census_under,
    every_census,
    the_carrier_ladder_movement,
    the_expectation_verdict,
)
from alghanem.arabic.mudari_prefix_preregistration import (
    MUDARI_PREFIX_SPECIFICATION_DIGEST,
    STANDING,
    THE_DECLARED_CLAIMS,
    THE_ENTAILED_EXPECTATION_FLOOR,
    ClaimGenus,
)


def main() -> None:
    """أطبع الشرطَ المختوم، ثمّ الأعدادَ الأربعة، ثمّ الحكمَ وسببَه."""

    print(f"منزلةُ المواصفة: {STANDING.value}")
    print(f"بصمتُها المُجمَّدة: {MUDARI_PREFIX_SPECIFICATION_DIGEST}")
    print(f"الحدُّ المُعلَن قبل العدّ: {THE_ENTAILED_EXPECTATION_FLOOR:.0%}")

    print("\nالدعاوى بأجناس سندها:")
    for genus in ClaimGenus:
        names = [claim.name for claim in THE_DECLARED_CLAIMS if claim.genus is genus]
        print(f"  {genus.value}: {len(names)} — {'، '.join(names)}")

    print("\nالأعدادُ الأربعة:")
    for census in every_census():
        sealed = census.kasra_and_fatha_share(SlotReading.SEALED_PENULTIMATE)
        post_hoc = census.kasra_and_fatha_share(SlotReading.POST_HOC_THIRD_SLOT)
        print(
            f"  {census.carrier.value} · {census.noun_filter.value}: "
            f"{census.matches} مُطابِقًا في {census.distinct_surfaces} صورة"
        )
        print(f"    المختومةُ (قبل الأخيرة): {sealed:.2%}")
        print(f"    البعديّةُ (الثالثة): {post_hoc:.2%}")

    print(f"\nحكمُ التوقُّع المُعلَن: {the_expectation_verdict().value}")

    census = census_under(
        CarrierKey.NARROW_HAMZA_ON_ALIF, NounFilter.TANWIN_BEARING_EXCLUDED
    )
    print("\nسببُ السقوط — حروفُ الخانة قبل الأخيرة حين تخلو من علامة:")
    for letter, count in census.unmarked_penultimate_letters:
        print(f"  {letter}: {count}")

    kasra, fatha = census.kasra_to_fatha(SlotReading.POST_HOC_THIRD_SLOT)
    print(f"\nالقسمةُ المُعلَنةُ بلا توقُّع: كسرة {kasra} · فتحة {fatha}")

    print("\nحركةُ سلَّم الحامل:")
    for noun_filter, movement in the_carrier_ladder_movement().items():
        print(f"  {noun_filter.value}: {movement:+d}")

    print("\nالصورُ التي أخرجتها مصفاةُ التنوين:")
    print("  " + "، ".join(THE_TANWIN_EXCLUDED_TYPES))

    print("\nالعشرُ الأكثرُ تكرارًا، مفتَّشةً بالعين:")
    for audit in THE_HAND_AUDITED_TOP_TYPES:
        kind = "اسم" if audit.is_a_noun else "فعل"
        print(f"  {audit.surface} ({audit.occurrences}) — {kind}: {audit.note}")

    print("\nحروفُ المضارعة في المُطابِق:")
    for letter, count in census.prefix_letters:
        print(f"  {letter}: {count}")

    print("\nمُعرَّفاتٌ نُسبت إلينا وليست في بايتاتنا:")
    for name, note in THE_ABSENT_IDENTIFIERS.items():
        print(f"  {name}: {note}")

    print("\nالبقايا المسمّاة:")
    for token in MUDARI_CENSUS_NAMED_RESIDUALS:
        print(f"  {token}")


if __name__ == "__main__":
    main()
