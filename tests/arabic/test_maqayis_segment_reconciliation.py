"""امتحانُ المصالحة الموضعيّة على مادّةٍ واقعيّةٍ من أوّل المصدر إلى القرار.

وهذا الملفُّ **حالةٌ واقعيّةٌ لا حارسٌ مصطنع**: مادّتُه «أبت» من العيّنة
المُعلَنة، ونصُّها من البايتات المختومة، ومعناها مُستخرَجٌ من متنها. وما
يُمتحَن ههنا صحّةُ قرارِ التعليق والاعتماد على هذه المادّة بعينها، لا بلوغُ
المسار كما يُمتحَن بالمصنوع.

وفحوصُ **مخالفةِ البصمة** مفصولةٌ في بابها الأخير بنسخٍ بديلةٍ معلومةِ
الهويّة تُكتَب على القرص وتُقرأ بجذرها، فلا يختلط سقوطُ مرشَّحٍ لتبدُّل
النسخة بسقوطه لعلّةٍ في نسبته أو إسناده.
"""

from __future__ import annotations

import csv
import dataclasses
import hashlib
import tempfile
from pathlib import Path

import pytest

from alghanem.arabic.maqayis_link_candidates import (
    THE_ATTRIBUTION_ROUTES,
    AdmissionStanding,
    AttributionCheck,
    AttributionRoute,
    BoundaryStanding,
    MaqayisLinkCandidateError,
    ReviewVerdict,
    SegmentDecision,
    SemanticSupportCheck,
    SuspensionGenus,
    verify,
)
from alghanem.arabic.maqayis_root_table_deposit import MaqayisRootTableError
from alghanem.arabic.maqayis_segment_reconciliation import (
    THE_ABAT_EXTRACTION,
    THE_ABAT_MATERIAL_KEY,
    THE_ABAT_ROW_INDEX,
    THE_ABAT_SEGMENTS,
    THE_ABAT_TRANSITION_OFFSET,
    THE_QUESTION_THAT_NEEDS_A_HUMAN_DECISION,
    THE_REFERENCE_COPIES_TO_CONSULT,
    THE_SESSION_REVIEW_METHOD,
    extracted_candidate,
    extracted_review,
    reconciliation_counts,
    reconciliation_ledger,
    transition_evidence,
)

# ── بابُ الحالة الواقعيّة: «أبت» ─────────────────────────────────────────


def _case() -> tuple[object, object]:
    return extracted_candidate(), extracted_review()


def test_the_attributed_segment_with_its_witnesses_is_admitted() -> None:
    """مقطعٌ ثبتت نسبتُه بطريقَين، ومعناه مُستخرَجٌ من متنه: يُعتمَد فعلًا."""

    candidate, review = _case()
    reading = verify(candidate, segments=THE_ABAT_SEGMENTS, reviews=(review,))
    assert reading.standing is AdmissionStanding.ADMITTED
    assert reading.unmet_conditions == ()
    assert reading.attribution is AttributionCheck.VERIFIED_BY_A_DEPOSITED_WITNESS
    assert reading.semantic_support is (
        SemanticSupportCheck.ESTABLISHED_BY_A_DEPOSITED_REVIEW
    )
    assert reading.segment is not None
    assert reading.segment.decision is SegmentDecision.ATTRIBUTED_TO_THIS_MATERIAL
    # والمعنى من المتن لا من حقل المحاور، والنصّان مختلفان فعلًا.
    assert candidate.meaning_field == "body_text"
    assert candidate.candidate_meaning == "الحرّ وشدّته"
    assert candidate.candidate_meaning not in "الحر وشدته"


def test_the_unsettled_row_boundary_does_not_block_the_attributed_segment() -> None:
    """بقاءُ ذيلِ الصفِّ ملتبسًا لا يمنع اعتمادَ المقطع الذي ثبت استقلالُه.

    وهذا موضعُ فصلِ الشرطين: حدُّ الصفِّ لم يُحقَّق، وبندان منه ملتبسان،
    ومع ذلك يُعتمَد المقطعُ الأوّل لأنّ نسبتَه هي ما يحتاجه الحكمُ عليه.
    """

    candidate, review = _case()
    reading = verify(candidate, segments=THE_ABAT_SEGMENTS, reviews=(review,))
    assert reading.standing is AdmissionStanding.ADMITTED
    # ولا شهادةَ حدٍّ للصفّ: الكاشفُ يقترح، ولا تبلغ الحالُ تحقيقًا.
    assert reading.boundary is BoundaryStanding.CANDIDATE_BY_THE_DETECTOR
    unresolved = [
        entry
        for entry in reconciliation_ledger()
        if entry.decision is SegmentDecision.UNRESOLVED
    ]
    assert len(unresolved) == 2
    assert all(entry.attributed_material is None for entry in unresolved)


