"""اختبارات اشتقاق اسم الشاهد: الإحالةُ إلى موضع الدليل تُشتَقّ ولا تُصدَّق."""

from __future__ import annotations

import pkgutil
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
import alghanem.program.witness_citation as witness_module
from alghanem.program.binary_outcome import GapClosureOutcome
from alghanem.program.witness_citation import (
    FABRICATED_WITNESS_NAME_DISCOVERY,
    WITNESS_CITATION_NAMED_RESIDUALS,
    CitationStanding,
    WitnessCitation,
    WitnessCitationError,
    audit_report_citations,
    cite_witness,
    derive_unsupported_citations,
    derive_witness_names,
    repository_root_path,
)

_AUDIT_TESTS = "tests/arabic/test_gflk_codec_revision_audit.py"
_REAL_WITNESS = "test_a_second_write_over_a_read_state_is_refused_not_absorbed"
_FABRICATED_WITNESS = "test_silent_overwrite_is_refused"


# --- الواقعةُ نفسُها، مُثبَّتةً تشغيلًا لا محكيّةً في تعليق --------------------


def test_the_fabricated_citation_is_refused_by_the_tree() -> None:
    """الاسمُ الذي أحال إليه التقرير غائبٌ عن ملفِّه المُسمّى، ويُقرأ غيابُه."""

    row = cite_witness(_FABRICATED_WITNESS, _AUDIT_TESTS)
    assert row.standing is CitationStanding.ABSENT_FROM_THE_NAMED_FILE
    assert not row.standing.is_supported_by_the_tree
    assert _FABRICATED_WITNESS not in row.derived_names


def test_the_real_witness_is_derived_from_the_named_file() -> None:
    """والشاهدُ القائم في موضعه يُشتَقّ من الملفّ نفسِه، فيقوم الفارق بينهما."""

    row = cite_witness(_REAL_WITNESS, _AUDIT_TESTS)
    assert row.standing is CitationStanding.DERIVED_FROM_THE_NAMED_FILE
    assert row.standing.is_supported_by_the_tree
    assert _REAL_WITNESS in row.derived_names


def test_the_fabricated_name_is_nowhere_in_the_test_tree() -> None:
    """ولا يقوم للاسم المُلفَّق موضعٌ في أيّ ملفِّ شواهدَ في الشجرة."""

    root = repository_root_path()
    for path in sorted((root / "tests").rglob("test_*.py")):
        names = derive_witness_names(str(path.relative_to(root)))
        assert names is not None
        assert _FABRICATED_WITNESS not in names


# --- الاشتقاق: قراءةٌ نحويّةٌ لا استيرادٌ ولا تشغيل ---------------------------


def test_names_are_derived_without_importing_the_file(tmp_path: Path) -> None:
    """ملفٌّ يرفع عند الاستيراد تُقرأ أسماؤه، فالقراءةُ ليست تشغيلًا."""

    module = tmp_path / "test_raises_on_import.py"
    module.write_text(
        'raise RuntimeError("importing me is not reading me")\n'
        "def test_written_here() -> None:\n    pass\n",
        encoding="utf-8",
    )
    assert derive_witness_names(module.name, root=tmp_path) == ("test_written_here",)


def test_a_file_outside_the_tree_is_refused_not_read(tmp_path: Path) -> None:
    with pytest.raises(WitnessCitationError):
        derive_witness_names("../outside.py", root=tmp_path)


def test_an_absolute_path_is_refused(tmp_path: Path) -> None:
    with pytest.raises(WitnessCitationError):
        derive_witness_names(str(tmp_path / "test_x.py"), root=tmp_path)


def test_a_file_that_does_not_parse_is_refused_not_read_as_empty(
    tmp_path: Path,
) -> None:
    (tmp_path / "test_broken.py").write_text("def (:\n", encoding="utf-8")
    with pytest.raises(WitnessCitationError):
        derive_witness_names("test_broken.py", root=tmp_path)


def test_a_missing_file_is_not_an_empty_file(tmp_path: Path) -> None:
    """غيابُ الملفّ يُرَدّ `None`، وخلوُّ ملفٍّ قائمٍ يُرَدّ صفًّا خاليًا."""

    assert derive_witness_names("test_absent.py", root=tmp_path) is None
    (tmp_path / "test_empty.py").write_text(
        "def helper() -> None:\n    pass\n", "utf-8"
    )
    assert derive_witness_names("test_empty.py", root=tmp_path) == ()


def test_the_missing_file_standing_is_separate_from_the_missing_name(
    tmp_path: Path,
) -> None:
    row = cite_witness("test_anything", "test_absent.py", root=tmp_path)
    assert row.standing is CitationStanding.FILE_NOT_IN_THE_TREE
    assert row.derived_names == ()


