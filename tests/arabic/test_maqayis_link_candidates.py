"""شواهدُ آلة المرشَّحات: تكشف العبورَ غيرَ المرخَّص، ولا تُفتَح بها بوّابة.

والاختباراتُ ههنا بابان مفصولان بنصّهما:

* **بابُ العشرين الفعليّة** — يقرأ البايتات المختومة ويشهد على ما فيها.
* **بابُ الحارس** — يصنع مرشَّحًا بيدٍ من صفوفٍ حقيقيّةٍ ليمتحن سلوكَ الحارس
  وحدَه؛ ولا يُقرأ شيءٌ منه شاهدًا على صحّة معنًى عربيّ.
"""

from __future__ import annotations

import dataclasses

import pytest

from alghanem.arabic.dal_madlul_bridge import SealStanding, governing_seal_reading
from alghanem.arabic.maqayis_link_candidates import (
    AN_ADMITTED_LEXICAL_LINK_ASSERTS_NO_EXTERNAL_FACT,
    MAQAYIS_LINK_CANDIDATE_NAMED_RESIDUALS,
    THE_CANDIDATE_SAMPLE_SIZE,
    THE_DISPLAY_EXCERPT_LIMIT,
    AdmissionStanding,
    AttributionCheck,
    BoundaryStanding,
    DalProcessing,
    InputUnitKind,
    LinkChainRung,
    MaqayisLinkCandidateError,
    ReviewAttestation,
    SufficiencyCheck,
    SuspensionGenus,
    candidate_counts,
    chain_reach,
    dal_readings,
    input_unit_reading,
    link_candidates,
    provenance_shares,
    report_rows,
    verify,
)
from alghanem.arabic.maqayis_witness_census import AxesStanding

# ── بابُ العشرين الفعليّة ───────────────────────────────────────────────


def test_the_input_unit_is_measured_and_is_not_a_used_word() -> None:
    """وحدةُ المدخل مفتاحُ جذرٍ مقيسًا: مطويُّ التضعيف في أكثره، عاري الحركة كلِّه."""

    reading = input_unit_reading()
    assert reading.examined == THE_CANDIDATE_SAMPLE_SIZE
    assert reading.bearing_a_written_haraka == 0
    assert reading.collapsed_gemination > 0
    assert reading.equal_to_root_full + reading.collapsed_gemination == reading.examined
    assert reading.kind is InputUnitKind.ROOT_KEY_DISPLAY_FORM


def test_all_twenty_dals_are_kept_including_the_blank_and_the_suspect() -> None:
    """العشرون محفوظون: الفارغُ صفٌّ، والمشتبهُ صفٌّ، ولا يُحذَف متعذِّر."""

    readings = dal_readings()
    assert len(readings) == THE_CANDIDATE_SAMPLE_SIZE
    assert sum(1 for reading in readings if reading.candidates == 0) > 0
    assert (
        sum(1 for reading in readings if reading.boundary is BoundaryStanding.SUSPECT)
        > 0
    )
    assert any(
        reading.axes_count_standing == AxesStanding.BLANK for reading in readings
    )


def test_the_counts_are_in_separate_units_and_never_sum_to_the_sample_size() -> None:
    """الدالُّ وحدةٌ والمحورُ وحدةٌ والمرشَّحُ وحدة؛ فلا تُجمَع في معادلةٍ واحدة."""

    counts = candidate_counts()
    readings = dal_readings()
    assert counts["دوال"] == THE_CANDIDATE_SAMPLE_SIZE
    assert counts["مرشحات"] == counts["محاور_مكتوبة"]
    assert counts["معتمدون"] + counts["معلقون"] == counts["مرشحات"]
    # دالٌّ واحدٌ يُخرِج محاورَ عدّة، فمقامُ المرشَّحين ليس مقامَ الدوالّ.
    assert any(reading.declared_axes > 1 for reading in readings)
    assert counts["مرشحات"] != counts["دوال"]


