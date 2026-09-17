"""اختباراتُ تعديل G0.VV-BIRTH-1A: إغلاقُ التنفيذ دون المساس بالأب المختوم."""

from __future__ import annotations

import importlib.util
from dataclasses import fields, replace
from pathlib import Path

import pytest

from alghanem.arabic.vv_birth_amendment import (
    ADVERSARIAL_EXTENSION_OPERATORS,
    AMENDMENT_DIGEST,
    AMENDMENT_ID,
    CONTEXT_SET_K0,
    EXTENSION_COUNT_AMENDMENT,
    EXTENSION_OPERATOR_SPECIFICATION,
    FORBIDDEN_TRACE_CONTENT,
    IDENTITY_PROJECTION_FORBIDDEN_PROVENANCE,
    REQUIRED_AMENDMENT_SITES,
    SUPERSEDED_PREREGISTRATION_PARENT,
    TRACE_FIELD_SPECIFICATIONS,
    TYPE_DISTINCTION_LAW,
    VV_BIRTH_AMENDMENT_NAMED_RESIDUALS,
    WEAKER_MODEL_IMPLEMENTATIONS,
    AdversarialOperator,
    AmendmentOutcome,
    ContextK0,
    ExtensionCountAmendment,
    ExtensionOperatorSpecification,
    InputField,
    OperatorClass,
    ProvenanceClass,
    SupersededPreregistrationParent,
    TraceFieldSpecification,
    TypeDistinctionLaw,
    VvBirthAmendmentError,
    adversarial_operator_named,
    amendment_digest,
    identity_projection_refuses,
    missing_amendment_sites,
    readout_module_is_absent,
    trace_projections_of,
    weaker_model_implementation_named,
)
from alghanem.arabic.vv_birth_hypothesis import (
    BANNED_IDENTITY_PROXIES,
    HypothesisIdentifier,
)
from alghanem.arabic.vv_birth_preregistration import (
    PREREGISTRATION_DIGEST,
    READOUT_MODULE_NAME,
)

_SOURCE_ROOT = Path(__file__).resolve().parents[2] / "src" / "alghanem"
_BASE_COMMIT_SHA = "a2652ad5de68a69e77a99722e6715ab747468042"


class TestTheParentIsNotTouched:
    def test_the_base_commit_sha_is_carried_verbatim(self) -> None:
        assert SUPERSEDED_PREREGISTRATION_PARENT.commit_sha == _BASE_COMMIT_SHA

    def test_the_base_content_digest_still_matches_the_living_module(self) -> None:
        assert SUPERSEDED_PREREGISTRATION_PARENT.content_digest == (
            PREREGISTRATION_DIGEST
        )

    def test_every_hypothesis_is_preserved_not_superseded(self) -> None:
        assert set(SUPERSEDED_PREREGISTRATION_PARENT.preserved_hypotheses) == set(
            HypothesisIdentifier
        )

    def test_dropping_a_hypothesis_is_refused(self) -> None:
        with pytest.raises(VvBirthAmendmentError):
            replace(
                SUPERSEDED_PREREGISTRATION_PARENT,
                preserved_hypotheses=(HypothesisIdentifier.H_E,),
            )

    def test_a_malformed_commit_sha_is_refused(self) -> None:
        for bad in ("", "abc", _BASE_COMMIT_SHA.upper(), "z" * 40):
            with pytest.raises(VvBirthAmendmentError):
                replace(SUPERSEDED_PREREGISTRATION_PARENT, commit_sha=bad)

    def test_a_digest_that_no_longer_matches_is_refused(self) -> None:
        with pytest.raises(VvBirthAmendmentError):
            SupersededPreregistrationParent(
                commit_sha=_BASE_COMMIT_SHA,
                content_digest="0" * 63,
                what_is_superseded="تنفيذٌ مفترض",
                what_is_preserved="فرضياتٌ مفترضة",
                preserved_hypotheses=tuple(HypothesisIdentifier),
            )

    def test_the_amendment_adds_outcomes_in_its_own_vocabulary(self) -> None:
        from alghanem.arabic.vv_birth_hypothesis import ExperimentOutcome

        sealed = {outcome.value for outcome in ExperimentOutcome}
        assert "REPRESENTATION_TAUTOLOGY" not in sealed
        assert "DISTINGUISHED_ON_K0" not in sealed
        assert "BORN" not in {outcome.value for outcome in AmendmentOutcome}

    def test_the_parent_modules_are_byte_identical_to_the_base_commit(self) -> None:
        import subprocess

        repository = _SOURCE_ROOT.parents[1]
        for name in ("vv_birth_hypothesis.py", "vv_birth_preregistration.py"):
            relative = f"src/alghanem/arabic/{name}"
            sealed = subprocess.run(
                ["git", "show", f"{_BASE_COMMIT_SHA}:{relative}"],
                cwd=repository,
                capture_output=True,
                check=True,
            ).stdout
            assert sealed
            assert sealed == (repository / relative).read_bytes(), name


