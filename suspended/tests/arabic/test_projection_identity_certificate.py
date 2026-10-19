"""Witnesses for the projection identity certificate: fibers, standings, transport."""

from __future__ import annotations

import pytest

from alghanem.arabic import projection_identity_certificate as module
from alghanem.arabic.carrier_projection_deposit import (
    THE_FOLDING,
    WordBoundary,
    census_of,
    deposited_text,
    project_word,
    repeated_skeletons_in,
    repeated_words_in,
    words_of,
)
from alghanem.arabic.fath_ayah_source_text import FATH_AYAH_SOURCE_ID
from alghanem.arabic.fatiha_source_text import FATIHA_SOURCE_ID
from alghanem.arabic.projection_identity_certificate import (
    PROJECTION_IDENTITY_NAMED_RESIDUALS,
    THE_DESTRUCTION_WITNESSES,
    THE_LICENSE_REGISTER,
    THE_ORDER,
    THE_SCOPE_RANK,
    CarrierDistinctionFinding,
    CollapseLicense,
    CollapseMechanism,
    CollapseStanding,
    DestructionWitness,
    ProjectionCertificate,
    ProjectionFiber,
    ProjectionIdentityError,
    TransportStanding,
    carrier_distinction_findings,
    certificate_of,
    fibers_of,
    fold_rule_digest,
    fold_stream,
    the_commutation_table,
    the_fold_and_the_boundary_commute_on,
    uncertified_carrier_distinctions,
)

FATIHA = FATIHA_SOURCE_ID
FATH = FATH_AYAH_SOURCE_ID


def _finding_for(certificate: ProjectionCertificate, skeleton: str) -> object:
    for finding in certificate.findings:
        if finding.skeleton == skeleton:
            return finding
    raise AssertionError(f"no finding for {skeleton!r}")


# --- the order is boundary first, then fold ---------------------------------


def test_the_declared_order_is_boundary_then_fold_then_adjacency() -> None:
    assert THE_ORDER[0].startswith("B:")
    assert THE_ORDER[1].startswith("F:")
    assert THE_ORDER[2].startswith("A:")


def test_no_probability_step_is_written_into_the_order() -> None:
    assert not any(step.startswith("P:") for step in THE_ORDER)


def test_the_fold_stream_keeps_whitespace_and_drops_residue() -> None:
    folded = fold_stream(deposited_text(FATIHA))
    assert "\n" in folded
    assert all(
        character.isspace() or character in set("".join(folded.split()))
        for character in folded
    )


def test_the_commutation_is_measured_on_both_deposits_with_both_rules() -> None:
    table = the_commutation_table()
    assert len(table) == 4


def test_the_commutation_holds_under_any_whitespace_on_both_deposits() -> None:
    for source_id in (FATIHA, FATH):
        assert the_fold_and_the_boundary_commute_on(
            source_id, WordBoundary.ANY_WHITESPACE
        )


def test_the_commutation_breaks_on_the_fatiha_under_the_space_only_rule() -> None:
    assert not the_fold_and_the_boundary_commute_on(FATIHA, WordBoundary.SPACE_ONLY)


def test_the_space_only_rule_is_inert_on_the_one_line_fath_deposit() -> None:
    assert the_fold_and_the_boundary_commute_on(FATH, WordBoundary.SPACE_ONLY)


def test_the_break_is_the_newline_the_fold_discards_and_the_rule_keeps() -> None:
    text = deposited_text(FATIHA)
    welded = [word for word in words_of(text, WordBoundary.SPACE_ONLY) if "\n" in word]
    assert welded
    assert all("\n" not in project_word(word) for word in welded)


def test_no_certificate_is_issued_where_the_two_orders_disagree() -> None:
    with pytest.raises(ProjectionIdentityError):
        certificate_of(FATIHA, WordBoundary.SPACE_ONLY)


# --- the collapse is a fiber, not a pair ------------------------------------


def test_every_word_of_a_fiber_projects_to_its_skeleton() -> None:
    for source_id in (FATIHA, FATH):
        for fiber in fibers_of(source_id, WordBoundary.ANY_WHITESPACE):
            for word in fiber.written:
                assert project_word(word) == fiber.skeleton


