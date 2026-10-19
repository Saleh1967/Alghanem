"""اختباراتُ مختبرِ حامل–الحالة الكتابيِّ بالقوانين الثلاثة."""

from __future__ import annotations

import pytest

from alghanem.arabic.carrier_state_birth_experiment import (
    ACCEPTED_PROVENANCE_BY_CLAIM_KIND,
    CARRIER_STATE_BIRTH_NAMED_RESIDUALS,
    ORTHOGRAPHIC_TARGET_INSTRUMENT_ID,
    REPRESENTATION_INSTRUMENT_ID,
    REQUIRED_LAW_KEYS,
    REQUIRED_LAWS,
    BirthExperimentOutcome,
    CandidateRepresentation,
    CarrierStateBirthError,
    ClaimKind,
    ContainmentBlocker,
    ContextOutcome,
    ContextualLaw,
    DeferredPhoneticCarrierState,
    IndependentTarget,
    LawApplicationRow,
    LawRole,
    MeasuredAttribute,
    PerformanceWitness,
    StateAttribution,
    TargetProvenance,
    WeakerAlternative,
    WrittenCarrierGenus,
    assess_coverage,
    assess_kernel_containment,
    assess_necessity,
    deposited_performance_witnesses,
    run_birth_experiment_on_the_deposited_fatiha,
)
from alghanem.arabic.ibtida_wasl_waqf_registration import (
    THE_THREE_LAWS,
    LawStanding,
    SuppliedLaw,
)

IBTIDA = REQUIRED_LAWS[0]
WASL = REQUIRED_LAWS[1]
WAQF = REQUIRED_LAWS[2]


def _attribution(carrier: str, value: str) -> StateAttribution:
    return StateAttribution(
        genus=WrittenCarrierGenus(carrier=carrier),
        attribute=MeasuredAttribute(state_vector=(("الحركة", value),)),
    )


def _representation(
    pairs: tuple[tuple[str, StateAttribution], ...],
) -> CandidateRepresentation:
    return CandidateRepresentation(
        instrument_id=REPRESENTATION_INSTRUMENT_ID, attributions=pairs
    )


def _target(values: tuple[tuple[str, str], ...]) -> IndependentTarget:
    return IndependentTarget(
        law_key="الابتداء",
        claim_kind=ClaimKind.KITABIYYA,
        provenance=TargetProvenance.MAQIS_BI_ALA_MUNFASILA,
        instrument_id=ORTHOGRAPHIC_TARGET_INSTRUMENT_ID,
        values=values,
    )


# --- القوانينُ مرجعٌ لا دليل -------------------------------------------------


def test_the_three_required_laws_are_the_deposited_members_themselves() -> None:
    assert REQUIRED_LAW_KEYS == ("الابتداء", "الوصل", "الوقف")
    for law in REQUIRED_LAWS:
        assert any(law.law is member for member in THE_THREE_LAWS)


def test_importing_a_law_does_not_raise_its_standing() -> None:
    for law in REQUIRED_LAWS:
        assert law.law.standing is LawStanding.MUWRADA_BILA_MASDARIN_MUSAMMA


def test_a_copied_law_text_is_refused_because_it_is_not_the_deposited_member() -> None:
    copied = SuppliedLaw(
        key=THE_THREE_LAWS[0].key,
        statement=THE_THREE_LAWS[0].statement,
        formal_text=THE_THREE_LAWS[0].formal_text,
        standing=LawStanding.MUWRADA_BILA_MASDARIN_MUSAMMA,
    )
    with pytest.raises(CarrierStateBirthError):
        ContextualLaw(
            law=copied,
            role=LawRole.TANZIM_AL_DUKHUL,
            domain_note="مجال",
            condition_note="شرط",
            cause_note="سبب",
            blocker_note="مانع",
        )


def test_the_three_laws_carry_entry_transition_and_closure_roles() -> None:
    assert IBTIDA.role is LawRole.TANZIM_AL_DUKHUL
    assert WASL.role is LawRole.TANZIM_AL_INTIQAL
    assert WAQF.role is LawRole.TANZIM_AL_IGHLAQ


# --- الحارسُ الثاني: الإسنادُ سابقٌ للمقطع ----------------------------------


