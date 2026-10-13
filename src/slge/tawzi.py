"""الموزِّع: قبل قارئ القوالب تُسأل الكلمةُ أهي من المبنيّات المودَعة — مرآةُ `Slge.Tawzi`.

الحروفُ والضمائرُ وأسماءُ الإشارة والاستفهام والموصولُ وظروفُ المكان والزمان المودَعة لا قالبَ لها؛
قراءتُها من جدولها بعينه: الكلمةُ = سوابقُ (من `jidh.PROCLITICS`، حتى اثنتين) + مبنيٌّ من الجدول +
لاحقةُ ضميرٍ متّصل (من `jidh.OBJECT_SUFFIXES`، وياءُ الإضافة ساكنة، وميمُ الجمع موصولة) أو لا لاحقة.

**الإغلاق** (ADR ٥٣، `Slge.Tawzi`): اللاحقةُ لا يحملها إلّا حاملُها — الجارُّ والناسخُ من الحروف والظروف،
ومن المتّصلة باءُ الجرّ ولامُه وحدَهما (`SUFFIX_HOSTS`، `HOST_BI_LI`؛ الكتاب س8128–8130، س14027) —
فوَهُمْ واوٌ وضميرٌ منفصل؛ والحرفُ موصولًا بمَا/مَنْ مركَّبٌ مغلق (فِيمَا، مِمَّا بإدغام النون في الميم:
`MA_COMPOUND`، `NUN_MIM_IDGHAM` س21468)؛ والتعديلاتُ المسمّاة: الألفُ المقصورة ياءً قبل اللاحقة
(`ALIF_TO_YA`)، ولامُ الجرّ مفتوحةً (`LAM_FATHA`)، والآخرُ المتحرّك مكسورًا قبل ياء الإضافة
(`KASR_BEFORE_YA` س8106: إِنِّي)، وبلا لاحقةٍ: الآخرُ الساكن لالتقاء الساكنين (`JUNCTION_*`، وميمُ الجمع
مضمومةً س18109)، وكافُ الخطاب بصورها (`KAF_KHITAB`: ذَلِكُمْ)، وهمزةُ الوصل ساقطةً بعد سابقة
(`WASL_DROP`: وَلِلَّذِينَ)؛ والفعلان ظَنَّ وحَسِبَ ليسا مبنيّين (`VERB_NOT_MABNI`). كلُّ قراءةٍ تُردّ إلى الكلمة
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

__all__ = ["COMPOUNDS", "HOSTS", "KINDS", "MIM_WASL", "SUFFIXES", "SUF_TABLE", "TABLE", "VARIANTS",
           "VERBS", "Mabni", "alif_to_ya", "junction", "restore", "tawzi", "variants"]

Word = tuple[Cell, ...]
KINDS: Final[tuple[str, ...]] = ("حرف", "ضمير", "إشارة", "استفهام", "موصول", "ظرف")

_ALIF: Final[Cell] = ("ا", SUKUN)
_YA: Final[Cell] = ("ي", SUKUN)


VERBS: Final[tuple[str, ...]] = ("ظَنَّ", "حَسِبَ")
"""فعلان في جدول أدوات الربط لهما قالبٌ يتصرّفان عليه — ليسا مبنيّين (`VERB_NOT_MABNI`،
`Tawzi.verbs`)."""


def _table() -> tuple[tuple[str, str, Word], ...]:
    rows: list[tuple[str, str, Word]] = []
    rows += [("حرف", p.name, cells_of(p.name)) for p in PARTICLES
             if not p.proclitic and p.name not in VERBS]
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
    ("حرف", p.name, cells_of(p.name)) for p in PARTICLES if p.proclitic and p.name in ("بِ", "لِ"))
"""حاملا الضمير من الحروف المتّصلة: بِ ولِ وحدَهما (`HOST_BI_LI`، `Tawzi.hosts`) — لا يُقرآن وحدَهما."""

_AMIL: Final[tuple[str, ...]] = ("جرّ", "نصب الاسم ورفع الخبر")
SUF_TABLE: Final[tuple[Word, ...]] = (
    *(cells_of(p.name) for p in PARTICLES if not p.proclitic and p.amal in _AMIL),
    *(form(z.stem) for z in STEMS for form in (mudaf, jarr, qat)), *CONSTANTS.values(),
    *(f for st in ZAMAN.values() for f in forms_of(st)))
"""ما يحمل لاحقةَ الضمير من المبنيّات القائمة بنفسها: الجارُّ والناسخُ والظروف (`SUFFIX_HOSTS`،
`Tawzi.sufTable`)."""

_MA_MAN: Final[tuple[Word, ...]] = ((("م", "فتح"), _ALIF), (("م", "فتح"), ("ن", SUKUN)))


def _join_ma(a: Word, b: Word) -> Word:
    """النونُ الساكنة آخرَ الحرف ميمٌ مدغمةٌ في ميم مَا/مَنْ (`NUN_MIM_IDGHAM`، `Tawzi.joinMa`)."""

    if a and a[-1] == ("ن", SUKUN):
        return (*a[:-1], ("م", SUKUN), *b)
    return (*a, *b)


COMPOUNDS: Final[tuple[tuple[str, str, Word], ...]] = tuple(
    ("حرف", f"{p.name}+{'مَا' if b == _MA_MAN[0] else 'مَنْ'}", _join_ma(cells_of(p.name), b))
    for p in PARTICLES if not p.proclitic and p.amal in _AMIL for b in _MA_MAN)
"""الحرفُ الجارُّ أو الناسخ موصولًا بمَا أو مَنْ (`MA_COMPOUND`، `Tawzi.compounds`): فِيمَا، مِمَّا، عَمَّنْ."""

VARIANTS: Final[tuple[str, ...]] = ("", "ALIF_TO_YA", "LAM_FATHA", "KASR_BEFORE_YA",
                                    "JUNCTION_KASRA", "JUNCTION_FATHA", "JUNCTION_DAMMA",
                                    "KAF_KHITAB", "WASL_DROP")
"""صورُ المبنيّ في الكلمة: كما في الجدول؛ وباللاحقة ألفُه ياءً، ولامُ الجرّ مفتوحةً (لَهُ)، وآخرُه المتحرّك
مكسورًا قبل ياء الإضافة (إِنِّي)؛ وبلا لاحقةٍ آخرُه الساكن مكسورًا أو مفتوحًا لالتقاء الساكنين (مِنَ، عَنِ)
وميمُ الجمع مضمومةً (هُمُ)، وكافُ الخطاب بصورها (ذَلِكُمْ)، وهمزةُ الوصل ساقطةً بعد سابقة (وَلِلَّذِينَ)."""

_LI: Final[Word] = (("ل", "كسر"),)
_LA: Final[Word] = (("ل", "فتح"),)
_MIM: Final[Cell] = ("م", SUKUN)
_YA_SUFS: Final[tuple[Word, ...]] = ((("ي", "فتح"),), (_YA,))


def _mim_wasl() -> tuple[Word, ...]:
    out: list[Word] = []
    for s in OBJECT_SUFFIXES:
        if s and s[-1] == _MIM:
            out += [(*s[:-1], ("م", "ضم")), (*s[:-1], ("م", "كسر"))]
    return tuple(out)


MIM_WASL: Final[tuple[Word, ...]] = _mim_wasl()
SUFFIXES: Final[tuple[Word, ...]] = (*OBJECT_SUFFIXES, (_YA,), *MIM_WASL)
"""اللواحق: ضمائرُ النصب والجرّ المتّصلة، وياءُ الإضافة ساكنة، وميمُ الجمع موصولةً مضمومةً أو مكسورة
(`SUF_MIM_WASL`، `Tawzi.sufs`)."""

_KAFS: Final[tuple[Word, ...]] = tuple(s for s in (*OBJECT_SUFFIXES, *MIM_WASL) if s[0][0] == "ك")

_CORES: Final[dict[Word, tuple[str, str]]] = {w: (k, n) for k, n, w in TABLE}
_PLAIN: Final[dict[Word, tuple[str, str]]] = {
    **{w: (k, n) for k, n, w in reversed(COMPOUNDS)}, **_CORES}
_PLAIN_ORDER: Final[tuple[Word, ...]] = tuple(dict.fromkeys(
    (*(w for _, _, w in TABLE), *(w for _, _, w in COMPOUNDS))))
_SUF_CORES: Final[dict[Word, tuple[str, str]]] = {
    **{w: _CORES[w] for w in SUF_TABLE}, **{w: (k, n) for k, n, w in HOSTS}}


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


def _kasr_last(core: Word) -> Word:
    """الآخرُ المتحرّك مكسورًا قبل ياء الإضافة (`KASR_BEFORE_YA`، `Tawzi.kasrLast`)؛ والساكنُ كما هو."""

    if core and core[-1][1] in ("فتح", "ضم"):
        return (*core[:-1], (core[-1][0], "كسر"))
    return core


def variants(core: Word, suf: Word, has_pre: bool = False) -> tuple[tuple[str, Word], ...]:
    """صورُ المبنيّ الجائزة في الكلمة بأسمائها (`Tawzi.variants`)."""

    if suf:
        lam = _LA if core == _LI else core
        out: list[tuple[str, Word]] = [("", core), ("ALIF_TO_YA", alif_to_ya(core)),
                                       ("LAM_FATHA", lam)]
        if suf in _YA_SUFS:
            out.append(("KASR_BEFORE_YA", _kasr_last(core)))
        return tuple(out)
    k, f = junction(core)
    out = [("", core), ("JUNCTION_KASRA", k), ("JUNCTION_FATHA", f)]
    if core and core[-1] == _MIM:
        out.append(("JUNCTION_DAMMA", (*core[:-1], ("م", "ضم"))))
    if core and core[-1] == ("ك", "فتح"):
        out += [("KAF_KHITAB", (*core[:-1], *kaf)) for kaf in _KAFS]
    if has_pre and core[:2] == (("ء", "فتح"), ("ل", SUKUN)):
        out.append(("WASL_DROP", core[1:]))
    return tuple(out)


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
        for suf in ((), *SUFFIXES):
            if suf and rest[len(rest) - len(suf):] != suf:
                continue
            surface = rest[: len(rest) - len(suf)] if suf else rest
            if not surface:
                continue
            cores = _SUF_CORES if suf else _PLAIN
            for core in (cores if suf else _PLAIN_ORDER):
                kind, name = cores[core]
                for variant, form in variants(core, suf, bool(pre)):
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
    assert all(not m.suf for m in tawzi(cells_of("وَهُمْ"))) and tawzi(cells_of("وَهُمْ"))
    assert [m.variant for m in tawzi(cells_of("إِنِّي"))] == ["KASR_BEFORE_YA"]
    assert any(m.name == "لِ" and m.variant == "LAM_FATHA" and m.suf == cells_of("هُمْ")
               for m in tawzi(cells_of("لَهُمْ")))
    assert any(m.variant == "JUNCTION_FATHA" for m in tawzi(cells_of("مِنَ")))
    assert not tawzi(cells_of("كَتَبَ")) and not tawzi(cells_of("بِ"))


_check()