def test_the_fibers_partition_the_written_words_of_the_deposit() -> None:
    for source_id in (FATIHA, FATH):
        fibers = fibers_of(source_id, WordBoundary.ANY_WHITESPACE)
        gathered = [word for fiber in fibers for word in fiber.written]
        assert sorted(gathered) == sorted(
            set(words_of(deposited_text(source_id), WordBoundary.ANY_WHITESPACE))
        )


def test_the_occurrences_of_a_fiber_are_the_places_its_words_fall() -> None:
    words = words_of(deposited_text(FATH), WordBoundary.ANY_WHITESPACE)
    for fiber in fibers_of(FATH, WordBoundary.ANY_WHITESPACE):
        for index in fiber.occurrences:
            assert words[index] in fiber.written


def test_the_counts_are_derived_from_the_fibers_not_written_down() -> None:
    certificate = certificate_of(FATH)
    assert certificate.written_forms == sum(fiber.size for fiber in certificate.fibers)
    assert certificate.skeleton_count == len(certificate.fibers)
    assert certificate.loss == sum(fiber.size - 1 for fiber in certificate.fibers)


def test_the_fath_loss_is_fifty_minus_forty_seven() -> None:
    certificate = certificate_of(FATH)
    assert (certificate.written_forms, certificate.skeleton_count) == (50, 47)
    assert certificate.loss == 3


def test_the_fatiha_loses_no_written_distinction_at_all() -> None:
    certificate = certificate_of(FATIHA)
    assert certificate.loss == 0
    assert certificate.collapsed == ()


def test_the_certificate_counts_agree_with_the_deposited_census() -> None:
    for source_id in (FATIHA, FATH):
        certificate = certificate_of(source_id)
        census = census_of(source_id, WordBoundary.ANY_WHITESPACE)
        assert certificate.written_forms == census.distinct_words
        assert certificate.skeleton_count == census.distinct_skeletons
        assert certificate.residue_occurrences == census.residue_occurrences
        assert certificate.residue_kinds == census.residue_kinds


def test_the_loss_formula_does_not_assume_a_fiber_of_size_two() -> None:
    fiber = ProjectionFiber(
        skeleton=project_word("مِنْ"),
        written=tuple(sorted(("مِنْ", "مِنَ", "مَن", "مِن"))),
        occurrences=(0, 1, 2, 3),
    )
    assert fiber.size == 4
    assert fiber.size - 1 == 3


def test_a_fiber_refuses_a_word_that_is_not_its_own() -> None:
    with pytest.raises(ProjectionIdentityError):
        ProjectionFiber(skeleton="الله", written=("مِنْ",), occurrences=(0,))


def test_a_fiber_refuses_to_exist_without_an_occurrence() -> None:
    with pytest.raises(ProjectionIdentityError):
        ProjectionFiber(skeleton="من", written=("مِنْ",), occurrences=())


# --- a declared fold is a mechanism, not a license --------------------------


def test_the_license_register_is_empty_on_this_evidence() -> None:
    assert THE_LICENSE_REGISTER == ()


def test_the_witness_register_is_empty_on_this_evidence() -> None:
    assert THE_DESTRUCTION_WITNESSES == ()


def test_nothing_is_licensed_and_nothing_is_destructive_on_this_evidence() -> None:
    for source_id in (FATIHA, FATH):
        standings = certificate_of(source_id).standings()
        assert standings[CollapseStanding.LICENSED_COLLAPSE] == ()
        assert standings[CollapseStanding.DESTRUCTIVE_COLLAPSE] == ()


def test_the_three_fath_collapses_are_unresolved_and_not_licensed() -> None:
    standings = certificate_of(FATH).standings()
    assert len(standings[CollapseStanding.UNRESOLVED_DISTINCTION]) == 3
    assert set(standings[CollapseStanding.UNRESOLVED_DISTINCTION]) == {
        "الله",
        "الكفار",
        "من",
    }


def test_every_fath_collapse_is_discarded_residue_and_not_declared_fold() -> None:
    certificate = certificate_of(FATH)
    for fiber in certificate.collapsed:
        finding = _finding_for(certificate, fiber.skeleton)
        assert finding.mechanism is CollapseMechanism.DISCARDED_RESIDUE  # type: ignore[attr-defined]


