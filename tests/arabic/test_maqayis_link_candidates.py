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
    A_SYNTHETIC_ADMISSION_DOES_NOT_VALIDATE_THE_REAL_SUSPENSIONS,
    AN_ADMITTED_LEXICAL_LINK_ASSERTS_NO_EXTERNAL_FACT,
    MAQAYIS_LINK_CANDIDATE_NAMED_RESIDUALS,
    THE_ABAT_BOUNDARY_REVIEW,
    THE_CANDIDATE_SAMPLE_SIZE,
    THE_CONDITIONS_FOR_A_LAFZ_BRIDGE,
    THE_DISPLAY_EXCERPT_LIMIT,
    THE_ONE_MATERIAL_ACTUALLY_REVIEWED,
    AdmissionStanding,
    AttributionCheck,
    BoundaryAttestation,
    BoundaryStanding,
    CounterClaimDetermination,
    DalProcessing,
    HeadFormulaClue,
    InputUnitKind,
    LinkChainRung,
    MaqayisLinkCandidateError,
    RefusalStanding,
    ReviewAttestation,
    ReviewMethod,
    ReviewVerdict,
    SemanticSupportCheck,
    SuspensionGenus,
    TextualMatchCheck,
    _sample_rows,
    candidate_counts,
    chain_reach,
    dal_readings,
    input_unit_reading,
    link_candidates,
    provenance_shares,
    reconciliation_rows,
    report_rows,
    suspension_reason_census,
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
        sum(
            1
            for reading in readings
            if reading.boundary is BoundaryStanding.UNDETERMINED_BY_THE_DETECTOR
        )
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


def test_the_one_real_review_refuses_the_boundary_it_examined() -> None:
    """مراجعةٌ واقعيّةٌ لمادّةٍ واحدة: «أبت» تبتلع «أبث»، فالقرارُ يتبع نتيجتَها.

    والشهادةُ مودَعةٌ ناقصةَ المقابلة عمدًا لأنّ المقابلةَ لم تُسلِّم؛ فلا
    ترفع الحدَّ، ولا يُقرأ وسمُ الصفِّ بالمفتاح تبعيّةً لكلِّ مقطعٍ فيه.
    """

    assert THE_ABAT_BOUNDARY_REVIEW.row_index == 12
    assert THE_ABAT_BOUNDARY_REVIEW.end_examined is True
    assert THE_ABAT_BOUNDARY_REVIEW.internal_headers_examined is True
    assert THE_ABAT_BOUNDARY_REVIEW.collated_with_the_next_material is False
    assert THE_ABAT_BOUNDARY_REVIEW.is_complete is False
    assert "أبث" in THE_ONE_MATERIAL_ACTUALLY_REVIEWED

    # والابتلاعُ مقروءٌ من المتن نفسِه لا من دعوى المراجع.
    rows = dict(_sample_rows(None))
    body = rows[12]["body_text"]
    assert rows[12]["root_full"] == "أبت"
    assert "أبِثٌ" in body and "الكَبِث" in body

    # والقرارُ يتبع الإيداع: الحدُّ يبقى غيرَ مُحقَّق والنسبةُ غيرَ معيَّنة.
    examined = [
        verify(candidate, boundaries=(THE_ABAT_BOUNDARY_REVIEW,))
        for candidate in link_candidates()
        if candidate.row_index == 12
    ]
    assert examined
    for reading in examined:
        assert reading.boundary is BoundaryStanding.CANDIDATE_BY_THE_DETECTOR
        assert reading.attribution is AttributionCheck.NOT_DETERMINED
        assert reading.standing is AdmissionStanding.SUSPENDED


