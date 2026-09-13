"""إغلاقُ جبهة «سائمة الغنم» بنتيجةٍ سالبةٍ تامّة، وما لم يتغيّر بإغلاقها.

الجبهةُ المُسجَّلة في `qayd_marker_preregistration` علّقت فتحَها على «إغلاق
تجربة سائمة الغنم بنتيجةٍ واحدةٍ كاملة». وهذه الاختباراتُ تُثبت ثلاثةً معًا:
أنّ المسحَ أُجري على كامل المصدر لا على بابه، وأنّ نتيجتَه **سالبةٌ تامّة** لا
ترقية، وأنّ شيئًا من البطاقة ولا من تسجيلها المسبق لم يتغيّر بها.

**وأثقلُ ما يُختبَر هنا ما لم يقع**: أنّ جنسَ الوقوف باقٍ، وأنّ مرتبةَ الموضع
العليا باقيةٌ بلا مدخل، وأنّ موضعَ البطاقة لم يُستبدَل بموضع الشاهد، وأنّ
الجبهةَ لم تُفتَح في الخطوة التي أغلقت شرطَها.
"""

import json
from pathlib import Path
from typing import Final

import pytest

from alghanem.arabic.level_two_manat import (
    LevelTwoStopGenus,
    QaydSignification,
)
from alghanem.arabic.level_two_source_texts import (
    CLOSURE_IS_NOT_THE_OPENING_OF_WHAT_IT_UNBLOCKS_NOTE,
    FATH_BARI_DIGITAL_WITNESS,
    FATH_BARI_WITNESS_LOCUS,
    FATH_BARI_WITNESS_PAGE_BRACKET,
    FATH_BARI_WITNESS_VOLUME,
    NAMED_RESIDUALS,
    QAYD_ATTRIBUTION_SCAN,
    DisqualifiedHit,
    QaydAttributionScan,
    SourceExhaustionStanding,
    derive_source_exhaustion,
    front_closure_condition_is_met,
    require_attested_fath_bari_excerpt,
)
from alghanem.arabic.lexical_transmission import (
    LEXICAL_CHAIN_MINIMUM_ATTRIBUTIONS,
    LexicalCitationStructure,
)
from alghanem.arabic.sentence_card_source_texts import (
    LocusVerification,
    SourceTextError,
)
from alghanem.arabic.transmission_standing import UnconstructibilityGenus

_COMPOSITION: Final = (
    Path(__file__).resolve().parents[2]
    / "examples"
    / "level_two_manat"
    / "ghanam_saima_composition.yaml"
)


def _composition_card() -> dict:
    return json.loads(_COMPOSITION.read_text(encoding="utf-8"))


def test_the_scan_ran_over_the_whole_source_not_over_one_chapter() -> None:
    """نطاقُ المسح كاملُ الكتاب، وهو مُصرَّحٌ به لا مُستنتَج."""

    statement = QAYD_ATTRIBUTION_SCAN.scope_statement

    assert "كاملُ الملفّ" in statement
    assert "لا كتابُ الزكاة وحده" in statement
    assert QAYD_ATTRIBUTION_SCAN.total_token_occurrences == 33
    assert QAYD_ATTRIBUTION_SCAN.scanned_tokens == ("سائمة", "السوم")


def test_the_source_is_exhausted_below_the_succession_threshold() -> None:
    """إسنادٌ واحدٌ دون عتبةِ التعاقب، فالموقفُ استنفادٌ لا بلوغ."""

    assert len(QAYD_ATTRIBUTION_SCAN.qualifying_attributions) == 1
    assert len(QAYD_ATTRIBUTION_SCAN.qualifying_attributions) < (
        LEXICAL_CHAIN_MINIMUM_ATTRIBUTIONS
    )
    assert derive_source_exhaustion(QAYD_ATTRIBUTION_SCAN) is (
        SourceExhaustionStanding.مستنفد_دون_عتبة_التعاقب
    )