def test_the_mechanism_of_a_preserved_distinction_is_none() -> None:
    certificate = certificate_of(FATIHA)
    assert all(
        finding.mechanism is CollapseMechanism.NONE for finding in certificate.findings
    )


def test_a_declared_fold_does_not_by_itself_make_a_standing_licensed() -> None:
    certificate = certificate_of(FATH)
    assert THE_FOLDING  # the fold is declared and non-empty
    assert certificate.standings()[CollapseStanding.LICENSED_COLLAPSE] == ()


def test_a_license_must_name_a_ground_and_more_than_one_written_form() -> None:
    with pytest.raises(ProjectionIdentityError):
        CollapseLicense(
            source_id=FATH, skeleton="من", written=("مِنْ", "مِنَ"), ground="   "
        )
    with pytest.raises(ProjectionIdentityError):
        CollapseLicense(source_id=FATH, skeleton="من", written=("مِنْ",), ground="ground")


def test_a_destruction_witness_must_be_bound_to_an_occurrence_and_a_name() -> None:
    with pytest.raises(ProjectionIdentityError):
        DestructionWitness(
            source_id=FATH,
            occurrence=-1,
            skeleton="من",
            distinction="ending",
            witness_id="w",
        )
    with pytest.raises(ProjectionIdentityError):
        DestructionWitness(
            source_id=FATH,
            occurrence=15,
            skeleton="من",
            distinction="ending",
            witness_id="  ",
        )


def test_a_license_only_applies_to_its_own_deposit_and_its_own_words() -> None:
    fiber = next(fiber for fiber in certificate_of(FATH).collapsed)
    entry = CollapseLicense(
        source_id=FATIHA,
        skeleton=fiber.skeleton,
        written=fiber.written,
        ground="a ground written elsewhere",
    )
    assert module._license_for(FATH, fiber) is None
    assert entry.source_id != FATH


def test_a_witness_bound_to_another_occurrence_does_not_make_destruction() -> None:
    fiber = next(fiber for fiber in certificate_of(FATH).collapsed)
    absent = max(fiber.occurrences) + 1000
    witness = DestructionWitness(
        source_id=FATH,
        occurrence=absent,
        skeleton=fiber.skeleton,
        distinction="ending",
        witness_id="witness-not-in-the-tree",
    )
    assert witness.occurrence not in fiber.occurrences
    assert module._witness_for(FATH, fiber) is None


def test_a_standing_refuses_to_be_licensed_without_a_ground() -> None:
    with pytest.raises(ProjectionIdentityError):
        module.StandingFinding(
            skeleton="من",
            standing=CollapseStanding.LICENSED_COLLAPSE,
            mechanism=CollapseMechanism.DISCARDED_RESIDUE,
            license_ground=None,
            witness_id=None,
        )


def test_a_standing_refuses_to_be_destructive_without_a_witness() -> None:
    with pytest.raises(ProjectionIdentityError):
        module.StandingFinding(
            skeleton="من",
            standing=CollapseStanding.DESTRUCTIVE_COLLAPSE,
            mechanism=CollapseMechanism.DISCARDED_RESIDUE,
            license_ground=None,
            witness_id=None,
        )


def test_a_preserved_distinction_refuses_a_collapse_mechanism() -> None:
    with pytest.raises(ProjectionIdentityError):
        module.StandingFinding(
            skeleton="من",
            standing=CollapseStanding.PRESERVED_DISTINCTION,
            mechanism=CollapseMechanism.DISCARDED_RESIDUE,
            license_ground=None,
            witness_id=None,
        )


def test_every_fiber_carries_exactly_one_standing() -> None:
    for source_id in (FATIHA, FATH):
        certificate = certificate_of(source_id)
        assert len(certificate.findings) == len(certificate.fibers)
        counted = sum(len(found) for found in certificate.standings().values())
        assert counted == len(certificate.fibers)


def test_the_four_standings_are_published_even_when_empty() -> None:
    standings = certificate_of(FATIHA).standings()
    assert set(standings) == set(CollapseStanding)


# --- the certificate is bound to its source, fold, boundary and scope -------


