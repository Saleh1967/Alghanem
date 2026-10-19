"""اختباراتُ الناسخ والمنسوخ: أكثرُها في ما **لم** يقع، لا في ما وقع."""

from __future__ import annotations

import pytest

from alghanem.arabic.naskh_mansukh import (
    IBTAL_IS_NOT_BUTLAN_NOTE,
    NAMED_RESIDUALS,
    NASKH_DEFINITION,
    TILAWA_ABROGATION_AS_TRANSMITTED,
    NaskhCandidate,
    NaskhMansukhError,
    NaskhOutcome,
    NaskhVenue,
    RankAdmission,
    RulingGenus,
    Taraakhi,
    TilawaAbrogationStanding,
    TimeBinding,
    derive_naskh,
    derive_rank_admission,
)
from alghanem.arabic.transmission_standing import TransmissionStanding
from alghanem.arabic.usul_dalala_sections import (
    SECTION_MODULES,
    DalalaSection,
    SectionCoding,
    read_sections,
)


def _candidate(**overrides: object) -> NaskhCandidate:
    base: dict[str, object] = {
        "ruling_genus": RulingGenus.شرعي,
        "taraakhi": Taraakhi.متراخ,
        "time_binding": TimeBinding.غير_مقيد_بوقت,
        "venue": NaskhVenue.قرآن,
        "mansukh_standing": TransmissionStanding.MUTAWATIR,
        "nasikh_standing": TransmissionStanding.MUTAWATIR,
    }
    base.update(overrides)
    return NaskhCandidate(**base)  # type: ignore[arg-type]


def test_three_conditions_together_yield_naskh() -> None:
    assert derive_naskh(_candidate()) is NaskhOutcome.ينسخ


def test_each_condition_alone_blocks_naskh() -> None:
    """كلُّ شرطٍ من الثلاثة كافٍ وحدَه لمنع النسخ؛ فالاجتماعُ مطلوبٌ لا أكثريّته."""

    assert (
        derive_naskh(_candidate(ruling_genus=RulingGenus.غير_شرعي))
        is NaskhOutcome.لا_نسخ
    )
    assert derive_naskh(_candidate(taraakhi=Taraakhi.غير_متراخ)) is NaskhOutcome.لا_نسخ
    assert (
        derive_naskh(_candidate(time_binding=TimeBinding.مقيد_بوقت_معين))
        is not NaskhOutcome.ينسخ
    )


def test_unknown_chronology_is_not_read_as_succession() -> None:
    """الجهلُ بالتراخي لا يُقرأ تراخيًا؛ وإلا أُثبِت نسخٌ بلا تاريخ."""

    assert derive_naskh(_candidate(taraakhi=Taraakhi.غير_معلوم)) is NaskhOutcome.لا_نسخ


def test_expiry_is_a_genus_of_its_own_not_a_failed_naskh() -> None:
    """انقضاءُ الوقت ليس نسخًا لم يستوفِ شروطَه، بل ما لا نسخَ فيه أصلًا."""

    outcome = derive_naskh(_candidate(time_binding=TimeBinding.مقيد_بوقت_معين))
    assert outcome is NaskhOutcome.انتهاء_وقت_لا_نسخ
    assert outcome is not NaskhOutcome.لا_نسخ


def test_expiry_precedes_the_other_conditions() -> None:
    """المقيَّدُ بوقتٍ يُخرَج من الباب ولو اختلّ معه شرطٌ آخر، فلا يُبتلَع جنسُه."""

    outcome = derive_naskh(
        _candidate(
            time_binding=TimeBinding.مقيد_بوقت_معين,
            ruling_genus=RulingGenus.غير_شرعي,
            taraakhi=Taraakhi.غير_متراخ,
        )
    )
    assert outcome is NaskhOutcome.انتهاء_وقت_لا_نسخ


def test_mutawatir_is_not_abrogated_by_ahad() -> None:
    assert (
        derive_rank_admission(TransmissionStanding.MUTAWATIR, TransmissionStanding.AHAD)
        is RankAdmission.مردود_بنزول_الرتبة
    )
    assert (
        derive_naskh(_candidate(nasikh_standing=TransmissionStanding.AHAD))
        is NaskhOutcome.لا_نسخ
    )


def test_ahad_may_abrogate_ahad_and_mutawatir_may_abrogate_ahad() -> None:
    """الردُّ منوطٌ بنزول الرتبة لا بكون الناسخ آحادًا في نفسه."""

    assert (
        derive_rank_admission(TransmissionStanding.AHAD, TransmissionStanding.AHAD)
        is RankAdmission.الرتبة_قائمة
    )
    assert (
        derive_rank_admission(TransmissionStanding.AHAD, TransmissionStanding.MUTAWATIR)
        is RankAdmission.الرتبة_قائمة
    )


