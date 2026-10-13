"""الصنفُ المغلق: وسمٌ يفصل المبنيّات عن الاسم والفعل — مرآةُ `Slge.Mughlaq` (ADR ٥٣).

الأدواتُ وحروفُ المعاني والضمائرُ وأسماءُ الإشارة والاستفهام والموصولُ، منفصلةً ومتّصلةً ومتّصلًا
بعضُها ببعض
(مِنْهُمْ، لَكُمْ، وَمِنْ، وَمِنْكُمْ، فِيمَا)، يقرؤها الموزِّع (`slge.tawzi`) من جداولها بقواعد
مسمّاة. والوسمُ ثلاثيّ
(`QISM`): **مغلق** إن قرأه الموزِّعُ بنواةٍ ليست ظرفًا، و**ظرف** إن لم يقرأه إلّا ظرفًا، و**مفتوح**
إن لم يقرأه —
فيُترك لقارئ الاسم والفعل (`maftuh_iff`، `mughlaq_iff`). والمغلقُ لا جذرَ يُحكم عليه منه
(`Qiraa.mughlaq_no_hukm`).

**إغلاقُ المعنى** (`closed_has_src`): لكلّ نواةٍ مغلقةٍ مصدرُ معنًى مسمًّى (`SOURCES`) — معانيها من
مبحث الحرف المختوم
(`maani`، «مختوم»)، أو عملُها من جدول الحروف الموحَّد، أو بابُها في أدوات الربط، أو بابُها ضميرًا
أو إشارةً أو استفهامًا أو
موصولًا (معلنةٌ في جداولها)، أو تركيبُها من حرفٍ ومَا/مَنْ. و`mana(m)` يجمع معنى القراءة كلّها:
السوابق، والنواة،
واللاحقة — نصًّا من جداولها، لا من الذاكرة.
"""

from __future__ import annotations

from typing import Final

from slge.cells import Cell
from slge.damair import ATTACHED_NASB, DETACHED_NASB, DETACHED_RAF
from slge.huruf import TABLE as HURUF
from slge.ishara import FORMS as ISHARA
from slge.istifham import FORMS as ISTIFHAM
from slge.maani import senses_of
from slge.marifa import MAWSUL
from slge.rawabit import BABS, PARTICLES, cells_of
from slge.tawzi import COMPOUNDS, HOSTS, MIM_WASL, TABLE, Mabni, tawzi
from slge.zaman import CONSTANTS as ZAMAN_CONSTANTS
from slge.zaman import STEMS as ZAMAN
from slge.zaman import forms_of
from slge.zuruf import CONSTANTS, STEMS, jarr, mudaf, qat

__all__ = ["QISM", "SOURCES", "ZARF_CELLS", "closed", "closed_core", "mana", "qism", "src"]

Word = tuple[Cell, ...]
QISM: Final[tuple[str, ...]] = ("مغلق", "ظرف", "مفتوح")
"""الوسمُ الثلاثيّ (`Mughlaq.Qism`)."""

SOURCES: Final[tuple[str, ...]] = ("نبهاني", "عمل", "ربط", "ضمير", "إشارة", "استفهام", "موصول",
                                   "تركيب")
"""مصادرُ المعنى بترتيبها (`Mughlaq.Src`)."""

ZARF_CELLS: Final[frozenset[Word]] = frozenset((
    *(form(z.stem) for z in STEMS for form in (mudaf, jarr, qat)), *CONSTANTS.values(),
    *(f for st in ZAMAN.values() for f in forms_of(st)), *(w for w, _ in ZAMAN_CONSTANTS.values())))
"""صورُ الظروف المودَعة (`zarfCells`)."""


def closed_core(core: Word) -> bool:
    """نواةٌ مغلقة: ما ليس ظرفًا (`closedCore`)."""

    return core not in ZARF_CELLS


def closed(w: Word) -> tuple[Mabni, ...]:
    """قراءاتُ الموزِّع المغلقة (`closed`)."""

    return tuple(m for m in tawzi(w) if closed_core(m.core))


def qism(w: Word) -> str:
    """الوسم (`qism`): مغلق، أو ظرف، أو مفتوح."""

    if closed(w):
        return "مغلق"
    return "ظرف" if tawzi(w) else "مفتوح"


_HURUF_IDX: Final[dict[Word, tuple[int, ...]]] = {}
for _i, _h in enumerate(HURUF):
    _HURUF_IDX[_h.cells] = (*_HURUF_IDX.get(_h.cells, ()), _i)
_PARTICLE: Final[dict[Word, str]] = {}
for _p in PARTICLES:
    _PARTICLE.setdefault(_p.cells, BABS[_p.bab])
