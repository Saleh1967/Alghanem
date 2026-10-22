"""نواةُ التوريث بتّاتٍ (`A116.TawrithBit`، ADR ١١٩).

التوقّعاتُ مستقلّةٌ عن الشيفرة المفحوصة:
١. جدولا البتّ والتعارض على القيم التسع مكتوبان باليد.
٢. صيغتا القناعين (البتّ والتعارض) في نصّ Lean بعينهما، والمرآةُ على أعدادٍ طبيعيّة
   (لا قوائم) تطابق الجدولَ المكتوب باليد خانةً خانة على كلّ الأزواج حتى عرض أربع خانات —
   فحصٌ للصيغة على `int` لا برهان (`BIT_LIST_NOT_NAT_MASK` في Lean).
٣. الأعدادُ بالعدّ الصريح: الأزواجُ ‎9ⁿ‎ والمتّسقةُ ‎7ⁿ‎ للأعراض 0–5، وللخامسة أرقامُ المرفق
   59,049 / 16,807 / 42,242.
٤. على الجدول المكتوب باليد: «الأوّلُ يغلب» و«الثاني يغلب» يفترقان في أزواج التعارض وحدَها —
   فحصٌ للجدولين لا لـMashru ولا لـ`maurutha` (مقابلتُهما بهما قراءةُ البنّاء، معلنة في
   ADR ١١٩؛ والمبرهَنُ `batt_comm_iff`).
٥. ثلاثُ طفراتٍ تُقتل: أسبقيّةٌ معكوسة، تعارضٌ بلا قناع المعلوم، بتٌّ بلا قناع المجهول.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from itertools import product
from pathlib import Path

LEAN = Path(__file__).resolve().parents[1] / "formal" / "a116" / "A116" / "TawrithBit.lean"

N, L, U = "naam", "la", "la_hukm"
VALS = (N, L, U)

# ١. باليد: (الأوّل، الثاني) ← البتّ، والتعارض.
BATT = {
    (N, N): N, (N, L): N, (N, U): N,
    (L, N): L, (L, L): L, (L, U): L,
    (U, N): N, (U, L): L, (U, U): U,
}
TANAQUD = {(N, L), (L, N)}

Mask = tuple[int, int]


def enc(state: tuple[str, ...]) -> Mask:
    known = sum((q != U) << i for i, q in enumerate(state))
    value = sum((q == N) << i for i, q in enumerate(state))
    return known, value


def dec(m: Mask, width: int) -> tuple[str, ...]:
    k, v = m
    assert v & ~k == 0
    return tuple(U if not (k >> i) & 1 else N if (v >> i) & 1 else L for i in range(width))


def fast(p: Mask, f: Mask) -> Mask:
    """صيغةُ `fastQ` في Lean: ‎(k₁ ∨ k₂, v₁ ∨ (¬k₁ ∧ v₂))‎."""
    return p[0] | f[0], p[1] | (~p[0] & f[1])


def conflict(p: Mask, f: Mask) -> int:
    """صيغةُ `conflictQ` في Lean: ‎k₁ ∧ k₂ ∧ (v₁ ⊕ v₂)‎."""
    return p[0] & f[0] & (p[1] ^ f[1])


def check(fast_: Callable[[Mask, Mask], Mask], conflict_: Callable[[Mask, Mask], int],
          width: int) -> list[str]:
    errs = []
    for s in product(VALS, repeat=width):
        for t in product(VALS, repeat=width):
            m = fast_(enc(s), enc(t))
            got = None if m[1] & ~m[0] else dec(m, width)
            want = tuple(BATT[(a, b)] for a, b in zip(s, t))
            if got != want:
                errs.append(f"BATT {s} {t}")
            c = conflict_(enc(s), enc(t))
            if c != sum(((a, b) in TANAQUD) << i for i, (a, b) in enumerate(zip(s, t))):
                errs.append(f"CONFLICT {s} {t}")
    return errs


def test_lean_formulas_are_the_mirror() -> None:
    text = LEAN.read_text(encoding="utf-8")
    assert ("def fastQ (p f : Bool × Bool) : Bool × Bool := "
            "(p.1 || f.1, p.2 || (!p.1 && f.2))") in text
    assert "def conflictQ (p f : Bool × Bool) : Bool := p.1 && f.1 && (p.2 != f.2)" in text
    assert re.search(r"\| some b, _ => some b\n\s*\| none, f => f", text)


def test_mirror_against_hand_tables() -> None:
    for w in range(5):
        assert check(fast, conflict, w) == [], w


def counts(width: int) -> tuple[int, int]:
    total = ok = 0
    for s in product(VALS, repeat=width):
        for t in product(VALS, repeat=width):
            total += 1
            ok += all((a, b) not in TANAQUD for a, b in zip(s, t))
    return total, ok


def test_counts_all_widths() -> None:
    for w in range(6):
        assert counts(w) == (9 ** w, 7 ** w), w
    total, ok = counts(5)
    assert (total, ok, total - ok) == (59049, 16807, 42242)


def test_precedences_differ_only_on_conflict() -> None:
    # «الثاني يغلب» جدولٌ يدويٌّ ثانٍ، لا قلبٌ للأوّل في الشيفرة.
    second_wins = {
        (N, N): N, (N, L): L, (N, U): N,
        (L, N): N, (L, L): L, (L, U): L,
        (U, N): N, (U, L): L, (U, U): U,
    }
    differ = {k for k in BATT if BATT[k] != second_wins[k]}
    assert differ == {(N, L), (L, N)}


def test_mutants_killed() -> None:
    def flipped(p: Mask, f: Mask) -> Mask:            # أسبقيّةٌ معكوسة
        return fast(f, p)

    def conflict_no_known(p: Mask, f: Mask) -> int:   # تعارضٌ بلا قناع المعلوم
        return p[1] ^ f[1]

    def fast_no_unknown(p: Mask, f: Mask) -> Mask:    # بتٌّ بلا قناع المجهول
        return p[0] | f[0], p[1] | f[1]

    assert check(flipped, conflict, 1), "MUTANT_PRECEDENCE_FLIPPED"
    assert check(fast, conflict_no_known, 1), "MUTANT_CONFLICT_NO_KNOWN"
    assert check(fast_no_unknown, conflict, 1), "MUTANT_FAST_NO_UNKNOWN"