def test_fard_is_refused_by_its_own_ground_not_by_rank_descent() -> None:
    """الفرضُ ليس رتبةً أدنى، بل خارجَ السلَّم؛ وعلّتُه غيرُ علّة الآحاد."""

    for pair in (
        (TransmissionStanding.MUTAWATIR, TransmissionStanding.FARD),
        (TransmissionStanding.FARD, TransmissionStanding.MUTAWATIR),
        (TransmissionStanding.AHAD, TransmissionStanding.FARD),
    ):
        admission = derive_rank_admission(*pair)
        assert admission is RankAdmission.مردود_بأن_الفرض_ليس_مقيسا
        assert admission is not RankAdmission.مردود_بنزول_الرتبة


def test_tilawa_is_recorded_as_unestablished_not_as_impossible() -> None:
    """«لم يثبت بالقطعيّ» سالبةُ ثبوتٍ لا سالبةُ إمكان."""

    assert TILAWA_ABROGATION_AS_TRANSMITTED is (
        TilawaAbrogationStanding.لم_يثبت_بالقطعي
    )
    assert TILAWA_ABROGATION_AS_TRANSMITTED is not TilawaAbrogationStanding.ممتنع
    assert TILAWA_ABROGATION_AS_TRANSMITTED is not TilawaAbrogationStanding.واقع
    assert len(TilawaAbrogationStanding) == 3


def test_no_field_describes_the_abrogated_ruling_as_defective() -> None:
    """`IbtalIsNotButlan`: النسخُ رفعُ حكمٍ صحيح، لا كشفٌ عن فساده."""

    names = set(NaskhCandidate.__dataclass_fields__)
    for forbidden in ("batil", "invalid", "corrupt", "weak", "defect"):
        assert not any(forbidden in name.lower() for name in names)
    assert "الإبطالُ" in IBTAL_IS_NOT_BUTLAN_NOTE


def test_no_written_outcome_field_exists() -> None:
    """النتيجةُ تُشتَقّ ولا تُكتَب، فلا حقلَ يُخالِف المُشتَقّ."""

    names = set(NaskhCandidate.__dataclass_fields__)
    for forbidden in ("result", "outcome", "verdict", "naskh_occurred"):
        assert not any(forbidden in name.lower() for name in names)


def test_free_text_is_refused_in_place_of_a_closed_member() -> None:
    with pytest.raises(NaskhMansukhError):
        _candidate(ruling_genus="شرعي")
    with pytest.raises(NaskhMansukhError):
        _candidate(time_binding="غير_مقيد_بوقت")
    with pytest.raises(NaskhMansukhError):
        derive_naskh("مرشح")  # type: ignore[arg-type]


def test_candidate_is_frozen() -> None:
    candidate = _candidate()
    with pytest.raises(Exception):
        candidate.taraakhi = Taraakhi.غير_متراخ  # type: ignore[misc]


def test_venue_is_declared_and_does_not_change_the_outcome() -> None:
    """المحلُّ مُصرَّحٌ لا مُشتَقّ، ولا تدّعي الوحدةُ حكمًا في النسخ عبر المحلَّين."""

    assert derive_naskh(_candidate(venue=NaskhVenue.سنة)) is NaskhOutcome.ينسخ
    assert "VENUE_IS_DECLARED_NOT_DERIVED" in NAMED_RESIDUALS
    assert "CROSS_VENUE_NASKH_IS_NOT_ADDRESSED" in NAMED_RESIDUALS


def test_supplied_wording_gap_is_named_not_absorbed() -> None:
    assert "NASKH_WORDING_IS_SUPPLIED_NOT_COLLATED" in NAMED_RESIDUALS
    assert "EXTRACTED_LINE_NUMBERS_ARE_NOT_PRINT_PAGINATION" in NAMED_RESIDUALS
    assert "إبطالُ الحكم" in NASKH_DEFINITION


def test_transmission_ladder_is_imported_not_rebuilt() -> None:
    """السلَّمُ مقروءٌ من `transmission_standing`، فلا مفردةَ رتبٍ ثانيةٌ هنا."""

    import alghanem.arabic.naskh_mansukh as module

    assert module.TransmissionStanding is TransmissionStanding


def test_section_coverage_is_read_from_the_tree_not_declared() -> None:
    """القسمُ الخامسُ صار `مُرمَّز` لأنّ وحدتَه في الشجرة، لا لأنّ جدولاً قال ذلك."""

    assert SECTION_MODULES[DalalaSection.الناسخ_والمنسوخ] == ("naskh_mansukh.py",)
    ledger = read_sections()
    reading = ledger.reading_for(DalalaSection.الناسخ_والمنسوخ)
    assert reading.coding is SectionCoding.مُرمَّز
    assert ledger.uncoded_sections == ()
