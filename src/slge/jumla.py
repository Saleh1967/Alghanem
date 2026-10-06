"""الجملةُ الاسميّة: طرفان مرفوعان، ورتبةٌ من الخانة، ومطابقةٌ عمليّات، ورابطٌ يُقرأ — مرآةُ `Jumla.lean`.

الرفعُ عمليّةٌ واحدةٌ على الطرفين (`nominal`؛ `nawasikh.raf`). صورُ المبتدأ يقرؤها `mubtada_kind` (ضميرٌ
منفصل من جدوله، مبنيٌّ من جداوله، اسمٌ ظاهرٌ من رفعه؛ والمصدرُ المؤوّل تيار)، وصورُ الخبر `khabar_kind`
(شبهُ جملةٍ من صدرها، جملةٌ فعليّةٌ من قالب الفعل، مفردٌ من رفعه). الرتبةُ دالّةٌ في الخانات لا في الموضع
(`order`): لامُ الابتداء، الصدارة، النكرةُ مع شبه الجملة، الضميرُ العائد، الخبرُ الفعليّ، تساوي الرتبة،
والجواز؛ والموضعُ المخالفُ يُرفض (`admissible`). المطابقةُ عمليّاتٌ على الخبر (`ta_nith`، `dual`، `jam_m`،
`jam_f`) وقراءةٌ من اللاحقة (`gender`، `number`، `agree`)؛ واستثناءُ جمع غير العاقل يقرؤه القالبُ
احتمالًا (`broken_plural`، `agree_loose`). الرابطُ في الخبر الجملة: ضميرٌ أو إشارةٌ أو إعادةُ اللفظ
(`rabit`)؛ والعمومُ والتلاؤمُ الأنطولوجيُّ معنًى ومعجم. القياسُ على MASAQ في `tools/gen_jumla_index.py`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from slge.categories import PRONOUNS
from slge.cells import STATES, Cell, licensed
from slge.damair import ATTACHED_NASB, ATTACHED_RAF
from slge.ishara import FORMS as ISHARA
from slge.istifham import FORMS as ISTIFHAM
from slge.majrurat import HARFS
from slge.marifa import MAWSUL, has_al
from slge.nawasikh import raf
from slge.nida import has_tanwin
from slge.rawabit import cells_of
from slge.sarf import MUNTAHA, on_template
from slge.tawabi import case_class
from slge.zaman import CONSTANTS as ZAMAN_CONSTANTS
from slge.zaman import STEMS as ZAMAN_STEMS
from slge.zaman import nasb_tanwin, raf_tanwin
from slge.zuruf import CONSTANTS as ZURUF_CONSTANTS
from slge.zuruf import STEMS as ZURUF_STEMS
from slge.zuruf import jarr, mudaf, qat, set_last

__all__ = ["VERB_TEMPLATES", "WITNESSES", "Jumla", "admissible", "agree", "agree_loose",
           "broken_plural", "dual", "gender", "jam_f", "jam_m", "khabar_kind", "lam",
           "mubtada_kind", "nakira", "nominal", "number", "order", "rabit", "shibh_jumla", "swap",
           "ta_nith"]

_A, _I, _U, SUKUN = STATES
Word = tuple[Cell, ...]


@dataclass(frozen=True, slots=True)
class Jumla:
    mubtada: Word
    khabar: Word
    khabar_first: bool = False


def nominal(m: Word, k: Word) -> Jumla:
    """الرفعُ عمليّةٌ واحدةٌ على الطرفين."""

    return Jumla(raf(m), raf(k), False)


# — صورُ المبتدأ والخبر —

_HARF_CELLS: Final[tuple[Word, ...]] = tuple(cells_of(h) for h in HARFS)
_ZURUF: Final[frozenset[Word]] = frozenset(
    op(z.stem) for z in ZURUF_STEMS for op in (mudaf, jarr, qat)
) | frozenset(ZURUF_CONSTANTS.values())
_ZAMAN: Final[frozenset[Word]] = frozenset(
    op(s) for s in ZAMAN_STEMS.values() for op in (mudaf, jarr, qat, raf_tanwin, nasb_tanwin)
) | frozenset(v[0] for v in ZAMAN_CONSTANTS.values())
VERB_TEMPLATES: Final[tuple[int, ...]] = tuple(range(29))
_ISTIFHAM: Final[frozenset[Word]] = frozenset(f.cells for f in ISTIFHAM)
_ISHARA: Final[frozenset[Word]] = frozenset(f.cells for f in ISHARA)
_AID: Final[tuple[Word, ...]] = (*(p.cells for p in ATTACHED_NASB), cells_of("هِ"), cells_of("هِمْ"),
                                  cells_of("هِمَا"), cells_of("هِنَّ"))


_MABNI: Final[frozenset[Word]] = _ISHARA | frozenset(MAWSUL.values()) | _ISTIFHAM


def mubtada_kind(w: Word) -> str:
    """ضميرٌ منفصل، أو اسمٌ مبنيٌّ من جداوله، أو اسمٌ ظاهرٌ مرفوع، أو لا يُقرأ (المصدرُ المؤوّل تيار)."""

    if w in PRONOUNS:
        return "ضمير"
    if w in _MABNI:
        return "مبني"
    return "اسم" if case_class(w) == "رفع" else "—"


_JARR_BEFORE_PRONOUN: Final[tuple[Word, ...]] = (
    (("ل", _A),), cells_of("إِلَيْ"), cells_of("عَلَيْ"), cells_of("لَدَيْ"), *_HARF_CELLS)


def jarr_pronoun(w: Word) -> bool:
    """جارٌّ (بصورته قبل الضمير) وضميرٌ متّصل: لَهُمْ، إِلَيْهِ، مِنْهُ، فِيهَا."""

    return any(w == (*h, *p) for p in _AID for h in _JARR_BEFORE_PRONOUN)


def shibh_jumla(w: Word) -> bool:
    """صدرُها حرفُ جرٍّ من خانتين فأكثر، أو متّصلٌ تليه أل، أو جارٌّ وضمير، أو ظرفٌ من `zuruf`/`zaman`."""

    if any(len(h) >= 2 and w[: len(h)] == h for h in _HARF_CELLS):
        return True
    if any(len(h) == 1 and w[:1] == h and has_al(w[1:]) for h in _HARF_CELLS[:5]):
        return True
    return jarr_pronoun(w) or w in _ZURUF or w in _ZAMAN


def is_verb(w: Word) -> bool:
    return any(on_template(k, w) for k in VERB_TEMPLATES)


def khabar_kind(w: Word) -> str:
    if shibh_jumla(w):
        return "شبه جملة"
    if is_verb(w):
        return "جملة فعلية"
    return "مفرد" if case_class(w) == "رفع" else "—"


# — الرتبة —


def swap(j: Jumla) -> Jumla:
    return Jumla(j.mubtada, j.khabar, not j.khabar_first)


def lam(w: Word) -> Word:
    """لامُ الابتداء: حرفٌ متّصل."""

    return (("ل", _A), *w)


def starts_lam(w: Word) -> bool:
    return bool(w) and w[0] == ("ل", _A)


def nakira(w: Word) -> bool:
    """النكرةُ من الخانة: تنوينٌ بلا أل."""

    return has_tanwin(w) and not has_al(w)


def has_aid_pronoun(w: Word) -> bool:
    """ضميرٌ متّصلٌ في الآخر من جدول `damair`."""

    return any(len(p) < len(w) and w[-len(p):] == p for p in _AID)


def order(j: Jumla) -> str:
    """الرتبةُ من الخانات لا من الموضع: كما في الحصر، 4 + 4 + الجواز."""

    m, k = j.mubtada, j.khabar
    if starts_lam(m):
        return "تقديم المبتدأ"
    if k in _ISTIFHAM:
        return "تقديم الخبر"
    if nakira(m) and shibh_jumla(k):
        return "تقديم الخبر"
    if has_aid_pronoun(m) and shibh_jumla(k):
        return "تقديم الخبر"
    kk = khabar_kind(k)
    if kk == "جملة فعلية":
        return "تقديم المبتدأ"
    if kk != "شبه جملة" and nakira(m) == nakira(k):
        return "تقديم المبتدأ"
    return "جواز"


def admissible(j: Jumla) -> bool:
    r = order(j)
    if r == "تقديم الخبر":
        return j.khabar_first
    if r == "تقديم المبتدأ":
        return not j.khabar_first
    return True


# — المطابقة —


def ta_nith(w: Word) -> Word:
    return (*set_last(w, _A), ("ت", _U))


def dual(w: Word) -> Word:
    return (*set_last(w, _A), ("ا", SUKUN), ("ن", _I))


def jam_m(w: Word) -> Word:
    return (*set_last(w, _U), ("و", SUKUN), ("ن", _A))


def jam_f(w: Word) -> Word:
    return (*set_last(w, _A), ("ا", SUKUN), ("ت", _U))


def number(w: Word) -> str:
    """العددُ من اللاحقة: َانِ/َيْنِ مثنًّى، ُونَ/ِينَ وَات جمعٌ، وما سواه مفرد."""

    if len(w) >= 3:
        n, g, p = w[-1], w[-2], w[-3]
        if n == ("ن", _I) and g[1] == SUKUN and g[0] in "اي" and p[1] == _A:
            return "مثنى"
        if n == ("ن", _A) and g[1] == SUKUN and g[0] in "وي":
            return "جمع"
        if n[0] == "ت" and g == ("ا", SUKUN) and p[1] == _A:
            return "جمع"
        if n == ("ن", SUKUN) and g[0] == "ت" and p == ("ا", SUKUN):
            return "جمع"
    return "مفرد"


def _core(w: Word) -> Word:
    return w if number(w) == "مفرد" else w[:-2]


def _ends_with_at(w: Word) -> bool:
    return len(w) >= 2 and w[-1][0] == "ت" and w[-2] == ("ا", SUKUN)


def gender(w: Word) -> str:
    """الجنس: جمعُ المؤنّث السالم، أو تاءُ التأنيث بعد فتحٍ في آخر الجذع (تحت التثنية والجمع)."""

    if number(w) == "جمع" and _ends_with_at(w):
        return "مؤنث"
    core = _core(w)
    if len(core) >= 2 and core[-1][0] == "ت" and core[-2][1] == _A:
        return "مؤنث"
    return "مذكر"


def _bare(w: Word) -> Word:
    return w[2:] if has_al(w) else w


def broken_plural(w: Word) -> bool:
    """جمعُ التكسير احتمالًا: على قالبٍ من قوالب الجموع (83–100 ومنتهى الجموع)."""

    b = set_last(_bare(w), _U)
    return any(on_template(k, b) for k in (*range(83, 101), *MUNTAHA))


def agree(m: Word, k: Word) -> bool:
    return gender(m) == gender(k) and number(m) == number(k)


def agree_loose(m: Word, k: Word) -> bool:
    """استثناءُ الحصر: جمعُ غير العاقل مع مفردٍ مؤنّث أو جمعٍ مؤنّثٍ سالم — العقلُ معجم."""

    return agree(m, k) or (
        broken_plural(m) and gender(k) == "مؤنث" and number(k) in ("مفرد", "جمع"))


# — الرابط —


_RABIT: Final[tuple[Word, ...]] = (*_AID, *(p.cells for p in ATTACHED_RAF), cells_of("وْنَ"),
                                    cells_of("يْنَ"), (("ا", SUKUN), ("ن", _I)))


def rabit(m: Word, w: Word) -> str:
    """الرابطُ بين المبتدأ وكلمةٍ من جملة الخبر: إعادةُ اللفظ، أو إشارة، أو ضميرٌ متّصل (نصبًا ورفعًا)."""

    if w == m:
        return "إعادة اللفظ"
    if w in _ISHARA:
        return "إشارة"
    return "ضمير" if any(len(p) < len(w) and w[-len(p):] == p for p in _RABIT) else "—"


WITNESSES: Final[dict[str, Jumla]] = {
    "فِي الدَّارِ رَجُلٌ": Jumla(cells_of("رَجُلٌ"), (*cells_of("فِي"), *cells_of("اَدَّارِ")), True),
    "أَيْنَ الْمَفَرُّ": Jumla(cells_of("اَلْمَفَرُّ"), cells_of("أَيْنَ"), True),
    "فِي الْمَدْرَسَةِ طُلَّابُهَا": Jumla(cells_of("طُلَّابُهَا"), (*cells_of("فِي"), *cells_of("اَلْمَدْرَسَةِ")),
                                     True),
    "زَيْدٌ دَرَسَ": Jumla(cells_of("زَيْدٌ"), cells_of("دَرَسَ")),
    "أَخِي رَفِيقِي": Jumla(cells_of("أَخِي"), cells_of("رَفِيقِي")),
    "لَزَيْدٌ قَائِمٌ": Jumla(lam(cells_of("زَيْدٌ")), cells_of("قَائِمٌ")),
    "السَّلَامَةُ فِي التَّأَنِّي": Jumla(cells_of("اَسَّلَامَةُ"), (*cells_of("فِي"), *cells_of("اَتَّأَنِّي"))),
}


def _check() -> None:
    expected = ("تقديم الخبر", "تقديم الخبر", "تقديم الخبر", "تقديم المبتدأ", "تقديم المبتدأ",
                "تقديم المبتدأ", "جواز")
    for (name, j), r in zip(WITNESSES.items(), expected, strict=True):
        if order(j) != r or not admissible(j):
            raise ValueError(f"ORDER:{name}")
    talib, mujtahid = cells_of("طَالِبُ"), cells_of("مُجْتَهِدُ")
    assert agree(talib, mujtahid) and agree(ta_nith(talib), ta_nith(mujtahid))
    assert agree(dual(talib), dual(mujtahid)) and agree(jam_m(talib), jam_m(mujtahid))
    assert not agree(talib, ta_nith(mujtahid)) and gender(dual(ta_nith(talib))) == "مؤنث"
    assert all(licensed(op(talib)) for op in (ta_nith, dual, jam_m, jam_f))
    assert broken_plural(cells_of("اَلْجِبَالُ")) and agree_loose(cells_of("اَلْجِبَالُ"), cells_of("شَاهِقَةُ"))
    assert rabit(cells_of("زَيْدٌ"), cells_of("أَبُوهُ")) == "ضمير"


_check()