class TestTheExtensionOperatorIsFrozenOperationally:
    def test_it_declares_all_six_execution_facets(self) -> None:
        spec = EXTENSION_OPERATOR_SPECIFICATION
        assert spec.allowed_inputs
        assert spec.forbidden_sources
        assert spec.domain_predicate.strip()
        assert len(spec.transformation_rule) >= 4
        assert spec.undefinedness_conditions
        assert spec.output_invariants

    def test_an_operator_with_no_declared_inputs_is_refused(self) -> None:
        with pytest.raises(VvBirthAmendmentError):
            replace(EXTENSION_OPERATOR_SPECIFICATION, allowed_inputs=())

    def test_an_operator_with_no_undefinedness_is_refused(self) -> None:
        with pytest.raises(VvBirthAmendmentError):
            replace(EXTENSION_OPERATOR_SPECIFICATION, undefinedness_conditions=())

    def test_the_madd_label_is_named_as_a_forbidden_source(self) -> None:
        joined = " ".join(EXTENSION_OPERATOR_SPECIFICATION.forbidden_sources)
        assert "MADD_EXTENSION" in joined
        assert "syllabifier" in joined

    def test_a_model_output_input_is_refused(self) -> None:
        leaked = InputField(
            name="predicted_role",
            provenance=ProvenanceClass.MODEL_OUTPUT,
            what_it_carries="دورًا تنبّأ به النموذجُ المرشَّح",
        )
        with pytest.raises(VvBirthAmendmentError):
            replace(
                EXTENSION_OPERATOR_SPECIFICATION,
                allowed_inputs=(
                    EXTENSION_OPERATOR_SPECIFICATION.allowed_inputs + (leaked,)
                ),
            )

    def test_reading_orthography_forces_the_orthographic_class(self) -> None:
        assert EXTENSION_OPERATOR_SPECIFICATION.operator_class is (
            OperatorClass.ORTHOGRAPHIC_EXTENSION_OPERATOR
        )
        with pytest.raises(VvBirthAmendmentError):
            replace(
                EXTENSION_OPERATOR_SPECIFICATION,
                operator_class=OperatorClass.STATE_ONLY_EXTENSION_OPERATOR,
            )

    def test_a_state_only_operator_is_allowed_when_it_reads_no_orthography(
        self,
    ) -> None:
        spec = ExtensionOperatorSpecification(
            operator_name="E_state_only",
            operator_class=OperatorClass.STATE_ONLY_EXTENSION_OPERATOR,
            allowed_inputs=(EXTENSION_OPERATOR_SPECIFICATION.allowed_inputs[0],),
            forbidden_sources=("وسمٌ مفترض",),
            domain_predicate="شرطٌ مفترض",
            transformation_rule=("خطوةٌ مفترضة",),
            undefinedness_conditions=("حالةٌ مفترضة",),
            output_invariants=("لازمٌ مفترض",),
        )
        assert spec.operator_class is OperatorClass.STATE_ONLY_EXTENSION_OPERATOR

    def test_a_duplicated_input_field_is_refused(self) -> None:
        first = EXTENSION_OPERATOR_SPECIFICATION.allowed_inputs[0]
        with pytest.raises(VvBirthAmendmentError):
            replace(EXTENSION_OPERATOR_SPECIFICATION, allowed_inputs=(first, first))


class TestTheAdversarialControls:
    def test_three_controls_are_frozen_before_any_readout(self) -> None:
        assert {operator.name for operator in ADVERSARIAL_EXTENSION_OPERATORS} == {
            "E_no_extension",
            "E_wrong_quality",
            "E_wrong_partner",
        }

    def test_each_names_the_invariant_it_must_break(self) -> None:
        for operator in ADVERSARIAL_EXTENSION_OPERATORS:
            assert operator.which_invariant_it_must_break.strip()

    def test_a_control_that_passes_yields_representation_tautology(self) -> None:
        for operator in ADVERSARIAL_EXTENSION_OPERATORS:
            assert operator.outcome_if_it_passes is (
                AmendmentOutcome.REPRESENTATION_TAUTOLOGY
            )

    def test_a_control_declaring_any_other_outcome_is_refused(self) -> None:
        with pytest.raises(VvBirthAmendmentError):
            AdversarialOperator(
                name="E_bogus",
                transformation_rule="قاعدةٌ مفترضة",
                which_invariant_it_must_break="لازمٌ مفترض",
                outcome_if_it_passes=AmendmentOutcome.UNDERPOWERED,
            )

    def test_an_unknown_control_is_refused_by_name(self) -> None:
        with pytest.raises(VvBirthAmendmentError):
            adversarial_operator_named("E_unknown")


