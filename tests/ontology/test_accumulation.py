"""اختباراتُ رصيد `K_t` — **اصطناعيّةٌ لعقود العمليّات**.

لا شاهدَ مصدريًّا ههنا بحال: الأدلّةُ مفروضةٌ لفحص العقود وحدَها. والشواهدُ
المصدريّةُ الواقعيّةُ في `tests/arabic/test_accumulation_run.py`، مفصولةٌ عن
هذه، ولا اتّصالَ لغويًّا في الموضعين.

وقاعدةُ هذا الملفّ: **المتوقَّعُ لا يستدعي المفحوص**. فما يُنتظَر من
`claim_verdict` و`type_reading` يُكتَب رقمًا أو اسمًا بيد، لا يُولَّد بإعادة
استدعاء الدالّة نفسِها.
"""

from __future__ import annotations

import pytest

from alghanem.ontology import (
    AccumulationError,
    AdmissionLicence,
    AdoptionLicence,
    ClaimKey,
    ClaimStanding,
    Correction,
    DesignationMethod,
    Evidence,
    EvidenceGenus,
    ExistenceStanding,
    FactRegister,
    IdentityNetwork,
    IncompatibilityWitness,
    Individual,
    InferenceRule,
    KnowledgeStock,
    Polarity,
    Proposition,
    PropositionForm,
    ReinstatementPolicy,
    RuleKind,
    RuleOrigin,
    Scope,
    claim_verdict,
    independent_supports,
)
from alghanem.ontology.facts import FactError
from alghanem.ontology.operations import OperationError

THE_SCOPE = Scope(domain_id="مجال-اصطناعيّ")
OTHER_SCOPE = Scope(domain_id="مجال-آخرُ-اصطناعيّ")


def _evidence(
    evidence_id: str,
    genus: EvidenceGenus = EvidenceGenus.ACCEPTED_REPORT,
    statement: str = "تقريرٌ مقبولٌ مفروضٌ لفحص العقد",
    scope: Scope = THE_SCOPE,
) -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        genus=genus,
        statement=statement,
        source_name="مصدرٌ مفروض",
        scope=scope,
    )


def _individual(individual_id: str, evidence: Evidence) -> Individual:
    return Individual(
        individual_id=individual_id,
        designation_method=DesignationMethod.PROPER_NAME,
        candidate_type_ids=(),
        existence=ExistenceStanding.ESTABLISHED,
        evidence_ref=evidence.ref,
    )


def _membership(
    proposition_id: str,
    subject: str,
    type_id: str,
    evidence: Evidence,
    scope: Scope = THE_SCOPE,
    polarity: Polarity = Polarity.AFFIRMED,
) -> Proposition:
    return Proposition(
        proposition_id=proposition_id,
        form=PropositionForm.TYPE_MEMBERSHIP,
        subject_id=subject,
        predicate_id=type_id,
        value=None,
        polarity=polarity,
        scope=scope,
        evidence_ref=evidence.ref,
    )


def _licence(proposition: Proposition, order: int) -> AdmissionLicence:
    return AdmissionLicence(
        proposition_id=proposition.proposition_id,
        scope=proposition.scope,
        evidence_ref=proposition.evidence_ref,
        recorded_order=order,
        depends_on_proposition_ids=proposition.derived_from_proposition_ids,
    )


def _stock(
    *evidence: Evidence, individuals: tuple[str, ...] = ("فرد",)
) -> KnowledgeStock:
    register = FactRegister(register_id="سجلّ-اصطناعيّ")
    for one in evidence:
        register = register.with_evidence(one)
    for individual_id in individuals:
        register = register.with_individual(_individual(individual_id, evidence[0]))
    return KnowledgeStock(
        stock_id="رصيد-اصطناعيّ",
        version=0,
        register=register,
        identity=IdentityNetwork(network_id="شبكة-اصطناعيّة"),
    )


