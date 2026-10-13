"""قانونُ التمام (ADR ٥٧): التوقّعاتُ من أمثلة النصّين وقواعد التوقيع المرسى، لا من الشيفرة.

١. الحدُّ الأدنى المكتمل: كلمةٌ واحدةٌ تامّةٌ إذا وفقط إذا لم تكن لبابها حاجةٌ قبلُ أو بعدُ —
   بقائمةٍ مكتوبةٍ باليد.
٢. أمثلةٌ بأبوابها: «إنّ اللهَ غفورٌ»، «إنّ في ذلك لآيةً»، «ما قام أحدٌ إلّا زيدٌ»، «هل قام زيدٌ»،
   «إنّ زيدًا هل…».
٣. الصدارة: لا تقع وما قبلها مفتوح، ولا ترى ما قبلها.
٤. الوصل: التشغيلُ على `a ++ b` هو التشغيلُ على `b` من حالات `a`.
وكلُّ قسمٍ بطفرةٍ مرفوضةٍ باسمها.
"""

from __future__ import annotations

from collections.abc import Callable

from slge import haja as H
from slge import tamam as T

INNA: T.Tok = ("harf", "mushabbaha")
ISM: T.Tok = ("ism", "mustaqill")
FIL: T.Tok = ("fil", "mustaqill")
JARR: T.Tok = ("harf", "jarr")
HAL: T.Tok = ("harf", "istifham")
MA: T.Tok = ("harf", "nafy")
ILLA: T.Tok = ("harf", "istithna")
WA: T.Tok = ("harf", "atf")
NAAM: T.Tok = ("harf", "jawab")
HUWA: T.Tok = ("mudmar", "damir")

Run = Callable[[list[T.St], list[list[T.Tok]]], list[T.St]]


def _tamm(seq: list[T.Tok], run: Run = T.run_all) -> bool:
    return T.tamm(run([T.START], [[t] for t in seq]))


def _alive(seq: list[T.Tok], run: Run = T.run_all) -> bool:
    return bool(run([T.START], [[t] for t in seq]))


# الكلمةُ الواحدة: تامّةٌ إن لم تكن لبابها حاجةٌ «قبل» أو «بعد»
# (من جدول الحاجة المرسى، مكتوبةً باليد هنا)
ALONE_TAMM = {"mustaqill", "ghayrMusnad", "damir"}


def test_minimal_complete() -> None:
    for b in H.BAB_ALL:
        for leaf in ("harf", "mudmar", "fil", "ism"):
            assert _tamm([(leaf, b)]) == (b in ALONE_TAMM), (leaf, b)


# أمثلة: (السلسلة، تامّة؟، حيّة؟)
EXAMPLES: tuple[tuple[str, list[T.Tok], bool, bool], ...] = (
    ("إنّ اللهَ غفورٌ", [INNA, ISM, ISM], True, True),
    ("إنّ اللهَ", [INNA, ISM], False, True),
    ("إنّ في ذلك لآيةً", [INNA, JARR, ISM, ISM], True, True),
    ("ما قام أحدٌ إلّا زيدٌ", [MA, FIL, ISM, ILLA, ISM], True, True),
    ("إلّا زيدٌ (بلا مستثنًى منه)", [ILLA, ISM], False, False),
    ("هل قام زيدٌ", [HAL, FIL, ISM], True, True),
    ("إنّ زيدًا هل…", [INNA, ISM, HAL], False, False),
    ("قام زيدٌ وعمرٌو", [FIL, ISM, WA, ISM], True, True),
    ("و… (لا معطوفَ عليه)", [WA, ISM], False, False),
    ("نعم (بلا قولٍ قبله)", [NAAM], False, False),
    ("هو قائمٌ", [HUWA, ISM], True, True),
)


def _example_failures(run: Run) -> list[str]:
    return [n for n, seq, tm, alive in EXAMPLES
            if _tamm(seq, run) != tm or _alive(seq, run) != alive]


def test_examples() -> None:
    assert _example_failures(T.run_all) == []


def test_mutant_sadr_fills_rejected() -> None:
    """SADR_FILLS: ذو الصدارة يقضي ما قبله — يقبل «إنّ زيدًا هل…» ويخالف «ليس صلةً لما قبله»
    (س9213)."""

    def step_all(s: T.St, t: T.Tok) -> list[T.St]:
        r = T.finish(s[1], T.fill(s[0], t), t)
        return [] if r is None else [r]

    def run(states: list[T.St], words: list[list[T.Tok]]) -> list[T.St]:
        for w in words:
            states = list(dict.fromkeys(r for s in states for t in w for r in step_all(s, t)))
        return states

    assert _example_failures(run) == ["إنّ زيدًا هل…"]


def test_mutant_qabl_unchecked_rejected() -> None:
    """QABL_UNCHECKED: حاجةُ «قبل» لا تُفحص — يقبل «إلّا زيدٌ» و«نعم» بلا ما قبلهما."""

    def finish(seen0: tuple[str, ...], stack1: tuple[tuple[str, ...], ...],
               t: T.Tok) -> T.St | None:
        sadr = t[1] in H.SADR
        if sadr and stack1:
            return None
        seen = () if sadr else seen0
        o = T.opens(t)
        return ((o, *stack1) if o else stack1, T.add_seen(t[0], seen))

    def run(states: list[T.St], words: list[list[T.Tok]]) -> list[T.St]:
        for w in words:
            nxt = []
            for s in states:
                for t in w:
                    st1 = s[0] if t[1] in H.SADR else T.fill(s[0], t)
                    r = finish(s[1], st1, t)
                    if r is not None:
                        nxt.append(r)
            states = list(dict.fromkeys(nxt))
        return states

    assert set(_example_failures(run)) == {"إلّا زيدٌ (بلا مستثنًى منه)", "و… (لا معطوفَ عليه)",
                                           "نعم (بلا قولٍ قبله)"}


def test_sadr_needs_closed_and_forgets() -> None:
    # ما قبله مفتوح ⇒ لا خطوة
    assert T.step_all(((("ism",),), ("harf",)), HAL) == []
    # ما رُئي قبله لا أثرَ له
    assert T.step_all(((), ("fil", "ism")), HAL) == T.step_all(T.START, HAL)


def test_wasl_is_inheritance() -> None:
    a = [[INNA], [ISM]]
    b = [[ISM], [WA], [ISM]]
    assert T.run_all([T.START], a + b) == T.run_all(T.run_all([T.START], a), b)