def test_the_reconciliation_table_carries_every_one_of_the_twenty() -> None:
    """جدولٌ صفّيٌّ لا قائمةٌ مختصرة: الدوالُّ الثلاثةُ بلا مرشَّحٍ صفوفٌ فيه."""

    rows = reconciliation_rows()
    assert len(rows) == THE_CANDIDATE_SAMPLE_SIZE == 20
    assert sum(int(row["مرشحات"]) for row in rows) == 19
    assert sum(1 for row in rows if row["مرشحات"] == 0) == 3
    assert sum(1 for row in rows if row["مرشحات"] == 2) == 2
    assert sum(1 for row in rows if row["مرشحات"] >= 1) == 17
    assert sum(int(row["معتمدون"]) for row in rows) == 0
    assert sum(int(row["معلقون"]) for row in rows) == 19
    assert sum(int(row["مرفوضون"]) for row in rows) == 0
    for row in rows:
        if row["مرشحات"] == 0:
            assert row["لماذا_لا_مرشح"]
        else:
            assert row["لماذا_لا_مرشح"] is None
            assert len(row["أسباب_التعليق"]) == row["مرشحات"]


def test_the_suspension_reasons_are_overlapping_not_exclusive_classes() -> None:
    """أسبابُ التعليق تُعَدّ منفردةً ومتقاطعةً؛ وجمعُها لا يساوي عددَ المعلَّقين."""

    census = suspension_reason_census()
    assert census["معلقون"] == 19
    singles = {key: value for key, value in census.items() if key.startswith("سبب: ")}
    joints = {key: value for key, value in census.items() if key.startswith("تقاطع: ")}
    assert singles and joints
    assert sum(singles.values()) > census["معلقون"]
    assert sum(joints.values()) == census["معلقون"]


def test_a_negation_form_is_not_read_as_a_determined_counter_claim() -> None:
    """رصدُ «ليس بأصل» تركيبٌ محفوظٌ لم يُعيَّن منفيُّه، فلا يُرفَع دليلًا مضادًّا."""

    empty = [reading for reading in dal_readings() if reading.candidates == 0]
    assert empty
    negating = [
        reading
        for reading in empty
        if reading.refusal is RefusalStanding.TARGET_UNDETERMINED
    ]
    assert negating
    for reading in negating:
        assert reading.refusal is not RefusalStanding.DETERMINED_COUNTER_CLAIM
        assert SuspensionGenus.COUNTER_EVIDENCE not in reading.suspension_genera
        assert SuspensionGenus.ABSENT_EVIDENCE in reading.suspension_genera


def test_a_deposited_determination_is_what_raises_a_negation_to_a_counter_claim() -> (
    None
):
    """التعارضُ يُحقَّق بتعيينٍ مودَعٍ يُسمّي المنفيَّ والدعوى وسببَ الانطباق."""

    bearing = next(
        reading
        for reading in dal_readings()
        if reading.refusal is RefusalStanding.TARGET_UNDETERMINED
    )
    determination = CounterClaimDetermination(
        material_key=bearing.material_key,
        negating_text="ليس",
        what_is_denied="استقلالُ المادّة أصلًا يُقاس عليه",
        claim_it_opposes="أنّ هذه المادّة تُخرِج أصلًا معجميًّا واحدًا",
        why_it_applies="تعيينٌ مصطنعٌ لامتحان الحارس، لا قراءةُ سياقٍ عربيّة",
    )
    after = next(
        reading
        for reading in dal_readings(determinations=(determination,))
        if reading.material_key == bearing.material_key
    )
    assert after.refusal is RefusalStanding.DETERMINED_COUNTER_CLAIM
    assert SuspensionGenus.COUNTER_EVIDENCE in after.suspension_genera


