"""الدالّةُ الفراكتاليّة (`A116.Fractal`، ADR ٧٧) من الصفر إلى آخر نصّ — على المصحف كلِّه.

التوقّعاتُ مستقلّةٌ عن Lean: آلةُ التوريث مكتوبةٌ هنا باليد من الأزواج الستّة. **الأثرُ** دالّةٌ من الحالات
الأربع (الابتداء، cv، v، c) إلى حالةٍ أو انقطاع، ممثَّلةً صفًّا من أربع قيم.
١. **الصفر**: أثرُ الفارغ الهويّة، وهو محايدُ التركيب يمينًا ويسارًا، والتركيبُ تجميعيّ
   على كلّ ثلاثة آثارٍ متتاليةٍ لكلمات أوّل ستّين آية.
٢. **نفسُها جبريًّا من الخانة إلى آخر نصّ**: أثرُ المصحف محسوبًا طبقةً طبقة
   (الخانات ← الكلمة ← الآية ← النصّ) تركيبًا يساوي أثرَه مسطَّحًا خانةً خانة؛ وكذلك كلُّ آية.
٣. **الجسرُ إلى البوّابة**: لكلّ كلمةٍ جاهزةٍ من المصحف، أثرُها من الابتداء غيرُ منقطعٍ
   ⟺ `continue_licensed` على أصنافها.
٤. الطفرة `MUTANT_COMPOSE_REVERSED`: التركيبُ معكوسًا يخالف التسطيح.
"""

from __future__ import annotations

from functools import reduce
from pathlib import Path

from gate import Refusal, enter
from gate.licence import continue_licensed, kind_of

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpora" / "quran-simple-enhanced.txt"

STATES = ("start", "cv", "v", "c")
DEAD = "dead"
WASL = {("cv", "cv"), ("cv", "v"), ("cv", "c"), ("v", "cv"), ("v", "c"), ("c", "cv")}
Athar = tuple[str, str, str, str]
ZERO: Athar = STATES


def step(state: str, x: str) -> str:
    """يرث `state` ويورث `x`، أو ينقطع."""
    if state == DEAD:
        return DEAD
    if state == "start":
        return x if x == "cv" else DEAD
    return x if (state, x) in WASL else DEAD


def athar_of(kinds: list[str]) -> Athar:
    out = []
    for s in STATES:
        for x in kinds:
            s = step(s, x)
        out.append(s)
    return (out[0], out[1], out[2], out[3])


def apply(f: Athar, s: str) -> str:
    return DEAD if s == DEAD else f[STATES.index(s)]


def compose(f: Athar, g: Athar) -> Athar:
    """f ثمّ g (كلايسلي)."""
    return (apply(g, f[0]), apply(g, f[1]), apply(g, f[2]), apply(g, f[3]))


def corpus() -> list[list[list[str]]]:
    """المصحف: آياتٌ، كلُّ آيةٍ كلماتٌ، كلُّ كلمةٍ أصنافُ خاناتها (الجاهزُ وحدَه)."""
    text = []
    for line in CORPUS.read_text(encoding="utf-8").splitlines():
        ayah = []
        for w in line.split():
            cert = enter(w.encode("utf-8"))
            if not isinstance(cert, Refusal):
                ayah.append(list(kind_of(cert.atoms)))
        text.append(ayah)
    return text


TEXT = corpus()


def test_zero_identity_and_assoc() -> None:
    words = [athar_of(w) for ayah in TEXT[:60] for w in ayah]
    assert athar_of([]) == ZERO
    for f in words:
        assert compose(ZERO, f) == f and compose(f, ZERO) == f
    for f, g, h in zip(words, words[1:], words[2:], strict=False):
        assert compose(compose(f, g), h) == compose(f, compose(g, h))


def test_same_from_cell_to_last_text() -> None:
    assert len(TEXT) == 6236
    ayat = []
    for ayah in TEXT:
        level1 = [athar_of(w) for w in ayah]
        a = reduce(compose, level1, ZERO)
        assert a == athar_of([x for w in ayah for x in w]), ayah
        ayat.append(a)
    whole = reduce(compose, ayat, ZERO)
    flat = [x for ayah in TEXT for w in ayah for x in w]
    assert whole == athar_of(flat)


def test_bridge_to_gate() -> None:
    n = 0
    for ayah in TEXT:
        for w in ayah:
            assert (athar_of(w)[0] != DEAD) == continue_licensed(w), w
            n += 1
    assert n > 0


def test_mutant_compose_reversed() -> None:
    def rev(f: Athar, g: Athar) -> Athar:
        return compose(g, f)
    bad = 0
    for ayah in TEXT[:200]:
        level1 = [athar_of(w) for w in ayah]
        if reduce(rev, level1, ZERO) != athar_of([x for w in ayah for x in w]):
            bad += 1
    assert bad > 0
