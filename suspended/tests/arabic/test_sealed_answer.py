"""شهاداتُ الطبقات الخمس: الترتيبُ، والثقةُ المعلنة، والختمُ الذي لا يُتجاوَز."""

from __future__ import annotations

from collections.abc import Mapping

import pytest

from alghanem.arabic.sealed_answer import (
    THE_COURT_DOCUMENT_NAMES,
    Answer,
    Confidence,
    Domain,
    Method,
    PipelineError,
    answer_question,
    court_document_scan,
    method_for,
    perceive,
    recall_constant,
    seal_the_answer,
)
from alghanem.arabic.turuq_balance import Claim, Tariqa, weigh
from alghanem.seals import Seal, SealGenus


def _agreeing_seal(name: str) -> Seal:
    def side() -> Mapping[str, str]:
        return {"حقل": "قيمة"}

    return Seal(
        name=name,
        genus=SealGenus.GENERATED,
        origin=f"python -c '{name}'",
        generate=side,
        transcription=side,
    )


def _drifted_seal(name: str) -> Seal:
    return Seal(
        name=name,
        genus=SealGenus.GENERATED,
        origin=f"python -c '{name}'",
        generate=lambda: {"حقل": "مقيس"},
        transcription=lambda: {"حقل": "منقول"},
    )


def _sound(name: str, tariqa: Tariqa) -> Claim:
    return Claim(
        name=name,
        tariqa=tariqa,
        counted_is_the_named=True,
        is_rederived=True,
    )


def test_a_question_without_a_marker_is_refused_not_guessed_weakly() -> None:
    reading = perceive("أين المفتاح؟")
    assert reading.is_refusal
    assert reading.confidence is None


def test_a_single_domain_marker_reads_decisive_and_several_read_proxy() -> None:
    lone = perceive("ما برهانُ هذا الاستلزام؟")
    assert lone.domain is Domain.THEORETICAL
    assert lone.confidence is Confidence.DECISIVE
    mixed = perceive("ما حكمُ هذا الدليل في باب القياس؟")
    assert mixed.confidence is Confidence.PROXY


def test_no_classification_is_emitted_without_its_confidence() -> None:
    for text in ("ما برهانُ هذا؟", "كم عدُّ البايتات؟", "ما اشتقاقُ هذا الجذر؟"):
        reading = perceive(text)
        assert (reading.domain is None) == (reading.confidence is None)


def test_each_domain_has_its_own_method_and_none_is_shared() -> None:
    methods = {domain: method_for(perceive(text)) for domain, text in _one_each()}
    assert len(set(methods.values())) == len(Domain)


def _one_each() -> tuple[tuple[Domain, str], ...]:
    return (
        (Domain.THEORETICAL, "ما برهانُ هذا الاستلزام؟"),
        (Domain.EMPIRICAL, "كم عدُّ البايتات؟"),
        (Domain.LINGUISTIC, "ما اشتقاقُ هذا الجذر؟"),
        (Domain.USOOLI, "ما مناطُ الحكم؟"),
    )


def test_relating_refuses_to_run_before_perception_settles() -> None:
    with pytest.raises(PipelineError):
        method_for(perceive("أين المفتاح؟"))


def test_a_name_without_a_seal_is_refused_as_a_claim() -> None:
    found = recall_constant("لا_ختمَ_له", (_agreeing_seal("غيرُه"),))
    assert found.refused_as_claim
    assert not found.is_usable


def test_a_drifted_seal_is_not_usable_as_a_constant() -> None:
    found = recall_constant("منزاح", (_drifted_seal("منزاح"),))
    assert not found.refused_as_claim
    assert not found.is_usable


def test_an_answer_with_no_usable_evidence_is_not_emitted_at_all() -> None:
    reading = perceive("ما برهانُ هذا الاستلزام؟")
    with pytest.raises(PipelineError):
        seal_the_answer(
            reading,
            method_for(reading),
            weigh(_sound("أ", Tariqa.COUNTING), _sound("ب", Tariqa.STRUCTURE)),
            (recall_constant("مفقود", (_agreeing_seal("غيرُه"),)),),
        )


def test_a_method_borrowed_from_another_domain_is_refused() -> None:
    reading = perceive("كم عدُّ البايتات؟")
    with pytest.raises(PipelineError):
        seal_the_answer(
            reading,
            Method.FORMAL,
            weigh(_sound("أ", Tariqa.COUNTING), _sound("ب", Tariqa.STRUCTURE)),
            (recall_constant("ختم", (_agreeing_seal("ختم"),)),),
        )


def test_the_emitted_answer_carries_the_fifth_genus_in_its_footer() -> None:
    answer = answer_question(
        "ما برهانُ هذا الاستلزام؟",
        ("ختم",),
        (_agreeing_seal("ختم"),),
        _sound("عدّ", Tariqa.COUNTING),
        _sound("بنيان", Tariqa.STRUCTURE),
    )
    assert answer.seal_genus is SealGenus.ANSWER_SEALED
    assert SealGenus.ANSWER_SEALED.value in answer.footer
    assert "ختم" in answer.footer


def test_an_answer_cannot_be_stamped_with_any_other_genus() -> None:
    reading = perceive("ما برهانُ هذا الاستلزام؟")
    with pytest.raises(PipelineError):
        Answer(
            perception=reading,
            method=Method.FORMAL,
            weighing=weigh(_sound("أ", Tariqa.COUNTING), _sound("ب", Tariqa.STRUCTURE)),
            evidence=(recall_constant("ختم", (_agreeing_seal("ختم"),)),),
            seal_genus=SealGenus.GENERATED,
        )


def test_the_fifth_genus_is_named_and_not_folded_into_the_four() -> None:
    values = {genus.value for genus in SealGenus}
    assert SealGenus.ANSWER_SEALED.value == "مختومُ_جواب"
    assert len(values) == len(SealGenus)


def test_a_misnamed_count_stops_the_pipeline_before_any_answer() -> None:
    misnamed = Claim(
        name="الشدّةُ مسمّاةً إدغامًا",
        tariqa=Tariqa.COUNTING,
        counted_is_the_named=False,
        is_rederived=True,
    )
    with pytest.raises(PipelineError):
        answer_question(
            "ما برهانُ هذا الاستلزام؟",
            ("ختم",),
            (_agreeing_seal("ختم"),),
            misnamed,
            _sound("بنيان", Tariqa.STRUCTURE),
        )


def test_the_four_court_documents_are_absent_and_the_scanner_is_not_blind() -> None:
    scan = court_document_scan()
    assert scan.absent == THE_COURT_DOCUMENT_NAMES
    assert scan.present == ()
    assert scan.scanner_is_not_blind
    assert scan.absence_is_admissible


def test_the_absence_verdict_is_withheld_from_a_blind_scanner() -> None:
    from alghanem.arabic.sealed_answer import CourtDocumentScan

    blind = CourtDocumentScan(
        present=(),
        absent=THE_COURT_DOCUMENT_NAMES,
        documents_the_scanner_did_see=0,
    )
    assert not blind.absence_is_admissible