def test_the_four_checks_separate_and_none_is_read_as_another() -> None:
    """المطابقةُ النصّيّةُ والنسبةُ والإسنادُ فحوصٌ مفصولة، ولا يُرفَع أدناها."""

    verifications = [verify(candidate) for candidate in link_candidates()]
    assert all(reading.source_integrity for reading in verifications)
    assert all(reading.segment_in_row for reading in verifications)
    assert all(
        reading.head_formula_clue is not HeadFormulaClue.DOES_NOT_NAME_THEM
        for reading in verifications
    )
    # النسبةُ غيرُ معيَّنةٍ في العشرين كلِّهم: لا شهادةَ حدٍّ مودَعةً لأيّ صفّ.
    assert all(
        reading.attribution is AttributionCheck.NOT_DETERMINED
        for reading in verifications
    )
    # والإسنادُ الدلاليُّ غيرُ مُثبَتٍ، ولو وقعت المطابقةُ النصّيّةُ بحروفها.
    assert all(
        reading.semantic_support
        is SemanticSupportCheck.NOT_ESTABLISHED_WITHOUT_A_REVIEW
        for reading in verifications
    )
    matches = {reading.textual_match for reading in verifications}
    assert TextualMatchCheck.MATCHES_VERBATIM in matches
    assert TextualMatchCheck.NO_TEXTUAL_MATCH in matches


def test_a_verbatim_textual_match_does_not_establish_semantic_support() -> None:
    """وقوعُ الصياغة بحروفها لا يرفعها إسنادًا، ولا غيابُها ينفيه."""

    verbatim = [
        reading
        for reading in (verify(candidate) for candidate in link_candidates())
        if reading.textual_match is TextualMatchCheck.MATCHES_VERBATIM
    ]
    assert verbatim
    for reading in verbatim:
        assert (
            reading.semantic_support
            is SemanticSupportCheck.NOT_ESTABLISHED_WITHOUT_A_REVIEW
        )
        assert reading.standing is AdmissionStanding.SUSPENDED
        assert not any("مطابقة" in condition for condition in reading.unmet_conditions)


def test_an_absent_textual_match_is_never_read_as_an_absent_support() -> None:
    """غيابُ المطابقة النصّيّة ليس في أسباب التعليق أصلًا، فلا يُقرأ نفيًا."""

    unmatched = [
        reading
        for reading in (verify(candidate) for candidate in link_candidates())
        if reading.textual_match is TextualMatchCheck.NO_TEXTUAL_MATCH
    ]
    assert unmatched
    for reading in unmatched:
        assert all(
            "الإسنادُ الدلاليّ" in condition or "صحّةُ النسبة" in condition
            for condition in reading.unmet_conditions
        )


def test_the_governing_text_absence_suspends_only_the_signification_kind() -> None:
    """غيابُ النصّ الحاكم يُعلِّق التصنيفَ وحدَه، ويبقى العملُ المعجميُّ ماضيًا."""

    assert governing_seal_reading().standing is SealStanding.ABSENT_FROM_THIS_TREE
    candidates = link_candidates()
    assert candidates
    assert all(candidate.signification_kind is None for candidate in candidates)


def test_the_chain_stops_at_the_second_rung_because_no_boundary_is_verified() -> None:
    """الوصلةُ الثانيةُ لا تُبلَغ بالكاشف: لا شهادةَ حدٍّ مودَعةً لأيّ صفٍّ بعدُ."""

    reach = dict((rung, (ok, why)) for rung, ok, why in chain_reach())
    assert reach[LinkChainRung.MATERIAL_KEY][0] is True
    assert reach[LinkChainRung.VERIFIED_MATERIAL][0] is False
    assert (
        f"0 من {THE_CANDIDATE_SAMPLE_SIZE}" in reach[LinkChainRung.VERIFIED_MATERIAL][1]
    )
    assert reach[LinkChainRung.EXTRACTED_MEANING][0] is False
    assert reach[LinkChainRung.LAFZ][0] is False
    assert reach[LinkChainRung.USAGE][0] is False
    assert "خارجَ النطاق" in reach[LinkChainRung.USAGE][1]


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
        if candidate.boundary is BoundaryStanding.CANDIDATE_BY_THE_DETECTOR:
            return candidate
    raise AssertionError("لا صفَّ محقَّقَ الحدّ في العيّنة، فلا يُمتحَن الحارس.")