def test_a_dal_with_more_than_one_axis_keeps_every_axis_and_its_alternatives() -> None:
    """تعدُّدُ المحاور محفوظٌ: مرشَّحٌ لكلّ محور، وبدائلُه إخوتُه في صفّه."""

    multiples = [
        candidate for candidate in link_candidates() if candidate.axis_total > 1
    ]
    assert multiples
    for candidate in multiples:
        assert len(candidate.alternatives) == candidate.axis_total - 1
        assert candidate.candidate_meaning not in candidate.alternatives


def test_the_axes_count_disagreement_is_recorded_without_adjudication() -> None:
    """خلافُ `axes_count` يُسجَّل بموقفه، ولا يُرجَّح طرفٌ آليًّا على طرف."""

    readings = dal_readings()
    standings = {reading.axes_count_standing for reading in readings}
    assert AxesStanding.DIFFERS in standings
    assert AxesStanding.AGREES in standings
    assert AxesStanding.BLANK in standings
    # المُخالِفُ يبقى مُخالِفًا ولا يُحوَّل عددُه ولا تُبدَّل قاعدةُ فصله.
    differing = [
        reading
        for reading in readings
        if reading.axes_count_standing == AxesStanding.DIFFERS
    ]
    for reading in differing:
        assert reading.candidates == reading.declared_axes


def test_no_candidate_is_admitted_and_each_suspension_names_its_genus() -> None:
    """لا معتمَدَ على هذه البايتات، وكلُّ تعليقٍ بجنسٍ مُسمًّى وشرطٍ غيرِ مستوفًى."""

    counts = candidate_counts()
    assert counts["معتمدون"] == 0
    for candidate in link_candidates():
        reading = verify(candidate)
        assert reading.standing is AdmissionStanding.SUSPENDED
        assert reading.suspension_genus is not None
        assert reading.unmet_conditions


def test_absent_evidence_and_counter_evidence_are_two_different_genera() -> None:
    """صفٌّ ساكتُ الحقل غيرُ صفٍّ يقول متنُه «ليس بأصل»؛ وفرقُهما مقيسٌ لا مقول."""

    empty = {
        reading.root_display: reading
        for reading in dal_readings()
        if reading.candidates == 0
    }
    assert empty
    genera = {name: reading.suspension_genera for name, reading in empty.items()}
    assert any(
        SuspensionGenus.COUNTER_EVIDENCE in value for value in genera.values()
    ), genera
    assert any(
        SuspensionGenus.ABSENT_EVIDENCE in value for value in genera.values()
    ), genera


def test_the_three_witnesses_separate_on_the_real_rows() -> None:
    """الشهاداتُ الثلاثُ تفترق فعلًا: سلامةٌ تامّة، ونسبةٌ قائمة، وكفايةٌ متفاوتة."""

    verifications = [verify(candidate) for candidate in link_candidates()]
    assert all(reading.source_integrity for reading in verifications)
    assert all(
        reading.attribution
        in (AttributionCheck.IN_THIS_MATERIAL, AttributionCheck.BOUNDARY_SUSPECT)
        for reading in verifications
    )
    sufficiency = {reading.sufficiency for reading in verifications}
    assert SufficiencyCheck.NOT_FOUND_IN_THE_WITNESS in sufficiency
    assert len(sufficiency) > 1


def test_a_normalised_agreement_is_never_read_as_a_verbatim_one() -> None:
    """الموافقةُ بعد تجريد التشكيل تُسمّى باسمها، فلا تُقرأ إسنادًا بالحروف."""

    normalised = [
        reading
        for reading in (verify(candidate) for candidate in link_candidates())
        if reading.sufficiency is SufficiencyCheck.SUPPORTED_UNDER_A_NAMED_NORMALISATION
    ]
    assert normalised
    for reading in normalised:
        assert reading.standing is AdmissionStanding.SUSPENDED
        assert reading.candidate.candidate_meaning not in reading.candidate.witness.text


