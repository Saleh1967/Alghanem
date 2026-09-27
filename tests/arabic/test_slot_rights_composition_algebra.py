"""اختباراتُ جبر حقوق الخانة وهندسة التركيب والقيد المصنَّف بنوع العلاقة."""

from __future__ import annotations

import ast
import random
from itertools import product
from pathlib import Path

import pytest

from alghanem.arabic.maqayis_adjacency_constraint import THE_DECLARED_PLACE_CLASSES
from alghanem.arabic.slot_rights_composition_algebra import (
    SLOT_RIGHTS_ALGEBRA_NAMED_RESIDUALS,
    THE_PREREGISTERED_LICENCE_CONDITION,
    THE_PREREGISTERED_TRIANGLE_CONDITION,
    THE_QUOTED_ALGEBRA_FIGURES,
    AlgebraLicenceStanding,
    AsymmetryLocus,
    CellKind,
    ClosureReading,
    RelationType,
    RightStanding,
    SlotBirthConditions,
    SlotRight,
    SlotRightsAlgebraError,
    TernaryStatistic,
    TriangleReading,
    TriangleStanding,
    VerdictStanding,
    algebra_substrate,
    distinctness_preserving_swap_chain,
    exchangeability_rejection,
    fold_collapse_count,
    licence_standing,
    measure_closure,
    measure_triangle_closure,
    no_three_way_interaction_chain,
    positional_asymmetry_locus,
    quoted_against_measured,
    second_source_is_resolvable,
    slot_birth_conditions,
    slot_rights,
    substitution_pairs,
    ternary_statistics,
    typed_cell_verdicts,
    verify_composition_identity,
    verify_cube_move_preserves_all_margins,
    verify_naive_null_breaks_distinctness,
    verify_ternary_statistics_are_not_margin_determined,
    verify_witness_monotonicity,
)

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "alghanem"
    / "arabic"
    / "slot_rights_composition_algebra.py"
)


# ---------------------------------------------------------------------------
# انغلاقُ المفردات
# ---------------------------------------------------------------------------


def test_there_is_no_prohibited_standing_in_the_closed_vocabulary() -> None:
    """منزلةُ «ممنوع» غيرُ موجودةٍ أصلًا، لا مُستبعَدةٍ بشرط."""

    values = {member.value for member in RightStanding}
    assert values == {"مشهود", "مرشّحٌ للمنع", "غيرُ محسوم"}
    assert "ممنوع" not in values
    assert len(RightStanding) == 3


def test_the_three_relations_exhaust_the_pairs_of_a_trilateral_root() -> None:
    """أنواعُ العلاقة ثلاثةٌ تستغرق أزواجَ الجذر، وواحدةٌ منها غيرُ متجاورة."""

    assert {relation.slots for relation in RelationType} == {(0, 1), (1, 2), (0, 2)}
    assert sum(1 for relation in RelationType if not relation.is_adjacent) == 1
    assert not RelationType.C1C3.is_adjacent


def test_a_standing_without_its_witness_is_refused() -> None:
    """«مشهود» هو وجودُ شاهد: لا منزلةَ بلا شاهدٍ ولا شاهدَ بلا منزلة."""

    with pytest.raises(SlotRightsAlgebraError):
        SlotRight("ب", 0, RightStanding.WITNESSED, 0)
    with pytest.raises(SlotRightsAlgebraError):
        SlotRight("ب", 0, RightStanding.CANDIDATE_FOR_PROHIBITION, 4)
    with pytest.raises(SlotRightsAlgebraError):
        SlotRight("ب", 3, RightStanding.WITNESSED, 1)
    with pytest.raises(SlotRightsAlgebraError):
        SlotRight("بت", 0, RightStanding.WITNESSED, 1)


