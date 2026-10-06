"""شبهُ الجملة: صورتان على الخانة، وزائدٌ يُردّ بعمليّة، وتعلُّقٌ ومحلٌّ يُقرآن ممّا قبلها — مرآةُ `Shibh.lean`.

الجارُّ والمجرور حرفٌ من `majrurat.HARFS` ثمّ جرٌّ على الآخر (`jarr_majrur`)؛ والظرفُ اسمٌ من جداول
`zuruf`/`zaman` منصوبًا (`zarf`)؛ والقارئُ `kind` يفرزهما. ردُّ الزائد رفعٌ يُعيد الاسمَ بعينه
(`zaid_restores`: مَا جَاءَ مِنْ أَحَدٍ = مَا جَاءَ أَحَدٌ). الجدولُ حاصر: المختصُّ (المسجد) لا يُقرأ ظرفًا فيُجرّ.
المرتكزُ ممّا قبل شبه الجملة: فعلٌ، مشتقٌّ، أو الكونُ المحذوف (`anchor`)؛ والمحلُّ من خانة ما قبلها: صلةٌ بعد
الموصول، نعتٌ بعد النكرة، خبرٌ بعد المعرفة المرفوعة، حالٌ بعد المنصوبة (`mahall`)؛ والكونُ المحذوفُ بحالة
المحلّ (`kawn`). القياسُ على MASAQ في `tools/gen_shibh_index.py`.
"""

from __future__ import annotations

from typing import Final

from slge.categories import PRONOUNS
from slge.cells import STATES, Cell, licensed
from slge.filiyya import is_zarf, verb_root
from slge.jumla import is_verb, shibh_jumla
from slge.majrurat import HARFS, jarr
from slge.mansubat import derived
from slge.marifa import MAWSUL, al, drop_tanwin
from slge.nawasikh import nasb, raf, tanwin
from slge.nida import has_tanwin
from slge.rawabit import cells_of
from slge.tawabi import case_class
from slge.zuruf import STEMS as ZURUF_STEMS
from slge.zuruf import set_last

__all__ = ["HARFS", "KAIN", "anchor", "jarr_majrur", "kawn", "kind", "mahall", "zaid_restores",
           "zarf"]

_A, _I, _U, SUKUN = STATES
Word = tuple[Cell, ...]


def jarr_majrur(h: Word, w: Word) -> Word:
    """الحرفُ ثمّ الاسمُ مجرورًا."""

    return (*h, *jarr(w))


def zarf(w: Word) -> Word:
    return nasb(w)


def kind(w: Word) -> str:
    """ظرفٌ من الجدول، أو جارٌّ ومجرور من الصدر، أو ليس شبهَ جملة."""

    if is_zarf(w):
        return "ظرف"
    return "جار ومجرور" if shibh_jumla(w) else "—"


def zaid_restores(w: Word) -> bool:
    """ردُّ الزائد: رفعُ المجرور بالزائد هو رفعُ الاسم بعينه."""

    return raf(jarr(w)) == raf(w)


def anchor(prev: Word) -> str:
    """المرتكزُ ممّا قبل شبه الجملة: فعلٌ، مشتقٌّ، وإلّا فالكونُ المحذوف."""

    if is_verb(prev):
        return "فعل"
    if derived(drop_tanwin(prev)):
        return "مشتق"
    return "كون محذوف"


_MAWSUL: Final[frozenset[Word]] = frozenset(MAWSUL.values())


def mahall(prev: Word) -> str:
    """المحلُّ من خانة ما قبلها: صلة، خبر (ضميرٌ منفصل أو معرفةٌ مرفوعة)، نعت، حال، أو لا يُقرأ."""

    if prev in _MAWSUL:
        return "صلة"
    if prev in PRONOUNS:
        return "خبر"
    if has_tanwin(prev):
        return "نعت"
    cc = case_class(prev)
    if cc == "رفع":
        return "خبر"
    if cc in ("نصب", "جرّ", "نصب/جرّ"):
        return "حال"
    return "—"


KAIN: Final[Word] = cells_of("كَائِنُ")
_ISTAQARRA: Final[Word] = cells_of("اِسْتَقَرَّ")


def kawn(m: str) -> Word:
    """الكونُ العامُّ المحذوف بحالة المحلّ: كَائِنٌ خبرًا، كَائِنًا نعتًا وحالًا، اسْتَقَرَّ صلةً."""

    if m == "خبر":
        return tanwin(raf(KAIN))
    if m in ("نعت", "حال"):
        return tanwin(nasb(KAIN))
    return _ISTAQARRA if m == "صلة" else ()


def _check() -> None:
    fi, dar = cells_of("فِي"), cells_of("اَدَّارُ")
    assert kind(jarr_majrur(fi, dar)) == "جار ومجرور" and case_class(jarr(dar)) == "جرّ"
    assert licensed(jarr_majrur(fi, dar)) and kind(cells_of("لَهُمْ")) == "جار ومجرور"
    assert kind(zarf(cells_of("فَوْقُ"))) == "ظرف" and kind(cells_of("مَسَاءً")) == "ظرف"
    assert kind(zarf(cells_of("مَسْجِدُ"))) == "—" and len(ZURUF_STEMS) == 17
    assert kind(jarr_majrur(fi, al(cells_of("مَسْجِدُ")))) == "جار ومجرور"
    assert all(zaid_restores(cells_of(w)) for w in ("أَحَدُ", "كِتَابُ", "رَجُلُ"))
    min_ahad = (*jarr_majrur(cells_of("مِنْ"), cells_of("أَحَدُ")), ("ن", SUKUN))
    assert min_ahad == cells_of("مِنْأَحَدٍ")
    assert anchor(cells_of("جَلَسَ")) == "فعل" and anchor(cells_of("قَائِمٌ")) == "مشتق"
    assert anchor(cells_of("اَلْعِلْمُ")) == "كون محذوف"
    assert mahall(cells_of("اَلْعِلْمُ")) == "خبر" and mahall(cells_of("طَائِرًا")) == "نعت"
    assert mahall(cells_of("اَلْعُصْفُورَ")) == "حال" and mahall(cells_of("اَلَّذِي")) == "صلة"
    assert case_class(kawn("خبر")) == "رفع" and case_class(kawn("حال")) == "نصب"
    assert all(licensed(kawn(m)) for m in ("خبر", "نعت", "حال", "صلة"))
    assert verb_root(kawn("صلة")) is None and set_last(KAIN, _A) == cells_of("كَائِنَ")


_check()