def _rule(evidence: Evidence, rule_id: str = "قاعدة") -> InferenceRule:
    return InferenceRule(
        rule_id=rule_id,
        version="1",
        kind=RuleKind.STRICT_IN_THE_DECLARED_MODEL,
        premise_patterns=("مقدّمة",),
        conclusion_pattern="نتيجة",
        applicability_note="تنطبق في النطاق المُعلَن وحدَه",
        blocker_ids=(),
        evidence_ref=evidence.ref,
    )


# ----- الترخيصان متمايزان -----


def test_the_adoption_licence_refuses_a_rule_name_without_its_version() -> None:
    evidence = _evidence("دليل")
    with pytest.raises(AccumulationError):
        AdoptionLicence(
            rule_versioned_id="قاعدة",
            origin=RuleOrigin.TRANSMITTED_FROM_A_SOURCE,
            condition_note="شرطٌ مُعلَن",
            evidence_ref=evidence.ref,
        )


def test_an_imported_rule_is_recorded_but_never_licenses_an_application() -> None:
    source = _evidence("دليل-مصدر", EvidenceGenus.STIPULATED_DEFINITION)
    rule = _rule(source)
    adoption = _evidence(
        "دليل-اعتماد",
        EvidenceGenus.STIPULATED_DEFINITION,
        f"أُدخِلت `{rule.versioned_id}` بلا تبرير",
    )
    stock = _stock(_evidence("دليل-وقائع"), source, adoption)
    stock = stock.adopt_rule(
        rule,
        AdoptionLicence(
            rule_versioned_id=rule.versioned_id,
            origin=RuleOrigin.IMPORTED_UNJUSTIFIED,
            condition_note="لا شرطَ مُعلَن",
            evidence_ref=adoption.ref,
        ),
        adoption,
    )
    assert stock.rule_of(rule.versioned_id) is not None
    assert stock.is_adopted(rule.versioned_id) is False


def test_the_adoption_evidence_must_name_the_rule_it_adopts() -> None:
    source = _evidence("دليل-مصدر", EvidenceGenus.STIPULATED_DEFINITION)
    rule = _rule(source)
    adoption = _evidence(
        "دليل-اعتماد", EvidenceGenus.STIPULATED_DEFINITION, "اعتمادٌ بلا تسميةٍ لشيء"
    )
    stock = _stock(_evidence("دليل-وقائع"), source, adoption)
    with pytest.raises(AccumulationError):
        stock.adopt_rule(
            rule,
            AdoptionLicence(
                rule_versioned_id=rule.versioned_id,
                origin=RuleOrigin.TRANSMITTED_FROM_A_SOURCE,
                condition_note="شرطٌ مُعلَن",
                evidence_ref=adoption.ref,
            ),
            adoption,
        )


def test_an_admission_licence_that_names_another_judgment_is_refused() -> None:
    evidence = _evidence("دليل")
    stock = _stock(evidence)
    proposition = _membership("حكم", "فرد", "نوع", evidence)
    stray = AdmissionLicence(
        proposition_id="حكمٌ-آخر",
        scope=THE_SCOPE,
        evidence_ref=evidence.ref,
        recorded_order=1,
    )
    with pytest.raises(AccumulationError):
        stock.admit(proposition, stray)


# ----- تعدّدُ البراهين وقياسُ استقلالها -----


def _two_supports() -> KnowledgeStock:
    first = _evidence("دليل-أوّل")
    second = _evidence("دليل-ثانٍ")
    stock = _stock(first, second)
    one = _membership("حكم-أوّل", "فرد", "نوع", first)
    two = _membership("حكم-ثانٍ", "فرد", "نوع", second)
    return stock.admit(one, _licence(one, 1)).admit(two, _licence(two, 2))


def test_two_supports_from_two_sources_are_two_independent_families() -> None:
    stock = _two_supports()
    claim = ClaimKey(
        subject_id="فرد",
        predicate_id="نوع",
        value=None,
        polarity=Polarity.AFFIRMED,
        scope=THE_SCOPE,
    )
    verdict = stock.verdict_for(claim)
    assert verdict.standing is ClaimStanding.SUPPORTED_IN_SCOPE
    assert verdict.independent_support_count == 2
    assert verdict.survives_one_retraction is True


