"""اختباراتُ الجسر اللغويِّ المشتقِّ لعائلة الفتح، وما يرفض أن يعبره.

المقياسُ هنا ليس عددَ العبارات المقبولة، بل أن يبقى الفاعلُ النحويُّ متمايزًا
عن الدور الدلاليِّ عن هويّة شاغله، وأن يُصيب الجسرُ صياغاتٍ وأفرادًا لم تُكتَب
الإجابةُ لها، وأن يقف عند ما لم يُحلَّل بدل أن يحمله على أقرب تركيب.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.door_domain_deposit import (
    DOOR_AGENT_ROLE_ID,
    DOOR_OPENING_EVENT_ID,
    DOOR_PATIENT_ROLE_ID,
    FORM_VII_EVENT_ID,
    FORM_VII_PATIENT_ROLE_ID,
    door_domain_store,
)
from alghanem.arabic.door_ontology_run import (
    DOOR_INDIVIDUAL_ID,
    THE_QUESTION_INTERVAL,
    ZAYD_INDIVIDUAL_ID,
    door_world_register,
    surface_candidates,
)
from alghanem.arabic.fath_ontology_bridge import (
    BridgeError,
    ProvenanceGenus,
    bridge_utterance,
)
from alghanem.arabic.fath_sense_import import (
    LexicalSenseError,
    import_sense_of_root,
    physical_opening_stipulation,
)
from alghanem.arabic.fath_surface_analysis import (
    A_SILENT_ORTHOGRAPHIC_APPENDAGE_IS_A_NAMED_SUSPENSION,
    Construction,
    SurfaceAnalysisError,
    SyntacticFunction,
    WordShape,
    read_utterance,
    read_word,
)
from alghanem.ontology import EvidenceGenus, FillerStanding, Scope

_ACTIVE = "فَتَحَ زَيْدٌ الْبَابَ"
_PASSIVE = "فُتِحَ الْبَابُ"
_FORM_VII = "انْفَتَحَ الْبَابُ"
_NEGATED = "لَمْ يَفْتَحْ زَيْدٌ الْبَابَ"
_CONDITIONAL = "إِنْ فَتَحَ زَيْدٌ الْبَابَ"


def _bridge(text: str):  # type: ignore[no-untyped-def]
    store = door_domain_store()
    register = door_world_register(store)
    return bridge_utterance(
        reading=read_utterance(text.encode()),
        store=store,
        register=register,
        time_scope=THE_QUESTION_INTERVAL,
        surface_candidates=surface_candidates(),
    )


# ----- القراءةُ مشتقّةٌ من البايتات لا منقولةٌ بجدول -----


def test_the_five_constructions_are_read_from_vowels_alone() -> None:
    assert (
        read_utterance(_ACTIVE.encode()).construction is Construction.ACTIVE_TRANSITIVE
    )
    assert (
        read_utterance(_PASSIVE.encode()).construction
        is Construction.PASSIVE_ONE_NOMINATIVE
    )
    assert (
        read_utterance(_FORM_VII.encode()).construction
        is Construction.FORM_VII_ONE_NOMINATIVE
    )
    assert (
        read_utterance(_NEGATED.encode()).construction
        is Construction.NEGATED_ACTIVE_TRANSITIVE
    )
    assert (
        read_utterance(_CONDITIONAL.encode()).construction
        is Construction.CONDITIONAL_ACTIVE_TRANSITIVE
    )


def test_the_root_is_extracted_from_every_one_of_the_four_verb_shapes() -> None:
    for text in (_ACTIVE, _PASSIVE, _FORM_VII, _NEGATED):
        verb = read_utterance(text.encode()).verb
        assert verb is not None
        assert verb.root_letters == ("ف", "ت", "ح")


def test_a_proper_name_and_a_frozen_noun_keep_their_root_withheld() -> None:
    for surface in ("زَيْدٌ", "الْبَابَ", "الْبَابُ"):
        reading = read_word(surface)
        assert reading.shape.is_noun
        assert reading.root_is_withheld
        assert reading.root_letters == ()


def test_a_ready_made_string_is_refused_because_the_digest_is_on_the_bytes() -> None:
    with pytest.raises(SurfaceAnalysisError):
        read_utterance(_ACTIVE)  # type: ignore[arg-type]


def test_an_unread_construction_is_named_and_never_coerced() -> None:
    reading = read_utterance("زَيْدٌ زَيْدٌ".encode())
    assert reading.construction is Construction.UNRECOGNISED
    assert all(
        function is SyntacticFunction.UNASSIGNED for function in reading.functions
    )
    with pytest.raises(BridgeError):
        _bridge("زَيْدٌ زَيْدٌ")


# ----- الفاعلُ النحويُّ ليس الدورَ الدلاليّ -----


def test_the_active_construction_separates_the_two_designated_roles() -> None:
    event = _bridge(_ACTIVE).content.event
    assert event.event_type_id == DOOR_OPENING_EVENT_ID
    agent = event.filling(DOOR_AGENT_ROLE_ID)
    patient = event.filling(DOOR_PATIENT_ROLE_ID)
    assert agent.standing is FillerStanding.DESIGNATED
    assert patient.standing is FillerStanding.DESIGNATED
    assert agent.designation is not None
    assert patient.designation is not None
    assert agent.designation.candidate_individual_ids == (ZAYD_INDIVIDUAL_ID,)
    assert patient.designation.candidate_individual_ids == (DOOR_INDIVIDUAL_ID,)


def test_the_passive_nominative_fills_the_patient_not_the_agent() -> None:
    event = _bridge(_PASSIVE).content.event
    patient = event.filling(DOOR_PATIENT_ROLE_ID)
    agent = event.filling(DOOR_AGENT_ROLE_ID)
    assert patient.standing is FillerStanding.DESIGNATED
    assert patient.designation is not None
    assert patient.designation.candidate_individual_ids == (DOOR_INDIVIDUAL_ID,)
    assert agent.standing is FillerStanding.UNNAMED_IN_THE_UTTERANCE
    assert agent.standing is not FillerStanding.DENIED_BY_THE_UTTERANCE
    assert agent.designation is None


def test_form_vii_profiles_no_agent_role_at_all_and_denies_nothing() -> None:
    event = _bridge(_FORM_VII).content.event
    assert event.event_type_id == FORM_VII_EVENT_ID
    assert event.filling(FORM_VII_PATIENT_ROLE_ID).standing is FillerStanding.DESIGNATED
    store = door_domain_store()
    role_ids = {role.role_id for role in store.event_type_of(FORM_VII_EVENT_ID).roles}
    assert DOOR_AGENT_ROLE_ID not in role_ids
    standings = {filling.standing for filling in event.role_fillings}
    assert FillerStanding.DENIED_BY_THE_UTTERANCE not in standings


def test_the_passive_and_the_active_disagree_only_about_the_agent() -> None:
    active = _bridge(_ACTIVE).content.event
    passive = _bridge(_PASSIVE).content.event
    assert active.event_type_id == passive.event_type_id
    assert (
        active.filling(DOOR_PATIENT_ROLE_ID).standing
        is passive.filling(DOOR_PATIENT_ROLE_ID).standing
    )
    assert (
        active.filling(DOOR_AGENT_ROLE_ID).standing
        is not passive.filling(DOOR_AGENT_ROLE_ID).standing
    )


# ----- الأثرُ يُسمّي ما استقبله وما أضافه -----


def test_the_trace_separates_the_derived_the_imported_and_the_stipulated() -> None:
    result = _bridge(_NEGATED)
    derived = result.items_of(ProvenanceGenus.DERIVED_FROM_BYTES)
    imported = result.items_of(ProvenanceGenus.IMPORTED_FROM_A_SOURCE)
    stipulated = result.items_of(ProvenanceGenus.STIPULATED_FOR_THE_DOMAIN)
    unknown = result.items_of(ProvenanceGenus.UNKNOWN)
    assert derived and imported and stipulated and unknown
    assert {"التركيب", "جذر-الفعل", "النفي"} <= {item.label for item in derived}
    assert "المعنى-المعتمد" in {item.label for item in imported}
    assert "تضييق-المعنى" in {item.label for item in stipulated}


def test_the_extension_points_are_named_and_left_suspended() -> None:
    result = _bridge(_ACTIVE)
    assert len(result.suspended_extension_points) == 4
    joined = " ".join(result.suspended_extension_points)
    for word in ("الحال", "التمييز", "المشتقّ", "المجاز"):
        assert word in joined
    assert "تعارضُ قيدٍ نوعيٍّ ليس مجازًا تلقائيًّا" in joined


# ----- المعنى مستوردٌ، والتضييقُ مُصطلَحٌ عليه -----


def test_the_imported_sense_carries_its_source_digest_and_establishes_nothing() -> None:
    scope = Scope(domain_id="مجال-الأبواب", timeline_id=None, start=None, end=None)
    imported = import_sense_of_root("فتح", scope)
    assert imported.entry_number == "2921"
    assert imported.semantic_axes == ("خلاف الاغلاق",)
    assert imported.evidence.source_digest is not None
    assert not imported.evidence.establishes_facts
    assert "الفاء والتاء والحاء" in imported.body_excerpt


def test_the_physical_narrowing_is_a_stipulation_not_read_off_the_entry() -> None:
    scope = Scope(domain_id="مجال-الأبواب", timeline_id=None, start=None, end=None)
    stipulation = physical_opening_stipulation(scope)
    assert stipulation.genus is EvidenceGenus.STIPULATED_DEFINITION
    assert stipulation.genus.is_substance_founding
    assert not stipulation.establishes_facts
    assert "الحُكْم" in import_sense_of_root("فتح", scope).body_excerpt


def test_a_root_with_no_entry_is_refused_rather_than_approximated() -> None:
    scope = Scope(domain_id="مجال-الأبواب", timeline_id=None, start=None, end=None)
    with pytest.raises(LexicalSenseError):
        import_sense_of_root("زززز", scope)


# ----- صياغاتٌ وأفرادٌ لم تُكتَب الإجابةُ لهم -----


def test_an_unseen_individual_and_an_unseen_pairing_still_go_through() -> None:
    store = door_domain_store()
    register = door_world_register(store)
    result = bridge_utterance(
        reading=read_utterance("فَتَحَ بَكْرٌ الْبَابَ".encode()),
        store=store,
        register=register,
        time_scope=THE_QUESTION_INTERVAL,
        surface_candidates=surface_candidates(),
    )
    agent = result.content.event.filling(DOOR_AGENT_ROLE_ID)
    assert agent.standing is FillerStanding.DESIGNATED
    assert agent.designation is not None
    assert agent.designation.candidate_individual_ids == ()
    unknown_labels = {item.label for item in result.items_of(ProvenanceGenus.UNKNOWN)}
    assert "تعيين:بَكْرٌ" in unknown_labels


def test_an_unseen_shape_that_also_reads_keeps_the_same_path() -> None:
    reading = read_utterance("فَتَحَ خَالِدٌ الْبَابَ".encode())
    assert reading.construction is Construction.ACTIVE_TRANSITIVE
    assert reading.functions[1] is SyntacticFunction.NOMINATIVE_AFTER_VERB


def test_the_differentiating_waw_of_amr_is_a_named_suspension_not_a_silent_guess() -> (
    None
):
    assert read_word("عَمْرٌو").shape is WordShape.UNRECOGNISED
    assert "واوُ «عَمْرٌو» الفارقة" in A_SILENT_ORTHOGRAPHIC_APPENDAGE_IS_A_NAMED_SUSPENSION
    with pytest.raises(BridgeError):
        _bridge("فَتَحَ عَمْرٌو الْبَابَ")


def test_a_verb_outside_the_licensed_root_is_refused_not_bent() -> None:
    reading = read_utterance("كَتَبَ زَيْدٌ الْبَابَ".encode())
    assert reading.construction is Construction.ACTIVE_TRANSITIVE
    verb = reading.verb
    assert verb is not None
    assert verb.root_letters == ("ك", "ت", "ب")
    assert verb.shape is WordShape.VERB_FORM_I_ACTIVE_PERFECT
    with pytest.raises(BridgeError):
        _bridge("كَتَبَ زَيْدٌ الْبَابَ")
