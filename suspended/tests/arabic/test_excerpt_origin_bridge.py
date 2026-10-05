"""شواهدُ جسر منشأ المقتطف: تُصادم المقيسَ ولا تنقله، وتُمسِك العنوانَ باسمه."""

from __future__ import annotations

import unicodedata

import pytest

from alghanem.arabic.excerpt_origin_bridge import (
    THE_ADDRESS_WITHOUT_A_SOURCE_IS_NOT_AN_IDENTITY,
    THE_PRIOR_AUDIT,
    THE_SEARCH_LIST,
    THE_THIRD_CLAIM_IS_NEVER_DERIVED_FROM_THE_FIRST_TWO,
    ClaimStanding,
    ExcerptOriginError,
    OriginClaim,
    OriginWitness,
    SourceStanding,
    TextSource,
    WordAddress,
    address_collisions,
    decode_audit,
    locate,
    origin_readings,
    prior_audit_standing,
    source_by_key,
    source_reading,
    transferable_context,
)

THE_PHRASE = "\u062d\u064e\u064a\u064e\u0627\u0629\u064c"
THE_ADDRESS = WordAddress("QURAN_SIMPLE", 186, 4)


def test_every_declared_source_is_sealed_and_present() -> None:
    """الأختامُ تُصادَم بالمقيس من القرص، ولا تُقرأ من حقلٍ مكتوب."""

    for source in THE_SEARCH_LIST:
        reading = source_reading(source)
        assert reading.standing is SourceStanding.SEALED_AND_PRESENT
        assert reading.measured_sha256 == source.declared_sha256
        assert reading.measured_byte_length == source.declared_byte_length


def test_a_lenient_decode_is_measured_not_assumed() -> None:
    """أثرُ الفكّ المتسامح يُقاس على هذه البايتات، ولا يُعمَّم ترخيصًا."""

    for source in THE_SEARCH_LIST:
        audit = decode_audit(source)
        assert audit.lenient_would_hide is False
        assert audit.characters_dropped_by_lenient == 0


def test_a_decode_policy_without_strict_is_refused() -> None:
    """سياسةُ فكٍّ لا تذكر الصرامةَ تُرَدّ عند البناء لا عند الاستعمال."""

    with pytest.raises(ExcerptOriginError):
        TextSource(
            key="X",
            title="t",
            edition="e",
            relative_path="corpora/quran-simple-enhanced.txt",
            declared_byte_length=1,
            declared_sha256="0" * 64,
            decode_policy="utf-8 errors=ignore",
            normalization_policy="بلا تطبيع",
            line_policy="\\n",
        )


def test_a_bare_address_resolves_to_a_different_word_in_each_source() -> None:
    """العنوانُ بلا مفتاح مصدرٍ إزاحةٌ لا هويّة؛ وهذا قياسٌ لا دعوى."""

    collisions = address_collisions(329, 3)
    assert len(collisions) == len(THE_SEARCH_LIST)
    surfaces = {surface for _, surface in collisions}
    assert THE_PHRASE not in surfaces
    assert len(surfaces) == 1, THE_ADDRESS_WITHOUT_A_SOURCE_IS_NOT_AN_IDENTITY


def test_the_prior_audit_material_is_absent_and_its_absence_is_named() -> None:
    """غيابُ مادّة التدقيق يُسجَّل بأسماء ما بُحث عنه، لا بوصفٍ مرسَل."""

    standing = prior_audit_standing()
    assert standing.archive_present is False
    assert standing.is_reproducible is False
    assert THE_PRIOR_AUDIT.archive_name.endswith(".zip")


def test_the_same_phrase_lives_in_two_sources_at_different_offsets() -> None:
    """العبارةُ نفسُها في مصدرَين بإزاحتَين مختلفتَين، فالسياقُ ليس خاصّتَها."""

    first = locate(WordAddress("QURAN_SIMPLE", 186, 4))
    second = locate(WordAddress("GLOBALQURAN_SIMPLE", 186, 4))
    assert first.surface == second.surface == THE_PHRASE
    assert first.char_offset != second.char_offset


def test_uniqueness_is_relative_to_the_declared_list() -> None:
    """التفرّدُ صفةُ موضعٍ في قائمةٍ مُعلَنة، فيَسقط بتوسيع القائمة وحدَها."""

    readings = origin_readings(THE_PHRASE)
    unique = next(
        one for one in readings if one.claim is OriginClaim.UNIQUE_IN_THE_SEARCH_LIST
    )
    assert unique.standing is ClaimStanding.REFUTED
    single = origin_readings(THE_PHRASE, sources=(source_by_key("QURAN_SIMPLE"),))
    unique_single = next(
        one for one in single if one.claim is OriginClaim.UNIQUE_IN_THE_SEARCH_LIST
    )
    assert unique_single.standing is ClaimStanding.ESTABLISHED


