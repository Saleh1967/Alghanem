"""مدوّنتان مُعلَنتا الدور: ختمان لا يُقاس أحدُهما على الآخر، ورقمٌ يُسمّى مصدرَه.

تُثبِّت هذه الشواهدُ ستّة أمور: الدورُ والختمُ مُعلَنان قبل القراءة فالمدوّنتان
مفترقتان في الاثنين معًا، والموضعُ ليس شهادةً فبايتاتٌ مخالفةٌ في الموضع المسنون
تُرفَض ولا تُخطَّى، وغيابُ البايتات رفضُ إخراجٍ لا قيمةٌ افتراضيّة، ومقابلةُ
المدوّنتين تُرفَض عند أوّل محاولةٍ لا بعد خروج رقمٍ منها، وكلُّ رقمٍ مولَّدٍ في
الوديعة يُعاد توليدُه من القرص فيُقابَل المُودَعُ بالمقيس، والرابعُ — الختمُ
المنقول — يبقى موسومًا واردًا وإن طابق لأنّ الموافقةَ خبرٌ عنه لا تبديلٌ لجنس
دخوله.
"""

import hashlib
import os
from dataclasses import fields, replace
from pathlib import Path

import pytest

from alghanem.arabic.audit_corpus_deposit import (
    A_SIX_CHARACTER_AGREEMENT_IS_NOT_A_MATCH,
    AUDIT_CORPUS_ATTRIBUTION,
    AUDIT_CORPUS_NAMED_RESIDUALS,
    AUDIT_CORPUS_PATH_VARIABLE,
    AUDIT_CORPUS_RELATIVE_PATH,
    NO_FIGURE_IS_COPIED_FROM_A_DISPLAY_INTO_A_DEPOSIT,
    THE_AUDIT_CORPUS,
    THE_AUDIT_CORPUS_FIGURES,
    THE_DECLARED_CORPORA,
    THE_MEASUREMENT_CORPUS,
    THE_SAME_FILE_NAME_IS_NOT_THE_SAME_BYTES,
    THE_SEAL_WAS_SOUGHT_IN_THE_WRONG_GENUS,
    TWO_SEALS_TWO_ROLES_AND_NEITHER_IS_MEASURED_AGAINST_THE_OTHER,
    AuditCorpusError,
    CorpusRole,
    CrossRoleReading,
    DeclaredCorpus,
    DepositedFigure,
    FigureProvenance,
    audit_corpus_bytes_are_resolvable,
    audit_corpus_path,
    git_blob_sha1,
    read_audit_corpus_bytes,
    refuse_to_read_one_against_the_other,
    regenerate_every_generated_figure,
    the_quoted_incoming_seal,
    the_quoted_seal_agreement_length,
    the_quoted_seal_is_a_prefix_of_the_generated_digest,
    vendored_audit_corpus_path,
)
from alghanem.arabic.masaq_corpus_deposit import SANCTIONED_DEPOSIT_FILENAMES


def test_the_two_corpora_differ_in_seal_and_in_role_together() -> None:
    """ختمان مختلفان ودوران مختلفان معلَنان؛ ولا يكفي أحدُ الفرقين."""

    assert len(THE_DECLARED_CORPORA) == 2
    assert THE_MEASUREMENT_CORPUS.role is CorpusRole.MEASUREMENT_CORPUS
    assert THE_AUDIT_CORPUS.role is CorpusRole.AUDIT_CORPUS
    assert THE_MEASUREMENT_CORPUS.sha256_hex != THE_AUDIT_CORPUS.sha256_hex
    assert THE_MEASUREMENT_CORPUS.byte_length != THE_AUDIT_CORPUS.byte_length
    assert len({corpus.role for corpus in THE_DECLARED_CORPORA}) == 2


def test_the_deposited_name_carries_its_source_and_does_not_collide() -> None:
    """الاسمُ المنبعيُّ واحدٌ، فالمُودَعُ سُمِّي بمصدره لئلّا يُطيح بالأوّل صمتًا."""

    assert THE_AUDIT_CORPUS.name != THE_MEASUREMENT_CORPUS.name
    assert THE_AUDIT_CORPUS.name in SANCTIONED_DEPOSIT_FILENAMES
    assert THE_MEASUREMENT_CORPUS.name in SANCTIONED_DEPOSIT_FILENAMES
    assert THE_AUDIT_CORPUS.name.endswith(THE_MEASUREMENT_CORPUS.name)


