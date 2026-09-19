"""اختباراتُ عقد الهمزة: أربعةُ حقولٍ مفصولة، وحكمان مقيسان لا مكتوبان."""

from __future__ import annotations

from pathlib import Path

import pytest

from alghanem.arabic import hamza_contract
from alghanem.arabic.hamza_contract import (
    HAMZA_CONTRACT_NAMED_RESIDUALS,
    THE_DECLARED_OCCURRENCES,
    CodecSeparationReport,
    ComponentAssessment,
    ContractField,
    DerivabilityStanding,
    HamzaContractError,
    HamzaFunction,
    HamzaIdentity,
    HamzaOccurrence,
    HamzaRealization,
    HamzaSeat,
    NecessityStanding,
    alif_neutrality_may_close_syllable_birth,
    assess_contract_fields,
    assess_field,
    codec_projection,
    contract_projection,
    delete_field,
    measure_codec_separation,
    seat_read_by_the_codec,
)
from alghanem.import_boundary import ImportBoundaryPolicy, audit_import_boundary


def _qat_on_alef(content: str = "مضمونٌ مكتوب") -> HamzaOccurrence:
    return HamzaOccurrence(
        surface="\u0623",
        index=0,
        identity=HamzaIdentity.HAMZA,
        seat=HamzaSeat.ON_ALEF,
        function=HamzaFunction.QAT,
        realization=HamzaRealization.REALIZED,
        context="مقامٌ مكتوب",
        declared_source="إعلانُ الاختبار",
        content=content,
    )


def test_the_hamza_contract_module_reaches_no_kernel_module() -> None:
    report = audit_import_boundary(
        (Path(str(hamza_contract.__file__)),),
        ImportBoundaryPolicy(
            policy_id="hamza-contract",
            permitted_modules=(),
            forbidden_packages=("alghanem.kernel",),
        ),
    )
    assert not [
        name for name in report.reached_modules if name.startswith("alghanem.kernel")
    ]


def test_the_module_exports_no_refine_or_split_authority() -> None:
    assert not hasattr(hamza_contract, "RefineSlot")
    for name in hamza_contract.__all__:
        assert "refine" not in name.lower()
        assert "split" not in name.lower()


def test_there_are_nine_named_residuals_all_distinct_and_non_blank() -> None:
    assert len(HAMZA_CONTRACT_NAMED_RESIDUALS) == 9
    assert len(set(HAMZA_CONTRACT_NAMED_RESIDUALS)) == 9
    assert all(note.strip() for note in HAMZA_CONTRACT_NAMED_RESIDUALS)


def test_the_four_fields_are_four_and_separate() -> None:
    assert len(ContractField) == len(set(ContractField))
    assert len(contract_projection(_qat_on_alef())) == len(ContractField)


# --- الكرسيُّ مفحوصٌ لا مُصدَّق ------------------------------------------------


@pytest.mark.parametrize(
    ("surface", "expected"),
    [
        ("\u0623", HamzaSeat.ON_ALEF),
        ("\u0625", HamzaSeat.ON_ALEF_KASRA),
        ("\u0624", HamzaSeat.ON_WAW),
        ("\u0626", HamzaSeat.ON_YEH),
        ("\u0622", HamzaSeat.ON_ALEF_MADDA),
        ("\u0621", HamzaSeat.BARE),
        ("\u0627", HamzaSeat.NO_HAMZA_SEAT),
        ("\u0671", HamzaSeat.NO_HAMZA_SEAT),
    ],
)
def test_the_seat_is_read_by_running_the_codec(
    surface: str, expected: HamzaSeat
) -> None:
    assert seat_read_by_the_codec(surface, 0) is expected


def test_a_seat_that_contradicts_the_codec_is_refused() -> None:
    with pytest.raises(HamzaContractError):
        HamzaOccurrence(
            surface="\u0623",
            index=0,
            identity=HamzaIdentity.HAMZA,
            seat=HamzaSeat.ON_WAW,
            function=HamzaFunction.QAT,
            realization=HamzaRealization.REALIZED,
            context="مقامٌ مكتوب",
            declared_source="إعلانُ الاختبار",
            content="مضمون",
        )


def test_an_index_outside_the_surface_is_refused() -> None:
    with pytest.raises(HamzaContractError):
        seat_read_by_the_codec("\u0623", 4)


