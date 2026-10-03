"""شواهدُ سلسلة الشهادة: يُشتَقّ الحكمُ ههنا ولا يُستلَم، ويَسقط بسقوط لازمه."""

from __future__ import annotations

import pytest

from alghanem.arabic.epistemic_layers import EpistemicStanding
from alghanem.arabic.excerpt_origin_bridge import (
    ClaimStanding,
    OriginWitness,
    WordAddress,
    locate,
)
from alghanem.arabic.word_certificate_chain import (
    AnalysisSubject,
    AnalysisWitness,
    CertificateLayer,
    LayerStanding,
    WordCertificateError,
    canonical_admission,
    certify,
    fingerprint,
    tanwin_reading,
)

THE_SURFACE = "\u062d\u064e\u064a\u064e\u0627\u0629\u064c"
THE_ADDRESS = WordAddress("QURAN_SIMPLE", 186, 4)
THE_MIRROR = WordAddress("GLOBALQURAN_SIMPLE", 186, 4)


def _origin_witness(address: WordAddress) -> OriginWitness:
    located = locate(address)
    return OriginWitness(
        dataset_id="TEST",
        dataset_line_id=address.rendered,
        source_key=address.source_key,
        source_char_offset=located.char_offset,
        method="حلُّ عنوانٍ مختوم",
        examiner="tests",
    )


def _analysis(
    subject: AnalysisSubject, claim: str = "دعوى", surface: str = THE_SURFACE
) -> AnalysisWitness:
    return AnalysisWitness(
        subject=subject,
        claim=claim,
        surface=surface,
        lexical_source="corpora/quran-simple-enhanced.txt",
        lexical_locus="2:179",
        examiner="tests",
    )


def _full_witnesses() -> tuple[AnalysisWitness, ...]:
    return (
        _analysis(AnalysisSubject.ROOT_AND_WAZN),
        _analysis(AnalysisSubject.SYNTACTIC_FUNCTION),
    )


# ١ — وقوعٌ حقيقيٌّ تُعاد شهادتُه من بايتاته


def test_a_real_occurrence_rebuilds_its_certificate_from_the_bytes() -> None:
    """الشهادةُ تُعاد من القرص عند كلّ نداء، فتثبت بصمتُها بلا تخزين."""

    first = certify(THE_ADDRESS)
    second = certify(THE_ADDRESS)
    assert first.located.surface == THE_SURFACE
    assert fingerprint(first) == fingerprint(second)
    assert len(first.transitions) == 7
    assert {one.layer for one in first.verdicts} == set(CertificateLayer)


def test_every_transition_names_its_nine_fields() -> None:
    """تسعةُ حقولٍ لا يُطوى منها حقل، والرتبةُ من السلّم القائم لا من جديد."""

    for step in certify(THE_ADDRESS).transitions:
        assert step.station_in and step.station_out
        assert step.condition and step.obstacle and step.witness
        assert isinstance(step.rank, EpistemicStanding)


# ٢ — العبارةُ نفسُها في مصدرَين بسياقَين مختلفَين


def test_the_same_surface_in_two_sources_yields_two_certificates() -> None:
    """المصدرُ جزءٌ من الهويّة: يتبدّل فتتبدّل الإزاحةُ والبصمةُ معًا."""

    here = certify(THE_ADDRESS)
    there = certify(THE_MIRROR)
    assert here.located.surface == there.located.surface == THE_SURFACE
    assert here.located.char_offset != there.located.char_offset
    assert fingerprint(here) != fingerprint(there)


# ٣ — مصدرٌ صحيحٌ بموضعِ مقتطفٍ خاطئ


def test_a_right_source_with_a_wrong_excerpt_offset_blocks_the_reference() -> None:
    """الموضعُ الخاطئ يَرُدّ المنشأَ بدليل، فتُحجَب طبقةُ الإحالة وحدَها."""

    bad = OriginWitness(
        dataset_id="TEST",
        dataset_line_id="L186:W4",
        source_key="QURAN_SIMPLE",
        source_char_offset=999_999,
        method="m",
        examiner="tests",
    )
    certificate = certify(
        THE_ADDRESS, witnesses=(bad,), analysis_witnesses=_full_witnesses()
    )
    assert certificate.is_licensed is False
    reference = next(
        one
        for one in certificate.verdicts
        if one.layer is CertificateLayer.REFERENCE
    )
    assert reference.standing is LayerStanding.SUSPENDED_BY_NAMED_CAUSE


# ٤ — تغييرُ شاهد الإحالة أو سحبُه