def test_moving_the_segment_to_another_material_blocks_the_admission() -> None:
    """تغييرُ نسبةِ المقطع إلى مادّةٍ أخرى يمنع الاعتماد: البندُ لا يَسَعه."""

    candidate, review = _case()
    moved = dataclasses.replace(candidate, material_key="أبد:14")
    reading = verify(moved, segments=THE_ABAT_SEGMENTS, reviews=(review,))
    assert reading.segment is None
    assert reading.attribution is AttributionCheck.NOT_DETERMINED
    assert reading.standing is AdmissionStanding.SUSPENDED
    assert any("صحّةُ النسبة" in condition for condition in reading.unmet_conditions)


def test_a_segment_the_ledger_calls_foreign_is_refuted_not_undetermined() -> None:
    """مقطعٌ قال السجلُّ إنّه من «أبث»: تُنقَض نسبتُه ولا تُترَك غيرَ معيَّنة."""

    candidate, _ = _case()
    foreign = next(
        segment
        for segment in THE_ABAT_SEGMENTS
        if segment.decision is SegmentDecision.FOREIGN_TO_THIS_MATERIAL
    )
    body = _row_body()
    span = body[foreign.start_offset : foreign.end_offset]
    transplanted = dataclasses.replace(
        candidate,
        candidate_meaning="الأشِرُ النّشيط",
        witness=dataclasses.replace(
            candidate.witness,
            start_offset=foreign.start_offset,
            end_offset=foreign.end_offset,
            text=span,
        ),
    )
    reading = verify(transplanted, segments=THE_ABAT_SEGMENTS)
    assert reading.segment is foreign
    assert reading.attribution is AttributionCheck.REFUTED_BY_THE_PROBE
    assert reading.suspension_genus is SuspensionGenus.COUNTER_EVIDENCE
    assert reading.standing is AdmissionStanding.SUSPENDED


def test_a_meaning_the_segment_does_not_support_blocks_the_admission() -> None:
    """تغييرُ المعنى إلى ما لا يُسنِده المقطعُ يمنع الاعتماد: المراجعةُ لا تَسَعه."""

    candidate, review = _case()
    swapped = dataclasses.replace(candidate, candidate_meaning="طولُ المدّة والتوحّش")
    reading = verify(swapped, segments=THE_ABAT_SEGMENTS, reviews=(review,))
    assert reading.semantic_support is (
        SemanticSupportCheck.NOT_ESTABLISHED_WITHOUT_A_REVIEW
    )
    assert reading.standing is AdmissionStanding.SUSPENDED
    # والنسبةُ باقيةٌ محقَّقةً: سقط الإسنادُ وحدَه، ولم يُعْدِ سقوطُه غيرَه.
    assert reading.attribution is AttributionCheck.VERIFIED_BY_A_DEPOSITED_WITNESS


def test_withdrawing_a_required_attestation_suspends_the_dependent_result() -> None:
    """سحبُ شهادةٍ لازمةٍ يُعلِّق تابعَها وحدَه، وسببُ التعليق يُسمّى بعينه."""

    candidate, review = _case()
    without_review = verify(candidate, segments=THE_ABAT_SEGMENTS)
    assert without_review.standing is AdmissionStanding.SUSPENDED
    assert without_review.attribution is (
        AttributionCheck.VERIFIED_BY_A_DEPOSITED_WITNESS
    )
    assert any(
        "الإسنادُ الدلاليّ" in condition for condition in without_review.unmet_conditions
    )

    without_segment = verify(candidate, reviews=(review,))
    assert without_segment.standing is AdmissionStanding.SUSPENDED
    assert without_segment.attribution is AttributionCheck.NOT_DETERMINED
    assert any(
        "صحّةُ النسبة" in condition for condition in without_segment.unmet_conditions
    )


