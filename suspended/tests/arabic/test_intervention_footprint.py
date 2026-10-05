"""Predicted-versus-observed commutation of controlled surface interventions."""

from __future__ import annotations

from pathlib import Path

import pytest

import alghanem
from alghanem.arabic.encoding import intervention_footprint
from alghanem.arabic.encoding.intervention import (
    InterventionCoordinateError,
    SurfaceAtomIntervention,
    apply_intervention,
)
from alghanem.arabic.encoding.intervention_footprint import (
    ALTERNATE_ATOMS,
    COORDINATE_CONFIGURATIONS,
    DERIVED_LAW_SCOPE_NOTE,
    IDENTICAL_PAIR_EXCLUSION_NOTE,
    INTERVENTION_TYPES,
    MINIMAL_ATOMS,
    NO_KERNEL_MODULE_CONSUMES_INTERVENTION_FOOTPRINT_NOTE,
    ORDERED_TRIPLES_ABSENCE_NOTE,
    PAYLOAD_INDEPENDENCE_NOTE,
    PREDICTION_ORACLE_MISMATCH_NOTE,
    REFERENCE_ATOMS,
    VALUE_COINCIDENCE_NOTE,
    CommutationAssessment,
    CommutationCheck,
    CommutationVerdict,
    ConflictReason,
    DerivedLawStatus,
    InterventionFootprint,
    InterventionFootprintError,
    PredictionOracleAgreement,
    check_commutation,
    commuting_pairs,
    critical_pairs,
    footprint,
    law_status,
    mismatched_pairs,
    observe_commutation,
    predict_commutation,
    reference_matrix,
    undefined_pairs,
)


def make(
    intervention_type: str,
    coordinates: tuple[int, ...],
    payload: str | None = None,
) -> SurfaceAtomIntervention:
    return SurfaceAtomIntervention(
        "reference-occurrence", "0", intervention_type, coordinates, payload
    )


def test_the_footprint_is_derived_from_its_intervention_not_written_beside_it() -> None:
    deletion = footprint(make("delete", (2,)))
    insertion = footprint(make("insert", (2,), "\u0632"))
    repetition = footprint(make("repeat", (2,)))
    exchange = footprint(make("swap", (3, 2)))
    replacement = footprint(make("substitute", (2,), "\u0632"))

    assert tuple(InterventionFootprint.__dataclass_fields__) == ("intervention",)
    assert deletion.write_set == (2,) and deletion.read_set == ()
    assert deletion.shift.delta == -1 and deletion.shift.origin == 3
    assert insertion.shift.delta == 1 and insertion.shift.origin == 2
    assert repetition.read_set == (2,) and repetition.shift.origin == 3
    assert exchange.read_set == (2, 3) and exchange.write_set == (2, 3)
    assert replacement.shift.delta == 0 and replacement.shift.origin is None
    assert replacement.touched == (2,)


def test_a_footprint_contradicting_its_intervention_cannot_be_constructed() -> None:
    with pytest.raises(TypeError):
        InterventionFootprint(  # type: ignore[call-arg]
            make("delete", (2,)), read_set=(9,)
        )


def test_a_shift_never_declares_an_origin_it_does_not_have() -> None:
    from alghanem.arabic.encoding.intervention_footprint import CoordinateShift

    with pytest.raises(InterventionFootprintError):
        CoordinateShift(0, 3)
    with pytest.raises(InterventionFootprintError):
        CoordinateShift(-1, None)


def test_disjoint_unshifting_interventions_commute() -> None:
    left = make("substitute", (1,), "\u0632")
    right = make("swap", (3, 4))

    check = check_commutation(left, right, REFERENCE_ATOMS, "distant")

    assert check.assessment.verdict is CommutationVerdict.COMMUTES
    assert check.assessment.reason is None
    assert check.observed is CommutationVerdict.COMMUTES
    assert check.agreement is PredictionOracleAgreement.MATCH


def test_a_shared_coordinate_conflicts_by_overlap() -> None:
    check = check_commutation(
        make("substitute", (2,), "\u0632"),
        make("delete", (2,)),
        REFERENCE_ATOMS,
        "same_coordinate",
    )

    assert check.assessment.verdict is CommutationVerdict.CONFLICTS
    assert check.assessment.reason is ConflictReason.OVERLAP
    assert check.observed is CommutationVerdict.CONFLICTS


