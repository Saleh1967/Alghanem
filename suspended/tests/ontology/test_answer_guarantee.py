"""فحوصُ ضمانِ الجواب: ماذا يفحص المتحقِّق بنفسه، وأين يبقى واثقًا؟

البابُ الأوّل: شاهدُ عدم اللزوم لا يُقبَل بالتسمية. نموذجٌ عنوانُه «مفتوح»
وآخرُ عنوانُه «مغلق» دعوى ثانيةٌ تُضاف إلى الأولى؛ والشهادةُ لا تخرج حتّى
يُفحَص في كلا النموذجين فضاءُ القيم، وإيداعُ أنواعِ الأحداث، واحترامُ المنفيِّ
في القول، واستيفاءُ كلِّ قاعدةٍ صارمةٍ لها قيدٌ منفَّذ.

والبابُ الثاني: حدودُ الضمان مُعلَنة. المتحقِّقُ يفحص منزلةَ المقدّمات
وتطبيقَ القواعد ومطابقةَ الأطراف وشمولَ النطاق وصلةَ الجواب بالسؤال؛ ولا
يفحص صدقَ التحليل اللغويِّ ولا مطابقةَ الدليل للواقع. وما لا يُفحَص يُسمّى
ههنا ولا يُطوى.
"""

from __future__ import annotations

import dataclasses as dc

import pytest

from alghanem.arabic.door_domain_deposit import (
    DOOR_OPENING_EVENT_ID,
    DOOR_STATE_ID,
    DOOR_STATE_OPEN,
    DOOR_STATE_SHUT,
    door_domain_store,
)
from alghanem.arabic.door_ontology_run import (
    DOOR_INDIVIDUAL_ID,
    THE_QUESTION_INTERVAL,
    ZAYD_INDIVIDUAL_ID,
    door_model_constraints,
    full_run,
)
from alghanem.ontology import (
    A_NAMED_MODEL_IS_NOT_AN_ADMISSIBLE_ONE,
    InferenceError,
    Model,
    ModelCheck,
    ModelConstraint,
    Scope,
    SupportStatus,
    VerificationCheck,
    check_model,
    non_entailment_witness,
    verify,
)

_REF = "سؤال-الفحص"


def _witness(**overrides: object):  # type: ignore[no-untyped-def]
    arguments: dict[str, object] = {
        "question_ref": _REF,
        "individual_id": DOOR_INDIVIDUAL_ID,
        "state_id": DOOR_STATE_ID,
        "values": (DOOR_STATE_SHUT, DOOR_STATE_OPEN),
        "shared_occurred_event_keys": (),
        "declared_model_note": "نموذجان داخل مجالٍ مُعلَن",
        "store": door_domain_store(),
        "constraints": door_model_constraints(),
    }
    arguments.update(overrides)
    return non_entailment_witness(**arguments)  # type: ignore[arg-type]


# ----- البابُ الأوّل: الشهادةُ تُفحَص ولا تُسمّى -----


def test_the_witness_reports_what_it_checked_in_both_models() -> None:
    witness = _witness()
    assert len(witness.admissibility) == 2
    for verdict in witness.admissibility:
        assert verdict.is_admissible
        assert ModelCheck.VALUE_IN_THE_DECLARED_SPACE in verdict.checked
        assert ModelCheck.EVENT_TYPE_IS_DEPOSITED in verdict.checked
        assert ModelCheck.DECLARED_CONSTRAINTS_HOLD in verdict.checked
        assert verdict.failed == ()
        assert verdict.unexecuted_rule_ids == ()
    assert witness.differing_values == (DOOR_STATE_SHUT, DOOR_STATE_OPEN)


def test_a_strict_rule_without_an_executed_constraint_blocks_the_certificate() -> None:
    with pytest.raises(InferenceError) as refusal:
        _witness(constraints=())
    message = str(refusal.value)
    assert ModelCheck.RULE_NOT_EXECUTABLE_HERE.value in message
    assert "قاعدة-أثر-الفتح@١" in message


def test_a_model_that_breaks_a_declared_constraint_blocks_the_certificate() -> None:
    with pytest.raises(InferenceError) as refusal:
        _witness(
            shared_occurred_event_keys=((DOOR_INDIVIDUAL_ID, DOOR_OPENING_EVENT_ID),)
        )
    message = str(refusal.value)
    assert ModelCheck.DECLARED_CONSTRAINTS_HOLD.value in message
    assert "قيد-أثر-الفتح" in message


def test_a_value_outside_the_declared_space_blocks_the_certificate() -> None:
    with pytest.raises(InferenceError) as refusal:
        _witness(values=(DOOR_STATE_SHUT, "مُوارَبٌ قليلًا"))
    assert ModelCheck.VALUE_IN_THE_DECLARED_SPACE.value in str(refusal.value)


def test_an_undeposited_event_type_blocks_the_certificate() -> None:
    with pytest.raises(InferenceError) as refusal:
        _witness(shared_occurred_event_keys=((DOOR_INDIVIDUAL_ID, "حدث_لم_يُودَع"),))
    assert ModelCheck.EVENT_TYPE_IS_DEPOSITED.value in str(refusal.value)


