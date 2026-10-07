"""النِّسَبُ الثلاث: الإسنادُ عمليّةٌ واحدة، والتقييدُ لا يُنشئ رفعًا، والتضمينُ ترتيبٌ جزئيّ — مرآةُ `Nisab`.

الإسناد: المسندُ إليه مرفوعٌ بعمليّةٍ واحدةٍ في الجملتين (`isnad`). التقييد: الحالُ والتمييزُ والمفعولُ نصبٌ،
والإضافةُ والجارُّ جرٌّ، والنعتُ تبعٌ (`taqyid_case`). التضمين: الجزئيّةُ المرتَّبة على الخانات (`contains`:
انعكاسيّةٌ متعدّيةٌ متضادّةُ التباين)، والصورةُ تتضمّن جذرَها (`form_contains_root`)، والفصلُ: ما اختلف قالبُه
اختلفت صورتُه (`species_distinct`)، وسلسلةُ أسلاف الوزن في الشبكة (`chain`، `dist`). القارئُ `nisba`
يقرأ النسبةَ بين كلمتين من خانتيهما؛ والتضمينُ بين كلمتين معنًى. القياسُ على MASAQ في
`tools/gen_nisab_index.py`.
"""

from __future__ import annotations

from typing import Final

from slge.cells import STATES, Cell
from slge.filiyya import has_subject, verb_root
from slge.jumla import is_verb, mubtada_kind, nakira, shibh_jumla
from slge.shabaka import CLASSICAL, ROOT
from slge.tawabi import case_class
from slge.wazn import AWZAN, FAL, fill, mizan

__all__ = ["F", "chain", "contains", "dist", "form_contains_root", "isnad", "nisba",
           "species_distinct", "taqyid_case"]

_A, _I, _U, SUKUN = STATES
Word = tuple[Cell, ...]
F: Final[int] = 125


def isnad(m: Word) -> Word:
    """المسندُ إليه مرفوع: مبتدأُ الاسميّة وفاعلُ الفعليّة ونائبُه عمليّةٌ واحدة."""

    from slge.nawasikh import raf

    return raf(m)


def taqyid_case(kind: str, w: Word) -> str:
    """حالةُ المقيِّد: نصبٌ (حال، تمييز، مفعول)، جرٌّ (إضافة، جارّ)، أو تبعٌ لمتبوعه (نعت)."""

    from slge.majrurat import jarr
    from slge.mansubat import hal

    if kind in ("حال", "تمييز", "مفعول"):
        return case_class(hal(w))
    if kind in ("إضافة", "جارّ"):
        return case_class(jarr(w))
    return "تبع"


def contains(big: tuple[object, ...], small: tuple[object, ...]) -> bool:
    """الجزئيّةُ المرتَّبة: `small` جزءٌ من `big` بترتيبه (انعكاسيّةٌ متعدّيةٌ متضادّةُ التباين)."""

    i = 0
    for x in big:
        if i < len(small) and small[i] == x:
            i += 1
    return i == len(small)


def form_contains_root(k: int, root: tuple[str, str, str]) -> bool:
    return contains(tuple(c[0] for c in fill(AWZAN[k].template, root)), root)


def species_distinct() -> bool:
    """ما اختلف قالبُه اختلفت صورتُه على الميزان؛ والقالبُ المودَعُ مرّتين (فِعَال) صورةٌ واحدة."""

    return all((mizan(a.template) == mizan(b.template)) == (a.template == b.template)
               for a in AWZAN for b in AWZAN)


_NAMES: Final[tuple[str, ...]] = tuple(w.name for w in AWZAN)


def chain(k: int, fuel: int = F) -> list[int]:
    """سلسلةُ أسلاف الوزن في شبكة البصريّين حتى الجذر."""

    out = [k]
    name = _NAMES[k]
    while fuel > 0 and name != ROOT and name in CLASSICAL:
        name = CLASSICAL[name]
        out.append(_NAMES.index(name))
        fuel -= 1
    return out


def dist(k: int, fuel: int = F) -> int:
    return len(chain(k, fuel)) - 1


def _musnad_ilayh(w: Word) -> bool:
    return mubtada_kind(w) != "—" or verb_root(w) is not None or has_subject(w)


def nisba(prev: Word, w: Word) -> str:
    """النسبةُ بين كلمتين من خانتيهما: إسناد، تقييد، أو لا تُقرأ (والتضمينُ بين كلمتين معنًى)."""

    if is_verb(w) or shibh_jumla(w):
        return "إسناد" if mubtada_kind(prev) != "—" else "—"
    if mubtada_kind(w) in ("مبني", "ضمير"):  # الموصولُ والإشارةُ والضميرُ فاعلًا أو خبرًا
        return "إسناد" if _musnad_ilayh(prev) else "—"
    cc = case_class(w)
    if cc == "نصب":
        return "تقييد"  # النصبُ فضلةٌ: تقييدٌ أبدًا
    if cc in ("جرّ", "نصب/جرّ"):
        return "تقييد"
    if cc == "رفع":
        if nakira(prev) and nakira(w) and case_class(prev) == "رفع":
            return "تقييد"
        return "إسناد" if _musnad_ilayh(prev) else "—"
    return "—"


def _check() -> None:
    from slge.rawabit import cells_of

    assert case_class(isnad(cells_of("اَلْعِلْمَ"))) == "رفع"
    assert taqyid_case("حال", cells_of("رَاكِبُ")) == "نصب"
    assert taqyid_case("إضافة", cells_of("زَيْدُ")) == "جرّ"
    a, b, c = (1, 2, 3), (1, 3), (3,)
    assert contains(a, a) and contains(a, b) and contains(b, c) and contains(a, c)
    assert not (contains(b, a) and contains(a, b)) and not contains(c, b)
    assert all(form_contains_root(k, FAL) for k in range(len(AWZAN)))
    assert species_distinct() and chain(_NAMES.index(ROOT)) == [29] and dist(7) == 3
    assert nisba(cells_of("اَلْعِلْمُ"), cells_of("نُورٌ")) == "إسناد"
    assert nisba(cells_of("رَجُلٌ"), cells_of("كَرِيمٌ")) == "تقييد"
    assert nisba(cells_of("كِتَابُ"), cells_of("زَيْدٍ")) == "تقييد"
    assert nisba(cells_of("اَلْعِلْمُ"), cells_of("دَرَسَ")) == "إسناد"
    assert nisba(cells_of("دَرَسَ"), cells_of("دَرَسَ")) == "—"


_check()
