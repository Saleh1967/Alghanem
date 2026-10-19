"""اختباراتُ شبكة التسمية والهويّة — **اصطناعيّةٌ لعقود العمليّات**.

لا شاهدَ مصدريًّا ههنا بحال: الأفرادُ والأدلّةُ مفروضةٌ لفحص العقد وحدَها،
وأجناسُها `DECLARED_HYPOTHESIS` و`ACCEPTED_REPORT`. والشواهدُ المصدريّةُ
الواقعيّةُ في `tests/arabic/test_identity_path_run.py`، مفصولةٌ عن هذه.
"""

from __future__ import annotations

import pytest

from alghanem.ontology import (
    ConflictPolicy,
    DesignationMethod,
    Evidence,
    EvidenceGenus,
    ExistenceStanding,
    FactRegister,
    IdentityCriterion,
    IdentityError,
    IdentityLink,
    IdentityNetwork,
    Individual,
    KeyAgreementStanding,
    KeyReading,
    NamedKind,
    Naming,
    NamingGenus,
    Scope,
    candidates_for_surface,
    linked_individual_ids,
)

THE_DOMAIN = "مجال-اصطناعيّ"


def _scope() -> Scope:
    return Scope(domain_id=THE_DOMAIN)


def _evidence(evidence_id: str, genus: EvidenceGenus) -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        genus=genus,
        statement=f"دليلٌ اصطناعيٌّ لفحص العقد: {evidence_id}",
        source_name="اختبارٌ اصطناعيٌّ مُعلَن",
        scope=_scope(),
    )


def _register(*individual_ids: str) -> FactRegister:
    register = FactRegister(register_id="سجلّ-اصطناعيّ")
    for individual_id in individual_ids:
        evidence = _evidence(f"دليل-{individual_id}", EvidenceGenus.DECLARED_HYPOTHESIS)
        register = register.with_evidence(evidence).with_individual(
            Individual(
                individual_id=individual_id,
                designation_method=DesignationMethod.PROPER_NAME,
                candidate_type_ids=("نوع-الإنسان",),
                existence=ExistenceStanding.ASSUMED_FOR_THE_DISCOURSE,
                evidence_ref=evidence.ref,
            )
        )
    return register


def _naming(
    naming_id: str, surface: str, named_id: str, register: FactRegister
) -> Naming:
    evidence = _evidence(f"دليل-{naming_id}", EvidenceGenus.LEXICAL_ATTESTATION)
    return Naming(
        naming_id=naming_id,
        surface=surface,
        named_id=named_id,
        named_kind=NamedKind.INDIVIDUAL,
        genus=NamingGenus.PROPER_NAME,
        language_id="ar",
        scope=_scope(),
        evidence_ref=evidence.ref,
    )


def _network_with(register: FactRegister, *namings: Naming) -> IdentityNetwork:
    network = IdentityNetwork(network_id="شبكة-اصطناعيّة")
    for naming in namings:
        network = network.with_naming(naming, register)
    return network


# ----- التسميةُ علاقةٌ لا هويّة -----


def test_one_surface_names_two_individuals_and_neither_is_chosen() -> None:
    register = _register("فرد-أ", "فرد-ب")
    network = _network_with(
        register,
        _naming("ت-أ", "زيد", "فرد-أ", register),
        _naming("ت-ب", "زيد", "فرد-ب", register),
    )
    found = candidates_for_surface("زيد", network, register)
    assert tuple(one.individual_id for one in found) == ("فرد-أ", "فرد-ب")
    assert all(one.reason for one in found)


def test_one_individual_carries_many_names_under_one_identifier() -> None:
    register = _register("فرد-أ")
    network = _network_with(
        register,
        _naming("ت-١", "زيد", "فرد-أ", register),
        _naming("ت-٢", "أبو أسامة", "فرد-أ", register),
    )
    assert len(network.namings_of_individual("فرد-أ")) == 2
    for surface in ("زيد", "أبو أسامة"):
        found = candidates_for_surface(surface, network, register)
        assert tuple(one.individual_id for one in found) == ("فرد-أ",)


