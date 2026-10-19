"""يقرأ البنيةَ الليفيّةَ من البتّات: أحزمةٌ هي أم قطاعٌ جزئيّ؟"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from alghanem.arabic.fath_ayah_source_text import (  # noqa: E402
    FATH_AYAH_SOURCE_TEXT,
)
from alghanem.arabic.fatiha_source_text import FATIHA_LINES  # noqa: E402
from alghanem.arabic.haraka_fiber_structure import (  # noqa: E402
    FIBER_STRUCTURE_NAMED_RESIDUALS,
    THE_CONTESTED_MARKS,
    FiberProfile,
    fiber_profile_of,
    realized_sets_over_letters,
    total_sections_over,
    widening_effect_on,
)
from alghanem.arabic.written_haraka_mark import THE_IMPORTED_HARAKAT  # noqa: E402

_SCOPES = (
    ("الفاتحة", "\n".join(FATIHA_LINES)),
    ("الفتح ٢٩", FATH_AYAH_SOURCE_TEXT),
)


def main() -> None:
    print("البنيةُ الليفيّة: π: E → B مقروءًا من البتّات وحدَها")
    print("=" * 62)

    print("\n— شرطُ الحزمة: تساوي الألياف")
    for scope, text in _SCOPES:
        profile = fiber_profile_of(text, scope)
        print(
            f"  {scope:<10}: قاعدة {profile.base_points:>4} | ليفٌ خالٍ "
            f"{profile.empty_fibers:>3} | أحجامٌ {profile.distinct_sizes} "
            f"| متساوية: {profile.is_equinumerous}"
        )
    print("  ← حجمان لا حجمٌ واحد، فليست حزمةَ ألياف بل قطاعٌ جزئيّ.")

    print("\n— القطاعاتُ الكلّيّة")
    for scope, text in _SCOPES:
        profile = fiber_profile_of(text, scope)
        marked = FiberProfile(
            scope=scope, sizes=tuple(s for s in profile.sizes if s > 0)
        )
        print(
            f"  {scope:<10}: فوق القاعدة كلِّها {total_sections_over(profile)} "
            f"| فوق الموسومة وحدَها {total_sections_over(marked)}"
        )

    print("\n— السؤالان يفترقان: ما خمد في الإسقاط يتحرّك في الليف")
    for scope, text in _SCOPES:
        effect = widening_effect_on(text, scope)
        print(
            f"  {scope:<10}: حكمٌ ثنائيٌّ تحرّك {effect.decisions_moved:>2} "
            f"| ليفٌ اتّسع {effect.fibers_enlarged:>2} "
            f"(شدّة {effect.by_shadda}، خنجريّة {effect.by_dagger})"
        )
    print("  ← فإفرادُ الليف صنيعُ الاستيراد لا صنيعُ الرسم.")

    print("\n— أقصى ليفٍ تحت المجموعتين")
    for scope, text in _SCOPES:
        narrow = fiber_profile_of(text, scope)
        wide = fiber_profile_of(
            text, scope, marks=THE_IMPORTED_HARAKAT | THE_CONTESTED_MARKS
        )
        print(
            f"  {scope:<10}: بالسبع {narrow.largest_fiber} "
            f"| بالتسع {wide.largest_fiber} {wide.distinct_sizes}"
        )

    print("\n— لو أُلحق الغياب عضوًا (اصطلاحًا لا قياسًا)")
    for scope, text in _SCOPES:
        profile = fiber_profile_of(text, scope)
        adjoined = FiberProfile(
            scope=scope, sizes=tuple(max(size, 1) for size in profile.sizes)
        )
        print(
            f"  {scope:<10}: متساوية {adjoined.is_equinumerous} "
            f"| قطاعاتٌ كلّيّة {total_sections_over(adjoined)}"
        )

    print("\n— فوق الحروف القاعديّة: أحجامُ ما تحقّق")
    for scope, text in _SCOPES:
        realized = realized_sets_over_letters(text)
        sizes = dict(sorted(Counter(len(v) for v in realized.values()).items()))
        print(f"  {scope:<10}: حروفٌ {len(realized):>2} | أحجامٌ {sizes}")

    print("\n— ما لا تُثبِته هذه البنية، مُسمًّى")
    for key in FIBER_STRUCTURE_NAMED_RESIDUALS:
        print(f"  • {key}")


if __name__ == "__main__":
    main()