@pytest.mark.parametrize("blank", ["", "   "])
def test_an_occurrence_without_a_written_context_is_refused(blank: str) -> None:
    with pytest.raises(HamzaContractError):
        HamzaOccurrence(
            surface="\u0623",
            index=0,
            identity=HamzaIdentity.HAMZA,
            seat=HamzaSeat.ON_ALEF,
            function=HamzaFunction.QAT,
            realization=HamzaRealization.REALIZED,
            context=blank,
            declared_source="إعلانُ الاختبار",
            content="مضمون",
        )


def test_an_occurrence_without_a_declared_source_is_refused() -> None:
    with pytest.raises(HamzaContractError):
        HamzaOccurrence(
            surface="\u0623",
            index=0,
            identity=HamzaIdentity.HAMZA,
            seat=HamzaSeat.ON_ALEF,
            function=HamzaFunction.QAT,
            realization=HamzaRealization.REALIZED,
            context="مقامٌ مكتوب",
            declared_source=" ",
            content="مضمون",
        )


def test_an_occurrence_without_content_is_refused() -> None:
    with pytest.raises(HamzaContractError):
        HamzaOccurrence(
            surface="\u0623",
            index=0,
            identity=HamzaIdentity.HAMZA,
            seat=HamzaSeat.ON_ALEF,
            function=HamzaFunction.QAT,
            realization=HamzaRealization.REALIZED,
            context="مقامٌ مكتوب",
            declared_source="إعلانُ الاختبار",
            content="",
        )


# --- التوليفاتُ الممنوعةُ بنيويًّا ---------------------------------------------


def test_what_is_not_a_hamza_may_not_carry_a_hamza_function() -> None:
    with pytest.raises(HamzaContractError):
        HamzaOccurrence(
            surface="\u0627",
            index=0,
            identity=HamzaIdentity.NOT_A_HAMZA,
            seat=HamzaSeat.NO_HAMZA_SEAT,
            function=HamzaFunction.QAT,
            realization=HamzaRealization.NOT_A_HAMZA_REALIZATION,
            context="مقامٌ مكتوب",
            declared_source="إعلانُ الاختبار",
            content="مضمون",
        )


def test_what_is_not_a_hamza_may_not_carry_a_hamza_realization() -> None:
    with pytest.raises(HamzaContractError):
        HamzaOccurrence(
            surface="\u0627",
            index=0,
            identity=HamzaIdentity.NOT_A_HAMZA,
            seat=HamzaSeat.NO_HAMZA_SEAT,
            function=HamzaFunction.NO_HAMZA_FUNCTION,
            realization=HamzaRealization.REALIZED,
            context="مقامٌ مكتوب",
            declared_source="إعلانُ الاختبار",
            content="مضمون",
        )


def test_a_hamza_without_a_declared_function_is_refused() -> None:
    with pytest.raises(HamzaContractError):
        HamzaOccurrence(
            surface="\u0623",
            index=0,
            identity=HamzaIdentity.HAMZA,
            seat=HamzaSeat.ON_ALEF,
            function=HamzaFunction.NO_HAMZA_FUNCTION,
            realization=HamzaRealization.REALIZED,
            context="مقامٌ مكتوب",
            declared_source="إعلانُ الاختبار",
            content="مضمون",
        )


def test_a_hamza_without_a_declared_realization_is_refused() -> None:
    with pytest.raises(HamzaContractError):
        HamzaOccurrence(
            surface="\u0623",
            index=0,
            identity=HamzaIdentity.HAMZA,
            seat=HamzaSeat.ON_ALEF,
            function=HamzaFunction.QAT,
            realization=HamzaRealization.NOT_A_HAMZA_REALIZATION,
            context="مقامٌ مكتوب",
            declared_source="إعلانُ الاختبار",
            content="مضمون",
        )


def test_wasl_may_not_sit_on_a_written_hamza_seat() -> None:
    with pytest.raises(HamzaContractError):
        HamzaOccurrence(
            surface="\u0623",
            index=0,
            identity=HamzaIdentity.HAMZA,
            seat=HamzaSeat.ON_ALEF,
            function=HamzaFunction.WASL,
            realization=HamzaRealization.ELIDED_IN_WASL,
            context="مقامٌ مكتوب",
            declared_source="إعلانُ الاختبار",
            content="مضمون",
        )


def test_wasl_may_not_be_fully_realized_in_every_context() -> None:
    with pytest.raises(HamzaContractError):
        HamzaOccurrence(
            surface="\u0627",
            index=0,
            identity=HamzaIdentity.HAMZA,
            seat=HamzaSeat.NO_HAMZA_SEAT,
            function=HamzaFunction.WASL,
            realization=HamzaRealization.REALIZED,
            context="مقامٌ مكتوب",
            declared_source="إعلانُ الاختبار",
            content="مضمون",
        )