def _verbatim_candidate():
    """مرشَّحٌ مصنوعٌ معناه مقتطعٌ من شاهده بحروفه؛ مطابقةٌ نصّيّةٌ لا إسناد."""

    candidate = _sound_candidate()
    witness = candidate.witness.text
    return dataclasses.replace(candidate, candidate_meaning=witness[5:15])


_SYNTHETIC_METHOD = ReviewMethod(
    performed_by="امتحانُ حارسٍ مصطنع",
    is_human=False,
    is_independent=False,
    procedure="إيداعٌ لامتحان مسار البوّابة وحدَه، لا نظرَ في نصٍّ عربيّ",
    materials_consulted=("لا شيء: مرشَّحٌ مصنوعٌ لا مادّةَ له",),
)


def _review_for(
    candidate, verdict: ReviewVerdict = ReviewVerdict.SUPPORTS_THE_MEANING
) -> ReviewAttestation:
    return ReviewAttestation(
        material_key=candidate.material_key,
        candidate_meaning=candidate.candidate_meaning,
        witness_text=candidate.witness.text,
        reviewer="امتحانُ حارسٍ مصطنع",
        statement="مودَعٌ لامتحان البوّابة وحدَها، لا شهادةً على معنًى عربيّ",
        method=_SYNTHETIC_METHOD,
        verdict=verdict,
        mode_of_support="وجهٌ مصطنعٌ لامتحان الحارس، لا إسنادَ معنًى",
    )


def _boundary_for(candidate, *, complete: bool = True) -> BoundaryAttestation:
    return BoundaryAttestation(
        material_key=candidate.material_key,
        row_index=candidate.row_index,
        end_examined=complete,
        internal_headers_examined=True,
        collated_with_the_next_material=True,
        reviewer="امتحانُ حارسٍ مصطنع",
        statement="شهادةُ حدٍّ مصطنعةٌ لامتحان المسار، لا تحقيقٌ لمادّةٍ عربيّة",
    )


def _opened(candidate):
    """أودِع ما يفتح المسار: شهادةُ حدٍّ ومراجعةٌ مُسنِدة؛ ولا ثالثَ يُفترَض."""

    return {
        "reviews": (_review_for(candidate),),
        "boundaries": (_boundary_for(candidate),),
    }


def test_the_guard_admits_only_when_every_declared_condition_meets() -> None:
    """مسارُ القبول يعمل على المصطنع؛ ولا يُقرأ تصحيحًا لقرارات العيّنة الواقعيّة."""

    candidate = _verbatim_candidate()
    reading = verify(candidate, **_opened(candidate))
    assert reading.attribution is AttributionCheck.VERIFIED_BY_A_DEPOSITED_WITNESS
    assert reading.semantic_support is (
        SemanticSupportCheck.ESTABLISHED_BY_A_DEPOSITED_REVIEW
    )
    assert reading.standing is AdmissionStanding.ADMITTED
    assert reading.unmet_conditions == ()
    assert A_SYNTHETIC_ADMISSION_DOES_NOT_VALIDATE_THE_REAL_SUSPENSIONS.startswith(
        "A_SYNTHETIC_ADMISSION_DOES_NOT_VALIDATE_THE_REAL_SUSPENSIONS"
    )


def test_an_incomplete_boundary_witness_does_not_verify_the_attribution() -> None:
    """شهادةُ حدٍّ لم يُفحَص فيها المنتهى لا تُحقِّق الحدّ، فتبقى النسبةُ معلَّقة."""

    candidate = _verbatim_candidate()
    partial = _boundary_for(candidate, complete=False)
    assert partial.is_complete is False
    reading = verify(
        candidate, reviews=(_review_for(candidate),), boundaries=(partial,)
    )
    assert reading.boundary is BoundaryStanding.CANDIDATE_BY_THE_DETECTOR
    assert reading.attribution is AttributionCheck.NOT_DETERMINED
    assert reading.standing is AdmissionStanding.SUSPENDED


