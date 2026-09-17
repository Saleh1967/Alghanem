"""اختباراتُ قياس فضاء الرصد لكلّ حامل: تُشغِّل القياسَ على نصٍّ مُودَعٍ وغيره."""

from __future__ import annotations

import pytest

from alghanem.arabic.carrier_fiber_preregistration import CARRIER_FIBER_STATE_SCHEMA
from alghanem.arabic.carrier_state_observed_fiber import (
    ABSENT,
    CARRIER_STATE_OBSERVED_FIBER_NAMED_RESIDUALS,
    OBSERVED_SPACE_IS_NOT_A_GLOBAL_PRODUCT,
    Boundary,
    CorpusDeposit,
    ObservedStateFiberError,
    derive_cross_axis_cooccurrences,
    read_corpus_lines,
    run_observed_fiber_on_the_deposited_fatiha,
    tabulate_observed_fibers,
)
from alghanem.canonical_content import canonical_digest

_ALIF = "\u0627"
_FATHA = "\u064e"
_DAMMA = "\u064f"
_KASRA = "\u0650"
_FATHATAN = "\u064b"
_SHADDA = "\u0651"
_SUKUN = "\u0652"


def _deposit_for(text: str) -> tuple[CorpusDeposit, tuple[str, ...]]:
    data = text.encode("utf-8")
    return read_corpus_lines(
        data, source_id="probe-corpus", expected_sha256=canonical_digest(data)
    )


# --- المدوّنةُ مدخلٌ ببصمتها --------------------------------------------------


def test_any_corpus_may_be_read_when_its_digest_matches() -> None:
    deposit, lines = _deposit_for("بَابٌ\nكِتَاب")
    assert deposit.byte_length > 0
    assert lines == ("بَابٌ", "كِتَاب")


def test_corpus_bytes_that_miss_their_digest_are_refused() -> None:
    with pytest.raises(ObservedStateFiberError):
        read_corpus_lines(
            "بَاب".encode(), source_id="probe-corpus", expected_sha256="0" * 64
        )


def test_a_deposit_without_a_canonical_digest_is_refused() -> None:
    with pytest.raises(ObservedStateFiberError):
        CorpusDeposit(
            source_id="x", sha256="abc", byte_length=3, normalization_form="NFC"
        )


# --- الحالةُ متَّجِهٌ على المحاور، لا قيمةٌ مسطّحة ----------------------------


def test_a_state_is_read_as_a_vector_over_the_measured_axes() -> None:
    deposit, lines = _deposit_for(f"ب{_FATHA}")
    table = tabulate_observed_fibers(lines, deposit=deposit)
    assert table.rows[0].state_vector == (
        ("vowel", _FATHA),
        ("nunation", ABSENT),
        ("gemination", ABSENT),
        ("quiescence", ABSENT),
    )


def test_gemination_and_a_vowel_occupy_two_axes_not_one_slot() -> None:
    deposit, lines = _deposit_for(f"ب{_FATHA}{_SHADDA}")
    table = tabulate_observed_fibers(lines, deposit=deposit)
    vector = dict(table.rows[0].state_vector)
    assert vector["gemination"] == _SHADDA
    assert vector["vowel"] == _FATHA
    assert table.axis_exclusivity_violations == ()


def test_two_vowels_on_one_carrier_are_kept_as_an_exclusivity_violation_row() -> None:
    deposit, lines = _deposit_for(f"ب{_FATHA}{_DAMMA}")
    table = tabulate_observed_fibers(lines, deposit=deposit)
    assert len(table.axis_exclusivity_violations) == 1
    violation = table.axis_exclusivity_violations[0]
    assert violation.axis_id == "vowel"
    assert violation.marks == (_FATHA, _DAMMA)
    assert len(table.rows) == 1


def test_a_deferred_axis_mark_is_kept_on_the_row_and_absent_from_the_vector() -> None:
    deposit, lines = _deposit_for("ب\u0670")
    table = tabulate_observed_fibers(lines, deposit=deposit)
    row = table.rows[0]
    assert row.deferred_axis_marks == ("\u0670",)
    assert "madd" not in dict(row.state_vector)


def test_a_mark_outside_every_declared_axis_is_kept_as_unread() -> None:
    deposit, lines = _deposit_for("ب\u0654")
    table = tabulate_observed_fibers(lines, deposit=deposit)
    assert table.rows[0].unread_marks == ("\u0654",)


# --- الموضعُ والطرفيّة --------------------------------------------------------


def test_boundary_is_derived_from_the_position_of_the_carrier_in_its_word() -> None:
    deposit, lines = _deposit_for("بسم")
    table = tabulate_observed_fibers(lines, deposit=deposit)
    assert [row.boundary for row in table.rows] == [
        Boundary.WORD_INITIAL,
        Boundary.WORD_MEDIAL,
        Boundary.WORD_FINAL,
    ]


def test_a_single_carrier_word_is_read_as_sole_not_initial() -> None:
    deposit, lines = _deposit_for("ب")
    table = tabulate_observed_fibers(lines, deposit=deposit)
    assert table.rows[0].boundary is Boundary.WORD_SOLE
    assert table.rows[0].stratum == (0, "WORD_SOLE")


# --- الليفُ: سعةٌ وتركيبٌ حقلان لا حقلٌ واحد ---------------------------------


