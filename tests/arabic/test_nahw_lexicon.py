"""اختباراتُ قاموس مصطلحات النحو — المرحلةِ صفرٍ لجسر الدالّ/المدلول.

والمادّتان النحويّتان ليستا في هذه الشجرة، فما يعتمد على بايتاتهما يُتخطّى
**حين لا تُحَلّ بايتاتُها** لا حين يخلو متغيّرُ البيئة؛ وما لا يعتمد عليها —
من عقودِ الوحدة وشكلِ الوديعة — يُفحَص في كلّ حال.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Final

import pytest

from alghanem.arabic.nahw_lexicon import (
    THE_DEFERRED_LINE,
    THE_DOORS,
    THE_EXTRACTIONS,
    THE_HEARING_CHECK_SAMPLE_SIZE,
    THE_HEARING_CHECK_VERDICTS,
    THE_LETTER_COUNT_CONFLICT,
    THE_MATERIALS,
    THE_PROBES,
    THE_SUSPENDED_GLOSS,
    THE_SUSPENDED_OPERATION,
    DeclaredExtraction,
    DeclaredMaterial,
    DeclaredProbe,
    DoorStanding,
    ExtractionRule,
    LexiconEntry,
    MaterialRole,
    NahwLexiconError,
    SealStanding,
    door_readings,
    hearing_check_sample,
    lexicon_entries,
    lexicon_metrics,
    material_text,
    probe_readings,
    report_markdown,
    report_rows,
    seal_readings,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
LEDGER_PATH = REPOSITORY_ROOT / "exhibits" / "nahw-lexicon" / "nahw_lexicon.jsonl"
REPORT_PATH = REPOSITORY_ROOT / "exhibits" / "nahw-lexicon" / "LEXICON-REPORT.md"


def _both_materials_open() -> bool:
    return all(
        material_text(key) is not None for key in ("MUGHNI_LABIB", "KITAB_SIBAWAYH")
    )


_BOTH_MATERIALS_OPEN: Final = _both_materials_open()

_SKIP_REASON: Final = (
    "بايتاتُ المغني وسيبويه غيرُ محلولةٍ في هذه البيئة؛ والتخطّي معلَّقٌ "
    "بالبايتات لا بالمتغيّر."
)


# --- عقودُ الإعلان، تُفحَص بلا بايتات ------------------------------------------


def test_the_three_materials_are_declared_with_full_seals() -> None:
    assert len(THE_MATERIALS) == 3
    for material in THE_MATERIALS:
        assert len(material.declared_sha256) == 64
        assert material.declared_byte_length > 0
        assert material.path_environment_variable.startswith("ALGHANEM_")


def test_the_governing_material_is_declared_and_is_not_the_expositor() -> None:
    governing = [
        material
        for material in THE_MATERIALS
        if material.role is MaterialRole.GOVERNING_CLASSIFICATION
    ]
    assert len(governing) == 1
    assert governing[0].key == "SHAKHSIYYA_THREE"


def test_a_material_with_a_malformed_seal_is_refused_at_construction() -> None:
    with pytest.raises(NahwLexiconError):
        DeclaredMaterial(
            key="X",
            title="X",
            relative_path="x.txt",
            path_environment_variable="ALGHANEM_X_PATH",
            declared_byte_length=1,
            declared_sha256="not-a-digest",
            role=MaterialRole.PRIMARY_EXPOSITION,
        )


def test_a_material_with_a_nonpositive_length_is_refused() -> None:
    with pytest.raises(NahwLexiconError):
        DeclaredMaterial(
            key="X",
            title="X",
            relative_path="x.txt",
            path_environment_variable="ALGHANEM_X_PATH",
            declared_byte_length=0,
            declared_sha256="0" * 64,
            role=MaterialRole.PRIMARY_EXPOSITION,
        )


def test_an_enumeration_without_a_sorting_rule_is_not_a_declared_enumeration() -> None:
    with pytest.raises(NahwLexiconError):
        DeclaredExtraction(
            key="X",
            door_number=1,
            material_key="MUGHNI_LABIB",
            rule=ExtractionRule.ENUMERATION_AFTER_ANCHOR,
            anchor="مرساة",
            stop=None,
            pattern=None,
            entry_name=None,
        )


def test_an_anchor_sentence_without_an_entry_name_is_refused() -> None:
    with pytest.raises(NahwLexiconError):
        DeclaredExtraction(
            key="X",
            door_number=1,
            material_key="MUGHNI_LABIB",
            rule=ExtractionRule.ANCHOR_SENTENCE,
            anchor="مرساة",
            stop=None,
            pattern=None,
            entry_name=None,
        )


def test_a_probe_outside_the_eight_doors_is_refused() -> None:
    with pytest.raises(NahwLexiconError):
        DeclaredProbe(9, "عبارة", "MUGHNI_LABIB")


def test_an_entry_without_a_witness_is_a_claim_without_a_witness() -> None:
    with pytest.raises(NahwLexiconError):
        LexiconEntry(
            door_number=1,
            door_title="باب",
            extraction_key="X",
            name="اسم",
            gloss="تعريف",
            operation="عمل",
            witness="   ",
            line_number=1,
            material_key="MUGHNI_LABIB",
            material_sha256="0" * 64,
        )


def test_an_entry_without_a_positive_line_number_is_refused() -> None:
    with pytest.raises(NahwLexiconError):
        LexiconEntry(
            door_number=1,
            door_title="باب",
            extraction_key="X",
            name="اسم",
            gloss="تعريف",
            operation="عمل",
            witness="دليل",
            line_number=0,
            material_key="MUGHNI_LABIB",
            material_sha256="0" * 64,
        )


def test_the_eight_doors_are_numbered_one_through_eight_without_a_gap() -> None:
    assert tuple(door.number for door in THE_DOORS) == tuple(range(1, 9))


def test_every_probe_and_extraction_names_a_declared_material() -> None:
    keys = {material.key for material in THE_MATERIALS}
    assert {probe.material_key for probe in THE_PROBES} <= keys
    assert {extraction.material_key for extraction in THE_EXTRACTIONS} <= keys


def test_the_deferred_line_is_carried_verbatim_and_names_both_later_phases() -> None:
    assert THE_DEFERRED_LINE == (
        "هذا قاموس أدوات ومصطلحات — لا وسمَ به نصًّا بعد، ولا جسرَ دال/مدلول؛ "
        "كلاهما طور لاحق يستعمل هذا القاموس."
    )


def test_the_letter_count_conflict_keeps_both_sides_and_adjudicates_neither() -> None:
    request, sibawayh = THE_LETTER_COUNT_CONFLICT
    assert "الثمانية والعشرون" in request
    assert "تسعة وعشرون" in sibawayh


# --- الأختامُ والغياب ----------------------------------------------------------


def test_the_governing_material_is_present_yet_still_yields_no_rows() -> None:
    """حضورُ البايتات ليس إخراجَ بنود: المادّةُ تُفتَح، والمجسّاتُ لا تقع فيها.

    فلا يُقرأ هذا الصفرُ «غيابًا» بعد اليومَ، ولا يُقرأ «بحثًا جرى فلم يجد»
    في مادّةٍ لم تُفتَح: البايتاتُ تُفتَح فعلًا وتُقرأ منها ١١٣٢ فقرة، ثمّ
    لا يقع فيها مجسٌّ من مجسّات هذه الوحدة.
    """

    present = [
        reading
        for reading in seal_readings()
        if reading.material.key == "SHAKHSIYYA_THREE"
    ]
    assert len(present) == 1
    assert present[0].standing is SealStanding.SEALED_AND_PRESENT
    assert present[0].is_readable
    lines = material_text("SHAKHSIYYA_THREE")
    assert lines is not None
    assert len(lines) == 1132
    assert all(entry.material_key != "SHAKHSIYYA_THREE" for entry in lexicon_entries())


def test_a_seal_mismatch_halts_instead_of_reading(tmp_path: Path) -> None:
    root = tmp_path
    (root / "corpora").mkdir()
    (root / "corpora" / "mughni-labib-shamela0006972-ara1.txt").write_bytes(b"x")
    reading = [
        seal for seal in seal_readings(root) if seal.material.key == "MUGHNI_LABIB"
    ][0]
    if reading.resolved_path is not None and reading.resolved_path.startswith(
        str(root)
    ):
        assert reading.standing is SealStanding.SEAL_MISMATCH_HALT
        assert not reading.is_readable


def test_a_door_with_no_entries_is_suspended_not_silently_dropped() -> None:
    readings = door_readings()
    assert len(readings) == len(THE_DOORS)
    for reading in readings:
        if reading.entry_count == 0:
            assert reading.standing is DoorStanding.SUSPENDED


# --- ما يحتاج البايتات --------------------------------------------------------


@pytest.mark.skipif(not _BOTH_MATERIALS_OPEN, reason=_SKIP_REASON)
def test_the_two_expository_materials_match_length_and_digest_together() -> None:
    for reading in seal_readings():
        if reading.material.key == "SHAKHSIYYA_THREE":
            continue
        assert reading.standing is SealStanding.SEALED_AND_PRESENT
        assert reading.measured_byte_length == reading.material.declared_byte_length
        assert reading.measured_sha256 == reading.material.declared_sha256


@pytest.mark.skipif(not _BOTH_MATERIALS_OPEN, reason=_SKIP_REASON)
def test_sibawayh_enumerates_twenty_nine_letters_not_the_twenty_eight_asked() -> None:
    names = [
        entry.name
        for entry in lexicon_entries()
        if entry.extraction_key == "SIBAWAYH_LETTER_ENUMERATION"
    ]
    assert len(names) == 29
    assert len(set(names)) == 29
    assert names[0] == "الهمزة"
    assert names[1] == "الألف"
    assert names[-1] == "الواو"


@pytest.mark.skipif(not _BOTH_MATERIALS_OPEN, reason=_SKIP_REASON)
def test_every_emitted_entry_carries_a_witness_and_a_raw_line_position() -> None:
    entries = lexicon_entries()
    assert entries
    for entry in entries:
        assert entry.witness.strip()
        assert entry.line_number > 0
        assert entry.material_sha256 in {
            material.declared_sha256 for material in THE_MATERIALS
        }


@pytest.mark.skipif(not _BOTH_MATERIALS_OPEN, reason=_SKIP_REASON)
def test_a_read_name_occurs_inside_its_own_witness() -> None:
    labelled = {
        extraction.key
        for extraction in THE_EXTRACTIONS
        if extraction.rule is ExtractionRule.ANCHOR_SENTENCE
    }
    read = [
        entry for entry in lexicon_entries() if entry.extraction_key not in labelled
    ]
    assert read
    for entry in read:
        assert entry.name.lstrip("و") in entry.witness, entry


@pytest.mark.skipif(not _BOTH_MATERIALS_OPEN, reason=_SKIP_REASON)
def test_a_declared_label_is_not_claimed_to_be_read_from_the_bytes() -> None:
    labelled = {
        extraction.key: extraction.entry_name
        for extraction in THE_EXTRACTIONS
        if extraction.rule is ExtractionRule.ANCHOR_SENTENCE
    }
    assert labelled
    for entry in lexicon_entries():
        if entry.extraction_key in labelled:
            assert entry.name == labelled[entry.extraction_key]
            assert entry.name not in entry.witness


@pytest.mark.skipif(not _BOTH_MATERIALS_OPEN, reason=_SKIP_REASON)
def test_a_declared_operation_is_read_from_the_bytes_not_invented() -> None:
    operated = [
        entry
        for entry in lexicon_entries()
        if entry.operation != THE_SUSPENDED_OPERATION
    ]
    assert operated
    for entry in operated:
        assert entry.operation in entry.witness


@pytest.mark.skipif(not _BOTH_MATERIALS_OPEN, reason=_SKIP_REASON)
def test_the_particles_named_with_their_operation_keep_each_its_own() -> None:
    by_name = {
        entry.name: entry.operation
        for entry in lexicon_entries()
        if entry.extraction_key == "MUGHNI_PARTICLES_NAMED_WITH_THEIR_OPERATION"
    }
    assert by_name["إن"] == "حرف توكيد"
    assert by_name["أن"] == "حرف مصدري"
    assert by_name["لن"] == "حرف نفي"
    assert by_name["لم"] == "حرف نفي"


@pytest.mark.skipif(not _BOTH_MATERIALS_OPEN, reason=_SKIP_REASON)
def test_the_unvocalized_bytes_collapse_anta_and_anti_into_one_form() -> None:
    names = [
        entry.name
        for entry in lexicon_entries()
        if entry.extraction_key == "MUGHNI_DETACHED_ADDRESSEE_PRONOUNS"
    ]
    assert names == ["أنت", "أنتما", "أنتم", "أنتن"]


@pytest.mark.skipif(not _BOTH_MATERIALS_OPEN, reason=_SKIP_REASON)
def test_a_probe_measuring_zero_is_reported_not_hidden() -> None:
    readings = probe_readings()
    zeroed = [
        reading
        for reading in readings
        if reading.material_opened and reading.occurrences == 0
    ]
    assert zeroed
    for reading in zeroed:
        assert reading.first_line_number is None
    sighted = [
        reading
        for reading in readings
        if reading.material_opened and reading.occurrences > 0
    ]
    assert sighted, "آلةٌ لا تُصيب شيئًا لا يُقرأ صفرُها خبرًا."


@pytest.mark.skipif(not _BOTH_MATERIALS_OPEN, reason=_SKIP_REASON)
def test_the_hearing_sample_is_deterministic_under_its_declared_seed() -> None:
    first = hearing_check_sample()
    second = hearing_check_sample()
    assert [entry.name for entry in first] == [entry.name for entry in second]
    assert len(first) == THE_HEARING_CHECK_SAMPLE_SIZE


@pytest.mark.skipif(not _BOTH_MATERIALS_OPEN, reason=_SKIP_REASON)
def test_every_hearing_verdict_belongs_to_the_sample_and_covers_it() -> None:
    sample = {
        f"{entry.extraction_key}::{entry.name}" for entry in hearing_check_sample()
    }
    verdicts = {key for key, _, _ in THE_HEARING_CHECK_VERDICTS}
    assert verdicts == sample


@pytest.mark.skipif(not _BOTH_MATERIALS_OPEN, reason=_SKIP_REASON)
def test_the_false_row_caught_by_the_ear_is_kept_in_the_ledger() -> None:
    names = [
        entry.name
        for entry in lexicon_entries()
        if entry.extraction_key == "MUGHNI_LETTER_CHAPTERS"
    ]
    assert "المراد" in names, "الصفُّ الساقطُ يُعرَض ساقطًا ولا يُحذَف."
    failed = [key for key, sound, _ in THE_HEARING_CHECK_VERDICTS if not sound]
    assert "MUGHNI_LETTER_CHAPTERS::المراد" in failed


@pytest.mark.skipif(not _BOTH_MATERIALS_OPEN, reason=_SKIP_REASON)
def test_the_metrics_are_rederived_and_the_witness_ratio_is_whole() -> None:
    metrics = lexicon_metrics()
    assert metrics.entry_count == len(lexicon_entries())
    assert metrics.witnessed_count == metrics.entry_count
    assert metrics.witness_ratio == 1.0
    assert metrics.materials_absent == 1
    assert metrics.materials_sealed_and_present == 2
    assert 0.0 < metrics.hearing_soundness < 1.0


@pytest.mark.skipif(not _BOTH_MATERIALS_OPEN, reason=_SKIP_REASON)
def test_no_row_pairs_a_dal_with_a_madlul_because_that_phase_is_deferred() -> None:
    for row in report_rows():
        assert "المدلول" not in row
        assert "قناة" not in row
        assert "مفهوم" not in row


@pytest.mark.skipif(not _BOTH_MATERIALS_OPEN, reason=_SKIP_REASON)
def test_the_deposited_ledger_collides_with_what_disk_produces_now() -> None:
    generated = [
        json.dumps(row, ensure_ascii=False, sort_keys=True) for row in report_rows()
    ]
    deposited = LEDGER_PATH.read_text(encoding="utf-8").splitlines()
    assert deposited == generated


@pytest.mark.skipif(not _BOTH_MATERIALS_OPEN, reason=_SKIP_REASON)
def test_the_deposited_report_collides_with_what_disk_produces_now() -> None:
    assert REPORT_PATH.read_text(encoding="utf-8") == report_markdown()


def test_the_deposited_ledger_rows_each_carry_the_seven_pillars() -> None:
    required = {
        "الباب",
        "الاسم",
        "التعريف المختصر",
        "العمل",
        "الدليل الحرفي",
        "الموضع",
        "المادة المختومة",
        "ختم المادة",
    }
    lines = LEDGER_PATH.read_text(encoding="utf-8").splitlines()
    assert lines
    for line in lines:
        row = json.loads(line)
        assert required <= set(row)
        assert str(row["الدليل الحرفي"]).strip()
        assert str(row["الموضع"]).startswith("سطر ")


def test_the_deposited_report_carries_the_deferred_line_verbatim() -> None:
    assert THE_DEFERRED_LINE in REPORT_PATH.read_text(encoding="utf-8")


def test_a_suspended_gloss_is_named_suspended_and_not_left_empty() -> None:
    assert THE_SUSPENDED_GLOSS.startswith("معلق")
    assert THE_SUSPENDED_OPERATION.startswith("معلق")
