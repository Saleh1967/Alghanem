"""بوّابةُ الخطّ المستقلّ: الانفكاكُ محسوبٌ، والمصدرُ مُودَع، والمُسجَّلُ لا يُقلَب.

يُثبِت هذا الاختبارُ خمسةَ أشياء: أنّ إعادةَ رسمِ الوصف نفسِه (تشكيلًا أو
تطويلًا أو مسافاتٍ أو حالةَ حرف) لا تُقبَل خطًّا ثانيًا، وأنّ الاستشهادَ بلا
بصمةِ حمولةٍ لا يُودِع مصدرًا، وأنّ انفكاكًا لا يأذن فيه المصدرُ يُرَدّ، وأنّ
خطًّا مستقلًّا حقًّا يقلب الفحصَ إلى `PASS` وحكمَ السلسلة إلى
`CLOSURE_MET_PENDING_AUTHORITY` فيُصدَّق، وأنّ البطاقةَ المُسجَّلة تبقى بعد
ذلك كلِّه `FAIL` و`DEFER_IN_SCOPE` ولا خطَّ مقبولٌ مُودَعٌ في المستودع.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.phonetic_economy_candidate import (
    CLOSURE_BLOCKING_RESIDUAL_CODE,
    PHONETIC_ECONOMY_CANDIDATE,
    TOOL_RECONSTRUCTION_RESIDUAL_CODE,
    CertifiedPhoneticEconomyFinding,
    ChainVerdict,
    ClosureOutcome,
    IndependenceAxis,
    PhoneticEconomyRegistrationError,
    PhoneticEvidenceItem,
    certify_phonetic_economy_candidate,
)
from alghanem.arabic.phonetic_economy_independent_line import (
    ADMITTED_INDEPENDENT_LINES,
    NO_INDEPENDENT_LINE_DEPOSITED,
    NO_INDEPENDENT_LINE_RESIDUAL_CODE,
    SESSION_BASELINE_EVIDENCE,
    AdmittedIndependentLine,
    ExternalSourceDeposit,
    IndependentLineAdmissionError,
    SourceDepositState,
    admit_independent_line,
    candidate_with_admitted_line,
    closure_check_with_admitted_line,
    cosmetic_axis_key,
)
from alghanem.arabic.phonetic_economy_tool import TOOL_MODULE_PATH

_DIGEST = "a" * 64

_BASELINE = SESSION_BASELINE_EVIDENCE
_SESSION_CORPUS = _BASELINE[0].corpus_identity
_SESSION_METRIC = _BASELINE[0].metric_definition


def _deposit(
    *axes: IndependenceAxis, payload_digest: str | None = _DIGEST
) -> ExternalSourceDeposit:
    return ExternalSourceDeposit(
        source_id="مصدرُ صوتيّاتٍ مستقلٌّ مفترَضٌ للاختبار",
        citation="سجلُّ مخارجَ مقيسٌ خارجَ الجلسة",
        licensed_axes=axes or (IndependenceAxis.كوربص,),
        payload_digest=payload_digest,
    )


def _line(
    *,
    key: str = "OTHER_LINE",
    corpus: str | None = None,
    tool: str | None = None,
    metric: str | None = None,
) -> PhoneticEvidenceItem:
    return PhoneticEvidenceItem(
        key=key,
        phenomenon="ظاهرةٌ صوتيّةٌ ثالثة",
        statistic_name="F",
        statistic_value=2.5,
        corpus_identity=corpus if corpus is not None else _SESSION_CORPUS,
        tool_identity=tool if tool is not None else TOOL_MODULE_PATH,
        metric_definition=metric if metric is not None else _SESSION_METRIC,
    )


def test_cosmetic_rewriting_is_not_a_second_source() -> None:
    """تطويلٌ وتشكيلٌ ومسافاتٌ زائدةٌ على الوصف نفسِه لا تصنع كوربصًا آخر."""

    disguised = "  " + _SESSION_CORPUS.replace("كوربص", "كــوربَص") + "  "
    assert cosmetic_axis_key(disguised) == cosmetic_axis_key(_SESSION_CORPUS)
    with pytest.raises(IndependentLineAdmissionError, match="ليست مصدرًا ثانيًا"):
        admit_independent_line(_line(corpus=disguised), _deposit(), _BASELINE)


def test_identical_line_is_refused() -> None:
    """خطٌّ يوافق الأساسَ على المحاور الثلاثة يُرَدّ ولو اختلف مفتاحُه."""

    with pytest.raises(IndependentLineAdmissionError, match="المحاور الثلاثة"):
        admit_independent_line(_line(), _deposit(), _BASELINE)


def test_repeated_evidence_key_is_not_a_second_line() -> None:
    """مفتاحُ دليلٍ قائمٌ لا يصير خطًّا ثانيًا بتبديل محتواه."""

    with pytest.raises(IndependentLineAdmissionError, match="NUN_SAKIN"):
        admit_independent_line(
            _line(key="NUN_SAKIN", corpus="كوربصٌ آخرُ مُودَع"),
            _deposit(),
            _BASELINE,
        )


def test_citation_without_digest_deposits_nothing() -> None:
    """الاستشهادُ وحدَه لا يُودِع مصدرًا؛ وحالُ الإيداع مُشتقٌّ من البصمة."""

    undeposited = _deposit(payload_digest=None)
    assert undeposited.state is SourceDepositState.غير_مُودَع
    with pytest.raises(IndependentLineAdmissionError, match="غيرُ مُودَعٍ"):
        admit_independent_line(
            _line(corpus="كوربصٌ آخرُ مقيسٌ خارجَ الجلسة"), undeposited, _BASELINE
        )


def test_malformed_digest_is_refused_at_construction() -> None:
    """بصمةٌ على غير شكلِ بصمةِ المستودع إيداعٌ مُدَّعًى، تُرَدُّ عند البناء."""

    with pytest.raises(IndependentLineAdmissionError, match="بصمةُ الحمولة"):
        _deposit(payload_digest="ليست-بصمة")


def test_unlicensed_axis_break_is_refused() -> None:
    """انفكاكٌ نصّيٌّ على محورٍ لا يأذن فيه المصدرُ ليس استقلالًا."""

    with pytest.raises(IndependentLineAdmissionError, match="لا يأذن فيها المصدرُ"):
        admit_independent_line(
            _line(metric="تعريفُ مقياسٍ منفصلٌ حقًّا"),
            _deposit(IndependenceAxis.كوربص),
            _BASELINE,
        )


def test_attached_tool_rewrapped_is_still_the_attached_tool() -> None:
    """الأداةُ المرفقةُ ملفوفةً بمسارٍ أو تعليقٍ ليست أداةً أخرى."""

    with pytest.raises(IndependentLineAdmissionError, match="الأداةُ المرفقةُ"):
        admit_independent_line(
            _line(tool="./" + TOOL_MODULE_PATH.upper() + " (إعادةُ تشغيلٍ لها نفسِها)"),
            _deposit(IndependenceAxis.أداة),
            _BASELINE,
        )


def test_admission_cannot_be_constructed_directly() -> None:
    """القبولُ يُصدَر من البوّابة وحدَها؛ وبناءُ الصنف مباشرةً يُرَدّ."""

    with pytest.raises(IndependentLineAdmissionError, match="admit_independent_line"):
        AdmittedIndependentLine(
            evidence=_line(corpus="كوربصٌ آخر"),
            deposit=_deposit(),
            baseline=_BASELINE,
        )


def _genuine_admission() -> AdmittedIndependentLine:
    return admit_independent_line(
        _line(
            key="INDEPENDENT_CORPUS_LINE",
            corpus="كوربصٌ آخرُ مُودَعٌ ببصمته، مقيسٌ خارجَ جلسة GFLK",
        ),
        _deposit(IndependenceAxis.كوربص),
        _BASELINE,
    )


def test_genuine_line_breaks_one_axis_and_flips_closure() -> None:
    """خطٌّ من كوربصٍ آخرَ مُودَعٍ ينفكّ على محورِه وحدَه ويقلب الفحصَ `PASS`."""

    admission = _genuine_admission()
    assert admission.broken_axes == (IndependenceAxis.كوربص,)
    extended = closure_check_with_admitted_line(
        PHONETIC_ECONOMY_CANDIDATE.closure_check, admission
    )
    assert extended.outcome is ClosureOutcome.PASS
    assert extended.collapsed_axes == (
        IndependenceAxis.أداة,
        IndependenceAxis.تعريف_المقياس,
    )


def test_flipped_candidate_drops_the_blocking_residual_and_certifies() -> None:
    """بطاقةُ الخطّ المقبول تُسقط بقيّةَ المنع، وتبلغ أقصى ما تبلغه: انتظارَ سلطة."""

    upgraded = candidate_with_admitted_line(
        PHONETIC_ECONOMY_CANDIDATE, _genuine_admission()
    )
    assert CLOSURE_BLOCKING_RESIDUAL_CODE not in upgraded.residual_codes
    assert TOOL_RECONSTRUCTION_RESIDUAL_CODE in upgraded.residual_codes
    assert upgraded.verdict is ChainVerdict.CLOSURE_MET_PENDING_AUTHORITY
    certified = certify_phonetic_economy_candidate(upgraded)
    assert isinstance(certified, CertifiedPhoneticEconomyFinding)
    assert certified.candidate is upgraded


def test_admission_is_not_portable_to_another_baseline() -> None:
    """قبولٌ حُكم على أدلّةٍ لا يُنقَل إلى أدلّةٍ غيرِها."""

    admission = _genuine_admission()
    other = closure_check_with_admitted_line(
        PHONETIC_ECONOMY_CANDIDATE.closure_check, admission
    )
    with pytest.raises(IndependentLineAdmissionError, match="أساسٍ إلى أساس"):
        closure_check_with_admitted_line(other, admission)


def test_registered_candidate_is_untouched() -> None:
    """المُسجَّلُ يبقى كما سُجِّل: نتيجةٌ سلبيةٌ لا تُمحى بقلبِ حالٍ لاحق."""

    candidate_with_admitted_line(PHONETIC_ECONOMY_CANDIDATE, _genuine_admission())
    assert PHONETIC_ECONOMY_CANDIDATE.closure_check.outcome is ClosureOutcome.FAIL
    assert PHONETIC_ECONOMY_CANDIDATE.verdict is ChainVerdict.DEFER_IN_SCOPE
    assert CLOSURE_BLOCKING_RESIDUAL_CODE in PHONETIC_ECONOMY_CANDIDATE.residual_codes
    with pytest.raises(PhoneticEconomyRegistrationError):
        certify_phonetic_economy_candidate(PHONETIC_ECONOMY_CANDIDATE)


def test_no_independent_corpus_line_is_deposited_in_this_repository() -> None:
    """لا خطَّ ينفكّ على محور الكوربص مُودَعًا؛ والبقيّةُ تقول ذلك بمداها."""

    assert ADMITTED_INDEPENDENT_LINES == ()
    assert NO_INDEPENDENT_LINE_DEPOSITED.code == NO_INDEPENDENT_LINE_RESIDUAL_CODE
    assert NO_INDEPENDENT_LINE_RESIDUAL_CODE == "NO_INDEPENDENT_CORPUS_LINE_DEPOSITED"
    assert "محورُ الكوربص" in NO_INDEPENDENT_LINE_DEPOSITED.statement


def test_admission_error_is_caught_as_registration_error() -> None:
    """رفضُ البوّابة فرعٌ من خطأ التسجيل، فلا يتسرّب صنفًا غيرَ مُلتقَط."""

    assert issubclass(IndependentLineAdmissionError, PhoneticEconomyRegistrationError)
    with pytest.raises(PhoneticEconomyRegistrationError):
        admit_independent_line(_line(), _deposit(), _BASELINE)
