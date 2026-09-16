"""اختباراتُ قياس فرضية «المصدر أوّلًا» على صفوفٍ مُصطنَعةٍ مُصرَّحٍ بجنسها.

ولا رقمَ في هذه الاختبارات مأخوذٌ من بايتات MASAQ: بايتاتُها لم تُفتَح في هذه
الشجرة، ومنزلةُ القياس `لم_تُفتَح_البايتات` مُعلَنة. والمُختبَرُ هنا **أنبوبُ
الاشتقاق وحارِسُه**: أنّ المصدرَ يُعَدّ كما وُسِم، وأنّ ما لا وزنَ له لا
يُحسَب فاصلًا ولا مشترَكًا، وأنّ الدعوى (ج) ترفع مانعَها بدل أن تُخرِج رقمًا.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.masaq_corpus_witness import MasaqColumnBinding, parse_masaq_rows
from alghanem.arabic.masdar_priority_census import (
    CENSUS_STANDING,
    MASDAR_CENSUS_NAMED_RESIDUALS,
    REDERIVED_FIGURES,
    UNTAGGED_FORM_LABEL,
    CensusStanding,
    MasdarPriorityCensusError,
    arriving_figures_without_a_rederivation,
    discrimination_table,
    masdar_records,
    permutation_test,
    root_profiles,
    single_root_witness,
    transitivity_from_masdar,
)
from alghanem.arabic.masdar_priority_preregistration import (
    ARRIVING_MASDAR_FIGURES,
    LEGISLATION_BARRIERS,
    MASDAR_CLAIMS,
    MASDAR_PERMUTATION_PROTOCOL,
    MASDAR_PRIORITY_PREREGISTRATION_DIGEST,
    ORDERING_OBJECTION,
    RegistrationStanding,
    claim_by_label,
    preregistration_digest,
)
from alghanem.arabic.masdar_priority_preregistration import (
    STANDING as REGISTRATION_STANDING,
)

BINDING = MasaqColumnBinding(
    declared_by="اختبارٌ مُصطنَع؛ لا حائزَ بايتاتٍ أعلن هذه الأسماء",
    what_it_assumes="أسماءُ الأعمدة مكتوبةٌ في الاختبار لا مقروءةٌ من ملفّ",
    location_column="location",
    form_column="form",
    morphological_tag_column="tag",
    root_column="root",
    lemma_column="lemma",
    verb_form_column="verb_form",
    masdar_tag_values=("GERUND",),
    meemi_masdar_tag_values=("GERUND_MEEM",),
)

SYNTHETIC_CSV = (
    "location,form,tag,root,lemma,verb_form\n"
    "(2:3:2:1),qiyAm,GERUND,qwm,qiyAm,\n"
    "(2:43:2:1),<iqAmp,GERUND,qwm,<iqAmp,IV\n"
    "(4:103:5:1),tqwym,GERUND,qwm,taqwiym,II\n"
    "(2:125:4:1),mqAm,GERUND_MEEM,qwm,maqAm,\n"
    "(1:2:1:1),qAm,V,qwm,qAma,\n"
    "(2:2:2:1),kitAb,GERUND,ktb,kitAbap,I\n"
    "(3:3:3:1),kitAb,GERUND,ktb,kitAbap,II\n"
    "(5:5:5:1),Darob,GERUND,Drb,Darob,I\n"
)


def records():  # type: ignore[no-untyped-def]
    return masdar_records(parse_masaq_rows(SYNTHETIC_CSV, BINDING), BINDING)


def test_the_standing_says_the_bytes_were_not_opened() -> None:
    assert CENSUS_STANDING is CensusStanding.BYTES_NOT_OPENED
    assert REDERIVED_FIGURES == ()
    assert arriving_figures_without_a_rederivation() == ARRIVING_MASDAR_FIGURES


def test_the_registration_is_frozen_and_declares_it_came_after_the_number() -> None:
    assert preregistration_digest() == MASDAR_PRIORITY_PREREGISTRATION_DIGEST
    assert REGISTRATION_STANDING is RegistrationStanding.FORMULATED_AFTER_THE_NUMBER


def test_each_of_the_three_claims_has_its_own_falsifier() -> None:
    assert len(MASDAR_CLAIMS) == 3
    falsifiers = {claim.what_would_falsify_it for claim in MASDAR_CLAIMS}
    assert len(falsifiers) == 3
    assert claim_by_label("أ_المصدر_يُميِّز_الوزن").counting_rule.name == (
        "MASDAR_FORM_PAIRS"
    )


def test_only_tagged_masdars_are_counted_and_untagged_forms_are_named() -> None:
    measured = records()
    assert len(measured) == 7
    assert all(record.morphological_tag != "V" for record in measured)
    assert any(record.verb_form == UNTAGGED_FORM_LABEL for record in measured)


def test_a_masdar_without_a_tagged_root_is_left_out_not_guessed() -> None:
    rootless = SYNTHETIC_CSV + "(9:9:9:1),xyz,GERUND,,xyz,IV\n"
    measured = masdar_records(parse_masaq_rows(rootless, BINDING), BINDING)
    assert all(record.root.strip() for record in measured)
    assert len(measured) == 7


def test_the_discrimination_table_counts_the_shared_beside_the_separating() -> None:
    table = discrimination_table(records(), BINDING)
    assert table.masdar_roots == 3
    assert table.roots_with_more_than_one_masdar == 1
    assert table.distinct_masdars == 6
    assert table.masdars_with_a_tagged_form == 4
    assert table.masdars_separating_one_form == 3
    assert table.masdars_shared_between_forms == 1
    assert table.separation_rate == pytest.approx(75.0)
    assert table.preregistration_digest == MASDAR_PRIORITY_PREREGISTRATION_DIGEST


def test_an_untagged_form_is_neither_separating_nor_shared() -> None:
    table = discrimination_table(records(), BINDING)
    assert (
        table.masdars_separating_one_form + table.masdars_shared_between_forms
        == table.masdars_with_a_tagged_form
    )
    assert table.masdars_with_a_tagged_form < table.distinct_masdars


def test_the_permutation_p_value_never_reaches_zero() -> None:
    outcome = permutation_test(records(), "اختبارٌ مُصطنَع")
    assert outcome.p_value >= MASDAR_PERMUTATION_PROTOCOL.p_value_floor
    assert outcome.p_value > 0.0
    assert outcome.sample_size == 5


def test_the_single_root_witness_is_one_root_not_a_rate() -> None:
    profile = single_root_witness(records(), "qwm")
    assert profile.distinct_masdar_count == 4
    assert dict(profile.forms_by_lemma)["<iqAmp"] == ("IV",)
    assert dict(profile.forms_by_lemma)["qiyAm"] == (UNTAGGED_FORM_LABEL,)


def test_an_unattested_root_is_refused_not_invented() -> None:
    with pytest.raises(MasdarPriorityCensusError):
        single_root_witness(records(), "zzz")


def test_claim_c_raises_its_barrier_instead_of_returning_a_number() -> None:
    with pytest.raises(MasdarPriorityCensusError) as error:
        transitivity_from_masdar("qwm")
    assert LEGISLATION_BARRIERS[1].the_rule_that_is_missing in str(error.value)


def test_the_named_residuals_carry_the_four_required_limits() -> None:
    for name in (
        "AHumanTagIsNotAMeasurement",
        "OneRootIsNotACorpus",
        "APresentMasdarIsNotAMeasuredTransitivity",
        "AbsenceInACorpusIsNotImpossibility",
    ):
        assert name in MASDAR_CENSUS_NAMED_RESIDUALS


def test_the_ordering_objection_is_recorded_without_being_executed() -> None:
    assert ORDERING_OBJECTION.the_order_it_proposes.startswith("مصدر")
    assert "جذرٌ واحد" in ORDERING_OBJECTION.evidence_borne
    assert ORDERING_OBJECTION.what_would_let_it_be_executed.strip()


def test_root_profiles_are_ordered_by_code_point_not_by_arrival() -> None:
    roots = [profile.root for profile in root_profiles(records())]
    assert roots == sorted(roots)