def test_the_closure_condition_is_met_by_a_negative_result() -> None:
    """النتيجةُ السالبةُ التامّة تُغلِق الشرطَ كما تُغلِقه الموجبة."""

    assert front_closure_condition_is_met(QAYD_ATTRIBUTION_SCAN) is True
    assert derive_source_exhaustion(QAYD_ATTRIBUTION_SCAN) is not (
        SourceExhaustionStanding.مستنفد_ببلوغ_عتبة_التعاقب
    )


def test_closing_the_condition_does_not_open_the_lexical_path_front() -> None:
    """الإغلاقُ يرفع المانعَ ولا يفتح الجبهة؛ ولا أداةَ بُنيت لها هنا."""

    assert "ClosureIsNotTheOpeningOfWhatItUnblocks" in (
        CLOSURE_IS_NOT_THE_OPENING_OF_WHAT_IT_UNBLOCKS_NOTE
    )
    module = Path(__file__).resolve().parents[2] / (
        "src/alghanem/arabic/level_two_source_texts.py"
    )
    body = module.read_text(encoding="utf-8")
    assert "طريق_النقل_المعجمي" not in body.split('"""', 2)[2]


def test_every_disqualified_hit_is_named_with_its_ground() -> None:
    """المُستبعَدُ يُسمّى بموضعه وسلطته وعلّته، ولا يُطوى في رقمٍ مُجمَل."""

    assert len(QAYD_ATTRIBUTION_SCAN.disqualified_hits) == 2
    authorities = {
        hit.named_authority for hit in QAYD_ATTRIBUTION_SCAN.disqualified_hits
    }
    assert authorities == {"مجاهد", "أبو عبيدة"}
    for hit in QAYD_ATTRIBUTION_SCAN.disqualified_hits:
        assert hit.line_number > 0
        assert hit.disqualification.strip()
        assert hit.named_authority not in QAYD_ATTRIBUTION_SCAN.qualifying_attributions


def test_a_manufactured_second_attribution_is_refused() -> None:
    """مقطعٌ لا يقع فيه اسمُ سلطةٍ مُحتسَبة يُردّ، ولا يُبلَغ به حدٌّ عدديّ."""

    with pytest.raises(SourceTextError):
        require_attested_fath_bari_excerpt("قال ابن حجر والراجح اعتباره هنا")

    accepted = require_attested_fath_bari_excerpt(
        "قال الزين بن المنير حذف وصف الغنم بالسائمة"
    )
    assert "الزين بن المنير" in accepted


def test_the_card_excerpt_carries_the_qualifying_authority_verbatim() -> None:
    """مقطعُ البطاقة نفسُه يجتاز حدَّ الاحتواء الذي يردّ المصنوع."""

    excerpt = _composition_card()["طريق_النقل_المعجمي"]["الإسنادات"][0][
        "الاقتباس_المنقول"
    ]

    assert require_attested_fath_bari_excerpt(excerpt) == excerpt


def test_the_witness_names_a_print_edition_and_earns_the_middle_rank_only() -> None:
    """شاهدٌ يُرقّم على طبعةٍ مُسمّاة يبلغ الرتبةَ الوسطى، ولا يبلغ العليا."""

    assert "دار المعرفة" in FATH_BARI_DIGITAL_WITNESS.print_edition
    assert FATH_BARI_WITNESS_LOCUS is (
        LocusVerification.ترقيم_طبعة_مرمز_رقميا_غير_مقابل
    )
    assert FATH_BARI_WITNESS_LOCUS is not LocusVerification.مقابل_بنسخة_ورقية_محققة
    assert "PAPER_COLLATION_STILL_HAS_NO_ENTRY" in NAMED_RESIDUALS


def test_the_volume_is_settled_and_the_page_is_not() -> None:
    """المجلَّدُ ثابتٌ بطرفَي العلامتين، والصفحةُ مترجِّحةٌ لعُرفٍ لم يُتحقَّق منه."""

    assert FATH_BARI_WITNESS_VOLUME == 3
    assert FATH_BARI_WITNESS_PAGE_BRACKET == (317, 318)
    assert "PAGE_MILESTONE_CONVENTION_NOT_VERIFIED" in NAMED_RESIDUALS


