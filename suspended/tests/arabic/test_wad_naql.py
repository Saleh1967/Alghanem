"""Tests for the fourth link: the wad is human, and known by naql alone."""

from __future__ import annotations

import json
import pkgutil
from dataclasses import FrozenInstanceError, fields
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic import (
    ADAM_TEACHING_EVIDENCE,
    DISTRIBUTIONAL_TRACE_IS_NOT_WAD_PATH_NOTE,
    RECORDED_ADAM_TEACHING_READING,
    RECORDED_TAWQIF_REFUTATION,
    REFUSED_DERIVATION_NOTES,
    WAD_SOURCE,
    WAD_SOURCE_TEXT,
    AdamTeachingReading,
    AdamTeachingRecord,
    DistributionalCorroboration,
    RefutationGround,
    StatisticalFunction,
    TawqifRefutation,
    TawqifRefutationGround,
    TransmissionStanding,
    WadDerivationRefusal,
    WadNaqlError,
    WadOrigin,
    WadRecord,
    refuse_derivation,
)
from alghanem.arabic.external_audit import audit_card

_EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "external_audit"
_CARDS = ("quru_2_228.yaml", "anna_2_223.yaml", "hadhan_20_63.yaml")


def ground(**overrides: object) -> RefutationGround:
    base: dict[str, object] = {
        "ground": TawqifRefutationGround.لا_طريق_بالوحي,
        "excerpt": "لا يوجد دليل شرعي على أن اللغات توقيفية من الله",
        "argument": "الوحيُ لا يُفهَم إلا بلغةٍ سابقةٍ عليه، فالطريقُ إليه دورٌ محال.",
    }
    base.update(overrides)
    return RefutationGround(**base)  # type: ignore[arg-type]


def wad(**overrides: object) -> WadRecord:
    base: dict[str, object] = {
        "lafz": "قُرُوء",
        "madlul": "الأطهار أو الحيض",
        "naql_source": "لسان العرب، مادة ق ر أ",
        "transmission": TransmissionStanding.AHAD,
    }
    base.update(overrides)
    return WadRecord(**base)  # type: ignore[arg-type]


def test_the_origin_is_derived_from_the_refutation_and_is_human() -> None:
    assert RECORDED_TAWQIF_REFUTATION.origin is WadOrigin.وضع_بشري
    assert len(WadOrigin) == 2


def test_the_origin_is_not_a_writable_field_on_any_type() -> None:
    for declaring_type in (TawqifRefutation, WadRecord):
        declared = {item.name for item in fields(declaring_type)}
        assert "origin" not in declared


def test_one_ground_alone_is_refused_as_an_exhaustion_that_never_happened() -> None:
    with pytest.raises(WadNaqlError, match="ثنائيٌّ لا يقوم بشِقٍّ واحد"):
        TawqifRefutation(source=WAD_SOURCE, grounds=(ground(),))


def test_a_repeated_ground_is_not_a_second_ground() -> None:
    with pytest.raises(WadNaqlError, match="ليس شِقًّا ثانيًا"):
        TawqifRefutation(source=WAD_SOURCE, grounds=(ground(), ground()))


def test_both_grounds_together_are_admitted_and_are_exactly_the_closed_two() -> None:
    refutation = RECORDED_TAWQIF_REFUTATION
    assert {item.ground for item in refutation.grounds} == set(TawqifRefutationGround)
    assert len(TawqifRefutationGround) == 2


def test_an_unnamed_source_is_refused_as_a_witness() -> None:
    with pytest.raises(WadNaqlError, match="اسمٌ حرٌّ لا يصلح شاهدًا"):
        TawqifRefutation(
            source="كتابٌ في اللغة",
            grounds=RECORDED_TAWQIF_REFUTATION.grounds,
        )


def test_an_excerpt_absent_from_the_attested_text_is_refused() -> None:
    with pytest.raises(WadNaqlError, match="نقلٌ بنصّه"):
        ground(excerpt="اللغات توقيفية من الله بلا خلاف")


def test_every_recorded_excerpt_is_verbatim_inside_the_attested_source_text() -> None:
    for item in RECORDED_TAWQIF_REFUTATION.grounds:
        assert item.excerpt in WAD_SOURCE_TEXT
    assert ADAM_TEACHING_EVIDENCE in WAD_SOURCE_TEXT


def test_the_taught_names_are_realities_not_lexemes() -> None:
    assert (
        RECORDED_ADAM_TEACHING_READING.reading
        is AdamTeachingReading.حقائق_الأشياء_وخواصها
    )
    assert RECORDED_ADAM_TEACHING_READING.teaches_realities_not_lexemes is True


def test_reading_the_names_as_lexemes_is_refused_by_the_source_itself() -> None:
    with pytest.raises(WadNaqlError, match="مسمّيات الأشياء لا اللغات"):
        AdamTeachingRecord(
            reading=AdamTeachingReading.ألفاظ_اللغة,
            excerpt=ADAM_TEACHING_EVIDENCE,
        )