def test_withdrawing_the_origin_witness_only_unseats_the_reference() -> None:
    """سحبُ شاهدٍ يُسقِط تابعَه وحدَه، وتبقى الطبقاتُ المستقلّةُ مرخَّصة."""

    with_it = certify(
        THE_ADDRESS,
        witnesses=(_origin_witness(THE_ADDRESS),),
        analysis_witnesses=_full_witnesses(),
    )
    without = certify(THE_ADDRESS, analysis_witnesses=_full_witnesses())
    assert with_it.is_licensed is True
    assert without.is_licensed is False
    for layer in (CertificateLayer.ENCODING, CertificateLayer.CANONICAL_ADMISSION):
        kept = next(one for one in without.verdicts if one.layer is layer)
        assert kept.standing is LayerStanding.LICENSED_IN_SCOPE


def test_withdrawing_the_root_witness_cascades_into_the_syntax_premise() -> None:
    """التابعُ يسقط بسقوط متبوعه: لا إعرابَ على جذرٍ لم يَثبُت."""

    certificate = certify(
        THE_ADDRESS,
        witnesses=(_origin_witness(THE_ADDRESS),),
        analysis_witnesses=(_analysis(AnalysisSubject.SYNTACTIC_FUNCTION),),
    )
    blocked = set(certificate.overall.blocking_premises)
    assert "\u0627\u0644\u062c\u0630\u0631\u064f \u0648\u0627\u0644\u0648\u0632\u0646\u064f \u0645\u062f\u062e\u0644\u0627\u0646 \u0645\u0639\u062c\u0645\u064a\u0651\u0627\u0646" in blocked
    syntax = next(
        one for one in certificate.premises if one.layer is CertificateLayer.SYNTAX
    )
    assert syntax.standing is ClaimStanding.SUSPENDED


def test_a_witness_whose_surface_differs_is_not_admitted() -> None:
    """شاهدٌ يصف سطحًا آخَر لا يُقبَل، ولو كان مصدرُه حاضرًا مختومًا."""

    certificate = certify(
        THE_ADDRESS,
        analysis_witnesses=(
            _analysis(
                AnalysisSubject.ROOT_AND_WAZN,
                surface="\u0646\u064e\u0638\u064e\u0631\u064c",
            ),
        ),
    )
    morphology = next(
        one for one in certificate.verdicts if one.layer is CertificateLayer.MORPHOLOGY
    )
    assert morphology.standing is LayerStanding.SUSPENDED_BY_NAMED_CAUSE


def test_a_witness_pointing_at_an_absent_source_is_not_admitted() -> None:
    """حضورُ المصدر يُقاس من القرص، فلا يُقبَل شاهدٌ يُحيل إلى غائب."""

    ghost = AnalysisWitness(
        subject=AnalysisSubject.ROOT_AND_WAZN,
        claim="دعوى",
        surface=THE_SURFACE,
        lexical_source="corpora/this-file-does-not-exist.txt",
        lexical_locus="x",
        examiner="tests",
    )
    assert ghost.source_is_present() is False
    certificate = certify(THE_ADDRESS, analysis_witnesses=(ghost,))
    morphology = next(
        one for one in certificate.verdicts if one.layer is CertificateLayer.MORPHOLOGY
    )
    assert morphology.standing is LayerStanding.SUSPENDED_BY_NAMED_CAUSE


# ٥ — دورُ التنوين، والرسمُ المحفوظ غيرُ التصيير الوقفيّ


def test_the_tanwin_nun_is_never_counted_among_the_root_letters() -> None:
    """نونُ التنوين تُعزَل بالمحارف، ولا تدخل في الحوامل البتّة."""

    reading = tanwin_reading(THE_SURFACE)
    assert reading.present is True
    assert reading.nun_is_a_root_letter is False
    assert "\u064c" not in reading.carriers_without_the_mark
    assert tanwin_reading("\u0627\u0644\u0652").present is False


def test_the_rasm_is_not_recoverable_from_the_one_hundred_sixteen() -> None:
    """الذرّاتُ تصييرٌ وصليّ: «ة» تصير «تُ» والتنوينُ «نْ»، فلا يُستردّ الرسم."""

    admission = canonical_admission(THE_SURFACE)
    assert admission.status == "READY"
    assert admission.replay_reproduced is True
    assert admission.rasm_is_recoverable_from_the_atoms is False
    assert set(admission.lost_in_the_rendering) == {"\u0629", "\u064c"}


def test_a_ready_protocol_state_is_not_a_licence_of_the_word() -> None:
    """حالةٌ جاهزةٌ مع حكمٍ إجماليٍّ معلَّق: الطبقاتُ لا يُنقَل حكمُ إحداها."""

    certificate = certify(THE_ADDRESS)
    assert certificate.admission.protocol_is_legal is True
    assert certificate.is_licensed is False


# ٦ — حدودُ الابتداء والوصل والوقف


