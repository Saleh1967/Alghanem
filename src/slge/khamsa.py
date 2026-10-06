"""الأسماء الخمسة: الإعرابُ بالحروف دالّةً — مرآةُ `formal/Slge/Khamsa.lean`.

أبٌ، أخٌ، حمٌ، فوٌ، ذو. القانونُ الواحد: الاسمُ **جذعٌ** وخانةُ إعراب: آخرُ الجذع يأخذ الحركةَ
القصيرةَ للحالة، ويليه حرفُ المدّ من جنسها ساكنًا (ضم↔و، فتح↔ا، كسر↔ي). فالإعرابُ بالحروف
إطالةُ الإعراب بالحركات (`Slge.Khamsa.madd_matches_short`)، والحالةُ تُقرأ من الصورة بعينها
(`caseOf_form`). الشروطُ (مفرد، مكبَّر، مضافٌ لغير ياء المتكلّم) معلَنةٌ في `Ctx`؛ ما خرج عنها
فبالحركة والتنوين أو بياء المتكلّم؛ وما لم يُغطَّ (الجمعُ والتصغير) يُردّ `None` لا تخمينًا.

الشواهد: صورُ أب وأخ وذو من شهادات بوّابة الغانم (2026-10-06؛ الرفعُ بلاحقةٍ لأنّ المجرّدَ خارج
المجال): أَبُوهُمْ، أَبَا، أَبِي، أَخُوهُمْ، أَخَا، أَخِي، ذُو، ذَا، ذِي، أَخٌ. وحمٌ وفوٌ بالقانون
نفسِه (معلن: ليسا في المدوّنة).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from slge.cells import ALPHABET, STATES, Cell, licensed

__all__ = ["CASES", "KHAMSA", "WITNESS", "Ctx", "Stem", "case_of", "decline", "form", "tanwin",
           "with_ya"]

CASES: Final[tuple[str, str, str]] = ("رفع", "نصب", "جر")
SHORT: Final[dict[str, str]] = {"رفع": STATES[2], "نصب": STATES[0], "جر": STATES[1]}
MADD: Final[dict[str, str]] = {"رفع": "و", "نصب": "ا", "جر": "ي"}
SUKUN: Final[str] = STATES[3]


@dataclass(frozen=True, slots=True)
class Stem:
    """الجذع: رأسُه خاناتٌ، وآخرُه حاملٌ يحمل الإعراب."""

    name: str
    head: tuple[Cell, ...]
    last: str


@dataclass(frozen=True, slots=True)
class Ctx:
    """شروطُ الإعراب بالحروف، معلَنةً لا مستنبَطة."""

    mufrad: bool = True
    mukabbar: bool = True
    mudaf: bool = True
    ila_ya: bool = False

    @property
    def by_letters(self) -> bool:
        return self.mufrad and self.mukabbar and self.mudaf and not self.ila_ya


def form(s: Stem, case: str) -> tuple[Cell, ...]:
    """الصورةُ بالحروف."""

    return (*s.head, (s.last, SHORT[case]), (MADD[case], SUKUN))


def with_ya(s: Stem) -> tuple[Cell, ...]:
    """المضافُ إلى ياء المتكلّم: صورةٌ واحدةٌ للحالات."""

    return (*s.head, (s.last, STATES[1]), ("ي", SUKUN))


def tanwin(s: Stem, case: str) -> tuple[Cell, ...]:
    """غيرُ المضاف: الحركةُ ونونُ التنوين ساكنة."""

    return (*s.head, (s.last, SHORT[case]), ("ن", SUKUN))


def case_of(word: tuple[Cell, ...]) -> str | None:
    """الحالةُ من حرف المدّ الأخير."""

    if not word:
        return None
    for case, madd in MADD.items():
        if word[-1] == (madd, SUKUN):
            return case
    return None


def decline(s: Stem, ctx: Ctx, case: str) -> tuple[Cell, ...] | None:
    if case not in CASES:
        raise ValueError("UNKNOWN_CASE")
    if ctx.by_letters:
        return form(s, case)
    if ctx.mufrad and ctx.mukabbar and ctx.mudaf and ctx.ila_ya:
        return with_ya(s)
    if ctx.mufrad and ctx.mukabbar and not ctx.mudaf:
        return tanwin(s, case)
    return None


_A = STATES[0]
KHAMSA: Final[tuple[Stem, ...]] = (
    Stem("أب", (("ء", _A),), "ب"),
    Stem("أخ", (("ء", _A),), "خ"),
    Stem("حم", (("ح", _A),), "م"),
    Stem("فو", (), "ف"),
    Stem("ذو", (), "ذ"),
)

WITNESS: Final[dict[str, tuple[Cell, ...]]] = {
    "أَبُوهُمْ": (("ء", _A), ("ب", STATES[2]), ("و", SUKUN), ("ه", STATES[2]), ("م", SUKUN)),
    "أَبَا": (("ء", _A), ("ب", _A), ("ا", SUKUN)),
    "أَبِي": (("ء", _A), ("ب", STATES[1]), ("ي", SUKUN)),
    "أَخُوهُمْ": (("ء", _A), ("خ", STATES[2]), ("و", SUKUN), ("ه", STATES[2]), ("م", SUKUN)),
    "أَخَا": (("ء", _A), ("خ", _A), ("ا", SUKUN)),
    "أَخِي": (("ء", _A), ("خ", STATES[1]), ("ي", SUKUN)),
    "ذُو": (("ذ", STATES[2]), ("و", SUKUN)),
    "ذَا": (("ذ", _A), ("ا", SUKUN)),
    "ذِي": (("ذ", STATES[1]), ("ي", SUKUN)),
    "أَخٌ": (("ء", _A), ("خ", STATES[2]), ("ن", SUKUN)),
}
"""ذرّاتُ البوّابة (`gate.enter`، الغانم `claude/official-gate`، 2026-10-06) خاناتٍ."""


def _check() -> None:
    for s in KHAMSA:
        for case in CASES:
            if not licensed(form(s, case)) or case_of(form(s, case)) != case:
                raise ValueError(f"KHAMSA_LAW_BROKEN:{s.name}:{case}")
    assert all(c in ALPHABET for c in MADD.values())


_check()
