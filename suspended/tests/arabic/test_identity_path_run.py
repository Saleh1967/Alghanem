"""اختباراتُ مسار الهويّة — **شواهدُ مصدريّةٌ واقعيّةٌ قابلةٌ لإعادة الاستخراج**.

المواضعُ الثلاثةُ تُقطَع من `corpora/quran-simple-enhanced.txt` بختمه وتُقابَل
بايتةً بايتة. وما سوى الموضع (مَن يحمل الاسم، ومتى وُحِّد) مفروضٌ مُعلَنٌ في
`identity_path_run`، وليس فيه جنسُ `DIRECT_OBSERVATION` البتّة.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from alghanem.arabic.identity_path_run import (
    FIRST_ZAYD,
    SECOND_ZAYD,
    THE_CITY,
    THE_LINK,
    THE_SOURCE_SEAL,
    agreeing_link,
    base_network,
    base_register,
    declared_evidence,
    declared_occurrences,
    full_run,
)
from alghanem.ontology import (
    CanonicalStanding,
    DesignationMethod,
    Evidence,
    EvidenceGenus,
    ExistenceStanding,
    IdentityError,
    Individual,
    NamedKind,
    Naming,
    NamingGenus,
    Occurrence,
    OffsetUnit,
    RepresentationStanding,
    Scope,
    candidates_for_surface,
    canonical_reading,
    linked_individual_ids,
    witness_occurrence,
)

ROOT = Path(__file__).resolve().parents[2]


# ----- الموضعُ يُقابَل بالبايتات -----


def test_the_three_deposited_positions_are_cut_and_matched() -> None:
    for occurrence in declared_occurrences():
        witness = witness_occurrence(occurrence, ROOT)
        assert witness.standing is RepresentationStanding.REPRODUCED, witness.note
        assert witness.cut_text == occurrence.surface
        assert witness.measured_sha256 == THE_SOURCE_SEAL


def test_a_position_moved_by_one_fails_the_witness_and_names_why() -> None:
    first = declared_occurrences()[0]
    moved = Occurrence(
        occurrence_id=first.occurrence_id,
        source_path=first.source_path,
        source_sha256=first.source_sha256,
        offset_unit=first.offset_unit,
        start=first.start + 1,
        end=first.end + 1,
        surface=first.surface,
    )
    witness = witness_occurrence(moved, ROOT)
    assert witness.standing is RepresentationStanding.TEXT_DOES_NOT_MATCH
    assert witness.cut_text != first.surface


def test_a_wrong_seal_is_refused_as_a_seal_not_as_a_missing_witness() -> None:
    first = declared_occurrences()[0]
    forged = Occurrence(
        occurrence_id=first.occurrence_id,
        source_path=first.source_path,
        source_sha256="0" * 64,
        offset_unit=first.offset_unit,
        start=first.start,
        end=first.end,
        surface=first.surface,
    )
    witness = witness_occurrence(forged, ROOT)
    assert witness.standing is RepresentationStanding.SEAL_MISMATCH
    assert witness.measured_sha256 == THE_SOURCE_SEAL


def test_an_absent_source_is_a_third_standing_of_its_own() -> None:
    first = declared_occurrences()[0]
    missing = Occurrence(
        occurrence_id=first.occurrence_id,
        source_path="corpora/لا-يوجد.txt",
        source_sha256=first.source_sha256,
        offset_unit=first.offset_unit,
        start=first.start,
        end=first.end,
        surface=first.surface,
    )
    witness = witness_occurrence(missing, ROOT)
    assert witness.standing is RepresentationStanding.SOURCE_MISSING
    assert witness.standing is not RepresentationStanding.SEAL_MISMATCH


# ----- المسارُ لا يُمرَّر قبل شهادته -----


def test_the_hundred_sixteen_is_not_run_before_a_reproduced_witness() -> None:
    first = declared_occurrences()[0]
    forged = Occurrence(
        occurrence_id=first.occurrence_id,
        source_path=first.source_path,
        source_sha256="0" * 64,
        offset_unit=first.offset_unit,
        start=first.start,
        end=first.end,
        surface=first.surface,
    )
    with pytest.raises(Exception):
        canonical_reading(forged, witness_occurrence(forged, ROOT))


def test_a_suspended_premise_is_named_and_never_called_complete() -> None:
    outcome = full_run(ROOT)
    by_id = {one.occurrence_id: one for one in outcome.readings}
    assert by_id["وقوع-المدينة"].standing is CanonicalStanding.NOT_READY
    assert by_id["وقوع-المدينة"].derived_text is None
    assert not by_id["وقوع-المدينة"].standing.is_complete
    assert by_id["وقوع-زيد"].standing is CanonicalStanding.READY_AND_REPRODUCED


def test_the_consumed_field_is_derived_from_the_replay_not_the_record() -> None:
    first = declared_occurrences()[0]
    witness = witness_occurrence(first, ROOT)
    honest = canonical_reading(first, witness)
    from canonical116.bridge import bridge, verify

    record = bridge(first.surface.encode("utf-8"))
    record["canonical_text"] = "نصٌّ محرَّفٌ لا أصلَ له"
    assert verify(record)["reproduced"] is True
    assert verify(record)["replay"]["canonical_text"] != record["canonical_text"]
    assert honest.derived_text == verify(record)["replay"]["canonical_text"]


# ----- اسمان لفردٍ واحد، وفردان باسمٍ واحد -----


def test_the_city_keeps_one_identifier_under_two_names() -> None:
    outcome = full_run(ROOT)
    assert outcome.city_names == ("الْمَدِينَةِ", "يَثْرِبَ")
    register = base_register()
    network = base_network(register)
    for surface in ("يَثْرِبَ", "الْمَدِينَةِ"):
        found = candidates_for_surface(surface, network, register)
        assert tuple(one.individual_id for one in found) == (THE_CITY,)


def test_two_bearers_of_zayd_stay_apart_until_a_link_is_bought() -> None:
    outcome = full_run(ROOT)
    assert tuple(one.individual_id for one in outcome.zayd_candidates) == (
        FIRST_ZAYD,
        SECOND_ZAYD,
    )
    assert outcome.linked_before == ()
    assert outcome.linked_after_link == (SECOND_ZAYD,)


def test_adding_a_third_bearer_is_a_data_line_not_an_engine_change() -> None:
    register = base_register()
    evidence = Evidence(
        evidence_id="دليل-وجود-زيد-الثالث",
        genus=EvidenceGenus.DECLARED_HYPOTHESIS,
        statement="فردٌ ثالثٌ يُسمّى «زيد»، مضافٌ في الاختبار بيانًا لا شفرة",
        source_name="فرضٌ مُعلَنٌ في هذا الاختبار",
        scope=Scope(domain_id="مجال-شبكة-الهويّة"),
    )
    register = register.with_evidence(evidence).with_individual(
        Individual(
            individual_id="فرد-زيد-الثالث",
            designation_method=DesignationMethod.PROPER_NAME,
            candidate_type_ids=("نوع-الإنسان",),
            existence=ExistenceStanding.ASSUMED_FOR_THE_DISCOURSE,
            evidence_ref=evidence.ref,
        )
    )
    network = base_network(register).with_naming(
        Naming(
            naming_id="تسمية-زيد-الثالث",
            surface="زيد",
            named_id="فرد-زيد-الثالث",
            named_kind=NamedKind.INDIVIDUAL,
            genus=NamingGenus.PROPER_NAME,
            language_id="ar",
            scope=Scope(domain_id="مجال-شبكة-الهويّة"),
            evidence_ref=evidence.ref,
        ),
        register,
    )
    found = candidates_for_surface("زيد", network, register)
    assert len(found) == 3
    assert "فرد-زيد-الثالث" in {one.individual_id for one in found}


# ----- المراجعةُ تمسّ التابعَ وحدَه -----


def test_the_derived_claim_is_suspended_by_the_retraction_and_only_it() -> None:
    outcome = full_run(ROOT)
    assert outcome.arrival_before_link == "غيرُ مودَعة"
    assert outcome.arrival_after_link == "مدعومة"
    assert outcome.arrival_after_retraction == "معلَّقة"
    assert outcome.arrival_after_independent == "مدعومة"


def test_retracting_the_link_leaves_the_direct_claim_standing() -> None:
    register = base_register()
    register = register.with_proposition(
        __import__("alghanem.ontology", fromlist=["Proposition"]).Proposition(
            proposition_id="قضيّة-وصول-الأوّل",
            form=__import__(
                "alghanem.ontology", fromlist=["PropositionForm"]
            ).PropositionForm.EVENT_OCCURRED,
            subject_id=FIRST_ZAYD,
            predicate_id="حدث-الوصول",
            value=None,
            polarity=__import__(
                "alghanem.ontology", fromlist=["Polarity"]
            ).Polarity.AFFIRMED,
            scope=Scope(
                domain_id="مجال-شبكة-الهويّة",
                timeline_id="محور-سنوات-الهجرة",
                start=5,
                end=5,
            ),
            evidence_ref=register.evidence_of("دليل-وصول-الأوّل").ref,
        )
    )
    after = register.retract("دليل-رابط-الهويّة")
    assert after.proposition_of("قضيّة-وصول-الأوّل").suspended is False


def test_an_unrelated_evidence_change_moves_no_verdict() -> None:
    register = base_register()
    before = tuple(one.suspended for one in register.propositions)
    after = register.retract("دليل-لا-متعلّق")
    assert tuple(one.suspended for one in after.propositions) == before


def test_the_conflict_policy_is_declared_and_its_reach_is_measured() -> None:
    outcome = full_run(ROOT)
    assert outcome.suspended_by_policy == (THE_LINK,)


def test_a_link_naming_an_unregistered_individual_is_refused() -> None:
    register = base_register()
    network = base_network(register)
    link = agreeing_link(register)
    forged = type(link)(
        link_id="رابط-غريب",
        left_individual_id="فرد-لا-وجودَ-له",
        right_individual_id=SECOND_ZAYD,
        criterion_id=link.criterion_id,
        key_readings=link.key_readings,
        evidence_ref=link.evidence_ref,
    )
    with pytest.raises(Exception):
        network.with_link(forged, register)


# ----- لا مشاهدةَ يكتبها اختبار -----


def test_no_declared_evidence_claims_a_direct_observation() -> None:
    genera = {one.genus for one in declared_evidence()}
    assert EvidenceGenus.DIRECT_OBSERVATION not in genera
    assert EvidenceGenus.MEASUREMENT in genera


def test_the_measurement_genus_belongs_only_to_the_sealed_cut() -> None:
    measured = tuple(
        one for one in declared_evidence() if one.genus is EvidenceGenus.MEASUREMENT
    )
    assert len(measured) == 1
    assert measured[0].source_digest == THE_SOURCE_SEAL


# ----- التسميةُ لا تُولِّد صفةً -----


def test_naming_the_city_does_not_make_it_a_kind_of_its_name() -> None:
    register = base_register()
    network = base_network(register)
    city = register.individual_of(THE_CITY)
    assert city.candidate_type_ids == ("نوع-المدينة",)
    assert linked_individual_ids(THE_CITY, network) == ()


def test_a_criterion_with_one_key_cannot_be_used_here_either() -> None:
    from alghanem.ontology import IdentityCriterion

    with pytest.raises(IdentityError):
        IdentityCriterion(
            criterion_id="معيار-ناقص",
            key_names=("سنة-الميلاد",),
            scope=Scope(domain_id="مجال-شبكة-الهويّة"),
            authority="سجلُّ تراجمِ المجال المفروض",
        )


def test_the_offset_unit_is_part_of_the_claim_not_a_detail() -> None:
    first = declared_occurrences()[0]
    assert first.offset_unit is OffsetUnit.CODEPOINT
    as_bytes = Occurrence(
        occurrence_id=first.occurrence_id,
        source_path=first.source_path,
        source_sha256=first.source_sha256,
        offset_unit=OffsetUnit.UTF8_BYTE,
        start=first.start,
        end=first.end,
        surface=first.surface,
    )
    assert witness_occurrence(as_bytes, ROOT).standing is not (
        RepresentationStanding.REPRODUCED
    )