def test_retracting_one_of_two_independent_supports_keeps_the_claim() -> None:
    stock = _two_supports().retract_evidence("دليل-أوّل")
    claim = ClaimKey(
        subject_id="فرد",
        predicate_id="نوع",
        value=None,
        polarity=Polarity.AFFIRMED,
        scope=THE_SCOPE,
    )
    verdict = stock.verdict_for(claim)
    assert verdict.standing is ClaimStanding.SUPPORTED_IN_SCOPE
    assert verdict.supporting_proposition_ids == ("حكم-ثانٍ",)
    assert verdict.independent_support_count == 1


def test_retracting_the_only_support_drops_the_claim() -> None:
    evidence = _evidence("دليل-وحيد")
    stock = _stock(evidence)
    only = _membership("حكم", "فرد", "نوع", evidence)
    stock = stock.admit(only, _licence(only, 1)).retract_evidence("دليل-وحيد")
    claim = ClaimKey(
        subject_id="فرد",
        predicate_id="نوع",
        value=None,
        polarity=Polarity.AFFIRMED,
        scope=THE_SCOPE,
    )
    assert stock.verdict_for(claim).supporting_proposition_ids == ()


def test_a_redeposited_derived_result_is_not_a_second_independent_support() -> None:
    source = _evidence("دليل-مصدر", EvidenceGenus.STIPULATED_DEFINITION)
    rule = _rule(source)
    base = _evidence("دليل-أساس")
    stock = _stock(base, source)
    premise = _membership("حكم-المقدّمة", "فرد", "مقدّمة", base)
    stock = stock.admit(premise, _licence(premise, 1))
    derived = Proposition(
        proposition_id="حكم-مشتقّ",
        form=PropositionForm.TYPE_MEMBERSHIP,
        subject_id="فرد",
        predicate_id="نوع",
        value=None,
        polarity=Polarity.AFFIRMED,
        scope=THE_SCOPE,
        evidence_ref=base.ref,
        derived_from_proposition_ids=("حكم-المقدّمة",),
        derived_by_rule=rule.versioned_id,
    )
    stock = stock.admit(derived, _licence(derived, 2))
    direct = _membership("حكم-مباشر", "فرد", "نوع", base)
    stock = stock.admit(direct, _licence(direct, 3))
    families = independent_supports(stock.register, ("حكم-مشتقّ", "حكم-مباشر"))
    assert len(families) == 1


# ----- اختلافُ النوع ليس تعارضًا -----


def test_two_compatible_types_on_one_individual_are_not_a_conflict() -> None:
    evidence = _evidence("دليل")
    stock = _stock(evidence)
    one = _membership("حكم-إنسان", "فرد", "إنسان", evidence)
    two = _membership("حكم-حيّ", "فرد", "كائنٌ-حيّ", evidence)
    stock = stock.admit(one, _licence(one, 1)).admit(two, _licence(two, 2))
    reading = stock.types_of("فرد", THE_SCOPE)
    assert reading.type_ids == ("إنسان", "كائنٌ-حيّ")
    assert reading.is_conflicted is False
    assert reading.conflicting_pairs == ()


def test_a_conflict_appears_only_with_a_witness_covering_that_scope() -> None:
    evidence = _evidence("دليل")
    witness_evidence = _evidence("دليل-شهادة", EvidenceGenus.STIPULATED_DEFINITION)
    register = FactRegister(register_id="سجلّ-اصطناعيّ")
    for one in (evidence, witness_evidence):
        register = register.with_evidence(one)
    register = register.with_individual(_individual("فرد", evidence))
    stock = KnowledgeStock(
        stock_id="رصيد-اصطناعيّ",
        version=0,
        register=register,
        identity=IdentityNetwork(network_id="شبكة-اصطناعيّة"),
        incompatibilities=(
            IncompatibilityWitness(
                witness_id="شهادة",
                type_a_id="حجر",
                type_b_id="شجر",
                scope=OTHER_SCOPE,
                evidence_ref=witness_evidence.ref,
            ),
        ),
    )
    one = _membership("حكم-حجر", "فرد", "حجر", evidence)
    two = _membership("حكم-شجر", "فرد", "شجر", evidence)
    stock = stock.admit(one, _licence(one, 1)).admit(two, _licence(two, 2))
    assert stock.types_of("فرد", THE_SCOPE).is_conflicted is False