def test_disjoint_coordinates_still_conflict_through_the_shift() -> None:
    check = check_commutation(
        make("delete", (1,)),
        make("substitute", (4,), "\u0632"),
        REFERENCE_ATOMS,
        "distant",
    )

    assert not set(footprint(check.assessment.left).touched) & set(
        footprint(check.assessment.right).touched
    )
    assert check.assessment.verdict is CommutationVerdict.CONFLICTS
    assert check.assessment.reason is ConflictReason.SHIFT
    assert check.observed is CommutationVerdict.CONFLICTS


def test_an_insert_shifts_from_its_own_coordinate_not_after_it() -> None:
    before = check_commutation(
        make("insert", (2,), "\u0632"),
        make("substitute", (1,), "\u0637"),
        REFERENCE_ATOMS,
        "adjacent",
    )
    at_origin = check_commutation(
        make("insert", (2,), "\u0632"),
        make("substitute", (3,), "\u0637"),
        REFERENCE_ATOMS,
        "adjacent",
    )

    assert before.assessment.verdict is CommutationVerdict.COMMUTES
    assert before.observed is CommutationVerdict.COMMUTES
    assert at_origin.assessment.reason is ConflictReason.SHIFT
    assert at_origin.observed is CommutationVerdict.CONFLICTS


def test_the_undefined_branch_is_reached_and_its_oracle_fails_by_name() -> None:
    first = make("delete", (4,))
    second = make("substitute", (5,), "\u0632")

    assessment = predict_commutation(first, second, len(REFERENCE_ATOMS))
    assert assessment.verdict is CommutationVerdict.UNDEFINED
    assert assessment.reason is ConflictReason.OUT_OF_RANGE

    intermediate = apply_intervention(first, REFERENCE_ATOMS)
    assert len(intermediate) == len(REFERENCE_ATOMS) - 1
    with pytest.raises(InterventionCoordinateError):
        apply_intervention(second, intermediate)

    assert observe_commutation(first, second, REFERENCE_ATOMS) is (
        CommutationVerdict.UNDEFINED
    )
    assert observe_commutation(second, first, REFERENCE_ATOMS) is (
        CommutationVerdict.UNDEFINED
    )


def test_undefined_is_decided_before_overlap_and_before_shift() -> None:
    assessment = predict_commutation(
        make("delete", (5,)), make("delete", (4,)), len(REFERENCE_ATOMS)
    )

    assert assessment.verdict is CommutationVerdict.UNDEFINED
    assert assessment.reason is ConflictReason.OUT_OF_RANGE


def test_an_intervention_outside_the_sequence_is_refused_not_judged() -> None:
    with pytest.raises(InterventionFootprintError):
        predict_commutation(
            make("delete", (9,)), make("delete", (1,)), len(REFERENCE_ATOMS)
        )


def test_a_verdict_cannot_be_paired_with_a_reason_that_contradicts_it() -> None:
    left = make("delete", (1,))
    right = make("delete", (3,))

    with pytest.raises(InterventionFootprintError):
        CommutationAssessment(
            left, right, 6, CommutationVerdict.COMMUTES, ConflictReason.SHIFT
        )
    with pytest.raises(InterventionFootprintError):
        CommutationAssessment(
            left, right, 6, CommutationVerdict.CONFLICTS, ConflictReason.OUT_OF_RANGE
        )
    with pytest.raises(InterventionFootprintError):
        CommutationAssessment(left, right, 6, CommutationVerdict.UNDEFINED, None)


def test_the_reference_matrix_covers_every_type_pair_and_every_configuration() -> None:
    checks = reference_matrix()

    configurations = {check.configuration for check in checks}
    type_pairs = {
        (
            check.assessment.left.intervention_type,
            check.assessment.right.intervention_type,
        )
        for check in checks
    }

    assert configurations == {name for name, *_ in COORDINATE_CONFIGURATIONS}
    assert type_pairs == {
        (left, right) for left in INTERVENTION_TYPES for right in INTERVENTION_TYPES
    }
    assert len(checks) == 198


