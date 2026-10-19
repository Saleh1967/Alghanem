"""Tests for the fourth AIM.1 milestone: the aims document read against its record."""

from __future__ import annotations

import ast
import pkgutil
from dataclasses import fields, replace
from pathlib import Path
from types import MappingProxyType

import pytest

import alghanem.kernel as kernel_package
from alghanem.program import (
    AIM_RECORDS,
    AIMS_DOCUMENT_NAMED_RESIDUALS,
    RECORD_PROSE_IS_PARAPHRASE_NOT_TRANSCRIPTION,
    SECTION_3_CLASSIFIES_SIX_OF_THIRTEEN,
    TRANSCRIPTION_FIDELITY_IS_NOT_AIM_TRUTH,
    AimEngagement,
    AimId,
    AimRecordCorrespondence,
    AimsDocumentLedger,
    AimsDocumentLedgerError,
    AttainmentStanding,
    BulletCensus,
    DeclaredAimBullet,
    DeclaredEngagementClass,
    ReadAimEntry,
    ReadBullet,
    ReadClassification,
    aims_document_path,
    correspond_records_to_document,
    load_aims_document,
    read_aims_document,
)
from alghanem.program import aims_document_ledger as reader_module
from alghanem.program.aims import DESIGN_SOURCE_OPEN_QUESTION

_ANSWER_MARKERS = (
    "answer",
    "verdict",
    "conclusion",
    "resolution",
    "decision",
    "outcome",
    "birth",
    "indicator",
    "score",
    "progress",
    "count",
    "total",
)


def _bullet(label: DeclaredAimBullet, line: int) -> ReadBullet:
    return ReadBullet(label=label, body="نصّ", document_line=line)


def _full_entry(aim_id: AimId, line: int = 10) -> ReadAimEntry:
    return ReadAimEntry(
        aim_id=aim_id,
        title="عنوان",
        bullets=(
            _bullet(DeclaredAimBullet.QUESTION, line + 1),
            _bullet(DeclaredAimBullet.ATTAINMENT, line + 2),
            _bullet(DeclaredAimBullet.NOT_ATTAINMENT, line + 3),
            _bullet(DeclaredAimBullet.CITATION, line + 4),
        ),
        document_line=line,
    )


def test_the_real_aims_document_is_read_without_any_refusal() -> None:
    ledger = load_aims_document()
    assert ledger.entry_count == len(AIM_RECORDS)
    assert tuple(entry.aim_id for entry in ledger.entries) == tuple(AIM_RECORDS)


def test_the_document_path_points_at_the_tracked_aims_file() -> None:
    path = aims_document_path()
    assert path.name == "AIMS.md"
    assert path.is_file()


def test_every_read_aim_carries_the_four_bullets_the_document_declares() -> None:
    ledger = load_aims_document()
    for entry in ledger.entries:
        labels = {bullet.label for bullet in entry.bullets}
        assert DeclaredAimBullet.QUESTION in labels
        assert DeclaredAimBullet.NOT_ATTAINMENT in labels
        assert DeclaredAimBullet.CITATION in labels
        assert len([label for label in labels if label.declares_attainment]) == 1


def test_the_one_aim_with_a_partial_attainment_is_read_as_partial() -> None:
    ledger = load_aims_document()
    partial = [
        entry.aim_id
        for entry in ledger.entries
        if entry.declared_attainment
        is AttainmentStanding.PARTIALLY_REACHED_WITH_NAMED_REMAINDER
    ]
    assert partial == [AimId.X1]
    entry = ledger.entry(AimId.X1)
    assert entry.bullet(DeclaredAimBullet.NAMED_REMAINDER) is not None
    assert entry.bullet(DeclaredAimBullet.ATTAINMENT) is None