class TestTheQuantityDomainIsConsistent:
    def test_the_chosen_bound_is_zero_or_one_extension(self) -> None:
        assert EXTENSION_COUNT_AMENDMENT.chosen_bound == (0, 1)
        assert EXTENSION_COUNT_AMENDMENT.quantity_codomain == (1, 2)

    def test_the_superseded_clause_is_quoted_not_summarised(self) -> None:
        assert "صفرٍ أو أكثرَ" in EXTENSION_COUNT_AMENDMENT.superseded_clause

    def test_a_bound_that_contradicts_the_codomain_is_refused(self) -> None:
        with pytest.raises(VvBirthAmendmentError):
            replace(EXTENSION_COUNT_AMENDMENT, quantity_codomain=(1, 2, 3))

    def test_the_unchosen_branch_is_recorded_with_what_it_would_need(self) -> None:
        assert EXTENSION_COUNT_AMENDMENT.what_the_other_branch_would_have_required

    def test_widening_the_bound_without_widening_the_codomain_is_refused(
        self,
    ) -> None:
        with pytest.raises(VvBirthAmendmentError):
            ExtensionCountAmendment(
                superseded_clause="بندٌ مفترض",
                chosen_bound=(0, 1, 2),
                quantity_codomain=(1, 2),
                why_this_branch="سببٌ مفترض",
                what_the_other_branch_would_have_required="لزومٌ مفترض",
            )


class TestTheWeakerModelsAreAlgorithmsNotProse:
    def test_all_four_rivals_carry_numbered_algorithms(self) -> None:
        for name in ("M_drop", "M_consonant", "M_second_vowel", "M_no_join"):
            implementation = weaker_model_implementation_named(name)
            assert len(implementation.algorithm) >= 3
            assert implementation.output.strip()
            assert implementation.undefined_conditions

    def test_the_leakage_baseline_is_implemented_and_still_not_evidence(self) -> None:
        baseline = weaker_model_implementation_named("M_identity_lookup")
        assert not baseline.counts_as_evidence
        assert all(
            field.provenance is ProvenanceClass.ORTHOGRAPHIC_IDENTITY
            for field in baseline.input_fields
        )

    def test_every_rival_counts_as_evidence(self) -> None:
        rivals = [
            implementation
            for implementation in WEAKER_MODEL_IMPLEMENTATIONS
            if implementation.counts_as_evidence
        ]
        assert len(rivals) == 4

    def test_an_implementation_of_an_unsealed_model_is_refused(self) -> None:
        with pytest.raises(VvBirthAmendmentError):
            weaker_model_implementation_named("M_invented_later")

    def test_an_implementation_of_a_model_absent_from_the_seal_is_refused(
        self,
    ) -> None:
        with pytest.raises(VvBirthAmendmentError):
            replace(WEAKER_MODEL_IMPLEMENTATIONS[0], name="M_written_later")

    def test_an_implementation_with_no_inputs_is_refused(self) -> None:
        with pytest.raises(VvBirthAmendmentError):
            replace(WEAKER_MODEL_IMPLEMENTATIONS[0], input_fields=())

    def test_an_implementation_with_no_algorithm_is_refused(self) -> None:
        with pytest.raises(VvBirthAmendmentError):
            replace(WEAKER_MODEL_IMPLEMENTATIONS[0], algorithm=())