def test_every_predicted_verdict_is_confirmed_by_the_applied_oracle() -> None:
    checks = reference_matrix()

    assert mismatched_pairs(checks) == ()
    assert law_status(checks) is DerivedLawStatus.DERIVED_LAW_CONFIRMED


def test_the_three_verdicts_are_all_populated_by_the_matrix() -> None:
    checks = reference_matrix()

    commuting = commuting_pairs(checks)
    critical = critical_pairs(checks)
    undefined = undefined_pairs(checks)

    assert len(commuting) + len(critical) + len(undefined) == len(checks)
    assert commuting and critical and undefined
    assert {entry.rsplit(":: ", 1)[1] for entry in critical} == {"overlap", "shift"}


def test_the_named_pair_lists_are_byte_stable() -> None:
    first = reference_matrix()
    second = reference_matrix()

    assert commuting_pairs(first) == commuting_pairs(second)
    assert critical_pairs(first) == critical_pairs(second)
    assert undefined_pairs(first) == undefined_pairs(second)
    assert "delete@4 × substitute@5 [upper_edge]" in undefined_pairs(first)
    assert "delete@1 × substitute@4 [distant] :: shift" in critical_pairs(first)


def test_identical_interventions_are_excluded_by_declaration() -> None:
    checks = reference_matrix()

    assert all(check.assessment.left != check.assessment.right for check in checks)
    assert "الأزواج المتطابقة مستثناةٌ من المصفوفة تصريحًا" in (
        IDENTICAL_PAIR_EXCLUSION_NOTE
    )


def test_a_mismatch_is_labelled_and_never_silently_dropped() -> None:
    left = make("delete", (1,))
    right = make("substitute", (4,), "\u0632")
    assessment = predict_commutation(left, right, len(REFERENCE_ATOMS))
    fabricated = CommutationCheck("distant", assessment, CommutationVerdict.COMMUTES)

    assert fabricated.agreement is (
        PredictionOracleAgreement.PREDICTION_ORACLE_MISMATCH
    )
    assert fabricated.label.startswith("PREDICTION_ORACLE_MISMATCH(")
    assert mismatched_pairs((fabricated,)) == (fabricated.label,)
    assert law_status((fabricated,)) is (DerivedLawStatus.PARTIAL_WITH_NAMED_RESIDUALS)


def test_value_coincidence_is_outside_the_declared_scope_not_swallowed() -> None:
    repeated_atoms = ("\u0623", "\u0623", "\u062c", "\u062f")
    check = check_commutation(
        make("repeat", (0,)),
        make("repeat", (1,)),
        repeated_atoms,
        "adjacent",
    )

    assert check.assessment.verdict is CommutationVerdict.CONFLICTS
    assert check.assessment.reason is ConflictReason.SHIFT
    assert check.observed is CommutationVerdict.COMMUTES
    assert check.agreement is (PredictionOracleAgreement.PREDICTION_ORACLE_MISMATCH)
    assert len(set(REFERENCE_ATOMS)) == len(REFERENCE_ATOMS)
    assert "مصادفةً قيميّة لا تبادلًا بنيويًّا" in VALUE_COINCIDENCE_NOTE


def test_a_non_adjacent_swap_straddling_a_shift_origin_conflicts_by_shift() -> None:
    check = check_commutation(
        make("delete", (2,)),
        make("swap", (1, 4)),
        REFERENCE_ATOMS,
        "straddling_swap",
    )

    assert check.assessment.verdict is CommutationVerdict.CONFLICTS
    assert check.assessment.reason is ConflictReason.SHIFT
    assert check.observed is CommutationVerdict.CONFLICTS
    assert check.agreement is PredictionOracleAgreement.MATCH
    assert f"{check.label} :: shift" in critical_pairs(reference_matrix())


