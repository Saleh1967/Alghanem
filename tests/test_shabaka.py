"""شبكةُ الأوزان: الجبرُ يحفظ الأصل، الحوافُّ محسوبة، والترتيبُ الكلاسيكيُّ مقيسٌ لا مقرَّر."""

from __future__ import annotations

from itertools import permutations

import pytest

from slge.cells import STATES, licensed
from slge.shabaka import (
    CLASSICAL,
    COMPUTED,
    ROOT,
    Edit,
    agreement,
    apply,
    diff,
    distance,
    edge_costs,
    minimal_tree,
    reachable,
)
from slge.wazn import AWZAN, FAL, Sym, fill, mizan, parse, root_of

BY = {w.name: w.template for w in AWZAN}


def test_diff_then_apply_is_identity_on_every_pair() -> None:
    for a, b in permutations(AWZAN, 2):
        edits = diff(a.template, b.template)
        assert apply(a.template, edits) == b.template, (a.name, b.name)
        assert distance(a.template, b.template) == distance(b.template, a.template)


def test_every_edit_keeps_the_root_recoverable() -> None:
    """`wf_run`: بعد أيّ تتابعٍ من العمليّات يبقى الأصلُ مستردًّا."""

    for a, b in permutations(AWZAN[:40], 2):
        t = a.template
        for e in diff(t, b.template):
            t = apply(t, (e,))
            assert root_of(t, fill(t, "كتب")) == ("ك", "ت", "ب"), (a.name, b.name, e)


def test_deleting_a_lone_root_slot_is_refused_by_name() -> None:
    t = parse("فَعَلَ")
    with pytest.raises(ValueError, match="CANNOT_DELETE_ROOT_SLOT"):
        apply(t, (Edit("del", 1),))
    geminate = parse("فَعَّلَ")
    assert len(apply(geminate, (Edit("del", 1),))) == 3  # فكُّ التضعيف جائز


def test_classical_edges_are_machine_checked_and_rooted() -> None:
    assert len(CLASSICAL) == len(AWZAN) - 1 and ROOT not in CLASSICAL
    for child, parent in CLASSICAL.items():
        assert apply(BY[parent], diff(BY[parent], BY[child])) == BY[child]
        assert licensed(mizan(BY[child]))
    assert reachable(CLASSICAL) and reachable(COMPUTED)
    assert not reachable({**CLASSICAL, "فَعَلَ": "فَاعِلٌ"})  # دورٌ: فَعَلَ ↔ فَاعِلٌ


def test_computed_tree_is_minimal_and_classical_is_not() -> None:
    """مقيس: شجرةُ البصريّين تكلّف 369 عمليّةً، والأقلُّ الممكن 166؛ ويتّفقان في 22 أبًا من 124
    (كانت 361/165/21 من 120 قبل قوالب الاسم الأربعة: أ2)."""

    cost = edge_costs()
    classical = sum(cost[(c, p)] for c, p in CLASSICAL.items())
    computed = sum(cost[(c, p)] for c, p in COMPUTED.items())
    assert (classical, computed) == (369, 166)
    assert computed <= classical
    assert agreement()[:2] == (22, 124)
    assert minimal_tree() == COMPUTED


def test_prim_is_minimal_against_a_mutant_tree() -> None:
    """طفرة: أيُّ تبديلِ أبٍ واحدٍ في الشجرة المحسوبة لا يُنقص كلفتَها."""

    cost = edge_costs()
    base = sum(cost[(c, p)] for c, p in COMPUTED.items())
    for child in list(COMPUTED)[:25]:
        for other in list(COMPUTED)[:25]:
            if other == child or other == COMPUTED[child]:
                continue
            mutant = {**COMPUTED, child: other}
            if reachable(mutant):
                assert sum(cost[(c, p)] for c, p in mutant.items()) >= base


def test_edit_states_only_live_in_the_four_states() -> None:
    assert all(e.state in STATES for e in diff(parse("فَعْلُ"), parse("فَعَلَ")) if e.op == "set")
    assert FAL == ("ف", "ع", "ل") and isinstance(Sym(0, None, STATES[0]), Sym)
