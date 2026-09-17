"""اختباراتُ المواصفة المُجمَّدة لليف الحامل: تُشغِّلها ولا تكتفي بوجودها."""

from __future__ import annotations

from dataclasses import replace

import pytest

from alghanem.arabic.carrier_fiber_preregistration import (
    ALTERNATIVE_HYPOTHESIS_TEXT,
    CARRIER_FIBER_PREREGISTRATION_NAMED_RESIDUALS,
    CARRIER_FIBER_STATE_SCHEMA,
    FROZEN_CARRIER_FIBER_SPECIFICATION,
    NULL_HYPOTHESIS_TEXT,
    WORD_ROLE_IS_A_DEFERRED_COVARIATE,
    AxisStanding,
    CanonicalCarrierFiberSpecificationEncoder,
    CarrierFiberPreregistrationError,
    CarrierFiberSpecificationContentBinding,
    CarrierFiberSpecificationContentIdentity,
    CorpusRole,
    Covariate,
    CovariateDeclaration,
    CovariateStanding,
    FiberMeasure,
    FiberOutcome,
    PreEvidenceCarrierFiberSpecificationRegistry,
    StateAxisDeclaration,
    StateSchema,
    freeze_declared_specification,
)

_FATHA = "\u064e"
_DAMMA = "\u064f"
_SHADDA = "\u0651"


# --- مخطَّطُ الحالة: محاورٌ لا مجموعةٌ مسطّحة --------------------------------


def test_the_declared_schema_is_a_product_of_axes_not_one_flat_axis() -> None:
    assert CARRIER_FIBER_STATE_SCHEMA.is_product_of_axes
    assert not CARRIER_FIBER_STATE_SCHEMA.is_single_axis
    assert [
        axis_id for axis_id, _ in CARRIER_FIBER_STATE_SCHEMA.declared_product_shape
    ] == [
        "vowel",
        "nunation",
        "gemination",
        "quiescence",
    ]


def test_absence_is_a_value_on_every_measured_axis() -> None:
    for _, size in CARRIER_FIBER_STATE_SCHEMA.declared_product_shape:
        assert size >= 2


def test_the_madd_axis_is_deferred_and_never_enters_the_measured_state() -> None:
    deferred = CARRIER_FIBER_STATE_SCHEMA.deferred_axes
    assert [axis.axis_id for axis in deferred] == ["madd"]
    assert not deferred[0].standing.enters_the_measured_state
    assert deferred[0] not in CARRIER_FIBER_STATE_SCHEMA.measured_axes


def test_one_mark_may_not_belong_to_two_axes() -> None:
    first = StateAxisDeclaration(
        axis_id="a",
        marks=(_FATHA,),
        standing=AxisStanding.MEASURED_AS_ORTHOGONAL_AXIS,
        exclusivity_within_axis_is_claimed=True,
        declared_reason="محورٌ أوّل",
    )
    second = replace(first, axis_id="b")
    with pytest.raises(CarrierFiberPreregistrationError):
        StateSchema(schema_id="two-axes-one-mark", axes=(first, second))


def test_a_schema_whose_axes_are_all_deferred_measures_nothing() -> None:
    deferred = StateAxisDeclaration(
        axis_id="madd",
        marks=(_SHADDA,),
        standing=AxisStanding.DEFERRED_NOT_READ_AS_A_STATE,
        exclusivity_within_axis_is_claimed=False,
        declared_reason="مؤجَّلٌ وحدَه",
    )
    with pytest.raises(CarrierFiberPreregistrationError):
        StateSchema(schema_id="all-deferred", axes=(deferred,))


def test_an_axis_without_marks_is_refused() -> None:
    with pytest.raises(CarrierFiberPreregistrationError):
        StateAxisDeclaration(
            axis_id="empty",
            marks=(),
            standing=AxisStanding.MEASURED_AS_ORTHOGONAL_AXIS,
            exclusivity_within_axis_is_claimed=True,
            declared_reason="بلا علامة",
        )


# --- المشاركات: ثلاثةٌ مضبوطةٌ، ودورُ الكلمة مؤجَّلٌ بالبناء -----------------


def test_the_frozen_controls_are_frequency_position_and_boundary() -> None:
    assert FROZEN_CARRIER_FIBER_SPECIFICATION.frozen_controls == (
        Covariate.FREQUENCY,
        Covariate.POSITION,
        Covariate.BOUNDARY,
    )
    assert FROZEN_CARRIER_FIBER_SPECIFICATION.deferred_covariates == (
        Covariate.WORD_ROLE,
    )


def test_word_role_may_not_be_declared_a_frozen_control() -> None:
    with pytest.raises(CarrierFiberPreregistrationError) as error:
        CovariateDeclaration(
            covariate=Covariate.WORD_ROLE,
            standing=CovariateStanding.FROZEN_CONTROL,
            declared_reason="وسمٌ صرفيٌّ مُختلَق",
        )
    assert WORD_ROLE_IS_A_DEFERRED_COVARIATE in str(error.value)


def test_a_specification_silent_about_one_covariate_is_refused() -> None:
    partial = tuple(
        declaration
        for declaration in FROZEN_CARRIER_FIBER_SPECIFICATION.covariates
        if declaration.covariate is not Covariate.WORD_ROLE
    )
    with pytest.raises(CarrierFiberPreregistrationError):
        replace(FROZEN_CARRIER_FIBER_SPECIFICATION, covariates=partial)


# --- الفرضيتان والمقاييس -----------------------------------------------------


