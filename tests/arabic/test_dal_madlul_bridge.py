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
    THE_FIFTH_SECTION_SENTENCE,
    THE_MADLUL_SECTIONS_IN_REQUEST_ORDER,
    THE_SUSPENSION_SAMPLE_SIZE,
    BridgePair,
    ChannelStanding,
    DalalaKind,
    DalMadlulBridgeError,
    DeclaredMaterial,
    MadlulExtraction,
    MadlulSection,
    MaterialRole,
    SealStanding,
    bridge_metrics,
    bridge_pairs,
    channel_readings,
    extract_madlul,
    fifth_section_reading,
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
    """حضورٌ مقيسٌ لا مقول: وصلت البايتاتُ بالختم المُعلَن فانقلب الحكمُ وحدَه.

    وكان هذا الشاهدُ يقرأ «غائبًا» حين كانت الشجرةُ خاليةً منها؛ فانقلب
    بانقلاب القرص لا بتعديلِ جملةٍ في النثر — وهو عينُ ما ادّعته البقيّة.
    """

    assert governing_seal_reading().standing is SealStanding.SEALED_AND_PRESENT

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


def test_the_three_channels_are_open_and_none_still_names_an_unmet_condition() -> None:
    """المفتاحُ الذي سُمّي قبل وصوله هو الذي فتحها: بايتاتُ ج٣ بختمها."""

    readings = channel_readings()
    assert len(readings) == 3
    assert {reading.gate.kind for reading in readings} == set(DalalaKind)
    for reading in readings:
        assert reading.standing is ChannelStanding.OPEN
        assert reading.unmet_condition is None
        assert reading.key_that_would_open_it


def test_a_channel_closes_again_the_moment_its_sealed_bytes_leave(
    tmp_path: Path,
) -> None:
    """الانفتاحُ مشروطٌ لا مكتسَب: شجرةٌ بلا بايتاتٍ تُقفل القنواتِ فورًا."""

    for reading in channel_readings(tmp_path):
        assert reading.standing is ChannelStanding.CLOSED_FOR_AN_UNSEALED_SOURCE
        assert reading.unmet_condition


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


def test_the_tree_transcription_is_not_a_seal_and_does_not_open_a_channel(
    tmp_path: Path,
) -> None:
    """نقلٌ في الشجرة يحمل الجُمَلَ الثلاثَ لا يفتح قناةً؛ الختمُ وحدَه يفتح."""

    overlap = transcription_is_not_a_seal()
    assert len(overlap) == len(THE_CHANNEL_GATES)
    found = [phrase for phrase, present in overlap if present]
    assert found == ["دلالة اللفظ على جزء المسمى"]

    carrier = tmp_path / "src" / "alghanem" / "arabic"
    carrier.mkdir(parents=True)
    (carrier / "sentence_card_source_texts.py").write_text(
        "\n".join(gate.defining_phrase for gate in THE_CHANNEL_GATES),
        encoding="utf-8",
    )
    assert all(present for _, present in transcription_is_not_a_seal(tmp_path))
    assert all(
        reading.standing is ChannelStanding.CLOSED_FOR_AN_UNSEALED_SOURCE
        for reading in channel_readings(tmp_path)
    )
    assert all(reading.is_open for reading in channel_readings())


def test_no_pair_is_emitted_while_the_matching_channel_is_closed(
    tmp_path: Path,
) -> None:
    """الرخصةُ شرطٌ قائم: شجرةٌ بلا بايتات ج٣ لا يُخرَج منها زوجٌ البتّة."""

    assert bridge_pairs(tmp_path) == ()


def test_every_emitted_pair_carries_its_licence_and_its_material_apart() -> None:
    """الرخصةُ من ج٣، والمادّةُ من المقاييس؛ ولا يقوم أحدُهما مقام الآخر."""

    pairs = bridge_pairs()
    assert pairs
    for pair in pairs:
        assert pair.channel is DalalaKind.مطابقة
        assert pair.madlul_section is MadlulSection.MEANING
        assert "2c6000bd4779" in pair.sealed_source
        assert pair.madlul in pair.verbatim_evidence


def test_a_denied_origin_is_never_turned_into_a_signified() -> None:
    """«ليس بأصل» نفيٌ؛ ولا يُنتزَع من النفي مدلولٌ ولا يُخرَج به زوج."""

    reading = extract_madlul("الهمزة والباء والشين ليس بأصل، لأنّ الهمزة مبدلة.")
    assert reading.madlul is None
    assert reading.unmet_rung is not None
    assert "أبش" not in {pair.dal for pair in bridge_pairs()}
    assert "أبش" in {item.dal for item in suspended_signifiers()}


def test_many_declared_origins_never_collapse_into_one_complete_named_thing() -> None:
    reading = extract_madlul("وأما الهمزة والجيم فلها أصلان: الحَفِيف، والشدَّة.")
    assert reading.madlul is None
    assert "أج" in {item.dal for item in suspended_signifiers()}


def test_a_coordinated_statement_is_left_whole_so_half_is_never_emitted() -> None:
    """«تدلّ على الدهر، وعلى شئ من أرفاغ البطن» لا يُقطَع نصفُه باسم تمامه."""

    reading = extract_madlul("الهمزة والباء والضاد تدلّ على الدهر، وعلى شئ منه.")
    assert reading.madlul is None
    assert "أبض" in {item.dal for item in suspended_signifiers()}


def test_the_reading_is_either_a_signified_or_a_named_rung_never_both() -> None:
    with pytest.raises(DalMadlulBridgeError):
        MadlulExtraction(madlul="الحفيف", verbatim="شاهد", unmet_rung="درجة")
    with pytest.raises(DalMadlulBridgeError):
        MadlulExtraction(madlul=None, verbatim="شاهد", unmet_rung=None)


