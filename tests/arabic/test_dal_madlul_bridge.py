"""شواهدُ جسر الدالِّ وحدَه بالمدلول وحدَه: تُصادم القياسَ ولا تنقله."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from alghanem.arabic.dal_madlul_bridge import (
    THE_CHANNEL_GATES,
    THE_CONTESTED_FIFTH_SECTION,
    THE_DECLARED_MATERIALS,
    THE_DEFERRED_LINE,
    THE_MADLUL_SECTIONS_IN_REQUEST_ORDER,
    THE_SUSPENSION_SAMPLE_SIZE,
    BridgePair,
    ChannelStanding,
    DalalaKind,
    DalMadlulBridgeError,
    DeclaredMaterial,
    MadlulSection,
    MaterialRole,
    SealStanding,
    bridge_metrics,
    bridge_pairs,
    channel_readings,
    governing_seal_reading,
    report_rows,
    seal_reading_for,
    seal_readings,
    suspended_signifiers,
    transcription_is_not_a_seal,
)


def test_the_governing_material_is_declared_by_its_seal_not_by_its_name() -> None:
    governing = governing_seal_reading()
    assert governing.material.role is MaterialRole.GOVERNING_DIVISION
    assert governing.material.declared_byte_length == 673_537
    assert governing.material.declared_sha256.startswith("360f7653")


def test_the_absence_is_measured_by_opening_the_path_not_by_a_written_sentence(
    tmp_path: Path,
) -> None:
    """غيابٌ مقيسٌ لا مقول: لو وصلت بايتاتٌ بالختم المُعلَن لانقلب الحكمُ وحدَه."""

    assert governing_seal_reading().standing is SealStanding.ABSENT_FROM_THIS_TREE

    governing = THE_DECLARED_MATERIALS[0]
    forged = tmp_path / governing.relative_path
    forged.write_bytes(b"x")
    readings = {reading.material.key: reading for reading in seal_readings(tmp_path)}
    assert readings[governing.key].standing is SealStanding.SEAL_MISMATCH_HALT
    assert readings[governing.key].measured_byte_length == 1


def test_a_seal_mismatch_is_a_halt_and_is_never_read_as_presence(
    tmp_path: Path,
) -> None:
    governing = THE_DECLARED_MATERIALS[0]
    (tmp_path / governing.relative_path).write_bytes(
        b"\0" * governing.declared_byte_length
    )
    reading = governing_seal_reading(tmp_path)
    assert reading.standing is SealStanding.SEAL_MISMATCH_HALT
    assert not reading.is_readable
    assert reading.measured_byte_length == governing.declared_byte_length
    assert reading.measured_sha256 != governing.declared_sha256


def test_the_present_lexical_origin_matches_the_seal_named_in_the_request() -> None:
    readings = {reading.material.key: reading for reading in seal_readings()}
    origin = readings["MAQAYIS_BY_ROOT"]
    assert origin.standing is SealStanding.SEALED_AND_PRESENT
    assert origin.material.declared_sha256.startswith("2c6000bd4779")
    assert origin.measured_sha256 == origin.material.declared_sha256
    measured = hashlib.sha256(
        (
            Path(__file__).resolve().parents[2] / origin.material.relative_path
        ).read_bytes()
    ).hexdigest()
    assert measured == origin.measured_sha256


def test_the_three_channels_are_closed_and_each_names_its_unmet_condition() -> None:
    readings = channel_readings()
    assert len(readings) == 3
    assert {reading.gate.kind for reading in readings} == set(DalalaKind)
    for reading in readings:
        assert reading.standing is ChannelStanding.CLOSED_FOR_AN_UNSEALED_SOURCE
        assert reading.unmet_condition
        assert reading.key_that_would_open_it


def test_matching_bytes_are_admitted_so_the_closure_is_a_lock_not_a_refusal(
    tmp_path: Path,
) -> None:
    """البابُ مقفلٌ لا مسدود: بايتاتٌ تطابق ختمَها تُقرأ «مختومةً حاضرة» فورًا."""

    payload = "دلالة اللفظ على تمام مسماه".encode()
    (tmp_path / "ج٣_مفترض.txt").write_bytes(payload)
    material = DeclaredMaterial(
        key="SHAKHSIYYA_THREE",
        title="بايتاتٌ مفترضةٌ لامتحان القفل",
        relative_path="ج٣_مفترض.txt",
        declared_byte_length=len(payload),
        declared_sha256=hashlib.sha256(payload).hexdigest(),
        role=MaterialRole.GOVERNING_DIVISION,
    )
    reading = seal_reading_for(material, tmp_path)
    assert reading.standing is SealStanding.SEALED_AND_PRESENT
    assert reading.is_readable


def test_a_material_declared_with_a_malformed_seal_is_refused() -> None:
    with pytest.raises(DalMadlulBridgeError):
        DeclaredMaterial(
            key="X",
            title="مادّةٌ بختمٍ ناقص",
            relative_path="x.txt",
            declared_byte_length=1,
            declared_sha256="360f7653",
            role=MaterialRole.DECLARED_LEXICAL_ORIGIN,
        )


def test_the_tree_transcription_is_not_a_seal_and_does_not_open_a_channel() -> None:
    overlap = transcription_is_not_a_seal()
    assert len(overlap) == len(THE_CHANNEL_GATES)
    found = [phrase for phrase, present in overlap if present]
    assert found == ["دلالة اللفظ على جزء المسمى"]
    assert all(
        reading.standing is ChannelStanding.CLOSED_FOR_AN_UNSEALED_SOURCE
        for reading in channel_readings()
    )


def test_no_pair_is_emitted_while_a_channel_is_closed() -> None:
    assert bridge_pairs() == ()


def test_a_pair_without_verbatim_evidence_is_refused_by_construction() -> None:
    with pytest.raises(DalMadlulBridgeError):
        BridgePair(
            dal="أج",
            channel=DalalaKind.مطابقة,
            madlul="الحفيف",
            madlul_section=MadlulSection.MEANING,
            verbatim_evidence="   ",
            sealed_source="maqayis_by_root_csv_999.csv",
        )


def test_a_pair_refuses_a_signified_section_outside_the_proven_division() -> None:
    with pytest.raises(DalMadlulBridgeError):
        BridgePair(
            dal="أج",
            channel=DalalaKind.مطابقة,
            madlul="الحفيف",
            madlul_section="معنى",  # type: ignore[arg-type]
            verbatim_evidence="وأما الهمزة والجيم فلها أصلان: الحَفِيف",
            sealed_source="maqayis_by_root_csv_999.csv",
        )


def test_the_suspended_are_first_class_rows_carrying_a_sealed_witness() -> None:
    suspended = suspended_signifiers()
    assert len(suspended) == THE_SUSPENSION_SAMPLE_SIZE
    assert len({item.dal for item in suspended}) == THE_SUSPENSION_SAMPLE_SIZE
    for item in suspended:
        assert item.verbatim_witness.strip()
        assert "2c6000bd4779" in item.sealed_source
        assert "مقفلة" in item.unmet_rung


def test_the_instrument_is_shown_sighted_before_its_zero_is_read() -> None:
    """صفرُ الأزواج بابٌ مقفلٌ لا آلةٌ عمياء: هي تقرأ دوالَّ بأعيانها وسطورَها."""

    suspended = suspended_signifiers()
    assert bridge_pairs() == ()
    assert suspended[0].dal == "أج"
    assert "الهمزة والجيم" in suspended[0].verbatim_witness


def test_suspension_refuses_to_run_on_an_unsealed_origin(tmp_path: Path) -> None:
    """فرقٌ بين «لا معلَّقَ» و«لم نقرأ»: الثاني رفضٌ يُرفَع لا عيّنةٌ فارغة."""

    with pytest.raises(DalMadlulBridgeError):
        suspended_signifiers(tmp_path)


def test_the_unmeasured_rates_are_named_unmeasured_and_never_read_as_one() -> None:
    metrics = bridge_metrics()
    assert metrics.pairs_emitted == 0
    assert metrics.suspended_count == THE_SUSPENSION_SAMPLE_SIZE
    assert metrics.coverage == 0.0
    assert metrics.truth_rate is None
    assert metrics.section_discipline is None


def test_the_separation_zero_declares_that_vacancy_reached_it() -> None:
    metrics = bridge_metrics()
    assert metrics.concept_joins == 0
    assert metrics.separation_holds
    assert metrics.the_zero_was_reached_by_vacancy


def test_the_five_sections_are_imported_not_rewritten() -> None:
    assert THE_MADLUL_SECTIONS_IN_REQUEST_ORDER == tuple(MadlulSection)
    assert THE_CONTESTED_FIFTH_SECTION == (
        MadlulSection.HADHAYAN.value,
        "لفظ_مركّب_مهمَل",
    )


def test_the_report_carries_every_genus_and_the_deferred_line() -> None:
    rows = report_rows()
    genera = [row["نوع"] for row in rows]
    assert genera.count("مادة") == len(THE_DECLARED_MATERIALS)
    assert genera.count("قناة") == len(THE_CHANNEL_GATES)
    assert genera.count("معلق") == THE_SUSPENSION_SAMPLE_SIZE
    assert genera.count("زوج") == 0
    assert genera.count("مقياس") == 1
    assert rows[-1] == {"نوع": "مؤجَّل", "سطر": THE_DEFERRED_LINE}


def test_no_report_row_joins_a_signifier_and_a_signified_into_a_concept() -> None:
    """حدُّ العقد: صفٌّ واحدٌ يجمعهما «مفهومًا» يُسقط المهمّةَ كلَّها."""

    for row in report_rows():
        assert "مفهوم" not in str(row.get("نوع", ""))
        if "دال" in row and "مدلول" in row:  # pragma: no cover - حارسٌ لا يُبلَغ
            pytest.fail("زوجٌ جمع الدالَّ والمدلولَ في صفٍّ واحدٍ بلا قناةٍ مفتوحة")


def test_the_deposited_report_is_what_the_disk_generates_now() -> None:
    root = Path(__file__).resolve().parents[2]
    deposit = root / "exhibits" / "dal-madlul-bridge" / "bridge_report.jsonl"
    generated = "\n".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True) for row in report_rows(root)
    )
    assert deposit.read_text(encoding="utf-8") == generated + "\n"
