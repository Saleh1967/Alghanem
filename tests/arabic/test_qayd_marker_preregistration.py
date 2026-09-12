"""حدودُ مسح علامات دلالة القيد: كلُّ حدٍّ مُسمًّى يُقابله مدخلٌ فعليٌّ يُظهِره.

**ولا يُقرأ من هذا الملفّ حكمٌ فقهيّ ولا حكمٌ على نصٍّ بعينه**: بطاقاتُ الحدود
هنا **مصنوعةٌ لهذا الضبط وحده** (`test_only`)، وسلطاتُها وألفاظُها مخترعةٌ
بالتصريح، فلا تُقرأ شهادةً على قائلٍ ولا على شرحٍ قائم. ولذلك بقيت في ملفّ
الاختبار ولم تُكتَب في `examples/`، على نصّ التعليل نفسِه في
`test_level_two_manat_negative_control.py`.

**ومعيارُ هذا الملفّ واحد**: ألّا يبقى في الشجرة ادّعاءُ حدٍّ لا يقع. فكلُّ عضوٍ
في `MarkerScanLimit` يُقابله هنا مدخلٌ يُشغِّل الأداةَ فعلًا ويُظهِر الحدَّ
كما وُصِف؛ فمتى زال الحدُّ سقط اختبارُه ولم يُقرَّ بيانُه بلا ما يُصدّقه.
"""

import json
from pathlib import Path
from typing import Final

import pytest

from alghanem.arabic.level_two_discrimination import (
    LEVEL_TWO_DISCRIMINATION_PREREGISTRATION,
)
from alghanem.arabic.level_two_manat import (
    SPECIFYING_TRANSMISSION_MARKERS,
    TARDI_TRANSMISSION_MARKERS,
    QaydSignification,
    derive_qayd_signification,
)
from alghanem.arabic.lexical_transmission import (
    LexicalAttribution,
    LexicalTransmissionDescriptor,
)
from alghanem.arabic.qayd_marker_preregistration import (
    LEXICAL_PATH_FRONT_IS_REGISTERED_NOT_OPENED,
    MARKER_SCAN_READS_THE_EXCERPT_ALONE_NOTE,
    MARKER_VOCABULARY_IS_FROZEN_BEFORE_ITS_TEXT_NOTE,
    NAMED_RESIDUALS,
    OPEN_FRONT_IS_REGISTERED_NOT_OPENED_NOTE,
    PRINT_EDITION_LOCUS_NOT_VERIFIED,
    QAYD_MARKER_PREREGISTRATION,
    SECONDARY_PARAPHRASE_IS_NOT_A_VERBATIM_EXCERPT_NOTE,
    TRANSMITTED_CONFLICT_CERTIFIES_NOTHING_FROZEN_NOTE,
    VERBATIM_TEXT_IS_NOT_SUPPLIED_HERE,
    MarkerOutcomeRegistration,
    MarkerScanLimit,
    QaydMarkerPreregistration,
    QaydMarkerPreregistrationError,
)

_TEST_ONLY_MARKER: Final = "test_only"

_COMPOSITION: Final = (
    Path(__file__).resolve().parents[2]
    / "examples"
    / "level_two_manat"
    / "ghanam_saima_composition.yaml"
)


def _descriptor(*excerpts: str) -> LexicalTransmissionDescriptor:
    """واصفٌ مخترعٌ لهذا الضبط: سلطاتُه مُسمّاةٌ بأنّها مخترعة، ونصوصُه كذلك."""

    return LexicalTransmissionDescriptor(
        entry_id=f"q-{_TEST_ONLY_MARKER}-marker-limits",
        compiler_source="مُجمِّعٌ مخترعٌ لهذا الضبط",
        entry_locus="قيدٌ مخترعٌ لهذا الضبط",
        attributions=tuple(
            LexicalAttribution(
                attributed_authority=f"سلطةٌ مخترعة {index}",
                verbatim_excerpt=excerpt,
                locus=f"موضعٌ مخترعٌ {index}",
            )
            for index, excerpt in enumerate(excerpts, start=1)
        ),
    )


def test_every_outcome_is_registered_with_licensed_and_refused_readings() -> None:
    """كلُّ عضوٍ في مفردة دلالة القيد مُسجَّلٌ قبل النصّ بنصَّيه، بلا استثناء."""

    registration = QAYD_MARKER_PREREGISTRATION

    for member in QaydSignification:
        entry = registration.registration_for(member)
        assert entry.licensed_reading.strip()
        assert entry.refused_reading.strip()
    assert {refusal.name for refusal in registration.refusals} >= {
        "MarkerVocabularyIsFrozenBeforeItsText",
        "MarkerScanReadsTheExcerptAlone",
        "TransmittedConflictCertifiesNothingFrozen",
    }