def test_a_deposited_review_may_deny_the_meaning_and_that_is_recorded() -> None:
    """المراجعةُ النافيةُ تُحفَظ بجهتها، فتُعلَّق بدليلٍ مضادٍّ لا بتعذُّر أداة."""

    candidate = _verbatim_candidate()
    reading = verify(
        candidate,
        reviews=(_review_for(candidate, ReviewVerdict.DENIES_THE_MEANING),),
        boundaries=(_boundary_for(candidate),),
    )
    assert reading.semantic_support is SemanticSupportCheck.DENIED_BY_A_DEPOSITED_REVIEW
    assert reading.standing is AdmissionStanding.SUSPENDED
    assert reading.suspension_genus is SuspensionGenus.COUNTER_EVIDENCE


def test_a_support_without_any_textual_match_is_admitted_all_the_same() -> None:
    """الإسنادُ لا يُشترَط له تطابقٌ حرفيّ: صياغةٌ مختلفةٌ تُعتمَد بمراجعتها."""

    base = _sound_candidate()
    candidate = dataclasses.replace(
        base, candidate_meaning="صياغةٌ لا تقع في الشاهد نصًّا البتّة"
    )
    reading = verify(candidate, **_opened(candidate))
    assert reading.textual_match is TextualMatchCheck.NO_TEXTUAL_MATCH
    assert reading.standing is AdmissionStanding.ADMITTED


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
    reading = verify(transplanted, **_opened(transplanted))
    assert reading.segment_in_row is False
    assert reading.attribution is AttributionCheck.REFUTED_BY_THE_PROBE
    assert reading.standing is AdmissionStanding.SUSPENDED
    assert any("وقوعُ المقطع" in condition for condition in reading.unmet_conditions)


def test_a_segment_in_a_row_is_not_a_segment_in_a_material() -> None:
    """وقوعُ المقطع في الصفّ ووسمُ الصفِّ بالمفتاح لا يُثبِتان تبعيّتَه للمادّة."""

    candidate = _verbatim_candidate()
    reading = verify(candidate, reviews=(_review_for(candidate),))
    assert reading.segment_in_row is True
    assert reading.head_formula_clue is HeadFormulaClue.NAMES_EVERY_RADICAL
    assert reading.attribution is AttributionCheck.NOT_DETERMINED
    assert reading.standing is AdmissionStanding.SUSPENDED
    assert any("صحّةُ النسبة" in condition for condition in reading.unmet_conditions)


def test_an_undetermined_boundary_suspends_what_depends_on_it() -> None:
    """حدٌّ لم يُعيِّنه الكاشفُ يُعلِّق نتائجَه التابعة ولو استوفى غيرُها شرطَه."""

    undetermined = next(
        candidate
        for candidate in link_candidates()
        if candidate.boundary is BoundaryStanding.UNDETERMINED_BY_THE_DETECTOR
    )
    forged = dataclasses.replace(
        undetermined, candidate_meaning=undetermined.witness.text[5:15]
    )
    reading = verify(forged, reviews=(_review_for(forged),))
    assert reading.textual_match is TextualMatchCheck.MATCHES_VERBATIM
    assert reading.attribution is AttributionCheck.NOT_DETERMINED
    assert reading.standing is AdmissionStanding.SUSPENDED
    assert reading.suspension_genus is SuspensionGenus.TOOL_UNAVAILABLE


def test_a_reviewed_material_does_not_open_its_neighbours() -> None:
    """مراجعةُ مادّةٍ إذنٌ فيها وحدَها، فلا تفتح جارتَها ولا معنًى آخرَ فيها."""

    candidate = _verbatim_candidate()
    opened = _opened(candidate)
    neighbour = next(
        other
        for other in link_candidates()
        if other.boundary is BoundaryStanding.CANDIDATE_BY_THE_DETECTOR
        and other.material_key != candidate.material_key
    )
    forged = dataclasses.replace(
        neighbour, candidate_meaning=neighbour.witness.text[5:15]
    )
    assert verify(forged, **opened).standing is AdmissionStanding.SUSPENDED
    assert verify(candidate, **opened).standing is AdmissionStanding.ADMITTED