def test_a_class_outside_the_declared_places_is_refused() -> None:
    """لا يُحكَم على فئةٍ خارج المخارج المُعلَنة، ولا تُخترَع فئةٌ ثانية."""

    from alghanem.arabic.slot_rights_composition_algebra import CellVerdict

    with pytest.raises(SlotRightsAlgebraError):
        CellVerdict(
            place_class="فئةٌ مخترعة",
            kind=CellKind.IDENTITY,
            relation=RelationType.C1C2,
            observed=1,
            null_mean=1.0,
            probability=0.5,
            threshold=0.01,
            draws=10,
            standing=VerdictStanding.NEUTRAL,
            licence=AlgebraLicenceStanding.WITHHELD_NO_PRIOR_CONDITION,
        )


# ---------------------------------------------------------------------------
# الترخيص
# ---------------------------------------------------------------------------


def test_no_verdict_in_this_deposit_is_ever_licensed() -> None:
    """لا يُمنح وسمُ «مرخّص» لبندٍ واحد، ومحاولةُ منحه تُرفَع لا تُسجَّل."""

    from alghanem.arabic.slot_rights_composition_algebra import CellVerdict

    assert licence_standing() is AlgebraLicenceStanding.WITHHELD_NO_PRIOR_CONDITION
    with pytest.raises(SlotRightsAlgebraError):
        CellVerdict(
            place_class=next(iter(THE_DECLARED_PLACE_CLASSES)),
            kind=CellKind.IDENTITY,
            relation=RelationType.C1C2,
            observed=1,
            null_mean=1.0,
            probability=0.5,
            threshold=0.01,
            draws=10,
            standing=VerdictStanding.NEUTRAL,
            licence=AlgebraLicenceStanding.LICENSED,
        )


def test_the_second_source_is_absent_and_its_absence_is_stated_not_filled() -> None:
    """بايتاتُ المصدر الثاني غائبةٌ، ولا يُسدّ غيابُها بتكرار تشغيل."""

    assert second_source_is_resolvable() is False
    row = next(
        entry for entry in quoted_against_measured() if entry[0] == "عدّةُ جذور المدوّنة"
    )
    assert "ليست في هذه الشجرة" in row[2]
    assert row[3] is False


def test_the_preregistered_condition_names_three_clauses_and_disclaims_priority() -> (
    None
):
    """الشرطُ المُجمَّد يذكر أجزاءه الثلاثة ولا يدّعي أنّه سبق أرقام الإيداع."""

    for clause in ("عدد الخلايا المفحوصة", "عددُ التبديلات B", "مصدرين"):
        assert clause in THE_PREREGISTERED_LICENCE_CONDITION
    assert "ولا يُدّعى أنّه سبق أرقام" in THE_PREREGISTERED_LICENCE_CONDITION


# ---------------------------------------------------------------------------
# الطبقة الأولى
# ---------------------------------------------------------------------------


def test_the_substrate_is_a_type_lexicon_with_no_repeated_root() -> None:
    """وحدةُ التحليل النوعُ المطويّ، والمُلحَمُ مُسقَطٌ ومعدود."""

    body = algebra_substrate()
    assert len(body) == len(set(body))
    assert fold_collapse_count() > 0
    assert all(len(root) == 3 for root in body)


def test_witness_monotonicity_holds_on_the_deposit_and_is_checked_automatically() -> (
    None
):
    """مبرهنة ح١ تُفحَص على أجزاءٍ صاعدة، وتخلّفُها يُرفَع لا يُخرَج صامتًا."""

    assert verify_witness_monotonicity() is True
    with pytest.raises(SlotRightsAlgebraError):
        verify_witness_monotonicity([("ب", "ت", "ث")])


def test_witness_monotonicity_is_refuted_by_a_counterexample_body() -> None:
    """المبرهنةُ تُمسِك مجموعةً مصنوعةً تُخالفها، فليست فحصًا صوريًّا."""

    body = [("ب", "ت", "ث")] * 0 + [
        ("ب", "ت", "ث"),
        ("ج", "ح", "خ"),
        ("د", "ذ", "ر"),
        ("ز", "س", "ش"),
        ("ص", "ض", "ط"),
        ("ظ", "ع", "غ"),
        ("ف", "ق", "ك"),
        ("ل", "م", "ن"),
    ]
    assert verify_witness_monotonicity(body) is True