def test_the_null_hypothesis_is_conditional_independence_not_a_count_comparison() -> (
    None
):
    assert FROZEN_CARRIER_FIBER_SPECIFICATION.null_hypothesis == NULL_HYPOTHESIS_TEXT
    assert "⟂" in NULL_HYPOTHESIS_TEXT
    assert "Frequency, Position, Boundary" in NULL_HYPOTHESIS_TEXT
    assert (
        FROZEN_CARRIER_FIBER_SPECIFICATION.alternative_hypothesis
        == ALTERNATIVE_HYPOTHESIS_TEXT
    )


def test_a_rewritten_hypothesis_is_refused() -> None:
    with pytest.raises(CarrierFiberPreregistrationError):
        replace(
            FROZEN_CARRIER_FIBER_SPECIFICATION,
            null_hypothesis="H0: |S(C)| تحدّده كثرةُ ظهور C",
        )


def test_capacity_and_composition_are_both_frozen_and_distribution_is_deferred() -> (
    None
):
    assert set(FROZEN_CARRIER_FIBER_SPECIFICATION.measures) == {
        FiberMeasure.CAPACITY,
        FiberMeasure.COMPOSITION,
    }
    assert not FiberMeasure.CONDITIONAL_DISTRIBUTION.is_measured_in_this_specification


def test_capacity_alone_is_refused_as_the_measure_set() -> None:
    with pytest.raises(CarrierFiberPreregistrationError):
        replace(FROZEN_CARRIER_FIBER_SPECIFICATION, measures=(FiberMeasure.CAPACITY,))


def test_the_outcome_vocabulary_covers_every_member() -> None:
    assert set(FROZEN_CARRIER_FIBER_SPECIFICATION.outcome_vocabulary) == set(
        FiberOutcome
    )
    with pytest.raises(CarrierFiberPreregistrationError):
        replace(
            FROZEN_CARRIER_FIBER_SPECIFICATION,
            outcome_vocabulary=(FiberOutcome.NARROWER_THAN_CHANCE,),
        )


def test_the_corpus_role_of_this_revision_is_calibration() -> None:
    assert FROZEN_CARRIER_FIBER_SPECIFICATION.corpus_role is (
        CorpusRole.CALIBRATION_WITNESS
    )


# --- التجميدُ والبصمةُ والربط -------------------------------------------------


def test_the_frozen_content_identity_is_stable_across_encodings() -> None:
    first = CanonicalCarrierFiberSpecificationEncoder.encode(
        FROZEN_CARRIER_FIBER_SPECIFICATION
    )
    second = CanonicalCarrierFiberSpecificationEncoder.encode(
        FROZEN_CARRIER_FIBER_SPECIFICATION
    )
    assert first.content_bytes == second.content_bytes
    assert first.content_id.digest == second.content_id.digest


def test_a_content_identity_may_not_be_constructed_outside_the_encoder() -> None:
    with pytest.raises(CarrierFiberPreregistrationError):
        CarrierFiberSpecificationContentIdentity(
            algorithm="sha256",
            canonicalization_version="carrier-fiber-specification-manifest-v1",
            digest="0" * 64,
        )


def test_refreezing_a_changed_specification_under_one_identity_is_refused() -> None:
    registry = PreEvidenceCarrierFiberSpecificationRegistry()
    registry.freeze(FROZEN_CARRIER_FIBER_SPECIFICATION)
    changed = replace(FROZEN_CARRIER_FIBER_SPECIFICATION, resampling_count=17)
    with pytest.raises(CarrierFiberPreregistrationError):
        registry.freeze(changed)


def test_freezing_the_same_specification_twice_returns_the_same_manifest() -> None:
    registry = PreEvidenceCarrierFiberSpecificationRegistry()
    first = registry.freeze(FROZEN_CARRIER_FIBER_SPECIFICATION)
    second = registry.freeze(FROZEN_CARRIER_FIBER_SPECIFICATION)
    assert first is second


def test_a_binding_to_another_specification_content_is_refused() -> None:
    registry = PreEvidenceCarrierFiberSpecificationRegistry()
    frozen = registry.freeze(FROZEN_CARRIER_FIBER_SPECIFICATION)
    changed = replace(
        FROZEN_CARRIER_FIBER_SPECIFICATION,
        revision_id="r2",
        revision_sequence=1,
        resampling_count=11,
    )
    with pytest.raises(CarrierFiberPreregistrationError):
        CarrierFiberSpecificationContentBinding(
            specification=changed, frozen_manifest=frozen
        )


def test_the_declared_specification_freezes_and_binds() -> None:
    binding = freeze_declared_specification()
    assert binding.specification is FROZEN_CARRIER_FIBER_SPECIFICATION
    assert len(binding.content_id.digest) == 64


# --- ما لا تحسمه المواصفة، مكتوبٌ لا مطويّ ------------------------------------


def test_every_named_residual_is_keyed_by_its_own_name() -> None:
    for name, text in CARRIER_FIBER_PREREGISTRATION_NAMED_RESIDUALS.items():
        assert text.startswith(f"{name}:")


def test_no_specification_field_carries_a_measured_value() -> None:
    forbidden = ("observed", "result", "verdict", "p_value", "rank")
    for name in CanonicalCarrierFiberSpecificationEncoder.COVERAGE:
        assert not [marker for marker in forbidden if marker in name], name


# --- سلطة: هذه الوحدة خاملة في النواة -----------------------------------------


def test_no_kernel_module_reads_this_preregistration() -> None:
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
        assert "carrier_fiber_preregistration" not in text, module.name
        assert "StateSchema" not in text, module.name