def test_section_three_classifies_only_some_aims_and_the_rest_are_unclassified() -> (
    None
):
    ledger = load_aims_document()
    engagements = ledger.declared_engagements
    assert ledger.classified_count < ledger.entry_count
    unclassified = [
        aim
        for aim, standing in engagements.items()
        if standing is AimEngagement.UNCLASSIFIED_IN_RECORD
    ]
    assert unclassified
    assert ledger.classified_count + len(unclassified) == ledger.entry_count


def test_the_written_record_corresponds_to_the_document_it_was_copied_from() -> None:
    correspondence = correspond_records_to_document()
    assert correspondence.corresponded_count == len(AIM_RECORDS)
    for aim_id, record in AIM_RECORDS.items():
        entry = correspondence.ledger.entry(aim_id)
        assert record.attainment is entry.declared_attainment
        assert record.engagement is correspondence.ledger.declared_engagements[aim_id]


def test_a_record_whose_attainment_drifts_from_the_document_is_refused() -> None:
    ledger = load_aims_document()
    drifted = dict(AIM_RECORDS)
    drifted[AimId.K1] = replace(
        drifted[AimId.K1],
        attainment=AttainmentStanding.PARTIALLY_REACHED_WITH_NAMED_REMAINDER,
        named_remainder="بقيّةٌ مُختلَقة",
    )
    with pytest.raises(AimsDocumentLedgerError, match="بلوغٌ مُشتَقٌّ"):
        AimRecordCorrespondence(ledger=ledger, records=MappingProxyType(drifted))


def test_a_record_whose_engagement_drifts_from_section_three_is_refused() -> None:
    ledger = load_aims_document()
    drifted = dict(AIM_RECORDS)
    drifted[AimId.K4] = replace(
        drifted[AimId.K4], engagement=AimEngagement.UNCLASSIFIED_IN_RECORD
    )
    with pytest.raises(AimsDocumentLedgerError, match="انشغالٌ مُعلَنٌ"):
        AimRecordCorrespondence(ledger=ledger, records=MappingProxyType(drifted))


def test_a_record_missing_an_aim_the_document_declares_is_refused() -> None:
    ledger = load_aims_document()
    thinned = {
        aim: record for aim, record in AIM_RECORDS.items() if aim is not AimId.T3
    }
    with pytest.raises(AimsDocumentLedgerError, match="يخالف §٢"):
        AimRecordCorrespondence(ledger=ledger, records=MappingProxyType(thinned))


def test_a_record_reordered_against_the_document_is_refused() -> None:
    ledger = load_aims_document()
    reordered = dict(reversed(list(AIM_RECORDS.items())))
    with pytest.raises(AimsDocumentLedgerError, match="يخالف §٢"):
        AimRecordCorrespondence(ledger=ledger, records=MappingProxyType(reordered))


def test_a_bullet_label_outside_the_closed_vocabulary_halts_the_read() -> None:
    text = (
        "## ٢. الغايات\n\n"
        "### AIM-K1 — عنوان\n\n"
        "* السؤال: س\n"
        "* البلوغ: ب\n"
        "* ليس بلوغًا: ل\n"
        "* المستند: م\n"
        "* وسمٌ مُستحدَث: ش\n\n"
        "## ٣. أين نحن\n\n"
        "* **لم تبدأ**: AIM-K1\n\n"
        "## ٤. المؤشر\n"
    )
    with pytest.raises(AimsDocumentLedgerError, match="خارج المفردة المغلقة"):
        read_aims_document(text)


def test_an_engagement_class_outside_the_closed_vocabulary_halts_the_read() -> None:
    text = (
        "## ٢. الغايات\n\n"
        "### AIM-K1 — عنوان\n\n"
        "* السؤال: س\n"
        "* البلوغ: ب\n"
        "* ليس بلوغًا: ل\n"
        "* المستند: م\n\n"
        "## ٣. أين نحن\n\n"
        "* **صنفٌ مُستحدَث**: AIM-K1\n\n"
        "## ٤. المؤشر\n"
    )
    with pytest.raises(AimsDocumentLedgerError, match="صنفٌ خارج المفردة"):
        read_aims_document(text)