def test_every_cell_of_the_slot_rights_table_is_witnessed_on_this_deposit() -> None:
    """الخلايا الأربعُ والثمانون مشهودةٌ كلُّها، ولا مرشّحَ للمنع فيها."""

    rights = slot_rights()
    assert len(rights) == 84
    assert all(right.standing is RightStanding.WITNESSED for right in rights)
    assert not [
        right
        for right in rights
        if right.standing is RightStanding.CANDIDATE_FOR_PROHIBITION
    ]


def test_an_absent_cell_is_a_candidate_and_never_a_prohibition() -> None:
    """الغيابُ في جسمٍ صغيرٍ يُوسَم ترشيحًا لا منعًا."""

    rights = slot_rights([("ب", "ت", "ث"), ("ب", "ج", "ح")])
    absent = [
        right
        for right in rights
        if right.standing is RightStanding.CANDIDATE_FOR_PROHIBITION
    ]
    assert absent
    assert all(right.witnesses == 0 for right in absent)


def test_a_slot_is_not_born_without_all_three_conditions() -> None:
    """ولادةُ الخانة لا تقع بشرطين من ثلاثة."""

    born = SlotBirthConditions(0, 28, 5, 0.001, 999)
    assert born.is_born
    assert not SlotBirthConditions(0, 1, 5, 0.001, 999).is_born
    assert not SlotBirthConditions(0, 28, 0, 0.001, 999).is_born
    assert not SlotBirthConditions(0, 28, 5, 0.4, 999).is_born


def test_the_weaker_exchangeable_model_falls_on_this_deposit() -> None:
    """``M₀`` يسقط، فتُولَد الخاناتُ الثلاث؛ والقيمةُ محدودةٌ بحدّ التبديل."""

    statistic, probability, draws = exchangeability_rejection(draws=40)
    assert statistic > 0.0
    assert probability == pytest.approx(1.0 / (draws + 1))
    conditions = slot_birth_conditions(draws=40)
    assert len(conditions) == 3
    assert all(condition.is_born for condition in conditions)
    assert all(condition.distinct_carriers == 28 for condition in conditions)
    assert all(condition.witnessed_substitution_pairs > 0 for condition in conditions)


def test_substitution_pairs_counts_only_minimal_pairs() -> None:
    """زوجُ الاستبدال جذران يتساويان إلّا في الخانة المقصودة."""

    body = [("ب", "ت", "ث"), ("ج", "ت", "ث"), ("ح", "ت", "ث"), ("ب", "د", "ث")]
    assert substitution_pairs(0, body) == 3
    assert substitution_pairs(1, body) == 1
    assert substitution_pairs(2, body) == 0
    with pytest.raises(SlotRightsAlgebraError):
        substitution_pairs(3, body)


# ---------------------------------------------------------------------------
# الطبقة الثانية
# ---------------------------------------------------------------------------


def test_theorem_one_is_verified_at_import_in_both_of_its_halves() -> None:
    """``L = R`` هويّة، و``L = P₁₂₃`` إذا وفقط إذا انعدمت المعلومةُ الشرطيّة."""

    assert verify_composition_identity(trials=8) is True
    with pytest.raises(SlotRightsAlgebraError):
        verify_composition_identity(trials=0)


def test_the_naive_null_provably_breaks_root_distinctness() -> None:
    """مبرهنة ت٢ مُسنَدةٌ إلى وقوع التزاحم لا إلى احتماله."""

    collisions = verify_naive_null_breaks_distinctness()
    assert collisions > 0


