"""جدولُ الوقف بقيد الحدّ (`A116.ExhaustPause`، ADR ١٨) وقانونُ «ا و ا و ا».

التوقّعاتُ مستقلّةٌ عن شيفرة Lean:

١. المرآة: جدولُ الدرجة d وقفًا يُبنى هنا باليد — ‎d − 1‎ داخليّةً من {CV، CVV، CVC، CVVC} بالأساس 4
   (الأقدمُ أعلى) ثمّ طرفيٌّ من الستّة — ويطابق `lake exe a116-table degrees-pause` (510 أسطر مودَعة):
   ‎6·4^(d−1)‎ صفًّا لكلّ درجة، بلا تكرار، والعدد ‎6·I(t) + d(u)‎.
٢. الجامعُ والمانع على `gate.licence.strict_pause_licensed` (لا على Lean): كلُّ كلمةٍ من {بَ، بْ، اْ، تْ}
   حتى تسع ذرّاتٍ مرخَّصةٍ وقفًا بقيد الحدّ صفٌّ في جدول درجتها، وكلُّ صفٍّ من الدرجتين 1 و2 تحقّقه كلمةٌ منها.
٣. الوصلُ داخلَ الوقف: كلُّ صفٍّ وصلًا (`degrees.csv`) صفٌّ وقفًا، والزيادةُ ‎3·4^(d−1)‎ هي الأطرافُ الثلاثة.
٤. «ا و ا و ا»: على الكلمات نفسها، المرخَّصُ وصلًا مرخَّصٌ وقفًا، والمرخَّصُ وقفًا لا يبدأ بساكن.
٥. الطفرتان: مرآةٌ تسقط CVVC من أطراف الوقف (`MUTANT_NO_MADD_ARID`) ومرآةٌ تعدّ بالأساس 3
   (`MUTANT_BASE3`) يُسقطهما الجدول.
"""

from __future__ import annotations

from itertools import product
from pathlib import Path

from gate.licence import SUKUN, kind_of, parse, strict_licensed, strict_pause_licensed

ROOT = Path(__file__).resolve().parents[1]
PAUSE = ROOT / "formal" / "a116" / "degrees-pause.csv"
CONT = ROOT / "formal" / "a116" / "degrees.csv"

INNER = ("CV", "CVV", "CVC", "CVVC")
PAUSE_FINAL = ("CV", "CVV", "CVC", "CVVC", "CVCC", "CVVCC")


def _rows(path: Path) -> list[tuple[int, int, str]]:
    out = []
    for line in path.open(encoding="utf-8"):
        d, n, ss = line.rstrip("\n").split(",")
        out.append((int(d), int(n), ss))
    return out


def _mirror(finals: tuple[str, ...] = PAUSE_FINAL, base: int = 4) -> list[tuple[int, int, str]]:
    out = []
    for d in range(1, 5):
        for t in product(INNER, repeat=d - 1):
            for u in finals:
                i = 0
                for s in t:
                    i = base * i + INNER.index(s)
                out.append((d, len(finals) * i + finals.index(u), "-".join((*t, u))))
    return sorted(out)


def test_pause_table_matches_mirror() -> None:
    rows = _rows(PAUSE)
    assert len(rows) == 510
    assert [sum(1 for r in rows if r[0] == d) for d in (1, 2, 3, 4)] == [6, 24, 96, 384]
    assert sorted(rows) == _mirror()
    assert [n for d, n, _ in rows if d == 3] == list(range(96))
    assert len({(d, ss) for d, _, ss in rows}) == 510


def test_named_mutants_are_refused() -> None:
    lean = sorted(_rows(PAUSE))
    no_arid = tuple(f for f in PAUSE_FINAL if f != "CVVC")
    assert _mirror(finals=no_arid) != lean  # MUTANT_NO_MADD_ARID
    assert _mirror(base=3) != lean  # MUTANT_BASE3


ALPHABET = ("بَ", "بْ", "ا" + SUKUN, "تْ")


def _words(max_len: int) -> list[tuple[str, ...]]:
    return [w for n in range(1, max_len + 1) for w in product(ALPHABET, repeat=n)]


WORDS = _words(9)


def _row(w: tuple[str, ...]) -> str | None:
    p = parse(kind_of(w))
    if p is None or p[0] != "none":
        return None
    return "-".join(p[1])


def test_jami_and_mani_on_gate_licence() -> None:
    table = {(d, ss) for d, _, ss in _rows(PAUSE)}
    seen = set()
    licensed = 0
    for w in WORDS:
        if strict_pause_licensed(w):
            licensed += 1
            row = _row(w)
            assert row is not None
            d = row.count("-") + 1
            if d <= 4:
                assert (d, row) in table, (w, row)  # الجامع
                seen.add((d, row))
    assert licensed > 0
    # المانع: كلُّ صفٍّ من الدرجتين 1 و2 تحقّقه كلمةٌ مرخَّصة (أطولُها CVVC-CVVCC: تسعُ ذرّات)
    assert {r for r in table if r[0] <= 2} <= seen


def test_continue_inside_pause() -> None:
    pause = {(d, ss) for d, _, ss in _rows(PAUSE)}
    cont = {(d, ss) for d, _, ss in _rows(CONT)}
    assert cont <= pause
    extra = pause - cont
    assert [sum(1 for r in extra if r[0] == d) for d in (1, 2, 3, 4)] == [3, 12, 48, 192]
    assert {ss.split("-")[-1] for _, ss in extra} == {"CVVC", "CVCC", "CVVCC"}


def test_awa_chain_on_gate_licence() -> None:
    wasl = waqf = 0
    for w in WORDS:
        if strict_licensed(w):
            wasl += 1
            assert strict_pause_licensed(w), w  # الوصلُ ⇒ الوقف
        if strict_pause_licensed(w):
            waqf += 1
            assert not w[0].endswith(SUKUN), w  # الوقفُ ⇒ الابتداء
    assert 0 < wasl < waqf
    # الشاهدان: بَاتْ مرخَّصٌ وقفًا لا وصلًا (المدُّ العارض)، وبَاتْبَ لا يُرخَّص (المُغلِقُ غيرُ مدغم)
    bat = ("بَ", "ا" + SUKUN, "تْ")
    assert strict_pause_licensed(bat) and not strict_licensed(bat)
    assert not strict_pause_licensed(("بَ", "ا" + SUKUN, "تْ", "بَ"))