def test_withdrawing_the_review_suspends_the_dependent_link_only() -> None:
    """سحبُ مقدّمةٍ لازمةٍ يُعلِّق تابعَها وحدَه، ولا يُفترَض بديلٌ صامتٌ مكانَها."""

    first = _verbatim_candidate()
    second = next(
        dataclasses.replace(other, candidate_meaning=other.witness.text[5:15])
        for other in link_candidates()
        if other.boundary is BoundaryStanding.CANDIDATE_BY_THE_DETECTOR
        and other.material_key != first.material_key
    )
    both = (_review_for(first), _review_for(second))
    edges = (_boundary_for(first), _boundary_for(second))
    assert verify(first, reviews=both, boundaries=edges).standing is (
        AdmissionStanding.ADMITTED
    )
    assert verify(second, reviews=both, boundaries=edges).standing is (
        AdmissionStanding.ADMITTED
    )

    withdrawn = (_review_for(second),)
    assert verify(first, reviews=withdrawn, boundaries=edges).standing is (
        AdmissionStanding.SUSPENDED
    )
    assert verify(second, reviews=withdrawn, boundaries=edges).standing is (
        AdmissionStanding.ADMITTED
    )


def test_changing_the_witness_or_the_meaning_forces_a_new_verification() -> None:
    """تغيُّرُ الشاهد أو المعنى يُسقِط الاعتمادَ حتّى يُستأنَف التحقّقُ عليهما."""

    candidate = _verbatim_candidate()
    opened = _opened(candidate)
    assert verify(candidate, **opened).standing is AdmissionStanding.ADMITTED

    moved = dataclasses.replace(
        candidate,
        witness=dataclasses.replace(
            candidate.witness,
            end_offset=candidate.witness.end_offset - 1,
            text=candidate.witness.text[:-1],
        ),
    )
    assert verify(moved, **opened).standing is AdmissionStanding.SUSPENDED

    renamed = dataclasses.replace(
        candidate, candidate_meaning=candidate.witness.text[6:16]
    )
    assert verify(renamed, **opened).standing is AdmissionStanding.SUSPENDED


def test_a_negation_form_is_recorded_without_infecting_its_neighbours() -> None:
    """تركيبُ النفي يُسجَّل بمنزلته ليُحقَّق، ولا يُعدي غيرَه ولا يُهمَل."""

    refusing = [
        reading
        for reading in dal_readings()
        if reading.refusal is not RefusalStanding.NO_NEGATION_FORM
    ]
    assert refusing
    for reading in refusing:
        assert reading.processing is DalProcessing.NO_ADMITTED_OUTPUT

    clean = _verbatim_candidate()
    clean_reading = verify(clean, **_opened(clean))
    assert clean_reading.refusal is RefusalStanding.NO_NEGATION_FORM
    assert clean_reading.standing is AdmissionStanding.ADMITTED


def test_an_admitted_link_asserts_nothing_outside_language() -> None:
    """اعتمادُ ربطٍ معجميٍّ لا يُصدِّق واقعةً خارجيّة، ولا يبلغ وصلةَ الاستعمال."""

    candidate = _verbatim_candidate()
    opened = _opened(candidate)
    reading = verify(candidate, **opened)
    assert reading.standing is AdmissionStanding.ADMITTED
    assert "خارجَ اللغة" in reading.scope
    reasons = {rung: why for rung, _, why in chain_reach(**opened)}
    reach = {rung: ok for rung, ok, _ in chain_reach(**opened)}
    assert reach[LinkChainRung.LAFZ] is False
    assert reach[LinkChainRung.USAGE] is False
    # حدُّ نطاقٍ محلّيٌّ لا امتناعٌ بالنظام؛ وشروطُ الجسر مُسمّاةٌ لا مُبهَمة.
    for rung in (LinkChainRung.LAFZ, LinkChainRung.USAGE):
        assert "خارجَ النطاق" in reasons[rung]
        assert "لا امتناعٌ في المشروع" in reasons[rung]
    assert len(THE_CONDITIONS_FOR_A_LAFZ_BRIDGE) == 5
    assert AN_ADMITTED_LEXICAL_LINK_ASSERTS_NO_EXTERNAL_FACT.startswith(
        "AN_ADMITTED_LEXICAL_LINK_ASSERTS_NO_EXTERNAL_FACT"
    )