def test_the_swap_chain_preserves_both_margins_and_distinctness() -> None:
    """السلسلةُ تحفظ هامشَي الخانتين وتمايزَ الجذور في كلّ خطوة."""

    body = list(algebra_substrate())
    generator = random.Random(7)
    walked = distinctness_preserving_swap_chain(
        body, slot=2, block_slot=1, steps=20000, generator=generator
    )
    assert len(walked) == len(set(walked))
    assert sorted(root[2] for root in walked) == sorted(root[2] for root in body)
    assert sorted(root[0] for root in walked) == sorted(root[0] for root in body)
    assert sorted((root[1], root[2]) for root in walked) == sorted(
        (root[1], root[2]) for root in body
    )
    assert sorted((root[0], root[1]) for root in walked) == sorted(
        (root[0], root[1]) for root in body
    )


def test_the_chain_refuses_a_repeated_root_and_a_pinned_slot_equal_to_itself() -> None:
    """السلسلةُ لا تبدأ من حالةٍ فيها تكرار، ولا تُثبَّت الخانةُ المُقايَضة."""

    generator = random.Random(1)
    with pytest.raises(SlotRightsAlgebraError):
        distinctness_preserving_swap_chain(
            [("ب", "ت", "ث"), ("ب", "ت", "ث")],
            slot=2,
            block_slot=1,
            steps=1,
            generator=generator,
        )
    with pytest.raises(SlotRightsAlgebraError):
        distinctness_preserving_swap_chain(
            [("ب", "ت", "ث")], slot=2, block_slot=2, steps=1, generator=generator
        )


def test_composition_closure_fails_on_this_deposit() -> None:
    """الرابطتان المتجاورتان لا تستغرقان الجذر، فـ``B₁₃`` رابطةٌ مستقلّة."""

    reading = measure_closure(draws=40, burn_in=40000, sweep=800)
    assert isinstance(reading, ClosureReading)
    assert reading.closure_holds is False
    assert reading.same_place_ratio < 1.0
    assert reading.identity_ratio < 1.0


def test_a_closure_reading_refuses_an_impossible_null_mean() -> None:
    """لا تُنسَب نسبةٌ إلى متوسّطٍ صفريٍّ غيرِ موجب."""

    with pytest.raises(SlotRightsAlgebraError):
        ClosureReading(1, 1, 0.0, 1.0, 0.5, 0.5, 10)
    with pytest.raises(SlotRightsAlgebraError):
        ClosureReading(1, 1, 1.0, 1.0, 0.5, 0.5, 0)


# ---------------------------------------------------------------------------
# الطبقة الثالثة
# ---------------------------------------------------------------------------


def test_every_typed_cell_carries_its_relation_kind_threshold_and_draws() -> None:
    """لا حكمَ بلا قيده: نوعُ العلاقة ونوعُ الخليّة والعتبةُ وعددُ التبديلات."""

    verdicts = typed_cell_verdicts(draws=30, burn_in=5000, sweep=200)
    assert verdicts
    assert {verdict.relation for verdict in verdicts} == set(RelationType)
    assert {verdict.kind for verdict in verdicts} == set(CellKind)
    assert all(verdict.threshold > 0.0 for verdict in verdicts)
    assert all(verdict.draws == 30 for verdict in verdicts)
    assert all(
        verdict.licence is AlgebraLicenceStanding.WITHHELD_NO_PRIOR_CONDITION
        for verdict in verdicts
    )


def test_a_single_letter_class_has_no_class_cell_at_all() -> None:
    """الفئةُ ذاتُ الحرف الواحد لا خليّةَ تجانسٍ لها، فلا تُعَدّ ولا تُصحَّح."""

    singletons = {
        name
        for name, letters in THE_DECLARED_PLACE_CLASSES.items()
        if len(letters) == 1
    }
    assert singletons
    verdicts = typed_cell_verdicts(draws=20, burn_in=2000, sweep=100)
    for verdict in verdicts:
        if verdict.place_class in singletons:
            assert verdict.kind is CellKind.IDENTITY


