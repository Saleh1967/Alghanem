"""اختبارُ المجال الثاني: هل النواةُ عامّةٌ أم برنامجٌ خاصٌّ بكلمة «باب»؟

نقلُ كتابٍ بين شخصَين لا يشترك مع فتح الباب في جذرٍ ولا وزنٍ ولا معجم؛ فإن
أجابت العملياتُ نفسُها عن سؤال الحيازة قبل الدليل وبعده، كان المشتركُ آليّةَ
التطبيق لا نصَّ المجال. وما يُقاس هنا أثرٌ معرفيّ: سكوتٌ قبل الدليل، وحسمٌ
بعده، وامتناعُ ترقية معرفةِ النوع إلى واقعة.
"""

from __future__ import annotations

import dataclasses as dc

import pytest

from alghanem.arabic.book_transfer_domain import (
    BOOK_HOLDING_STATE_ID,
    BOOK_INDIVIDUAL_ID,
    BOOK_LOCATION_STATE_ID,
    BOOK_OWNERSHIP_STATE_ID,
    BOOK_TRANSFER_EVENT_ID,
    BOOK_TYPE_ID,
    HELD_BY_FIRST,
    HELD_BY_SECOND,
    OWNED_BY_SECOND,
    THE_BOOK_DOMAIN_SCOPE,
    THREE_STATES_ARE_NOT_ONE,
    book_holding_question,
    book_transfer_store,
    book_world_register,
    holding_before_and_after,
    transfer_observation,
)
from alghanem.arabic.door_domain_deposit import door_domain_store
from alghanem.ontology import (
    EvidenceGenus,
    ExistenceStanding,
    FactError,
    Polarity,
    Proposition,
    PropositionForm,
    SupportStatus,
    assess_support,
    hold_state,
    requirements_for,
)


def test_the_second_domain_answers_with_silence_then_with_a_decision() -> None:
    before, after = holding_before_and_after(THE_BOOK_DOMAIN_SCOPE)
    assert before == SupportStatus.UNDECIDED_BY_AVAILABLE_PREMISES.value
    assert after == SupportStatus.SUPPORTS_PROPOSITION.value


def test_the_question_names_the_state_and_its_carrier_and_its_scope() -> None:
    question = book_holding_question(THE_BOOK_DOMAIN_SCOPE)
    assert question.subject_id == BOOK_INDIVIDUAL_ID
    assert question.predicate_id == BOOK_HOLDING_STATE_ID
    assert question.scope == THE_BOOK_DOMAIN_SCOPE
    assert requirements_for(question, book_transfer_store())


def test_the_deposited_state_has_exactly_the_two_declared_values() -> None:
    store = book_transfer_store()
    state = store.state_of(BOOK_HOLDING_STATE_ID)
    assert set(state.mutually_exclusive_values) == {HELD_BY_FIRST, HELD_BY_SECOND}


def test_knowing_the_transfer_event_type_deposits_no_transfer_at_all() -> None:
    store = book_transfer_store()
    assert store.event_type_of(BOOK_TRANSFER_EVENT_ID).roles
    register = book_world_register()
    assert all(
        proposition.subject_id != BOOK_TRANSFER_EVENT_ID
        for proposition in register.propositions
    )


def test_an_individual_exists_by_its_evidence_not_by_being_mentioned() -> None:
    register = book_world_register()
    for individual in register.individuals:
        assert individual.existence is ExistenceStanding.ESTABLISHED
        assert individual.evidence_ref is not None


def test_the_transfer_observation_is_fact_establishing_and_scoped() -> None:
    evidence = transfer_observation(HELD_BY_SECOND, THE_BOOK_DOMAIN_SCOPE)
    assert evidence.genus is EvidenceGenus.DIRECT_OBSERVATION
    assert evidence.establishes_facts
    assert evidence.scope.covers(THE_BOOK_DOMAIN_SCOPE)


def test_a_lexical_attestation_cannot_deposit_a_holding_fact() -> None:
    evidence = transfer_observation(HELD_BY_SECOND, THE_BOOK_DOMAIN_SCOPE)
    forged = type(evidence)(
        evidence_id=evidence.evidence_id,
        genus=EvidenceGenus.LEXICAL_ATTESTATION,
        statement=evidence.statement,
        scope=evidence.scope,
        source_name=evidence.source_name,
        source_digest=evidence.source_digest,
    )
    assert not forged.establishes_facts
    register = book_world_register().with_evidence(forged)
    proposition = Proposition(
        proposition_id="قضيّة-مُزوَّرة",
        form=PropositionForm.STATE_HOLDS,
        subject_id=BOOK_INDIVIDUAL_ID,
        predicate_id=BOOK_HOLDING_STATE_ID,
        value=HELD_BY_SECOND,
        polarity=Polarity.AFFIRMED,
        scope=THE_BOOK_DOMAIN_SCOPE,
        evidence_ref=forged.ref,
    )
    with pytest.raises(FactError):
        register.with_proposition(proposition)


# ----- العمومُ: المجالان يتقاسمان المحرِّك ولا يتقاسمان المعجم -----


def test_the_two_domains_share_no_identifier_yet_share_the_same_machinery() -> None:
    books = book_transfer_store()
    doors = door_domain_store()
    book_ids = {definition.type_id for definition in books.types}
    door_ids = {definition.type_id for definition in doors.types}
    assert BOOK_TYPE_ID in book_ids
    assert BOOK_TYPE_ID not in door_ids
    assert type(books) is type(doors)
    assert not (book_ids & door_ids)


