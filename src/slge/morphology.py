"""الصرف: شبكةُ الأوزان، والزوائدُ بوظائفها، والإعراب، والمقامات، والتصنيف.

جدولُ الزوائد واحد (`OPS`)، و`PREFIX` و`SUFFIX` مشتقّان منه. وفي الأصل كانت ثلاثةَ
جداولَ مكتوبةً باليد، فخالف `OPS` قاعدة ρ في أربعة صفوف (‎(أ، فتح)‎ والألفُ ليست
حاملًا؛ و‎(ا، فتح)‎ في استفعل وانفعل والتثنية)، وجدولا `PREFIX/SUFFIX` سليمان؛ فصُحّح
`OPS` إلى ما في أخويه بأعيانهما، لا من الذاكرة.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Final

from .cells import ALPHABET, SUKUN, Cell, Word, licensed
from .lexicon import CLOSED, skeleton_match

__all__ = [
    "GRID",
    "GRID_NOM",
    "IIRAB",
    "MADD",
    "MADI_SUFFIX",
    "MUZARA_PREFIX",
    "MUZARA_SUFFIX",
    "OPS",
    "PREFIX",
    "SUFFIX",
    "Slot",
    "classify",
    "conjugate",
    "generate",
    "iirab",
    "rho_role",
    "tanwin",
    "wasl_join",
]

Slot = tuple[str, str, str]
"""‎(النوع، المفتاح، الحالة)‎: «s» موضعٌ جذريّ مفتاحُه ف/ع/ل/م، و«f» ثابتٌ مفتاحُه حرفُه."""

_ROOT_KEYS: Final[str] = "فعلم"


def _g(spec: str) -> tuple[Slot, ...]:
    """قالبٌ مكتوبٌ مضغوطًا: ‎«s:ف:فتح f:ا:سكون …»‎."""

    out: list[Slot] = []
    for part in spec.split():
        kind, key, state = part.split(":")
        out.append((kind, key, state))
    return tuple(out)


GRID: Final[dict[str, tuple[Slot, ...]]] = {
    "I-fatha": _g("s:ف:فتح s:ع:فتح s:ل:فتح"),
    "I-kasra": _g("s:ف:فتح s:ع:كسر s:ل:فتح"),
    "I-damma": _g("s:ف:فتح s:ع:ضم s:ل:فتح"),
    "II": _g("s:ف:فتح s:ع:سكون s:ع:فتح s:ل:فتح"),
    "III": _g("s:ف:فتح f:ا:سكون s:ع:فتح s:ل:فتح"),
    "IV": _g("f:ء:فتح s:ف:سكون s:ع:فتح s:ل:فتح"),
    "V": _g("f:ت:فتح s:ف:فتح s:ع:سكون s:ع:فتح s:ل:فتح"),
    "VI": _g("f:ت:فتح s:ف:فتح f:ا:سكون s:ع:فتح s:ل:فتح"),
    "VII": _g("f:ء:فتح f:ن:سكون s:ف:فتح s:ع:فتح s:ل:فتح"),
    "VIII": _g("f:ء:فتح s:ف:سكون f:ت:فتح s:ع:فتح s:ل:فتح"),
    "IX": _g("f:ء:فتح s:ف:سكون s:ع:فتح s:ل:سكون s:ل:فتح"),
    "X": _g("f:ء:فتح f:س:سكون f:ت:فتح s:ف:سكون s:ع:فتح s:ل:فتح"),
    "Q": _g("s:ف:فتح s:ع:سكون s:ل:فتح s:م:فتح"),
}
"""شبكةُ الأفعال I–X والرباعيّ، كما في `slge.GRID` حرفًا."""

GRID_NOM: Final[dict[str, tuple[Slot, ...]]] = {
    "MS-1 فَعْل": _g("s:ف:فتح s:ع:سكون s:ل:فتح"),
    "MS-2 فُعُول": _g("s:ف:ضم s:ع:ضم f:و:سكون s:ل:ضم"),
    "MS-3 فِعَال": _g("s:ف:كسر s:ع:فتح f:ا:سكون s:ل:فتح"),
    "MS-4 فَعَالَة": _g("s:ف:فتح s:ع:فتح f:ا:سكون s:ل:فتح f:ت:فتح"),
    "MS-5 تَفْعِيل": _g("f:ت:فتح s:ف:سكون s:ع:كسر f:ي:سكون s:ل:فتح"),
    "MS-6 فِعَالَة": _g("s:ف:كسر s:ع:فتح f:ا:سكون s:ل:فتح f:ت:فتح"),
    "MS-7 مُفَاعَلَة": _g("f:م:ضم s:ف:فتح f:ا:سكون s:ع:فتح f:ل:سكون f:ت:فتح"),
    "MS-8 مَفْعَل": _g("f:م:فتح s:ف:سكون s:ع:فتح s:ل:سكون"),
    "MS-9 مَفْعِل": _g("f:م:فتح s:ف:سكون s:ع:كسر s:ل:سكون"),
    "JN-1 فِعْلَة": _g("s:ف:كسر s:ع:سكون s:ل:فتح f:ت:فتح"),
    "JN-3 مَفَاعِل": _g("f:م:فتح s:ف:فتح f:ا:سكون s:ع:كسر s:ل:فتح"),
    "JN-5 أَفْعِلَة": _g("f:ء:فتح s:ف:سكون s:ع:كسر s:ل:فتح f:ت:فتح"),
    "NS-1 يَفْعُلِيّ": _g("f:ي:فتح s:ف:فتح s:ع:ضم s:ل:كسر f:ي:سكون f:ي:فتح"),
}
"""الشبكةُ الاسميّة كما في `slge.GRID_NOM` حرفًا (ومنها «MS-7» بثابتٍ ‎(ل، سكون)‎ كما كُتب)."""


def generate(grid_id: str, root: str) -> list[Cell]:
    """املأ قالبًا بجذر: الحرفُ الأوّل للفاء، والثاني للعين، والثالث للّام، والرابع للميم."""

    template = GRID.get(grid_id) or GRID_NOM.get(grid_id)
    if template is None:
        raise KeyError(grid_id)
    keys = {k for kind, k, _ in template if kind == "s"}
    need = _ROOT_KEYS[: max(_ROOT_KEYS.index(k) for k in keys) + 1]
    if len(root) != len(need) or any(c not in ALPHABET for c in root):
        raise ValueError(f"القالب {grid_id} يطلب جذرًا من {len(need)} أحرف من الـ29")
    slots: Mapping[str, str] = dict(zip(need, root, strict=True))
    return [(slots[key] if kind == "s" else key, state) for kind, key, state in template]


def _c(spec: str) -> tuple[Cell, ...]:
    parts = spec.split()
    return tuple((parts[i], parts[i + 1]) for i in range(0, len(parts), 2))


OPS: Final[tuple[tuple[tuple[Cell, ...], str, str], ...]] = (
    (_c("ا سكون ل سكون"), "مقدمة", "تعريفي (بالوصل)"),
    (_c("ء فتح"), "مقدمة", "ضميري-زمني (1)"),
    (_c("ن فتح"), "مقدمة", "ضميري-زمني (1ج)"),
    (_c("ي فتح"), "مقدمة", "ضميري-زمني (3)"),
    (_c("ت فتح"), "مقدمة", "ضميري-زمني/تأنيث"),
    (_c("ب كسر"), "مقدمة", "سابق جر"),
    (_c("ل كسر"), "مقدمة", "سابق جر/تعليق"),
    (_c("م فتح"), "مقدمة", "اشتقاقي (ميمية)"),
    (_c("ت فتح"), "مقدمة", "اشتقاقي (تفعيل)"),
    (_c("ء فتح"), "مقدمة", "اشتقاقي (إحداث)"),
    (_c("ء فتح س سكون ت فتح"), "مقدمة", "اشتقاقي (استفعل)"),
    (_c("ء فتح ن سكون"), "مقدمة", "اشتقاقي (انفعل)"),
    (_c("ت سكون"), "خاتمة", "تصريفي (تأنيث) + ضميري (2ف/ج)"),
    (_c("ت ضم"), "خاتمة", "ضميري (1)"),
    (_c("ت فتح"), "خاتمة", "ضميري (2م)"),
    (_c("ت كسر"), "خاتمة", "ضميري (2مؤ)"),
    (_c("ه ضم"), "خاتمة", "ضميري (غائب)"),
    (_c("ن فتح ا سكون"), "خاتمة", "ضميري (متكلم جمع)"),
    (_c("ا سكون"), "خاتمة", "عدّ (تثنية)"),
    (_c("و فتح"), "خاتمة", "عدّ (جمع م)"),
    (_c("ن فتح"), "خاتمة", "عدّ (نسوة) + وقاية"),
    (_c("ي سكون ي فتح"), "خاتمة", "اشتقاقي (نسبة)"),
)
"""الزوائدُ بوظائفها (جدول 1.7): ‎22‎ صفًّا."""


def _distinct(position: str) -> tuple[tuple[Cell, ...], ...]:
    seen: list[tuple[Cell, ...]] = []
    for cells, pos, _ in OPS:
        if pos == position and cells not in seen:
            seen.append(cells)
    return tuple(seen)


PREFIX: Final[tuple[tuple[Cell, ...], ...]] = _distinct("مقدمة")
SUFFIX: Final[tuple[tuple[Cell, ...], ...]] = _distinct("خاتمة")


def wasl_join(a: Word, b: Word) -> list[Cell]:
    """قانون الوصل في الصرف: همزةُ الوصل في صدر الثاني تسقط."""

    rest = list(b)
    if rest and rest[0] == ("ا", SUKUN):
        rest = rest[1:]
    return [*a, *rest]


def tanwin(word: Word) -> list[Cell]:
    """التنوين (قانون 1.8): ‎+ (ن، سكون)‎."""

    return [*word, ("ن", SUKUN)]


IIRAB: Final[dict[str, str]] = {"رفع": "ضم", "نصب": "فتح", "جر": "كسر", "جزم": SUKUN}


def iirab(word: Word, case: str) -> list[Cell]:
    """الإعرابُ مشغّلُ الخانة الأخيرة وحدها (ONTOLOGY-4)."""

    if not word:
        raise ValueError("لا إعرابَ لخالية")
    out = [*word[:-1], (word[-1][0], IIRAB[case])]
    if case != "جزم" and not licensed(out):
        raise ValueError(f"الإعرابُ {case} أخرج كلمةً غيرَ مرخَّصة")
    return out


MADD: Final[dict[str, str]] = {"ا": "فتح", "و": "ضم", "ي": "كسر"}


def rho_role(cell: Cell, prev_state: str) -> str:
    """دورُ الخانة الساكنة: «مد» إن جانسها ما قبلها، و«إغلاق» إن لم يجانسها."""

    c, s = cell
    if s == SUKUN and c in MADD:
        return "مد" if prev_state == MADD[c] else "إغلاق"
    return "سكون-صرفي"


MADI_SUFFIX: Final[dict[str, tuple[Cell, ...]]] = {
    "هو": (), "هي": _c("ت سكون"), "أنا": _c("ت ضم"), "أنتَ": _c("ت فتح"),
    "أنتِ": _c("ت كسر"), "نحن": _c("ن فتح ا سكون"), "أنتم": _c("ت ضم م سكون"),
    "هنّ": _c("ن فتح"), "هم": _c("و فتح"),
}
MUZARA_PREFIX: Final[dict[str, tuple[Cell, ...]]] = {
    "أنا": _c("ء فتح"), "أنتَ": _c("ت فتح"), "أنتِ": _c("ت فتح"), "هو": _c("ي فتح"),
    "هي": _c("ت فتح"), "نحن": _c("ن فتح"), "أنتم": _c("ت فتح"), "هنّ": _c("ي فتح"),
    "هم": _c("ي فتح"),
}
MUZARA_SUFFIX: Final[dict[str, tuple[Cell, ...]]] = {
    "أنا": (), "أنتَ": (), "أنتِ": _c("ي فتح ن فتح"), "هو": (), "هي": (), "نحن": (),
    "أنتم": _c("و فتح ن فتح"), "هنّ": _c("ن فتح"), "هم": _c("و فتح ن فتح"),
}


def conjugate(root: str, tense: str, person: str) -> list[Cell]:
    """تصريفُ الثلاثيّ بالأشخاص (ONTOLOGY-5): «ماضٍ» على فَعَلَ، و«مضارع» على يَفْعُلُ."""

    if len(root) != 3:
        raise ValueError("التصريفُ هنا للثلاثيّ")
    f, e, l_ = root[0], root[1], root[2]
    if tense == "ماضٍ":
        word: list[Cell] = [(f, "فتح"), (e, "فتح"), (l_, "فتح"), *MADI_SUFFIX[person]]
    elif tense == "مضارع":
        word = [*MUZARA_PREFIX[person], (f, SUKUN), (e, "ضم"), (l_, "ضم"),
                *MUZARA_SUFFIX[person]]
    else:
        raise ValueError(f"زمنٌ غيرُ معلن: {tense}")
    if not licensed(word):
        raise ValueError(f"تصريفٌ غيرُ مرخَّص: {root} {tense} {person}")
    return word


def classify(word: Word) -> tuple[str, list[Cell]]:
    """الخانتان: «bin1» مدخلٌ مغلق أو زائدٌ عليه أو هيكلٌ من الجرد، و«bin2» ما سواه."""

    w = list(word)
    if tuple(w) in CLOSED:
        return ("bin1", w)
    for aff in PREFIX:
        k = len(aff)
        if len(w) > k and tuple(w[:k]) == aff:
            rest = w[k:]
            if tuple(rest) in CLOSED or skeleton_match(rest):
                return ("bin1", rest)
    if skeleton_match(w):
        return ("bin1", w)
    return ("bin2", w)
