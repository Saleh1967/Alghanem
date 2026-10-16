"""قانونُ التوريث (`A116.Tawrith`، ADR ٧٥) على البوّابة.

التوقّعاتُ مستقلّةٌ عن Lean: تُقرأ من `gate.licence` وحدَها على كلّ متتاليات الأصناف.
١. **يرث ما قبله ويورث ما بعده**: كلُّ سابقٍ مرخَّصٍ وصلًا حتى سبع ذرّات، مجموعًا بآخر صنفٍ فيه،
   لا يفترق ما بعده حتى أربع ذرّات — فالحالةُ الموروثةُ آخرُ صنف (مثولُ `ofNizam`).
٢. **والحالةُ حدٌّ أدنى**: الأصنافُ الثلاثة يفصلها لاحقٌ مثنى مثنى، فلا تُدمج حالتان.
٣. **الوقفُ لا يورث**: ما رُخّص وقفًا ولم يُرخَّص وصلًا لا يُوصل بعده صنف.
٤. الطفرتان: حالةٌ تنسى المدّ (`MUTANT_STATE_FORGETS_MADD`) ووقفٌ يورث (`MUTANT_WAQF_INHERITS`) تُرفضان.
"""

from __future__ import annotations

from collections.abc import Callable
from itertools import product

from gate.licence import continue_licensed, pause_licensed

KS = ("cv", "v", "c")


def seqs(n: int) -> list[tuple[str, ...]]:
    return [s for m in range(n + 1) for s in product(KS, repeat=m)]


PREFIXES = [a for a in seqs(7) if a and continue_licensed(a)]
SUFFIXES = seqs(4)


def violations(state: Callable[[tuple[str, ...]], object]) -> list[tuple[tuple[str, ...], ...]]:
    """سابقان بحالةٍ واحدة يفترق بعدهما لاحق."""
    seen: dict[object, tuple[str, ...]] = {}
    bad = []
    for a in PREFIXES:
        rep = seen.setdefault(state(a), a)
        for b in SUFFIXES:
            if continue_licensed(rep + b) != continue_licensed(a + b):
                bad.append((rep, a, b))
                break
    return bad


def test_state_is_last_kind() -> None:
    assert {a[-1] for a in PREFIXES} == set(KS)
    assert violations(lambda a: a[-1]) == []


def test_state_is_minimal() -> None:
    reps = {k: next(a for a in PREFIXES if a[-1] == k) for k in KS}
    for x, y in product(KS, repeat=2):
        if x != y:
            assert any(continue_licensed(reps[x] + b) != continue_licensed(reps[y] + b)
                       for b in SUFFIXES), (x, y)


def test_waqf_does_not_bequeath() -> None:
    waqf_only = [a for a in seqs(7) if pause_licensed(a) and not continue_licensed(a)]
    assert waqf_only
    for a in waqf_only:
        for x in KS:
            assert not pause_licensed(a + (x,)), (a, x)


def test_mutants_rejected() -> None:
    # MUTANT_STATE_FORGETS_MADD: الحالةُ متحرّكٌ أو ساكنٌ فحسب، فيندمج المدُّ بالمُغلِق.
    assert violations(lambda a: a[-1] == "cv") != []

    # MUTANT_WAQF_INHERITS: وقفٌ يجيز (c، c) في أيّ موضع — أي يورث ما بعده.
    def mutant_pause(k: tuple[str, ...]) -> bool:
        allowed = {("cv", "cv"), ("cv", "v"), ("cv", "c"), ("v", "cv"), ("v", "c"),
                   ("c", "cv"), ("c", "c")}
        return bool(k) and k[0] == "cv" and all(p in allowed for p in zip(k, k[1:], strict=False))
    assert any(mutant_pause(k) != pause_licensed(k) for k in seqs(7))
