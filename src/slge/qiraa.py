"""القراءةُ الموحَّدة: الحرفُ أوّلًا، والجذعُ على الصورة وعلى أصلها المردود — مرآةُ `Slge.Qiraa` (ADR ٤٢).

ثلاثةُ قرّاءٍ قائمين تُركَّب ولا يُزاد عليها: ما يقرؤه الموزِّعُ ونواتُه من حروف المعاني (`huruf.TABLE`) حرفٌ
فلا جذرَ يُحكم عليه منه (`harf_no_hukm`) ولا تُحذف قراءاتُ الجذع (`jidh_sub_qiraa`: عَلَى/عَلَا، خَلَا)؛
والجذعُ على الصورة كما هي (`jidh`)؛ والجذعُ على الأصل الذي ردّت `sawabiq` ساقطَه في الوصل (غيرَ أل،
فالجذعُ يقرؤها أصلًا): كلُّ قراءةٍ تُردّ بعينها (`qiraa_restores`) وأصلُها يصعد إلى جذعها (`qiraa_ascends`).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from slge.cells import Cell
from slge.huruf import TABLE as HURUF
from slge.jidh import Reading as JReading
from slge.jidh import jidh
from slge.maqayis import attested
from slge.mughlaq import closed
from slge.sawabiq import Reading as SReading
from slge.sawabiq import sawabiq
from slge.tawzi import Mabni, tawzi

__all__ = ["HURUF_CELLS", "Reading", "harf", "hukm_readings", "lifted", "qiraa", "rank", "restored"]

Word = tuple[Cell, ...]
HURUF_CELLS: Final[frozenset[Word]] = frozenset(h.cells for h in HURUF)
"""خاناتُ حروف المعاني (`hurufCells`)."""


def harf(w: Word) -> tuple[Mabni, ...]:
    """قراءاتُ الموزِّع التي نواتُها من حروف المعاني."""

    return tuple(m for m in tawzi(w) if m.core in HURUF_CELLS)


@dataclass(frozen=True, slots=True)
class Reading:
    """قراءةُ الجذع، وقراءةُ السابقة التي رُدّ بها الأصلُ إن كانت (`via`)."""

    via: SReading | None
    r: JReading


def lifted(w: Word) -> tuple[SReading, ...]:
    """قراءاتُ السابقة الموصولة غيرِ أل: ما سقط فيها رُدّ."""

    return tuple(m for m in sawabiq(w) if m.under != m.rest and m.kind != "AL")


def restored(w: Word) -> tuple[Reading, ...]:
    """الجذعُ على الأصل المردود (`pre ++ under`)."""

    return tuple(Reading(m, r) for m in lifted(w) for r in jidh((*m.pre, *m.under)))


def qiraa(w: Word) -> tuple[Reading, ...]:
    """الجذعُ على الصورة ثمّ على الأصل المردود."""

    return (*(Reading(None, r) for r in jidh(w)), *restored(w))


def hukm_readings(w: Word) -> tuple[Reading, ...]:
    """لا شيءَ إن قرأ الموزِّعُ الكلمةَ حرفًا أو مغلقًا (`Qiraa.mughlaq_no_hukm`، ADR ٥٣)، وإلّا
    القراءةُ الموحَّدة كلُّها."""

    return () if harf(w) or closed(w) else qiraa(w)


def rank(qs: tuple[Reading, ...]) -> tuple[Reading, ...]:
    """المشهودُ في المقاييس أوّلًا بترتيبٍ ثابت؛ لا قراءةَ تسقط (`Maqayis.mem_rank`)."""

    return (*(q for q in qs if attested(q.r)), *(q for q in qs if not attested(q.r)))


def _check() -> None:
    from slge.rawabit import cells_of

    for t in ("فِي", "مِنْ", "إِلَى", "لَكُمْ"):
        assert harf(cells_of(t)) and not hukm_readings(cells_of(t)), t
    kataba = cells_of("كَتَبَ")
    assert not harf(kataba) and hukm_readings(kataba) == qiraa(kataba)
    famshu = cells_of("فَمْشُوْ")
    rs = restored(famshu)
    assert rs and all(q.via is not None and q.r.restore() == (*q.via.pre, *q.via.under) for q in rs)
    for q in qiraa(famshu):
        assert q.via is None or (*q.via.pre, *q.via.rest) == famshu


_check()