def test_candidates_grow_when_data_grows_without_touching_the_engine() -> None:
    register = _register("فرد-أ", "فرد-ب", "فرد-ج")
    network = _network_with(
        register,
        _naming("ت-أ", "زيد", "فرد-أ", register),
        _naming("ت-ب", "زيد", "فرد-ب", register),
    )
    assert len(candidates_for_surface("زيد", network, register)) == 2
    widened = network.with_naming(_naming("ت-ج", "زيد", "فرد-ج", register), register)
    assert len(candidates_for_surface("زيد", widened, register)) == 3


def test_a_naming_of_an_unregistered_individual_is_refused() -> None:
    register = _register("فرد-أ")
    network = IdentityNetwork(network_id="شبكة-اصطناعيّة")
    with pytest.raises(Exception):
        network.with_naming(_naming("ت-غ", "زيد", "فرد-غائب", register), register)


# ----- المعيارُ والرابط -----


def test_a_criterion_of_one_key_is_refused_at_construction() -> None:
    with pytest.raises(IdentityError):
        IdentityCriterion(
            criterion_id="معيار-ناقص",
            key_names=("سنة-الميلاد",),
            scope=_scope(),
            authority="سلطةٌ مُسمّاة",
        )


def test_a_criterion_without_a_named_authority_is_refused() -> None:
    with pytest.raises(IdentityError):
        IdentityCriterion(
            criterion_id="معيار-بلا-سلطة",
            key_names=("أ", "ب"),
            scope=_scope(),
            authority="  ",
        )


def _criterion() -> IdentityCriterion:
    return IdentityCriterion(
        criterion_id="معيار",
        key_names=("مفتاح-أ", "مفتاح-ب"),
        scope=_scope(),
        authority="سلطةٌ مُسمّاة",
    )


def _link(readings: tuple[KeyReading, ...], register: FactRegister) -> IdentityLink:
    return IdentityLink(
        link_id="رابط",
        left_individual_id="فرد-أ",
        right_individual_id="فرد-ب",
        criterion_id="معيار",
        key_readings=readings,
        evidence_ref=register.evidence_of("دليل-رابط").ref,
    )


def _linkable() -> tuple[FactRegister, IdentityNetwork]:
    register = _register("فرد-أ", "فرد-ب")
    register = register.with_evidence(
        _evidence("دليل-رابط", EvidenceGenus.ACCEPTED_REPORT)
    )
    network = _network_with(
        register,
        _naming("ت-أ", "زيد", "فرد-أ", register),
        _naming("ت-ب", "زيد", "فرد-ب", register),
    ).with_criterion(_criterion())
    return register, network


def test_one_agreeing_key_is_not_an_identity_proof() -> None:
    register, network = _linkable()
    link = _link(
        (
            KeyReading(key_name="مفتاح-أ", left_value="س", right_value="س"),
            KeyReading(key_name="مفتاح-ب", left_value=None, right_value="ص"),
        ),
        register,
    )
    assert link.agreeing_key_names == ("مفتاح-أ",)
    with pytest.raises(IdentityError):
        network.with_link(link, register)


def test_a_silent_key_is_neither_agreement_nor_difference() -> None:
    reading = KeyReading(key_name="مفتاح-أ", left_value="س", right_value=None)
    assert reading.standing is KeyAgreementStanding.NOT_RECORDED


def test_a_link_whose_keys_all_agree_is_deposited_and_unifies() -> None:
    register, network = _linkable()
    network = network.with_link(
        _link(
            (
                KeyReading(key_name="مفتاح-أ", left_value="س", right_value="س"),
                KeyReading(key_name="مفتاح-ب", left_value="ص", right_value="ص"),
            ),
            register,
        ),
        register,
    )
    assert linked_individual_ids("فرد-أ", network) == ("فرد-ب",)


def test_retracting_a_link_unlinks_without_erasing_it() -> None:
    register, network = _linkable()
    network = network.with_link(
        _link(
            (
                KeyReading(key_name="مفتاح-أ", left_value="س", right_value="س"),
                KeyReading(key_name="مفتاح-ب", left_value="ص", right_value="ص"),
            ),
            register,
        ),
        register,
    )
    after = network.retract_link("رابط")
    assert linked_individual_ids("فرد-أ", after) == ()
    assert after.link_of("رابط").retracted is True
    assert len(after.links) == 1
    assert len(after.namings) == len(network.namings)