# ----- التصحيحُ والتعليقُ وأثرُهما -----


def test_a_correction_suspends_the_old_judgment_and_keeps_its_history() -> None:
    evidence = _evidence("دليل")
    fresh = _evidence("دليل-مراجعة")
    stock = _stock(evidence, fresh)
    old = _membership("حكم-قديم", "فرد", "حجر", evidence)
    stock = stock.admit(old, _licence(old, 1))
    new = _membership("حكم-جديد", "فرد", "شجر", fresh)
    stock = stock.correct(
        Correction(
            correction_id="تصحيح",
            corrected_proposition_id="حكم-قديم",
            replacement_proposition_id="حكم-جديد",
            scope=THE_SCOPE,
            recorded_order=2,
            reason="سببٌ مُعلَن",
            evidence_ref=fresh.ref,
            policy=ReinstatementPolicy.KEEP_SUSPENDED_UNTIL_NEW_EVIDENCE,
        ),
        new,
        _licence(new, 3),
    )
    assert stock.register.proposition_of("حكم-قديم").suspended is True
    assert len(stock.corrections_of("حكم-قديم")) == 1


def test_a_correction_recorded_before_what_it_corrects_is_refused() -> None:
    evidence = _evidence("دليل")
    fresh = _evidence("دليل-مراجعة")
    stock = _stock(evidence, fresh)
    old = _membership("حكم-قديم", "فرد", "حجر", evidence)
    stock = stock.admit(old, _licence(old, 5))
    new = _membership("حكم-جديد", "فرد", "شجر", fresh)
    with pytest.raises(AccumulationError):
        stock.correct(
            Correction(
                correction_id="تصحيح",
                corrected_proposition_id="حكم-قديم",
                replacement_proposition_id="حكم-جديد",
                scope=THE_SCOPE,
                recorded_order=2,
                reason="سببٌ مُعلَن",
                evidence_ref=fresh.ref,
                policy=ReinstatementPolicy.RESTORE_THE_EARLIER_SUPPORT,
            ),
            new,
            _licence(new, 6),
        )


def test_a_local_conflict_leaves_an_unrelated_claim_untouched() -> None:
    evidence = _evidence("دليل")
    fresh = _evidence("دليل-مراجعة")
    stock = _stock(evidence, fresh, individuals=("فرد", "فردٌ-آخر"))
    old = _membership("حكم-قديم", "فرد", "حجر", evidence)
    other = _membership("حكم-بعيد", "فردٌ-آخر", "شجر", evidence)
    stock = stock.admit(old, _licence(old, 1)).admit(other, _licence(other, 2))
    new = _membership("حكم-جديد", "فرد", "شجر", fresh)
    stock = stock.correct(
        Correction(
            correction_id="تصحيح",
            corrected_proposition_id="حكم-قديم",
            replacement_proposition_id="حكم-جديد",
            scope=THE_SCOPE,
            recorded_order=3,
            reason="سببٌ مُعلَن",
            evidence_ref=fresh.ref,
            policy=ReinstatementPolicy.KEEP_SUSPENDED_UNTIL_NEW_EVIDENCE,
        ),
        new,
        _licence(new, 4),
    )
    assert stock.register.proposition_of("حكم-بعيد").suspended is False


# ----- نقضُ الاعتماد -----


