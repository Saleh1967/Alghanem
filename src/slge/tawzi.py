"""الموزِّع: قبل قارئ القوالب تُسأل الكلمةُ أهي من المبنيّات المودَعة — مرآةُ `Slge.Tawzi`.

الحروفُ والضمائرُ وأسماءُ الإشارة والاستفهام والموصولُ وظروفُ المكان والزمان المودَعة لا قالبَ لها؛
قراءتُها من جدولها بعينه: الكلمةُ = سوابقُ (من `jidh.PROCLITICS`، حتى اثنتين) + مبنيٌّ من الجدول +
لاحقةُ ضميرٍ متّصل (من `jidh.OBJECT_SUFFIXES` ولواحقِ القواعد `SUF_EXTRA`) أو لا لاحقة. والتعديلاتُ
مسمّاةٌ كلُّها (`VARIANTS`، `SUF_RULES`): الألفُ المقصورة ياءً (عَلَيْهِمْ)، لامُ الجرّ مفتوحة (لَهُ)،
التقاءُ الساكنين (مِنَ)، وبالقواعد الخمس المرساة في الكتاب (ADR ٥٢): ميمُ الجمع مضمومةً أو مكسورةً في
الوصل (لَهُمُ، عَلَيْهِمِ)، وياءُ المتكلّم ساكنةً (لِي)، وهمزةُ وصل «الـ» ساقطةً بعد سابقة (وَلِلَّذِينَ)، و«مَا» مع
الحرف قبلها كلمةً (فِيمَا). كلُّ قراءةٍ تُردّ إلى الكلمة
بعينها (`restore`)، والقراءاتُ لا تُحذف، والقسمةُ «مبنيّة» لا تُسوّى ولا تُقطع على قالب. ما ليس في
الجدول لا يُقرأ هنا، ويُترك لقارئ القوالب؛ وما لم يقرأه هذا ولا ذاك وهو حرفٌ عند المرجع يُسمّى
`PARTICLE_NOT_IN_TABLE`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from slge.categories import PRONOUNS
from slge.cells import SUKUN, Cell, licensed
from slge.damair import ATTACHED_NASB, ATTACHED_RAF, DETACHED_NASB, DETACHED_RAF
from slge.huruf import TABLE as HURUF
from slge.ishara import FORMS as ISHARA
from slge.istifham import FORMS as ISTIFHAM
from slge.jidh import OBJECT_SUFFIXES, PROCLITICS
from slge.maani_table import SENSES
from slge.maani_table import TABLE as MAANI
from slge.marifa import MAWSUL
from slge.rawabit import BABS, PARTICLES, cells_of
from slge.zaman import CONSTANTS as ZAMAN_CONSTANTS
from slge.zaman import STEMS as ZAMAN
from slge.zaman import forms_of
from slge.zuruf import CONSTANTS, STEMS, jarr, mudaf, qat

__all__ = ["ANCHORS", "BASE_VARIANTS", "GAP", "HOSTS", "KINDS", "MA_HOSTS", "QISM", "RULES",
           "SOURCES", "SUF_EXTRA", "SUF_KASRA", "SUF_RULES", "TABLE", "VARIANTS", "Anchor",
           "Juz", "Mabni", "Wasm", "alif_to_ya", "is_base", "junction", "maana", "maana_suffix",
           "mim_damma", "mim_kasra", "restore", "tawzi", "variants", "wasl_drop", "wasm",
           "ya_sakina"]

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
                                    "JUNCTION_FATHA", "MIM_DAMMA", "MA_COMPOUND", "WASL_DROP")
"""صورُ المبنيّ في الكلمة: كما في الجدول؛ ألفُه ياءً قبل اللاحقة؛ لامُ الجرّ مفتوحةً قبل الضمير (لَهُ)؛
آخرُه الساكن مكسورًا أو مفتوحًا لالتقاء الساكنين (مِنَ، عَنِ) بلا لاحقة؛ ميمُ جمعه مضمومة (هُمُ)؛ الحرفُ
مع «مَا» (فِيمَا)؛ وبعد سابقةٍ همزةُ وصله ساقطة (لِلَّذِينَ)."""

BASE_VARIANTS: Final[tuple[str, ...]] = VARIANTS[:5]
"""الصورُ قبل قواعد ADR ٥٢."""
RULES: Final[frozenset[str]] = frozenset(
    {"MIM_DAMMA", "MIM_KASRA", "YA_SAKINA", "WASL_DROP", "MA_COMPOUND"})
"""القواعدُ الخمس المسجَّلة قبل الشيفرة (ADR ٥٢)، كلٌّ باسمه ومرساته في الكتاب المختوم."""

_MIM: Final[Cell] = ("م", SUKUN)
MA: Final[Word] = (("م", "فتح"), ("ا", SUKUN))


def mim_damma(w: Word) -> Word:
    """`MIM_DAMMA` (س18109–18110): ميمُ الجمع الساكنة بعد ضمٍّ أو كسرٍ مضمومة؛ وإلّا كما هو."""

    if len(w) >= 2 and w[-1] == _MIM and w[-2][1] in ("ضم", "كسر"):
        return (*w[:-1], ("م", "ضم"))
    return w


def mim_kasra(w: Word) -> Word:
    """`MIM_KASRA` (س18118): ميمُ هِمْ مكسورة؛ وإلّا كما هو."""

    if len(w) >= 2 and w[-1] == _MIM and w[-2][1] == "كسر":
        return (*w[:-1], ("م", "كسر"))
    return w


def ya_sakina(w: Word) -> Word:
    """`YA_SAKINA` (س4456): ياءُ المتكلّم المفتوحة ساكنة؛ وإلّا كما هو."""

    return (("ي", SUKUN),) if w == (("ي", "فتح"),) else w


def wasl_drop(w: Word) -> Word:
    """`WASL_DROP` (س17527): همزةُ وصل «الـ» أوّلَ المبنيّ تسقط بعد سابقة؛ وإلّا كما هو."""

    if len(w) >= 2 and w[0] == ("ء", "فتح") and w[1] == ("ل", SUKUN):
        return w[1:]
    return w


_HUM: Final[Word] = (("ه", "ضم"), _MIM)
_KUM: Final[Word] = (("ك", "ضم"), _MIM)
_HIM: Final[Word] = (("ه", "كسر"), _MIM)
SUF_RULES: Final[dict[Word, tuple[str, Word]]] = {
    mim_damma(_HUM): ("MIM_DAMMA", _HUM), mim_damma(_KUM): ("MIM_DAMMA", _KUM),
    mim_damma(_HIM): ("MIM_DAMMA", _HIM), mim_kasra(_HIM): ("MIM_KASRA", _HIM),
    ya_sakina((("ي", "فتح"),)): ("YA_SAKINA", (("ي", "فتح"),)),
}
"""لاحقةُ القاعدة ← (اسمُ القاعدة، لاحقةُ الجدول التي تُصيِّرها) — `Tawzi.sufExtra_named`."""
SUF_EXTRA: Final[tuple[Word, ...]] = tuple(SUF_RULES)

_LI: Final[Word] = (("ل", "كسر"),)
_LA: Final[Word] = (("ل", "فتح"),)

_CORES: Final[dict[Word, tuple[str, str]]] = {w: (k, n) for k, n, w in TABLE}
MA_HOSTS: Final[frozenset[Word]] = frozenset(cells_of(p.name) for p in PARTICLES if not p.proclitic)
"""الحروفُ المنفصلة التي تُجعل «مَا» معها كلمةً (`MA_COMPOUND`، س5825–5826؛ `Tawzi.maHosts`)."""
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


def variants(core: Word, suf: Word, wasl: bool = False) -> tuple[tuple[str, Word], ...]:
    """صورُ المبنيّ الجائزة في الكلمة بأسمائها (`variants`)؛ `wasl`: بعد سابقة."""

    out: tuple[tuple[str, Word], ...]
    if suf:
        lam = _LA if core == _LI else core
        out = ("", core), ("ALIF_TO_YA", alif_to_ya(core)), ("LAM_FATHA", lam)
    else:
        k, f = junction(core)
        out = (("", core), ("JUNCTION_KASRA", k), ("JUNCTION_FATHA", f),
               ("MIM_DAMMA", mim_damma(core)),
               *((("MA_COMPOUND", (*core, *MA)),) if core in MA_HOSTS else ()))
    return (*out, ("WASL_DROP", wasl_drop(core))) if wasl else out


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
    suf_rule: str = ""
    """اسمُ قاعدة اللاحقة (`SUF_RULES`) إن كانت من لواحق القواعد."""


def restore(m: Mabni) -> Word:
    """الردُّ: السوابقُ ثمّ الصورةُ ثمّ اللاحقة — الكلمةُ بعينها."""

    return (*(c for p in m.pre for c in p), *m.surface, *m.suf)


def _pres() -> tuple[tuple[Word, ...], ...]:
    return ((), *((p,) for p in PROCLITICS), *((p, q) for p in PROCLITICS for q in PROCLITICS))


_PRES: Final[tuple[tuple[Word, ...], ...]] = _pres()


def tawzi(w: Word, rules: frozenset[str] = RULES) -> tuple[Mabni, ...]:
    """قراءاتُ الكلمة مبنيًّا: كلُّ (سوابق، مبنيٌّ من الجدول بصورةٍ جائزة، لاحقة) يردّ الكلمةَ بعينها
    (`tawzi`)؛ الحرفُ المتّصل حاملًا لا يُقرأ إلّا بلاحقة. `rules`: القواعدُ المسمّاة العاملة (كلُّها
    افتراضًا؛ والحذفُ للقياس بالحذف، ADR ٥٢)."""

    out: list[Mabni] = []
    for pre in _PRES:
        flat = tuple(c for p in pre for c in p)
        if w[: len(flat)] != flat:
            continue
        rest = w[len(flat):]
        extra = tuple(x for x in SUF_EXTRA if SUF_RULES[x][0] in rules)
        for suf in ((), *OBJECT_SUFFIXES, *extra):
            if suf and rest[len(rest) - len(suf):] != suf:
                continue
            surface = rest[: len(rest) - len(suf)] if suf else rest
            if not surface:
                continue
            cores = {**_CORES, **_HOST_CORES} if suf else _CORES
            for core, (kind, name) in cores.items():
                for variant, form in variants(core, suf, bool(pre)):
                    if variant in RULES and variant not in rules:
                        continue
                    if form == surface:
                        rule = SUF_RULES[suf][0] if suf in SUF_RULES else ""
                        m = Mabni(pre, kind, name, core, surface, variant, suf, rule)
                        assert restore(m) == w
                        out.append(m)
                        break
    return tuple(out)


def is_base(m: Mabni) -> bool:
    """قراءةٌ بلا قاعدةٍ من قواعد ADR ٥٢ (`Tawzi.base`): ما كان الموزِّعُ يقرؤه قبلها بعينه."""

    return m.variant in BASE_VARIANTS and not m.suf_rule


# — الوسمُ المغلق (ADR ٥٢): التعريفُ والمعنى من المودَع، أو فجوةٌ باسمها —

QISM: Final[dict[str, str]] = {"حرف": "حرف", "ضمير": "اسم مبنيّ", "إشارة": "اسم مبنيّ",
                               "استفهام": "اسم مبنيّ", "موصول": "اسم مبنيّ", "ظرف": "اسم مبنيّ",
                               "أداة": "أداة"}
"""القسمُ بتقسيم ج3 «المفرد: اسم، وفعل، وحرف» (`NabhaniTable`): الوسمُ المغلق لا يُخرج المبنيَّ من الاسم،
بل يفصله عن الاسم والفعل المفتوحين (ما يُقرأ بقالبٍ وجذر). و«أداة»: أداةُ ربطٍ من `rawabit` ليست في جدول
حروف المعاني (`huruf`) — لَيْسَ، ظَنَّ، غَيْرُ، حِينَ… — فقسمُها (اسمٌ أو فعلٌ أو حرف) غيرُ مودَعٍ هنا
(`QISM_NOT_DEPOSITED`)، ووظيفتُها مودَعة (`rawabit.BABS`)."""

GAP: Final[str] = "MEANING_NOT_DEPOSITED"
"""ما لا معنى له في مودَعٍ مسمًّى: يُسمّى ولا يُكتب له معنًى من الذاكرة."""


_HURUF: Final[dict[Word, tuple[int, ...]]] = {}
for _i, _h in enumerate(HURUF):
    _HURUF[_h.cells] = (*_HURUF.get(_h.cells, ()), _i)
_RAWABIT: Final[dict[Word, tuple[str, ...]]] = {}
for _r in PARTICLES:
    _RAWABIT[_r.cells] = (*_RAWABIT.get(_r.cells, ()),
                          f"{_r.name} — وظيفةُ الربط: {BABS[_r.bab]}"
                          + (f"؛ العمل: {_r.amal}" if _r.amal else ""))


def _rows_all() -> tuple[tuple[str, str, Word], ...]:
    """صفوفُ الجداول كلُّها قبل نزع التكرار: الصورةُ الواحدة قد تكون في بابين (مَنْ حرفًا واستفهامًا
    وموصولًا)، والوسمُ يحمل الأبوابَ كلَّها ولا يختار."""

    rows: list[tuple[str, str, Word]] = []
    rows += [("حرف" if p.cells in _HURUF else "أداة", p.name, p.cells) for p in PARTICLES]
    rows += [("حرف", h.name, h.cells) for h in HURUF]
    rows += [("ضمير", "", w) for w in PRONOUNS]
    rows += [("ضمير", p.name, p.cells) for p in DETACHED_NASB]
    rows += [("إشارة", f.name, f.cells) for f in ISHARA]
    rows += [("استفهام", f.name, f.cells) for f in ISTIFHAM]
    rows += [("موصول", n, w) for n, w in MAWSUL.items()]
    rows += [("ظرف", z.name, form(z.stem)) for z in STEMS for form in (mudaf, jarr, qat)]
    rows += [("ظرف", n, w) for n, w in CONSTANTS.items()]
    rows += [("ظرف", n, f) for n, st in ZAMAN.items() for f in forms_of(st)]
    rows += [("ظرف", n, w) for n, (w, _) in ZAMAN_CONSTANTS.items()]
    return tuple(r for r in rows if r[2])


def _babs() -> dict[Word, tuple[tuple[str, str], ...]]:
    names: dict[Word, dict[str, list[str]]] = {}
    for k, n, w in _rows_all():
        ns = names.setdefault(w, {}).setdefault(k, [])
        if n and n not in ns:
            ns.append(n)
    return {w: tuple((k, "/".join(ns)) for k, ns in d.items()) for w, d in names.items()}


_BABS: Final[dict[Word, tuple[tuple[str, str], ...]]] = _babs()
"""الصورةُ ← أبوابُها كلُّها (البابُ مرّةً بأسمائه)."""
_ATT: Final[dict[Word, tuple[str, str]]] = {}
for _p in (*ATTACHED_NASB, *ATTACHED_RAF):
    _ATT.setdefault(_p.cells, (_p.group, _p.role))
_DET: Final[dict[Word, tuple[str, str]]] = {}
for _p in (*DETACHED_RAF, *DETACHED_NASB):
    _DET.setdefault(_p.cells, (_p.group, _p.role))
_ISHARA: Final[dict[Word, tuple[str, str]]] = {f.cells: (f.bab, f.dalala) for f in ISHARA}
_ISTIFHAM: Final[dict[Word, tuple[str, str]]] = {f.cells: (f.kind, f.dalala) for f in ISTIFHAM}
_ZAMAN: Final[frozenset[Word]] = frozenset(
    {*(f for st in ZAMAN.values() for f in forms_of(st)),
     *(w for w, _ in ZAMAN_CONSTANTS.values())})
_ZURUF: Final[dict[Word, str]] = {
    **{f: z.bab for z in STEMS for f in (mudaf(z.stem), jarr(z.stem), qat(z.stem))},
    **{w: "ظرف مكان" for w in CONSTANTS.values()}}


@dataclass(frozen=True)
class Anchor:
    """معنًى منقولٌ بنصّه من مختومٍ مسمًّى: المصدرُ (`SOURCES`)، والسطرُ (يبدأ من 1 بعد فكّ الضغط)، والعبارةُ
    بعينها كما في السطر — تُطابَق حرفًا حرفًا (`tests/test_tawzi.py`) ولا يُكتب معنًى من الذاكرة."""

    bab: str
    cells: Word
    source: str
    line: int
    quote: str

    def text(self) -> str:
        return f"«{self.quote}» ({SOURCES[self.source][1]} س{self.line})"


SOURCES: Final[dict[str, tuple[str, str]]] = {
    "kitab": ("openiti-sibawayh-kitab.txt.gz", "الكتاب"),
    "ibn-aqil": ("openiti-ibn-aqil-alfiyya.txt.gz", "ابن عقيل"),
}
_IA = "ibn-aqil"
_M = MAWSUL
_MAWSUL_QUOTES: Final[tuple[tuple[tuple[str, ...], int, str], ...]] = (
    (("الَّذِي",), 1051, "الذي للمفرد المذكر"),
    (("الَّتِي",), 1051, "والتي للمفرد المؤنثة"),
    (("اللَّذَانِ", "اللَّتَانِ"), 1052,
     "ثنيت أسقطت الياء وأتيت مكانها بالألف في حالة الرفع نحو اللذان واللتان"),
    (("اللَّذَيْنِ", "اللَّتَيْنِ"), 1053, "والياء في حالتي الجر والنصب فتقول اللذين واللتين"),
    (("الَّذِينَ",), 1069, "ويقال للمذكر العاقل في الجمع الذين مطلقا"),
    (("اللَّاتِي", "اللَّائِي"), 1075, "ويقال في جمع المؤنث اللات واللاء"),
    (("اللَّاتِي", "اللَّائِي"), 1076, "ويجوز إثبات الياء فتقول اللاتي واللائي"),
    (("مَنْ", "مَا"), 1084, "أن من وما والألف واللام تكون بلفظ واحد"),
    (("مَنْ", "مَا"), 1085, "للمذكر والمؤنث المفرد والمثنى والمجموع"),
    (("مَا",), 1089, "وأكثر ما تستعمل ما في غير العاقل"),
    (("مَنْ",), 1092, "بالعكس فأكثر ما تستعمل في العاقل"),
    (("ذُو",), 1103, "طييء استعمال ذو موصولة وتكون للعاقل ولغيره"),
    (("أَيُّ",), 1181, "يعني أن أيا مثل ما في أنها تكون بلفظ واحد للمذكر والمؤنث"),
)
_HA_KASRA: Final = (18128, "فالهاء تكسر إذا كان قبلها ياء أو كسرة")
_NI: Final = (8088, "علامة إضمار المنصوب المتكلم نى")
ANCHORS: Final[tuple[Anchor, ...]] = (
    *(Anchor("موصول", _M[n], _IA, line, q) for ns, line, q in _MAWSUL_QUOTES for n in ns),
    Anchor("حرف", (("ل", "فتح"),), "kitab", 2391, "لام الابتداء"),
    Anchor("حرف", (("ل", "فتح"),), "kitab", 18346, "ولام اليمين التي في لأفعلن"),
)
"""المعاني المرساة: الموصولاتُ من شرح ابن عقيل (باب الموصول، س1026–1181) إلّا اللَّوَاتِي فلا ذكرَ لها فيه
فتبقى `GAP`؛ ولامُ التوكيد السابقةُ (لَ) من الكتاب: لامُ الابتداء ولامُ اليمين معًا بلا اختيار."""

SUF_KASRA: Final[dict[Word, tuple[Word, int, str]]] = {
    **{(("ه", "كسر"), *p.cells[1:]): (p.cells, *_HA_KASRA)
       for p in ATTACHED_NASB if p.cells[0] == ("ه", "ضم")},
    (("ن", "كسر"), ("ي", SUKUN)): (ATTACHED_NASB[0].cells, *_NI),
}
"""لاحقةٌ ← أصلُها في `damair` وموضعُ تعليلها في الكتاب: هاءُ الضمير تُكسر بعد ياءٍ أو كسرة (س18128)، ونِي
علامةُ المنصوب المتكلّم (س8088). لا يغيّر قراءةً؛ يردّ المعنى وحدَه."""


def maana(bab: str, cells: Word, attached: bool = False) -> tuple[tuple[str, ...], str]:
    """(المعنى، مصدرُه) من الجدول المودَع للباب، بلا اختيارٍ بين ما تعدّد:

    * الحرف والأداة: لكلّ صفٍّ له في `huruf` عملُه ومدخولُه ومعانيه بترتيب ج3 (`maani_table`)، ووظيفتُه
      في الربط من `rawabit`؛
    * الضمير: زمرتُه ودورُه (`damair`)، المتّصلُ لاحقةً والمنفصلُ نواةً؛
    * الإشارة: بابُها ودلالتُها؛ الاستفهام: نوعُه ودلالتُه؛ الظرف: زمانٌ (`zaman`) أو بابُه في المكان
      (`zuruf`)؛
    * وما لا معنى له في مودَعٍ مسمًّى فـ`GAP` — لا يُكتب له معنًى من الذاكرة."""

    if bab in ("حرف", "أداة") and (cells in _HURUF or cells in _RAWABIT):
        alts = []
        for i in _HURUF.get(cells, ()):
            h = HURUF[i]
            senses = "، ".join(SENSES[k] for k in MAANI.get(i, ()))
            alts.append(f"{h.name} — العمل: {h.amal or 'لا'}؛ المدخول: {h.cls}"
                        + (f"؛ المعاني: {senses}" if senses else ""))
        alts += _RAWABIT.get(cells, ())
        return tuple(alts), "huruf+maani_table+rawabit"
    if bab == "ضمير":
        table = _ATT if attached else _DET
        if cells in table:
            return table[cells], "damair"
    if bab == "إشارة" and cells in _ISHARA:
        return _ISHARA[cells], "ishara"
    if bab == "استفهام" and cells in _ISTIFHAM:
        return _ISTIFHAM[cells], "istifham"
    if bab == "ظرف" and cells in _ZAMAN:
        return ("ظرف زمان",), "zaman"
    if bab == "ظرف" and cells in _ZURUF:
        return (_ZURUF[cells],), "zuruf"
    anchored = tuple(a.text() for a in ANCHORS if a.bab == bab and a.cells == cells)
    if anchored:
        return anchored, "+".join(dict.fromkeys(a.source for a in ANCHORS
                                                if a.bab == bab and a.cells == cells))
    return (), GAP


@dataclass(frozen=True)
class Juz:
    """جزءٌ من الكلمة المغلقة بدوره (سابقة، نواة، لاحقة): خاناتُه في الكلمة، وأبوابُه كلُّها بأسمائها
    ومعانيها من المودَع أو `GAP`."""

    dawr: str
    cells: Word
    babs: tuple[tuple[str, str, tuple[str, ...], str], ...]
    """(الباب، الاسم، المعنى، مصدرُه) لكلّ بابٍ يقع فيه الجزءُ في الجداول."""


@dataclass(frozen=True)
class Wasm:
    """الوسمُ المغلق: القسمُ (حرف/اسم مبنيّ، وقد يكونان معًا لصورةٍ في بابين)، والأجزاءُ بأدوارها، وأسماءُ
    القواعد التي قرأتها. موصولةً الأجزاءُ هي الكلمة بعينها."""

    qism: tuple[str, ...]
    parts: tuple[Juz, ...]
    rules: tuple[str, ...]


def _juz(dawr: str, cells: Word, key: Word, attached: bool) -> Juz:
    babs = _BABS.get(key) or (("حرف", ""),)
    return Juz(dawr, cells, tuple((b, n, *maana(b, key, attached)) for b, n in babs))


def maana_suffix(suf: Word) -> tuple[tuple[str, ...], str]:
    """معنى اللاحقة: تُردّ لاحقةُ القاعدة إلى أصلها في الجدول (`SUF_RULES`)، ثمّ هاءُ الضمير المكسورةُ ونِي
    إلى أصلهما في `damair` بموضع تعليلهما في الكتاب (`SUF_KASRA`)؛ وما سوى ذلك `GAP`."""

    orig = SUF_RULES[suf][1] if suf in SUF_RULES else suf
    sense, src = maana("ضمير", orig, True)
    if src == GAP and orig in SUF_KASRA:
        base, line, quote = SUF_KASRA[orig]
        sense, src = maana("ضمير", base, True)
        sense, src = (*sense, f"«{quote}» (الكتاب س{line})"), src + "+kitab"
    return sense, src


def wasm(m: Mabni) -> Wasm:
    """وسمُ قراءةٍ من قراءات الموزِّع: كلُّ جزءٍ ببابه ومعناه أو فجوته، ولا جزءَ يضيع."""

    parts = [_juz("سابقة", p, p, False) for p in m.pre]
    core = _juz("نواة", m.surface, m.core, False)
    parts.append(core)
    if m.suf:
        parts.append(Juz("لاحقة", m.suf, (("ضمير", "", *maana_suffix(m.suf)),)))
    qism = tuple(dict.fromkeys(QISM[b] for b, *_ in core.babs))
    rules = tuple(r for r in (m.variant, m.suf_rule) if r)
    return Wasm(qism, tuple(parts), rules)


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
    assert any(m.suf_rule == "MIM_DAMMA" for m in tawzi(cells_of("لَهُمُ")))
    assert any(m.variant == "MA_COMPOUND" for m in tawzi(cells_of("فِيمَا")))
    for m in tawzi(cells_of("وَمِنْكُمْ")):
        t = wasm(m)
        assert tuple(c for j in t.parts for c in j.cells) == cells_of("وَمِنْكُمْ")


_check()
