"""اختباراتُ مسح الطريق المعجميّ: الجوابُ من نقيضةٍ واحدة، والحدودُ مُسمّاة."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from alghanem.arabic.level_two_manat import CARD_COMPOSITION_RELATION_KEY
from alghanem.arabic.lexical_path_census import (
    NAMED_RESIDUALS,
    CardLexicalPathReading,
    LexicalPathCensus,
    LexicalPathCensusError,
    LexicalPathStanding,
    QaydCoOccurrence,
    derive_lexical_path_standing,
    read_lexical_path_census,
)
from alghanem.arabic.lexical_transmission import (
    CARD_LEXICAL_PATH_KEY,
    LexicalCitationStructure,
)

_ROOT = Path(__file__).resolve().parents[2]


def _reading(
    name: str,
    co_occurrence: QaydCoOccurrence,
    attributions: tuple[str, ...] = (),
) -> CardLexicalPathReading:
    return CardLexicalPathReading(
        card_relative_path=name,
        declared_keys=("الإسنادات", "المادة", "المصدر"),
        attributions_declared=attributions,
        qayd_co_occurrence=co_occurrence,
    )


def test_the_variable_is_answered_read_in_its_own_right() -> None:
    census = read_lexical_path_census(_ROOT)
    assert census.standing is LexicalPathStanding.يقرأ_في_نفسه


def test_one_counter_instance_suffices_and_the_ratio_does_not_matter() -> None:
    """لو كانت النسبةُ واحدًا إلى كثيرٍ لما تغيّر المُشتَقّ؛ فالحاسمُ الوجودُ."""

    lone = (
        _reading("a", QaydCoOccurrence.بلا_نسبة_تركيب),
        _reading("b", QaydCoOccurrence.مع_نسبة_تركيب),
        _reading("c", QaydCoOccurrence.مع_نسبة_تركيب),
        _reading("d", QaydCoOccurrence.مع_نسبة_تركيب),
    )
    assert derive_lexical_path_standing(lone) is LexicalPathStanding.يقرأ_في_نفسه


def test_dependency_stands_only_when_no_counter_instance_exists() -> None:
    readings = (
        _reading("a", QaydCoOccurrence.مع_نسبة_تركيب),
        _reading("b", QaydCoOccurrence.مع_نسبة_تركيب),
    )
    assert (
        derive_lexical_path_standing(readings)
        is LexicalPathStanding.تابع_لطريق_نقل_القيد
    )


def test_an_empty_tree_answers_neither_side() -> None:
    """خلوُّ الشجرة من إعلانٍ ليس شاهدًا على التبعيّة ولا على الاستقلال."""

    standing = derive_lexical_path_standing(())
    assert standing is LexicalPathStanding.غير_محسوم
    assert standing is not LexicalPathStanding.تابع_لطريق_نقل_القيد
    assert standing is not LexicalPathStanding.يقرأ_في_نفسه


def test_counter_instances_are_named_not_only_counted() -> None:
    census = read_lexical_path_census(_ROOT)
    assert census.counter_instances
    for name in census.counter_instances:
        assert name.startswith("examples/")


def test_declaring_the_path_is_not_walking_it() -> None:
    """أكثرُ المُعلِنين يُعلن بتعدادٍ خالٍ؛ والمسحُ يُسمّي ذلك ولا يطويه."""

    census = read_lexical_path_census(_ROOT)
    assert census.declared_but_empty
    assert set(census.declared_but_empty) <= set(
        reading.card_relative_path for reading in census.readings
    )
    assert "DECLARING_A_PATH_IS_NOT_WALKING_IT" in NAMED_RESIDUALS


def test_an_empty_declaration_still_counts_as_a_counter_instance() -> None:
    """الدعوى المُبطَلة دعوى **إعلان**، فيُبطلها إعلانٌ ولو كان تعدادُه خاليًا."""

    census = read_lexical_path_census(_ROOT)
    empty = set(census.declared_but_empty)
    assert empty
    assert empty <= set(census.counter_instances)


def test_schema_identity_is_recorded_at_its_limit() -> None:
    census = read_lexical_path_census(_ROOT)
    assert census.declared_key_shapes == (("الإسنادات", "المادة", "المصدر"),)
    assert "SCHEMA_IDENTITY_IS_NOT_SEMANTIC_INDEPENDENCE" in NAMED_RESIDUALS


def test_the_census_matches_the_cards_actually_in_the_tree() -> None:
    """المسحُ مقروءٌ من الشجرة لا من قائمةٍ مُجمَّدة، فيُطابَق بفحصٍ مستقلّ."""

    expected: set[str] = set()
    for path in sorted((_ROOT / "examples").rglob("*.yaml")):
        if CARD_LEXICAL_PATH_KEY in path.read_text(encoding="utf-8"):
            expected.add(path.relative_to(_ROOT).as_posix())
    census = read_lexical_path_census(_ROOT)
    assert {reading.card_relative_path for reading in census.readings} == expected
    assert "CARD_CORPUS_IS_NOT_FROZEN_BY_THIS_MODULE" in NAMED_RESIDUALS


def test_co_occurrence_is_read_from_the_card_not_assumed() -> None:
    census = read_lexical_path_census(_ROOT)
    for reading in census.readings:
        text = (_ROOT / reading.card_relative_path).read_text(encoding="utf-8")
        declares = CARD_COMPOSITION_RELATION_KEY in json.dumps(
            json.loads(text), ensure_ascii=False
        )
        expected = (
            QaydCoOccurrence.مع_نسبة_تركيب
            if declares
            else QaydCoOccurrence.بلا_نسبة_تركيب
        )
        assert reading.qayd_co_occurrence is expected


def test_no_vocabulary_was_widened_to_answer_the_variable() -> None:
    """الجبهةُ فُتِحت بجوابٍ، لا بعضوٍ جديدٍ في مفردةٍ قائمة."""

    assert len(LexicalCitationStructure) == 3
    assert len(LexicalPathStanding) == 3
    assert len(QaydCoOccurrence) == 2
    assert "NO_CITATION_STRUCTURE_IS_DERIVED_HERE" in NAMED_RESIDUALS


def test_the_registration_of_the_front_was_not_rewritten() -> None:
    """مَن أجاب سؤالًا بتحرير موضع تسجيله أزاله ولم يُجِبه."""

    source = (
        _ROOT / "src" / "alghanem" / "arabic" / "qayd_marker_preregistration.py"
    ).read_text(encoding="utf-8")
    assert "LEXICAL_PATH_FRONT_IS_REGISTERED_NOT_OPENED" in source
    assert "أهو طريقٌ ثالثٌ يُقرأ في نفسه أم تابعٌ" in source


def test_only_one_shape_of_dependence_was_tested() -> None:
    assert "CO_OCCURRENCE_IS_NOT_THE_ONLY_SHAPE_OF_DEPENDENCE" in NAMED_RESIDUALS
    assert "THIS_TREE_IS_NOT_THE_WORLD" in NAMED_RESIDUALS


def test_no_written_answer_field_exists() -> None:
    for declaring in (CardLexicalPathReading, LexicalPathCensus):
        names = set(declaring.__dataclass_fields__)
        for forbidden in ("standing", "answer", "result", "verdict", "count"):
            assert not any(forbidden in name.lower() for name in names)


def test_duplicate_and_malformed_readings_are_refused() -> None:
    with pytest.raises(LexicalPathCensusError):
        LexicalPathCensus(
            readings=(
                _reading("a", QaydCoOccurrence.بلا_نسبة_تركيب),
                _reading("a", QaydCoOccurrence.مع_نسبة_تركيب),
            )
        )
    with pytest.raises(LexicalPathCensusError):
        _reading("", QaydCoOccurrence.بلا_نسبة_تركيب)
    with pytest.raises(LexicalPathCensusError):
        CardLexicalPathReading(
            card_relative_path="a",
            declared_keys=(),
            attributions_declared=(),
            qayd_co_occurrence="بلا_نسبة_تركيب",  # type: ignore[arg-type]
        )
    with pytest.raises(LexicalPathCensusError):
        derive_lexical_path_standing(
            [_reading("a", QaydCoOccurrence.بلا_نسبة_تركيب)]  # type: ignore[arg-type]
        )


def test_a_missing_tree_is_refused_not_read_as_no_cards() -> None:
    with pytest.raises(LexicalPathCensusError):
        read_lexical_path_census(_ROOT / "لا-يوجد")