def test_qat_may_not_be_elided_in_wasl() -> None:
    with pytest.raises(HamzaContractError):
        HamzaOccurrence(
            surface="\u0623",
            index=0,
            identity=HamzaIdentity.HAMZA,
            seat=HamzaSeat.ON_ALEF,
            function=HamzaFunction.QAT,
            realization=HamzaRealization.ELIDED_IN_WASL,
            context="مقامٌ مكتوب",
            declared_source="إعلانُ الاختبار",
            content="مضمون",
        )


def test_lengthening_without_the_madda_seat_is_refused() -> None:
    with pytest.raises(HamzaContractError):
        HamzaOccurrence(
            surface="\u0623",
            index=0,
            identity=HamzaIdentity.HAMZA,
            seat=HamzaSeat.ON_ALEF,
            function=HamzaFunction.QAT,
            realization=HamzaRealization.LENGTHENED,
            context="مقامٌ مكتوب",
            declared_source="إعلانُ الاختبار",
            content="مضمون",
        )


def test_the_madda_seat_without_lengthening_is_refused() -> None:
    with pytest.raises(HamzaContractError):
        HamzaOccurrence(
            surface="\u0622",
            index=0,
            identity=HamzaIdentity.HAMZA,
            seat=HamzaSeat.ON_ALEF_MADDA,
            function=HamzaFunction.QAT,
            realization=HamzaRealization.REALIZED,
            context="مقامٌ مكتوب",
            declared_source="إعلانُ الاختبار",
            content="مضمون",
        )


def test_no_occurrence_claims_to_be_a_complete_phonetic_description() -> None:
    assert all(
        not item.is_a_complete_phonetic_description for item in THE_DECLARED_OCCURRENCES
    )


# --- الحذفُ والاختباران -------------------------------------------------------


@pytest.mark.parametrize("field", list(ContractField))
def test_deleting_a_field_drops_exactly_that_field(field: ContractField) -> None:
    occurrence = _qat_on_alef()
    full = contract_projection(occurrence)
    deleted = delete_field(occurrence, field)
    assert len(deleted) == len(full)
    assert sum(1 for value in deleted if value is None) == 1
    kept = [pair for pair in zip(full, deleted) if pair[1] is not None]
    assert all(left == right for left, right in kept)


def test_deleting_an_unnamed_field_is_refused() -> None:
    with pytest.raises(HamzaContractError):
        delete_field(_qat_on_alef(), "الكرسيّ")  # type: ignore[arg-type]


def test_an_empty_domain_proves_nothing() -> None:
    with pytest.raises(HamzaContractError):
        assess_field(ContractField.SEAT, ())
    with pytest.raises(HamzaContractError):
        measure_codec_separation(())


def test_assessing_an_unnamed_field_is_refused() -> None:
    with pytest.raises(HamzaContractError):
        assess_field("الكرسيّ", THE_DECLARED_OCCURRENCES)  # type: ignore[arg-type]


def test_every_field_is_assessed_and_none_is_omitted() -> None:
    assessments = assess_contract_fields(THE_DECLARED_OCCURRENCES)
    assert len(assessments) == len(ContractField)
    assert {item.field for item in assessments} == set(ContractField)
    assert all(isinstance(item, ComponentAssessment) for item in assessments)


def _assessment_of(field: ContractField) -> ComponentAssessment:
    return assess_field(field, THE_DECLARED_OCCURRENCES)


def test_the_seat_is_necessary_and_not_determined_on_this_domain() -> None:
    seat = _assessment_of(ContractField.SEAT)
    assert seat.necessity is NecessityStanding.NECESSARY_ON_THIS_DOMAIN
    assert seat.derivability is DerivabilityStanding.NOT_DETERMINED_BY_THE_OTHER_FIELDS
    assert seat.a_separate_field_is_required


def test_the_realization_is_necessary_and_not_determined_on_this_domain() -> None:
    realization = _assessment_of(ContractField.REALIZATION)
    assert realization.necessity is NecessityStanding.NECESSARY_ON_THIS_DOMAIN
    assert realization.a_separate_field_is_required
    assert realization.merged_contents


def test_necessity_is_read_from_merged_contents_not_declared() -> None:
    for assessment in assess_contract_fields(THE_DECLARED_OCCURRENCES):
        assert (
            bool(assessment.merged_contents) == assessment.the_information_is_required
        )
        assert all(len(row) > 1 for row in assessment.merged_contents)


