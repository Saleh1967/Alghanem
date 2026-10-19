"""قارئٌ لتوسيع عيّنة المزدوجات: أين ثبت الترتيبُ وأين انهار.

python examples/arabic/read_pair_sample_widening.py
"""

from __future__ import annotations

from alghanem.arabic.pair_sample_widening import (
    PAIR_SAMPLE_WIDENING_NAMED_RESIDUALS as RESIDUALS,
)
from alghanem.arabic.pair_sample_widening import (
    THE_TAIL_AUDITED,
    prose_scope_fingerprint,
    prose_scope_has_drifted,
    shadda_bearing_pairs,
    tanwin_initial_pairs,
    the_floor_is_not_arabic,
    the_floor_moves_across_the_ladder,
    the_leader_is_stable_across_the_ladder,
    the_least_frequent_arabic_pair,
    the_widening_ladder,
)


def main() -> None:
    """يعرض سُلَّمَ التوسيع، ثمّ مادّةَ القاع مفحوصةً، ثمّ البقايا."""

    ladder = the_widening_ladder()

    print("سُلَّمُ التوسيع:")
    print(f"  {'الدرجة':<24}{'مزدوجات':>9}{'متحقّق':>8}{'المتصدّر':>12}{'القاع':>12}")
    for census in ladder:
        lead = census.leaders[0]
        floor = census.ranked[-1]
        print(
            f"  {census.scope:<24}{census.total_pairs:>9}{census.realized:>6}/36"
            f"{lead.occurrences:>12}{floor.occurrences:>12}"
        )

    widest = ladder[-1]
    print()
    print(f"التوسيع: {widest.total_pairs // ladder[1].total_pairs} ضعفًا")
    print(f"المتصدّرُ ثابتٌ في الدرجات الثلاث: {the_leader_is_stable_across_the_ladder()}")
    print(f"والقاعُ يتزحزح في كلِّ درجة:        {the_floor_moves_across_the_ladder()}")

    body = shadda_bearing_pairs(widest)
    print()
    print("الجُرف:")
    share = body / widest.total_pairs
    print(f"  ما فيه شدّة: {body} من {widest.total_pairs} ({share:.3%})")
    print(f"  ما لا شدّة فيه: {widest.total_pairs - body}")

    print()
    print("القاعُ مفحوصًا:")
    for entry in THE_TAIL_AUDITED:
        mark = "عربيّة" if entry.is_arabic else "ليست عربيّة"
        print(f"  {'+'.join(entry.codepoints)}  {entry.occurrences:>3}  [{mark}]")
        print(f"      {entry.provenance}")

    least = the_least_frequent_arabic_pair()
    print()
    print(f"القاعُ المُعلَنُ ليس عربيّةً: {the_floor_is_not_arabic()}")
    print(f"وأقلُّ العربيِّ وقوعًا: {'+'.join(least.codepoints)} عند {least.occurrences}")

    print()
    print("فرقُ السِّجلّ (مزدوجاتٌ مبدوءةٌ بتنوين):")
    for census in (ladder[1], widest):
        print(f"  {census.scope:<24}{tanwin_initial_pairs(census):>8}")

    fingerprint = prose_scope_fingerprint()
    print()
    print(f"نطاقُ النثر: {fingerprint.files} ملفًّا، {fingerprint.text_bytes} بايتًا")
    print(f"زحزحةٌ عمّا قِيس عليه: {prose_scope_has_drifted()}")

    print()
    print("البقايا المسمّاة:")
    for text in RESIDUALS.values():
        print(f"  - {text}")


if __name__ == "__main__":
    main()
