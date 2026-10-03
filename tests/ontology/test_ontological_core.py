"""اختباراتٌ **ذاتُ أثرٍ معرفيّ** لنواة التفسير الأنطولوجيّ.

لا يقيس هذا الملفُّ عددَ الجمل المقبولة؛ يقيس أن يتغيّر الحكمُ حين تتغيّر
معرفةٌ ذاتُ صلة، وأن يثبت حين تتغيّر معرفةٌ لا صلةَ لها، وأن يُعلَّق حين تُحذَف
مقدّمةٌ لازمة، وأن يُفرَّق بين عدم الحسم وبين إثبات عدم اللزوم.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.book_transfer_domain import (
    BOOK_HOLDING_STATE_ID,
    BOOK_INDIVIDUAL_ID,
    HELD_BY_SECOND,
    book_transfer_store,
    book_world_register,
    holding_before_and_after,
)
from alghanem.arabic.door_domain_deposit import (
    DOOR_OPENING_EVENT_ID,
    DOOR_STATE_ID,
    DOOR_STATE_OPEN,
    DOOR_STATE_SHUT,
    DOOR_TYPE_ID,
    door_domain_store,
)
from alghanem.arabic.door_ontology_run import (
    DOOR_INDIVIDUAL_ID,
    LEAF_INDIVIDUAL_ID,
    THE_OBSERVED_INTERVAL,
    THE_QUESTION_INTERVAL,
    ZAYD_INDIVIDUAL_ID,
    door_state_observation,
    door_world_register,
    full_run,
    occurrence_question,
    state_question,
)
from alghanem.ontology import (
    AcceptanceStanding,
    Declared,
    EpistemicError,
    Evidence,
    EvidenceGenus,
    FactError,
    InferenceError,
    MembershipTest,
    Modality,
    NegationScope,
    OperationError,
    Polarity,
    Proposition,
    PropositionForm,
    QuestionKind,
    RequirementGenus,
    Scope,
    SupportStatus,
    ValueStatus,
    assess_support,
    check_membership,
    deletion_test,
    non_entailment_witness,
    refuse_part_as_instance,
    refuse_silence_as_negation,
    refuse_unknown_as_a_kind,
    requirements_for,
    verify,
)

_LATER = Scope(domain_id="مجال-الأبواب", timeline_id="خطّ-زمن-الدار", start=40, end=50)


# ----- الحالاتُ الخمسُ، وفرقُ الصمت عن النفي -----


def test_the_five_statuses_separate_two_different_silences() -> None:
    silences = tuple(status for status in SupportStatus if status.is_a_silence)
    assert len(silences) == 2
    assert SupportStatus.UNDECIDED_BY_AVAILABLE_PREMISES in silences
    assert SupportStatus.OUT_OF_SCOPE_OR_UNSUPPORTED in silences
    for status in silences:
        assert not status.is_decided


def test_a_silence_is_never_read_as_a_negation() -> None:
    with pytest.raises(InferenceError):
        refuse_silence_as_negation(SupportStatus.UNDECIDED_BY_AVAILABLE_PREMISES)
    with pytest.raises(InferenceError):
        refuse_silence_as_negation(SupportStatus.OUT_OF_SCOPE_OR_UNSUPPORTED)
    assert refuse_silence_as_negation(SupportStatus.SUPPORTS_NEGATION) is None


# ----- أثرُ تغيّر الدليل على الحكم -----


def test_an_evaluation_only_tag_change_moves_no_derived_reading() -> None:
    first = full_run()
    second = full_run()
    assert first.bridge.content.content_id == second.bridge.content.content_id
    assert first.state_after.status is second.state_after.status


def test_changing_a_relevant_evidence_changes_the_dependent_judgment() -> None:
    run = full_run()
    assert run.state_before.status is SupportStatus.UNDECIDED_BY_AVAILABLE_PREMISES
    assert run.state_after.status is SupportStatus.SUPPORTS_PROPOSITION


def test_changing_an_unrelated_evidence_leaves_the_judgment_standing() -> None:
    run = full_run()
    assert run.state_after_irrelevant_change.status is run.state_after.status


def test_amending_the_evidence_an_answer_rests_on_suspends_that_answer() -> None:
    run = full_run()
    store = door_domain_store()
    register = door_world_register(store)
    observation = door_state_observation(DOOR_STATE_SHUT)
    from alghanem.ontology import hold_state

    held = hold_state(
        individual_id=DOOR_INDIVIDUAL_ID,
        state_id=DOOR_STATE_ID,
        value=DOOR_STATE_SHUT,
        scope=THE_OBSERVED_INTERVAL,
        evidence=observation,
        proposition_id="قضيّة-حال-الباب",
        register=register,
        store=store,
    )
    amended = Evidence(
        evidence_id=observation.evidence_id,
        genus=observation.genus,
        statement=observation.statement + "؛ ثمّ تبيّن أنّ المشاهدَ غيرُ هذا الباب",
        source_name=observation.source_name,
        scope=observation.scope,
        source_digest=None,
    )
    after = held.amend_evidence(amended)
    assert held.proposition_of("قضيّة-حال-الباب").suspended is False
    assert after.proposition_of("قضيّة-حال-الباب").suspended is True
    assert run.state_after.status is SupportStatus.SUPPORTS_PROPOSITION


def test_deleting_a_necessary_premise_suspends_the_proof_that_used_it() -> None:
    run = full_run()
    assert run.minimality.is_irredundant_for_this_proof
    assert run.minimality.removable_premise_ids == ()


def test_irredundancy_is_not_claimed_to_be_global_minimality() -> None:
    run = full_run()
    assert run.minimality.global_minimality is Declared.UNDECLARED
    assert run.minimality.alternative_proof_count is None


def test_a_deletion_test_refuses_to_run_on_an_undecided_proof() -> None:
    from alghanem.ontology import QuestionError

    with pytest.raises(QuestionError):
        deletion_test(
            ("مقدّمة",),
            lambda _: SupportStatus.UNDECIDED_BY_AVAILABLE_PREMISES,
        )


# ----- عدمُ الحسم ليس إثباتًا لعدم اللزوم -----


def test_non_entailment_is_proved_by_two_models_not_by_a_silence() -> None:
    run = full_run()
    assert run.state_before.status.is_a_silence
    first, second = run.witness.differing_values
    assert first != second
    assert {first, second} == {DOOR_STATE_SHUT, DOOR_STATE_OPEN}


def test_a_witness_whose_models_agree_is_refused() -> None:
    with pytest.raises(InferenceError):
        non_entailment_witness(
            question_ref="سؤال",
            individual_id=DOOR_INDIVIDUAL_ID,
            state_id=DOOR_STATE_ID,
            values=(DOOR_STATE_SHUT, DOOR_STATE_SHUT),
            shared_occurred_event_keys=(),
            declared_model_note="نموذجان لا يختلفان",
        )


# ----- النطاقُ: المشاهَدُ لا يُعمَّم -----


def test_an_observed_interval_does_not_settle_an_unobserved_one() -> None:
    store = door_domain_store()
    register = door_world_register(store)
    from alghanem.ontology import hold_state

    held = hold_state(
        individual_id=DOOR_INDIVIDUAL_ID,
        state_id=DOOR_STATE_ID,
        value=DOOR_STATE_SHUT,
        scope=THE_OBSERVED_INTERVAL,
        evidence=door_state_observation(DOOR_STATE_SHUT),
        proposition_id="قضيّة-حال-الباب",
        register=register,
        store=store,
    )
    target = Proposition(
        proposition_id="هدف",
        form=PropositionForm.STATE_HOLDS,
        subject_id=DOOR_INDIVIDUAL_ID,
        predicate_id=DOOR_STATE_ID,
        value=DOOR_STATE_SHUT,
        polarity=Polarity.AFFIRMED,
        scope=_LATER,
        evidence_ref=held.proposition_of("قضيّة-حال-الباب").evidence_ref,
    )
    assessment = assess_support("سؤال-متأخّر", target, held, store)
    assert assessment.status is SupportStatus.UNDECIDED_BY_AVAILABLE_PREMISES


def test_a_proposition_may_not_outrun_the_scope_of_its_evidence() -> None:
    store = door_domain_store()
    register = door_world_register(store)
    from alghanem.ontology import hold_state

    with pytest.raises(OperationError):
        hold_state(
            individual_id=DOOR_INDIVIDUAL_ID,
            state_id=DOOR_STATE_ID,
            value=DOOR_STATE_SHUT,
            scope=_LATER,
            evidence=door_state_observation(DOOR_STATE_SHUT),
            proposition_id="قضيّة-متجاوِزة",
            register=register,
            store=store,
        )


# ----- السؤالُ يُغيِّر الحدَّ الأدنى المكتمل -----


def test_a_syntactic_question_needs_fewer_premises_than_a_factual_one() -> None:
    store = door_domain_store()
    syntactic = requirements_for(_question_of(QuestionKind.SYNTACTIC_FUNCTION), store)
    factual = requirements_for(_question_of(QuestionKind.EVENT_OCCURRENCE), store)
    stateful = requirements_for(_question_of(QuestionKind.CURRENT_STATE), store)
    assert len(syntactic) < len(factual) <= len(stateful)
    assert RequirementGenus.ACCEPTED_FACT not in {item.genus for item in syntactic}
    assert RequirementGenus.ACCEPTED_FACT in {item.genus for item in factual}


def test_a_state_question_offers_the_defeasible_persistence_rule_as_optional() -> None:
    store = door_domain_store()
    stateful = requirements_for(_question_of(QuestionKind.CURRENT_STATE), store)
    licensed = [
        item for item in stateful if item.genus is RequirementGenus.LICENSED_RULE
    ]
    assert licensed
    assert all(not item.obligatory for item in licensed)
    assert all("مانع" in item.statement for item in licensed)


def test_an_out_of_scope_question_declares_zero_requirements() -> None:
    store = door_domain_store()
    assert requirements_for(_question_of(QuestionKind.OUT_OF_SCOPE), store) == ()


def _question_of(kind: QuestionKind):  # type: ignore[no-untyped-def]
    from alghanem.ontology import Question

    return Question(
        question_id=f"سؤال-{kind.value}",
        text="سؤالٌ للاختبار",
        kind=kind,
        subject_id=DOOR_INDIVIDUAL_ID,
        predicate_id=DOOR_STATE_ID,
        scope=THE_QUESTION_INTERVAL,
    )


# ----- التحقّقُ يفحص خمسةَ مواضع، والقبولُ مربوط -----


def test_the_verifier_names_five_places_and_fails_them_separately() -> None:
    run = full_run()
    checks = {check for check, _, _ in run.report.findings}
    assert len(checks) == 5
    assert run.report.passed
    for check in checks:
        assert run.report.reason_for(check)


def test_a_verification_goes_stale_when_an_influencing_element_changes() -> None:
    from alghanem.ontology import Answer, accept, hold_state

    store = door_domain_store()
    register = door_world_register(store)
    run = full_run()
    held = hold_state(
        individual_id=DOOR_INDIVIDUAL_ID,
        state_id=DOOR_STATE_ID,
        value=DOOR_STATE_SHUT,
        scope=THE_OBSERVED_INTERVAL,
        evidence=door_state_observation(DOOR_STATE_SHUT),
        proposition_id="قضيّة-حال-الباب",
        register=register,
        store=store,
    )
    question = state_question()
    derivation = assess_support(
        question.question_id,
        Proposition(
            proposition_id="هدف",
            form=PropositionForm.STATE_HOLDS,
            subject_id=DOOR_INDIVIDUAL_ID,
            predicate_id=DOOR_STATE_ID,
            value=DOOR_STATE_SHUT,
            polarity=Polarity.AFFIRMED,
            scope=THE_QUESTION_INTERVAL,
            evidence_ref=held.proposition_of("قضيّة-حال-الباب").evidence_ref,
        ),
        held,
        store,
    )
    answer = Answer(
        question_id=question.question_id,
        status=derivation.status,
        derivation=derivation,
        statement="البابُ مغلقٌ في الفترة المُعلَنة",
    )
    report = verify(question, answer, held, store)
    record = accept(question, answer, report, store, held, run.bridge.content)
    assert record.is_accepted
    assert not record.is_stale_against(store, held, run.bridge.content)
    moved = held.retract("مشاهدة-حال-الباب")
    assert record.is_stale_against(store, moved, run.bridge.content)


# ----- الانتقالُ بين المستويات -----


def test_a_conditional_content_is_never_deposited_as_a_fact() -> None:
    from alghanem.arabic.door_ontology_run import surface_candidates
    from alghanem.arabic.fath_ontology_bridge import bridge_utterance
    from alghanem.arabic.fath_surface_analysis import read_utterance

    store = door_domain_store()
    register = door_world_register(store)
    reading = read_utterance("إِنْ فَتَحَ زَيْدٌ الْبَابَ".encode())
    bridge = bridge_utterance(
        reading=reading,
        store=store,
        register=register,
        time_scope=THE_QUESTION_INTERVAL,
        surface_candidates=surface_candidates(),
    )
    assert bridge.content.event.modality is Modality.CONDITIONAL
    assert not bridge.content.event.commits_to_occurrence
    evidence = Evidence(
        evidence_id="خبر",
        genus=EvidenceGenus.ACCEPTED_REPORT,
        statement="خبرٌ معتمد",
        source_name="مصدرٌ معتمد",
        scope=THE_QUESTION_INTERVAL,
        source_digest=None,
    )
    with pytest.raises(FactError):
        register.deposit_from_discourse(bridge.content, evidence, "قضيّة")


def test_moving_from_negation_to_condition_changes_the_commitments() -> None:
    from alghanem.arabic.door_ontology_run import surface_candidates
    from alghanem.arabic.fath_ontology_bridge import bridge_utterance
    from alghanem.arabic.fath_surface_analysis import read_utterance

    store = door_domain_store()
    register = door_world_register(store)
    negated = bridge_utterance(
        reading=read_utterance("لَمْ يَفْتَحْ زَيْدٌ الْبَابَ".encode()),
        store=store,
        register=register,
        time_scope=THE_QUESTION_INTERVAL,
        surface_candidates=surface_candidates(),
    ).content.event
    conditional = bridge_utterance(
        reading=read_utterance("إِنْ فَتَحَ زَيْدٌ الْبَابَ".encode()),
        store=store,
        register=register,
        time_scope=THE_QUESTION_INTERVAL,
        surface_candidates=surface_candidates(),
    ).content.event
    assert negated.polarity is Polarity.NEGATED
    assert negated.negation_scope is NegationScope.WHOLE_EVENT_OCCURRENCE
    assert negated.commits_to_non_occurrence
    assert conditional.polarity is Polarity.AFFIRMED
    assert not conditional.commits_to_non_occurrence
    assert not conditional.commits_to_occurrence


def test_a_lexical_attestation_founds_the_store_but_deposits_no_fact() -> None:
    store = door_domain_store()
    attestation = store.evidence_of(
        next(
            item.ref
            for item in store.evidence
            if item.genus is EvidenceGenus.LEXICAL_ATTESTATION
        )
    )
    assert attestation.genus.is_substance_founding
    assert not attestation.establishes_facts
    assert attestation.standing is AcceptanceStanding.DECLARED_ONLY


def test_knowing_the_type_does_not_establish_an_occurrence_for_an_individual() -> None:
    store = door_domain_store()
    register = door_world_register(store)
    definition = store.event_type_of(DOOR_OPENING_EVENT_ID)
    assert definition.resulting_state_value == DOOR_STATE_OPEN
    target = Proposition(
        proposition_id="هدف",
        form=PropositionForm.EVENT_OCCURRED,
        subject_id=ZAYD_INDIVIDUAL_ID,
        predicate_id=DOOR_OPENING_EVENT_ID,
        value=None,
        polarity=Polarity.AFFIRMED,
        scope=THE_QUESTION_INTERVAL,
        evidence_ref=register.individuals[0].evidence_ref,
    )
    assert (
        assess_support("سؤال", target, register, store).status
        is SupportStatus.UNDECIDED_BY_AVAILABLE_PREMISES
    )


# ----- العملياتُ تحفظ الفروقَ النوعيّة -----


def test_membership_is_run_through_conditions_not_read_off_a_name() -> None:
    store = door_domain_store()
    register = door_world_register(store)
    verdict = check_membership(DOOR_INDIVIDUAL_ID, DOOR_TYPE_ID, register, store)
    assert verdict.is_member
    assert len(verdict.satisfied_condition_ids) == 2
    conditions = {
        condition.test
        for condition in store.type_of(DOOR_TYPE_ID).membership_conditions
    }
    assert conditions == {
        MembershipTest.ATTRIBUTE_EQUALS,
        MembershipTest.HAS_CAPABILITY,
    }


def test_a_part_is_never_promoted_to_an_instance_of_the_whole_type() -> None:
    store = door_domain_store()
    register = door_world_register(store)
    verdict = check_membership(LEAF_INDIVIDUAL_ID, DOOR_TYPE_ID, register, store)
    assert not verdict.is_member
    assert verdict.status is not ValueStatus.KNOWN
    with pytest.raises(OperationError):
        refuse_part_as_instance("جزء_من")


def test_unknown_is_a_status_and_never_an_ontological_kind() -> None:
    assert refuse_unknown_as_a_kind("value_status", ValueStatus.KNOWN) is None
    for field_name in ("kind", "genus", "type_id", "sort"):
        with pytest.raises(EpistemicError):
            refuse_unknown_as_a_kind(field_name, ValueStatus.UNKNOWN)


# ----- المجالُ الثاني يُعيد استعمال الآلة نفسها -----


def test_the_second_domain_reuses_the_very_same_operations() -> None:
    before, after = holding_before_and_after(
        Scope(domain_id="مجال-الكتب", timeline_id="خطّ-زمن-المجلس", start=5, end=15)
    )
    assert before == SupportStatus.UNDECIDED_BY_AVAILABLE_PREMISES.value
    assert after == SupportStatus.SUPPORTS_PROPOSITION.value


def test_the_second_domain_knows_its_type_without_witnessing_a_transfer() -> None:
    store = book_transfer_store()
    register = book_world_register()
    scope = Scope(domain_id="مجال-الكتب", timeline_id="خطّ-زمن-المجلس", start=5, end=15)
    target = Proposition(
        proposition_id="هدف",
        form=PropositionForm.STATE_HOLDS,
        subject_id=BOOK_INDIVIDUAL_ID,
        predicate_id=BOOK_HOLDING_STATE_ID,
        value=HELD_BY_SECOND,
        polarity=Polarity.AFFIRMED,
        scope=scope,
        evidence_ref=register.individuals[0].evidence_ref,
    )
    assert (
        assess_support("سؤال", target, register, store).status
        is SupportStatus.UNDECIDED_BY_AVAILABLE_PREMISES
    )


def test_the_occurrence_question_is_answered_from_the_deposited_negation() -> None:
    run = full_run()
    assert run.occurrence_before.status is SupportStatus.SUPPORTS_NEGATION
    assert run.occurrence_after.status is SupportStatus.SUPPORTS_NEGATION
    assert occurrence_question().kind is QuestionKind.EVENT_OCCURRENCE