def test_a_missing_section_is_a_named_refusal_not_an_empty_ledger() -> None:
    text = "## ٢. الغايات\n\n### AIM-K1 — عنوان\n\n* السؤال: س\n"
    with pytest.raises(AimsDocumentLedgerError, match="قسمٌ"):
        read_aims_document(text)


def test_a_missing_document_is_a_named_refusal_not_an_empty_ledger(
    tmp_path: Path,
) -> None:
    with pytest.raises(AimsDocumentLedgerError, match="تعذّرت قراءة"):
        load_aims_document(tmp_path / "لا-وجود-له.md")


def test_blank_document_text_is_refused() -> None:
    with pytest.raises(AimsDocumentLedgerError):
        read_aims_document("   \n")


def test_an_aim_missing_a_required_bullet_is_refused() -> None:
    with pytest.raises(AimsDocumentLedgerError, match="نقاطٌ لازمةٌ غائبة"):
        ReadAimEntry(
            aim_id=AimId.K1,
            title="عنوان",
            bullets=(
                _bullet(DeclaredAimBullet.QUESTION, 11),
                _bullet(DeclaredAimBullet.ATTAINMENT, 12),
                _bullet(DeclaredAimBullet.CITATION, 13),
            ),
            document_line=10,
        )


def test_an_aim_declaring_two_attainment_bullets_is_refused() -> None:
    with pytest.raises(AimsDocumentLedgerError, match="نقطةُ بلوغٍ واحدة"):
        ReadAimEntry(
            aim_id=AimId.K1,
            title="عنوان",
            bullets=(
                _bullet(DeclaredAimBullet.QUESTION, 11),
                _bullet(DeclaredAimBullet.ATTAINMENT, 12),
                _bullet(DeclaredAimBullet.ATTAINMENT_REACHED_TODAY, 13),
                _bullet(DeclaredAimBullet.NAMED_REMAINDER, 14),
                _bullet(DeclaredAimBullet.NOT_ATTAINMENT, 15),
                _bullet(DeclaredAimBullet.CITATION, 16),
            ),
            document_line=10,
        )


def test_a_remainder_bullet_without_a_partial_attainment_is_refused() -> None:
    with pytest.raises(AimsDocumentLedgerError, match="بقيّةٌ مُسمّاة بلا"):
        ReadAimEntry(
            aim_id=AimId.K1,
            title="عنوان",
            bullets=(
                _bullet(DeclaredAimBullet.QUESTION, 11),
                _bullet(DeclaredAimBullet.ATTAINMENT, 12),
                _bullet(DeclaredAimBullet.NAMED_REMAINDER, 13),
                _bullet(DeclaredAimBullet.NOT_ATTAINMENT, 14),
                _bullet(DeclaredAimBullet.CITATION, 15),
            ),
            document_line=10,
        )


def test_a_partial_attainment_without_a_named_remainder_is_refused() -> None:
    with pytest.raises(AimsDocumentLedgerError, match="بلا بقيّةٍ مُسمّاة"):
        ReadAimEntry(
            aim_id=AimId.K1,
            title="عنوان",
            bullets=(
                _bullet(DeclaredAimBullet.QUESTION, 11),
                _bullet(DeclaredAimBullet.ATTAINMENT_REACHED_TODAY, 12),
                _bullet(DeclaredAimBullet.NOT_ATTAINMENT, 13),
                _bullet(DeclaredAimBullet.CITATION, 14),
            ),
            document_line=10,
        )