_DAMIR: Final[dict[Word, str]] = {}
for _d in (*DETACHED_RAF, *DETACHED_NASB):
    _DAMIR.setdefault(_d.cells, f"{_d.group}: {_d.role}")
_ISHARA: Final[dict[Word, str]] = {}
for _f in ISHARA:
    _ISHARA.setdefault(_f.cells, f"{_f.bab}: {_f.dalala}")
_ISTIFHAM: Final[dict[Word, str]] = {}
for _q in ISTIFHAM:
    _ISTIFHAM.setdefault(_q.cells, _q.dalala)
_MAWSUL: Final[frozenset[Word]] = frozenset(MAWSUL.values())
_COMPOUND: Final[dict[Word, str]] = {w: n for _, n, w in COMPOUNDS}


def src(core: Word) -> str | None:
    """مصدرُ معنى النواة بالترتيب الثابت (`src`): حروفُ المعاني، ثمّ أدواتُ الربط، ثمّ الضمائر، ثمّ
    الإشارة، ثمّ
    الاستفهام، ثمّ الموصول، ثمّ التركيب."""

    if core in _HURUF_IDX:
        return "نبهاني" if any(senses_of(i) for i in _HURUF_IDX[core]) else "عمل"
    if core in _PARTICLE:
        return "ربط"
    if core in _DAMIR:
        return "ضمير"
    if core in _ISHARA:
        return "إشارة"
    if core in _ISTIFHAM:
        return "استفهام"
    if core in _MAWSUL:
        return "موصول"
    if core in _COMPOUND:
        return "تركيب"
    return None


def _core_mana(core: Word) -> tuple[str, ...]:
    s = src(core)
    if s in ("نبهاني", "عمل"):  # كلُّ مداخل الصورة: معانيها من المصدر، وإلّا عملُها — لا يُختار منها
        return tuple(dict.fromkeys(x for i in _HURUF_IDX[core] for x in
                                   (senses_of(i) or (f"عمل: {HURUF[i].amal or 'بلا عمل'}",))))
    if s == "ربط":
        return (f"باب: {_PARTICLE[core]}",)
    if s == "ضمير":
        return (_DAMIR[core],)
    if s == "إشارة":
        return (_ISHARA[core],)
    if s == "استفهام":
        return (_ISTIFHAM[core],)
    if s == "موصول":
        return ("اسم موصول",)
    if s == "تركيب":
        a, b = _COMPOUND[core].split("+")
        return (*_core_mana(cells_of(a)), f"تركيب مع {b}")
    return ()


_SUF_MANA: Final[dict[Word, str]] = {p.cells: f"{p.name}: {p.role}" for p in ATTACHED_NASB}


def _suf_mana(suf: Word) -> str:
    if suf in _SUF_MANA:
        return _SUF_MANA[suf]
    if suf[0] == ("ه", "كسر"):  # «فالهاء تُكسر إذا كان قبلها ياءٌ أو كسرة» (الكتاب س18128)
        return _suf_mana((("ه", "ضم"), *suf[1:])) + " (الهاءُ مكسورة)"
    if suf in MIM_WASL:
        return _SUF_MANA[(*suf[:-1], ("م", "سكون"))] + " (ميمُ الجمع موصولة)"
    if suf == (("ي", "سكون"),):
        return _SUF_MANA[(("ي", "فتح"),)] + " (ساكنة)"
    return _SUF_MANA.get(suf, "")


def mana(m: Mabni) -> tuple[tuple[str, tuple[str, ...]], ...]:
    """معنى القراءة المغلقة كلّها: كلُّ سابقةٍ بمعانيها، ثمّ النواةُ بمعانيها ومصدرها، ثمّ
    اللاحقة."""

    out: list[tuple[str, tuple[str, ...]]] = [("سابقة", _core_mana(p) or (f"سابقة {p}",))
                                              for p in m.pre]
    out.append((src(m.core) or "", _core_mana(m.core)))
    if m.suf:
        out.append(("لاحقة", (_suf_mana(m.suf),)))
    return tuple(out)


def _check() -> None:
    cores = [w for _, _, w in (*TABLE, *COMPOUNDS, *HOSTS)]
    assert all(src(k) is not None and _core_mana(k) for k in cores if closed_core(k))
    assert qism(cells_of("لَهُمْ")) == "مغلق" and qism(cells_of("وَهُمْ")) == "مغلق"
    assert qism(cells_of("عِنْدَهُ")) == "ظرف" and qism(cells_of("كَتَبَ")) == "مفتوح"


_check()