def test_the_third_claim_is_never_derived_from_the_first_two() -> None:
    """الوجدانُ والتفرّدُ لا يُنتجان المنشأ؛ تبقى الثالثةُ معلَّقةً بلا شهادة."""

    readings = origin_readings(THE_PHRASE, sources=(source_by_key("QURAN_SIMPLE"),))
    found = next(
        one for one in readings if one.claim is OriginClaim.PRESENT_IN_A_SOURCE
    )
    origin = next(
        one for one in readings if one.claim is OriginClaim.IS_THE_ORIGIN_OF_THE_EXCERPT
    )
    assert found.standing is ClaimStanding.ESTABLISHED
    assert origin.standing is ClaimStanding.SUSPENDED
    assert THE_THIRD_CLAIM_IS_NEVER_DERIVED_FROM_THE_FIRST_TWO in origin.evidence


def test_a_correct_source_with_a_wrong_offset_is_refuted_not_suspended() -> None:
    """مصدرٌ صحيحٌ بموضعٍ خاطئ يُرَدّ بدليلٍ، ولا يُخلَط بغياب الشهادة."""

    witness = OriginWitness(
        dataset_id="D",
        dataset_line_id="L",
        source_key="QURAN_SIMPLE",
        source_char_offset=999_999,
        method="m",
        examiner="e",
    )
    origin = next(
        one
        for one in origin_readings(THE_PHRASE, witnesses=(witness,))
        if one.claim is OriginClaim.IS_THE_ORIGIN_OF_THE_EXCERPT
    )
    assert origin.standing is ClaimStanding.REFUTED


def test_an_established_origin_moves_with_the_witness_and_falls_without_it() -> None:
    """الشهادةُ تُثبِت المنشأ، وسحبُها يُعيده معلَّقًا لا ممتنعًا."""

    located = locate(THE_ADDRESS)
    witness = OriginWitness(
        dataset_id="D",
        dataset_line_id="L186:W4",
        source_key="QURAN_SIMPLE",
        source_char_offset=located.char_offset,
        method="m",
        examiner="e",
    )
    with_it = next(
        one
        for one in origin_readings(THE_PHRASE, witnesses=(witness,))
        if one.claim is OriginClaim.IS_THE_ORIGIN_OF_THE_EXCERPT
    )
    without = next(
        one
        for one in origin_readings(THE_PHRASE)
        if one.claim is OriginClaim.IS_THE_ORIGIN_OF_THE_EXCERPT
    )
    assert with_it.standing is ClaimStanding.ESTABLISHED
    assert without.standing is ClaimStanding.SUSPENDED


def test_context_is_never_transferred_to_an_unproven_excerpt() -> None:
    """لا يُنقَل سياقٌ إلى مقتطفٍ لم يَثبُت منشؤه؛ يُرفَع الخطأُ ولا يُبتلَع."""

    with pytest.raises(ExcerptOriginError):
        transferable_context(origin_readings(THE_PHRASE), locate(THE_ADDRESS))


def test_an_address_beyond_the_source_is_refused_by_measurement() -> None:
    """ما لا تحتمله البايتاتُ يُرَدّ بعدد أسطرها لا بتخمين."""

    with pytest.raises(ExcerptOriginError):
        locate(WordAddress("QURAN_SIMPLE", 10**7, 1))
    with pytest.raises(ExcerptOriginError):
        locate(WordAddress("QURAN_SIMPLE", 186, 10**4))


def test_a_surface_is_compared_verbatim_and_never_folded_silently() -> None:
    """الطيُّ يُسمّى ولا يُجرى: غائبٌ بحرفه حاضرٌ بالطيّ يُرفَع به الخطأ."""

    verbatim = locate(WordAddress("QURAN_SIMPLE", 186, 7)).surface
    assert origin_readings(verbatim)[0].standing is ClaimStanding.ESTABLISHED
    stored = "\u0634\u0651\u064e"
    canonical = unicodedata.normalize("NFC", stored)
    assert canonical != stored
    assert origin_readings(stored)[0].standing is ClaimStanding.ESTABLISHED
    with pytest.raises(ExcerptOriginError):
        origin_readings(canonical)