def test_the_attribution_admits_only_a_written_carrier_and_a_measured_state() -> None:
    with pytest.raises(CarrierStateBirthError):
        StateAttribution(
            genus="ب",  # type: ignore[arg-type]
            attribute=MeasuredAttribute(state_vector=(("الحركة", "فتحة"),)),
        )
    with pytest.raises(CarrierStateBirthError):
        StateAttribution(
            genus=WrittenCarrierGenus(carrier="ب"),
            attribute="مبتدأ",  # type: ignore[arg-type]
        )


def test_the_attribution_exposes_no_predicate_field_at_all() -> None:
    attribution = _attribution("ب", "فتحة")
    assert not hasattr(attribution, "predicate")
    assert not hasattr(attribution, "gloss")
    assert attribution.output == ("ب", (("الحركة", "فتحة"),))


# --- الحارسُ الأوّل: لا اجتيازَ على مجالٍ فقير -------------------------------


def test_an_empty_domain_is_deferred_and_never_passes() -> None:
    decision = assess_kernel_containment(
        IBTIDA, _representation((("أ", _attribution("ب", "فتحة")),)), _target(())
    )
    assert decision.outcome is ContextOutcome.IRJA
    assert decision.blocker is ContainmentBlocker.LA_WUQUAT_FI_AL_MAJAL


def test_a_domain_with_a_constant_target_is_deferred_not_passed() -> None:
    representation = _representation(
        (("أ", _attribution("ب", "فتحة")), ("ب", _attribution("ت", "ضمّة")))
    )
    decision = assess_kernel_containment(
        IBTIDA, representation, _target((("أ", "واحد"), ("ب", "واحد")))
    )
    assert decision.outcome is ContextOutcome.IRJA
    assert decision.blocker is ContainmentBlocker.LA_ZAWJ_YUFARRIQUH_AL_HADAF
    assert decision.discriminating_pairs == 0


def test_a_pass_records_the_width_of_its_discriminating_pairs() -> None:
    representation = _representation(
        (("أ", _attribution("ب", "فتحة")), ("ب", _attribution("ت", "ضمّة")))
    )
    decision = assess_kernel_containment(
        IBTIDA, representation, _target((("أ", "واحد"), ("ب", "اثنان")))
    )
    assert decision.outcome is ContextOutcome.IJTIYAZ
    assert decision.discriminating_pairs == 1
    assert decision.passed_pairs == 1
    assert "لا يُعمَّم على كلّ نموذجٍ ممكن" in decision.scope_note


def test_a_merged_pair_that_the_target_separates_is_a_recorded_refutation() -> None:
    representation = _representation(
        (("أ", _attribution("ب", "فتحة")), ("ب", _attribution("ب", "فتحة")))
    )
    decision = assess_kernel_containment(
        IBTIDA, representation, _target((("أ", "واحد"), ("ب", "اثنان")))
    )
    assert decision.outcome is ContextOutcome.NAQD
    assert decision.merge_witnesses[0].first_context == "أ"
    assert decision.passed_pairs == 0


# --- استقلالُ الهدف بحسب نوع الدعوى -----------------------------------------


def test_a_target_whose_provenance_is_the_representation_itself_is_refused() -> None:
    with pytest.raises(CarrierStateBirthError):
        IndependentTarget(
            law_key="الابتداء",
            claim_kind=ClaimKind.KITABIYYA,
            provenance=TargetProvenance.AL_TAMTHIL_NAFSUH,
            instrument_id="x",
            values=(),
        )


def test_a_target_measured_by_the_in_tree_syllabifier_is_refused() -> None:
    with pytest.raises(CarrierStateBirthError):
        IndependentTarget(
            law_key="الابتداء",
            claim_kind=ClaimKind.KITABIYYA,
            provenance=TargetProvenance.AL_MUQATTI_FI_AL_SHAJARA,
            instrument_id="x",
            values=(),
        )


def test_an_orthographic_target_does_not_need_a_gloss_registry() -> None:
    assert (
        ACCEPTED_PROVENANCE_BY_CLAIM_KIND[ClaimKind.KITABIYYA]
        is TargetProvenance.MAQIS_BI_ALA_MUNFASILA
    )
    assert (
        ACCEPTED_PROVENANCE_BY_CLAIM_KIND[ClaimKind.DALALIYYA]
        is TargetProvenance.WASM_MUSTAQILL
    )