def test_the_attribution_is_a_licence_condition_not_an_ornament() -> None:
    """الإسنادُ يُسمّي المستودعَ ومنبعَه ووصفَ النسخ، ولا يخرج رقمٌ بحذفه."""

    assert THE_AUDIT_CORPUS.attribution == AUDIT_CORPUS_ATTRIBUTION
    assert "GlobalQuran" in AUDIT_CORPUS_ATTRIBUTION
    assert "Tanzil" in AUDIT_CORPUS_ATTRIBUTION
    assert THE_AUDIT_CORPUS.sha256_hex in AUDIT_CORPUS_ATTRIBUTION


def test_no_type_here_carries_a_verdict_or_verified_field() -> None:
    """الحكمُ مُشتَقٌّ لا مكتوب: لا حقلَ `verdict` ولا `verified` في الوديعة."""

    for datatype in (DeclaredCorpus, DepositedFigure):
        names = {field.name for field in fields(datatype)}
        assert not any(
            token in name
            for name in names
            for token in ("verdict", "verified", "holds", "agrees")
        )


def test_an_empty_field_is_refused_at_construction() -> None:
    """المفرداتُ مغلقةٌ والنصوصُ لازمة؛ والرفضُ عند الإنشاء لا عند الاستعمال."""

    with pytest.raises(AuditCorpusError):
        replace(THE_AUDIT_CORPUS, attribution="   ")
    with pytest.raises(AuditCorpusError):
        replace(THE_AUDIT_CORPUS, byte_length=0)
    with pytest.raises(AuditCorpusError):
        DepositedFigure(
            name="بلا قيمة",
            value="",
            provenance=FigureProvenance.GENERATED_FROM_THE_DISK_AT_DEPOSIT,
        )