def test_an_unregistered_outcome_or_limit_is_refused_at_construction() -> None:
    """تغطيةُ المخرجات والحدود تسبق القراءة، وناقصُها يُرفَض عند الإنشاء."""

    registration = QAYD_MARKER_PREREGISTRATION

    with pytest.raises(QaydMarkerPreregistrationError, match="غيرُ مُسجَّلٍ قبل النصّ"):
        QaydMarkerPreregistration(
            scan_surface=registration.scan_surface,
            limits=registration.limits,
            outcomes=registration.outcomes[:-1],
            widening_condition=registration.widening_condition,
            refusals=registration.refusals,
        )

    with pytest.raises(QaydMarkerPreregistrationError, match="غيرُ مُسمًّى قبل النصّ"):
        QaydMarkerPreregistration(
            scan_surface=registration.scan_surface,
            limits=registration.limits[:-1],
            outcomes=registration.outcomes,
            widening_condition=registration.widening_condition,
            refusals=registration.refusals,
        )


def test_the_scan_reads_the_excerpt_alone_and_not_the_authority_or_locus() -> None:
    """علامةٌ واقعةٌ في موضعٍ أو مادّةٍ لا تُغيّر دلالةَ القيد بحرف."""

    descriptor = LexicalTransmissionDescriptor(
        entry_id=f"q-{_TEST_ONLY_MARKER}-surface",
        compiler_source="مُجمِّعٌ مخترعٌ في مفهوم المخالفة",
        entry_locus="بابٌ مخترعٌ في مفهوم المخالفة",
        attributions=(
            LexicalAttribution(
                attributed_authority="سلطةٌ مخترعة",
                verbatim_excerpt="قالت سلطةٌ مخترعة: كلامٌ لا علامةَ فيه البتّة",
                locus="موضعٌ مخترعٌ فيه مفهوم المخالفة",
            ),
        ),
    )

    assert derive_qayd_signification(descriptor) is (
        QaydSignification.دلالة_القيد_غير_محسومة
    )
    assert "وحده" in MARKER_SCAN_READS_THE_EXCERPT_ALONE_NOTE


def test_the_scan_is_blind_to_negation_as_its_registration_states() -> None:
    """علامةٌ واقعةٌ داخل نفيٍ تُقرأ علامةً وقعت، وهذا عكسُ مراد قائلها."""

    descriptor = _descriptor("قالت سلطةٌ مخترعة 1: ليس هذا من مفهوم المخالفة في شيء")

    assert derive_qayd_signification(descriptor) is QaydSignification.قيد_مخصص
    assert "عكسُ مراد قائله" in QAYD_MARKER_PREREGISTRATION.statement_for(
        MarkerScanLimit.عمى_عن_النفي
    )


def test_the_scan_is_blind_to_the_stance_of_the_saying() -> None:
    """ترددُ قائلٍ يقع عند المسح كجزمه، فلا يُقرأ مُخرَجُه نسبةً جازمةً إليه."""

    hesitant = _descriptor("قالت سلطةٌ مخترعة 1: يحتمل أن يكون الوصفُ طرديًّا")
    assertive = _descriptor("قالت سلطةٌ مخترعة 1: الوصفُ طرديٌّ قطعًا")

    assert derive_qayd_signification(hesitant) is QaydSignification.وصف_طردي
    assert derive_qayd_signification(assertive) is derive_qayd_signification(hesitant)
    assert "جازمةً" in QAYD_MARKER_PREREGISTRATION.statement_for(
        MarkerScanLimit.عمى_عن_جهة_القول
    )


def test_the_scan_is_blind_to_who_carries_the_marker() -> None:
    """علامةٌ يَنقُلها ناقلٌ عن خصمه ليردّها تقع عنده كالعلامة يقولها عن نفسه."""

    descriptor = _descriptor(
        "قالت سلطةٌ مخترعة 1: زعم بعضُ المخالفين أنّه لا مفهوم له، وهذا مردود"
    )

    assert derive_qayd_signification(descriptor) is QaydSignification.وصف_طردي
    assert "حكايةَ خلافٍ" in QAYD_MARKER_PREREGISTRATION.statement_for(
        MarkerScanLimit.عمى_عن_ناقل_العلامة
    )