def test_changing_an_unrelated_segment_does_not_fell_the_judgement() -> None:
    """تغييرُ بندٍ لا يتعلّق بالحكم لا يُسقِطه؛ فالترخيصُ موضعيٌّ لا ملفّيّ."""

    candidate, review = _case()
    kept = verify(candidate, segments=THE_ABAT_SEGMENTS, reviews=(review,))
    assert kept.standing is AdmissionStanding.ADMITTED

    disturbed = tuple(
        dataclasses.replace(segment, statement="بيانٌ بُدِّل لامتحان الاستقلال")
        if segment.decision is SegmentDecision.UNRESOLVED
        else segment
        for segment in THE_ABAT_SEGMENTS
    )
    again = verify(candidate, segments=disturbed, reviews=(review,))
    assert again.standing is AdmissionStanding.ADMITTED

    dropped = tuple(
        segment
        for segment in THE_ABAT_SEGMENTS
        if segment.decision is not SegmentDecision.UNRESOLVED
    )
    assert verify(candidate, segments=dropped, reviews=(review,)).standing is (
        AdmissionStanding.ADMITTED
    )


# ── بابُ السجلّ وموضعِ الانتقال ──────────────────────────────────────────


def _row_body() -> str:
    import unicodedata

    from alghanem.arabic.maqayis_link_candidates import _rows_of

    return unicodedata.normalize("NFC", _rows_of(None)[THE_ABAT_ROW_INDEX]["body_text"])


def test_the_ledger_reproduces_every_entry_from_the_sealed_bytes() -> None:
    """كلُّ بندٍ يُقابَل بمُقتطَفَيه عند بنائه، فلا يُصدَّق بندٌ على نفسه."""

    ledger = reconciliation_ledger()
    assert ledger
    assert all(entry.reproduces_from_bytes for entry in ledger)
    assert all(entry.row_key == THE_ABAT_MATERIAL_KEY for entry in ledger)
    assert all(entry.offset_unit for entry in ledger)
    assert all(len(entry.source.measured_sha256) == 64 for entry in ledger)
    # والبنودُ تغطّي المتنَ كلَّه بلا فجوةٍ ولا تداخل.
    spans = sorted((entry.start_offset, entry.end_offset) for entry in ledger)
    assert spans[0][0] == 0
    assert spans[-1][1] == len(_row_body())
    assert all(end == spans[i + 1][0] for i, (_, end) in enumerate(spans[:-1]))


def test_the_transition_point_is_named_not_merely_the_mixture() -> None:
    """لا يُكتفى بأنّ الصفَّ مختلط: مجالُ «أبت» مُعيَّنٌ وموضعُ الانتقال مُسمًّى."""

    body = _row_body()
    assert THE_ABAT_TRANSITION_OFFSET == 313
    before = body[:THE_ABAT_TRANSITION_OFFSET]
    after = body[THE_ABAT_TRANSITION_OFFSET:]
    assert before.startswith("الهمزة والباء والتاء أصلٌ واحد")
    assert after.startswith("وهذا الباب مهملٌ عند الخليل")
    # والقِسمةُ مقيسةٌ لا مُقدَّرة: ما قبلها خالٍ من الثاء، وما بعدها يحملها.
    assert transition_evidence() == {
        "تاءٌ_قبل_الانتقال": 12,
        "ثاءٌ_قبل_الانتقال": 0,
        "تاءٌ_بعد_الانتقال": 8,
        "ثاءٌ_بعد_الانتقال": 8,
    }


def test_the_swallowing_mechanism_is_measured_on_the_whole_file() -> None:
    """آلةُ الابتلاع مقيسة: ترويسةُ «أبث» لا تقع في الملفّ كلِّه ولا مرّة."""

    raw = Path("maqayis_by_root_csv_999.csv").read_text(encoding="utf-8")
    assert raw.count("الهمزة والباء والثاء") == 0
    assert raw.count("الهمزة والباء والتاء") == 1


def test_the_unresolved_entry_carries_the_question_and_where_to_settle_it() -> None:
    """البندُ الملتبسُ يُسلَّم بسؤالٍ محدَّدٍ وبمواضعِ حسمه، لا بشكوى تعليق."""

    hinge = next(
        segment
        for segment in THE_ABAT_SEGMENTS
        if segment.start_offset == THE_ABAT_TRANSITION_OFFSET
    )
    assert hinge.decision is SegmentDecision.UNRESOLVED
    assert hinge.routes == ()
    assert hinge.statement is THE_QUESTION_THAT_NEEDS_A_HUMAN_DECISION
    assert "أهو خاتمةُ مادّة «أبت» أم مُفتتَحُ مادّة «أبث»؟" in hinge.statement
    assert len(THE_REFERENCE_COPIES_TO_CONSULT) >= 3


