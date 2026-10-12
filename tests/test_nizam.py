"""نظامُ الأنظمة (`A116.Nizam`، ADR ٢٣): الترخيصُ الثلاثيّ علاقةُ جوارٍ محضة.

التوقّعاتُ مستقلّةٌ عن Lean وعن `gate.licence`: الأزواجُ المأذونة تُعدّ هنا باليد من المقاطع الستّة —
داخلَ المقطع (cv ثمّ ما يليه، v ثمّ c في CVVC) وعلى حدّ مقطعين (ما يسبق cv) — فتكون ستّةً وصلًا،
و(c، c) وقفًا طرفًا وحدَه؛ ثمّ:
١. جدولُ `lake exe a116-table nizam` المودَع يطابقها زوجًا زوجًا.
٢. القاعدةُ المحلّيّة (ابتداءٌ بمتحرّك، وكلُّ زوجٍ مأذون، و(c، c) في الطرف وقفًا) تساوي `continue_licensed`
   و`pause_licensed` في البوّابة على كلّ متتاليةٍ من الأصناف حتى عشر ذرّات.
٣. الطفرتان: حذفُ (v، c) من المأذون (`MUTANT_NO_MADD_CLOSER`) وإذنُ (c، c) وصلًا (`MUTANT_CC_IN_WASL`)
   يخالفان البوّابة.
"""

from __future__ import annotations

from itertools import product
from pathlib import Path

from gate.licence import continue_licensed, pause_licensed

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "formal" / "a116" / "nizam.csv"
KS = ("cv", "v", "c")

# باليد من المقاطع: بعد المتحرّك أيُّ صنف؛ المدُّ يليه متحرّكٌ (CVV|CV) أو ساكنٌ يُغلق (CVVC)؛
# والساكنُ المُغلِق يليه متحرّكٌ وحده وصلًا.
WASL = {("cv", "cv"), ("cv", "v"), ("cv", "c"), ("v", "cv"), ("v", "c"), ("c", "cv")}
WAQF = {("c", "c")}  # CVCC وCVVCC: طرفًا وحدَه


def local(k: tuple[str, ...], pause: bool, wasl: set[tuple[str, str]] = WASL,
          waqf: set[tuple[str, str]] = WAQF) -> bool:
    if not k:
        return True
    if k[0] != "cv":
        return False
    pairs = list(zip(k, k[1:], strict=False))
    for i, p in enumerate(pairs):
        last = i == len(pairs) - 1
        if p not in wasl and not (pause and last and p in waqf):
            return False
    return True


def seqs(n: int) -> list[tuple[str, ...]]:
    return [s for m in range(n + 1) for s in product(KS, repeat=m)]


SEQS = seqs(10)


def test_table_matches_hand_count() -> None:
    rows = [line.rstrip("\n").split(",") for line in TABLE.open(encoding="utf-8")]
    assert len(rows) == 9
    assert {(a, b) for a, b, w, _ in rows if w == "true"} == WASL
    assert {(a, b) for a, b, _, q in rows if q == "true"} == WAQF


def test_local_rule_is_the_gate() -> None:
    for k in SEQS:
        assert continue_licensed(k) == local(k, pause=False), k
        assert pause_licensed(k) == local(k, pause=True), k


def test_named_mutants_disagree_with_the_gate() -> None:
    no_closer = WASL - {("v", "c")}
    assert any(continue_licensed(k) != local(k, False, wasl=no_closer)
               for k in SEQS)  # MUTANT_NO_MADD_CLOSER
    cc = WASL | {("c", "c")}
    assert any(continue_licensed(k) != local(k, False, wasl=cc) for k in SEQS)  # MUTANT_CC_IN_WASL
