"""قيدُ الحدّ نظامًا على (صنف، خانة) (`A116.NizamHadd`، ADR ٢٥).

التوقّعاتُ مستقلّةٌ عن Lean وعن شيفرة القيد:
١. الأدوار: جدولُ `lake exe a116-table roles` المودَع — مئةٌ وستّ عشرةَ دورًا، لكلّ دورٍ عددٌ وحيد،
   والصنفُ باقي العدد على 3 (cv = 0، v = 1، c = 2) وعددُ الخانة حاصلُه؛ وبالعدّ باليد من الشبكة:
   المتحرّكُ 28 حاملًا × 3 حركات (الألفُ لا تتحرّك) = 84، والساكنُ مُغلِقًا 29، والمدُّ ثلاثة (ا، و، ي)
   — فالخانةُ ذاتُ الدورين حرفُ مدٍّ ساكن.
٢. النافذة: قاعدةٌ مكتوبةٌ هنا — ابتداءٌ بمتحرّك، وكلُّ زوجٍ مأذون، وكلُّ (مدّ، مُغلِق، بعد) بعدُه بحامل
   المُغلِق، ولا (مدّ، مُغلِق) في الطرف وصلًا — تساوي `strict_licensed`؛ ووقفًا (الزوجُ (c، c) طرفًا، وبلا
   شرط الطرف) تساوي `strict_pause_licensed` — على كلّ كلمةٍ من {بَ، بْ، تْ، تَ، اْ} من خانتين إلى سبع
   (لا همزةَ فيها، فلا مدَّ فرق: ذاك استثناءٌ مسمًّى خارج النظام، `farq_outside_nizam`).
٣. الطفرتان: نافذةٌ لا تشترط الحامل (`MUTANT_NO_CARRIER`)، وطرفٌ مأذونٌ وصلًا (`MUTANT_TARAF_OPEN`).
"""

from __future__ import annotations

from itertools import product
from pathlib import Path

from gate.licence import SUKUN, kind_of, strict_licensed, strict_pause_licensed

ROOT = Path(__file__).resolve().parents[1]
ROLES = ROOT / "formal" / "a116" / "roles.csv"
KN = {"cv": 0, "v": 1, "c": 2}
WASL = {("cv", "cv"), ("cv", "v"), ("cv", "c"), ("v", "cv"), ("v", "c"), ("c", "cv")}


def test_every_role_has_its_number() -> None:
    rows = [line.rstrip("\n").split(",") for line in ROLES.open(encoding="utf-8")]
    assert len(rows) == 116
    ns = [int(n) for *_, n in rows]
    assert len(set(ns)) == 116
    for atom, kind, cell, n in rows:
        assert int(n) % 3 == KN[kind] and int(n) // 3 == int(cell)
    kinds = [k for _, k, _, _ in rows]
    assert (kinds.count("cv"), kinds.count("c"), kinds.count("v")) == (84, 29, 3)
    two = {a for a, *_ in rows if [r[0] for r in rows].count(a) == 2}
    assert two == {"ا" + SUKUN, "و" + SUKUN, "ي" + SUKUN}


def rule(w: tuple[str, ...], pause: bool, carrier: bool = True, taraf: bool = True) -> bool:
    k = kind_of(w)
    if not k or k[0] != "cv":
        return False
    for i in range(len(k) - 1):
        last = i == len(k) - 2
        if (k[i], k[i + 1]) not in WASL and not (pause and last and (k[i], k[i + 1]) == ("c", "c")):
            return False
    for i in range(len(k) - 2):
        if k[i] == "v" and k[i + 1] == "c" and carrier and w[i + 1][0] != w[i + 2][0]:
            return False
    return not (taraf and not pause and len(k) >= 2 and (k[-2], k[-1]) == ("v", "c"))


ALPHABET = ("بَ", "بْ", "تْ", "تَ", "ا" + SUKUN)
WORDS = [w for n in range(2, 8) for w in product(ALPHABET, repeat=n)]


def test_window_rule_is_the_gate() -> None:
    for w in WORDS:
        assert strict_licensed(w) == rule(w, pause=False), w
        assert strict_pause_licensed(w) == rule(w, pause=True), w


def test_named_mutants_disagree() -> None:
    # MUTANT_NO_CARRIER
    assert any(strict_licensed(w) != rule(w, False, carrier=False) for w in WORDS)
    # MUTANT_TARAF_OPEN
    assert any(strict_licensed(w) != rule(w, False, taraf=False) for w in WORDS)