def test_the_governing_text_absence_suspends_only_the_signification_kind() -> None:
    """غيابُ النصّ الحاكم يُعلِّق التصنيفَ وحدَه، ويبقى العملُ المعجميُّ ماضيًا."""

    assert governing_seal_reading().standing is SealStanding.ABSENT_FROM_THIS_TREE
    candidates = link_candidates()
    assert candidates
    assert all(candidate.signification_kind is None for candidate in candidates)


def test_the_chain_stops_at_the_lafz_by_a_declared_prohibition() -> None:
    """الوصلتان الرابعةُ والخامسةُ ممتنعتان بالنظام لا بنقص دليل، ويُقال ذلك."""

    reach = dict((rung, (ok, why)) for rung, ok, why in chain_reach())
    assert reach[LinkChainRung.MATERIAL_KEY][0] is True
    assert reach[LinkChainRung.VERIFIED_MATERIAL][0] is True
    assert reach[LinkChainRung.EXTRACTED_MEANING][0] is False
    assert reach[LinkChainRung.LAFZ][0] is False
    assert reach[LinkChainRung.USAGE][0] is False
    assert "مشتقٍّ" in reach[LinkChainRung.USAGE][1]


def test_nothing_here_is_claimed_to_be_generated_from_structure() -> None:
    """المعنى منقولٌ من رصيدٍ لا مولَّدٌ من بنية؛ والنسبُ الثلاثُ معدودة."""

    shares = provenance_shares()
    assert shares.generated_from_structure == 0
    assert shares.transported_from_stock == candidate_counts()["مرشحات"]
    assert shares.established_by_linking == candidate_counts()["معتمدون"]


def test_the_display_excerpt_never_replaces_the_full_witness_reference() -> None:
    """المقتطفُ عرضٌ والمرجعُ شاهد؛ وحدُّ العرض لا يبتر ما يُعاد به التحقّق."""

    for candidate in link_candidates():
        witness = candidate.witness
        assert witness.end_offset > witness.start_offset
        assert "نقاط الشفرة" in witness.offset_unit
        assert len(witness.display_excerpt) <= THE_DISPLAY_EXCERPT_LIMIT
        assert witness.display_excerpt == witness.text[:THE_DISPLAY_EXCERPT_LIMIT]
        if witness.is_truncated_for_display:
            assert len(witness.text) > len(witness.display_excerpt)


def test_the_report_carries_a_row_for_every_dal_and_every_candidate() -> None:
    """السجلُّ يحمل جنسَ كلِّ صفّ، فلا يُقرأ صفُّ دالٍّ مرشَّحًا ولا مرشَّحٌ معتمَدًا."""

    rows = report_rows()
    kinds = [row["نوع"] for row in rows]
    assert kinds.count("دال") == THE_CANDIDATE_SAMPLE_SIZE
    assert kinds.count("مرشح") == candidate_counts()["مرشحات"]
    assert kinds.count("وصلة") == len(LinkChainRung)
    assert "عدّ" in kinds
    assert all(row["حال_الاعتماد"] == "معلَّق" for row in rows if row["نوع"] == "مرشح")


def test_every_named_residual_is_exported_and_prefixed_by_its_own_name() -> None:
    """كلُّ باقٍ مُسمًّى مُصدَّرٌ، ونصُّه يبدأ باسمه؛ ولا اسمَ بلا نصّ."""

    assert MAQAYIS_LINK_CANDIDATE_NAMED_RESIDUALS
    for name, text in MAQAYIS_LINK_CANDIDATE_NAMED_RESIDUALS.items():
        assert text.startswith(name)