def test_a_correction_finer_than_the_two_sided_floor_is_unresolvable_not_neutral() -> (
    None
):
    """ضيقُ العدد يُخرِج «متعذّرًا»، ولا يُقرأ حيادًا مصنوعًا."""

    verdicts = typed_cell_verdicts(draws=20, burn_in=2000, sweep=100)
    assert 2.0 / 21.0 >= verdicts[0].threshold
    assert all(
        verdict.standing is VerdictStanding.UNRESOLVABLE_AT_THIS_B
        for verdict in verdicts
    )


def test_the_positional_asymmetry_lives_in_the_identity_cell_alone() -> None:
    """الفرقُ بين العلاقتين المتجاورتين في التماثل لا في التجانس."""

    locus = positional_asymmetry_locus(draws=200)
    assert isinstance(locus, AsymmetryLocus)
    assert locus.locus is CellKind.IDENTITY
    assert locus.identity_difference > locus.class_difference
    assert locus.identity_probability < locus.class_probability


def test_an_asymmetry_locus_refuses_an_impossible_probability() -> None:
    """قيمةُ p في مجال ]0,1]، وصفرٌ حدٌّ لا قيمة."""

    with pytest.raises(SlotRightsAlgebraError):
        AsymmetryLocus(1, 1, 0.0, 0.5, 0.025, 10)
    with pytest.raises(SlotRightsAlgebraError):
        AsymmetryLocus(1, 1, 0.5, 0.5, 0.025, 0)


# ---------------------------------------------------------------------------
# المنقولُ في وجه المقيس، والخمولُ السلطويّ
# ---------------------------------------------------------------------------


def test_the_quoted_root_total_does_not_match_what_this_tree_measures() -> None:
    """العدّةُ المنقولةُ لا يُعيدها هذا القرص، ويُقرأ الفرقُ ولا يُطوى."""

    rows = quoted_against_measured()
    quoted = next(row for row in rows if row[0] == "عدّةُ جذور المقاييس")
    assert quoted[1] == "4,362 جذرًا"
    assert quoted[3] is False
    assert f"{len(algebra_substrate()):,}" in quoted[2]


def test_the_quoted_cell_total_is_the_one_figure_that_does_replicate() -> None:
    """أربعٌ وثمانون خليّةً مشهودةٌ كلُّها: منقولٌ طابق المقيس."""

    rows = quoted_against_measured()
    cells = next(row for row in rows if row[0] == "خلايا الحقوق")
    assert cells[3] is True


def test_the_quoted_figures_are_recorded_and_none_is_used_as_a_premise() -> None:
    """المنقولُ مُسجَّلٌ بقيده، ولا يدخل في حسابٍ ولا يُبنى عليه حكم."""

    assert THE_QUOTED_ALGEBRA_FIGURES
    source = MODULE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in {
            "typed_cell_verdicts",
            "measure_closure",
            "slot_rights",
            "exchangeability_rejection",
            "positional_asymmetry_locus",
        }:
            names = {
                child.id for child in ast.walk(node) if isinstance(child, ast.Name)
            }
            assert "THE_QUOTED_ALGEBRA_FIGURES" not in names


def test_this_module_imports_neither_the_kernel_nor_the_programme() -> None:
    """اتّجاهُ الاعتماد مفحوصٌ بشجرة الصياغة لا بالثقة."""

    tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            assert "kernel" not in node.module
            assert "program" not in node.module
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert "kernel" not in alias.name
                assert "program" not in alias.name


def test_every_named_residual_is_a_sentence_and_none_is_an_empty_label() -> None:
    """البقايا المُسمّاةُ جملٌ تُقرأ، لا وسومٌ فارغة."""

    assert len(SLOT_RIGHTS_ALGEBRA_NAMED_RESIDUALS) >= 7
    for name, text in SLOT_RIGHTS_ALGEBRA_NAMED_RESIDUALS.items():
        assert name.isupper()
        assert len(text) > 60


