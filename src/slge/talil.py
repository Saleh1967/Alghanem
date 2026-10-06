"""التعليلُ والسببيّة: العلّةُ فضلةٌ لا تُرفَع، وصورتاها كلمةٌ واحدة، والسببيّةُ ترتيبٌ صارم — مرآةُ `Talil`.

المفعولُ لأجله مصدرٌ منصوب (`maful_li_ajlih`)، وفرزُه عن المطلق بالجذر (`filiyya.sort_fadla`). صورتا
التعليل (نصبُ المصدر، جرُّه بالحرف) كلمةٌ بعينها إلّا خانةَ الآخر (`two_forms_same_word`). أدواتُ التعليل
جدولٌ حاصر (`TOOLS`) بعملها: جرُّ الاسم، عملُ إِنَّ (لِأَنَّ)، نصبُ المضارع (`apply`)؛ وليس فيها ما يرفع
العلّة. السببيّةُ الاشتقاقيّة: المصدرُ علّةُ المشتقّ — `derives(a, b)`: `b` سلفُ `a` في شبكة البصريّين،
ترتيبٌ جزئيٌّ صارم (لا انعكاس، تعدٍّ، لا دور). التنازعُ: إعمالُ الثاني لقربه والأوّلُ بضميره (`tanazu`).
القارئُ `talil` يقرأ التعليلَ بين كلمتين من خانتيهما. القياسُ على MASAQ في `tools/gen_talil_index.py`.
السلسلةُ هنا من `shabaka.CLASSICAL` مباشرةً (لا من `nisab`: الطبقةُ واحدة).
"""

from __future__ import annotations

from typing import Final

from slge.cells import STATES, Cell, licensed
from slge.damair import attach
from slge.filiyya import masdar_root, sort_fadla
from slge.majrurat import jarr
from slge.marifa import has_al
from slge.nawasikh import AMAL, nasb
from slge.rawabit import PARTICLES, cells_of
from slge.shabaka import CLASSICAL, ROOT
from slge.tawabi import case_class
from slge.wazn import AWZAN

__all__ = ["LI_ANNA", "MIN_AJLI", "TOOLS", "F", "apply", "derives", "maful_li_ajlih", "talil",
           "tanazu", "two_forms_same_word"]

_A, _I, _U, SUKUN = STATES
Word = tuple[Cell, ...]
F: Final[int] = 121


def maful_li_ajlih(w: Word) -> Word:
    """مصدرٌ منصوب؛ التنوينُ عمليّةٌ أخرى (المضافُ بلا تنوين: حَذَرَ الْمَوْتِ)."""

    return nasb(w)


def two_forms_same_word(w: Word) -> bool:
    """النصبُ مصدرًا والجرُّ بالحرف كلمةٌ بعينها: ما قبل الآخر واحدٌ والطولُ واحد."""

    a, b = maful_li_ajlih(w), jarr(w)
    return a[:-1] == b[:-1] and len(a) == len(b)


LI: Final[Word] = cells_of("لِ")
BI: Final[Word] = cells_of("بِ")
MIN_AJLI: Final[Word] = (*cells_of("مِنْ"), *jarr(cells_of("أَجْلُ")))
LI_ANNA: Final[Word] = (*LI, *cells_of("أَنَّ"))
KAY: Final[Word] = cells_of("كَيْ")

# (الاسم، الخانات، العمل): جرُّ الاسم | عملُ إِنَّ | نصبُ المضارع
TOOLS: Final[tuple[tuple[str, Word, str], ...]] = (
    ("لِ", LI, "جرّ"), ("بِ", BI, "جرّ"), ("مِنْ أَجْلِ", MIN_AJLI, "جرّ"),
    ("لِأَنَّ", LI_ANNA, "إنّ"), ("كَيْ", KAY, "نصب الفعل"), ("لِ (كي)", LI, "نصب الفعل"),
)