def test_a_repeated_bullet_label_within_one_aim_is_refused() -> None:
    with pytest.raises(AimsDocumentLedgerError, match="وسمٌ مكرّر"):
        ReadAimEntry(
            aim_id=AimId.K1,
            title="عنوان",
            bullets=(
                _bullet(DeclaredAimBullet.QUESTION, 11),
                _bullet(DeclaredAimBullet.QUESTION, 12),
                _bullet(DeclaredAimBullet.ATTAINMENT, 13),
                _bullet(DeclaredAimBullet.NOT_ATTAINMENT, 14),
                _bullet(DeclaredAimBullet.CITATION, 15),
            ),
            document_line=10,
        )


def test_an_aim_repeated_in_the_document_is_refused() -> None:
    entries = (_full_entry(AimId.K1, 10), _full_entry(AimId.K1, 20))
    census = BulletCensus(
        bullets=tuple(bullet for entry in entries for bullet in entry.bullets)
    )
    with pytest.raises(AimsDocumentLedgerError, match="غايةٌ مكرّرة في §٢"):
        AimsDocumentLedger(
            entries=entries,
            classifications=(
                ReadClassification(
                    declared_class=DeclaredEngagementClass.NOT_STARTED,
                    aim_ids=(AimId.K1,),
                    document_line=40,
                ),
            ),
            bullets=census,
        )


def test_an_aim_classified_twice_in_section_three_is_refused() -> None:
    entry = _full_entry(AimId.K1, 10)
    with pytest.raises(AimsDocumentLedgerError, match="مُصنَّفة مرّتين"):
        AimsDocumentLedger(
            entries=(entry,),
            classifications=(
                ReadClassification(
                    declared_class=DeclaredEngagementClass.NOT_STARTED,
                    aim_ids=(AimId.K1,),
                    document_line=40,
                ),
                ReadClassification(
                    declared_class=DeclaredEngagementClass.BLOCKED_BY_NAMED_OBSTACLE,
                    aim_ids=(AimId.K1,),
                    document_line=41,
                ),
            ),
            bullets=BulletCensus(bullets=entry.bullets),
        )


def test_a_classified_aim_with_no_entry_in_section_two_is_refused() -> None:
    entry = _full_entry(AimId.K1, 10)
    with pytest.raises(AimsDocumentLedgerError, match="لا مدخلَ لها في §٢"):
        AimsDocumentLedger(
            entries=(entry,),
            classifications=(
                ReadClassification(
                    declared_class=DeclaredEngagementClass.NOT_STARTED,
                    aim_ids=(AimId.T3,),
                    document_line=40,
                ),
            ),
            bullets=BulletCensus(bullets=entry.bullets),
        )


def test_a_classification_row_naming_no_aim_is_refused() -> None:
    with pytest.raises(AimsDocumentLedgerError, match="بلا غاياتٍ"):
        ReadClassification(
            declared_class=DeclaredEngagementClass.NOT_STARTED,
            aim_ids=(),
            document_line=40,
        )


def test_asking_for_an_aim_absent_from_the_document_is_a_named_refusal() -> None:
    ledger = load_aims_document()
    entries = tuple(entry for entry in ledger.entries if entry.aim_id is not AimId.T3)
    trimmed = AimsDocumentLedger(
        entries=entries,
        classifications=ledger.classifications,
        bullets=ledger.bullets,
    )
    with pytest.raises(AimsDocumentLedgerError, match="لا مدخلَ في §٢"):
        trimmed.entry(AimId.T3)


def test_the_bullet_census_counts_every_bullet_the_document_carries() -> None:
    ledger = load_aims_document()
    from_entries = sum(len(entry.bullets) for entry in ledger.entries)
    assert ledger.bullets.bullet_count == from_entries
    questions = ledger.bullets.bullets_with_label(DeclaredAimBullet.QUESTION)
    assert len(questions) == ledger.entry_count


def test_bullets_out_of_document_order_are_refused() -> None:
    with pytest.raises(AimsDocumentLedgerError, match="ترتيب النقاط"):
        BulletCensus(
            bullets=(
                _bullet(DeclaredAimBullet.QUESTION, 20),
                _bullet(DeclaredAimBullet.ATTAINMENT, 10),
            )
        )