def _applied_stock() -> tuple[KnowledgeStock, InferenceRule]:
    source = _evidence("دليل-مصدر", EvidenceGenus.STIPULATED_DEFINITION)
    rule = _rule(source)
    adoption = _evidence(
        "دليل-اعتماد",
        EvidenceGenus.STIPULATED_DEFINITION,
        f"يُعتمَد `{rule.versioned_id}` في هذا المجال",
    )
    base = _evidence("دليل-أساس")
    stock = _stock(base, source, adoption)
    stock = stock.adopt_rule(
        rule,
        AdoptionLicence(
            rule_versioned_id=rule.versioned_id,
            origin=RuleOrigin.TRANSMITTED_FROM_A_SOURCE,
            condition_note="شرطٌ مُعلَن",
            evidence_ref=adoption.ref,
        ),
        adoption,
    )
    premise = _membership("حكم-المقدّمة", "فرد", "مقدّمة", base)
    stock = stock.admit(premise, _licence(premise, 1))
    derived = Proposition(
        proposition_id="حكم-مشتقّ",
        form=PropositionForm.TYPE_MEMBERSHIP,
        subject_id="فرد",
        predicate_id="نوع",
        value=None,
        polarity=Polarity.AFFIRMED,
        scope=THE_SCOPE,
        evidence_ref=base.ref,
        derived_from_proposition_ids=("حكم-المقدّمة",),
        derived_by_rule=rule.versioned_id,
    )
    stock, blocked = stock.apply_adopted_rule(
        rule.versioned_id, ("حكم-المقدّمة",), derived, _licence(derived, 2)
    )
    assert blocked is None
    return stock, rule


def test_revoking_a_rule_licence_suspends_its_applications() -> None:
    stock, rule = _applied_stock()
    stock = stock.revoke_adoption(rule.versioned_id)
    assert stock.register.proposition_of("حكم-مشتقّ").suspended is True
    assert stock.register.proposition_of("حكم-المقدّمة").suspended is False


def test_a_revoked_rule_cannot_be_applied_again() -> None:
    stock, rule = _applied_stock()
    stock = stock.revoke_adoption(rule.versioned_id)
    again = Proposition(
        proposition_id="حكم-مشتقّ-ثانٍ",
        form=PropositionForm.TYPE_MEMBERSHIP,
        subject_id="فرد",
        predicate_id="نوع",
        value=None,
        polarity=Polarity.AFFIRMED,
        scope=THE_SCOPE,
        evidence_ref=stock.register.evidence_of("دليل-أساس").ref,
        derived_from_proposition_ids=("حكم-المقدّمة",),
        derived_by_rule=rule.versioned_id,
    )
    after, blocked = stock.apply_adopted_rule(
        rule.versioned_id, ("حكم-المقدّمة",), again, _licence(again, 9)
    )
    assert blocked is not None
    assert after.version == stock.version


def test_a_rule_cycle_without_premises_produces_nothing() -> None:
    source = _evidence("دليل-مصدر", EvidenceGenus.STIPULATED_DEFINITION)
    rule = _rule(source)
    adoption = _evidence(
        "دليل-اعتماد",
        EvidenceGenus.STIPULATED_DEFINITION,
        f"يُعتمَد `{rule.versioned_id}` في هذا المجال",
    )
    base = _evidence("دليل-أساس")
    stock = _stock(base, source, adoption)
    stock = stock.adopt_rule(
        rule,
        AdoptionLicence(
            rule_versioned_id=rule.versioned_id,
            origin=RuleOrigin.TRANSMITTED_FROM_A_SOURCE,
            condition_note="شرطٌ مُعلَن",
            evidence_ref=adoption.ref,
        ),
        adoption,
    )
    with pytest.raises(FactError):
        Proposition(
            proposition_id="حكم-بلا-مقدّمة",
            form=PropositionForm.TYPE_MEMBERSHIP,
            subject_id="فرد",
            predicate_id="نوع",
            value=None,
            polarity=Polarity.AFFIRMED,
            scope=THE_SCOPE,
            evidence_ref=base.ref,
            derived_by_rule=rule.versioned_id,
        )
    unsupported = _membership("حكم-بلا-مقدّمة", "فرد", "نوع", base)
    with pytest.raises(OperationError):
        stock.apply_adopted_rule(
            rule.versioned_id, (), unsupported, _licence(unsupported, 1)
        )
    assert stock.register.propositions == ()


# ----- شهادةُ الانتقال لا تُعبَث بها -----


