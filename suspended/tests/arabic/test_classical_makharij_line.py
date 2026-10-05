"""الجدولُ التقليديُّ المُودَع: بصمةٌ مُعادةُ الاشتقاق، وانفكاكٌ محسوب، ومقاديرُ منهارة.

يُثبِت هذا الاختبارُ ستّةَ أشياء: أنّ الجدولَ مُودَعٌ ببصمةٍ تُعاد اشتقاقًا لا
تُعلَن، وأنّه يُرقّم ثمانيةً وعشرين حرفًا بلا تكرارٍ ولا إسقاط، وأنّ حرفًا بلا
رتبةٍ يُرَدُّ صريحًا لا يُتجاوَز صمتًا، وأنّ الخطَّ المُودَعَ ينفكّ على محورَي
الأداة وتعريفِ المقياس وحدَهما فيقلب الفحصَ إلى `PASS` وحكمَ البطاقة المُمدَّدة
إلى `CLOSURE_MET_PENDING_AUTHORITY`، وأنّ اتّجاهَ الدعوى صمد ومقاديرَ الجلسة
انهارت فسُجِّلت البقيّةُ محسوبةً، وأنّ البطاقةَ المُسجَّلة بقيت `FAIL`
و`DEFER_IN_SCOPE` لم تُمسّ.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.classical_makharij_table import (
    CLASSICAL_MAKHARIJ,
    CLASSICAL_ORDINAL,
    CLASSICAL_TABLE_DIGEST,
    ClassicalMakhrajError,
    average_ordinal_distance,
    classical_lam_f,
    classical_nun_f,
    rederive_classical_table_digest,
)
from alghanem.arabic.phonetic_economy_candidate import (
    CLOSURE_BLOCKING_RESIDUAL_CODE,
    PHONETIC_ECONOMY_CANDIDATE,
    TOOL_RECONSTRUCTION_RESIDUAL_CODE,
    ChainVerdict,
    ClosureOutcome,
    IndependenceAxis,
)
from alghanem.arabic.phonetic_economy_classical_line import (
    CLASSICAL_EXTENDED_CANDIDATE,
    CLASSICAL_MAKHARIJ_DEPOSIT,
    CLASSICAL_NUN_LINE,
    CLASSICAL_NUN_LINE_ADMISSION,
    CLASSICAL_TABLE_READINGS,
    MAGNITUDE_COLLAPSE_RESIDUAL_CODE,
)
from alghanem.arabic.phonetic_economy_independent_line import SourceDepositState
from alghanem.arabic.phonetic_economy_tool import (
    IDGHAM_NUN_LETTERS,
    IZHAR_NUN_LETTERS,
    PLACE_NUM,
    compute_lam_f,
    compute_nun_f,
)

RECORDED_TABLE_DIGEST = (
    "5830bc0c72d31621a644a9bc5035082b248946cb898e23a2f251377529526def"
)


def test_table_digest_is_rederived_not_declared() -> None:
    """البصمةُ تُحسَب من بايتات الجدول الآن، وتطابق المُسجَّلَ في المادة المرجعية."""

    assert rederive_classical_table_digest() == CLASSICAL_TABLE_DIGEST
    assert CLASSICAL_TABLE_DIGEST == RECORDED_TABLE_DIGEST


def test_table_ranks_every_consonant_exactly_once() -> None:
    """ثمانيةٌ وعشرون حرفًا في ستّةَ عشرَ مخرجًا، بلا حرفٍ في مخرجَين."""

    assert len(CLASSICAL_MAKHARIJ) == 16
    assert len(CLASSICAL_ORDINAL) == 28
    letters = "".join(letters for _rank, _name, letters in CLASSICAL_MAKHARIJ)
    assert len(letters) == len(set(letters)) == 28
    assert set(CLASSICAL_ORDINAL) == set(PLACE_NUM)


def test_unranked_letter_is_refused_not_skipped() -> None:
    """حرفٌ بلا رتبةٍ يُرَدُّ صريحًا؛ وإسقاطُه صمتًا يُغيّر المتوسّطَ بلا أثر."""

    with pytest.raises(ClassicalMakhrajError, match="لا رتبةَ لها"):
        average_ordinal_distance(frozenset({"ن", "ا"}), 9)
    with pytest.raises(ClassicalMakhrajError, match="غيرِ فارغة"):
        average_ordinal_distance(frozenset(), 9)


def test_classical_table_is_not_the_session_table() -> None:
    """الترتيبُ التقليديُّ يخالف جدولَ الجلسة، وليس إعادةَ رسمٍ له."""

    assert CLASSICAL_ORDINAL != dict(PLACE_NUM)
    # الجلسةُ جعلت الشفويّ ١ والحلقيّ ٩؛ والتقليديُّ يعكس الاتّجاه.
    assert CLASSICAL_ORDINAL["ء"] < CLASSICAL_ORDINAL["ب"]
    assert PLACE_NUM["ء"] > PLACE_NUM["ب"]


def test_direction_survives_under_the_independent_table() -> None:
    """النسبتان تبقيان فوق الواحد: الإظهارُ والقمريُّ أبعدُ مخرجًا فعلًا."""

    assert classical_nun_f() > 1.0
    assert classical_lam_f() > 1.0
    nun = average_ordinal_distance(IZHAR_NUN_LETTERS, CLASSICAL_ORDINAL["ن"])
    assert nun > average_ordinal_distance(IDGHAM_NUN_LETTERS, CLASSICAL_ORDINAL["ن"])


def test_session_magnitudes_collapse_under_the_independent_table() -> None:
    """المقاديرُ تنهار، ولامُ التعريف خاصّةً؛ والانهيارُ محسوبٌ لا مكتوب."""

    readings = {reading.phenomenon_key: reading for reading in CLASSICAL_TABLE_READINGS}
    lam = readings["LAM_TARIF"]
    assert lam.session_value == 9.5
    assert lam.direction_preserved
    assert not lam.reproduces_session_magnitude
    assert lam.magnitude_ratio < 0.25
    nun = readings["NUN_SAKIN"]
    assert nun.direction_preserved
    assert not nun.reproduces_session_magnitude
    # ولا يُقرأ الانهيارُ فارقَ تقريبٍ عن أداة المستودع المبسَّطة.
    assert round(classical_lam_f(), 1) != round(compute_lam_f(), 1)
    assert round(classical_nun_f(), 1) != round(compute_nun_f(), 1)


def test_deposit_is_deposited_and_licenses_only_what_it_covers() -> None:
    """المصدرُ مُودَعٌ ببصمته، ويأذن في الأداة وتعريفِ المقياس دون الكوربص."""

    assert CLASSICAL_MAKHARIJ_DEPOSIT.state is SourceDepositState.مُودَع
    assert CLASSICAL_MAKHARIJ_DEPOSIT.payload_digest == CLASSICAL_TABLE_DIGEST
    assert CLASSICAL_MAKHARIJ_DEPOSIT.licenses(IndependenceAxis.أداة)
    assert CLASSICAL_MAKHARIJ_DEPOSIT.licenses(IndependenceAxis.تعريف_المقياس)
    assert not CLASSICAL_MAKHARIJ_DEPOSIT.licenses(IndependenceAxis.كوربص)


def test_admitted_line_breaks_two_axes_not_three() -> None:
    """ينفكّ محورا الأداة والمقياس، ومحورُ الكوربص باقٍ منطبقًا."""

    assert CLASSICAL_NUN_LINE_ADMISSION.broken_axes == (
        IndependenceAxis.أداة,
        IndependenceAxis.تعريف_المقياس,
    )
    assert (
        CLASSICAL_NUN_LINE.corpus_identity
        == PHONETIC_ECONOMY_CANDIDATE.closure_check.evidence[0].corpus_identity
    )


def test_extended_candidate_passes_but_reaches_only_pending_authority() -> None:
    """الفحصُ ينقلب `PASS`، وأقصى الحكم انتظارُ سلطةٍ لم تُبنَ، لا ولادة."""

    assert CLASSICAL_EXTENDED_CANDIDATE.closure_check.outcome is ClosureOutcome.PASS
    assert (
        CLASSICAL_EXTENDED_CANDIDATE.verdict
        is ChainVerdict.CLOSURE_MET_PENDING_AUTHORITY
    )
    assert not any(member.name in {"BORN", "CERTIFIED"} for member in ChainVerdict)


def test_extended_candidate_carries_the_new_and_the_surviving_residuals() -> None:
    """تسقط بقيّةُ منعِ الإغلاق وحدَها، وتبقى بقيّةُ الأداة وتُضاف بقايا الحدود."""

    codes = CLASSICAL_EXTENDED_CANDIDATE.residual_codes
    assert CLOSURE_BLOCKING_RESIDUAL_CODE not in codes
    assert TOOL_RECONSTRUCTION_RESIDUAL_CODE in codes
    assert MAGNITUDE_COLLAPSE_RESIDUAL_CODE in codes
    assert "CORPUS_AXIS_STILL_COLLAPSED" in codes
    assert "ORDINAL_DISTANCE_IS_OUR_MODELLING_STEP" in codes


def test_registered_negative_result_is_untouched() -> None:
    """المُسجَّلُ يبقى كما سُجِّل؛ ونتيجةٌ سلبيةٌ لا تُمحى بإيداعٍ لاحق."""

    assert PHONETIC_ECONOMY_CANDIDATE.closure_check.outcome is ClosureOutcome.FAIL
    assert PHONETIC_ECONOMY_CANDIDATE.verdict is ChainVerdict.DEFER_IN_SCOPE
    assert CLOSURE_BLOCKING_RESIDUAL_CODE in PHONETIC_ECONOMY_CANDIDATE.residual_codes
    assert len(PHONETIC_ECONOMY_CANDIDATE.closure_check.evidence) == 2


def test_lam_is_read_as_a_comparison_not_a_second_evidence_line() -> None:
    """لامُ التعريف مقارنةٌ لا خطُّ دليلٍ ثانٍ؛ وأداةٌ واحدةٌ مرّتين هي العطبُ عينه."""

    keys = tuple(
        item.key for item in CLASSICAL_EXTENDED_CANDIDATE.closure_check.evidence
    )
    assert keys == ("NUN_SAKIN", "LAM_TARIF", "NUN_SAKIN_CLASSICAL_TABLE")