def test_a_blank_bullet_body_is_refused() -> None:
    with pytest.raises(AimsDocumentLedgerError, match="نصّ النقطة"):
        ReadBullet(label=DeclaredAimBullet.QUESTION, body="   ", document_line=10)


def test_a_non_positive_document_line_is_refused() -> None:
    with pytest.raises(AimsDocumentLedgerError, match="موضع النقطة"):
        ReadBullet(label=DeclaredAimBullet.QUESTION, body="نصّ", document_line=0)


def test_the_bullet_vocabulary_stays_the_six_labels_the_document_uses() -> None:
    assert [member.value for member in DeclaredAimBullet] == [
        "السؤال",
        "البلوغ",
        "البلوغ الحاصل اليوم",
        "ما بقي مفتوحًا فيها",
        "ليس بلوغًا",
        "المستند",
    ]


def test_the_two_declared_classes_map_onto_two_distinct_engagements() -> None:
    assert len(DeclaredEngagementClass) == 2
    mapped = {member.engagement for member in DeclaredEngagementClass}
    assert len(mapped) == 2
    assert AimEngagement.UNCLASSIFIED_IN_RECORD not in mapped


@pytest.mark.parametrize(
    "declaring_type",
    [
        ReadBullet,
        ReadAimEntry,
        ReadClassification,
        BulletCensus,
        AimsDocumentLedger,
        AimRecordCorrespondence,
    ],
)
def test_no_type_here_carries_an_answer_bearing_field(declaring_type: type) -> None:
    for item in fields(declaring_type):
        assert not any(marker in item.name for marker in _ANSWER_MARKERS), item.name


def test_the_correspondence_carries_no_pass_or_fail_field() -> None:
    names = {item.name for item in fields(AimRecordCorrespondence)}
    assert names == {"ledger", "records"}


def test_the_module_cites_its_direct_design_source() -> None:
    assert reader_module.__doc__ is not None
    assert DESIGN_SOURCE_OPEN_QUESTION in reader_module.__doc__
    assert DESIGN_SOURCE_OPEN_QUESTION in reader_module.DESIGN_SOURCE_CITATION_NOTE


def test_the_residuals_left_by_this_reader_are_named_not_hidden() -> None:
    assert set(AIMS_DOCUMENT_NAMED_RESIDUALS) == {
        RECORD_PROSE_IS_PARAPHRASE_NOT_TRANSCRIPTION,
        TRANSCRIPTION_FIDELITY_IS_NOT_AIM_TRUTH,
        SECTION_3_CLASSIFIES_SIX_OF_THIRTEEN,
    }
    assert all(text.strip() for text in AIMS_DOCUMENT_NAMED_RESIDUALS.values())
    with pytest.raises(TypeError):
        AIMS_DOCUMENT_NAMED_RESIDUALS["X"] = "y"  # type: ignore[index]


def test_this_reader_is_not_the_indicator_and_imports_no_other_reader() -> None:
    source = Path(reader_module.__file__ or "").read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module is not None:
            imported.add(node.module)
        elif isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
    assert not any(
        name.endswith(("constitution_ledger", "deferred_value_ledger"))
        for name in imported
    ), imported
    assert "ConstitutionLedger" not in imported
    assert not any(
        isinstance(node, ast.Name)
        and node.id in {"ConstitutionLedger", "DeferredValueLedger"}
        for node in ast.walk(tree)
    )


def test_no_kernel_module_reads_the_aims_document_reader() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        source = module.module_finder.find_spec(  # type: ignore[union-attr]
            module.name
        )
        assert source is not None and source.origin is not None
        text = Path(source.origin).read_text(encoding="utf-8")
        assert "alghanem.program" not in text, module.name
        assert "AimsDocumentLedger" not in text, module.name
        assert "AimRecordCorrespondence" not in text, module.name
