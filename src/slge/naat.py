"""النعتُ الحقيقيّ: مطابقةٌ في أربعة من الخانة، والحملُ واحدٌ والفرقُ التعريف، والجملةُ بعد النكرة نعت.

مرآةُ `Naat`. المتّجهُ الرباعيّ يُقرأ من الخانات (`vec`): الإعرابُ (`tawabi.case_class`)، والتعريفُ (نفيُ
`jumla.nakira`)، والجنسُ والعددُ تحت التنوين (`jumla.gender`، `jumla.number`). النعتُ الحقيقيّ مطابقةٌ في
الأربعة (`naat_ok`)، والمخالفُ إعرابًا أو تعريفًا ممنوع. النعتُ والخبرُ على معرفةٍ مرفوعةٍ يتّفقان في ثلاثةٍ
ويفترقان في التعريف (`haml_kind`). الجملةُ بعد النكرة نعتٌ وبعد المعرفة حالٌ (`jumla_mahall`). العمليّةُ
`naat` تجعل الجذعَ على إعراب المنعوت وتعريفه. القياسُ على MASAQ في `tools/gen_naat_index.py`.
"""

from __future__ import annotations

from slge.categories import PRONOUNS
from slge.cells import Cell
from slge.jumla import agree, gender, is_verb, nakira, number
from slge.majrurat import jarr
from slge.marifa import al, drop_tanwin, has_al
from slge.nawasikh import nasb, raf, tanwin
from slge.tawabi import case_class, follows

__all__ = ["haml_kind", "jumla_mahall", "naat", "naat_ok", "vec"]

Word = tuple[Cell, ...]


def vec(w: Word) -> tuple[str, bool, str, str]:
    """(الإعراب، معرفة؟، الجنس، العدد) من الخانات."""

    return case_class(w), not nakira(w), gender(drop_tanwin(w)), number(drop_tanwin(w))


def naat_ok(m: Word, n: Word) -> bool:
    """النعتُ الحقيقيّ: تبعٌ في الإعراب، وتعريفٌ واحد، وجنسٌ وعددٌ موافقان."""

    return follows(n, m) and nakira(m) == nakira(n) and agree(drop_tanwin(m), drop_tanwin(n))


def haml_kind(m: Word, n: Word) -> str:
    """على المعرفة المرفوعة: مطابقٌ في الأربعة ⇒ نعت؛ مرفوعٌ موافقٌ نكرةٌ بعد معرفة ⇒ خبر."""

    if naat_ok(m, n):
        return "نعت"
    if (case_class(m) == "رفع" == case_class(n) and agree(drop_tanwin(m), drop_tanwin(n))
            and not nakira(m) and nakira(n)):
        return "خبر"
    return "—"


def jumla_mahall(prev: Word) -> str:
    """الجملُ بعد النكرات صفات، وبعد المعارف المقروءةِ الإعراب أحوال."""

    if is_verb(prev) or prev in PRONOUNS:
        return "—"
    if nakira(prev):
        return "نعت"
    return "حال" if case_class(prev) != "لا تقرؤه الخانة" else "—"


def naat(m: Word, k: Word) -> Word:
    """الجذعُ على إعراب المنعوت (رفع/نصب/جرّ) ثمّ على تعريفه (أل أو تنوين)."""

    cc = case_class(m)
    k2 = raf(k) if cc == "رفع" else nasb(k) if cc == "نصب" else jarr(k) if cc == "جرّ" else k
    if has_al(m):
        return al(k2)
    return tanwin(k2) if nakira(m) else k2


def _check() -> None:
    from slge.jumla import dual, ta_nith
    from slge.rawabit import cells_of

    rajul, tawil = cells_of("رَجُلُ"), cells_of("طَوِيلُ")
    alrajul, rajulun = al(rajul), tanwin(rajul)
    rajulan, alrajuli = tanwin(nasb(rajul)), al(jarr(rajul))
    for m in (alrajul, rajulun, rajulan, alrajuli):
        assert naat_ok(m, naat(m, tawil)) and haml_kind(m, naat(m, tawil)) == "نعت", m
    assert naat(alrajul, tawil) == cells_of("اَطَّوِيلُ") and naat(rajulun, tawil) == cells_of("طَوِيلٌ")
    madrasa, kabira = ta_nith(cells_of("مَدْرَسُ")), ta_nith(cells_of("كَبِيرُ"))
    assert naat_ok(tanwin(madrasa), naat(tanwin(madrasa), kabira))
    assert not naat_ok(rajulun, tanwin(nasb(tawil))) and not naat_ok(rajulun, al(tawil))
    assert not naat_ok(rajulun, tanwin(kabira)) and not naat_ok(dual(rajul), tanwin(tawil))
    assert haml_kind(alrajul, tanwin(tawil)) == "خبر" and haml_kind(rajulun, al(tawil)) == "—"
    assert jumla_mahall(rajulan) == "نعت" and jumla_mahall(nasb(alrajul)) == "حال"
    assert jumla_mahall(cells_of("دَرَسَ")) == "—"
    assert vec(rajulun) == ("رفع", False, "مذكر", "مفرد")


_check()