def test_a_phonetic_claim_may_not_be_carried_by_a_measured_orthographic_target() -> (
    None
):
    with pytest.raises(CarrierStateBirthError):
        IndependentTarget(
            law_key="الابتداء",
            claim_kind=ClaimKind.SAWTIYYA,
            provenance=TargetProvenance.MAQIS_BI_ALA_MUNFASILA,
            instrument_id="x",
            values=(),
        )


def test_a_target_measured_by_the_representation_instrument_is_not_independent() -> (
    None
):
    target = IndependentTarget(
        law_key="الابتداء",
        claim_kind=ClaimKind.KITABIYYA,
        provenance=TargetProvenance.MAQIS_BI_ALA_MUNFASILA,
        instrument_id=REPRESENTATION_INSTRUMENT_ID,
        values=(("أ", "واحد"),),
    )
    with pytest.raises(CarrierStateBirthError):
        assess_kernel_containment(
            IBTIDA, _representation((("أ", _attribution("ب", "فتحة")),)), target
        )


# --- صفُّ التطبيق كاملُ الحقول ------------------------------------------------


def test_an_application_row_without_a_site_of_change_is_refused() -> None:
    with pytest.raises(CarrierStateBirthError):
        LawApplicationRow(
            law_key="الابتداء",
            context_id="٠:٠",
            entry_state="دخول",
            exit_state="خروج",
            site_of_change="   ",
            preserved_invariant="الهوية",
            discriminating_difference="فرق",
            effect_note="أثر",
            evidence_id="دليل",
            residue_note="بقيّة",
        )


def test_an_application_row_without_a_preserved_invariant_is_refused() -> None:
    with pytest.raises(CarrierStateBirthError):
        LawApplicationRow(
            law_key="الابتداء",
            context_id="٠:٠",
            entry_state="دخول",
            exit_state="خروج",
            site_of_change="محل",
            preserved_invariant="",
            discriminating_difference="فرق",
            effect_note="أثر",
            evidence_id="دليل",
            residue_note="بقيّة",
        )


# --- الاكتمالُ مشروطٌ بالتغطية ------------------------------------------------


def test_coverage_requires_a_decision_for_every_required_law() -> None:
    decision = assess_kernel_containment(IBTIDA, _representation(()), None)
    with pytest.raises(CarrierStateBirthError):
        assess_coverage((decision,))


def test_one_law_passing_while_two_are_deferred_yields_an_overall_defer() -> None:
    representation = _representation(
        (("أ", _attribution("ب", "فتحة")), ("ب", _attribution("ت", "ضمّة")))
    )
    passed = assess_kernel_containment(
        IBTIDA, representation, _target((("أ", "واحد"), ("ب", "اثنان")))
    )
    coverage = assess_coverage(
        (
            passed,
            assess_kernel_containment(WASL, representation, None),
            assess_kernel_containment(WAQF, representation, None),
        )
    )
    assert passed.outcome is ContextOutcome.IJTIYAZ
    assert coverage.overall is ContextOutcome.IRJA
    assert coverage.is_complete is False
    assert coverage.deferred_laws == ("الوصل", "الوقف")
    assert coverage.laws_with_witnesses == ("الابتداء",)


def test_a_refutation_outranks_a_deferral_in_the_aggregate() -> None:
    representation = _representation(
        (("أ", _attribution("ب", "فتحة")), ("ب", _attribution("ب", "فتحة")))
    )
    refuted = assess_kernel_containment(
        IBTIDA, representation, _target((("أ", "واحد"), ("ب", "اثنان")))
    )
    coverage = assess_coverage(
        (
            refuted,
            assess_kernel_containment(WASL, representation, None),
            assess_kernel_containment(WAQF, representation, None),
        )
    )
    assert coverage.overall is ContextOutcome.NAQD
    assert coverage.failed_laws == ("الابتداء",)


# --- ضرورةُ المعلومة تُشغَّل ولا تُفترَض ------------------------------------


def test_a_weaker_alternative_that_passes_shows_the_dropped_part_is_needless() -> None:
    representation = _representation(
        (("أ", _attribution("ب", "فتحة")), ("ب", _attribution("ت", "فتحة")))
    )
    decisions = assess_necessity(
        IBTIDA, representation, _target((("أ", "واحد"), ("ب", "اثنان")))
    )
    by_alternative = {decision.alternative: decision for decision in decisions}
    genus_only = by_alternative[WeakerAlternative.AL_JINS_WAHDAH]
    attribute_only = by_alternative[WeakerAlternative.AL_SIFA_WAHDAHA]
    assert genus_only.outcome is ContextOutcome.IJTIYAZ
    assert genus_only.information_is_necessary is False
    assert attribute_only.outcome is ContextOutcome.NAQD
    assert attribute_only.information_is_necessary is True