def test_two_individuals_sharing_a_surface_stay_apart_without_a_link() -> None:
    register, network = _linkable()
    assert linked_individual_ids("فرد-أ", network) == ()
    assert len(candidates_for_surface("زيد", network, register)) == 2


# ----- سياسةُ التعارض وحدُّها -----


def _contested() -> tuple[FactRegister, IdentityNetwork]:
    register, network = _linkable()
    register = register.with_evidence(
        _evidence("دليل-معارض", EvidenceGenus.ACCEPTED_REPORT)
    )
    network = network.with_link(
        _link(
            (
                KeyReading(key_name="مفتاح-أ", left_value="س", right_value="س"),
                KeyReading(key_name="مفتاح-ب", left_value="ص", right_value="ص"),
            ),
            register,
        ),
        register,
    ).amend_link_readings(
        "رابط",
        (
            KeyReading(key_name="مفتاح-أ", left_value="س", right_value="ع"),
            KeyReading(key_name="مفتاح-ب", left_value="ص", right_value="ص"),
        ),
        register.evidence_of("دليل-معارض").ref,
    )
    return register, network


def test_a_contested_link_is_reached_by_amendment_not_by_deposit() -> None:
    register, network = _contested()
    assert network.link_of("رابط").differing_key_names == ("مفتاح-أ",)
    with pytest.raises(IdentityError):
        _network_with(register).with_criterion(_criterion()).with_link(
            _link(
                (
                    KeyReading(key_name="مفتاح-أ", left_value="س", right_value="ع"),
                    KeyReading(key_name="مفتاح-ب", left_value="ص", right_value="ص"),
                ),
                register,
            ),
            register,
        )


def test_the_narrow_policy_suspends_only_the_contested_link() -> None:
    _, network = _contested()
    after, suspended = network.apply_conflict_policy(
        ConflictPolicy.SUSPEND_THE_CONTESTED_LINKS
    )
    assert suspended == ("رابط",)
    assert after.link_of("رابط").retracted is True


def test_the_component_policy_suspends_a_link_that_is_not_contested() -> None:
    register, network = _contested()
    register = register.with_evidence(
        _evidence("دليل-رابط-ثانٍ", EvidenceGenus.ACCEPTED_REPORT)
    )
    evidence = _evidence("دليل-فرد-ج", EvidenceGenus.DECLARED_HYPOTHESIS)
    register = register.with_evidence(evidence).with_individual(
        Individual(
            individual_id="فرد-ج",
            designation_method=DesignationMethod.PROPER_NAME,
            candidate_type_ids=("نوع-الإنسان",),
            existence=ExistenceStanding.ASSUMED_FOR_THE_DISCOURSE,
            evidence_ref=evidence.ref,
        )
    )
    network = network.with_link(
        IdentityLink(
            link_id="رابط-ثانٍ",
            left_individual_id="فرد-ب",
            right_individual_id="فرد-ج",
            criterion_id="معيار",
            key_readings=(
                KeyReading(key_name="مفتاح-أ", left_value="ع", right_value="ع"),
                KeyReading(key_name="مفتاح-ب", left_value="ص", right_value="ص"),
            ),
            evidence_ref=register.evidence_of("دليل-رابط-ثانٍ").ref,
        ),
        register,
    )
    _, narrow = network.apply_conflict_policy(
        ConflictPolicy.SUSPEND_THE_CONTESTED_LINKS
    )
    _, wide = network.apply_conflict_policy(ConflictPolicy.SUSPEND_THE_COMPONENT)
    assert narrow == ("رابط",)
    assert wide == ("رابط", "رابط-ثانٍ")
    assert "رابط-ثانٍ" not in narrow


# ----- اسمُ العَلَم لا يُشتَقّ منه وصف -----


def test_naming_a_person_salih_deposits_no_attribute_proposition() -> None:
    register = _register("فرد-أ")
    network = _network_with(register, _naming("ت-أ", "صالح", "فرد-أ", register))
    assert len(network.namings_of_individual("فرد-أ")) == 1
    assert register.propositions == ()
    assert not hasattr(network, "attribute_of")
