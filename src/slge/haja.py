"""توقيعُ الحاجة وقسمةُ المفرد بمعيار الحاجة (ADR ٥٦) — مرآةُ `formal/Slge/Haja.lean`.

لكلّ بابٍ من المغلق قائمةُ حاجاتٍ: (الجهة، ما يقضيها، الاتّصال، مفتاحُ المرساة في `haja_table`). والصدارةُ
للشرط
والاستفهام. ولكلّ مدخلٍ من جدول الحروف الموحَّد (68) بابُه بترتيبه.
"""

from __future__ import annotations

from typing import Final

from slge.cells import Cell
from slge.damair import DETACHED_NASB, DETACHED_RAF
from slge.haja_table import KEYS
from slge.huruf import TABLE as HURUF
from slge.istifham import FORMS as ISTIFHAM
from slge.marifa import MAWSUL
from slge.rawabit import cells_of

__all__ = ["BABS", "BAB_ALL", "HARF_BABS", "NEEDS", "PARTICLES", "SADR", "Haja", "bab_of",
           "core_babs", "mufrad_of"]

Haja = tuple[str, str, bool, str]
"""(الجهة: قبل/بعد/أيّ، ما يقضيها: اسم/فعل/جزء، الاتّصال، المفتاح)."""

BAB_ALL: Final[tuple[str, ...]] = (
    "mustaqill", "jarr", "mushabbaha", "atf", "istithna", "shart", "nafy", "amilFil", "tanbih",
    "jawab", "rad", "istifham", "nida", "damir", "mawsul", "ghayrMusnad")

NEEDS: Final[dict[str, tuple[Haja, ...]]] = {
    "mustaqill": (),
    "jarr": (("bad", "ism", False, "H_IDAFA"), ("ayy", "fil", False, "H_IDAFA")),
    "mushabbaha": (("bad", "ism", False, "H_MUSHABBAHA"), ("bad", "juz", False, "H_MUSHABBAHA")),
    "atf": (("qabl", "juz", False, "H_ATF"), ("bad", "juz", False, "H_ATF")),
    "istithna": (("qabl", "juz", True, "H_ISTITHNA"), ("bad", "ism", True, "H_ISTITHNA")),
    "shart": (("bad", "juz", True, "H_SHART"), ("ayy", "juz", True, "H_SHART")),
    "nafy": (("bad", "juz", False, "H_NAFY"),),
    "amilFil": (("bad", "fil", False, "H_ISTIQBAL"),),
    "tanbih": (("bad", "juz", False, "H_TANBIH"),),
    "jawab": (("qabl", "juz", False, "H_JAWAB"),),
    "rad": (("qabl", "juz", False, "H_RAD"),),
    "istifham": (("bad", "juz", False, "H_SADARA"),),
    "nida": (("bad", "ism", False, "H_NIDA"),),
    "damir": (("ayy", "ism", False, "H_DAMIR"),),
    "mawsul": (("bad", "juz", False, "H_MAWSUL"),),
    "ghayrMusnad": (),
}

SADR: Final[frozenset[str]] = frozenset({"shart", "istifham"})
HARF_BABS: Final[frozenset[str]] = frozenset({
    "jarr", "mushabbaha", "atf", "istithna", "shart", "nafy", "amilFil", "tanbih", "jawab", "rad",
    "istifham", "nida"})

BABS: Final[tuple[str, ...]] = (
    *("jarr",) * 13, *("istithna",) * 3, "jarr",
    *("mushabbaha",) * 6, *("nida",) * 6, "mushabbaha", "ghayrMusnad",
    *("amilFil",) * 12, "shart", "shart", "amilFil", "amilFil", "rad", "amilFil",
    *("atf",) * 9, "istifham", "istifham", "nafy", "nafy", "amilFil", "amilFil", "nafy",
    "ghayrMusnad", "tanbih", "tanbih")
"""بابُ كلّ مدخلٍ من `huruf.TABLE` بترتيبه."""


PARTICLES: Final[tuple[tuple[str, str, str, str], ...]] = (
    ("إِلَّا", "إلا", "istithna", "H_ISTITHNA"), ("غَيْرُ", "غير", "istithna", "H_ISTITHNA"),
    ("إِذَا", "إذا", "shart", "H_SHART"), ("مَنْ", "من", "shart", "H_SHART"),
    ("مَهْمَا", "مهما", "shart", "H_SHART"), ("حَيْثُمَا", "حيثما", "shart", "H_SHART"),
    ("أَيْنَمَا", "أينما", "shart", "H_SHART"), ("لَوْ", "لو", "shart", "H_LAW"),
    ("نَعَمْ", "نعم", "jawab", "H_JAWAB_HURUF"), ("بَلَى", "بلى", "jawab", "H_JAWAB_HURUF"),
    ("أَجَلْ", "أجل", "jawab", "H_JAWAB_HURUF"))
"""أدواتُ الربط خارج الجدول الموحَّد ببابها حيث يسمّيها المرسى بلفظها: (الصورة، الاسمُ في النصّ، الباب،
المفتاح)."""


def bab_of(i: int) -> str:
    return BABS[i] if 0 <= i < len(BABS) else "ghayrMusnad"


Word = tuple[Cell, ...]
_HURUF_IDX: Final[dict[Word, tuple[int, ...]]] = {}
for _i, _h in enumerate(HURUF):
    _HURUF_IDX[_h.cells] = (*_HURUF_IDX.get(_h.cells, ()), _i)
_PART: Final[dict[Word, str]] = {cells_of(v): b for v, _, b, _ in PARTICLES}
_DAMIR: Final[frozenset[Word]] = frozenset(d.cells for d in (*DETACHED_RAF, *DETACHED_NASB))
_ISTIFHAM: Final[frozenset[Word]] = frozenset(q.cells for q in ISTIFHAM)
_MAWSUL: Final[frozenset[Word]] = frozenset(MAWSUL.values())


def core_babs(core: Word) -> tuple[str, ...]:
    """أبوابُ نواةٍ مغلقة بخاناتها: حروفُ الجدول الموحَّد، وأداةُ ربطٍ يسمّيها المرسى، والضميرُ
    والاستفهامُ والموصول من جداولها — كلُّ ما يطابق، بلا تكرار؛ وما لا يطابق شيئًا «بلا سند»."""

    out = [bab_of(i) for i in _HURUF_IDX.get(core, ())]
    if core in _PART:
        out.append(_PART[core])
    if core in _ISTIFHAM:
        out.append("istifham")
    if core in _MAWSUL:
        out.append("mawsul")
    if core in _DAMIR:
        out.append("damir")
    return tuple(dict.fromkeys(out)) or ("ghayrMusnad",)


def mufrad_of(bab: str, hayaa: bool) -> str:
    """حرفٌ، أو مضمرٌ (لا يستقلّ)، أو فعلٌ (بهيئته)، أو اسم."""

    if bab in HARF_BABS:
        return "harf"
    if NEEDS[bab]:
        return "mudmar"
    return "fil" if hayaa else "ism"


def _check() -> None:
    assert len(BABS) == len(HURUF) == 68
    assert set(NEEDS) == set(BAB_ALL)
    assert all(h[3] in KEYS for hs in NEEDS.values() for h in hs)
    assert all(k in KEYS and b in HARF_BABS for _, _, b, k in PARTICLES)


_check()