# ── بابُ الحارس: مرشَّحاتٌ تُصنَع بيدٍ لامتحان السلوك وحدَه ───────────────
#
# ما تحت هذا الخطّ **لا يشهد على صحّة معنًى عربيّ**: هو امتحانُ حارسٍ يُبنى
# على صفوفٍ حقيقيّةٍ من البايتات المختومة، ويُقرأ سلوكًا لا لغة.


def _sound_candidate():
    """مرشَّحٌ من صفٍّ حدُّه محقَّقٌ، ليُمتحَن عليه الحارسُ صعودًا وهبوطًا."""

    for candidate in link_candidates():
        if candidate.boundary is BoundaryStanding.SOUND:
            return candidate
    raise AssertionError("لا صفَّ محقَّقَ الحدّ في العيّنة، فلا يُمتحَن الحارس.")


def _verbatim_candidate():
    """مرشَّحٌ مصنوعٌ معناه مقتطعٌ من شاهده بحروفه، فتستوفي الكفايةُ شرطَها."""

    candidate = _sound_candidate()
    witness = candidate.witness.text
    return dataclasses.replace(candidate, candidate_meaning=witness[5:15])


def _review_for(candidate) -> ReviewAttestation:
    return ReviewAttestation(
        material_key=candidate.material_key,
        candidate_meaning=candidate.candidate_meaning,
        witness_text=candidate.witness.text,
        reviewer="امتحانُ حارسٍ مصطنع",
        statement="مودَعٌ لامتحان البوّابة وحدَها، لا شهادةً على معنًى عربيّ",
    )


def test_the_guard_admits_only_when_all_five_conditions_meet() -> None:
    """البوّابةُ تفتح فعلًا: فحصٌ صاعدٌ يمنع أن يكون صفرُ المعتمَدين عمى آلة."""

    candidate = _verbatim_candidate()
    reading = verify(candidate, reviews=(_review_for(candidate),))
    assert reading.sufficiency is SufficiencyCheck.SUPPORTS_VERBATIM
    assert reading.attribution is AttributionCheck.IN_THIS_MATERIAL
    assert reading.standing is AdmissionStanding.ADMITTED
    assert reading.unmet_conditions == ()


def test_a_genuine_witness_from_another_material_fails_the_attribution() -> None:
    """شاهدٌ أصيلٌ في الملفّ لكنّه من مادّةٍ أخرى: تسقط النسبةُ ولا يُعتمَد."""

    candidates = link_candidates()
    host = _verbatim_candidate()
    foreign = next(
        other
        for other in candidates
        if other.row_index != host.row_index and other.witness.text != host.witness.text
    )
    transplanted = dataclasses.replace(host, witness=foreign.witness)
    reading = verify(transplanted, reviews=(_review_for(transplanted),))
    assert reading.attribution is not AttributionCheck.IN_THIS_MATERIAL
    assert reading.standing is AdmissionStanding.SUSPENDED
    assert any("صحّةُ النسبة" in condition for condition in reading.unmet_conditions)


def test_a_witness_inside_the_material_that_does_not_support_the_meaning() -> None:
    """شاهدٌ من المادّة نفسِها لا يُسنِد المعنى: لا تكفي الأوّلتان لاعتماده."""

    candidate = dataclasses.replace(
        _sound_candidate(), candidate_meaning="معنًى لا يقع في هذا الشاهد البتّة"
    )
    reading = verify(candidate, reviews=(_review_for(candidate),))
    assert reading.source_integrity is True
    assert reading.attribution is AttributionCheck.IN_THIS_MATERIAL
    assert reading.sufficiency is SufficiencyCheck.NOT_FOUND_IN_THE_WITNESS
    assert reading.standing is AdmissionStanding.SUSPENDED


