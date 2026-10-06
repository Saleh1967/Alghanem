"""النداء: الأداةُ حرفٌ، والمنادى يُقرأ حكمُه من خانته الأخيرة — مرآةُ `formal/Slge/Nida.lean`.

**الأدوات** ستّ (أَ، أَيْ، أَيَا، هَيَا، يَا، وَا): حروفٌ مرخَّصة؛ والهمزةُ حرفٌ متّصل، ويَا تنتهي بألفٍ
ساكنة فوصلُها بكلّ مرخَّصٍ مرخَّص (`ya_junction`). **قانونُ المنادى** على الخانة الأخيرة من جذعه
(قبل الضمير المتّصل إن لحق): ضمٌّ بلا تنوين ⇒ مبنيٌّ على الضمّ في محلّ نصب؛ فتحٌ ⇒ معربٌ منصوب
(مضافٌ أو شبيهٌ به)؛ فتحٌ بتنوين ⇒ نكرةٌ غيرُ مقصودة؛ كسرٌ ⇒ مضافٌ إلى ياءٍ محذوفة؛ واوٌ/ألفٌ فنونٌ
⇒ مبنيٌّ على الواو/الألف. المبرهَن: التنوينُ لا يجامع البناء (`tanwin_never_bina`)، والضمُّ بناءٌ
(`damm_is_bina`). **الندبة** (حَسْرَتَاهْ) ساكنان متجاوران: غيرُ مرخَّصةٍ ثنائيًّا
(`nudba_not_binary_licensed`) — صورةُ وقفٍ للثلاثيّ في الغانم.

القياسُ على شريحة MASAQ المجمَّدة (489 منادًى بشهادات البوّابة) في `tools/gen_nida_index.py`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from slge.cells import STATES, Cell, licensed

__all__ = ["PARTICLES", "YA", "Particle", "has_tanwin", "hukm", "is_bina", "nudba", "ya_junction"]

_A, _I, _U, SUKUN = STATES
YA: Final[tuple[Cell, ...]] = (("ي", _A), ("ا", SUKUN))


@dataclass(frozen=True, slots=True)
class Particle:
    name: str
    cells: tuple[Cell, ...]
    masafa: str  # قريب | بعيد | قريب وبعيد | ندبة
    witnessed: bool


PARTICLES: Final[tuple[Particle, ...]] = (
    Particle("أَ", (("ء", _A),), "قريب", True),
    Particle("أَيْ", (("ء", _A), ("ي", SUKUN)), "قريب", False),
    Particle("أَيَا", (("ء", _A), ("ي", _A), ("ا", SUKUN)), "بعيد", False),
    Particle("هَيَا", (("ه", _A), ("ي", _A), ("ا", SUKUN)), "بعيد", False),
    Particle("يَا", YA, "قريب وبعيد", True),
    Particle("وَا", (("و", _A), ("ا", SUKUN)), "ندبة", False),
)


def has_tanwin(word: tuple[Cell, ...]) -> bool:
    """التنوين كما تُخرجه البوّابة: حركةٌ فنونٌ ساكنة في الآخر."""

    return len(word) >= 2 and word[-1] == ("ن", SUKUN) and word[-2][1] != SUKUN


def hukm(stem: tuple[Cell, ...]) -> str:
    """حكمُ المنادى من الخانة الأخيرة لجذعه."""

    if has_tanwin(stem):
        return "نكرة غير مقصودة (منصوب)" if stem[-2][1] == _A else "لا تقرؤه الخانة"
    if not stem:
        return "لا تقرؤه الخانة"
    n = stem[-1]
    if len(stem) >= 2:
        g = stem[-2]
        if n == ("ن", _A) and g == ("و", SUKUN):
            return "مبني على الواو"
        if n == ("ن", _I) and g == ("ا", SUKUN):
            return "مبني على الألف"
    return {_U: "مبني على الضم", _A: "معرب منصوب", _I: "مضاف إلى ياء محذوفة"}.get(
        n[1], "لا تقرؤه الخانة")


def is_bina(h: str) -> bool:
    return h.startswith("مبني")


def ya_junction(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    if not licensed(word):
        raise ValueError("MUNADA_NOT_LICENSED")
    return (*YA, *word)


def nudba(stem: tuple[Cell, ...]) -> tuple[Cell, ...]:
    """ألفٌ فهاءُ سكتٍ: صورةُ وقفٍ، غيرُ مرخَّصةٍ ثنائيًّا."""

    return (*stem, ("ا", SUKUN), ("ه", SUKUN))


def _check() -> None:
    assert all(licensed(p.cells) for p in PARTICLES)
    assert is_bina(hukm((("ء", _A), ("ا", SUKUN), ("د", _A), ("م", _U))))
    assert not licensed(nudba((("ح", _A), ("س", SUKUN), ("ر", _A), ("ت", _A))))


_check()