def test_changing_a_party_in_a_saved_certificate_shows_its_inconsistency() -> None:
    stock = _two_supports()
    claim = ClaimKey(
        subject_id="فرد",
        predicate_id="نوع",
        value=None,
        polarity=Polarity.AFFIRMED,
        scope=THE_SCOPE,
    )
    saved = stock.verdict_for(claim)
    tampered = ClaimKey(
        subject_id="فردٌ-ليس-هو",
        predicate_id="نوع",
        value=None,
        polarity=Polarity.AFFIRMED,
        scope=THE_SCOPE,
    )
    assert claim_verdict(stock.register, tampered).standing is ClaimStanding.UNKNOWN
    assert saved.standing is ClaimStanding.SUPPORTED_IN_SCOPE


def test_changing_the_polarity_in_a_saved_certificate_shows_its_inconsistency() -> None:
    stock = _two_supports()
    claim = ClaimKey(
        subject_id="فرد",
        predicate_id="نوع",
        value=None,
        polarity=Polarity.NEGATED,
        scope=THE_SCOPE,
    )
    verdict = stock.verdict_for(claim)
    assert verdict.standing is ClaimStanding.NEGATED_IN_SCOPE
    assert verdict.negating_proposition_ids == ("حكم-أوّل", "حكم-ثانٍ")


def test_changing_the_scope_in_a_saved_certificate_shows_its_inconsistency() -> None:
    stock = _two_supports()
    claim = ClaimKey(
        subject_id="فرد",
        predicate_id="نوع",
        value=None,
        polarity=Polarity.AFFIRMED,
        scope=OTHER_SCOPE,
    )
    assert stock.verdict_for(claim).standing is ClaimStanding.UNKNOWN


def test_a_new_lawful_input_is_re_evaluated_and_not_refused_for_a_new_digest() -> None:
    stock = _two_supports()
    third = _evidence("دليل-ثالث", statement="تقريرٌ ثالثٌ بمضمونٍ مختلفٍ فبصمةٍ مختلفة")
    stock = stock.with_evidence(third)
    item = _membership("حكم-ثالث", "فرد", "نوع", third)
    stock = stock.admit(item, _licence(item, 3))
    claim = ClaimKey(
        subject_id="فرد",
        predicate_id="نوع",
        value=None,
        polarity=Polarity.AFFIRMED,
        scope=THE_SCOPE,
    )
    assert stock.verdict_for(claim).independent_support_count == 3


# ----- ما لا يرقى تلقائيًّا -----


def test_a_declared_hypothesis_never_deposits_an_occurrence() -> None:
    hypothesis = _evidence(
        "دليل-فرضيّة", EvidenceGenus.DECLARED_HYPOTHESIS, "فرضيّةٌ مُعلَنة"
    )
    anchor = _evidence("دليل-مرساة")
    stock = _stock(anchor, hypothesis)
    item = _membership("حكم", "فرد", "نوع", hypothesis)
    with pytest.raises(FactError):
        stock.admit(item, _licence(item, 1))


def test_an_earlier_record_does_not_make_a_later_one_its_effect() -> None:
    evidence = _evidence("دليل")
    stock = _stock(evidence)
    first = _membership("حكم-أسبق", "فرد", "حالٌ-أولى", evidence)
    second = _membership("حكم-لاحق", "فرد", "حالٌ-ثانية", evidence)
    stock = stock.admit(first, _licence(first, 1)).admit(second, _licence(second, 2))
    causal = ClaimKey(
        subject_id="فرد",
        predicate_id="سبَّبَ-الحالَ-الثانية",
        value=None,
        polarity=Polarity.AFFIRMED,
        scope=THE_SCOPE,
    )
    assert stock.verdict_for(causal).standing is ClaimStanding.UNKNOWN


def test_a_capacity_does_not_deposit_the_act() -> None:
    evidence = _evidence("دليل")
    stock = _stock(evidence)
    capacity = _membership("حكم-قدرة", "فرد", "قادرٌ-على-الفتح", evidence)
    stock = stock.admit(capacity, _licence(capacity, 1))
    act = ClaimKey(
        subject_id="فرد",
        predicate_id="فتَحَ",
        value=None,
        polarity=Polarity.AFFIRMED,
        scope=THE_SCOPE,
    )
    assert stock.verdict_for(act).standing is ClaimStanding.UNKNOWN