def test_a_deferred_alternative_says_nothing_about_necessity() -> None:
    decisions = assess_necessity(WASL, _representation(()), None)
    for decision in decisions:
        assert decision.outcome is ContextOutcome.IRJA
        assert decision.information_is_necessary is None


# --- المخرجاتُ الثلاثةُ مفصولةٌ في النوع -------------------------------------


def test_no_performance_witness_is_deposited_so_the_phonetic_output_is_deferred() -> (
    None
):
    assert deposited_performance_witnesses() == ()


def test_the_phonetic_output_refuses_anything_that_is_not_a_performance_witness() -> (
    None
):
    with pytest.raises(CarrierStateBirthError):
        DeferredPhoneticCarrierState(witness="الرسمُ يدلّ")  # type: ignore[arg-type]


def test_a_performance_witness_needs_a_named_reading_dialect_and_context() -> None:
    with pytest.raises(CarrierStateBirthError):
        PerformanceWitness(
            witness_id="شاهد",
            reading="",
            dialect="لهجة",
            context="سياق",
            source_sha256="0" * 64,
        )


# --- التشغيلُ على النصّ المُودَع ----------------------------------------------


def test_the_deposited_run_passes_ibtida_and_defers_wasl_and_waqf() -> None:
    outcome = run_birth_experiment_on_the_deposited_fatiha()
    coverage = outcome.orthographic_candidate.coverage
    ibtida = coverage.decision_for("الابتداء")
    assert ibtida.outcome is ContextOutcome.IJTIYAZ
    assert ibtida.discriminating_pairs > 0
    for key in ("الوصل", "الوقف"):
        deferred = coverage.decision_for(key)
        assert deferred.outcome is ContextOutcome.IRJA
        assert deferred.blocker is ContainmentBlocker.LA_HADAF_MUSTAQILL
    assert coverage.overall is ContextOutcome.IRJA
    assert coverage.is_complete is False


def test_the_deposited_run_separates_the_three_outputs_without_a_promotion_path() -> (
    None
):
    outcome = run_birth_experiment_on_the_deposited_fatiha()
    assert isinstance(outcome, BirthExperimentOutcome)
    assert outcome.orthographic_candidate.is_born is False
    assert outcome.orthographic_candidate.carries_a_complete_certificate is False
    assert outcome.phonetic_carrier_state is None
    assert outcome.phonetic_deferral_reason.startswith(
        "NO_PERFORMANCE_WITNESS_IS_DEPOSITED"
    )
    assert outcome.syllable.certificate_issued is False
    assert outcome.certificate_issuance_is_delegated is True
    assert outcome.grants_authority_to_the_syllable_or_the_syntax is False


def test_every_application_row_on_the_deposited_text_is_field_complete() -> None:
    outcome = run_birth_experiment_on_the_deposited_fatiha()
    rows = outcome.orthographic_candidate.applications
    assert rows
    for row in rows:
        assert row.law_key == "الابتداء"
        assert row.site_of_change.strip()
        assert row.preserved_invariant.strip()
        assert row.evidence_id.startswith(ORTHOGRAPHIC_TARGET_INSTRUMENT_ID)


def test_the_deposited_run_records_that_a_weaker_alternative_also_passes() -> None:
    outcome = run_birth_experiment_on_the_deposited_fatiha()
    ibtida_necessity = [
        decision
        for decision in outcome.orthographic_candidate.necessity
        if decision.law_key == "الابتداء"
    ]
    assert {decision.outcome for decision in ibtida_necessity} == {
        ContextOutcome.IJTIYAZ
    }
    assert all(
        decision.information_is_necessary is False for decision in ibtida_necessity
    )


# --- البقايا المُسمّاة ---------------------------------------------------------


def test_there_are_twelve_named_residuals_all_distinct_and_non_blank() -> None:
    assert len(CARRIER_STATE_BIRTH_NAMED_RESIDUALS) == 12
    for name, text in CARRIER_STATE_BIRTH_NAMED_RESIDUALS.items():
        assert text.startswith(f"{name}:")
        assert text.strip()
    assert len(set(CARRIER_STATE_BIRTH_NAMED_RESIDUALS.values())) == 12
