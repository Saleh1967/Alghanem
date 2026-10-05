"""يقرأ عدَّ المزدوجات: ما قِيس، وما أُجيز ولم يقع، وما رُفض عن المدوّنة."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from alghanem.arabic.fath_ayah_source_text import (  # noqa: E402
    FATH_AYAH_SOURCE_TEXT,
)
from alghanem.arabic.fatiha_source_text import FATIHA_LINES  # noqa: E402
from alghanem.arabic.mark_pair_census import (  # noqa: E402
    MARK_PAIR_NAMED_RESIDUALS,
    THE_NINE_MARKS,
    combining_classes_are_all_distinct,
    corpus_run_is_available,
    pair_census_over,
    possible_pairs,
)

_SCOPES = (
    ("الفاتحة", "\n".join(FATIHA_LINES)),
    ("الفتح ٢٩", FATH_AYAH_SOURCE_TEXT),
)


def main() -> None:
    print("المزدوجُ الأكثرُ تكرارًا: مقيسٌ على المُودَعَين، مُهيَّأٌ للمدوّنة")
    print("=" * 64)

    print("\n— أوّلًا: هل بايتاتُ المدوّنة حاضرة؟")
    available = corpus_run_is_available()
    print(f"  حاضرة: {available}")
    if not available:
        print("  ← فلا يُنشَر ههنا رقمٌ عن المدوّنة، ولا يُقدَّر من المُودَعَين.")

    print("\n— ما يُجيزه اليونيكود (لا ما يقع)")
    print(f"  الأصنافُ اللاصقةُ متمايزةٌ كلُّها: {combining_classes_are_all_distinct()}")
    for mark in THE_NINE_MARKS:
        print(f"    U+{ord(mark):04X}  ccc={__import__('unicodedata').combining(mark)}")
    print(f"  المزدوجاتُ المُجازة: {len(possible_pairs())} — لا يمنع الجدولُ واحدًا")

    print("\n— المقيسُ على المُودَعَين، مرتَّبًا")
    for scope, text in _SCOPES:
        census = pair_census_over(text, scope)
        print(
            f"\n  {scope}: مواضعُ {census.positions_read} | مزدوجاتٌ "
            f"{census.total_pairs} | متحقّقٌ {census.realized} من 36"
        )
        for count in census.ranked:
            first, second = count.codepoints
            names = " + ".join(name.replace("ARABIC ", "") for name in count.names)
            print(f"    {first} {second}  {names:<34} {count.occurrences}")
        leaders = census.leaders
        if leaders:
            print(
                f"    ← المتصدّر: {' + '.join(leaders[0].codepoints)} "
                f"| بلا منازع: {census.the_lead_is_uncontested}"
            )

    print("\n— وما لم يقع ليس ممنوعًا")
    realized = {
        count.pair
        for scope, text in _SCOPES
        for count in pair_census_over(text, scope).ranked
    }
    print(
        f"  وقع في النصّين مجتمعين {len(realized)} من 36، ولم يقع {36 - len(realized)}"
    )

    print("\n— ما لا يُثبِته هذا العدّ، مُسمًّى")
    for key in MARK_PAIR_NAMED_RESIDUALS:
        print(f"  • {key}")


if __name__ == "__main__":
    main()