def test_both_domains_are_founded_on_the_very_same_candidate_kinds() -> None:
    books = book_transfer_store()
    doors = door_domain_store()
    book_suffixes = tuple(
        candidate_id.split("-", 2)[-1] for candidate_id in books.ontology.candidate_ids
    )
    door_suffixes = tuple(
        candidate_id.split("-", 2)[-1] for candidate_id in doors.ontology.candidate_ids
    )
    assert book_suffixes == door_suffixes
    assert len(book_suffixes) == 11
    for book_id, door_id in zip(
        books.ontology.candidate_ids, doors.ontology.candidate_ids, strict=True
    ):
        assert (
            books.ontology.candidate(book_id).kind
            is doors.ontology.candidate(door_id).kind
        )


# ----- الموضعُ والحيازةُ والملكيّةُ ثلاثٌ لا واحدة -----


def test_the_three_states_are_deposited_as_three_not_folded_into_one() -> None:
    store = book_transfer_store()
    state_ids = {definition.state_id for definition in store.states}
    assert state_ids == {
        BOOK_HOLDING_STATE_ID,
        BOOK_LOCATION_STATE_ID,
        BOOK_OWNERSHIP_STATE_ID,
    }
    for state_id in state_ids:
        values = set(store.state_of(state_id).mutually_exclusive_values)
        assert len(values) == 2
    assert set(
        store.state_of(BOOK_HOLDING_STATE_ID).mutually_exclusive_values
    ).isdisjoint(store.state_of(BOOK_OWNERSHIP_STATE_ID).mutually_exclusive_values)


def test_the_transfer_decides_holding_and_leaves_ownership_undecided() -> None:
    scope = THE_BOOK_DOMAIN_SCOPE
    store = book_transfer_store()
    evidence = dc.replace(
        transfer_observation(HELD_BY_SECOND, scope),
        evidence_id="مشاهدة-حيازةٍ-بعد-النقل",
    )
    register = book_world_register()
    register = hold_state(
        individual_id=BOOK_INDIVIDUAL_ID,
        state_id=BOOK_HOLDING_STATE_ID,
        value=HELD_BY_SECOND,
        scope=scope,
        evidence=evidence,
        register=register,
        store=store,
        proposition_id="قضيّة-الحيازة-بعد-النقل",
    )
    holding = assess_support(
        "سؤال-الحيازة",
        Proposition(
            proposition_id="هدف-الحيازة",
            form=PropositionForm.STATE_HOLDS,
            subject_id=BOOK_INDIVIDUAL_ID,
            predicate_id=BOOK_HOLDING_STATE_ID,
            value=HELD_BY_SECOND,
            polarity=Polarity.AFFIRMED,
            scope=scope,
            evidence_ref=evidence.ref,
        ),
        register,
        store,
    )
    ownership = assess_support(
        "سؤال-الملكيّة",
        Proposition(
            proposition_id="هدف-الملكيّة",
            form=PropositionForm.STATE_HOLDS,
            subject_id=BOOK_INDIVIDUAL_ID,
            predicate_id=BOOK_OWNERSHIP_STATE_ID,
            value=OWNED_BY_SECOND,
            polarity=Polarity.AFFIRMED,
            scope=scope,
            evidence_ref=evidence.ref,
        ),
        register,
        store,
    )
    assert holding.status is SupportStatus.SUPPORTS_PROPOSITION
    assert ownership.status is SupportStatus.UNDECIDED_BY_AVAILABLE_PREMISES
    assert ownership.status is not SupportStatus.SUPPORTS_NEGATION
    assert "الملكيّةُ لا تتحرّك إلّا بسببٍ مُعلَنٍ لها" in THREE_STATES_ARE_NOT_ONE


def test_no_rule_in_the_deposit_names_ownership_or_location_as_its_consequent() -> None:
    store = book_transfer_store()
    for rule in store.rules:
        assert BOOK_OWNERSHIP_STATE_ID not in rule.conclusion_pattern
        assert BOOK_LOCATION_STATE_ID not in rule.conclusion_pattern


def test_the_direction_of_the_transfer_is_not_baked_into_the_domain_data() -> None:
    scope = THE_BOOK_DOMAIN_SCOPE
    store = book_transfer_store()
    for value in (HELD_BY_FIRST, HELD_BY_SECOND):
        evidence = dc.replace(
            transfer_observation(value, scope),
            evidence_id=f"مشاهدة-اتّجاهٍ-{value}",
        )
        register = book_world_register()
        register = hold_state(
            individual_id=BOOK_INDIVIDUAL_ID,
            state_id=BOOK_HOLDING_STATE_ID,
            value=value,
            scope=scope,
            evidence=evidence,
            register=register,
            store=store,
            proposition_id="قضيّة-الحيازة",
        )
        derivation = assess_support(
            "سؤال-الحيازة",
            Proposition(
                proposition_id="هدف",
                form=PropositionForm.STATE_HOLDS,
                subject_id=BOOK_INDIVIDUAL_ID,
                predicate_id=BOOK_HOLDING_STATE_ID,
                value=value,
                polarity=Polarity.AFFIRMED,
                scope=scope,
                evidence_ref=evidence.ref,
            ),
            register,
            store,
        )
        assert derivation.status is SupportStatus.SUPPORTS_PROPOSITION