def test_the_scan_is_blind_to_a_shared_word_that_means_something_else() -> None:
    """«أخرجه» تخريجًا للحديث تقع علامةَ تخصيصٍ عند المسح، وهي أرجحُ المصادفات."""

    descriptor = _descriptor("قالت سلطةٌ مخترعة 1: أخرجه صاحبُ الجامع في بابه")

    assert derive_qayd_signification(descriptor) is QaydSignification.قيد_مخصص
    assert "تخريجٌ للحديث" in QAYD_MARKER_PREREGISTRATION.statement_for(
        MarkerScanLimit.عمى_عن_اشتراك_اللفظ
    )


def test_a_conflict_of_markers_is_registered_as_a_case_certifying_nothing() -> None:
    """اجتماعُ العلامتين يُخرِج التعارضَ المنقول، ولا يفتح مُجمَّدًا ولا يُفركِل."""

    descriptor = _descriptor(
        "قالت سلطةٌ مخترعة 1: هذا القيدُ أخرج ما عداه من الحكم",
        "قالت سلطةٌ مخترعة 2: بل الوصفُ طرديٌّ لا مفهوم له",
    )
    entry = QAYD_MARKER_PREREGISTRATION.registration_for(
        QaydSignification.دلالة_القيد_متعارضة
    )

    assert derive_qayd_signification(descriptor) is (
        QaydSignification.دلالة_القيد_متعارضة
    )
    assert "قضيّةً لا عطلًا" in entry.licensed_reading
    assert TRANSMITTED_CONFLICT_CERTIFIES_NOTHING_FROZEN_NOTE in entry.refused_reading


def test_the_widening_condition_precedes_any_text_it_would_be_measured_on() -> None:
    """شرطُ توسيع المفردة مكتوبٌ قبل النصّ، لا يُكتَب بعد رؤية أثره عليه."""

    condition = QAYD_MARKER_PREREGISTRATION.widening_condition

    assert MARKER_VOCABULARY_IS_FROZEN_BEFORE_ITS_TEXT_NOTE in condition
    assert "يسبق" in condition


def test_the_residuals_are_named_and_the_verbatim_text_is_not_supplied_here() -> None:
    """الفضلاتُ مُسمّاةٌ بنصّها: عمى المسح، وموضعُ النقل، وموضعُ الطبعة، والجبهة."""

    assert set(NAMED_RESIDUALS) == {
        "SCAN_IS_BLIND_TO_NEGATION_AND_STANCE",
        "VERBATIM_TEXT_IS_NOT_SUPPLIED_HERE",
        "PRINT_EDITION_LOCUS_NOT_VERIFIED",
        "LEXICAL_PATH_FRONT_IS_REGISTERED_NOT_OPENED",
    }
    assert all(statement.strip() for statement in NAMED_RESIDUALS.values())
    assert (
        "موضعُ النصّ بطاقتُه لا هذا السجلّ"
        in (NAMED_RESIDUALS["VERBATIM_TEXT_IS_NOT_SUPPLIED_HERE"])
    )


def test_the_open_front_is_registered_with_its_observation_locus_only() -> None:
    """المتغيّرُ المرصود يُسمّى بموضع رصده، وتاريخُه من الكوميت لا من نصٍّ مكتوب."""

    residual = NAMED_RESIDUALS[LEXICAL_PATH_FRONT_IS_REGISTERED_NOT_OPENED]

    assert "طريق_النقل_المعجمي" in residual
    assert "الكوميت الذي أُضيفت فيه هذه البقيّة" in residual
    assert OPEN_FRONT_IS_REGISTERED_NOT_OPENED_NOTE in residual
    assert {refusal.name for refusal in QAYD_MARKER_PREREGISTRATION.refusals} >= {
        "OpenFrontIsRegisteredNotOpened"
    }


def test_the_failed_attempt_and_its_later_supply_are_both_kept_in_the_record() -> None:
    """الامتناعُ الأوّل والتزويدُ اللاحق مكتوبان معًا: لا يُمحى أحدُهما بالآخر."""

    residual = NAMED_RESIDUALS[VERBATIM_TEXT_IS_NOT_SUPPLIED_HERE]

    assert "طُلِب النصُّ فامتنع ثمّ زُوِّد" in residual
    assert "بإسنادٍ واحدٍ لا اثنين" in residual
    assert "حكايةُ معنًى في وسائط ثانوية" in residual
    assert SECONDARY_PARAPHRASE_IS_NOT_A_VERBATIM_EXCERPT_NOTE in residual
    assert "الطبري" in SECONDARY_PARAPHRASE_IS_NOT_A_VERBATIM_EXCERPT_NOTE
    assert "لتعذُّر التحقق الحرفيّ وحده" in (
        SECONDARY_PARAPHRASE_IS_NOT_A_VERBATIM_EXCERPT_NOTE
    )
    assert {refusal.name for refusal in QAYD_MARKER_PREREGISTRATION.refusals} >= {
        "SecondaryParaphraseIsNotAVerbatimExcerpt"
    }