def test_a_suspect_boundary_suspends_what_depends_on_it() -> None:
    """حدُّ مادّةٍ مشتبهٌ يُعلِّق نتائجَه التابعة ولو استوفى غيرُها شرطَه."""

    suspect = next(
        candidate
        for candidate in link_candidates()
        if candidate.boundary is BoundaryStanding.SUSPECT
    )
    forged = dataclasses.replace(suspect, candidate_meaning=suspect.witness.text[5:15])
    reading = verify(forged, reviews=(_review_for(forged),))
    assert reading.sufficiency is SufficiencyCheck.SUPPORTS_VERBATIM
    assert reading.attribution is AttributionCheck.BOUNDARY_SUSPECT
    assert reading.standing is AdmissionStanding.SUSPENDED
    assert reading.suspension_genus is SuspensionGenus.ABSENT_EVIDENCE


def test_a_reviewed_material_does_not_open_its_neighbours() -> None:
    """مراجعةُ مادّةٍ إذنٌ فيها وحدَها، فلا تفتح جارتَها ولا معنًى آخرَ فيها."""

    candidate = _verbatim_candidate()
    review = _review_for(candidate)
    neighbour = next(
        other
        for other in link_candidates()
        if other.boundary is BoundaryStanding.SOUND
        and other.material_key != candidate.material_key
    )
    forged = dataclasses.replace(
        neighbour, candidate_meaning=neighbour.witness.text[5:15]
    )
    assert verify(forged, reviews=(review,)).standing is AdmissionStanding.SUSPENDED
    assert verify(candidate, reviews=(review,)).standing is AdmissionStanding.ADMITTED


def test_withdrawing_the_review_suspends_the_dependent_link_only() -> None:
    """سحبُ مقدّمةٍ لازمةٍ يُعلِّق تابعَها وحدَه، ولا يُفترَض بديلٌ صامتٌ مكانَها."""

    first = _verbatim_candidate()
    second = next(
        dataclasses.replace(other, candidate_meaning=other.witness.text[5:15])
        for other in link_candidates()
        if other.boundary is BoundaryStanding.SOUND
        and other.material_key != first.material_key
    )
    both = (_review_for(first), _review_for(second))
    assert verify(first, reviews=both).standing is AdmissionStanding.ADMITTED
    assert verify(second, reviews=both).standing is AdmissionStanding.ADMITTED

    withdrawn = (_review_for(second),)
    assert verify(first, reviews=withdrawn).standing is AdmissionStanding.SUSPENDED
    assert verify(second, reviews=withdrawn).standing is AdmissionStanding.ADMITTED


def test_changing_the_witness_or_the_meaning_forces_a_new_verification() -> None:
    """تغيُّرُ الشاهد أو المعنى يُسقِط الاعتمادَ حتّى يُستأنَف التحقّقُ عليهما."""

    candidate = _verbatim_candidate()
    review = _review_for(candidate)
    assert verify(candidate, reviews=(review,)).standing is AdmissionStanding.ADMITTED

    moved = dataclasses.replace(
        candidate,
        witness=dataclasses.replace(
            candidate.witness,
            end_offset=candidate.witness.end_offset - 1,
            text=candidate.witness.text[:-1],
        ),
    )
    assert verify(moved, reviews=(review,)).standing is AdmissionStanding.SUSPENDED

    renamed = dataclasses.replace(
        candidate, candidate_meaning=candidate.witness.text[6:16]
    )
    assert verify(renamed, reviews=(review,)).standing is AdmissionStanding.SUSPENDED


def test_counter_evidence_is_recorded_and_does_not_flip_the_verdict_by_itself() -> None:
    """الشاهدُ المعارضُ يُسجَّل بجنسه ليُقوَّم، ولا يُعدي غيرَه ولا يُهمَل."""

    refusing = [
        reading for reading in dal_readings() if reading.carries_a_refusal_formula
    ]
    assert refusing
    for reading in refusing:
        assert SuspensionGenus.COUNTER_EVIDENCE in reading.suspension_genera
        assert reading.processing is DalProcessing.NO_ADMITTED_OUTPUT

    clean = _verbatim_candidate()
    clean_reading = verify(clean, reviews=(_review_for(clean),))
    assert clean_reading.counter_evidence_in_witness is False
    assert clean_reading.standing is AdmissionStanding.ADMITTED