def test_a_deposited_review_does_not_lift_the_file_nor_the_third_rung() -> None:
    """الترخيصُ محلّيّ: مراجعةٌ مودَعةٌ تفتح مرشَّحَها وحدَه، ولا ترفع الملفَّ.

    والمرشَّحُ المصنوعُ ليس من العشرين، فلا يُحسَب في بلوغ الوصلة الثالثة؛
    وأمّا مرشَّحو العشرين فيبقَون معلَّقين بشروطهم ولو أُودِعت مراجعتُهم.
    """

    made = _verbatim_candidate()
    assert verify(made, **_opened(made)).standing is AdmissionStanding.ADMITTED

    real_reviews = tuple(
        ReviewAttestation(
            material_key=candidate.material_key,
            candidate_meaning=candidate.candidate_meaning,
            witness_text=candidate.witness.text,
            reviewer="امتحانُ حارسٍ مصطنع",
            statement="إيداعٌ لامتحان البوّابة، لا شهادةً على معنًى عربيّ",
            method=_SYNTHETIC_METHOD,
            mode_of_support="وجهٌ مصطنعٌ لامتحان الحارس",
        )
        for candidate in link_candidates()
    )
    # ولا شهادةَ حدٍّ تُودَع لأيٍّ منهم، فالنسبةُ تبقى غيرَ معيَّنة.
    readings = [
        verify(candidate, reviews=real_reviews) for candidate in link_candidates()
    ]
    assert all(reading.standing is AdmissionStanding.SUSPENDED for reading in readings)
    reach = dict((rung, ok) for rung, ok, _ in chain_reach(reviews=real_reviews))
    assert reach[LinkChainRung.EXTRACTED_MEANING] is False


def test_a_partially_processed_dal_is_never_read_as_an_exhausted_one() -> None:
    """«عولجت محاورُه» حكمٌ على حقول هذا الملفّ، لا استيفاءٌ لمعاني المادّة."""

    readings = dal_readings()
    assert not [
        reading
        for reading in readings
        if reading.processing is DalProcessing.ALL_DECLARED_AXES_PROCESSED
    ]
    partial = [
        reading
        for reading in readings
        if reading.processing is DalProcessing.PARTIALLY_PROCESSED
    ]
    assert partial
    assert all(reading.admitted == 0 for reading in partial)
    # وعلّةُ الجزئيّةِ مُسمّاةٌ: لا حدَّ مُحقَّقًا بشهادةٍ في العشرين كلِّهم.
    assert all(
        reading.boundary is not BoundaryStanding.VERIFIED_BY_A_DEPOSITED_WITNESS
        for reading in readings
    )


def test_a_candidate_with_an_empty_meaning_is_refused_at_construction() -> None:
    """مرشَّحٌ بمعنًى فارغٍ يُرفَض عند الإنشاء، ولا يُحمَل على أقرب حالةٍ مقبولة."""

    with pytest.raises(MaqayisLinkCandidateError):
        dataclasses.replace(_sound_candidate(), candidate_meaning="   ")


def test_a_row_index_outside_the_bytes_is_refused_not_defaulted() -> None:
    """رتبةُ صفٍّ خارجَ البايتات رفضٌ مرفوع، لا قراءةٌ تُحمَل على أقرب صفّ."""

    with pytest.raises(MaqayisLinkCandidateError):
        verify(dataclasses.replace(_sound_candidate(), row_index=10**9))