def test_a_swap_sharing_exactly_one_coordinate_conflicts_by_overlap() -> None:
    check = check_commutation(
        make("delete", (1,)),
        make("swap", (1, 3)),
        REFERENCE_ATOMS,
        "swap_shares_one_coordinate",
    )

    assert set(footprint(check.assessment.left).touched) & set(
        footprint(check.assessment.right).touched
    ) == {1}
    assert check.assessment.verdict is CommutationVerdict.CONFLICTS
    assert check.assessment.reason is ConflictReason.OVERLAP
    assert check.observed is CommutationVerdict.CONFLICTS


def test_the_widened_configurations_are_still_confirmed_by_the_oracle() -> None:
    checks = reference_matrix()
    widened = {"straddling_swap", "swap_shares_one_coordinate"}

    assert widened <= {name for name, *_ in COORDINATE_CONFIGURATIONS}
    assert [check for check in checks if check.configuration in widened]
    assert mismatched_pairs(checks) == ()
    assert law_status(checks) is DerivedLawStatus.DERIVED_LAW_CONFIRMED


def test_the_minimal_two_atom_sequence_is_measured_not_assumed() -> None:
    checks = reference_matrix(MINIMAL_ATOMS)

    assert len(MINIMAL_ATOMS) == 2
    assert len(set(MINIMAL_ATOMS)) == len(MINIMAL_ATOMS)
    assert checks
    assert mismatched_pairs(checks) == ()
    assert law_status(checks) is DerivedLawStatus.DERIVED_LAW_CONFIRMED
    assert undefined_pairs(checks)


def test_the_verdicts_follow_coordinates_and_length_not_atom_values() -> None:
    reference = reference_matrix()
    alternate = reference_matrix(ALTERNATE_ATOMS)

    assert len(ALTERNATE_ATOMS) == len(REFERENCE_ATOMS)
    assert len(set(ALTERNATE_ATOMS)) == len(ALTERNATE_ATOMS)
    assert not set(ALTERNATE_ATOMS) & set(REFERENCE_ATOMS)
    assert commuting_pairs(alternate) == commuting_pairs(reference)
    assert critical_pairs(alternate) == critical_pairs(reference)
    assert undefined_pairs(alternate) == undefined_pairs(reference)
    assert mismatched_pairs(alternate) == ()
    assert "الإحداثيات والطول وحدهما" in PAYLOAD_INDEPENDENCE_NOTE


def test_ordered_triples_are_absent_by_record_not_by_silence() -> None:
    exported = set(intervention_footprint.__all__) - {"ORDERED_TRIPLES_ABSENCE_NOTE"}

    assert not [name for name in exported if "triple" in name.lower()]
    assert not [
        name
        for name in exported
        if callable(getattr(intervention_footprint, name)) and "triple" in name.lower()
    ]
    assert "ولا ثلاثياتٍ هنا" in ORDERED_TRIPLES_ABSENCE_NOTE
    assert "لا يُشتَقّ " in ORDERED_TRIPLES_ABSENCE_NOTE


def test_an_empty_matrix_confirms_no_law() -> None:
    with pytest.raises(InterventionFootprintError):
        law_status(())


def test_no_module_consumes_the_intervention_footprint_verdict() -> None:
    package_root = Path(alghanem.__file__).parent
    permitted = {
        package_root / "arabic" / "encoding" / "intervention_footprint.py",
        package_root / "arabic" / "encoding" / "__init__.py",
    }
    consumers = [
        path
        for path in package_root.rglob("*.py")
        if path not in permitted
        and "intervention_footprint" in path.read_text(encoding="utf-8")
    ]

    assert consumers == []
    assert "لا وحدةَ نواة ولا " in (
        NO_KERNEL_MODULE_CONSUMES_INTERVENTION_FOOTPRINT_NOTE
    )


def test_no_kernel_module_reads_the_intervention_layer_at_all() -> None:
    kernel_root = Path(alghanem.__file__).parent / "kernel"
    readers = [
        path
        for path in kernel_root.rglob("*.py")
        if "intervention" in path.read_text(encoding="utf-8")
    ]

    assert readers == []


def test_the_recorded_scope_note_does_not_claim_a_generalized_law() -> None:
    assert "لا قانونَ تبادلٍ " in DERIVED_LAW_SCOPE_NOTE
    assert "PREDICTION_ORACLE_MISMATCH" in PREDICTION_ORACLE_MISMATCH_NOTE