def test_wasl_is_tested_only_against_a_neighbour_that_exists_in_the_bytes() -> None:
    """لا تُختلَق كلمةٌ تالية: الوصلُ يُختبَر بجارٍ مقروءٍ أو لا يُختبَر."""

    certificate = certify(THE_ADDRESS)
    assert certificate.boundary.wasl_is_testable is True
    assert certificate.boundary.following_word is not None
    tail = locate(THE_ADDRESS)
    last = WordAddress("QURAN_SIMPLE", 186, len(tail.line_text.split()))
    edge = certify(last)
    assert edge.boundary.wasl_is_testable is False
    assert edge.boundary.following_word is None


def test_a_pause_performance_is_never_read_from_a_boundary_alone() -> None:
    """آخِرُ السطر حدُّ ملفٍّ لا أداءُ قارئ، فتبقى المقدّمةُ معلَّقةً دومًا."""

    for address in (THE_ADDRESS, THE_MIRROR):
        certificate = certify(address)
        waqf = next(
            one
            for one in certificate.premises
            if one.layer is CertificateLayer.SYLLABLE_LICENCE
            and "\u0627\u0644\u0648\u0642\u0641" in one.name
        )
        assert waqf.standing is ClaimStanding.SUSPENDED
        assert waqf.required_for_the_claim is False


# ٧ — إعادةُ بصمةِ شهادةٍ محرّفة


def test_a_tampered_certificate_does_not_reproduce_its_fingerprint() -> None:
    """البصمةُ من المحتوى المُشتَقّ: من حرّف سطحًا أو منزلةً تحرّكت بصمتُه."""

    honest = certify(THE_ADDRESS)
    moved = certify(WordAddress("QURAN_SIMPLE", 186, 3))
    licensed = certify(
        THE_ADDRESS,
        witnesses=(_origin_witness(THE_ADDRESS),),
        analysis_witnesses=_full_witnesses(),
    )
    assert len({fingerprint(honest), fingerprint(moved), fingerprint(licensed)}) == 3


# ٨ — الحكمُ مُشتَقٌّ ولا يُستلَم


def test_the_issuer_refuses_a_standing_supplied_by_the_caller() -> None:
    """لا تُبتلَع دعوى المستدعي صامتةً: تُرَدّ باسم القاعدة ويُرفَع الخطأ."""

    with pytest.raises(WordCertificateError):
        certify(THE_ADDRESS, standing_from_caller="\u0645\u0631\u062e\u0651\u0635\u0629")


def test_an_absent_evidence_is_suspended_and_never_refused() -> None:
    """غيابُ الدليل تعليقٌ مسمًّى؛ ولا يُقال ممتنعٌ إلّا بدليلٍ مقيس."""

    certificate = certify(THE_ADDRESS)
    standings = {one.standing for one in certificate.verdicts}
    assert LayerStanding.REFUSED_WITH_EVIDENCE not in standings
    assert LayerStanding.SUSPENDED_BY_NAMED_CAUSE in standings
    assert certificate.overall.blocking_premises


def test_a_premise_without_its_four_answers_is_refused_at_construction() -> None:
    """السكوتُ عن أحد الأسئلة الأربعة يُرَدّ عند البناء لا عند القراءة."""

    from alghanem.arabic.word_certificate_chain import Premise

    with pytest.raises(WordCertificateError):
        Premise(
            name="x",
            layer=CertificateLayer.SYNTAX,
            why_invoked="",
            admission_evidence="b",
            why_it_applies_here="c",
            what_it_establishes="d",
            standing=ClaimStanding.ESTABLISHED,
            required_for_the_claim=True,
        )


# ٩ — حالةٌ مستقلّةٌ لم يُصمَّم التنفيذُ لنصّها


def test_an_independent_address_the_chain_was_not_designed_for() -> None:
    """موضعٌ آخَرُ بلا تنوينٍ ولا تاءٍ مربوطة: السلسلةُ تعمل بلا تخصيص."""

    address = WordAddress("QURAN_SIMPLE", 1, 1)
    certificate = certify(address)
    assert certificate.located.surface
    assert certificate.boundary.ibtida_is_readable is True
    assert certificate.boundary.preceding_word is None
    assert len(certificate.transitions) == 7
    assert certificate.overall.standing is LayerStanding.SUSPENDED_BY_NAMED_CAUSE
    assert fingerprint(certificate) != fingerprint(certify(THE_ADDRESS))


# ١٠ — النطاقُ مُعلَنٌ قبل القياس، ولا يُضيَّق بعده


def test_the_declared_scope_insulates_the_quran_results() -> None:
    """العزلُ مُعلَنٌ في كلّ حكمٍ مرخَّص، فلا تُرحَّل نتيجةٌ إلى الإملاء."""

    certificate = certify(
        THE_ADDRESS,
        witnesses=(_origin_witness(THE_ADDRESS),),
        analysis_witnesses=_full_witnesses(),
    )
    assert certificate.is_licensed is True
    assert certificate.scope.insulation[0] in certificate.overall.cause
    assert certificate.scope.deferred
