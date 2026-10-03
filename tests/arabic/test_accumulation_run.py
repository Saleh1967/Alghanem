"""اختباراتُ الشريحة — **مصدريّةٌ، مفصولةٌ عن اختبارات العقود**.

العقودُ الاصطناعيّةُ في `tests/ontology/test_accumulation.py`؛ وههنا شاهدٌ من
بايتاتٍ على القرص: «التفكير» بختمه، تُقرأ منه أربعةُ مواضعَ ويُفحَص أنّ ما
نُقِل هو ما فيه. ولا اتّصالَ لغويًّا ههنا ولا مسارَ ١١٦.
"""

from __future__ import annotations

import hashlib

import pytest

from alghanem.arabic.accumulation_run import (
    THE_BOOK_SEAL,
    THE_SOURCE_CARDS,
    base_stock,
    living_rule,
    read_source_cards,
    run_slice,
    source_propositions,
    the_book_path,
    the_extraction,
)
from alghanem.ontology import ClaimStanding, Polarity, PropositionForm


def test_the_scanned_book_is_present_under_its_declared_seal() -> None:
    path = the_book_path()
    assert path.is_file()
    assert hashlib.sha256(path.read_bytes()).hexdigest() == THE_BOOK_SEAL


def test_every_card_is_reproduced_from_the_bytes_at_its_own_offsets() -> None:
    text = the_extraction()
    for card in THE_SOURCE_CARDS:
        assert text[card.start : card.end] == card.excerpt


def test_each_excerpt_occurs_exactly_once_so_the_offset_is_not_ambiguous() -> None:
    text = the_extraction()
    for card in THE_SOURCE_CARDS:
        assert text.count(card.excerpt) == 1


def test_the_cards_are_read_as_reproduced() -> None:
    readings = read_source_cards()
    assert len(readings) == len(THE_SOURCE_CARDS)
    assert all(one.is_reproduced for one in readings)


def test_a_card_whose_excerpt_is_shifted_is_not_reproduced() -> None:
    from alghanem.arabic.accumulation_run import SourceCard

    card = THE_SOURCE_CARDS[0]
    moved = SourceCard(
        card_id=card.card_id,
        start=card.start + 1,
        end=card.end + 1,
        excerpt=card.excerpt,
        standing_note=card.standing_note,
        extracted_meaning=card.extracted_meaning,
        engineering_counterpart=card.engineering_counterpart,
        counterpart_limit=card.counterpart_limit,
    )
    assert the_extraction()[moved.start : moved.end] != moved.excerpt


def test_a_card_refuses_a_span_that_does_not_match_its_excerpt_length() -> None:
    from alghanem.arabic.accumulation_run import SourceCard

    with pytest.raises(ValueError):
        SourceCard(
            card_id="بطاقةٌ-مكسورة",
            start=0,
            end=3,
            excerpt="أربعة",
            standing_note="لا شيء",
            extracted_meaning="لا شيء",
            engineering_counterpart="لا شيء",
            counterpart_limit="لا شيء",
        )


def test_every_card_names_the_limit_of_its_engineering_counterpart() -> None:
    for card in THE_SOURCE_CARDS:
        assert card.counterpart_limit.strip()
        assert card.standing_note.strip()


def test_the_source_propositions_attribute_a_saying_and_not_an_outside_fact() -> None:
    rows = source_propositions()
    assert len(rows) == len(THE_SOURCE_CARDS)
    for _, _, proposition in rows:
        assert proposition.form is PropositionForm.ATTRIBUTE_VALUE
        assert proposition.predicate_id == "نصُّ-الوقوع"
        assert proposition.polarity is Polarity.AFFIRMED


def test_no_source_card_is_turned_into_an_adopted_rule() -> None:
    stock = base_stock()
    assert stock.rules == ()
    assert stock.adoptions == ()


def test_the_rule_of_the_slice_is_not_adopted_before_its_licence() -> None:
    stock = base_stock()
    assert stock.is_adopted(living_rule().versioned_id) is False


def test_no_evidence_in_the_simulated_domain_is_a_direct_observation() -> None:
    from alghanem.ontology import EvidenceGenus

    for one in base_stock().register.evidence:
        assert one.genus is not EvidenceGenus.DIRECT_OBSERVATION


def test_two_individuals_sharing_a_surface_are_not_merged_by_the_name() -> None:
    from alghanem.ontology import candidates_for_surface

    stock = base_stock()
    candidates = candidates_for_surface("سالم", stock.identity, stock.register)
    assert len(candidates) == 2
    assert stock.identity.links == ()


def test_the_slice_runs_and_reports_nine_numbered_lines() -> None:
    outcome = run_slice()
    assert len(outcome.lines) == 9
    assert all(line.strip() for line in outcome.lines)


def test_the_slice_fingerprint_moves_at_every_recorded_stage() -> None:
    marks = run_slice().fingerprints
    assert len(marks) == 4
    assert len({digest for _, digest in marks}) == 4


def test_the_slice_is_deterministic_on_the_same_tree() -> None:
    assert run_slice().fingerprints == run_slice().fingerprints


def test_the_slice_shows_a_witnessed_conflict_and_an_unwitnessed_agreement() -> None:
    lines = run_slice().lines
    assert "مشهودٌ" in lines[2]
    assert "غيرُ مشهود" in lines[4]


def test_the_slice_keeps_the_corrected_judgment_and_names_its_policy() -> None:
    line = run_slice().lines[3]
    assert "معلَّقٌ ومحفوظ" in line
    assert "يبقى_معلَّقًا" in line


def test_the_slice_moves_from_support_to_dependency_conflict_and_back() -> None:
    lines = run_slice().lines
    assert ClaimStanding.SUPPORTED_IN_SCOPE.value in lines[7]
    assert ClaimStanding.DEPENDENCY_CONFLICT.value in lines[7]
    assert ClaimStanding.SUPPORTED_IN_SCOPE.value in lines[8]


def test_a_second_domain_passes_through_the_same_operations() -> None:
    """المدينةُ والشخصُ يمرّان بالعمليّات نفسِها، بلا دالّةٍ خاصّةٍ بمجال."""

    import alghanem.arabic.accumulation_run as module

    names = {name for name in dir(module) if name.startswith("_run_")}
    assert names == set()