class TestTheLeakBanIsByProvenanceNotByName:
    def test_the_three_forbidden_provenance_classes(self) -> None:
        assert IDENTITY_PROJECTION_FORBIDDEN_PROVENANCE == frozenset(
            {
                ProvenanceClass.ORTHOGRAPHIC_IDENTITY,
                ProvenanceClass.PROGRAM_POSITION,
                ProvenanceClass.MODEL_OUTPUT,
            }
        )

    def test_a_renamed_banned_proxy_is_still_refused(self) -> None:
        renamed = InputField(
            name="unicode_scalar",
            provenance=ProvenanceClass.ORTHOGRAPHIC_IDENTITY,
            what_it_carries="نقطةَ الترميز نفسَها تحت اسمٍ آخر",
        )
        assert renamed.name not in BANNED_IDENTITY_PROXIES
        assert identity_projection_refuses(renamed)

    def test_a_program_index_is_refused_under_any_name(self) -> None:
        for name in ("letter_index", "position_key", "nth"):
            field = InputField(
                name=name,
                provenance=ProvenanceClass.PROGRAM_POSITION,
                what_it_carries="موضعًا برمجيًّا",
            )
            assert identity_projection_refuses(field)

    def test_a_state_observation_is_admitted(self) -> None:
        field = InputField(
            name="vowel_state",
            provenance=ProvenanceClass.STATE_OBSERVATION,
            what_it_carries="حالةَ الحامل",
        )
        assert not identity_projection_refuses(field)

    def test_a_physical_observation_is_admitted_though_absent_today(self) -> None:
        field = InputField(
            name="measured_duration",
            provenance=ProvenanceClass.PHYSICAL_OBSERVATION,
            what_it_carries="مدّةً مقيسةً من صوتٍ مُسجَّل",
        )
        assert not identity_projection_refuses(field)


class TestTheTraceOrderIsInformationalNotSetTheoretic:
    def test_the_declared_trace_fields_are_three(self) -> None:
        assert len(TRACE_FIELD_SPECIFICATIONS) == 3
        assert {spec.name for spec in TRACE_FIELD_SPECIFICATIONS} == {
            "source_vowel_quality",
            "extension_partner_identity",
            "licence_reference",
        }

    def test_no_field_recovers_the_whole_input(self) -> None:
        assert not any(spec.recovers_whole_input for spec in TRACE_FIELD_SPECIFICATIONS)

    def test_a_field_that_recovers_the_whole_input_is_refused(self) -> None:
        with pytest.raises(VvBirthAmendmentError):
            TraceFieldSpecification(
                name="compact_note",
                what_it_carries="ملاحظةً مضغوطة",
                what_is_recoverable_from_it_alone="المُدخَلُ كاملًا",
                recovers_whole_input=True,
                is_droppable_in_a_projection=True,
            )

    @pytest.mark.parametrize("marker", FORBIDDEN_TRACE_CONTENT)
    def test_a_field_named_after_forbidden_content_is_refused(
        self, marker: str
    ) -> None:
        with pytest.raises(VvBirthAmendmentError):
            TraceFieldSpecification(
                name=marker,
                what_it_carries="محتوًى ممنوع",
                what_is_recoverable_from_it_alone="لا شيء",
                recovers_whole_input=False,
                is_droppable_in_a_projection=True,
            )

    def test_the_projections_are_single_field_drops(self) -> None:
        full = tuple(spec.name for spec in TRACE_FIELD_SPECIFICATIONS)
        projections = trace_projections_of(full)
        assert len(projections) == 3
        for projection in projections:
            assert len(projection) == len(full) - 1
            assert set(projection) < set(full)

    def test_an_undeclared_trace_field_is_refused(self) -> None:
        with pytest.raises(VvBirthAmendmentError):
            trace_projections_of(("source_vowel_quality", "everything_else"))