def test_the_stock_version_rises_on_every_write() -> None:
    evidence = _evidence("دليل")
    stock = _stock(evidence)
    item = _membership("حكم", "فرد", "نوع", evidence)
    assert stock.version == 0
    assert stock.admit(item, _licence(item, 1)).version == 1


def test_the_content_id_moves_when_the_stock_moves() -> None:
    evidence = _evidence("دليل")
    stock = _stock(evidence)
    item = _membership("حكم", "فرد", "نوع", evidence)
    assert stock.content_id != stock.admit(item, _licence(item, 1)).content_id


# ----- حدودُ هذه النواة، مُمتحَنةً لا مُعلَنةً قولًا -----


def test_every_module_name_is_importable_from_the_package_surface() -> None:
    """ما في `__all__` مستوردٌ فعلًا؛ واسمٌ مُعلَنٌ بلا استيرادٍ تصديرٌ كاذب."""

    import alghanem.ontology as package

    assert [name for name in package.__all__ if not hasattr(package, name)] == []


def _two_premise_conclusion() -> tuple[KnowledgeStock, InferenceRule]:
    """نتيجةٌ اشتُقّت من مقدّمتين، إحداهما ستُصحَّح ببديلٍ يحمل مضمونَها."""

    source = _evidence("دليل-مصدر", EvidenceGenus.STIPULATED_DEFINITION)
    rule = _rule(source)
    adoption = _evidence(
        "دليل-اعتماد",
        EvidenceGenus.STIPULATED_DEFINITION,
        f"يُعتمَد `{rule.versioned_id}` في هذا المجال",
    )
    first = _evidence("دليل-أوّل")
    second = _evidence("دليل-ثانٍ")
    fresh = _evidence("دليل-مراجعة")
    stock = _stock(first, source, adoption, second, fresh)
    stock = stock.adopt_rule(
        rule,
        AdoptionLicence(
            rule_versioned_id=rule.versioned_id,
            origin=RuleOrigin.TRANSMITTED_FROM_A_SOURCE,
            condition_note="شرطٌ مُعلَن",
            evidence_ref=adoption.ref,
        ),
        adoption,
    )
    one = _membership("مقدّمة-أولى", "فرد", "مقدّمة", first)
    two = _membership("مقدّمة-ثانية", "فرد", "مقدّمةٌ-ثانية", second)
    stock = stock.admit(one, _licence(one, 1)).admit(two, _licence(two, 2))
    conclusion = Proposition(
        proposition_id="نتيجة",
        form=PropositionForm.TYPE_MEMBERSHIP,
        subject_id="فرد",
        predicate_id="نوع",
        value=None,
        polarity=Polarity.AFFIRMED,
        scope=THE_SCOPE,
        evidence_ref=first.ref,
        derived_from_proposition_ids=("مقدّمة-أولى", "مقدّمة-ثانية"),
        derived_by_rule=rule.versioned_id,
    )
    stock, blocked = stock.apply_adopted_rule(
        rule.versioned_id,
        ("مقدّمة-أولى", "مقدّمة-ثانية"),
        conclusion,
        _licence(conclusion, 3),
    )
    assert blocked is None
    return stock, rule


