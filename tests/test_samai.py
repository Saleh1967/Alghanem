"""الحذفُ السماعيّ (ADR ٤٠): خُذْ، كُلْ، مُرْ قائمةٌ مغلقة من الكتاب لا قاعدةٌ صوتيّة.

التوقّعاتُ مكتوبةٌ باليد من نصّ سيبويه («وأما ما جاء من الأفعال فخذ وكل ومر، وبعض العرب يقول أوكل فيتم»
س18368–18369؛ «فقف على هذه الأشياء حيث وقفوا» س2700–2701): أصلُ كُلُوا ءُءْكُلُوا على قالب الأمر
ءُفْعُلْ وجذرُه ء ك ل مشهودٌ في المقاييس، وكذا خُذْ ومُرْ؛ وما سوى الثلاثة لا يمسّه الحذف — يُؤْمِنُ أوّلًا.
والطفراتُ (قائمةٌ رابعة، قاعدةٌ صوتيّةٌ عامّة، إسقاطُ شرط الضمّ) تُرفض بتوقّعاتٍ مسمّاة.
"""

from __future__ import annotations

from collections.abc import Callable

from slge.cells import SUKUN, Cell, licensed
from slge.ilal import HEARD, RULES, apply, ascend, down, positions, record, restore, undo
from slge.jidh import jidh
from slge.maqayis import attested, roots_of
from slge.rawabit import cells_of

Word = tuple[Cell, ...]
H_U: Cell = ("ء", "ضم")
H_S: Cell = ("ء", SUKUN)


def samai_roots(word: str) -> set[tuple[str, bool]]:
    """جذورُ القراءات التي سلسلتُها الحذفُ السماعيّ، ومشهودُها في المقاييس."""

    return {("".join(x), attested(r)) for r in jidh(cells_of(word))
            if any(rule == "SAMAI_FA" for rule, _ in r.ilal) for x in roots_of(r)}


def test_the_list_is_closed_and_last() -> None:
    assert RULES[-1] == "SAMAI_FA" and len(RULES) == 14
    assert set(HEARD) == {("خ", "ذ"), ("ك", "ل"), ("م", "ر")}


def test_kulu_khudh_mur_read_their_original() -> None:
    assert samai_roots("وَكُلُوْ") == {("ءكل", True)}
    assert samai_roots("كُلُوْ") == {("ءكل", True)}
    assert samai_roots("فَكُلِي") == {("ءكل", True)}
    assert samai_roots("خُذْ") == {("ءخذ", True)}
    assert samai_roots("خُذُوْ") == {("ءخذ", True)}
    assert samai_roots("مُرْ") == {("ءمر", True)}
    # الأصلُ بعينه، والصعودُ إليه، والردُّ بالسجلّ
    r = next(r for r in jidh(cells_of("وَكُلُوْ")) if r.ilal == (("SAMAI_FA", 0),))
    assert r.pre == ((("و", "فتح"),),) and r.asl == cells_of("ءُءْكُلُ") and r.templates == (10,)
    assert ascend(r.ilal, (*r.asl, *r.suf)) == (*r.stem, *r.suf)
    u = cells_of("ءُءْخُذْ")
    assert apply("SAMAI_FA", u, 0) == cells_of("خُذْ")
    assert restore(cells_of("خُذْ"), record("SAMAI_FA", u, 0)) == u
    assert licensed(u) and licensed(cells_of("خُذْ"))  # samai_closed


def test_what_is_not_listed_is_untouched() -> None:
    for word in ("يُؤْمِنُ", "قُلْ", "كُتُبٌ", "وَكَلَ", "وُكِّلُوْ"):
        w = cells_of(word)
        assert all(not undo("SAMAI_FA", w, i) for i in range(len(w) + 1)), word
        assert not samai_roots(word), word
    # النافذةُ صدرُ الجذع فتنزل مُرْسَلٌ إلى ءُءْمُرْسَلٌ، والقالبُ (ءُفْعُلْ) هو الحاصرُ في الأمر: لا قراءة
    assert undo("SAMAI_FA", cells_of("مُرْسَلٌ"), 0) and not samai_roots("مُرْسَلٌ")
    # وموضعُه صدرُ الجذع وحدَه (`positions`): أُكُلَهَا تقبله في الموضع 1 ولا يُستعمل فيه
    assert undo("SAMAI_FA", cells_of("أُكُلَهَا"), 1) and not samai_roots("أُكُلَهَا")
    assert positions("SAMAI_FA", 4) == (0,)
    # المضمومُ بلا قائمة (كُتُبٌ) والقائمةُ بلا ضمّ (وَكَلَ، كَلَّ) كلاهما خارج القاعدة
    assert down("SAMAI_FA", cells_of("كَلَ")) == ()


Down = Callable[[Word], tuple[Word, ...]]


def _expectations(dn: Down) -> list[str]:
    """التوقّعاتُ المسمّاة على دالّة نزول: ما يُرفض به المتحوّل."""

    bad = []
    if dn(cells_of("كُلُوْ")) != ((H_U, H_S, *cells_of("كُلُوْ")),):
        bad.append("KUL_NOT_RESTORED")
    if dn(cells_of("يُؤْمِنُ")):
        bad.append("YUMIN_TOUCHED")
    if dn(cells_of("قُلْ")):
        bad.append("FOURTH_VERB_ADMITTED")
    if dn(cells_of("كَلَ")):
        bad.append("DAMMA_NOT_REQUIRED")
    return bad


def test_mutants_are_refused_by_name() -> None:
    assert _expectations(lambda w: down("SAMAI_FA", w)) == []

    def fourth(w: Word) -> tuple[Word, ...]:  # قائمةٌ رابعة: قُلْ
        if len(w) >= 2 and w[0][1] == "ضم" and (w[0][0], w[1][0]) in (*HEARD, ("ق", "ل")):
            return ((H_U, H_S, *w),)
        return ()

    def general(w: Word) -> tuple[Word, ...]:  # قاعدةٌ صوتيّةٌ عامّة: كلُّ مضمومٍ أوّلًا
        return ((H_U, H_S, *w),) if len(w) >= 2 and w[0][1] == "ضم" else ()

    def no_damma(w: Word) -> tuple[Word, ...]:  # إسقاطُ شرط الضمّ
        return ((H_U, H_S, *w),) if len(w) >= 2 and (w[0][0], w[1][0]) in HEARD else ()

    assert _expectations(fourth) == ["FOURTH_VERB_ADMITTED"]
    assert _expectations(general) == ["YUMIN_TOUCHED", "FOURTH_VERB_ADMITTED"]
    assert _expectations(no_damma) == ["DAMMA_NOT_REQUIRED"]