def test_the_card_locus_is_not_overwritten_by_the_witness_locus() -> None:
    """رقمُ البطاقة باقٍ بحروفه؛ ورقمُ الشاهد يُكتَب إلى جانبه لا مكانَه."""

    card = _composition_card()

    assert "[ص: 372]" in card["طريق_النقل_المعجمي"]["الإسنادات"][0]["الموضع"]
    assert "317" not in json.dumps(card, ensure_ascii=False)
    assert "CARD_LOCUS_AND_WITNESS_LOCUS_ARE_TWO_EDITIONS" in NAMED_RESIDUALS


def test_exhaustion_changes_neither_the_stop_genus_nor_the_qayd_reading() -> None:
    """الاستنفادُ يُبيّن نهائيةَ الوقوف ولا يرفعه ولا يُبدّل جنسَه."""

    assert LevelTwoStopGenus.وقوف_آلة_لانقطاع_نقل_القيد in LevelTwoStopGenus
    assert QaydSignification.دلالة_القيد_غير_محسومة in QaydSignification
    assert LexicalCitationStructure.عنوان_واحد_مسطح in LexicalCitationStructure
    assert (
        UnconstructibilityGenus.REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH
        in UnconstructibilityGenus
    )
    assert "EXHAUSTION_DOES_NOT_CHANGE_THE_STOP_GENUS" in NAMED_RESIDUALS


def test_one_exhausted_source_is_not_an_exhausted_question() -> None:
    """حدُّ الدعوى مُسمًّى: كتابٌ واحدٌ استُنفِد، لا المسألةُ كلُّها."""

    residual = NAMED_RESIDUALS["ONE_EXHAUSTED_SOURCE_IS_NOT_AN_EXHAUSTED_QUESTION"]

    assert "ExhaustedSourceIsNotAnExhaustedWorld" in residual


def test_the_measurement_is_rederivable_from_a_named_file() -> None:
    """القياسُ مُثبَتٌ ببصمةٍ وحجم، لأنّ الكوربص غيرُ منقولٍ في الشجرة."""

    assert len(QAYD_ATTRIBUTION_SCAN.witness_sha256) == 64
    assert QAYD_ATTRIBUTION_SCAN.witness_byte_length == 32_917_581
    assert "CORPUS_IS_NOT_VENDORED_IN_THIS_TREE" in NAMED_RESIDUALS


def test_a_scan_with_more_counted_hits_than_occurrences_is_refused() -> None:
    """تصريحان متناقضان في قياسٍ واحدٍ يُردّان ولا يُرجَّح أحدهما صمتًا."""

    with pytest.raises(SourceTextError):
        QaydAttributionScan(
            witness=FATH_BARI_DIGITAL_WITNESS,
            witness_sha256=QAYD_ATTRIBUTION_SCAN.witness_sha256,
            witness_byte_length=1,
            scanned_tokens=("سائمة",),
            total_token_occurrences=0,
            qualifying_attributions=("الزين بن المنير",),
            disqualified_hits=(),
            scope_statement="بيان",
        )


def test_a_repeated_authority_does_not_make_a_succession() -> None:
    """تكرارُ سلطةٍ واحدةٍ لا يُبلَغ به التعاقب، فيُردّ عند الإنشاء."""

    with pytest.raises(SourceTextError):
        QaydAttributionScan(
            witness=FATH_BARI_DIGITAL_WITNESS,
            witness_sha256=QAYD_ATTRIBUTION_SCAN.witness_sha256,
            witness_byte_length=10,
            scanned_tokens=("سائمة",),
            total_token_occurrences=10,
            qualifying_attributions=("الزين بن المنير", "الزين بن المنير"),
            disqualified_hits=(),
            scope_statement="بيان",
        )


def test_a_disqualified_hit_without_a_ground_is_refused() -> None:
    """الاستبعادُ يُعلَّل، وإلّا صار انتقاءً صامتًا."""

    with pytest.raises(SourceTextError):
        DisqualifiedHit(
            line_number=1,
            excerpt="مقطع",
            named_authority="فلان",
            disqualification="   ",
        )
