"""الموزِّع: قبل قارئ القوالب تُسأل الكلمةُ أهي من المبنيّات المودَعة — مرآةُ `Slge.Tawzi`.

الحروفُ والضمائرُ وأسماءُ الإشارة والاستفهام والموصولُ وظروفُ المكان والزمان المودَعة لا قالبَ لها؛
قراءتُها من جدولها بعينه: الكلمةُ = سوابقُ (من `jidh.PROCLITICS`، حتى اثنتين) + مبنيٌّ من الجدول +
لاحقةُ ضميرٍ متّصل (من `jidh.OBJECT_SUFFIXES`) أو لا لاحقة. تعديلٌ واحدٌ مسمًّى عند اللاحقة: الألفُ
المقصورة آخرَ المبنيّ تصير ياءً ساكنة (عَلَى + هِمْ ← عَلَيْهِمْ: `ALIF_TO_YA`). كلُّ قراءةٍ تُردّ إلى الكلمة
بعينها (`restore`)، والقراءاتُ لا تُحذف، والقسمةُ «مبنيّة» لا تُسوّى ولا تُقطع على قالب. ما ليس في
الجدول لا يُقرأ هنا، ويُترك لقارئ القوالب؛ وما لم يقرأه هذا ولا ذاك وهو حرفٌ عند المرجع يُسمّى
`PARTICLE_NOT_IN_TABLE`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from slge.categories import PRONOUNS
from slge.cells import SUKUN, Cell, licensed
from slge.damair import DETACHED_NASB
from slge.ishara import FORMS as ISHARA
from slge.istifham import FORMS as ISTIFHAM
from slge.jidh import OBJECT_SUFFIXES, PROCLITICS
from slge.marifa import MAWSUL
from slge.rawabit import PARTICLES, cells_of
from slge.zaman import CONSTANTS as ZAMAN_CONSTANTS
from slge.zaman import STEMS as ZAMAN
from slge.zaman import forms_of
from slge.zuruf import CONSTANTS, STEMS, jarr, mudaf, qat

__all__ = ["HOSTS", "KINDS", "TABLE", "VARIANTS", "Mabni", "alif_to_ya", "junction", "restore",
           "tawzi", "variants"]

Word = tuple[Cell, ...]
KINDS: Final[tuple[str, ...]] = ("حرف", "ضمير", "إشارة", "استفهام", "موصول", "ظرف")

_ALIF: Final[Cell] = ("ا", SUKUN)
_YA: Final[Cell] = ("ي", SUKUN)


def _table() -> tuple[tuple[str, str, Word], ...]:
    rows: list[tuple[str, str, Word]] = []
    rows += [("حرف", p.name, cells_of(p.name)) for p in PARTICLES if not p.proclitic]
    rows += [("ضمير", "", w) for w in PRONOUNS]
    rows += [("ضمير", p.name, p.cells) for p in DETACHED_NASB]
    rows += [("إشارة", f.name, f.cells) for f in ISHARA]
    rows += [("استفهام", f.name, f.cells) for f in ISTIFHAM]
    rows += [("موصول", n, w) for n, w in MAWSUL.items()]
    rows += [("ظرف", z.name, form(z.stem)) for z in STEMS for form in (mudaf, jarr, qat)]
    rows += [("ظرف", n, w) for n, w in CONSTANTS.items()]
    rows += [("ظرف", n, f) for n, st in ZAMAN.items() for f in forms_of(st)]
    rows += [("ظرف", n, w) for n, (w, _) in ZAMAN_CONSTANTS.items()]
    seen: set[Word] = set()
    out: list[tuple[str, str, Word]] = []
    for row in rows:
        if row[2] and row[2] not in seen:  # الصورةُ الواحدة مرّةً بأوّل بابٍ تظهر فيه
            seen.add(row[2])
            out.append(row)
    return tuple(out)


TABLE: Final[tuple[tuple[str, str, Word], ...]] = _table()
"""(البابُ، الاسمُ، الخانات) — المبنيّاتُ المودَعة بصورها، بلا تكرار صورة."""

HOSTS: Final[tuple[tuple[str, str, Word], ...]] = tuple(
    ("حرف", p.name, cells_of(p.name)) for p in PARTICLES if p.proclitic)
"""الحروفُ المتّصلة (بِ لِ كَ وَ…): مبنيٌّ حاملٌ لضميرٍ فقط (بِهِ، لَكُمْ) — لا تُقرأ وحدَها هنا."""

VARIANTS: Final[tuple[str, ...]] = ("", "ALIF_TO_YA", "LAM_FATHA", "JUNCTION_KASRA",
                                    "JUNCTION_FATHA")
"""صورُ المبنيّ في الكلمة: كما في الجدول؛ ألفُه ياءً قبل اللاحقة؛ لامُ الجرّ مفتوحةً قبل الضمير (لَهُ)؛
آخرُه الساكن مكسورًا أو مفتوحًا لالتقاء الساكنين (مِنَ، عَنِ) بلا لاحقة."""

_LI: Final[Word] = (("ل", "كسر"),)
_LA: Final[Word] = (("ل", "فتح"),)

_CORES: Final[dict[Word, tuple[str, str]]] = {w: (k, n) for k, n, w in TABLE}
_HOST_CORES: Final[dict[Word, tuple[str, str]]] = {w: (k, n) for k, n, w in HOSTS}


def alif_to_ya(core: Word) -> Word:
    """الألفُ المقصورة آخرَ المبنيّ ياءً ساكنة قبل اللاحقة (عَلَى ← عَلَيْ)؛ وإلّا كما هو."""

    if len(core) >= 2 and core[-1] == _ALIF and core[-2][1] == "فتح":
        return (*core[:-1], _YA)
    return core


def junction(core: Word) -> tuple[Word, Word]:
    """آخرُ المبنيّ الساكن مكسورًا (القاعدةُ) أو مفتوحًا (مِنَ) لالتقاء الساكنين؛ وإلّا الصورةُ نفسُها
    مرّتين."""

    if core and core[-1][1] == SUKUN and not _is_madd(core):
        return ((*core[:-1], (core[-1][0], "كسر")), (*core[:-1], (core[-1][0], "فتح")))
    return core, core


def _is_madd(core: Word) -> bool:
    """آخرُه حرفُ مدّ (ألفٌ، أو واوٌ بعد ضمّ، أو ياءٌ بعد كسر): خانةٌ ساكنة لا يلتقي بها ساكن."""

    k = core[-1][0]
    before = core[-2][1] if len(core) >= 2 else ""
    return k == "ا" or (k == "و" and before == "ضم") or (k == "ي" and before == "كسر")


def variants(core: Word, suf: Word) -> tuple[tuple[str, Word], ...]:
    """صورُ المبنيّ الجائزة في الكلمة بأسمائها (`variants`)."""

    if suf:
        lam = _LA if core == _LI else core
        return ("", core), ("ALIF_TO_YA", alif_to_ya(core)), ("LAM_FATHA", lam)
    k, f = junction(core)
    return ("", core), ("JUNCTION_KASRA", k), ("JUNCTION_FATHA", f)


@dataclass(frozen=True)
class Mabni:
    """قراءةُ مبنيّ: السوابقُ، البابُ والاسم، صورةُ المبنيّ في الجدول، صورتُه في الكلمة واسمُ تعديلها،
    اللاحقة."""

    pre: tuple[Word, ...]
    kind: str
    name: str
    core: Word
    surface: Word
    variant: str
    suf: Word


def restore(m: Mabni) -> Word:
    """الردُّ: السوابقُ ثمّ الصورةُ ثمّ اللاحقة — الكلمةُ بعينها."""

    return (*(c for p in m.pre for c in p), *m.surface, *m.suf)


def _pres() -> tuple[tuple[Word, ...], ...]:
    return ((), *((p,) for p in PROCLITICS), *((p, q) for p in PROCLITICS for q in PROCLITICS))


_PRES: Final[tuple[tuple[Word, ...], ...]] = _pres()


def tawzi(w: Word) -> tuple[Mabni, ...]:
    """قراءاتُ الكلمة مبنيًّا: كلُّ (سوابق، مبنيٌّ من الجدول بصورةٍ جائزة، لاحقة) يردّ الكلمةَ بعينها
    (`tawzi`)؛ الحرفُ المتّصل حاملًا لا يُقرأ إلّا بلاحقة."""

    out: list[Mabni] = []
    for pre in _PRES:
        flat = tuple(c for p in pre for c in p)
        if w[: len(flat)] != flat:
            continue
        rest = w[len(flat):]
        for suf in ((), *OBJECT_SUFFIXES):
            if suf and rest[len(rest) - len(suf):] != suf:
                continue
            surface = rest[: len(rest) - len(suf)] if suf else rest
            if not surface:
                continue
            cores = {**_CORES, **_HOST_CORES} if suf else _CORES
            for core, (kind, name) in cores.items():
                for variant, form in variants(core, suf):
                    if form == surface:
                        m = Mabni(pre, kind, name, core, surface, variant, suf)
                        assert restore(m) == w
                        out.append(m)
                        break
    return tuple(out)


def _check() -> None:
    assert len(TABLE) > 150 and all(licensed(w) for _, _, w in TABLE)
    assert {k for k, _, _ in TABLE} == set(KINDS)
    assert alif_to_ya(cells_of("عَلَى")) == cells_of("عَلَيْ")
    assert alif_to_ya(cells_of("مِنْ")) == cells_of("مِنْ")
    ms = tawzi(cells_of("عَلَيْهِمْ"))
    assert ms and all(restore(m) == cells_of("عَلَيْهِمْ") for m in ms)
    assert any(m.name == "عَلَى" and m.suf == cells_of("هِمْ") for m in ms)
    assert any(m.pre == (cells_of("لَ"),) and m.kind == "ضمير" for m in tawzi(cells_of("لَهُمْ")))
    assert any(m.name == "لِ" and m.variant == "LAM_FATHA" and m.suf == cells_of("هُمْ")
               for m in tawzi(cells_of("لَهُمْ")))
    assert any(m.variant == "JUNCTION_FATHA" for m in tawzi(cells_of("مِنَ")))
    assert not tawzi(cells_of("كَتَبَ")) and not tawzi(cells_of("بِ"))


_check()
