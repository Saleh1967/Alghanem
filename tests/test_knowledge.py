"""المعرفة: صورُ الغزالي، والقبولُ بالدليل، وسلامةُ `infer` على كلّ عالمٍ صغير."""

from __future__ import annotations

from itertools import combinations, product

import pytest

from slge.knowledge import (
    Admission,
    Degree,
    Form,
    Genus,
    Licence,
    LicenceGround,
    Literal,
    Outcome,
    Standing,
    WorldKnowledgeError,
    WorldRule,
    infer,
    productive,
)
from world_fixture import ADMITTED, PROPOSED_RULES, ev, rule

_CONCEPTS = ("أ", "ب", "ج")


def test_ghazali_table() -> None:
    assert {f for f in Form if productive(Degree.اخص, f)} == {Form.عين_المقدم, Form.نقيض_التالي}
    assert all(productive(Degree.مساو, f) for f in Form)


def test_human_animal() -> None:
    rules = ADMITTED
    assert infer(Literal("إنسان", True), "حيوان", rules).conclusion == Literal("حيوان", True)
    assert infer(Literal("حيوان", False), "إنسان", rules).conclusion == Literal("إنسان", False)
    assert infer(Literal("إنسان", False), "حيوان", rules).outcome is Outcome.غير_منتج
    assert infer(Literal("حيوان", True), "إنسان", rules).outcome is Outcome.غير_منتج


def test_candidates_never_produce() -> None:
    rules = ADMITTED + PROPOSED_RULES
    v = infer(Literal("ضرب", True), "محرم", rules)
    assert v.outcome is Outcome.ناقص and v.conclusion is None
    assert v.would_conclude == Literal("محرم", True)
    only = tuple(r for r in rules if r.admission is Admission.مرشح)
    for c in ("أذى", "ضرب"):
        for aff in (True, False):
            assert infer(Literal(c, aff), "محرم", only).outcome is not Outcome.منتج


def test_admission_requires_the_right_genus() -> None:
    with pytest.raises(WorldKnowledgeError):
        rule("x", "أ", "ب", Standing.عادي, ev("معجم", Genus.شاهد_معجمي, "م"), ("مانع",))
    with pytest.raises(WorldKnowledgeError):
        rule("x", "أ", "ب", Standing.عادي, None)  # عاديٌّ بلا مانع
    for r in PROPOSED_RULES:
        with pytest.raises(WorldKnowledgeError):
            r.admit(ev("رأي", Genus.فرضية, "مولد"))


def test_blocker_stops_a_habitual_rule() -> None:
    sun = rule("شمس-نهار", "شمس", "نهار", Standing.عادي, ev("م", Genus.مشاهدة, "محك"),
               ("كسوف",), Degree.مساو)
    v = infer(Literal("شمس", True), "نهار", (sun,), present_blockers=frozenset({"كسوف"}))
    assert v.outcome is Outcome.لا_طريق and v.blocked_by == ("كسوف",)


def test_licence_lifts_and_hypothesis_does_not() -> None:
    zakat = next(r for r in ADMITTED if r.rule_id == "سائمة-زكاة")
    hyp = Licence(zakat.rule_id, LicenceGround.وصف_مفهم, ev("ر", Genus.فرضية, "مولد"))
    assert infer(Literal("سائمة", False), "زكاة", (zakat,), (hyp,)).outcome is Outcome.ناقص
    real = Licence(zakat.rule_id, LicenceGround.وصف_مفهم, ev("ن", Genus.خبر_مقبول, "نص"))
    v = infer(Literal("سائمة", False), "زكاة", (zakat,), (real,))
    assert v.conclusion == Literal("زكاة", False) and v.defeasible
    assert v.path[0].licence is LicenceGround.وصف_مفهم


def _all_rules() -> list[WorldRule]:
    out = []
    for a, b in product(_CONCEPTS, repeat=2):
        if a != b:
            for d in Degree:
                out.append(rule(f"{a}{b}{d.value}", a, b, Standing.تعريفي,
                                ev("ت", Genus.تعريف_مشترط, "تعريف"), (), d))
    return out


def _holds(r: WorldRule, m: dict[str, bool]) -> bool:
    a, b = m[r.antecedent], m[r.consequent]
    return (not a or b) if r.degree is Degree.اخص else a == b


def test_every_produced_step_is_productive() -> None:
    """السلامة استقصاءً: كلُّ رصيدٍ من ثلاث قواعد فأقلّ على ثلاثة مفاهيم، وكلُّ معطًى وكلُّ هدف.

    إذا أنتج `infer` فالنتيجةُ صادقةٌ في كلّ نموذجٍ ثنائيٍّ للمفاهيم الثلاثة يصدق فيه الرصيدُ
    والمعطى — وهذا معنى «منتج» نفسُه الذي برهنه Lean للخطوة الواحدة، ممدودًا إلى الطريق.
    """

    rules = _all_rules()
    models = [dict(zip(_CONCEPTS, bits, strict=True))
              for bits in product((False, True), repeat=3)]
    checked = 0
    for k in range(4):
        for base in combinations(rules, k):
            for c, aff, target in product(_CONCEPTS, (True, False), _CONCEPTS):
                v = infer(Literal(c, aff), target, base)
                if v.outcome is not Outcome.منتج:
                    continue
                assert v.conclusion is not None
                for step in v.path:
                    r = next(x for x in base if x.rule_id == step.rule_id)
                    assert productive(r.degree, step.form)
                for m in models:
                    if m[c] == aff and all(_holds(r, m) for r in base):
                        assert m[v.conclusion.concept] == v.conclusion.affirmed
                checked += 1
    assert checked > 1000