def test_determination_is_read_from_undetermined_rows_not_declared() -> None:
    for assessment in assess_contract_fields(THE_DECLARED_OCCURRENCES):
        determined = (
            assessment.derivability
            is DerivabilityStanding.DETERMINED_BY_THE_OTHER_FIELDS
        )
        assert determined == (not assessment.undetermined_values)


def test_a_determined_field_needs_no_separate_field_even_if_informative() -> None:
    for assessment in assess_contract_fields(THE_DECLARED_OCCURRENCES):
        if (
            assessment.derivability
            is DerivabilityStanding.DETERMINED_BY_THE_OTHER_FIELDS
        ):
            assert not assessment.a_separate_field_is_required


def test_a_field_that_merges_nothing_on_a_single_case_is_not_shown_necessary() -> None:
    lone = (_qat_on_alef(),)
    for field in ContractField:
        assessment = assess_field(field, lone)
        assert (
            assessment.necessity is NecessityStanding.NOT_SHOWN_NECESSARY_ON_THIS_DOMAIN
        )
        assert not assessment.merged_contents


def test_two_cases_sharing_a_deletion_but_not_a_content_prove_necessity() -> None:
    pair = (
        _qat_on_alef("همزةُ قطعٍ في أوّل الكلمة"),
        HamzaOccurrence(
            surface="\u0624",
            index=0,
            identity=HamzaIdentity.HAMZA,
            seat=HamzaSeat.ON_WAW,
            function=HamzaFunction.QAT,
            realization=HamzaRealization.REALIZED,
            context="مقامٌ مكتوب",
            declared_source="إعلانُ الاختبار",
            content="همزةُ قطعٍ في وسط الكلمة",
        ),
    )
    assessment = assess_field(ContractField.SEAT, pair)
    assert assessment.necessity is NecessityStanding.NECESSARY_ON_THIS_DOMAIN
    assert assessment.merged_contents == (
        ("همزةُ قطعٍ في أوّل الكلمة", "همزةُ قطعٍ في وسط الكلمة"),
    )


# --- المِرمازُ: ما حفظه وما دمجه ----------------------------------------------


def test_the_codec_projection_carries_only_a_carrier_and_a_seat() -> None:
    assert len(codec_projection(_qat_on_alef())) == 2


def test_the_codec_keeps_some_rasm_differences() -> None:
    report = measure_codec_separation(THE_DECLARED_OCCURRENCES)
    assert isinstance(report, CodecSeparationReport)
    assert report.the_codec_keeps_some_rasm_differences
    assert len(report.seat_differences_kept) > 1


def test_the_codec_merges_occurrences_that_differ_in_function_or_realization() -> None:
    report = measure_codec_separation(THE_DECLARED_OCCURRENCES)
    assert report.merged_by_the_codec
    assert not report.the_codec_is_a_complete_phonetic_fiber
    assert report.distinct_codec_outputs < report.distinct_contract_outputs


def test_the_merged_rows_carry_their_contents_not_a_rate() -> None:
    report = measure_codec_separation(THE_DECLARED_OCCURRENCES)
    for row in report.merged_by_the_codec:
        assert len(row) > 1
        assert all(text.strip() for text in row)


def test_the_wasl_alef_and_the_madd_alef_are_among_the_merged() -> None:
    report = measure_codec_separation(THE_DECLARED_OCCURRENCES)
    merged = {text for row in report.merged_by_the_codec for text in row}
    wasl = {
        item.content
        for item in THE_DECLARED_OCCURRENCES
        if item.function is HamzaFunction.WASL
    }
    not_a_hamza = {
        item.content
        for item in THE_DECLARED_OCCURRENCES
        if item.identity is HamzaIdentity.NOT_A_HAMZA
    }
    assert wasl <= merged
    assert not_a_hamza <= merged


def test_the_declared_domain_is_written_and_every_case_is_checked() -> None:
    assert len(THE_DECLARED_OCCURRENCES) > 1
    assert all(item.context.strip() for item in THE_DECLARED_OCCURRENCES)
    assert all(item.declared_source.strip() for item in THE_DECLARED_OCCURRENCES)
    assert {item.seat for item in THE_DECLARED_OCCURRENCES} == set(HamzaSeat)


def test_alif_neutrality_may_not_close_syllable_birth() -> None:
    assert not alif_neutrality_may_close_syllable_birth()