def test_every_quoted_algebra_figure_has_its_twin_in_the_one_register() -> None:
    """المنقولُ يُسجَّل في سجلّ الأرقام الواحد لا في مخزنٍ موازٍ."""

    from alghanem.program.direct_certainty import REPORTED_UNVERIFIED_FIGURES

    recorded = {
        (record.subject, record.figure_text) for record in REPORTED_UNVERIFIED_FIGURES
    }
    for subject, figure in THE_QUOTED_ALGEBRA_FIGURES.items():
        assert (subject, figure) in recorded


# ---------------------------------------------------------------------------
# الطبقة الرابعة: الترخيصُ مثلّثًا لا سلسلة
# ---------------------------------------------------------------------------


def test_the_cube_move_preserves_every_one_of_the_three_margins() -> None:
    """مبرهنة ث١ مفحوصةٌ عدًّا لا وصفًا."""

    assert verify_cube_move_preserves_all_margins() is True


def test_the_three_ternary_statistics_each_have_a_counter_witness() -> None:
    """مبرهنة ث٢: لا إحصاءةَ فيها فضلةُ هوامش، وإلّا كان الاختبارُ فارغًا."""

    assert verify_ternary_statistics_are_not_margin_determined() is True


def test_a_bare_cube_cannot_move_the_coverage_statistic_at_all() -> None:
    """الكشفُ الذي سبق العدّ: التغطيةُ لا يُحرّكها مكعّبٌ مجرّد، فلزم الصدى."""

    letters = ("a", "b", "c", "d", "e", "f")
    sides = [
        [
            (letters[first], letters[2 + middle], letters[4 + last])
            for first, middle, last in diagonal
        ]
        for diagonal in (
            ((0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)),
            ((0, 0, 1), (0, 1, 0), (1, 0, 0), (1, 1, 1)),
        )
    ]
    for assignment in product("012", repeat=len(letters)):
        places = dict(zip(letters, assignment, strict=True))
        left = ternary_statistics(sides[0], places)
        right = ternary_statistics(sides[1], places)
        assert (
            left[TernaryStatistic.PLACE_TRIPLE_COVERAGE]
            == right[TernaryStatistic.PLACE_TRIPLE_COVERAGE]
        )


def test_the_chain_never_changes_the_size_of_the_lexicon() -> None:
    """الحارسُ الذي أسقط خللًا واقعًا: الحجمُ ثابتٌ في كلّ خطوة."""

    body = algebra_substrate()
    present = set(body)
    letters = tuple(sorted({letter for root in body for letter in root}))
    no_three_way_interaction_chain(
        present,
        letters,
        accepted_target=5,
        generator=random.Random(3),
        proposal_budget=200_000,
    )
    assert len(present) == len(body)


def test_the_chain_preserves_all_three_pairwise_tables_exactly() -> None:
    """ما يتحرّك هو الحدُّ الثلاثيُّ وحدَه؛ والجداولُ الثلاثةُ لا تُمسّ."""

    body = algebra_substrate()
    present = set(body)
    letters = tuple(sorted({letter for root in body for letter in root}))

    def tables(rows: set[tuple[str, str, str]]) -> tuple[list[tuple[str, str]], ...]:
        return tuple(
            sorted((row[left], row[right]) for row in rows)
            for left, right in ((0, 1), (1, 2), (0, 2))
        )

    before = tables(present)
    moved = no_three_way_interaction_chain(
        present,
        letters,
        accepted_target=30,
        generator=random.Random(5),
        proposal_budget=2_000_000,
    )
    assert moved > 0
    assert tables(present) == before


def test_the_triangle_condition_was_written_before_the_count() -> None:
    """الشرطُ نصٌّ يُقرأ، وفيه العتبةُ والحارسُ ومنعُ الترخيص معًا."""

    assert "قبل تشغيل قياسها" in THE_PREREGISTERED_TRIANGLE_CONDITION
    assert "UNMIXED" in THE_PREREGISTERED_TRIANGLE_CONDITION
    assert "مرخّص" in THE_PREREGISTERED_TRIANGLE_CONDITION