def test_a_witness_nested_in_a_class_is_derived(tmp_path: Path) -> None:
    (tmp_path / "test_nested.py").write_text(
        "class TestGroup:\n    def test_inside(self) -> None:\n        pass\n", "utf-8"
    )
    assert derive_witness_names("test_nested.py", root=tmp_path) == ("test_inside",)


# --- الصفّ: لا يُخالف حكمُه ما اشتُقّ منه ------------------------------------


def test_a_row_claiming_derivation_without_the_name_is_refused() -> None:
    with pytest.raises(WitnessCitationError):
        WitnessCitation(
            claimed_name="test_x",
            relative_path=_AUDIT_TESTS,
            standing=CitationStanding.DERIVED_FROM_THE_NAMED_FILE,
            derived_names=("test_y",),
        )


def test_a_row_claiming_absence_while_the_name_is_derived_is_refused() -> None:
    with pytest.raises(WitnessCitationError):
        WitnessCitation(
            claimed_name="test_x",
            relative_path=_AUDIT_TESTS,
            standing=CitationStanding.ABSENT_FROM_THE_NAMED_FILE,
            derived_names=("test_x",),
        )


def test_a_missing_file_row_carrying_derived_names_is_refused() -> None:
    with pytest.raises(WitnessCitationError):
        WitnessCitation(
            claimed_name="test_x",
            relative_path="tests/absent.py",
            standing=CitationStanding.FILE_NOT_IN_THE_TREE,
            derived_names=("test_x",),
        )


def test_a_blank_name_or_path_is_refused() -> None:
    with pytest.raises(WitnessCitationError):
        cite_witness("  ", _AUDIT_TESTS)
    with pytest.raises(WitnessCitationError):
        cite_witness("test_x", "   ")


# --- التقرير: صفٌّ لكلّ إحالةٍ فيه، ولا يُختصَر إلى كلمة ---------------------


def test_a_report_is_read_row_by_row_and_its_unsupported_rows_are_named() -> None:
    rows = audit_report_citations(
        [
            (_REAL_WITNESS, _AUDIT_TESTS),
            (_FABRICATED_WITNESS, _AUDIT_TESTS),
            ("test_anything", "tests/arabic/test_absent_file.py"),
        ]
    )
    assert [row.standing for row in rows] == [
        CitationStanding.DERIVED_FROM_THE_NAMED_FILE,
        CitationStanding.ABSENT_FROM_THE_NAMED_FILE,
        CitationStanding.FILE_NOT_IN_THE_TREE,
    ]
    unsupported = derive_unsupported_citations(rows)
    assert [row.claimed_name for row in unsupported] == [
        _FABRICATED_WITNESS,
        "test_anything",
    ]


def test_a_citation_that_is_not_a_name_and_a_file_is_refused() -> None:
    with pytest.raises(WitnessCitationError):
        audit_report_citations([("test_x",)])  # type: ignore[list-item]


def test_unsupported_citations_refuses_what_is_not_a_row() -> None:
    with pytest.raises(WitnessCitationError):
        derive_unsupported_citations(["test_x"])  # type: ignore[list-item]


# --- السجلّ والحدّ ------------------------------------------------------------


def test_the_incident_is_recorded_in_the_second_outcome_class() -> None:
    assert (
        FABRICATED_WITNESS_NAME_DISCOVERY.outcome
        is GapClosureOutcome.DEEPER_LAYER_REVEALED
    )
    assert _FABRICATED_WITNESS in FABRICATED_WITNESS_NAME_DISCOVERY.narrowed_unknown
    assert _REAL_WITNESS in FABRICATED_WITNESS_NAME_DISCOVERY.narrowed_unknown


def test_every_named_residual_is_non_blank_and_carries_its_own_code() -> None:
    assert WITNESS_CITATION_NAMED_RESIDUALS
    for residual in WITNESS_CITATION_NAMED_RESIDUALS:
        code = residual.split(":")[0]
        assert code.strip()
        assert getattr(witness_module, code) == residual


def test_this_reader_is_not_read_by_any_kernel_module() -> None:
    for info in pkgutil.walk_packages(
        kernel_package.__path__, prefix=f"{kernel_package.__name__}."
    ):
        source = Path(
            repository_root_path(),
            "src",
            *info.name.split("."),
        ).with_suffix(".py")
        if not source.is_file():
            continue
        assert "witness_citation" not in source.read_text(encoding="utf-8")


def test_the_reader_imports_nothing_from_the_kernel_and_no_gate_reads_it() -> None:
    source = Path(witness_module.__file__).read_text(encoding="utf-8")
    assert "kernel" not in source.replace("`kernel/`", "")
    certainty = Path(
        repository_root_path(), "src/alghanem/program/direct_certainty.py"
    ).read_text(encoding="utf-8")
    assert "witness_citation" not in certainty
