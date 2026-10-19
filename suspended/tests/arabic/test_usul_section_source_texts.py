"""موادُّ القسم المُزوَّد: ما نُقِل بحروفه يُفحَص، وما وُصِف لا يُحمَل نصًّا.

الاختبارُ هنا يُثبِت أربعةَ أشياء: أنّ المفروزَ بجنس التزويد لا يُخلَط، وأنّ
موضعَ كلّ مادّةٍ `موضع_غير_متحقق` لأنّ كتابَ القسم لم يُسَمَّ، وأنّ الفحصَ
بالاحتواء لا يجري إلّا على المنقول بحروفه، وأنّ النقلَ لا يُغيِّر موقفَ بندٍ
واحدٍ في بطاقة الجملة ولا مفردةً مُجمَّدةً في هذه الطبقة.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.comprehension_defect import (
    PRIORITY_LADDER_ARGUMENTS_ARE_PARAPHRASE_NOT_TRANSCRIPTION,
    ComprehensionDefectCause,
    compare_defect_priority,
    priority_argument,
)
from alghanem.arabic.sentence_card_preregistration import (
    SENTENCE_CARD_PREREGISTRATION,
    CardItem,
    ItemStanding,
)
from alghanem.arabic.sentence_card_source_texts import LocusVerification
from alghanem.arabic.usul_section_source_texts import (
    DAWR_PROOF_FOR_INSHA,
    DESCRIBED_SECTION_MATERIAL,
    MURADIF_EXAMPLES_FARD_AND_HARAM,
    MUSHTARAK_EXAMPLE_TAHUR,
    MUTAWATI_EXAMPLE_HAJJ,
    OUTSIDE_THE_LANGUAGE_EXCERPT,
    PRIORITY_LADDER_EXCERPT,
    SECTION_EXCERPTS,
    TAWLID_TOOLS_DOMAIN_EXCERPT,
    DescribedSectionMaterial,
    SectionExcerpt,
    SectionMaterialStanding,
    SectionTextError,
    described_material_for,
    require_attested_section_excerpt,
    section_excerpt_for,
)


def _excerpt(**changes: object) -> SectionExcerpt:
    base: dict[str, object] = {
        "key": "K",
        "verbatim_text": "حروفٌ منقولة",
        "corroborated_terms": ("موضعٌ مُسمًّى",),
        "locus_statement": "موضعٌ مُسمًّى",
        "locus_verification": LocusVerification.موضع_غير_متحقق,
        "named_residuals": ("SECTION_SOURCE_BOOK_IS_NOT_NAMED",),
    }
    base.update(changes)
    return SectionExcerpt(**base)  # type: ignore[arg-type]


def _described(**changes: object) -> DescribedSectionMaterial:
    base: dict[str, object] = {
        "key": "K",
        "description": "وصفٌ بلا حروفٍ منقولة",
        "related_terms": ("موضعٌ مُسمًّى",),
        "named_residuals": (
            "SECTION_SOURCE_BOOK_IS_NOT_NAMED",
            "MATERIAL_IS_DESCRIBED_NOT_TRANSCRIBED",
        ),
    }
    base.update(changes)
    return DescribedSectionMaterial(**base)  # type: ignore[arg-type]


def test_the_two_registries_are_exactly_their_declared_members() -> None:
    assert tuple(SECTION_EXCERPTS) == (
        "PRIORITY_LADDER_EXCERPT",
        "TAWLID_TOOLS_DOMAIN_EXCERPT",
        "OUTSIDE_THE_LANGUAGE_EXCERPT",
    )
    assert tuple(DESCRIBED_SECTION_MATERIAL) == (
        "DAWR_PROOF_FOR_INSHA",
        "MUTAWATI_EXAMPLE_HAJJ",
        "MUSHTARAK_EXAMPLE_TAHUR",
        "MURADIF_EXAMPLES_FARD_AND_HARAM",
    )
    assert section_excerpt_for("PRIORITY_LADDER_EXCERPT") is PRIORITY_LADDER_EXCERPT
    assert described_material_for("DAWR_PROOF_FOR_INSHA") is DAWR_PROOF_FOR_INSHA


def test_the_two_standings_are_never_the_same_genus() -> None:
    for excerpt in SECTION_EXCERPTS.values():
        assert excerpt.standing is SectionMaterialStanding.منقول_بحروفه
    for material in DESCRIBED_SECTION_MATERIAL.values():
        assert material.standing is SectionMaterialStanding.موصوف_بلا_نقل_حرفي
    assert len(SectionMaterialStanding) == 2


def test_an_unregistered_key_is_refused_and_not_read_across_registries() -> None:
    with pytest.raises(SectionTextError, match="لا نصَّ منقولًا"):
        section_excerpt_for("DAWR_PROOF_FOR_INSHA")
    with pytest.raises(SectionTextError, match="لا مادّةَ موصوفةً"):
        described_material_for("PRIORITY_LADDER_EXCERPT")


def test_every_locus_is_unverified_because_the_book_was_never_named() -> None:
    for excerpt in SECTION_EXCERPTS.values():
        assert excerpt.locus_verification is LocusVerification.موضع_غير_متحقق
        assert "SECTION_SOURCE_BOOK_IS_NOT_NAMED" in excerpt.named_residuals
    for material in DESCRIBED_SECTION_MATERIAL.values():
        assert "SECTION_SOURCE_BOOK_IS_NOT_NAMED" in material.named_residuals


def test_a_locus_may_not_be_raised_above_unverified_here() -> None:
    with pytest.raises(SectionTextError, match="لا يُرفَع عن"):
        _excerpt(locus_verification=LocusVerification.ترقيم_طبعة_مرمز_رقميا_غير_مقابل)
    with pytest.raises(SectionTextError, match="لا يُرفَع عن"):
        _excerpt(locus_verification=LocusVerification.مقابل_بنسخة_ورقية_محققة)


def test_a_material_without_its_naming_residual_is_refused() -> None:
    with pytest.raises(SectionTextError, match="SECTION_SOURCE_BOOK_IS_NOT_NAMED"):
        _excerpt(named_residuals=("OTHER",))
    with pytest.raises(SectionTextError, match="MATERIAL_IS_DESCRIBED_NOT_TRANSCRIBED"):
        _described(named_residuals=("SECTION_SOURCE_BOOK_IS_NOT_NAMED",))
    with pytest.raises(SectionTextError, match="بلا بقيّةٍ مُسمّاةٍ واحدة"):
        _excerpt(named_residuals=())


def test_a_material_that_names_no_locus_of_this_layer_is_refused() -> None:
    with pytest.raises(SectionTextError, match="لا يُعاضِد موضعًا واحدًا"):
        _excerpt(corroborated_terms=())
    with pytest.raises(SectionTextError, match="موضعٌ مكرَّر"):
        _excerpt(corroborated_terms=("أ", "أ"))
    with pytest.raises(SectionTextError, match="لا تُسمّي موضعًا واحدًا"):
        _described(related_terms=())


def test_the_ladder_excerpt_carries_the_naql_over_ishtirak_comparison() -> None:
    assert (
        require_attested_section_excerpt(
            "PRIORITY_LADDER_EXCERPT", "النقل أولى من الاشتراك"
        )
        == "النقل أولى من الاشتراك"
    )
    require_attested_section_excerpt("PRIORITY_LADDER_EXCERPT", "الاشتراك أضعف الجميع")
    assert PRIORITY_LADDER_EXCERPT.corroborated_terms == (
        ComprehensionDefectCause.ISHTIRAK.value,
        ComprehensionDefectCause.NAQL.value,
    )


def test_the_transcribed_comparison_agrees_with_the_recorded_rank() -> None:
    assert (
        compare_defect_priority(
            ComprehensionDefectCause.NAQL, ComprehensionDefectCause.ISHTIRAK
        )
        == -1
    )
    argument = priority_argument(
        ComprehensionDefectCause.NAQL, ComprehensionDefectCause.ISHTIRAK
    )
    assert argument.verdict == "النقل أولى"


def test_only_one_of_the_ten_comparisons_was_transcribed() -> None:
    transcribed = 0
    for first in ComprehensionDefectCause:
        for second in ComprehensionDefectCause:
            if first is second:
                continue
            verdict = priority_argument(first, second).verdict
            try:
                require_attested_section_excerpt("PRIORITY_LADDER_EXCERPT", verdict)
            except SectionTextError:
                continue
            transcribed += 1
    assert transcribed == 2  # النقل أولى، في الاتجاهين
    assert (
        "PRIORITY_LADDER_ARGUMENTS_ARE_PARAPHRASE_NOT_TRANSCRIPTION"
        in PRIORITY_LADDER_ARGUMENTS_ARE_PARAPHRASE_NOT_TRANSCRIPTION
    )
    assert (
        "usul_section_source_texts"
        in PRIORITY_LADDER_ARGUMENTS_ARE_PARAPHRASE_NOT_TRANSCRIPTION
    )


def test_a_quotation_not_in_the_excerpt_is_refused_not_paraphrased() -> None:
    with pytest.raises(SectionTextError, match="لا يقع حرفُه"):
        require_attested_section_excerpt(
            "PRIORITY_LADDER_EXCERPT", "التخصيص أولى من المجاز"
        )
    with pytest.raises(SectionTextError, match="الاقتباسُ نصٌّ غير فارغ"):
        require_attested_section_excerpt("PRIORITY_LADDER_EXCERPT", "  ")


def test_the_described_material_is_not_reachable_by_containment_check() -> None:
    with pytest.raises(SectionTextError, match="لا نصَّ منقولًا"):
        require_attested_section_excerpt("DAWR_PROOF_FOR_INSHA", "طلقتك")
    assert not hasattr(DAWR_PROOF_FOR_INSHA, "verbatim_text")


def test_the_dawr_material_leaves_the_khabar_insha_item_untouched() -> None:
    standing = SENTENCE_CARD_PREREGISTRATION.registration_for(
        CardItem.KHABAR_INSHA
    ).standing
    assert standing is ItemStanding.SOURCE_TEXT_SUPPLIED_WITHOUT_CERTIFICATE
    assert (
        "KHABAR_INSHA_ITEM_STANDING_IS_UNCHANGED_BY_THIS_MATERIAL"
        in DAWR_PROOF_FOR_INSHA.named_residuals
    )
    assert DAWR_PROOF_FOR_INSHA.related_terms == (CardItem.KHABAR_INSHA.value,)


def test_the_sevenfold_examples_name_their_own_unclosed_remainders() -> None:
    assert MUTAWATI_EXAMPLE_HAJJ.related_terms == ("متواطئ",)
    assert MUSHTARAK_EXAMPLE_TAHUR.related_terms == ("مشترك",)
    assert MURADIF_EXAMPLES_FARD_AND_HARAM.related_terms == ("مترادف",)
    assert (
        "INITIAL_ASSIGNMENT_FOR_EACH_MEANING_IS_NOT_EVIDENCED_HERE"
        in MUSHTARAK_EXAMPLE_TAHUR.named_residuals
    )
    assert (
        "TENSION_WITH_MURADIF_PRESUMPTION_IS_RECORDED_NOT_RESOLVED"
        in MURADIF_EXAMPLES_FARD_AND_HARAM.named_residuals
    )


def test_the_two_generation_excerpts_carry_the_words_they_are_cited_for() -> None:
    require_attested_section_excerpt(
        "TAWLID_TOOLS_DOMAIN_EXCERPT", "التعريب خاص بأسماء الأشياء"
    )
    require_attested_section_excerpt(
        "OUTSIDE_THE_LANGUAGE_EXCERPT", "فلا تكون عربية على الإطلاق"
    )
    assert TAWLID_TOOLS_DOMAIN_EXCERPT.corroborated_terms == (
        "تعريب",
        "اشتقاق",
        "مجاز",
    )
    assert OUTSIDE_THE_LANGUAGE_EXCERPT.corroborated_terms == (
        "شرعية",
        "عرفية",
        "لغوية",
    )


def test_no_material_carries_a_result_bearing_field() -> None:
    for declaring_type in (SectionExcerpt, DescribedSectionMaterial):
        names = {field.name for field in declaring_type.__dataclass_fields__.values()}
        for token in ("result", "outcome", "verdict", "birth", "certificate"):
            assert not any(token in name.lower() for name in names)
