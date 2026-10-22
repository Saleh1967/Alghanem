"""العمليّةُ المحفوظة على عدد الخانات (ADR ١٢١، `A116/AmaliyyaHafiza.lean`).

* **الشاهدُ المستقلّ:**
  * عددُ الخانات ‎F‎ يُحسب هنا من تعريفه مكتوبًا باليد:
    ‎F(w) = Σ_{j<|w|} 116ʲ + Σ dᵢ·116^(|w|−1−i)‎.
  * والرقمُ ‎dᵢ = 4·(موضعُ الحامل في `gate.bridge.ALPHABET`) + الحالة‎.
* **ثلاثةُ مصادر تتّفق على «كَتَبَ» و«كُتِبَ»:**
  * المعادلةُ باليد.
  * والعددُ الذي تطبعه البوّابة: ‎integer = P(F, rank)‎، فيُفكّ الزوج هنا بيدٍ أخرى.
  * والثوابتُ في نصّ Lean (`shahid_raqm`).
* **على أعداد البوّابة** (كلماتُ أوّل ستّين سطرًا من المصحف المختوم، الجاهزةُ منها):
  * عددُ البوّابة المفكوك هو ‎F‎ المكتوبُ باليد على ذرّاتها.
  * والوصلُ ‎F(w) = 116^|v|·F(u) + F(v)‎ لكلّ موضع قسمة، والتبديلُ على «كَتَبَ»/«كُتِبَ».
* **طفرتان على مادّةٍ مفحوصة:** أسٌّ مُزاح في الوصل، وقلبُ حاملين في ترتيب الجسر؛
  كلتاهما تخالف أعدادَ البوّابة.
"""

from __future__ import annotations

import re
from math import isqrt
from pathlib import Path

import gate
from gate.bridge import ALPHABET

ROOT = Path(__file__).resolve().parents[1]
LEAN = (ROOT / "formal" / "a116" / "A116" / "AmaliyyaHafiza.lean").read_text(encoding="utf-8")
HARAKA = {"َ": 0, "ُ": 1, "ِ": 2, "ْ": 3}  # فتحة، ضمّة، كسرة، سكون


def F(ds: list[int]) -> int:
    n = len(ds)
    return sum(116 ** j for j in range(n)) + sum(d * 116 ** (n - 1 - i) for i, d in enumerate(ds))


def digits_of(word: str) -> list[int]:
    out, i = [], 0
    while i < len(word):
        out.append(4 * ALPHABET.index(word[i]) + HARAKA[word[i + 1]])
        i += 2
    return out


def unpair(n: int) -> tuple[int, int]:
    """عكسُ ‎pair u r = tri (u + r) + r‎ (`Numbering.pair`)، مكتوبًا هنا."""
    w = (isqrt(8 * n + 1) - 1) // 2
    r = n - w * (w + 1) // 2
    return w - r, r


def lean_literals() -> list[int]:
    m = re.search(r"theorem shahid_raqm :(.*?):= by", LEAN, re.S)
    assert m
    return [int(x) for x in re.findall(r"= (\d+)", m.group(1))]


def test_hand_digits() -> None:
    assert digits_of("كَتَبَ") == [84, 8, 4]
    assert digits_of("كُتِبَ") == [85, 10, 4]


def test_three_sources_agree() -> None:
    lits = lean_literals()
    assert lits == [85, 1049, 1158497, 1144809]
    for word, expected in (("كَتَبَ", 1144809), ("كُتِبَ", 1158497)):
        assert F(digits_of(word)) == expected
        cert = gate.enter(word.encode("utf-8"))
        assert isinstance(cert, gate.Certificate), word
        u, rank = unpair(cert.integer)
        assert (u, rank) == (expected, 0), word
    assert F([84]) == 85 and F([8, 4]) == 1049
    assert F([84, 8, 4]) == 116 ** 2 * F([84]) + F([8, 4])


def corpus_words(limit: int = 60) -> list[tuple[list[int], int]]:
    """كلماتُ أوّل ‎limit‎ سطرًا من المصحف المختوم: رقمُ خاناتها من ذرّات البوّابة، و‎F‎ من عددها المفكوك."""
    path = ROOT / "corpora" / "quran-simple-enhanced.txt"
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines[:limit]:
        for w in line.split():
            cert = gate.enter(w.encode("utf-8"))
            if not isinstance(cert, gate.Certificate):
                continue
            ds = [4 * ALPHABET.index(x[0]) + HARAKA[x[1]] for x in cert.core.atoms]
            out.append((ds, unpair(cert.integer)[0]))
    return out


WORDS = corpus_words()


def test_gate_number_is_hand_formula() -> None:
    """عددُ البوّابة على كلّ كلمةٍ جاهزة هو ‎F‎ المكتوبُ هنا باليد."""
    assert len(WORDS) > 500
    for ds, f_gate in WORDS:
        assert f_gate == F(ds), ds


def test_concat_law_on_gate_numbers() -> None:
    """الوصلُ على أعداد البوّابة: لكلّ كلمةٍ ولكلّ موضع قسمة ‎F(w) = 116^|v|·F(u) + F(v)‎."""
    for ds, f_gate in WORDS:
        for k in range(len(ds) + 1):
            u, v = ds[:k], ds[k:]
            assert f_gate == 116 ** len(v) * F(u) + F(v)


def test_substitution_law_on_gate_numbers() -> None:
    """التبديلُ: بين «كَتَبَ» و«كُتِبَ» عددا البوّابة بفرق الرقمين في ‎116^(ما بعدهما)‎."""
    k1, k2 = (unpair(c.integer)[0] for c in (gate.enter(w.encode("utf-8")) for w in ("كَتَبَ", "كُتِبَ"))
              if isinstance(c, gate.Certificate))
    assert k2 - k1 == (85 - 84) * 116 ** 2 + (10 - 8) * 116 == 13688


def test_mutants_refused_on_gate_numbers() -> None:
    """طفرتان على مادّةٍ مفحوصة: أسٌّ مُزاح، وترتيبُ حاملين مقلوب — كلتاهما تخالف أعدادَ البوّابة."""
    shifted = sum(1 for ds, f in WORDS if len(ds) > 1
                  and f != 116 ** (len(ds) - 1 + 1) * F(ds[:1]) + F(ds[1:]))
    assert shifted == sum(1 for ds, _ in WORDS if len(ds) > 1)
    swap = {0: 4 * ALPHABET.index("ب"), 4 * ALPHABET.index("ب"): 0}
    def mutate(ds: list[int]) -> list[int]:
        return [swap.get(d - d % 4, d - d % 4) + d % 4 for d in ds]
    assert any(f != F(mutate(ds)) for ds, f in WORDS)


def test_lean_definitions() -> None:
    assert "def wasl (p q : Nat × Nat) : Nat × Nat := (116 ^ q.2 * p.1 + q.1, p.2 + q.2)" in LEAN
    assert "∀ a, g (J.enc a) = (f a).map K.enc" in LEAN
    assert "sorry" not in LEAN