def test_the_knowledge_path_comes_from_the_imported_transmission_vocabulary() -> None:
    for standing in TransmissionStanding:
        assert wad(transmission=standing).transmission is standing
    with pytest.raises(WadNaqlError, match="TransmissionStanding"):
        wad(transmission="متواتر")


def test_a_wad_record_is_known_only_by_naql_and_names_its_source() -> None:
    record = wad()
    assert record.known_only_by_naql is True
    assert record.origin is WadOrigin.وضع_بشري
    with pytest.raises(WadNaqlError, match="مصدرُ النقل"):
        wad(naql_source="  ")


def test_both_refused_derivations_raise_rather_than_warn() -> None:
    assert len(WadDerivationRefusal) == 2
    for path in WadDerivationRefusal:
        with pytest.raises(WadNaqlError) as caught:
            refuse_derivation(path)
        assert str(caught.value) == REFUSED_DERIVATION_NOTES[path]


def test_a_wad_record_carries_no_distributional_derivation_field() -> None:
    declared = {item.name.lower() for item in fields(WadRecord)}
    for marker in ("distribution", "cluster", "frequency", "probe", "corpus"):
        assert not any(marker in name for name in declared), marker


def test_corroboration_is_bound_to_a_wad_already_known_by_naql() -> None:
    with pytest.raises(WadNaqlError, match="دعوى اكتشافٍ لا مصادقة"):
        DistributionalCorroboration(
            wad="قُرُوء",  # type: ignore[arg-type]
            probe_reference="RECORDED_PROBE_REPORT",
            observed_regularity="انتظامٌ مرصود",
        )


def test_statistics_raise_diraya_and_never_make_riwaya() -> None:
    record = wad(transmission=TransmissionStanding.AHAD)
    corroboration = DistributionalCorroboration(
        wad=record,
        probe_reference="RECORDED_PROBE_REPORT",
        observed_regularity="انتظامٌ توزيعيٌّ مستقرّ",
    )
    assert corroboration.function is StatisticalFunction.يرفع_دراية
    assert corroboration.transmission_after_corroboration is record.transmission
    assert len(StatisticalFunction) == 2


def test_the_corroboration_cannot_rewrite_the_transmission_standing() -> None:
    record = wad(transmission=TransmissionStanding.FARD)
    corroboration = DistributionalCorroboration(
        wad=record,
        probe_reference="RECORDED_PROBE_REPORT",
        observed_regularity="انتظامٌ توزيعيٌّ مستقرّ",
    )
    with pytest.raises(FrozenInstanceError):
        corroboration.wad = wad(  # type: ignore[misc]
            transmission=TransmissionStanding.MUTAWATIR
        )
    assert corroboration.transmission_after_corroboration is TransmissionStanding.FARD


def test_the_trace_boundary_names_both_sides_without_correcting_either() -> None:
    assert "أثرُ الوضع غيرُ طريقِ معرفته" in DISTRIBUTIONAL_TRACE_IS_NOT_WAD_PATH_NOTE
    assert "ONLY_LEGITIMATE_TARGET_NOTE" in DISTRIBUTIONAL_TRACE_IS_NOT_WAD_PATH_NOTE


def test_the_existing_semantic_target_note_is_untouched_by_this_module() -> None:
    from alghanem.arabic.maluma_mafhum import ONLY_LEGITIMATE_TARGET_NOTE

    assert ONLY_LEGITIMATE_TARGET_NOTE == (
        "هدفُ الدلالة المشروع الوحيد استرجاعُ الوضع: انتظامٌ توزيعيٌّ مستقرٌّ "
        "عبر مجتمعٍ لغوي، قابلٌ للرصد إحصائيًّا في كوربصٍ كبير."
    )


def test_no_type_here_carries_a_verdict_or_birth_field() -> None:
    for declaring_type in (
        RefutationGround,
        TawqifRefutation,
        AdamTeachingRecord,
        WadRecord,
        DistributionalCorroboration,
    ):
        declared = {item.name.lower() for item in fields(declaring_type)}
        for marker in ("verdict", "birth", "freeze", "rank", "count"):
            assert not any(marker in name for name in declared), marker


def test_the_module_reads_no_kernel_authority() -> None:
    source = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "alghanem"
        / "arabic"
        / "wad_naql.py"
    ).read_text(encoding="utf-8")
    imports = tuple(
        line for line in source.splitlines() if line.startswith(("import ", "from "))
    )
    assert imports
    assert not any("kernel" in line for line in imports)


def test_no_kernel_module_reads_this_wad_layer() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        spec = module.module_finder.find_spec(module.name)  # type: ignore[union-attr]
        assert spec is not None and spec.origin is not None
        text = Path(spec.origin).read_text(encoding="utf-8")
        for name in ("wad_naql", "WadRecord", "TawqifRefutation"):
            assert name not in text, (module.name, name)


@pytest.mark.parametrize("card", _CARDS)
def test_this_module_changes_no_external_audit_field(card: str) -> None:
    before = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    wad()
    after = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    assert before == after