def test_two_carriers_may_share_a_capacity_and_differ_in_composition() -> None:
    deposit, lines = _deposit_for(f"ب{_FATHA} ت{_DAMMA}")
    table = tabulate_observed_fibers(lines, deposit=deposit)
    first = table.fiber_for("ب")
    second = table.fiber_for("ت")
    assert first.capacity == second.capacity == 1
    assert set(first.composition) != set(second.composition)


def test_the_product_refutation_is_derived_and_carries_its_scope() -> None:
    deposit, lines = _deposit_for(f"ب{_FATHA} ت{_DAMMA}")
    table = tabulate_observed_fibers(lines, deposit=deposit)
    witness = table.derive_product_refutation()
    assert witness is not None
    assert witness.refutes_global_product_in_scope
    assert witness.scope_note == OBSERVED_SPACE_IS_NOT_A_GLOBAL_PRODUCT
    assert witness.source_sha256 == deposit.sha256


def test_a_corpus_whose_carriers_share_one_fiber_refutes_nothing() -> None:
    deposit, lines = _deposit_for(f"ب{_FATHA} ت{_FATHA}")
    table = tabulate_observed_fibers(lines, deposit=deposit)
    assert table.derive_product_refutation() is None


def test_an_absent_carrier_is_refused_by_name_not_given_an_empty_fiber() -> None:
    deposit, lines = _deposit_for("ب")
    table = tabulate_observed_fibers(lines, deposit=deposit)
    with pytest.raises(ObservedStateFiberError):
        table.fiber_for("ز")


def test_the_observed_support_never_exceeds_the_flat_product_size() -> None:
    table = run_observed_fiber_on_the_deposited_fatiha()
    assert table.observed_support_size <= table.global_product_size


# --- اجتماعُ المحاور: شاهدٌ على عدم التنافي ----------------------------------


def test_cross_axis_cooccurrence_is_derived_from_the_rows() -> None:
    deposit, lines = _deposit_for(f"ب{_FATHA}{_SHADDA}")
    table = tabulate_observed_fibers(lines, deposit=deposit)
    cooccurrences = derive_cross_axis_cooccurrences(table)
    assert [
        (row.first_axis_id, row.second_axis_id, row.occurrence_count)
        for row in cooccurrences
    ] == [("vowel", "gemination", 1)]


def test_the_deposited_text_shows_gemination_with_a_vowel() -> None:
    table = run_observed_fiber_on_the_deposited_fatiha()
    pairs = {
        (row.first_axis_id, row.second_axis_id): row.occurrence_count
        for row in derive_cross_axis_cooccurrences(table)
    }
    assert pairs[("vowel", "gemination")] > 0


# --- المعايرةُ على النصّ المُودَع ---------------------------------------------


def test_the_calibration_run_uses_the_deposited_digest_and_the_frozen_schema() -> None:
    table = run_observed_fiber_on_the_deposited_fatiha()
    assert table.schema == CARRIER_FIBER_STATE_SCHEMA
    assert len(table.deposit.sha256) == 64
    assert len(table.rows) > 0


def test_every_occurrence_of_the_deposited_text_is_one_row() -> None:
    table = run_observed_fiber_on_the_deposited_fatiha()
    assert len(table.rows) == sum(fiber.frequency for fiber in table.fibers)


def test_the_alif_fiber_of_the_deposited_text_is_derived_not_declared() -> None:
    table = run_observed_fiber_on_the_deposited_fatiha()
    fiber = table.fiber_for(_ALIF)
    assert fiber.frequency > 0
    assert fiber.capacity == len(set(fiber.composition))


def test_a_nunated_carrier_is_read_on_the_nunation_axis() -> None:
    deposit, lines = _deposit_for(f"ب{_FATHATAN}")
    table = tabulate_observed_fibers(lines, deposit=deposit)
    assert dict(table.rows[0].state_vector)["nunation"] == _FATHATAN
    assert dict(table.rows[0].state_vector)["vowel"] == ABSENT


def test_a_quiescent_carrier_is_read_on_its_own_axis() -> None:
    deposit, lines = _deposit_for(f"ب{_SUKUN}")
    table = tabulate_observed_fibers(lines, deposit=deposit)
    assert dict(table.rows[0].state_vector)["quiescence"] == _SUKUN


def test_a_kasra_is_read_on_the_vowel_axis() -> None:
    deposit, lines = _deposit_for(f"ب{_KASRA}")
    table = tabulate_observed_fibers(lines, deposit=deposit)
    assert dict(table.rows[0].state_vector)["vowel"] == _KASRA


# --- ما لا يحسمه القياس، مكتوبٌ لا مطويّ --------------------------------------


def test_every_named_residual_is_keyed_by_its_own_name() -> None:
    for name, text in CARRIER_STATE_OBSERVED_FIBER_NAMED_RESIDUALS.items():
        assert text.startswith(f"{name}:")


# --- سلطة: هذا القياس خاملٌ في النواة -----------------------------------------


def test_no_kernel_module_reads_this_measurement() -> None:
    import pkgutil

    import alghanem.kernel as kernel_package

    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        source = module.module_finder.find_spec(  # type: ignore[union-attr]
            module.name
        )
        assert source is not None and source.origin is not None
        with open(source.origin, encoding="utf-8") as handle:
            text = handle.read()
        assert "carrier_state_observed_fiber" not in text, module.name
        assert "ObservedFiberTable" not in text, module.name