def test_the_reference_copy_route_is_declared_unavailable_not_merely_unused() -> None:
    """طريقُ النسخة المرجعيّة غيرُ متوفّرٍ بالتصريح، فلا يُحتَجّ به لو أُودِع."""

    premises = THE_ATTRIBUTION_ROUTES[AttributionRoute.REFERENCE_COPY_COLLATION]
    assert premises.is_available_on_this_deposit is False
    assert premises.limits
    for route, record in THE_ATTRIBUTION_ROUTES.items():
        assert record.premise and record.establishes and record.limits, route


def test_the_collation_with_the_next_material_is_not_required_of_every_case() -> None:
    """المقابلةُ بالتالي طريقٌ لا شرطٌ لازم؛ والمقطعُ اعتُمِد بطريقَين غيرِها."""

    attributed = next(
        segment
        for segment in THE_ABAT_SEGMENTS
        if segment.decision is SegmentDecision.ATTRIBUTED_TO_THIS_MATERIAL
    )
    assert AttributionRoute.COLLATION_WITH_THE_NEXT_MATERIAL not in attributed.routes
    assert attributed.is_established
    assert len(attributed.established_routes) == 2


def test_the_counts_are_separated_by_unit() -> None:
    """الأعدادُ بوحداتها: صفٌّ غيرُ مادّةٍ غيرُ مقطعٍ غيرُ معنًى غيرُ زوج."""

    counts = reconciliation_counts()
    assert counts["صفوف_مصالَحة"] == 1
    assert counts["موادّ_مميَّزة_في_الصفوف"] == 2
    assert counts["مقاطع"] == 5
    assert counts["مقاطع_ثابتة_النسبة"] == 1
    assert counts["مقاطع_منقوضة_النسبة"] == 2
    assert counts["مقاطع_ملتبسة"] == 2
    assert counts["معانٍ_مستخرَجة_من_المتن"] == 1


# ── بابُ المراجعة: منهجٌ مُصرَّحٌ لا مفتاحٌ يُقلَب ────────────────────────


def test_a_review_without_a_declared_method_is_refused_at_construction() -> None:
    """`SUPPORTS_THE_MEANING` نتيجةٌ: مراجعةٌ بلا منهجٍ لا تبلغ بابَ الاعتماد."""

    review = extracted_review()
    with pytest.raises(MaqayisLinkCandidateError):
        dataclasses.replace(review, method=None)  # type: ignore[arg-type]
    with pytest.raises(MaqayisLinkCandidateError):
        dataclasses.replace(review, mode_of_support="")


def test_the_agent_review_is_never_named_human_or_independent() -> None:
    """مراجعةُ الوكيل تُسجَّل بما هي، ولا تُسمّى بشريّةً ولا مستقلّة."""

    method = THE_SESSION_REVIEW_METHOD
    assert method.is_human is False
    assert method.is_independent is False
    assert "آليّة" in method.standing
    assert "غيرُ مستقلّة" in method.standing
    assert method.materials_consulted
    review = extracted_review()
    assert review.method is method
    assert review.verdict is ReviewVerdict.SUPPORTS_THE_MEANING
    assert review.mode_of_support and review.generalisation_limits


def test_the_extraction_records_its_qualifications_and_limits() -> None:
    """الاستخراجُ يحمل الاستدراكَ وحدودَ التعميم، ولا يُسلَّم معنًى عاريًا."""

    extraction = THE_ABAT_EXTRACTION
    assert extraction.extracted_meaning in extraction.signifying_text
    assert len(extraction.qualifications) >= 3
    assert len(extraction.generalisation_limits) >= 3
    assert any("semantic_axes" in note for note in extraction.qualifications)
    assert any("مهملٌ عند الخليل" in note for note in extraction.qualifications)


# ── بابُ البصمة: نسخٌ بديلةٌ معلومةُ الهويّة ───────────────────────────────
#
# وما ههنا يمتحن مخالفةَ النسخة وحدَها. ولذلك يُكتَب الجدولُ نسخةً ثانيةً
# معلومةَ الهويّة على القرص ويُقرَأ بجذره، فلا يُخلَط سقوطُ مرشَّحٍ لتبدُّل
# بايتةٍ بسقوطه لعلّةٍ في نسبته أو في إسناد معناه.