def test_the_print_edition_locus_residual_is_raised_in_part_and_not_in_whole() -> None:
    """[ص: 372] رفعت البقيّةَ جزئيًّا، والمجلَّدُ والنسخةُ الورقية لم يُتحقَّقا."""

    residual = NAMED_RESIDUALS[PRINT_EDITION_LOCUS_NOT_VERIFIED]

    assert "جزئيًّا لا كلّيًّا" in residual
    assert "رقمَ المجلَّد لم يُذكَر" in residual
    assert "الطبريُّ" in residual
    assert "لا تمسّ المُشتَقّ" in residual


def test_the_supplied_text_filled_the_card_and_left_vocabularies_untouched() -> None:
    """النقلُ حرّك البطاقةَ وحدها: لا مفردةَ وُسِّعت، ولا احتمالَ نتيجةٍ أُضيف."""

    card = json.loads(_COMPOSITION.read_text(encoding="utf-8"))
    excerpt = card["طريق_النقل_المعجمي"]["الإسنادات"][0]["الاقتباس_المنقول"]

    assert len(card["طريق_النقل_المعجمي"]["الإسنادات"]) == 1
    assert not any(marker in excerpt for marker in SPECIFYING_TRANSMISSION_MARKERS)
    assert not any(marker in excerpt for marker in TARDI_TRANSMISSION_MARKERS)
    assert len(QaydSignification) == 4
    assert len(MarkerScanLimit) == 4


def test_registering_a_front_builds_no_tool_and_widens_no_closed_vocabulary() -> None:
    """التسجيلُ تأريخٌ لا عمل: لا مفردةَ وُسِّعت، ولا متغيّرَ التجربة تبدّل."""

    assert "لا تُبنى له أداةٌ" in OPEN_FRONT_IS_REGISTERED_NOT_OPENED_NOTE
    assert (
        "NoRicherStructureBeforeLowerOpenResidualClosure"
        in OPEN_FRONT_IS_REGISTERED_NOT_OPENED_NOTE
    )
    assert len(QaydSignification) == 4
    assert len(MarkerScanLimit) == 4
    assert "الإسنادات" in LEVEL_TWO_DISCRIMINATION_PREREGISTRATION.controlled_variable
    assert "ولا يُمَسّ شيءٌ سواه" in (
        LEVEL_TWO_DISCRIMINATION_PREREGISTRATION.controlled_variable
    )


def test_every_named_limit_is_registered_with_a_statement_of_its_own() -> None:
    """لا حدَّ مُسمًّى بلا بيان، ولا بيانَ مكرَّرٌ يُغني عن حدٍّ آخر."""

    statements = [
        QAYD_MARKER_PREREGISTRATION.statement_for(limit) for limit in MarkerScanLimit
    ]

    assert set(QAYD_MARKER_PREREGISTRATION.registered_limits) == set(MarkerScanLimit)
    assert len(set(statements)) == len(statements)


def test_a_registration_without_a_named_refusal_is_refused() -> None:
    """تسجيلٌ بلا رفضٍ مُسمًّى لا يقوم: حدودُ المسح تُسمّى ولا تُترَك للقارئ."""

    registration = QAYD_MARKER_PREREGISTRATION

    with pytest.raises(QaydMarkerPreregistrationError, match="بلا رفضٍ مُسمًّى"):
        QaydMarkerPreregistration(
            scan_surface=registration.scan_surface,
            limits=registration.limits,
            outcomes=registration.outcomes,
            widening_condition=registration.widening_condition,
            refusals=(),
        )

    with pytest.raises(QaydMarkerPreregistrationError, match="المُخرَجُ من مفردته"):
        MarkerOutcomeRegistration(
            signification="قيد_مخصص",  # type: ignore[arg-type]
            licensed_reading="نصٌّ مخترعٌ لهذا الضبط",
            refused_reading="نصٌّ مخترعٌ لهذا الضبط",
        )