def test_an_admitted_link_asserts_nothing_outside_language() -> None:
    """اعتمادُ ربطٍ معجميٍّ لا يُصدِّق واقعةً خارجيّة، ولا يبلغ وصلةَ الاستعمال."""

    candidate = _verbatim_candidate()
    review = _review_for(candidate)
    reading = verify(candidate, reviews=(review,))
    assert reading.standing is AdmissionStanding.ADMITTED
    assert "خارجَ اللغة" in reading.scope
    reach = dict((rung, ok) for rung, ok, _ in chain_reach(reviews=(review,)))
    assert reach[LinkChainRung.LAFZ] is False
    assert reach[LinkChainRung.USAGE] is False
    assert AN_ADMITTED_LEXICAL_LINK_ASSERTS_NO_EXTERNAL_FACT.startswith(
        "AN_ADMITTED_LEXICAL_LINK_ASSERTS_NO_EXTERNAL_FACT"
    )


def test_a_deposited_review_does_not_lift_the_file_nor_the_third_rung() -> None:
    """الترخيصُ محلّيّ: مراجعةٌ مودَعةٌ تفتح مرشَّحَها وحدَه، ولا ترفع الملفَّ.

    والمرشَّحُ المصنوعُ ليس من العشرين، فلا يُحسَب في بلوغ الوصلة الثالثة؛
    وأمّا مرشَّحو العشرين فيبقَون معلَّقين بشروطهم ولو أُودِعت مراجعتُهم.
    """

    made = _verbatim_candidate()
    review = _review_for(made)
    assert verify(made, reviews=(review,)).standing is AdmissionStanding.ADMITTED

    real_reviews = tuple(
        ReviewAttestation(
            material_key=candidate.material_key,
            candidate_meaning=candidate.candidate_meaning,
            witness_text=candidate.witness.text,
            reviewer="امتحانُ حارسٍ مصطنع",
            statement="إيداعٌ لامتحان البوّابة، لا شهادةً على معنًى عربيّ",
        )
        for candidate in link_candidates()
    )
    readings = [
        verify(candidate, reviews=real_reviews) for candidate in link_candidates()
    ]
    assert all(reading.standing is AdmissionStanding.SUSPENDED for reading in readings)
    reach = dict((rung, ok) for rung, ok, _ in chain_reach(reviews=real_reviews))
    assert reach[LinkChainRung.EXTRACTED_MEANING] is False


def test_a_partially_processed_dal_is_never_read_as_an_exhausted_one() -> None:
    """«عولجت محاورُه» حكمٌ على حقول هذا الملفّ، لا استيفاءٌ لمعاني المادّة."""

    readings = dal_readings()
    processed = [
        reading
        for reading in readings
        if reading.processing is DalProcessing.ALL_DECLARED_AXES_PROCESSED
    ]
    assert processed
    assert all(reading.admitted == 0 for reading in processed)
    assert all(reading.boundary is BoundaryStanding.SOUND for reading in processed)


def test_a_candidate_with_an_empty_meaning_is_refused_at_construction() -> None:
    """مرشَّحٌ بمعنًى فارغٍ يُرفَض عند الإنشاء، ولا يُحمَل على أقرب حالةٍ مقبولة."""

    with pytest.raises(MaqayisLinkCandidateError):
        dataclasses.replace(_sound_candidate(), candidate_meaning="   ")


def test_a_row_index_outside_the_bytes_is_refused_not_defaulted() -> None:
    """رتبةُ صفٍّ خارجَ البايتات رفضٌ مرفوع، لا قراءةٌ تُحمَل على أقرب صفّ."""

    with pytest.raises(MaqayisLinkCandidateError):
        verify(dataclasses.replace(_sound_candidate(), row_index=10**9))
