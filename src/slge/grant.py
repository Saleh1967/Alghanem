"""المنح: لا اسمَ قبل قبضته — مرآةُ `formal/Slge/Grant.lean`.

قانونُ الجسر كما وصل في `tarkib/bridge.py` (تسليم 2026-10-06): ‎grants = Λ(observables, witness,
check)‎. وكان هناك الفحصُ **نصًّا** (`check_tool: str`) والحكمُ **حقلًا** (`check_verdict: "PASS"`)،
فقَبِل `grant()` جسرًا زُوِّر حكمُه بسطرٍ واحد (`dataclasses.replace(b, check_verdict="PASS")`)؛
ومن سبعة جسورٍ لم يمرّ إلّا الأوّل، وليس لما بعده أداةٌ تعمل. وهنا الفحصُ **دالّةٌ على الخانات**
والمنحُ **نتيجتُها**: لا حقلَ يُملأ، ولا حكمَ يُحمَل. ما لا دالّةَ له لا يُصاغ جسرًا أصلًا؛ يُذكر
في `DECLARED` اسمًا معلَنًا بدَينه.

الجسرُ المودَع الأوّل: **المرسوم** — فحصُه الترخيصُ نفسُه (`cells.licensed`)، فلا يُمنح إلّا
لمرخَّصٍ، وهو بالجسر `Admissible` في الـ116 (`Slge.Grant.mursam_sound`).
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Final

from slge.cells import Cell, licensed

__all__ = ["DECLARED", "LADDER", "MURSAM", "Bridge", "Granted", "Refusal", "climb", "grant"]

Check = Callable[[Sequence[Cell]], bool]


@dataclass(frozen=True, slots=True)
class Bridge:
    """الجسر: اسمُه، ما يمنحه، فحصُه دالّةً، شاهدُه، وبقيّتُه المعلَنة."""

    name: str
    grants: str
    check: Check
    witness: str | None = None
    residual: str = ""


@dataclass(frozen=True, slots=True)
class Granted:
    """ما مُنح: الاسمُ والجسرُ والخاناتُ التي جرى عليها الفحص."""

    grants: str
    via: str
    cells: tuple[Cell, ...]
    residual: str


@dataclass(frozen=True, slots=True)
class Refusal:
    """رفضٌ مسمًّى."""

    code: str
    bridge: str


def grant(b: Bridge, cells: Sequence[Cell]) -> Granted | Refusal:
    """يمنح إن أعاد الفحصُ `True` الآن؛ وإلّا رفضٌ باسمه. لا طريقَ ثالث."""

    if not b.check(cells):
        return Refusal("CHECK-REFUSED", b.name)
    return Granted(b.grants, b.name, tuple(cells), b.residual)


MURSAM: Final[Bridge] = Bridge(
    "b-mursam", "مرسوم", licensed, None, "المقدَّر والساكنُ في الصدر خارج المنح: دَينُ قراءة",
)
"""الدرجةُ الأولى: المرسوم. فحصُه الترخيص؛ مبرهَنٌ `Slge.Grant.mursam_sound`."""

LADDER: Final[tuple[Bridge, ...]] = (MURSAM,)
"""السُّلَّم: كلُّ درجةٍ تشترط ما تحتها (`Slge.Grant.Ladder`). درجةٌ واحدةٌ لها فحصٌ يعمل."""


def climb(cells: Sequence[Cell], ladder: Sequence[Bridge] = LADDER) -> tuple[Granted, ...]:
    """يصعد السُّلَّمَ درجةً درجة ويقف عند أوّل رفض؛ فلا درجةَ تُمنح فوق مرفوضة."""

    out: list[Granted] = []
    for b in ladder:
        g = grant(b, cells)
        if isinstance(g, Refusal):
            break
        out.append(g)
    return tuple(out)


DECLARED: Final[dict[str, str]] = {
    "b-R-TN": "اسم:مؤكّد — يلزمه فحصُ أفعالٍ مبصومٌ لم يصل",
    "b-mustarajac": "مبنيّ:مسترجَع — يلزمه عدّادُ الفائض في الاتّجاهين",
    "b-sinf": "صنف-الكلمة — يلزمه معجمٌ مبصوم؛ ومقيسٌ هنا أنّ الشكلَ لا يكفي (H=1.17 بت)",
    "b-irab-wazifa": "فاعل/مفعول — الرقمُ المنقول (92.3%) بلا أداةٍ ولا مرجعٍ محجوب",
    "b-jumla": "جملة — حدُّها دَينٌ (TAXONOMY-DEBT) حتى يُودَع",
    "b-ifada": "إفادة-موقَّعة — بلا توقيع",
}
"""الجسورُ الستّةُ التي وصلت بلا فحصٍ يعمل: أسماءٌ معلَنةٌ بدَينها، لا جسور. تعود جسرًا حين
يصير فحصُها دالّةً على خاناتٍ من شهادات البوّابة مقيسةً على MASAQ."""
