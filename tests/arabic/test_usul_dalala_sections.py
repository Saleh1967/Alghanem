"""اختباراتُ سقفِ أقسامِ أصولِ الدلالة الخمسة، وخريطةِ تغطيتها المُشتَقّة."""

from __future__ import annotations

import pkgutil
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic import (
    COVERAGE_IS_READ_FROM_THE_TREE_NOTE,
    FIVE_SECTIONS_ARE_CLOSED_NOTE,
    NASKH_TEXT_ARRIVED_NOTE,
    NASKH_TEXT_NOT_EXTRACTED_RESIDUAL,
    REJECTED_PROPOSALS,
    REQUESTED_SECTIONS_ARE_NOT_ATTESTED_NOTE,
    SECTION_CLOSURE_WORDING_NOT_TRANSCRIBED,
    SECTION_MODULES,
    AttributionOutcome,
    DalalaSection,
    ProposalRejection,
    RejectionGround,
    SectionCoding,
    UsulDalalaSectionsError,
    attribute_proposal,
    modules_of_section,
    read_sections,
)
from alghanem.arabic.usul_dalala_sections import USUL_DALALA_IS_NOT_A_GATE_NOTE

_MODULE = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "alghanem"
    / "arabic"
    / "usul_dalala_sections.py"
)


def test_the_sections_are_five_and_closed() -> None:
    assert len(DalalaSection) == 5
    assert len(SECTION_MODULES) == len(DalalaSection)
    assert "خمسة" in FIVE_SECTIONS_ARE_CLOSED_NOTE


def test_an_unattributed_proposal_is_refused_not_silently_admitted() -> None:
    outcome = attribute_proposal("بندٌ دلاليٌّ جديد", None)
    assert outcome is AttributionOutcome.مردود


def test_an_attributed_proposal_returns_to_its_section() -> None:
    outcome = attribute_proposal("تخصيصُ العام", DalalaSection.العموم_والخصوص)
    assert outcome is AttributionOutcome.مسند_إلى_قسم


def test_the_apparent_and_interpreted_precedent_is_recorded_by_name() -> None:
    names = {rejection.proposal for rejection in REJECTED_PROPOSALS}
    assert any("الظاهر" in name and "المؤو" in name for name in names)
    assert REJECTED_PROPOSALS


def test_a_rejection_returning_to_a_section_must_name_it() -> None:
    with pytest.raises(UsulDalalaSectionsError):
        ProposalRejection(
            proposal="بندٌ يُردُّ إلى قسمٍ قائم",
            statement="نصُّ الردّ",
            ground=RejectionGround.راجع_إلى_قسم_قائم,
            returns_to=None,
        )


def test_a_rejection_not_returning_to_a_section_may_not_name_one() -> None:
    with pytest.raises(UsulDalalaSectionsError):
        ProposalRejection(
            proposal="بندٌ لا يزيد شيئًا",
            statement="نصُّ الردّ",
            ground=RejectionGround.تمحل_لا_يزيد_شيئا,
            returns_to=DalalaSection.العموم_والخصوص,
        )


def test_the_coverage_is_read_from_the_tree_not_written_in_a_report() -> None:
    ledger = read_sections()
    coding = {reading.section: reading.coding for reading in ledger.readings}
    assert coding[DalalaSection.العموم_والخصوص] is SectionCoding.مُرمَّز
    assert coding[DalalaSection.المطلق_والمقيد] is SectionCoding.مُرمَّز
    assert coding[DalalaSection.الناسخ_والمنسوخ] is SectionCoding.مُرمَّز
    assert "الشجرة" in COVERAGE_IS_READ_FROM_THE_TREE_NOTE


def test_the_naskh_section_gained_its_module_when_its_text_arrived() -> None:
    """كان `غير_مُرمَّز` بعلّةٍ مُسمّاة، فصار `مُرمَّز` بارتفاع تلك العلّة نفسها.

    وانقلابُ القراءة جاء من الشجرة: وُضِعت الوحدةُ فقُرِئت، ولم يُحرَّر جدولُ
    تغطيةٍ ليقول إنّها مُرمَّزة.
    """

    assert modules_of_section(DalalaSection.الناسخ_والمنسوخ) == ("naskh_mansukh.py",)
    assert "NASKH" in NASKH_TEXT_ARRIVED_NOTE


def test_the_lifted_residual_is_kept_and_marked_lifted_not_erased() -> None:
    """البقيّةُ المرفوعةُ تبقى مكتوبةً: رفعُها حادثةٌ تُقرأ لا أثرٌ يُمحى."""

    assert "NASKH_TEXT_NOT_EXTRACTED" in NASKH_TEXT_NOT_EXTRACTED_RESIDUAL
    assert "مرفوعة" in NASKH_TEXT_NOT_EXTRACTED_RESIDUAL


def test_lifting_one_residual_did_not_lift_its_neighbour() -> None:
    """مجيءُ النصّ رفع «لا نصَّ له»، ولم يرفع «لم يُقابَل نصُّه» بطبعةٍ مُسمّاة."""

    assert "لم تُنقَل بحروفها" in SECTION_CLOSURE_WORDING_NOT_TRANSCRIBED
    assert "NASKH_WORDING_IS_SUPPLIED_NOT_COLLATED" in NASKH_TEXT_ARRIVED_NOTE


def test_every_declared_module_exists_in_the_tree() -> None:
    root = Path(__file__).resolve().parents[2] / "src" / "alghanem" / "arabic"
    for modules in SECTION_MODULES.values():
        for name in modules:
            assert (root / name).is_file(), name


def test_the_source_gap_of_the_closure_is_named_not_folded() -> None:
    assert "SECTION_CLOSURE_WORDING_NOT_TRANSCRIBED" in (
        SECTION_CLOSURE_WORDING_NOT_TRANSCRIBED
    )
    assert "«تسجيل» لا «شهادة»" in REQUESTED_SECTIONS_ARE_NOT_ATTESTED_NOTE


def test_the_module_declares_its_own_limits_by_name() -> None:
    assert "لا سلطة" in USUL_DALALA_IS_NOT_A_GATE_NOTE


def test_the_module_imports_no_kernel_authority() -> None:
    source = _MODULE.read_text(encoding="utf-8")
    imports = tuple(
        line for line in source.splitlines() if line.startswith(("import ", "from "))
    )
    assert imports
    assert not any("kernel" in line for line in imports)


def test_no_kernel_module_reads_this_registration() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        spec = module.module_finder.find_spec(module.name)  # type: ignore[union-attr]
        assert spec is not None and spec.origin is not None
        text = Path(spec.origin).read_text(encoding="utf-8")
        for name in ("usul_dalala_sections", "DalalaSection", "SectionCoverageLedger"):
            assert name not in text, (module.name, name)