class TestTheTypeClaimIsBoundedByK0:
    def test_k0_is_frozen_with_at_least_two_contexts(self) -> None:
        assert len(CONTEXT_SET_K0) >= 2
        assert len({context.name for context in CONTEXT_SET_K0}) == len(CONTEXT_SET_K0)

    def test_the_law_quantifies_over_k0_only(self) -> None:
        assert "∀ k ∈ K_0" in TYPE_DISTINCTION_LAW.equivalence_law

    def test_the_only_three_outcomes_are_bounded_ones(self) -> None:
        assert TYPE_DISTINCTION_LAW.admissible_outcomes == (
            AmendmentOutcome.DISTINGUISHED_ON_K0,
            AmendmentOutcome.NOT_DISTINGUISHED_ON_K0,
            AmendmentOutcome.UNDERPOWERED,
        )

    def test_absence_on_k0_is_declared_not_to_be_type_identity(self) -> None:
        assert "لا تعني" in TYPE_DISTINCTION_LAW.what_not_distinguished_does_not_mean

    def test_the_asymmetry_between_the_two_hypotheses_is_recorded(self) -> None:
        note = TYPE_DISTINCTION_LAW.asymmetry_note
        assert "H_different_type" in note
        assert "لا يفنّدها" in note

    def test_a_law_admitting_a_type_equality_outcome_is_refused(self) -> None:
        with pytest.raises(VvBirthAmendmentError):
            replace(
                TYPE_DISTINCTION_LAW,
                admissible_outcomes=(
                    AmendmentOutcome.DISTINGUISHED_ON_K0,
                    AmendmentOutcome.NOT_DISTINGUISHED_ON_K0,
                ),
            )

    def test_a_single_context_set_is_refused(self) -> None:
        with pytest.raises(VvBirthAmendmentError):
            replace(TYPE_DISTINCTION_LAW, contexts=(CONTEXT_SET_K0[0],))

    def test_a_blank_context_is_refused(self) -> None:
        with pytest.raises(VvBirthAmendmentError):
            ContextK0(
                name="k_blank",
                what_it_places_the_centre_in="  ",
                what_it_observes="شيءٌ ما",
            )

    def test_a_law_without_an_asymmetry_note_is_refused(self) -> None:
        with pytest.raises(VvBirthAmendmentError):
            TypeDistinctionLaw(
                equivalence_law="قانونٌ مفترض ∀ k ∈ K_0",
                contexts=CONTEXT_SET_K0,
                admissible_outcomes=TYPE_DISTINCTION_LAW.admissible_outcomes,
                what_not_distinguished_does_not_mean="لا تعني شيئًا",
                asymmetry_note="   ",
            )


class TestStillNoReadoutAndNoJudgement:
    def test_the_readout_module_still_does_not_exist(self) -> None:
        assert readout_module_is_absent()
        assert importlib.util.find_spec(READOUT_MODULE_NAME) is None
        assert not (_SOURCE_ROOT / "arabic" / "vv_birth_readout.py").exists()

    def test_no_declared_field_carries_a_judgement(self) -> None:
        markers = ("verdict", "born", "score", "measured")
        for declaring_type in (
            SupersededPreregistrationParent,
            ExtensionOperatorSpecification,
            ExtensionCountAmendment,
            TraceFieldSpecification,
            TypeDistinctionLaw,
        ):
            declared = {item.name for item in fields(declaring_type)}
            for marker in markers:
                assert not any(marker in name for name in declared), marker

    def test_the_amendment_is_named_and_digested(self) -> None:
        assert AMENDMENT_ID == "G0.VV-BIRTH-1A"
        assert AMENDMENT_DIGEST == amendment_digest()
        assert len(AMENDMENT_DIGEST) == 64

    def test_the_amendment_digest_differs_from_the_parent_digest(self) -> None:
        assert AMENDMENT_DIGEST != PREREGISTRATION_DIGEST

    def test_its_site_list_is_independent_and_complete(self) -> None:
        assert missing_amendment_sites() == ()
        assert len(set(REQUIRED_AMENDMENT_SITES)) == len(REQUIRED_AMENDMENT_SITES)

    def test_a_removed_amendment_site_is_actually_detected(self, monkeypatch) -> None:
        import alghanem.arabic.vv_birth_amendment as amendment_module

        monkeypatch.delattr(amendment_module, "CONTEXT_SET_K0")
        assert ("vv_birth_amendment", "CONTEXT_SET_K0") in missing_amendment_sites()

    def test_the_site_list_is_written_by_hand_not_read_from_the_text(self) -> None:
        source = (_SOURCE_ROOT / "arabic" / "vv_birth_amendment.py").read_text(
            encoding="utf-8"
        )
        head, _, _ = source.partition("def missing_amendment_sites")
        declaration = head.rpartition("REQUIRED_AMENDMENT_SITES")[2]
        for forbidden in ("__all__", "dir(", "splitlines", "read_text", "getmembers"):
            assert forbidden not in declaration, forbidden

    def test_the_named_residuals_are_sorted_and_distinct(self) -> None:
        assert list(VV_BIRTH_AMENDMENT_NAMED_RESIDUALS) == sorted(
            VV_BIRTH_AMENDMENT_NAMED_RESIDUALS
        )
        assert len(set(VV_BIRTH_AMENDMENT_NAMED_RESIDUALS)) == len(
            VV_BIRTH_AMENDMENT_NAMED_RESIDUALS
        )

    def test_it_reads_no_kernel_authority(self) -> None:
        source = (_SOURCE_ROOT / "arabic" / "vv_birth_amendment.py").read_text(
            encoding="utf-8"
        )
        imports = tuple(
            line
            for line in source.splitlines()
            if line.startswith(("import ", "from "))
        )
        assert imports
        assert not any("kernel" in line for line in imports)
