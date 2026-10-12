"""الحدُّ بين كلمتين مثولًا للنواة (`A116.NizamLine`، ADR ٢٧): الترخيصُ من الخانة إلى السطر.

التوقّعاتُ مستقلّةٌ عن Lean وعن شيفرة الحدّ: قاعدةُ السطر مكتوبةٌ هنا على أصناف السطر موصولًا —
التسطيحُ مرخَّصٌ بقيد الحدّ، ولكلّ حدٍّ بين كلمتين: لا (مدّ، مُغلِق) عابرٌ (آخرُ الأولى، أوّلُ الثانية)، ولا (مدّ،
مُغلِق) آخرَ الأولى داخلَها — ثمّ:
١. سطرٌ من كلمتين: القاعدةُ تساوي `strict_joined` و`strict_joined_pause` في البوّابة، على كلّ زوجِ
   كلماتٍ من {بَ، بْ، تْ، اْ} بطول 1 … 3.
٢. سطرٌ من ثلاث: القاعدةُ تساوي التسطيحَ مرخَّصًا وألّا تقطع قافيةُ مدٍّ أيَّ حدٍّ (`straddles` بين السابق كلِّه
   واللاحق كلِّه) — على كلّ ثلاثٍ بطول 1 … 2.
٣. الطفرتان: حدٌّ بلا شرطه الثاني (`MUTANT_SEAM_ONE_SIDED`)، وحدٌّ لا يُفحص (`MUTANT_NO_SEAM`).
"""

from __future__ import annotations

from itertools import product

from gate.licence import (
    SUKUN,
    kind_of,
    straddles,
    strict_joined,
    strict_joined_pause,
    strict_licensed,
    strict_pause_licensed,
)

ALPHABET = ("بَ", "بْ", "تْ", "ا" + SUKUN)


def words(max_len: int) -> list[tuple[str, ...]]:
    return [w for n in range(1, max_len + 1) for w in product(ALPHABET, repeat=n)]


def line_rule(ws: tuple[tuple[str, ...], ...], pause: bool, second: bool = True,
              seams: bool = True) -> bool:
    flat = tuple(a for w in ws for a in w)
    if not (strict_pause_licensed(flat) if pause else strict_licensed(flat)):
        return False
    if not seams:
        return True
    k = kind_of(flat)
    b = 0
    for w in ws[:-1]:
        start, b = b, b + len(w)
        if k[b - 1] == "v" and k[b] == "c":
            return False
        if second and b - start >= 2 and k[b - 2] == "v" and k[b - 1] == "c":
            return False
    return True


W3 = words(3)
PAIRS = [(a, b) for a in W3 for b in W3]
W2 = words(2)
TRIPLES = [(a, b, c) for a in W2 for b in W2 for c in W2]


def test_two_word_line_is_strict_joined() -> None:
    for left, right in PAIRS:
        assert line_rule((left, right), pause=False) == strict_joined(left, right), (left, right)
        assert line_rule((left, right), pause=True) == strict_joined_pause(left, right)


def test_three_word_line_is_every_seam() -> None:
    for ws in TRIPLES:
        flat = ws[0] + ws[1] + ws[2]
        gate = strict_licensed(flat) and not straddles(ws[0], ws[1] + ws[2]) and not straddles(
            ws[0] + ws[1], ws[2])
        assert line_rule(ws, pause=False) == gate, ws


def test_named_mutants_disagree() -> None:
    # MUTANT_SEAM_ONE_SIDED
    assert any(line_rule(p, False, second=False) != strict_joined(*p) for p in PAIRS)
    # MUTANT_NO_SEAM
    assert any(line_rule(p, False, seams=False) != strict_joined(*p) for p in PAIRS)
