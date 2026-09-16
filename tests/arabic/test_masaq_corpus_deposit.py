"""اختباراتُ إيداع MASAQ شاهدًا مُبصَّمًا وأرقامِه العشرين بقواعد عدّها.

والأسطرُ المكتوبةُ هنا **مُصطنَعةٌ مُصرَّحٌ بجنسها**: بايتاتُ المدوَّنة غيرُ
منسوخةٍ إلى هذه الشجرة، والمُحاكى بنيةُ الصفّ وحدَها — ترويسةٌ، وسجلٌّ فيه
فاصلُ سطرٍ داخل حقلٍ مُقتبَس، ومقاطعُ كلمةٍ واحدةٍ تحمل `Word_No` مكرَّرًا.
ولا يُقرأ من سطرٍ مُصطنَعٍ رقمٌ عن المدوَّنة البتّة؛ أرقامُها كلُّها من
البايتات المُبصَّمة، وإعادةُ اشتقاقها اختبارٌ يُفعَّل ببايتات `corpora/MASAQ.csv`
المُودَعة في الشجرة، أو بمسارٍ يُصرَّح به في `ALGHANEM_MASAQ_PATH`.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

import pytest

from alghanem.arabic.masaq_corpus_deposit import (
    DEPOSITED_DERIVED_NOUN_COUNTS,
    DEPOSITED_EMBEDDED_NEWLINE_BREAKS,
    DEPOSITED_EMBEDDED_NEWLINE_RECORDS,
    DEPOSITED_LINE_COUNT,
    DEPOSITED_RECORD_COUNT,
    DERIVED_NOUN_TAGS,
    MASAQ_ATTRIBUTION,
    MASAQ_BYTE_LENGTH,
    MASAQ_DEPOSIT_NAMED_RESIDUALS,
    MASAQ_DOI,
    MASAQ_LICENCE,
    MASAQ_PATH_VARIABLE,
    MASAQ_REDERIVED_FIGURES,
    MASAQ_RELATIVE_PATH,
    MASAQ_SHA256,
    MIRROR_CORROBORATION,
    MORPH_TAG_COLUMN,
    SEGMENT_INDEX_COLUMN,
    WORD_KEY_COLUMN,
    MasaqDepositError,
    MirrorCorroboration,
    RederivedFigure,
    deposit_place_is_clean,
    figures_named,
    lines_are_conserved,
    masaq_path,
    masaq_records,
    read_masaq_bytes,
    rederive_embedded_newline_breaks,
    rederive_embedded_newline_records,
    rederive_line_count,
    rederive_record_count,
    rederive_tag_count,
    unsanctioned_deposit_files,
    vendored_masaq_path,
)

SYNTHETIC_HEADER = "ID,Sura_No,Verse_No,Word_No,Column5,Morph_Tag,Gloss"
"""ترويسةٌ مُصطنَعةٌ تحمل الأعمدةَ المُعلَنة وحدَها؛ ليست ترويسةَ الملفّ الحقيقيّ."""

SYNTHETIC_ROWS = (
    "1,1,1,1,1,PREP,in-(the)-name",
    "1,1,1,2,1,GERUND,name",
    "2,1,1,1,2,NOUN_ACTIVE_PART,merciful",
    "3,1,2,1,3,GERUND_MEEM,a-standing",
    '4,1,3,1,4,GERUND,"a gloss that carries\na line break inside a quoted field"',
    "5,1,4,1,5,NOUN_DIMINUTIVE,a-little-one",
)

SYNTHETIC_CSV = "\n".join((SYNTHETIC_HEADER, *SYNTHETIC_ROWS)) + "\n"
SYNTHETIC_BYTES = SYNTHETIC_CSV.encode("utf-8")


def test_the_deposit_carries_twenty_figures_each_with_a_counting_rule() -> None:
    assert len(MASAQ_REDERIVED_FIGURES) == 20
    names = [figure.name for figure in MASAQ_REDERIVED_FIGURES]
    assert len(set(names)) == len(names)
    for figure in MASAQ_REDERIVED_FIGURES:
        assert figure.counting_rule.strip()
        assert figure.what_it_does_not_establish.strip()
        assert callable(figure.derive)


def test_a_figure_without_a_counting_rule_cannot_be_constructed() -> None:
    with pytest.raises(MasaqDepositError):
        RederivedFigure(
            name="رقمٌ بلا قاعدة",
            deposited=1,
            counting_rule="   ",
            what_it_does_not_establish="حدٌّ مكتوب",
            derive=len,
        )


def test_a_figure_without_a_written_limit_cannot_be_constructed() -> None:
    with pytest.raises(MasaqDepositError):
        RederivedFigure(
            name="رقمٌ بلا حدّ",
            deposited=1,
            counting_rule="قاعدةٌ مكتوبة",
            what_it_does_not_establish="",
            derive=len,
        )


def test_the_fourteen_derived_noun_tags_are_deposited_with_their_counts() -> None:
    assert len(DERIVED_NOUN_TAGS) == 14
    assert DEPOSITED_DERIVED_NOUN_COUNTS["GERUND"] == 4_216
    assert DEPOSITED_DERIVED_NOUN_COUNTS["GERUND_MEEM"] == 125
    assert DEPOSITED_DERIVED_NOUN_COUNTS["NOUN_DIMINUTIVE"] == 1
    assert sum(DEPOSITED_DERIVED_NOUN_COUNTS.values()) == 11_245
    for item in DERIVED_NOUN_TAGS:
        figure = figures_named([f"{item.arabic_name} — {item.tag}"])[0]
        assert figure.deposited == item.deposited_count


def test_an_unnamed_figure_is_refused_rather_than_skipped() -> None:
    with pytest.raises(MasaqDepositError):
        figures_named(["رقمٌ لا وجودَ له"])


def test_embedded_newline_makes_line_count_exceed_record_count() -> None:
    """قاعدتان مشروعتان تُعطيان عددين، والفرقُ مقيسٌ لا مُقدَّر."""

    lines = rederive_line_count(SYNTHETIC_BYTES)
    records = rederive_record_count(SYNTHETIC_BYTES)

    assert lines == len(SYNTHETIC_ROWS) + 2
    assert records == len(SYNTHETIC_ROWS)
    assert lines - records == 1 + rederive_embedded_newline_breaks(SYNTHETIC_BYTES)


def test_splitlines_hides_embedded_newlines_from_the_reader() -> None:
    """العطبُ الذي أمسكه الشاهد: الشقُّ قبل القراءة يُخفي الفواصلَ عن كلّ عدّ."""

    import csv

    split_first = [
        row for row in csv.reader(SYNTHETIC_BYTES.decode("utf-8").splitlines())
    ]
    hidden = sum(1 for row in split_first if any("\n" in field for field in row))
    assert hidden == 0

    assert rederive_embedded_newline_records(SYNTHETIC_BYTES) == 1
    assert rederive_embedded_newline_breaks(SYNTHETIC_BYTES) == 1


def test_a_record_may_carry_more_than_one_embedded_break() -> None:
    """ولذلك أُودِع عددُ الفواصل مع عددِ حامليها: ١٧٦ مقابل ١٥٤."""

    data = (SYNTHETIC_HEADER + "\n" + '6,1,5,1,6,GERUND,"one\ntwo\nthree"\n').encode(
        "utf-8"
    )

    assert rederive_embedded_newline_records(data) == 1
    assert rederive_embedded_newline_breaks(data) == 2
    assert DEPOSITED_EMBEDDED_NEWLINE_BREAKS > DEPOSITED_EMBEDDED_NEWLINE_RECORDS


def test_word_no_is_a_segment_index_not_a_word_index() -> None:
    """الخلطُ بينهما أهبط قياسَ دقّةٍ من ٢٣٫٣٪ إلى ٠٫٣٪ قبل أن يُمسَك."""

    records = masaq_records(SYNTHETIC_BYTES)
    first_word = [
        record
        for record in records
        if (record["Sura_No"], record["Verse_No"], record[WORD_KEY_COLUMN])
        == ("1", "1", "1")
    ]

    assert len(first_word) == 2
    assert [record[SEGMENT_INDEX_COLUMN] for record in first_word] == ["1", "2"]
    assert SEGMENT_INDEX_COLUMN != WORD_KEY_COLUMN


def test_a_tag_is_counted_by_equality_not_by_containment() -> None:
    """`GERUND_MEEM` ليس `GERUND`؛ ومن عدَّ بالاحتواء ضمَّ خمسةَ أبوابٍ في باب."""

    assert rederive_tag_count(SYNTHETIC_BYTES, "GERUND") == 2
    assert rederive_tag_count(SYNTHETIC_BYTES, "GERUND_MEEM") == 1
    assert rederive_tag_count(SYNTHETIC_BYTES, "NOUN_ACTIVE_PART") == 1


def test_an_untagged_category_counts_zero_and_zero_means_not_annotated_here() -> None:
    assert rederive_tag_count(SYNTHETIC_BYTES, "ADJ_INTENS") == 0
    assert (
        "AnImportedTagIsAHumanJudgementNotAMeasurement" in MASAQ_DEPOSIT_NAMED_RESIDUALS
    )


def test_a_missing_tag_column_stops_the_count_instead_of_sliding_to_a_neighbour() -> (
    None
):
    data = b"ID,Sura_No,Gloss\n1,1,in-(the)-name\n"

    with pytest.raises(MasaqDepositError):
        rederive_tag_count(data, "GERUND")


def test_every_line_is_accounted_for_without_remainder() -> None:
    """جردُ تغطيةٍ لا تصديقُ مضمون؛ والحدُّ مكتوبٌ في مُخلَّفٍ مُسمًّى."""

    assert lines_are_conserved(SYNTHETIC_BYTES)
    assert "AConservationAuditIsNotAnAccuracyClaim" in MASAQ_DEPOSIT_NAMED_RESIDUALS


def test_the_deposited_line_and_record_counts_differ_by_header_plus_breaks() -> None:
    assert DEPOSITED_LINE_COUNT - DEPOSITED_RECORD_COUNT == (
        1 + DEPOSITED_EMBEDDED_NEWLINE_BREAKS
    )


def test_bytes_are_refused_on_a_length_or_a_digest_mismatch(tmp_path: Path) -> None:
    impostor = tmp_path / "MASAQ.csv"
    impostor.write_bytes(SYNTHETIC_BYTES)

    with pytest.raises(MasaqDepositError):
        read_masaq_bytes(impostor)

    with pytest.raises(MasaqDepositError):
        read_masaq_bytes(tmp_path / "absent.csv")


def test_no_path_is_guessed_beyond_the_deposited_location(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """الموضعُ المسنونُ وحدَه يُجرَّب بلا تصريح؛ وغيابُه رفضٌ لا تخمين."""

    monkeypatch.delenv(MASAQ_PATH_VARIABLE, raising=False)

    if vendored_masaq_path().is_file():
        assert masaq_path() == vendored_masaq_path()
        return

    with pytest.raises(MasaqDepositError):
        read_masaq_bytes()


def test_the_deposited_location_is_resolved_from_the_tree_not_the_cwd(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.delenv(MASAQ_PATH_VARIABLE, raising=False)
    monkeypatch.chdir(tmp_path)

    assert vendored_masaq_path().is_absolute()
    assert vendored_masaq_path().as_posix().endswith(MASAQ_RELATIVE_PATH)
    assert MASAQ_RELATIVE_PATH == "corpora/MASAQ.csv"


def test_a_declared_path_outranks_the_deposited_location(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """الإيداعُ في الشجرة لا يُبطِل تصريحًا؛ والمُمرَّرُ يسبق البيئةَ ويسبقانه."""

    elsewhere = tmp_path / "MASAQ.csv"
    monkeypatch.setenv(MASAQ_PATH_VARIABLE, str(elsewhere))

    assert masaq_path() == elsewhere
    assert masaq_path(tmp_path / "passed.csv") == tmp_path / "passed.csv"


def test_the_deposited_location_is_no_certificate_of_the_bytes(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """ملفٌّ في الموضع الصحيح ببايتاتٍ أخرى مرفوضٌ كغيره: الموضعُ ليس بصمة."""

    impostor = tmp_path / "MASAQ.csv"
    impostor.write_bytes(SYNTHETIC_BYTES)
    monkeypatch.setenv(MASAQ_PATH_VARIABLE, str(impostor))

    with pytest.raises(MasaqDepositError):
        read_masaq_bytes()


def test_sha256_is_identity_not_order() -> None:
    """`Sha256OrdersNothing` مُنفَّذًا لا مُعادًا: ترتيبُ المدخلين لا يُورَّث."""

    assert b"a" < b"b"
    assert hashlib.sha256(b"a").hexdigest() > hashlib.sha256(b"b").hexdigest()
    assert b"1" < b"2"
    assert hashlib.sha256(b"1").hexdigest() < hashlib.sha256(b"2").hexdigest()
    assert "Sha256OrdersNothing" in MASAQ_DEPOSIT_NAMED_RESIDUALS


def test_one_changed_byte_changes_the_whole_digest() -> None:
    original = hashlib.sha256(SYNTHETIC_BYTES).hexdigest()
    altered = hashlib.sha256(
        SYNTHETIC_BYTES.replace(b"GERUND", b"gERUND", 1)
    ).hexdigest()

    shared_prefix = 0
    for left, right in zip(original, altered):
        if left != right:
            break
        shared_prefix += 1

    assert original != altered
    assert shared_prefix < 8


def test_the_attribution_is_a_licence_condition_carried_in_the_module() -> None:
    assert MASAQ_LICENCE == "CC BY 3.0"
    assert MASAQ_DOI in MASAQ_ATTRIBUTION
    assert "Sawalha" in MASAQ_ATTRIBUTION
    assert len(MASAQ_SHA256) == 64
    assert MASAQ_BYTE_LENGTH == 20_302_008
    assert MORPH_TAG_COLUMN in SYNTHETIC_HEADER


@pytest.mark.skipif(
    not os.environ.get(MASAQ_PATH_VARIABLE) and not vendored_masaq_path().is_file(),
    reason=(
        "the MASAQ bytes are absent from this checkout. Its CC BY 3.0 licence "
        f"permits depositing them at {MASAQ_RELATIVE_PATH}; until they are "
        f"there, set {MASAQ_PATH_VARIABLE} to the exact MASAQ.csv whose digest "
        "is deposited to re-derive all twenty figures here"
    ),
)
def test_all_twenty_figures_rederive_from_the_deposited_bytes() -> None:
    data = read_masaq_bytes()

    drifted = [
        figure.name for figure in MASAQ_REDERIVED_FIGURES if not figure.holds(data)
    ]

    assert drifted == []
    assert lines_are_conserved(data)


def test_the_synthetic_lines_are_declared_and_carry_no_corpus_figure() -> None:
    """ما خرج من هذه الأسطر رقمٌ عن المدوَّنة؛ وهو نصُّ `SyntheticLinesAreDeclared`."""

    assert "SyntheticLinesAreDeclaredNotHidden" in MASAQ_DEPOSIT_NAMED_RESIDUALS
    assert rederive_record_count(SYNTHETIC_BYTES) != DEPOSITED_RECORD_COUNT
    assert rederive_line_count(SYNTHETIC_BYTES) != DEPOSITED_LINE_COUNT
    assert (
        rederive_tag_count(SYNTHETIC_BYTES, "GERUND")
        != (DEPOSITED_DERIVED_NOUN_COUNTS["GERUND"])
    )


def test_a_mirror_with_another_digest_corroborates_but_is_not_these_bytes() -> None:
    """الأبوابُ الأربعةَ عشرَ طابقت في مرآةٍ أخرى، وستّةُ أرقامٍ خالفت؛ ولا تُخلَط."""

    assert MIRROR_CORROBORATION.mirror_sha256 != MASAQ_SHA256
    assert MIRROR_CORROBORATION.mirror_byte_length != MASAQ_BYTE_LENGTH
    assert set(MIRROR_CORROBORATION.figures_that_matched) == set(
        DEPOSITED_DERIVED_NOUN_COUNTS
    )
    assert len(MIRROR_CORROBORATION.figures_that_did_not) == 6
    assert "AMirrorWithAnotherDigestIsNotTheseBytes" in MASAQ_DEPOSIT_NAMED_RESIDUALS


def test_a_mirror_that_agrees_in_everything_is_not_recorded_as_a_corroboration() -> (
    None
):
    with pytest.raises(MasaqDepositError):
        MirrorCorroboration(
            mirror_byte_length=1,
            mirror_sha256="0" * 64,
            figures_that_matched=("GERUND",),
            figures_that_did_not=(),
            what_it_establishes="موافقةٌ تامّة",
            what_it_does_not_establish="حدٌّ مكتوب",
        )


def test_no_unsanctioned_file_sits_in_the_deposit_place() -> None:
    """موضعُ الإيداع لا يسكنه إلّا بيانُه وبايتاتُه باسمها المسنون.

    ورفعٌ فاشلٌ ينزل فيه باسمٍ آخرَ يُوهِم أنّ البايتات حاضرة، وهو ما وقع
    مرّتين في هذه الشجرة؛ فالمنعُ اختبارٌ لا تنبيهٌ في بيان.
    """

    strays = unsanctioned_deposit_files()
    assert strays == (), [path.name for path in strays]
    assert deposit_place_is_clean()
    assert "AFailedUploadIsNotADeposit" in MASAQ_DEPOSIT_NAMED_RESIDUALS


def test_a_stray_name_in_the_deposit_place_is_caught_before_any_digest(
    tmp_path: Path,
) -> None:
    """الاسمُ الطارئُ يُمسَك قبل المطابقة، فلا يُعتذَر له بقِصَرِ بايتاته."""

    (tmp_path / "README.md").write_text("بيانٌ مأذونٌ فيه", encoding="utf-8")
    (tmp_path / MASAQ_RELATIVE_PATH.rsplit("/", 1)[1]).write_bytes(b"")
    stray = tmp_path / "Masaq cor.txt"
    stray.write_bytes(b"\n")

    assert unsanctioned_deposit_files(tmp_path) == (stray,)
    assert not deposit_place_is_clean(tmp_path)


def test_an_absent_deposit_place_has_no_stray_files(tmp_path: Path) -> None:
    assert unsanctioned_deposit_files(tmp_path / "لا-وجودَ-له") == ()