def test_the_certificate_names_its_source_fold_boundary_and_scope() -> None:
    certificate = certificate_of(FATH)
    assert certificate.source_identity == FATH
    assert certificate.fold_rule == fold_rule_digest()
    assert certificate.boundary_rule is WordBoundary.ANY_WHITESPACE
    assert certificate.scope_rank == THE_SCOPE_RANK


def test_the_fold_digest_moves_when_the_fold_moves() -> None:
    assert fold_rule_digest() == fold_rule_digest()
    assert len(fold_rule_digest()) == 64


def test_no_certificate_is_issued_for_a_text_outside_the_scope() -> None:
    with pytest.raises(ProjectionIdentityError):
        certificate_of("some-text-not-in-the-tree")


def test_the_certificate_refuses_a_fold_digest_that_is_not_the_deposited_one() -> None:
    certificate = certificate_of(FATH)
    with pytest.raises(ProjectionIdentityError):
        ProjectionCertificate(
            source_identity=certificate.source_identity,
            fold_rule="0" * 64,
            boundary_rule=certificate.boundary_rule,
            fibers=certificate.fibers,
            findings=certificate.findings,
            residue_occurrences=certificate.residue_occurrences,
            residue_kinds=certificate.residue_kinds,
            trace=certificate.trace,
            domain=certificate.domain,
            scope_rank=certificate.scope_rank,
        )


def test_the_certificate_refuses_a_residue_that_does_not_match_the_census() -> None:
    certificate = certificate_of(FATH)
    with pytest.raises(ProjectionIdentityError):
        ProjectionCertificate(
            source_identity=certificate.source_identity,
            fold_rule=certificate.fold_rule,
            boundary_rule=certificate.boundary_rule,
            fibers=certificate.fibers,
            findings=certificate.findings,
            residue_occurrences=0,
            residue_kinds=certificate.residue_kinds,
            trace=certificate.trace,
            domain=certificate.domain,
            scope_rank=certificate.scope_rank,
        )


def test_the_certificate_refuses_a_trace_that_reorders_the_projection() -> None:
    certificate = certificate_of(FATH)
    with pytest.raises(ProjectionIdentityError):
        ProjectionCertificate(
            source_identity=certificate.source_identity,
            fold_rule=certificate.fold_rule,
            boundary_rule=certificate.boundary_rule,
            fibers=certificate.fibers,
            findings=certificate.findings,
            residue_occurrences=certificate.residue_occurrences,
            residue_kinds=certificate.residue_kinds,
            trace=tuple(reversed(THE_ORDER)),
            domain=certificate.domain,
            scope_rank=certificate.scope_rank,
        )


def test_the_scope_stays_two_deposits_of_eighty_three_words() -> None:
    total = sum(
        census_of(source_id, WordBoundary.ANY_WHITESPACE).words
        for source_id in (FATIHA, FATH)
    )
    assert total == 83


# --- transport withholds a certificate, it does not locate a property -------


def test_the_transported_classes_gather_carriers_the_projection_separates() -> None:
    classes = uncertified_carrier_distinctions()
    assert classes
    assert all(len(klass) > 1 for klass in classes)


def test_the_uncertified_classes_are_measured_not_written_down() -> None:
    from alghanem.arabic.blind_skeleton_transport import classes_that_transport

    measured = {
        frozenset(
            {THE_FOLDING.get(letter, letter) for letter in klass}
            & set(module.the_twenty_nine())
        )
        for klass in classes_that_transport()
    }
    assert set(uncertified_carrier_distinctions()) <= measured


def test_the_fold_moves_where_the_uncertified_distinction_falls() -> None:
    classes = {frozenset(klass) for klass in uncertified_carrier_distinctions()}
    assert frozenset({"ت", "ه"}) in classes
    assert frozenset({"ء", "و"}) in classes


def test_a_failure_to_transport_is_not_read_as_a_font_or_position_property() -> None:
    residual = PROJECTION_IDENTITY_NAMED_RESIDUALS[
        "A_PROPERTY_THAT_DOES_NOT_TRANSPORT_IS_NOT_CERTIFIED_AS_A_CARRIER_INVARIANT"
    ]
    assert "لا يُثبِت موطنًا" in residual


