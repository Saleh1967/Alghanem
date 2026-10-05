"""المبنيّاتُ والأدوات: سجلٌّ مغلقٌ يُكتب بالرسم المشكول وحده، والذرّاتُ مشتقّةٌ منه.

في الأصل (`slge.PARTICLES`، `slge_layers.PARTICLES_FULL`، `slge_layers.MABNI`) كُتب كلُّ
مدخلٍ مرّتين: رسمًا وذرّاتٍ باليد، فاختلفا في عشرة مداخل من `slge_layers` (مثلًا «هِيَ» ذرّاتُها
‎(ه، فتح)(ي، سكون)‎، و«إِنَّ» ذرّاتُها همزةٌ مفتوحة). وهنا مصدرٌ واحد: الرسم، تُشتقّ
منه الذرّاتُ بـ`to_atoms`، فلا يقع ذلك الصنفُ من الخطأ أصلًا.
"""

from __future__ import annotations

from typing import Final

from .cells import Cell, Word, licensed, shadow
from .orthography import begin, to_atoms

__all__ = [
    "CLOSED",
    "MABNI",
    "PARTICLES",
    "SKELETONS",
    "WASL",
    "entry",
    "skeleton_match",
]

PARTICLES: Final[tuple[str, ...]] = (
    "مِنْ", "عَنْ", "عَلَى", "قَدْ", "لَمْ", "لَنْ", "بَلْ", "هَلْ", "أَنْ", "إِنْ", "إِذَا",
    "إِذْ", "عِنْدَمَا", "كُلَّمَا", "حِينَئِذٍ", "لَا", "مَا", "وَ",
)
"""الأدواتُ المعلنة (ملحق ٦)."""

MABNI: Final[tuple[str, ...]] = (
    "هَذَا", "ذَانِكَ", "تِلْكَ", "أُولَئِكَ", "أَنَا", "نَحْنُ", "هُوَ", "هِيَ", "ذَا", "الَّذِي",
    "إِنَّ", "كَانَ", "لَكِنَّ", "أَيْنَ", "لَيْسَ", "مَنْ", "ثُمَّ",
)
"""المبنيّاتُ المعلنة (قوالب MASAQ)، بتصنيف الأصل نفسِه."""

WASL: Final[frozenset[str]] = frozenset({"الَّذِي"})
"""ما يبدأ بهمزة وصل: يُرخَّص بعد `begin` لا قبله."""

CLOSED: Final[dict[tuple[Cell, ...], str]] = {
    tuple(to_atoms(label)): label for label in (*PARTICLES, *MABNI)
}
"""ذرّاتُ كلّ مدخلٍ ← رسمُه."""

SKELETONS: Final[frozenset[str]] = frozenset({
    "MMM", "MSMM", "MMSMM", "MSMMM", "MSMSM", "MSMSMM",  # شبكة الأفعال I–X + Q
    "MSM", "MMSM", "MSMS", "MMSMSM",                    # مصادر/ممنوع نواة
    "MMSMS", "MMMSM", "MMMS",                           # جمع/نواسخ نواة
})


def entry(label: str) -> list[Cell]:
    """ذرّاتُ مدخلٍ في صورة نطقه: بعد قانون الابتداء إن بدأ بوصل."""

    cells = to_atoms(label)
    return begin(cells) if label in WASL else cells


def skeleton_match(word: Word) -> bool:
    """أهو من أنماط الجرد المعلنة (ظلًّا) ومرخَّص؟"""

    return licensed(word) and shadow(word) in SKELETONS
