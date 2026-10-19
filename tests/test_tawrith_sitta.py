"""التوريثُ بين الطبقات (`A116.TawrithSitta`، ADR ٧٦) على البوّابة.

التوقّعاتُ مستقلّةٌ عن Lean: آلةٌ مكتوبةٌ هنا باليد من الأزواج الستّة (لا من `gate`) تمشي على الكلمات
كلمةً كلمة — كلُّ كلمةٍ ترث آخرَ صنفٍ ممّا قبلها، والأولى من الابتداء — ثمّ تُقابَل
بـ`continue_licensed` على السطر مسطّحًا.
١. على كلّ تقسيمٍ لكلّ متتاليةٍ حتى ثماني ذرّات إلى كلمات، توريثُ الكلمات هو ترخيصُ التسطيح (`lic_lift`).
٢. الشاهد: «cv» بعد «cv c» يُوصل و«c» بعده لا، و«c» وحده لا يُبتدأ (`shahid_tabaqat`).
٣. الطفرة `MUTANT_WORD_REINIT`: كلمةٌ تبتدئ من القانون لا ممّا قبلها تخالف البوّابة.
"""

from __future__ import annotations

from itertools import product

from gate.licence import continue_licensed

KS = ("cv", "v", "c")
WASL = {("cv", "cv"), ("cv", "v"), ("cv", "c"), ("v", "cv"), ("v", "c"), ("c", "cv")}


def step(state: str | None, x: str) -> str | None:
    """يرث `state` ويورث `x`، أو يُمنع (`None`)."""
    if state is None:
        return x if x == "cv" else None
    return x if (state, x) in WASL else None


def words_licensed(words: list[tuple[str, ...]], reinit: bool = False) -> bool:
    state: str | None = None
    for w in words:
        if reinit:
            state = None
        for x in w:
            state = step(state, x)
            if state is None:
                return False
    return True


def splits(seq: tuple[str, ...]) -> list[list[tuple[str, ...]]]:
    out = []
    n = len(seq)
    for cuts in product((False, True), repeat=max(n - 1, 0)):
        words, cur = [], [seq[0]] if seq else []
        for i, c in enumerate(cuts):
            if c:
                words.append(tuple(cur))
                cur = []
            cur.append(seq[i + 1])
        if cur:
            words.append(tuple(cur))
        out.append(words)
    return out


SEQS = [s for m in range(1, 9) for s in product(KS, repeat=m)]


def test_layers_inherit() -> None:
    n = 0
    for s in SEQS:
        g = continue_licensed(s)
        for ws in splits(s):
            assert words_licensed(ws) == g, (s, ws)
            n += 1
    assert n > len(SEQS)


def test_shahid() -> None:
    assert words_licensed([("cv", "c"), ("cv",)]) and continue_licensed(("cv", "c", "cv"))
    assert not words_licensed([("cv", "c"), ("c",)]) and not continue_licensed(("cv", "c", "c"))
    assert not words_licensed([("c",)]) and not continue_licensed(("c",))


def test_mutant_reinit_rejected() -> None:
    bad = [(s, ws) for s in SEQS[:400] for ws in splits(s)
           if words_licensed(ws, reinit=True) != continue_licensed(s)]
    assert bad
