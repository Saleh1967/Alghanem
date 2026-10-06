"""الأفعال الخمسة: الإعرابُ بالنون بتًّا واحدًا — مرآةُ `formal/Slge/Afal.lean`.

يَفْعَلَانِ، تَفْعَلَانِ، يَفْعَلُونَ، تَفْعَلُونَ، تَفْعَلِينَ. القانونُ الواحد: جذعُ المضارع + ضميرٌ متّصل
(ألف الاثنين، واو الجماعة، ياء المخاطبة) تسبقه الحركةُ من جنسه — قانونُ الأسماء الخمسة نفسُه —
ثمّ النونُ علامةَ الرفع، وحذفُها علامةَ النصب والجزم. المبرهَن: الرفعُ يُقرأ من الآخر (`moodOf_form`)؛
صورةُ النصب هي صورةُ الجزم بعينها (`nasb_eq_jazm`: الفرقُ نحويٌّ لا صرفيّ)؛ الضميرُ يُقرأ من حرفه
(`pronounOf_form`). وألفُ الفارقة بعد الواو بقيّةُ رسمٍ في الشهادة (`FARIQA`)، لا خانة.

الشواهد من شهادات البوّابة (2026-10-06): يَفْعَلُونَ، يَفْعَلُوا، تَعْلَمُونَ، تَعْلَمُوا، يَقْتَتِلَانِ،
تَخَافِي. ولا شاهدَ في المدوّنة لنصب الاثنين ولا لرفع المخاطبة (تَفْعَلِينَ): بالقانون (معلن).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from slge.cells import STATES, Cell, licensed

__all__ = ["FIVE", "MOODS", "PRONOUNS", "STEMS", "WITNESS", "Stem", "agree", "form", "mood_of",
           "pronoun_of"]

PRONOUNS: Final[tuple[str, str, str]] = ("الاثنين", "الجماعة", "المخاطبة")
MOODS: Final[tuple[str, str, str]] = ("رفع", "نصب", "جزم")
GLIDE: Final[dict[str, str]] = {"الاثنين": "ا", "الجماعة": "و", "المخاطبة": "ي"}
BEFORE: Final[dict[str, str]] = {"الاثنين": STATES[0], "الجماعة": STATES[2], "المخاطبة": STATES[1]}
PREFIX: Final[dict[str, str]] = {"غائب": "ي", "مخاطب": "ت"}
SUKUN: Final[str] = STATES[3]


@dataclass(frozen=True, slots=True)
class Stem:
    """جذعُ المضارع: حرفُ المضارعة (غائب/مخاطب) بحالته، الجسدُ خانات، والحرفُ الأخير بلا حالة."""

    name: str
    prefix: str
    prefix_state: str
    body: tuple[Cell, ...]
    last: str


def agree(prefix: str, pronoun: str) -> bool:
    """جدولُ المطابقة المعلَن: ياءُ المخاطبة للمخاطب وحدَه."""

    return not (prefix == "غائب" and pronoun == "المخاطبة")


FIVE: Final[tuple[tuple[str, str], ...]] = tuple(
    (pr, p) for pr in PREFIX for p in PRONOUNS if agree(pr, p)
)
"""الخمسة: (غائب، الاثنين)، (غائب، الجماعة)، (مخاطب، الاثنين)، (مخاطب، الجماعة)،
(مخاطب، المخاطبة)."""


def form(s: Stem, pronoun: str, mood: str) -> tuple[Cell, ...]:
    if not agree(s.prefix, pronoun):
        raise ValueError("PREFIX_PRONOUN_DISAGREE")
    if mood not in MOODS:
        raise ValueError("UNKNOWN_MOOD")
    nun: tuple[Cell, ...] = ()
    if mood == "رفع":
        nun = (("ن", STATES[1] if pronoun == "الاثنين" else STATES[0]),)
    return ((PREFIX[s.prefix], s.prefix_state), *s.body, (s.last, BEFORE[pronoun]),
            (GLIDE[pronoun], SUKUN), *nun)


def mood_of(word: tuple[Cell, ...]) -> str:
    """رفعٌ إن ختمت بالنون، وإلّا فنصبٌ/جزم (لا يُفرَّق بينهما صرفيًّا)."""

    return "رفع" if word and word[-1][0] == "ن" else "نصب/جزم"


def pronoun_of(word: tuple[Cell, ...]) -> str | None:
    w = word[:-1] if mood_of(word) == "رفع" else word
    if not w:
        return None
    for p, g in GLIDE.items():
        if w[-1] == (g, SUKUN):
            return p
    return None


_A, _I, _U = STATES[0], STATES[1], STATES[2]
STEMS: Final[tuple[Stem, ...]] = (
    Stem("يَفْعَلُ", "غائب", _A, (("ف", SUKUN), ("ع", _A)), "ل"),
    Stem("تَعْلَمُ", "مخاطب", _A, (("ع", SUKUN), ("ل", _A)), "م"),
    Stem("يَقْتَتِلُ", "غائب", _A, (("ق", SUKUN), ("ت", _A), ("ت", _I)), "ل"),
    Stem("تَخَافُ", "مخاطب", _A, (("خ", _A), ("ا", SUKUN)), "ف"),
)

WITNESS: Final[dict[str, tuple[Cell, ...]]] = {
    "يَفْعَلُونَ": (("ي", _A), ("ف", SUKUN), ("ع", _A), ("ل", _U), ("و", SUKUN), ("ن", _A)),
    "يَفْعَلُوا": (("ي", _A), ("ف", SUKUN), ("ع", _A), ("ل", _U), ("و", SUKUN)),
    "تَعْلَمُونَ": (("ت", _A), ("ع", SUKUN), ("ل", _A), ("م", _U), ("و", SUKUN), ("ن", _A)),
    "تَعْلَمُوا": (("ت", _A), ("ع", SUKUN), ("ل", _A), ("م", _U), ("و", SUKUN)),
    "يَقْتَتِلَانِ": (("ي", _A), ("ق", SUKUN), ("ت", _A), ("ت", _I), ("ل", _A), ("ا", SUKUN),
                   ("ن", _I)),
    "تَخَافِي": (("ت", _A), ("خ", _A), ("ا", SUKUN), ("ف", _I), ("ي", SUKUN)),
}
"""ذرّاتُ `gate.enter` خاناتٍ؛ يَفْعَلُوا وتَعْلَمُوا تحملان بقيّةَ FARIQA في شهادتيهما."""


def _check() -> None:
    for s in STEMS:
        for p in PRONOUNS:
            if not agree(s.prefix, p):
                continue
            for m in MOODS:
                w = form(s, p, m)
                if not licensed(w) or pronoun_of(w) != p:
                    raise ValueError(f"AFAL_LAW_BROKEN:{s.name}:{p}:{m}")


_check()