def test_a_model_that_realises_what_the_utterance_denies_blocks_the_certificate() -> (
    None
):
    outcome = full_run()
    store = door_domain_store()
    constraints = (
        *door_model_constraints(),
        ModelConstraint(
            constraint_id="قيد-أثر-الانفتاح",
            rule_versioned_id="قاعدة-أثر-الفتح@١",
            individual_id=DOOR_INDIVIDUAL_ID,
            trigger_event_type_id=DOOR_OPENING_EVENT_ID,
            required_state_id=DOOR_STATE_ID,
            required_value=DOOR_STATE_OPEN,
        ),
    )
    offending = Model(
        model_id="نموذجٌ-يُوقِع-المنفيّ",
        state_values={(DOOR_INDIVIDUAL_ID, DOOR_STATE_ID): DOOR_STATE_OPEN},
        occurred_event_keys=((ZAYD_INDIVIDUAL_ID, DOOR_OPENING_EVENT_ID),),
    )
    verdict = check_model(offending, store, constraints, outcome.bridge.content)
    assert not verdict.is_admissible
    assert ModelCheck.NEGATED_CONTENT_RESPECTED in verdict.failed


def test_the_refusal_names_why_a_title_is_not_a_proof() -> None:
    assert "تسميةٌ لا برهان" in A_NAMED_MODEL_IS_NOT_AN_ADMISSIBLE_ONE
    with pytest.raises(InferenceError) as refusal:
        _witness(constraints=())
    assert A_NAMED_MODEL_IS_NOT_AN_ADMISSIBLE_ONE in str(refusal.value)


# ----- البابُ الثاني: مواضعُ ثقةِ المتحقِّق -----


def test_the_verifier_always_reports_all_five_places() -> None:
    outcome = full_run()
    reported = {check for check, _passed, _reason in outcome.report.findings}
    assert reported == set(VerificationCheck)
    assert outcome.report.passed
    assert outcome.accepted


def test_a_premise_outside_the_register_fails_the_standing_check() -> None:
    from alghanem.arabic.door_ontology_run import door_world_register, state_question
    from alghanem.ontology import Answer

    outcome = full_run()
    store = door_domain_store()
    register = door_world_register(store)
    forged = dc.replace(
        outcome.state_after,
        premise_proposition_ids=("قضيّةٌ-لا-وجودَ-لها",),
        conclusion_proposition_id="قضيّةٌ-لا-وجودَ-لها",
    )
    answer = Answer(
        question_id=state_question().question_id,
        status=SupportStatus.SUPPORTS_PROPOSITION,
        derivation=forged,
        statement="جوابٌ يستند إلى مقدّمةٍ ليست في السجلّ",
    )
    report = verify(state_question(), answer, register, store)
    assert VerificationCheck.PREMISES_STANDING in report.failed_checks
    assert not report.passed


def test_widening_the_answer_beyond_the_evidence_scope_fails_the_coverage_check() -> (
    None
):
    outcome = full_run()
    store = door_domain_store()
    from alghanem.arabic.door_ontology_run import (
        door_state_observation,
        door_world_register,
        state_question,
    )
    from alghanem.ontology import Answer, hold_state

    register = door_world_register(store)
    observation = door_state_observation(DOOR_STATE_SHUT)
    register = hold_state(
        individual_id=DOOR_INDIVIDUAL_ID,
        state_id=DOOR_STATE_ID,
        value=DOOR_STATE_SHUT,
        scope=THE_QUESTION_INTERVAL,
        evidence=observation,
        register=register,
        store=store,
        proposition_id="قضيّة-حال-الباب",
    )
    wider = Scope(
        domain_id=THE_QUESTION_INTERVAL.domain_id,
        timeline_id=THE_QUESTION_INTERVAL.timeline_id,
        start=THE_QUESTION_INTERVAL.start,
        end=(THE_QUESTION_INTERVAL.end or 0) + 1000,
    )
    assert not THE_QUESTION_INTERVAL.covers(wider)
    question = state_question()
    widened = dc.replace(question, scope=wider)
    answer = Answer(
        question_id=widened.question_id,
        status=SupportStatus.SUPPORTS_PROPOSITION,
        derivation=outcome.state_after,
        statement="الباب مغلق في فترةٍ أوسعَ من فترة الدليل",
    )
    report = verify(widened, answer, register, store)
    assert VerificationCheck.SCOPE_COVERAGE in report.failed_checks
    assert not report.passed


def test_an_answer_carrying_a_foreign_derivation_is_refused_at_construction() -> None:
    from alghanem.arabic.door_ontology_run import state_question
    from alghanem.ontology import Answer, VerificationError

    outcome = full_run()
    with pytest.raises(VerificationError):
        Answer(
            question_id=state_question().question_id,
            status=outcome.occurrence_before.status,
            derivation=outcome.occurrence_before,
            statement="جوابُ سؤالِ الوقوع مُقدَّمٌ عن سؤالِ الحال",
        )