def test_every_uncertified_class_comes_back_typed_and_grounded() -> None:
    findings = carrier_distinction_findings()
    assert len(findings) == len(uncertified_carrier_distinctions())
    assert all(isinstance(finding, CarrierDistinctionFinding) for finding in findings)
    assert {finding.members for finding in findings} == set(
        uncertified_carrier_distinctions()
    )
    for finding in findings:
        assert finding.ground.strip()


def test_the_only_standing_transport_can_issue_is_a_withheld_certificate() -> None:
    assert set(TransportStanding) == {
        TransportStanding.NOT_CERTIFIED_AS_CARRIER_INVARIANT
    }
    assert all(
        finding.standing is TransportStanding.NOT_CERTIFIED_AS_CARRIER_INVARIANT
        for finding in carrier_distinction_findings()
    )


def test_no_name_in_the_interface_reads_as_falsification() -> None:
    banned = ("false_", "_false", "refut", "disprov", "invalid", "falsif")
    for name in module.__all__:
        if name in PROJECTION_IDENTITY_NAMED_RESIDUALS:
            continue
        assert not any(word in name.lower() for word in banned), name


def test_a_class_of_one_member_is_not_a_distinction_finding() -> None:
    with pytest.raises(ProjectionIdentityError):
        CarrierDistinctionFinding(
            members=frozenset({"ب"}),
            standing=TransportStanding.NOT_CERTIFIED_AS_CARRIER_INVARIANT,
            ground="سند",
        )


def test_a_finding_without_a_written_ground_is_refused() -> None:
    with pytest.raises(ProjectionIdentityError):
        CarrierDistinctionFinding(
            members=frozenset({"ب", "ت"}),
            standing=TransportStanding.NOT_CERTIFIED_AS_CARRIER_INVARIANT,
            ground="   ",
        )


def test_the_commutation_requirement_is_bound_to_this_contract_only() -> None:
    residual = PROJECTION_IDENTITY_NAMED_RESIDUALS[
        "NO_CERTIFICATE_UNDER_AN_UNORDERED_COMPOSITION"
    ]
    assert "لا مسقطٌ لا يتبادل" in residual
    assert "شرطُ هذا" in residual


# --- no probability, and no invariance the projection itself made -----------


def test_the_projection_repeats_more_than_the_writing_does() -> None:
    assert len(repeated_words_in(FATH)) == 3
    assert len(repeated_skeletons_in(FATH)) == 5


def test_no_probability_name_is_exported_from_this_unit() -> None:
    banned = ("entropy", "probab", "nll", "likelihood", "markov", "transition_matrix")
    for name in module.__all__:
        if name in PROJECTION_IDENTITY_NAMED_RESIDUALS:
            continue
        assert not any(word in name.lower() for word in banned)


def test_no_authority_field_is_written_into_the_certificate() -> None:
    from dataclasses import fields

    named = {field.name for field in fields(ProjectionCertificate)}
    assert not named & {"verdict", "licensed", "born", "frozen", "authority", "rank"}


def test_the_scope_rank_is_local_and_not_a_kernel_readiness_rank() -> None:
    assert THE_SCOPE_RANK == "two-deposits-eighty-three-words"


# --- the residuals are named by their keys ----------------------------------


def test_every_residual_starts_with_its_own_key() -> None:
    for key, text in PROJECTION_IDENTITY_NAMED_RESIDUALS.items():
        assert text.startswith(f"{key}: ")


def test_every_named_residual_is_exported() -> None:
    for key in PROJECTION_IDENTITY_NAMED_RESIDUALS:
        assert key in module.__all__


def test_the_two_laws_of_this_unit_are_named_residuals() -> None:
    assert (
        "NO_MARKOV_STATE_WITHOUT_A_PROJECTION_IDENTITY_CERTIFICATE"
        in PROJECTION_IDENTITY_NAMED_RESIDUALS
    )
    assert (
        "NO_STATISTICAL_INVARIANCE_CLAIM_FROM_AN_INVARIANCE_"
        "THE_PROJECTION_ITSELF_MADE" in PROJECTION_IDENTITY_NAMED_RESIDUALS
    )