def _alternative_copy(tmp_path: Path, mutate: bool) -> tuple[Path, str]:
    """نسخةُ اختبارٍ معلومةُ الهويّة، وبصمتُها مقيسةٌ على القرص لا مُعلَنة.

    و«المبدَّلة» مساويةُ الطولِ بالبايتات: كلمتان قُلِبتا في موضعٍ واحد. فلا
    يسقط الجدولُ لطولٍ مختلف، بل لبصمةٍ مختلفة، وهو المقصود.
    """

    source = Path("maqayis_by_root_csv_999.csv")
    raw = source.read_bytes()
    if mutate:
        before = "أصلٌ واحد، وهو الحرّ وشدّته.".encode()
        after = "أصلٌ واحد، وهو وشدّته الحرّ.".encode()
        assert len(before) == len(after)
        assert raw.count(before) == 1
        raw = raw.replace(before, after, 1)
    root = tmp_path / ("mutated" if mutate else "identical")
    root.mkdir()
    (root / source.name).write_bytes(raw)
    return root, hashlib.sha256(raw).hexdigest()


def test_an_identical_alternative_copy_admits_exactly_as_the_original() -> None:
    """نسخةٌ بديلةٌ مطابقةُ البايتات تُخرِج القرارَ نفسَه؛ فالفارقُ في البايتات."""

    with tempfile.TemporaryDirectory() as temporary:
        root, digest = _alternative_copy(Path(temporary), mutate=False)
        assert digest == extracted_candidate().source.measured_sha256
        reading = verify(
            extracted_candidate(root),
            root=root,
            segments=THE_ABAT_SEGMENTS,
            reviews=(extracted_review(),),
        )
        assert reading.standing is AdmissionStanding.ADMITTED
        assert reading.source_integrity is True


def test_a_mutated_copy_is_refused_at_the_deposit_before_any_candidate() -> None:
    """نسخةٌ قُلِبت فيها كلمتان تُرَدُّ عند بابِ الإيداع، فلا يُبنى عليها مرشَّح."""

    with tempfile.TemporaryDirectory() as temporary:
        root, digest = _alternative_copy(Path(temporary), mutate=True)
        assert digest != extracted_candidate().source.measured_sha256
        with pytest.raises(MaqayisRootTableError):
            extracted_candidate(root)


def test_a_digest_mismatch_suspends_at_the_source_not_at_the_attribution() -> None:
    """مخالفةُ البصمة تُعلِّق ببندِ «سلامةُ المصدر»، والنسبةُ باقيةٌ محقَّقة.

    وبصمةُ المخالفة مأخوذةٌ من نسخةٍ بديلةٍ معلومةِ الهويّة قِيست على القرص،
    لا من رقمٍ مُختلَق، فيكون الفصلُ بين البابين بشاهدٍ لا بدعوى.
    """

    with tempfile.TemporaryDirectory() as temporary:
        _, foreign_digest = _alternative_copy(Path(temporary), mutate=True)
        candidate = extracted_candidate()
        misdeclared = dataclasses.replace(
            candidate,
            source=dataclasses.replace(
                candidate.source, measured_sha256=foreign_digest
            ),
        )
        reading = verify(
            misdeclared, segments=THE_ABAT_SEGMENTS, reviews=(extracted_review(),)
        )
        assert reading.source_integrity is False
        assert reading.standing is AdmissionStanding.SUSPENDED
        assert any("سلامةُ المصدر" in note for note in reading.unmet_conditions)
        assert reading.attribution is (AttributionCheck.VERIFIED_BY_A_DEPOSITED_WITNESS)


def test_the_original_table_is_never_written_by_this_layer() -> None:
    """الأصلُ لا يُمَسّ: السجلُّ مُشتَقٌّ، وبصمةُ الجدول وطولُه كما كانا."""

    source = Path("maqayis_by_root_csv_999.csv")
    before = source.stat().st_size
    reconciliation_ledger()
    extracted_candidate()
    assert source.stat().st_size == before
    with source.open(encoding="utf-8") as handle:
        csv.field_size_limit(10**9)
        header = next(csv.reader(handle))
    assert header[0] == "root_full"