def apply(amal: str, w: Word) -> Word:
    """عملُ الأداة على الخانة: جرٌّ، أو نصبُ اسم إِنَّ، أو نصبُ المضارع — لا رفعَ فيها."""

    if amal == "جرّ":
        return jarr(w)
    if amal == "إنّ":
        assert AMAL["إنّ"] == ("نصب", "رفع")
        return nasb(w)
    return nasb(w)


_NAMES: Final[tuple[str, ...]] = tuple(w.name for w in AWZAN)


def _chain(k: int, fuel: int = F) -> list[int]:
    out, name = [k], _NAMES[k]
    while fuel > 0 and name != ROOT and name in CLASSICAL:
        name = CLASSICAL[name]
        out.append(_NAMES.index(name))
        fuel -= 1
    return out


def derives(a: int, b: int) -> bool:
    """`b` علّةُ `a`: سلفٌ له في شبكة البصريّين (المصدرُ أصلُ المشتقّ)."""

    return b in _chain(a)[1:]


def tanazu(v1: Word, v2: Word, w: Word, p: Word) -> tuple[Word, Word, Word]:
    """إعمالُ الثاني لقربه: الأوّلُ بضميره متّصلًا، والثاني ناصبٌ للمتنازَع فيه."""

    return attach(v1, p), v2, nasb(w)


def talil(prev: Word, w: Word) -> str:
    """لِأَنَّ؛ مصدرٌ منصوبٌ بلا «ال» بغير جذر الفعل ⇒ لأجله؛ لِ/بِ على مصدرٍ مجرور ⇒ بالحرف (احتمال)."""

    if w == LI_ANNA:
        return "لأنّ"
    if case_class(w) == "نصب" and not has_al(w) and sort_fadla(w, prev) == "مفعول لأجله":
        return "مفعول لأجله"
    if w[:1] in (LI, BI) and masdar_root(w[1:]) is not None and case_class(w) == "جرّ":
        return "تعليل بالحرف"
    return "—"


def _check() -> None:
    darasa, hadhar, dars = cells_of("دَرَسَ"), cells_of("حَذَرَ"), cells_of("دَرْسَ")
    assert case_class(maful_li_ajlih(hadhar)) == "نصب" and two_forms_same_word(hadhar)
    assert sort_fadla(hadhar, darasa) == "مفعول لأجله" and sort_fadla(dars, darasa) == "مفعول مطلق"
    assert all(licensed(cs) for _, cs, _ in TOOLS) and len(TOOLS) == 6
    names = {p.name: p.amal for p in PARTICLES}
    assert all(names[n] == "جرّ" for n in ("لِ", "بِ", "مِنْ")) and names["كَيْ"] == "نصب"
    assert all(case_class(apply(a, cells_of("زَيْدُ"))) != "رفع" for _, _, a in TOOLS)
    assert case_class(jarr(cells_of("أَجْلُ"))) == "جرّ" and licensed(MIN_AJLI)
    ks = range(len(AWZAN))
    assert not any(derives(k, k) for k in ks)
    assert all(derives(a, ROOT_K) for a in ks if a != ROOT_K)
    assert not any(derives(ROOT_K, b) for b in ks)
    assert all(not derives(b, a) for a in ks for b in ks if derives(a, b))
    t = tanazu(cells_of("عَلِمْتُ"), cells_of("عَمِلْتُ"), cells_of("اَلْخَيْرُ"), (("ه", _U),))
    assert t[0] == cells_of("عَلِمْتُهُ") and licensed(t[0]) and case_class(t[2]) == "نصب"
    assert talil(darasa, hadhar) == "مفعول لأجله" and talil(darasa, dars) == "—"
    assert talil(darasa, (*BI, *cells_of("ضَرْبِ"))) == "تعليل بالحرف"
    assert talil(darasa, (*LI, *cells_of("حِكْمَةِ"))) == "تعليل بالحرف"
    assert talil(darasa, LI_ANNA) == "لأنّ" and talil(darasa, cells_of("زَيْدٌ")) == "—"
    assert talil(cells_of("أَكَلَ"), cells_of("اَدَّرْسَ")) == "—"


ROOT_K: Final[int] = _NAMES.index(ROOT)
_check()
