"""أدواتُ التوليد الثلاث: مجالٌ حصريٌّ لكلّ أداة، وحكمُ الخروج عن اللغة بجهة الأخذ.

الاختبارُ هنا يُثبِت خمسةَ أشياء: أنّ لكلّ أداةٍ مجالًا واحدًا لا يشاركها فيه
غيرُها، وأنّ الموقفَ مُشتَقٌّ من جهة الأخذ وحدها لا من التوزيع ولا من الأداة،
وأنّ `غير_محسوم` لا يُحمَل على أحد الطرفين، وأنّ الشواهدَ المنقولةَ مُغلَقةٌ
مُسمّاةٌ ببقاياها، وأنّ نفيَ الحقائق الثلاث مقروءٌ في حروف المنقول لا مُشتَقٌّ
من `HaqiqaGenus`.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.lafz_madlul_relation_formal import HaqiqaGenus
from alghanem.arabic.tawlid_lafzi import (
    CITED_LEXEME_WITNESSES,
    TOOL_EXCLUSIVE_DOMAIN,
    CitedLexemeWitness,
    ForeignBorrowingMode,
    GeneratedContentKind,
    GeneratedLexemeStanding,
    LafzGenerationTool,
    TawlidLafziError,
    cited_lexeme_witness_for,
    required_tool_for,
    standing_for_borrowing_mode,
    tool_domain,
)
from alghanem.arabic.usul_section_source_texts import (
    OUTSIDE_THE_LANGUAGE_EXCERPT,
    require_attested_section_excerpt,
)


def test_each_tool_has_exactly_one_exclusive_domain() -> None:
    assert len(TOOL_EXCLUSIVE_DOMAIN) == len(LafzGenerationTool)
    assert set(TOOL_EXCLUSIVE_DOMAIN.values()) == set(GeneratedContentKind)
    assert (
        tool_domain(LafzGenerationTool.TARIB)
        is GeneratedContentKind.THING_OR_PROPER_NAME
    )
    assert tool_domain(LafzGenerationTool.ISHTIQAQ) is GeneratedContentKind.MEANING
    assert tool_domain(LafzGenerationTool.MAJAZ) is GeneratedContentKind.IMAGINATION


def test_the_content_kind_determines_the_required_tool_not_the_reverse() -> None:
    for tool, kind in TOOL_EXCLUSIVE_DOMAIN.items():
        assert required_tool_for(kind) is tool


def test_a_value_outside_the_closed_vocabularies_is_refused() -> None:
    with pytest.raises(TawlidLafziError, match="الأداةُ عضوٌ"):
        tool_domain("تعريب")  # type: ignore[arg-type]
    with pytest.raises(TawlidLafziError, match="نوعُ المحتوى عضوٌ"):
        required_tool_for("معنى")  # type: ignore[arg-type]
    with pytest.raises(TawlidLafziError, match="جهةُ الأخذ عضوٌ"):
        standing_for_borrowing_mode("غير_محسوم")  # type: ignore[arg-type]


def test_the_standing_follows_the_borrowing_mode_alone() -> None:
    assert (
        standing_for_borrowing_mode(ForeignBorrowingMode.LAFZ_TAKEN_AND_SHAPED)
        is GeneratedLexemeStanding.ARABIC_BY_CORRECT_TARIB
    )
    assert (
        standing_for_borrowing_mode(ForeignBorrowingMode.MEANING_TAKEN_WITH_ALIEN_ROOT)
        is GeneratedLexemeStanding.OUTSIDE_THE_LANGUAGE
    )


def test_an_undecided_borrowing_mode_is_never_coerced_to_either_side() -> None:
    assert (
        standing_for_borrowing_mode(ForeignBorrowingMode.UNDECIDED)
        is GeneratedLexemeStanding.UNDECIDED
    )
    witness = CitedLexemeWitness(
        lafz="لفظٌ لم تُعرَف جهةُ أخذه",
        arabic_root_note="لم يُذكَر أصلُه",
        content_kind=GeneratedContentKind.THING_OR_PROPER_NAME,
        tool_used=LafzGenerationTool.TARIB,
        borrowing_mode=ForeignBorrowingMode.UNDECIDED,
        named_residuals=("SECTION_SOURCE_BOOK_IS_NOT_NAMED",),
    )
    assert witness.standing is GeneratedLexemeStanding.UNDECIDED


def test_correct_tarib_of_a_thing_keeps_the_lexeme_arabic() -> None:
    witness = CitedLexemeWitness(
        lafz="فلسفة",
        arabic_root_note="أُخِذ اللفظُ الأعجميُّ نفسُه فصِيغ على وزنٍ عربيّ",
        content_kind=GeneratedContentKind.THING_OR_PROPER_NAME,
        tool_used=LafzGenerationTool.TARIB,
        borrowing_mode=ForeignBorrowingMode.LAFZ_TAKEN_AND_SHAPED,
        named_residuals=("SECTION_SOURCE_BOOK_IS_NOT_NAMED",),
    )
    assert witness.standing is GeneratedLexemeStanding.ARABIC_BY_CORRECT_TARIB
    assert witness.tool_matches_its_domain


def test_the_cited_lexemes_are_exactly_the_five_the_source_named() -> None:
    assert tuple(CITED_LEXEME_WITNESSES) == (
        "هاتف",
        "سيارة",
        "قطار",
        "عربة",
        "مقود",
    )
    with pytest.raises(TawlidLafziError, match="لا شاهدَ منقولًا"):
        cited_lexeme_witness_for("تلفون")


def test_every_cited_lexeme_mixed_the_tools_and_fell_outside_the_language() -> None:
    for witness in CITED_LEXEME_WITNESSES.values():
        assert witness.content_kind is GeneratedContentKind.THING_OR_PROPER_NAME
        assert witness.tool_used is LafzGenerationTool.ISHTIQAQ
        assert not witness.tool_matches_its_domain
        assert witness.standing is GeneratedLexemeStanding.OUTSIDE_THE_LANGUAGE
        assert "CITED_LEXEMES_ARE_NOT_VOCABULARY_ROWS" in witness.named_residuals
        assert "SECTION_SOURCE_BOOK_IS_NOT_NAMED" in witness.named_residuals


def test_a_witness_without_a_named_residual_is_refused() -> None:
    with pytest.raises(TawlidLafziError, match="بلا بقيّةٍ مُسمّاةٍ واحدة"):
        CitedLexemeWitness(
            lafz="لفظ",
            arabic_root_note="بيان",
            content_kind=GeneratedContentKind.MEANING,
            tool_used=LafzGenerationTool.ISHTIQAQ,
            borrowing_mode=ForeignBorrowingMode.UNDECIDED,
            named_residuals=(),
        )
    with pytest.raises(TawlidLafziError, match="اللفظ نصٌّ غير فارغ"):
        CitedLexemeWitness(
            lafz="  ",
            arabic_root_note="بيان",
            content_kind=GeneratedContentKind.MEANING,
            tool_used=LafzGenerationTool.ISHTIQAQ,
            borrowing_mode=ForeignBorrowingMode.UNDECIDED,
            named_residuals=("SECTION_SOURCE_BOOK_IS_NOT_NAMED",),
        )


def test_the_three_haqiqa_genera_are_read_in_the_quotation_not_derived() -> None:
    for genus in HaqiqaGenus:
        require_attested_section_excerpt("OUTSIDE_THE_LANGUAGE_EXCERPT", genus.value)
    assert (
        "لا تُعتبر من ألفاظ اللغة العربية" in OUTSIDE_THE_LANGUAGE_EXCERPT.verbatim_text
    )


def test_the_standing_is_not_stored_in_any_field() -> None:
    names = set(CitedLexemeWitness.__dataclass_fields__)
    assert "standing" not in names
    for token in ("result", "outcome", "verdict", "birth", "certificate"):
        assert not any(token in name.lower() for name in names)