def test_the_statement_is_read_from_the_head_not_from_anywhere_in_the_article() -> None:
    """«ليس بأصل» في وسط المقالة لا يُلغي تصريحَ صدرها؛ الصدرُ هو المحكوم."""

    body = "وأما الهمزة والنون فأصلٌ واحد، وهو صوتٌ بتوجّع. وقيل ليس بأصل هناك."
    assert extract_madlul(body).madlul == "صوتٌ بتوجّع"


def test_the_fifth_section_is_settled_by_quoting_the_sealed_material() -> None:
    """الحسمُ توحيدُ اسمين لمسمًّى واحد، منقولًا بحروفه لا معلنًا في النثر."""

    reading = fifth_section_reading()
    assert reading.standing is SealStanding.SEALED_AND_PRESENT
    assert reading.is_settled
    assert reading.verbatim == THE_FIFTH_SECTION_SENTENCE
    assert "الهذيان" in reading.verbatim
    assert "مركباً مهملاً" in reading.verbatim
    assert reading.sealed_source is not None
    assert "360f7653" in reading.sealed_source


def test_the_settlement_dies_with_its_witness(tmp_path: Path) -> None:
    """دعوى الحسم لا تعيش بعد شاهدها: شجرةٌ بلا بايتاتٍ لا حسمَ فيها."""

    reading = fifth_section_reading(tmp_path)
    assert not reading.is_settled
    assert reading.verbatim is None
    assert reading.sealed_source is None


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
    assert len(suspended) == 13
    assert len({item.dal for item in suspended}) == len(suspended)
    for item in suspended:
        assert item.verbatim_witness.strip()
        assert "2c6000bd4779" in item.sealed_source
        assert item.unmet_rung.strip()
    assert len(suspended) + len(bridge_pairs()) == THE_SUSPENSION_SAMPLE_SIZE
    assert len({item.unmet_rung for item in suspended}) > 1


def test_the_instrument_is_shown_sighted_before_its_zero_is_read() -> None:
    """الآلةُ تقرأ دوالَّ بأعيانها وسطورَها، فتُخرِج ما استوفى وتُعلّق ما لم يستوفِ."""

    suspended = suspended_signifiers()
    assert suspended[0].dal == "أج"
    assert "الهمزة والجيم" in suspended[0].verbatim_witness
    assert bridge_pairs()[0].dal == "أز"


def test_suspension_refuses_to_run_on_an_unsealed_origin(tmp_path: Path) -> None:
    """فرقٌ بين «لا معلَّقَ» و«لم نقرأ»: الثاني رفضٌ يُرفَع لا عيّنةٌ فارغة."""

    with pytest.raises(DalMadlulBridgeError):
        suspended_signifiers(tmp_path)


def test_the_unmeasured_rates_are_named_unmeasured_and_never_read_as_one() -> None:
    metrics = bridge_metrics()
    assert metrics.pairs_emitted == 7
    assert metrics.suspended_count == 13
    assert metrics.dals_examined == THE_SUSPENSION_SAMPLE_SIZE
    assert metrics.coverage == 0.35
    assert metrics.truth_rate is None
    assert metrics.section_discipline == 1.0


def test_the_separation_zero_is_now_earned_and_no_longer_reached_by_vacancy() -> None:
    """صفرُ جمعِ المفهوم كان يُبلَغ بالخلوّ؛ وقد صار مكتسَبًا بسبعة أزواجٍ قائمة."""

    metrics = bridge_metrics()
    assert metrics.concept_joins == 0
    assert metrics.separation_holds
    assert not metrics.the_zero_was_reached_by_vacancy


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
    assert genera.count("معلق") == 13
    assert genera.count("زوج") == 7
    assert genera.count("معلق") + genera.count("زوج") == THE_SUSPENSION_SAMPLE_SIZE
    assert genera.count("مقياس") == 1
    assert rows[-1] == {"نوع": "مؤجَّل", "سطر": THE_DEFERRED_LINE}


def test_no_report_row_joins_a_signifier_and_a_signified_into_a_concept() -> None:
    """حدُّ العقد: صفٌّ يجمعهما «مفهومًا» يُسقط المهمّةَ كلَّها.

    وصفُّ الزوج يحمل الحقلين متمايزين وبينهما قناتُه المسمّاة — وذلك وسمٌ
    لا وعاء. فالممنوعُ حقلٌ ثالثٌ يذوبان فيه، لا اجتماعُهما في سطرِ سجلّ.
    """

    joined = 0
    for row in report_rows():
        assert "مفهوم" not in set(row)
        assert "مفهوم" not in str(row.get("نوع", ""))
        if "دال" in row and "مدلول" in row:
            joined += 1
            assert row["نوع"] == "زوج"
            assert row["قناة"] in {kind.value for kind in DalalaKind}
            assert row["دال"] != row["مدلول"]
    assert joined == len(bridge_pairs())


def test_the_report_records_the_settlement_with_its_quoted_witness() -> None:
    rows = [row for row in report_rows() if row["نوع"] == "خامس_متنازع"]
    assert len(rows) == 1
    assert rows[0]["أحُسم"] is True
    assert rows[0]["الشاهد"] == THE_FIFTH_SECTION_SENTENCE


def test_the_deposited_report_is_what_the_disk_generates_now() -> None:
    root = Path(__file__).resolve().parents[2]
    deposit = root / "exhibits" / "dal-madlul-bridge" / "bridge_report.jsonl"
    generated = "\n".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True) for row in report_rows(root)
    )
    assert deposit.read_text(encoding="utf-8") == generated + "\n"
