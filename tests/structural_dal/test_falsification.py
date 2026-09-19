"""`G0.SDAL-0.FALSIFICATION`: مصفوفةُ تكذيبٍ على جبر `zero-one`.

تُقاس هنا أربعةُ محاور: إعادةُ البناء مع حفظ الهويّة، وتبديلُ رمز خانةٍ،
وإسقاطُ خانة، وتبديلُ الشاهد بين مدخلين اثنين؛ ثمّ يُقاس منعُ رفع
`ShapePartitionHypothesis` إلى جذرٍ أو وزنٍ أو مدلولٍ أو إفادة.

ولا يقيس هذا الملفُّ لسانًا: الرموزُ مُصطنَعةٌ، والحدُّ خانتان.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from alghanem.structural_bridge import (
    BitPosition,
    bridge_two_bits,
    compare_with_the_path,
)
from alghanem.structural_dal import (
    FORBIDDEN_NAME_FRAGMENTS,
    SHAPE_PARTITION_HYPOTHESIS_IS_NOT_A_ROOT_CANDIDATE,
    SHAPE_PARTITION_HYPOTHESIS_IS_NOT_A_WEIGHT_CANDIDATE,
    ZERO_ONE_BOUND,
    IdentityTransitionMode,
    OutputContractComponent,
    PromotionStanding,
    ShapePartitionHypothesis,
    SlotRole,
    StructuralDalError,
    StructuralDecomposition,
    ascend_one_slot,
    decompose,
    enumerate_shape_partitions,
    origin_whole,
    prove_zero_one_algebra,
)
from alghanem.structural_dal.laws import (
    SHAPE_PARTITION_HYPOTHESIS_IS_NOT_A_SIGNIFIED_CANDIDATE,
    SHAPE_PARTITION_HYPOTHESIS_IS_NOT_AN_UTTERANCE_BENEFIT_CANDIDATE,
)
from alghanem.structural_dal.slots import StructuralWhole


def _two_slot_whole(
    subject: str, tokens: tuple[str, ...] = ("SlotA", "SlotB")
) -> StructuralWhole:
    """كلٌّ بخانتين برموزٍ مُصطنَعةٍ ومِرساةٍ خاصّةٍ بهذا الموضوع."""

    return origin_whole(
        whole_id=f"whole.{subject}",
        anchor_id=f"anchor.{subject}",
        carrier_id=f"carrier.{subject}",
        tokens=tokens,
    )


def _decompositions(whole: StructuralWhole) -> tuple[StructuralDecomposition, ...]:
    """كلُّ تفكيكات الكلّ على كلِّ فرضيّاته."""

    return tuple(
        decompose(whole, hypothesis)
        for hypothesis in enumerate_shape_partitions(whole).hypotheses
    )


# ————— إعادةُ البناء وحفظُ الهويّة —————


def test_every_decomposition_rebuilds_its_whole_token_for_token() -> None:
    """كلُّ تفكيكٍ يُعيد بناءَ رموز كلِّه بترتيبها، فلا بناءَ ناقصٌ يُقبَل."""

    whole = _two_slot_whole("rebuild")
    decompositions = _decompositions(whole)

    assert decompositions
    for decomposition in decompositions:
        assert decomposition.reconstruction == whole.tokens
        assert decomposition.reconstructs_whole
        assert decomposition.covers_every_slot_once


def test_rebuilding_preserves_lineage_and_keeps_part_identity_apart() -> None:
    """إعادةُ البناء تحفظ نسبَ الأجزاء ولا تُذيب هويّةَ الجزء في نسبه."""

    whole = _two_slot_whole("identity")

    for decomposition in _decompositions(whole):
        assert decomposition.preserves_parent_anchor
        assert decomposition.parts_carry_distinct_identity
        for part in decomposition.parts:
            assert part.parent_anchor_id == whole.anchor_id
            assert part.part_anchor_id != whole.anchor_id
        assert (
            OutputContractComponent.PART_WHOLE_IDENTITY
            in decomposition.satisfied_contract_components
        )


def test_rescaling_preserves_the_instance_identity_of_its_input() -> None:
    """الصعودُ خانةً واحدةً يُبقي المِرساةَ عينَها ويُراكِم الأثرَ ولا يُعيد بناءه."""

    before = origin_whole(
        whole_id="whole.rescale",
        anchor_id="anchor.rescale",
        carrier_id="carrier.rescale",
        tokens=("SlotA",),
    )
    ascent = ascend_one_slot(
        before, "SlotB", mode=IdentityTransitionMode.SAME_ENTITY_RESCALING
    )

    assert ascent.preserves_instance_identity
    assert ascent.after.anchor_id == before.anchor_id
    assert ascent.after.tokens == (*before.tokens, "SlotB")
    assert ascent.trace_is_cumulative


# ————— تبديلُ البتّ وإسقاطُه —————


def test_flipping_one_slot_token_changes_the_measured_content_identity() -> None:
    """تبديلُ رمزِ خانةٍ واحدةٍ فرقٌ قادح: البصمةُ تتغيّر وإعادةُ البناء تتبعه."""

    original = _two_slot_whole("flip", ("SlotA", "SlotB"))
    flipped = _two_slot_whole("flip", ("SlotA", "SlotC"))

    assert original.slot_count == flipped.slot_count
    assert original.anchor_id == flipped.anchor_id
    assert original.content_id != flipped.content_id

    hypothesis = ShapePartitionHypothesis(
        hypothesis_id="shape.flip", roles=(SlotRole.CORE, SlotRole.TRANSFORM)
    )
    before = decompose(original, hypothesis)
    after = decompose(flipped, hypothesis)

    assert before.reconstructs_whole and after.reconstructs_whole
    assert before.reconstruction != after.reconstruction
    assert before.as_canonical_content() != after.as_canonical_content()


def test_a_flipped_token_does_not_lift_the_blocking_residual() -> None:
    """التبديلُ لا يرفع الحاجب: الموقفُ محجوبٌ قبله وبعده بسببٍ مُسمًّى واحد."""

    hypothesis = ShapePartitionHypothesis(
        hypothesis_id="shape.flip.blocked", roles=(SlotRole.CORE, SlotRole.TRANSFORM)
    )
    standings = {
        decompose(_two_slot_whole("blocked", tokens), hypothesis).promotion_standing
        for tokens in (("SlotA", "SlotB"), ("SlotA", "SlotC"))
    }

    assert standings == {PromotionStanding.PROMOTION_BLOCKED}


def test_dropping_a_slot_from_the_partition_is_refused_not_absorbed() -> None:
    """إسقاطُ خانةٍ من التقسيم يُرفَض باسمه، ولا يُبتلَع في تفكيكٍ يبدو تامًّا."""

    whole = _two_slot_whole("drop")
    hypothesis = ShapePartitionHypothesis(
        hypothesis_id="shape.drop", roles=(SlotRole.CORE, SlotRole.TRANSFORM)
    )
    complete = decompose(whole, hypothesis)
    truncated = tuple(
        part
        if part.role is not SlotRole.TRANSFORM
        else type(part)(
            part_id=part.part_id,
            part_anchor_id=part.part_anchor_id,
            parent_anchor_id=part.parent_anchor_id,
            role=part.role,
            slot_map=(),
        )
        for part in complete.parts
    )

    with pytest.raises(StructuralDalError):
        StructuralDecomposition(
            decomposition_id="decomposition.drop",
            whole=whole,
            hypothesis=hypothesis,
            parts=truncated,
        )


def test_dropping_a_slot_from_the_whole_changes_its_measured_scale() -> None:
    """إسقاطُ الخانة من الكلّ يُنزِل مقياسَه ويُغيّر بصمتَه، ولا يمرُّ صامتًا."""

    two = _two_slot_whole("scale", ("SlotA", "SlotB"))
    one = _two_slot_whole("scale", ("SlotA",))

    assert two.slot_count == 2
    assert one.slot_count == 1
    assert two.content_id != one.content_id
    assert (
        enumerate_shape_partitions(two).count != enumerate_shape_partitions(one).count
    )


def test_a_hypothesis_that_does_not_cover_every_slot_is_refused() -> None:
    """فرضيّةٌ تُسنِد أدوارًا لأقلَّ من خانات كلِّها مردودةٌ، ولا تُكمَّل ضمنًا."""

    whole = _two_slot_whole("coverage")
    short = ShapePartitionHypothesis(
        hypothesis_id="shape.short", roles=(SlotRole.CORE,)
    )

    with pytest.raises(StructuralDalError):
        decompose(whole, short)


# ————— تبديلُ الشاهد بين مدخلين —————


def test_a_decomposition_cannot_carry_the_parts_of_another_input() -> None:
    """شاهدُ مدخلٍ لا يُحتَجُّ به على آخر: أجزاءُ الأوّل تحمل مِرساتَه فتُرَدّ."""

    first = _two_slot_whole("witness.first")
    second = _two_slot_whole("witness.second")
    hypothesis = ShapePartitionHypothesis(
        hypothesis_id="shape.witness", roles=(SlotRole.CORE, SlotRole.TRANSFORM)
    )
    borrowed = decompose(first, hypothesis).parts

    assert first.anchor_id != second.anchor_id
    with pytest.raises(StructuralDalError):
        StructuralDecomposition(
            decomposition_id="decomposition.swapped",
            whole=second,
            hypothesis=hypothesis,
            parts=borrowed,
        )


def test_two_inputs_do_not_share_one_measured_report() -> None:
    """تشغيلان على رمزين مختلفين تقريران مختلفان، فلا يُنسَب أثرُ أحدهما للآخر."""

    left = prove_zero_one_algebra(base_token="SlotA", added_token="SlotB")
    right = prove_zero_one_algebra(base_token="SlotA", added_token="SlotC")

    assert left.ascent.after.content_id != right.ascent.after.content_id
    assert left.weaker.output != right.weaker.output
    assert left.algebra_holds and right.algebra_holds


def test_the_witness_of_a_swapped_token_does_not_reconstruct_the_other_whole() -> None:
    """بناءُ شاهدِ مدخلٍ لا يُطابق رموزَ مدخلٍ آخر، وهذا هو الفرقُ القادح."""

    first = _two_slot_whole("swap.first", ("SlotA", "SlotB"))
    second = _two_slot_whole("swap.second", ("SlotA", "SlotC"))
    hypothesis = ShapePartitionHypothesis(
        hypothesis_id="shape.swap", roles=(SlotRole.CORE, SlotRole.TRANSFORM)
    )

    assert decompose(first, hypothesis).reconstruction != second.tokens
    assert decompose(second, hypothesis).reconstruction != first.tokens


# ————— منعُ الرفع إلى جذرٍ أو وزنٍ أو مدلولٍ أو إفادة —————


def test_a_hypothesis_names_the_four_genera_it_is_not() -> None:
    """الفرضيّةُ تُسمّي الأجناسَ الأربعةَ التي لا تُرفَع إليها، مفردةً ومجموعة."""

    whole = _two_slot_whole("refusal")
    hypotheses = enumerate_shape_partitions(whole)
    refusals = (
        SHAPE_PARTITION_HYPOTHESIS_IS_NOT_A_ROOT_CANDIDATE,
        SHAPE_PARTITION_HYPOTHESIS_IS_NOT_A_WEIGHT_CANDIDATE,
        SHAPE_PARTITION_HYPOTHESIS_IS_NOT_A_SIGNIFIED_CANDIDATE,
        SHAPE_PARTITION_HYPOTHESIS_IS_NOT_AN_UTTERANCE_BENEFIT_CANDIDATE,
    )

    assert hypotheses.what_it_is_not == refusals
    for hypothesis in hypotheses.hypotheses:
        assert hypothesis.what_it_is_not == refusals


def test_the_hypothesis_set_never_yields_a_winner_to_promote() -> None:
    """لا فائزَ يُرفَع: المجموعةُ تُعرَض كاملةً بلا ترجيحٍ مهما كثرت فرضيّاتُها."""

    hypotheses = enumerate_shape_partitions(_two_slot_whole("winner"))

    assert hypotheses.count > 1
    assert hypotheses.forced_winner is None
    assert hypotheses.refusal.strip()


def test_no_decomposition_at_one_is_ever_permitted_promotion() -> None:
    """كلُّ تفكيكٍ عند الواحد محجوبُ الترقية، فلا مخرجَ مُرقًّى في هذا الطور."""

    report = prove_zero_one_algebra()

    assert report.blocked_attempts
    assert report.permitted_attempts == ()
    for attempt in report.promotion_attempts:
        assert attempt.standing is PromotionStanding.PROMOTION_BLOCKED
        assert attempt.refusal.strip()
        assert not hasattr(attempt, "promoted")


def test_the_report_carries_no_certificate_and_no_promoted_output() -> None:
    """التقريرُ لا يحمل شهادةً ولا ناتجًا مُرقًّى، وكلُّ ولادةِ فرعٍ مؤجَّلة."""

    report = prove_zero_one_algebra()

    assert report.deferred_births
    for birth in report.deferred_births:
        assert birth.refusal.strip()
        assert not hasattr(birth, "certificate")
    for field_name in ("certificate", "verdict", "promoted_whole"):
        assert not hasattr(report, field_name)


def test_the_layer_names_no_root_weight_signified_or_benefit_in_its_vocabulary() -> (
    None
):
    """مفرداتُ الطبقة خاليةٌ من الجذر والوزن والمدلول والإفادة، فحصًا لا تصريحًا."""

    report = prove_zero_one_algebra()

    assert report.vocabulary.is_clean
    assert report.vocabulary.violations == ()
    assert report.isolation.is_isolated


# ————— حدُّ البرهان عند خانتين —————


def test_the_proof_bound_is_two_slots_and_is_refused_above_it() -> None:
    """حدُّ البرهان خانتان: ما فوقَهما مردودٌ باسمه لا مُقاسٌ بامتدادٍ ضمنيّ."""

    assert ZERO_ONE_BOUND == 2

    three = origin_whole(
        whole_id="whole.bound",
        anchor_id="anchor.bound",
        carrier_id="carrier.bound",
        tokens=("SlotA", "SlotB", "SlotC"),
    )
    with pytest.raises(StructuralDalError):
        enumerate_shape_partitions(three)
    with pytest.raises(StructuralDalError):
        ascend_one_slot(
            _two_slot_whole("bound"),
            "SlotC",
            mode=IdentityTransitionMode.SAME_ENTITY_RESCALING,
        )


def test_the_hypothesis_count_at_the_bound_is_derived_not_frozen() -> None:
    """عددُ الفرضيّات عند الحدّ مُشتَقٌّ من الأدوار والخانات، لا رقمٌ مكتوبٌ سلفًا."""

    roles = len(SlotRole)
    one = enumerate_shape_partitions(
        origin_whole(
            whole_id="whole.count",
            anchor_id="anchor.count",
            carrier_id="carrier.count",
            tokens=("SlotA",),
        )
    )
    two = enumerate_shape_partitions(_two_slot_whole("count"))

    assert one.count == roles
    assert two.count == roles**2


# ————— المسارُ العربيُّ لا يستعمل هذا الشاهد —————


def _imported_modules(path: Path) -> set[str]:
    """وحداتُ `alghanem` المُصرَّحُ استيرادُها في ملفٍّ واحد."""

    tree = ast.parse(path.read_text(encoding="utf-8"))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
        elif isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
    return modules


def test_no_arabic_module_reads_the_zero_one_structural_algebra() -> None:
    """المسارُ العربيُّ لا يستورد هذا الجبرَ أصلًا: لا في انتقالٍ ولا في تدقيق."""

    arabic = Path("src/alghanem/arabic").resolve()
    readers = sorted(
        path.name
        for path in arabic.rglob("*.py")
        if any(
            module.startswith("alghanem.structural_dal")
            for module in _imported_modules(path)
        )
    )

    assert readers == []


def test_only_the_named_bridge_joins_this_algebra_to_a_benefit() -> None:
    """جسرٌ واحدٌ مُسمًّى يجمع الجبرَ بالإفادة، وهو نفسُه يُثبِت أنّه لا يمسُّها."""

    source = Path("src/alghanem").resolve()
    algebra = source / "structural_dal"
    joiners = sorted(
        str(path.relative_to(source))
        for path in source.rglob("*.py")
        if algebra not in path.parents
        and "structural_dal" in (text := path.read_text(encoding="utf-8")).lower()
        and "ifada" in text.lower()
    )

    assert joiners == ["structural_bridge/byte_slot_bridge.py"]


def test_the_named_bridge_derives_no_benefit_of_its_own() -> None:
    """الجسرُ المُسمّى لا يشتقُّ إفادةً: يُساق المصدرُ قبله وبعده فلا يتغيّر شيء."""

    bridge = bridge_two_bits(
        "اللَّهُ نُورٌ".encode(),
        BitPosition(byte_index=0, bit_index=0),
        BitPosition(byte_index=1, bit_index=7),
    )
    comparison = compare_with_the_path(bridge)

    assert comparison.the_whole_run_is_unchanged
    assert not hasattr(bridge, "ifada")
    assert SHAPE_PARTITION_HYPOTHESIS_IS_NOT_AN_UTTERANCE_BENEFIT_CANDIDATE in (
        bridge.what_it_is_not
    )


def test_inside_the_algebra_a_benefit_is_named_only_to_be_refused() -> None:
    """داخل الجبر لا تُذكَر الإفادةُ إلّا في قانون نفيٍ أو في قائمة منعٍ مفحوصة."""

    algebra = Path("src/alghanem/structural_dal").resolve()
    carriers = sorted(
        path.name
        for path in algebra.rglob("*.py")
        if "ifada" in path.read_text(encoding="utf-8").lower()
    )

    assert carriers == ["audit.py", "laws.py"]
    assert "!= IfadaCandidate" in (
        SHAPE_PARTITION_HYPOTHESIS_IS_NOT_AN_UTTERANCE_BENEFIT_CANDIDATE
    )
    assert "ifada" in FORBIDDEN_NAME_FRAGMENTS
