"""يقرأ المحمولَ المُقرَّر من اليونيكود: وزنَ استيراده، وقطعيّته، وحدَّه."""

from __future__ import annotations

import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from alghanem.arabic.fath_ayah_source_text import (  # noqa: E402
    FATH_AYAH_SOURCE_TEXT,
)
from alghanem.arabic.fatiha_source_text import FATIHA_LINES  # noqa: E402
from alghanem.arabic.written_haraka_mark import (  # noqa: E402
    CANONICAL_FORMS,
    THE_IMPORTED_HARAKAT,
    UNICODE_VERSION,
    WRITTEN_HARAKA_NAMED_RESIDUALS,
    census_of,
    compatibility_exceptions,
    has_written_haraka_mark,
    import_weight,
    imported_haraka_names,
    positions_of,
)


def main() -> None:
    print("HasWrittenHarakaMark: محمولٌ يُقرَّر من اليونيكود وحدَه")
    print("=" * 62)

    weight = import_weight()
    print(f"\n— وزنُ الاستيراد (يونيكود {UNICODE_VERSION})")
    print(f"  المجموعةُ المشتقّة (Mn في كتل العربيّة) : {weight.superset}")
    print(f"  المستورَدُ اختيارًا                     : {weight.selected}")
    print(f"  نصيبُه                                 : {weight.share:.3f}%")
    for codepoint, name in imported_haraka_names():
        print(f"    {codepoint}  {name}")
    for excluded in ("\u0651", "\u0670"):
        print(
            f"    [خارجٌ بالاختيار] U+{ord(excluded):04X}  "
            f"{unicodedata.name(excluded)} — وهو Mn كالسبع"
        )

    print("\n— القياسُ على المُودَعَين")
    for scope, text in (
        ("الفاتحة", "\n".join(FATIHA_LINES)),
        ("الفتح ٢٩", FATH_AYAH_SOURCE_TEXT),
    ):
        census = census_of(text, scope)
        print(
            f"  {scope:<10}: مواضع {census.total:>4} | موسوم {census.marked:>4} "
            f"| غيرُ موسوم {census.unmarked:>3} | {census.marked_share:.3f}%"
        )

    print("\n— ثباتُ الحكم تحت الصورتين القانونيّتين")
    for scope, text in (
        ("الفاتحة", "\n".join(FATIHA_LINES)),
        ("الفتح ٢٩", FATH_AYAH_SOURCE_TEXT),
    ):
        readings = [census_of(text, scope, form=form) for form in CANONICAL_FORMS]
        agree = readings[0].marked == readings[1].marked
        print(
            f"  {scope:<10}: NFC {readings[0].marked} | NFD {readings[1].marked} "
            f"| متطابقان: {agree}"
        )

    print("\n— أثرُ إدخال ما أُخرج بالاختيار، مقيسًا")
    for scope, text in (
        ("الفاتحة", "\n".join(FATIHA_LINES)),
        ("الفتح ٢٩", FATH_AYAH_SOURCE_TEXT),
    ):
        widened = THE_IMPORTED_HARAKAT | {"\u0651", "\u0670"}
        moved = sum(
            1
            for position in positions_of(text)
            if bool(set(position.marks) & widened) != has_written_haraka_mark(position)
        )
        print(f"  {scope:<10}: مواضعُ تحرّك حكمُها = {moved}")

    breaks = len(compatibility_exceptions())
    print(f"\n— حدُّ البرهان: تنكسر التسويةُ التوافقيّة في {breaks} نقطة")
    for character in compatibility_exceptions()[:3]:
        target = [f"U+{ord(x):04X}" for x in unicodedata.normalize("NFKD", character)]
        print(f"    U+{ord(character):04X} {unicodedata.name(character)} → {target}")
    print("    …")

    print("\n— ما لا يُثبِته هذا المحمول، مُسمًّى")
    for key in WRITTEN_HARAKA_NAMED_RESIDUALS:
        print(f"  • {key}")


if __name__ == "__main__":
    main()