def test_the_resolution_order_is_passed_then_declared_then_vendored(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """ثلاثةُ أبوابٍ بترتيبها، ولا رابعَ يُخمَّن من مجلَّد العمل."""

    passed = tmp_path / "مُمرَّر.txt"
    declared = tmp_path / "مُصرَّح.txt"
    passed.write_bytes(b"x")
    declared.write_bytes(b"y")
    monkeypatch.setenv(AUDIT_CORPUS_PATH_VARIABLE, str(declared))
    assert audit_corpus_path(passed) == passed
    assert audit_corpus_path() == declared
    monkeypatch.delenv(AUDIT_CORPUS_PATH_VARIABLE, raising=False)
    assert audit_corpus_path() == vendored_audit_corpus_path()
    assert vendored_audit_corpus_path().is_absolute()
    assert vendored_audit_corpus_path().as_posix().endswith(AUDIT_CORPUS_RELATIVE_PATH)


def test_absence_of_the_bytes_is_a_refusal_and_not_a_default(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """غيابُ الثلاثة رفضٌ صريح، والقراءةُ من مسارٍ لا ملفَّ فيه رفضٌ كذلك."""

    monkeypatch.setenv(AUDIT_CORPUS_PATH_VARIABLE, str(tmp_path / "ليس-هنا.txt"))
    assert audit_corpus_bytes_are_resolvable() is False
    with pytest.raises(AuditCorpusError):
        read_audit_corpus_bytes()
    with pytest.raises(AuditCorpusError):
        regenerate_every_generated_figure()


def test_a_file_in_the_sanctioned_place_is_still_matched_against_the_seal(
    tmp_path: Path,
) -> None:
    """الموضعُ ليس شهادة: بايتاتٌ مخالفةٌ تُرفَض ولا تُخطَّى، والطولُ وحدَه لا يكفي."""

    wrong_length = tmp_path / "قصير.txt"
    wrong_length.write_bytes(b"\xef\xbb\xbf" * 3)
    with pytest.raises(AuditCorpusError, match="طولُ البايتات"):
        read_audit_corpus_bytes(wrong_length)

    same_length = tmp_path / "مطابقُ الطول.txt"
    same_length.write_bytes(b"\x00" * THE_AUDIT_CORPUS.byte_length)
    with pytest.raises(AuditCorpusError, match="بصمة"):
        read_audit_corpus_bytes(same_length)


def test_reading_one_corpus_against_the_other_is_refused_at_the_attempt() -> None:
    """الرفضُ عند أوّل محاولة؛ والمدوّنةُ مع نفسها تمرّ لأنّ الختمَ واحد."""

    with pytest.raises(CrossRoleReading):
        refuse_to_read_one_against_the_other(THE_MEASUREMENT_CORPUS, THE_AUDIT_CORPUS)
    with pytest.raises(CrossRoleReading):
        refuse_to_read_one_against_the_other(THE_AUDIT_CORPUS, THE_MEASUREMENT_CORPUS)
    refuse_to_read_one_against_the_other(THE_AUDIT_CORPUS, THE_AUDIT_CORPUS)
    assert issubclass(CrossRoleReading, AuditCorpusError)


def test_two_corpora_of_one_role_but_two_seals_are_refused_as_well() -> None:
    """لا استثناءَ للدور الواحد: اختلافُ الختم وحدَه مانعٌ من المقابلة."""

    twin = replace(THE_AUDIT_CORPUS, sha256_hex="0" * 64)
    assert twin.role is THE_AUDIT_CORPUS.role
    with pytest.raises(CrossRoleReading):
        refuse_to_read_one_against_the_other(THE_AUDIT_CORPUS, twin)


def test_the_git_blob_seal_is_computed_here_and_not_transcribed() -> None:
    """ختمُ كائن git يُحسَب من ترويسةٍ وبايتات، ويُطابَق بتنفيذٍ مستقلٍّ ههنا."""

    data = b"the quick brown fox"
    expected = hashlib.sha1(
        b"blob %d\x00" % len(data) + data, usedforsecurity=False
    ).hexdigest()
    assert git_blob_sha1(data) == expected


def test_every_generated_figure_is_regenerated_from_the_quoted_one() -> None:
    """ثلاثةٌ مولَّدةٌ وواحدٌ واردٌ، ولا يُخلَط الجنسان في عدٍّ واحد."""

    generated = [figure for figure in THE_AUDIT_CORPUS_FIGURES if figure.is_generated]
    quoted = [figure for figure in THE_AUDIT_CORPUS_FIGURES if not figure.is_generated]
    assert len(generated) == 3
    assert len(quoted) == 1
    assert quoted[0].provenance is FigureProvenance.QUOTED_INCOMING_NOT_REPRODUCED
    assert len({figure.name for figure in THE_AUDIT_CORPUS_FIGURES}) == 4


@pytest.mark.skipif(
    not audit_corpus_bytes_are_resolvable(),
    reason="بايتاتُ مدوّنة التدقيق غيرُ محلولةٍ في هذه البيئة",
)
def test_the_deposited_figures_match_what_the_disk_generates_today() -> None:
    """كلُّ رقمٍ مولَّدٍ يُعاد من القرص فيُقابَل المُودَعُ بالمقيس لا بالمنقول."""

    regenerated = regenerate_every_generated_figure()
    for figure in THE_AUDIT_CORPUS_FIGURES:
        if figure.is_generated:
            assert regenerated[figure.name] == figure.value
    assert set(regenerated) == {
        figure.name for figure in THE_AUDIT_CORPUS_FIGURES if figure.is_generated
    }


@pytest.mark.skipif(
    not audit_corpus_bytes_are_resolvable(),
    reason="بايتاتُ مدوّنة التدقيق غيرُ محلولةٍ في هذه البيئة",
)
def test_the_quoted_seal_agrees_in_six_characters_and_is_not_a_prefix() -> None:
    """المنقولُ يقارب المولَّدَ ولا يطابقه؛ والمقاربةُ عددٌ يُخرَج لا حكمٌ يُكتَب."""

    assert the_quoted_seal_is_a_prefix_of_the_generated_digest() is False
    assert the_quoted_seal_agreement_length() == 6
    quoted = the_quoted_incoming_seal()
    assert len(quoted.value) == 7
    assert regenerate_every_generated_figure()["بصمةُ SHA-256"][:6] == quoted.value[:6]


@pytest.mark.skipif(
    not audit_corpus_bytes_are_resolvable(),
    reason="بايتاتُ مدوّنة التدقيق غيرُ محلولةٍ في هذه البيئة",
)
def test_a_near_agreement_does_not_promote_the_quoted_figure_to_measured() -> None:
    """لا يُرقّى واردٌ إلى مولَّدٍ بمقاربة، ولا يُطرَح بها من الوديعة."""

    quoted = the_quoted_incoming_seal()
    assert quoted.is_generated is False
    assert quoted.provenance is FigureProvenance.QUOTED_INCOMING_NOT_REPRODUCED
    assert quoted.value not in regenerate_every_generated_figure().values()


@pytest.mark.skipif(
    not audit_corpus_bytes_are_resolvable(),
    reason="بايتاتُ مدوّنة التدقيق غيرُ محلولةٍ في هذه البيئة",
)
def test_the_read_bytes_carry_the_declared_length_and_digest() -> None:
    """القراءةُ لا تُسلِّم بايتاتٍ إلّا بعد مطابقة الطول والبصمة معًا."""

    data = read_audit_corpus_bytes()
    assert len(data) == THE_AUDIT_CORPUS.byte_length
    assert hashlib.sha256(data).hexdigest() == THE_AUDIT_CORPUS.sha256_hex
    assert hashlib.sha256(data).hexdigest() != THE_MEASUREMENT_CORPUS.sha256_hex


def test_the_named_residuals_open_with_their_own_key() -> None:
    """كلُّ باقٍ مُسمًّى يفتتح نصَّه باسمه، وأربعتُها مُدرَجةٌ في الخارطة."""

    assert set(AUDIT_CORPUS_NAMED_RESIDUALS) == {
        "TWO_SEALS_TWO_ROLES_AND_NEITHER_IS_MEASURED_AGAINST_THE_OTHER",
        "THE_SAME_FILE_NAME_IS_NOT_THE_SAME_BYTES",
        "NO_FIGURE_IS_COPIED_FROM_A_DISPLAY_INTO_A_DEPOSIT",
        "THE_SEAL_WAS_SOUGHT_IN_THE_WRONG_GENUS",
        "A_SIX_CHARACTER_AGREEMENT_IS_NOT_A_MATCH",
    }
    for key, text in AUDIT_CORPUS_NAMED_RESIDUALS.items():
        assert text.startswith(f"{key}: ")
    assert TWO_SEALS_TWO_ROLES_AND_NEITHER_IS_MEASURED_AGAINST_THE_OTHER.startswith(
        "TWO_SEALS_TWO_ROLES"
    )
    assert "16,796" in NO_FIGURE_IS_COPIED_FROM_A_DISPLAY_INTO_A_DEPOSIT
    assert "8b387e8" in THE_SEAL_WAS_SOUGHT_IN_THE_WRONG_GENUS
    assert "quran-simple-enhanced.txt" in THE_SAME_FILE_NAME_IS_NOT_THE_SAME_BYTES
    assert "ستّة" in A_SIX_CHARACTER_AGREEMENT_IS_NOT_A_MATCH


def test_the_module_imports_neither_kernel_nor_program() -> None:
    """الوحدةُ خاملةٌ سلطويًّا: لا تستورد `kernel/` ولا `program/`."""

    source = (
        vendored_audit_corpus_path().parent.parent
        / "src"
        / "alghanem"
        / "arabic"
        / "audit_corpus_deposit.py"
    ).read_text(encoding="utf-8")
    assert "alghanem.kernel" not in source
    assert "alghanem.program" not in source


def test_the_path_variable_is_read_from_the_environment_by_that_exact_name(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """اسمُ المتغيّر معلَنٌ في الوديعة، وهو الذي يُقرأ لا اسمٌ قريبٌ منه."""

    assert AUDIT_CORPUS_PATH_VARIABLE == "ALGHANEM_AUDIT_CORPUS_PATH"
    elsewhere = tmp_path / "هناك.txt"
    elsewhere.write_bytes(b"z")
    monkeypatch.setitem(os.environ, AUDIT_CORPUS_PATH_VARIABLE, str(elsewhere))
    assert audit_corpus_path() == elsewhere