def test_a_correction_suspends_a_conclusion_its_replacement_would_relicense() -> None:
    """**المثالُ المُسمّى للقصور المحافظ.**

    المقدّمةُ الأولى تُصحَّح ببديلٍ يحمل **المحمولَ نفسَه** في النطاق نفسِه،
    فالقاعدةُ كانت تنطلق على البديل كما انطلقت على المصحَّحة. ومع ذلك تُعلَّق
    النتيجة. فالتعليقُ يمشي على الاشتقاق لا على المضمون — وهذا تجاوزٌ مقيسٌ
    لا مُدَّعًى.
    """

    stock, _ = _two_premise_conclusion()
    fresh = stock.register.evidence_of("دليل-مراجعة")
    replacement = _membership("مقدّمة-أولى-مصحَّحة", "فرد", "مقدّمة", fresh)
    corrected = stock.register.proposition_of("مقدّمة-أولى")

    assert replacement.predicate_id == corrected.predicate_id
    assert replacement.scope == corrected.scope
    assert replacement.polarity is corrected.polarity

    stock = stock.correct(
        Correction(
            correction_id="تصحيح",
            corrected_proposition_id="مقدّمة-أولى",
            replacement_proposition_id="مقدّمة-أولى-مصحَّحة",
            scope=THE_SCOPE,
            recorded_order=4,
            reason="الدليلُ الأوّل نُسِب خطأً، والمضمونُ باقٍ",
            evidence_ref=fresh.ref,
            policy=ReinstatementPolicy.KEEP_SUSPENDED_UNTIL_NEW_EVIDENCE,
        ),
        replacement,
        _licence(replacement, 5),
    )

    assert stock.register.proposition_of("نتيجة").suspended is True
    assert stock.register.proposition_of("مقدّمة-ثانية").suspended is False
    assert stock.register.proposition_of("مقدّمة-أولى-مصحَّحة").suspended is False


def test_the_overshoot_is_undone_only_by_a_new_licensed_derivation() -> None:
    """ولا تعود النتيجةُ إلّا باشتقاقٍ جديدٍ بترخيصه؛ لا بأثرٍ تلقائيّ."""

    stock, rule = _two_premise_conclusion()
    fresh = stock.register.evidence_of("دليل-مراجعة")
    replacement = _membership("مقدّمة-أولى-مصحَّحة", "فرد", "مقدّمة", fresh)
    stock = stock.correct(
        Correction(
            correction_id="تصحيح",
            corrected_proposition_id="مقدّمة-أولى",
            replacement_proposition_id="مقدّمة-أولى-مصحَّحة",
            scope=THE_SCOPE,
            recorded_order=4,
            reason="الدليلُ الأوّل نُسِب خطأً، والمضمونُ باقٍ",
            evidence_ref=fresh.ref,
            policy=ReinstatementPolicy.KEEP_SUSPENDED_UNTIL_NEW_EVIDENCE,
        ),
        replacement,
        _licence(replacement, 5),
    )
    claim = ClaimKey(
        subject_id="فرد",
        predicate_id="نوع",
        value=None,
        polarity=Polarity.AFFIRMED,
        scope=THE_SCOPE,
    )
    assert stock.verdict_for(claim).supporting_proposition_ids == ()

    again = Proposition(
        proposition_id="نتيجةٌ-مُعادةُ-الاشتقاق",
        form=PropositionForm.TYPE_MEMBERSHIP,
        subject_id="فرد",
        predicate_id="نوع",
        value=None,
        polarity=Polarity.AFFIRMED,
        scope=THE_SCOPE,
        evidence_ref=fresh.ref,
        derived_from_proposition_ids=("مقدّمة-أولى-مصحَّحة", "مقدّمة-ثانية"),
        derived_by_rule=rule.versioned_id,
    )
    stock, blocked = stock.apply_adopted_rule(
        rule.versioned_id,
        ("مقدّمة-أولى-مصحَّحة", "مقدّمة-ثانية"),
        again,
        _licence(again, 6),
    )
    assert blocked is None
    assert stock.verdict_for(claim).supporting_proposition_ids == (
        "نتيجةٌ-مُعادةُ-الاشتقاق",
    )
    assert stock.register.proposition_of("نتيجة").suspended is True


def test_the_declared_overshoot_names_a_test_that_exists_in_this_file() -> None:
    """الإعلانُ يُسمّي اختبارَه، والاسمُ المُسمّى موجودٌ ههنا — لا دعوى بلا شاهد."""

    from alghanem.ontology import (
        THE_SUSPENSION_IS_CONSERVATIVE_AND_HERE_IS_WHERE_IT_OVERSHOOTS as declared,
    )

    named = "test_a_correction_suspends_a_conclusion_its_replacement_would_relicense"
    assert named in declared
    assert named in globals()