def test_a_still_chain_is_read_as_unmixed_and_never_as_a_closed_triangle() -> None:
    """جمودُ السلسلة منزلةٌ ثالثةٌ لا انغلاق."""

    reading = TriangleReading(
        observed=dict.fromkeys(TernaryStatistic, 7),
        null_mean=dict.fromkeys(TernaryStatistic, 7.0),
        probability=dict.fromkeys(TernaryStatistic, 1.0),
        spread=dict.fromkeys(TernaryStatistic, 1),
        accepted_moves=0,
        draws=200,
        threshold=0.05 / 3,
        accepted_floor=1000,
    )
    assert reading.mixed is False
    assert reading.standing is TriangleStanding.UNMIXED


def test_a_threshold_finer_than_the_two_sided_floor_is_unmixed_not_closed() -> None:
    """عتبةٌ أدقُّ من حدّ التبديل تُخرِج تعذّرًا لا انغلاقًا."""

    reading = TriangleReading(
        observed=dict.fromkeys(TernaryStatistic, 7),
        null_mean=dict.fromkeys(TernaryStatistic, 9.0),
        probability=dict.fromkeys(TernaryStatistic, 1.0),
        spread=dict.fromkeys(TernaryStatistic, 40),
        accepted_moves=5000,
        draws=10,
        threshold=0.05 / 3,
        accepted_floor=1000,
    )
    assert reading.standing is TriangleStanding.UNMIXED


def test_one_statistic_beyond_the_threshold_makes_the_triangle_fail() -> None:
    """خروجُ إحصاءةٍ واحدةٍ يكفي لإسقاط المثلّث، بالشرط المكتوب."""

    probability = dict.fromkeys(TernaryStatistic, 0.9)
    probability[TernaryStatistic.PLACE_HOMOGENEOUS] = 0.001
    reading = TriangleReading(
        observed=dict.fromkeys(TernaryStatistic, 7),
        null_mean=dict.fromkeys(TernaryStatistic, 9.0),
        probability=probability,
        spread=dict.fromkeys(TernaryStatistic, 40),
        accepted_moves=5000,
        draws=2000,
        threshold=0.05 / 3,
        accepted_floor=1000,
    )
    assert reading.standing is TriangleStanding.FAILS


def test_a_triangle_reading_missing_a_statistic_is_refused() -> None:
    """قراءةٌ ناقصةُ الإحصاءات لا تُبنى."""

    with pytest.raises(SlotRightsAlgebraError):
        TriangleReading(
            observed={TernaryStatistic.PLACE_HOMOGENEOUS: 1},
            null_mean={TernaryStatistic.PLACE_HOMOGENEOUS: 1.0},
            probability={TernaryStatistic.PLACE_HOMOGENEOUS: 1.0},
            spread={TernaryStatistic.PLACE_HOMOGENEOUS: 2},
            accepted_moves=5000,
            draws=200,
            threshold=0.05 / 3,
            accepted_floor=1000,
        )


def test_the_triangle_measurement_runs_and_reports_its_own_mixing() -> None:
    """قياسٌ قصيرٌ يُخرِج قراءةً كاملةً ويُصرّح بخلطه لا يُخفيه."""

    reading = measure_triangle_closure(
        draws=3,
        burn_in=2,
        sweep=1,
        proposal_budget=60_000,
        accepted_floor=1000,
        seed=17,
    )
    assert isinstance(reading, TriangleReading)
    assert reading.standing is TriangleStanding.UNMIXED
    assert set(reading.observed) == set(TernaryStatistic)


def test_the_triangle_layer_grants_no_licence_whatever_it_finds() -> None:
    """المنزلتان معًا خارج الترخيص، لأنّ المصدرَ الثاني غائب."""

    assert licence_standing() is not AlgebraLicenceStanding.LICENSED
    assert "مرخّص" in THE_PREREGISTERED_TRIANGLE_CONDITION
