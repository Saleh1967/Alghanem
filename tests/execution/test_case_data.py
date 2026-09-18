"""`G0.CASE-0.DATA`: المدوّنةُ المكتوبةُ تُقرَأ من ملفّاتها ويُفحَص اتّساقُها الداخليّ.

    MATRIX  ≺  DATA  ≺  READOUT  ≺  DIGEST LEDGER

**ولا يُشغَّل المحرّكُ هنا**: هذه الطبقةُ تثبت أنّ الحالةَ مكتوبةٌ مشروعةُ
الاستشهاد متّسقةٌ مع نفسها ومع المصفوفة المجمَّدة؛ ولا تثبت أنّها بلغت الخليّةَ
التي ادّعتها. تلك دعوًى تبقى دعوًى إلى `G0.CASE-0.READOUT`.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from alghanem.execution.case_data import (
    CORPUS_ROOT_NAME,
    CaseDataError,
    DeclaredDifference,
    EngineSeamWitness,
    GoldenCaseCorpus,
    GoldenExecutionCase,
    GoldenExpectation,
    InvalidInputWitness,
)
from alghanem.execution.coverage import COVERAGE_MATRIX
from alghanem.execution.frozen_json import DiffOperation
from alghanem.execution.standing import InputFaultKind

_CORPUS_ROOT = Path(__file__).resolve().parents[2] / CORPUS_ROOT_NAME


def _read(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict), path.name
    return loaded


def _folder(name: str) -> tuple[tuple[str, dict[str, Any]], ...]:
    directory = _CORPUS_ROOT / name
    assert directory.is_dir(), name
    return tuple((path.stem, _read(path)) for path in sorted(directory.glob("*.json")))


def _corpus() -> GoldenCaseCorpus:
    return GoldenCaseCorpus.of(
        manifest=_read(_CORPUS_ROOT / "MANIFEST.json"),
        cases=tuple(item for _, item in _folder("cases")),
        expectations=tuple(item for _, item in _folder("expectations")),
        invalid_input_witnesses=tuple(item for _, item in _folder("invalid")),
        engine_seam_witnesses=tuple(item for _, item in _folder("seam")),
    )


def _expectation_document() -> dict[str, Any]:
    return deepcopy(_read(_CORPUS_ROOT / "expectations" / "case0.baseline.pass.json"))


def _case_document() -> dict[str, Any]:
    return deepcopy(_read(_CORPUS_ROOT / "cases" / "case0.baseline.pass.json"))


def _replace(path: str, before: Any, after: Any, statement: str) -> dict[str, Any]:
    return {
        "operation": "replace",
        "path": path,
        "before": before,
        "after": after,
        "statement": statement,
    }


def _add(path: str, after: Any, statement: str) -> dict[str, Any]:
    return {
        "operation": "add",
        "path": path,
        "before": None,
        "after": after,
        "statement": statement,
    }


def _remove(path: str, before: Any, statement: str) -> dict[str, Any]:
    return {
        "operation": "remove",
        "path": path,
        "before": before,
        "after": None,
        "statement": statement,
    }


def _second_anchor() -> dict[str, Any]:
    return {
        "anchor_id": "anchor.second",
        "role_site": {
            "linguistic_ontology_id": "linguistic.A",
            "license_id": "license.term",
            "function": "term_anchor_role",
        },
        "condition_site": {"base_id": "base.A", "place": "identity_criterion"},
    }


def _counter_case(
    case_id: str,
    differences: list[dict[str, Any]],
    multiplicity: str | None = None,
) -> dict[str, Any]:
    case = _case_document()
    case["case_id"] = case_id
    case["baseline_case_id"] = "case0.baseline.pass"
    case["declared_differences"] = differences
    case["multiplicity_is_the_proof"] = multiplicity
    return case


def _corpus_with(*cases: dict[str, Any]) -> GoldenCaseCorpus:
    expectations = []
    for case in cases:
        expectation = _expectation_document()
        expectation["case_id"] = case["case_id"]
        expectations.append(expectation)
    return GoldenCaseCorpus.of(
        manifest=_read(_CORPUS_ROOT / "MANIFEST.json"),
        cases=tuple(item for _, item in _folder("cases")) + cases,
        expectations=tuple(item for _, item in _folder("expectations"))
        + tuple(expectations),
        invalid_input_witnesses=tuple(item for _, item in _folder("invalid")),
        engine_seam_witnesses=tuple(item for _, item in _folder("seam")),
    )


def test_the_written_corpus_is_read_and_is_internally_consistent() -> None:
    corpus = _corpus()
    assert corpus.cases
    assert corpus.engine_seam_witnesses
    assert corpus.invalid_input_witnesses


def test_a_file_name_carries_the_identity_written_inside_it() -> None:
    for stem, document in _folder("cases"):
        assert stem == document["case_id"]
    for stem, document in _folder("expectations"):
        assert stem == document["case_id"]
    for folder in ("invalid", "seam"):
        for stem, document in _folder(folder):
            assert stem == document["witness_id"]


def test_what_is_not_covered_is_named_and_is_not_passed_over_in_silence() -> None:
    corpus = _corpus()
    coverage = corpus.coverage
    assert not coverage.is_complete
    assert coverage.uncovered_requirement_ids == (
        corpus.declared_uncovered_requirement_ids
    )
    required = {item.requirement_id for item in COVERAGE_MATRIX.required_cases}
    assert set(coverage.cited_requirement_ids) <= required
    assert set(coverage.uncovered_requirement_ids) <= required


def test_a_declared_residual_that_drifts_from_the_citations_is_refused() -> None:
    manifest = _read(_CORPUS_ROOT / "MANIFEST.json")
    manifest["uncovered_requirement_ids"] = []
    with pytest.raises(CaseDataError):
        GoldenCaseCorpus.of(
            manifest=manifest,
            cases=tuple(item for _, item in _folder("cases")),
            expectations=tuple(item for _, item in _folder("expectations")),
            invalid_input_witnesses=tuple(item for _, item in _folder("invalid")),
            engine_seam_witnesses=tuple(item for _, item in _folder("seam")),
        )


def test_an_expectation_that_carries_an_execution_digest_is_refused() -> None:
    document = _expectation_document()
    document["expected_execution_digest"] = None
    with pytest.raises(CaseDataError):
        GoldenExpectation.of(document)


def test_a_nested_readout_key_is_refused_wherever_it_hides() -> None:
    document = _expectation_document()
    document["expected_trace"][0]["execution_digest"] = "أيًّا كانت"
    with pytest.raises(CaseDataError):
        GoldenExpectation.of(document)


def test_an_expectation_pinned_to_another_matrix_is_refused() -> None:
    document = _expectation_document()
    document["matrix_digest"] = "0" * 64
    with pytest.raises(CaseDataError):
        GoldenExpectation.of(document)


def test_an_expectation_pinned_to_another_law_set_is_refused() -> None:
    document = _expectation_document()
    document["law_set_digest"] = "0" * 64
    with pytest.raises(CaseDataError):
        GoldenExpectation.of(document)


def test_a_satisfied_row_does_not_carry_the_case_to_pass_by_itself() -> None:
    document = _expectation_document()
    document["expected_trace"].append(
        {
            "law": "role_license_is_operative",
            "subject_id": "anchor.second",
            "standing": "violated",
            "blocked_by": None,
        }
    )
    with pytest.raises(CaseDataError):
        GoldenExpectation.of(document)


def test_a_violation_forces_block_even_beside_every_other_standing() -> None:
    document = _expectation_document()
    document["expected_trace"].append(
        {
            "law": "role_license_is_operative",
            "subject_id": "anchor.second",
            "standing": "violated",
            "blocked_by": None,
        }
    )
    document["expected_trace"].append(
        {
            "law": "condition_sites_are_licensed_for_use",
            "subject_id": "anchor.second",
            "standing": "unresolved",
            "blocked_by": None,
        }
    )
    document["expected_disposition"] = "defer"
    with pytest.raises(CaseDataError):
        GoldenExpectation.of(document)


def test_a_verdict_that_disagrees_with_its_own_trace_is_refused() -> None:
    document = _expectation_document()
    document["expected_disposition"] = "block"
    with pytest.raises(CaseDataError):
        GoldenExpectation.of(document)


def test_a_violation_that_has_no_row_in_the_trace_is_refused() -> None:
    document = _expectation_document()
    document["expected_violations"] = [
        {"law": "role_license_is_operative", "subject_id": "predicate.A"}
    ]
    with pytest.raises(CaseDataError):
        GoldenExpectation.of(document)


def test_two_contradicting_standings_for_one_law_on_one_subject_are_refused() -> None:
    document = _expectation_document()
    document["expected_trace"].append(
        {
            "law": "role_license_is_operative",
            "subject_id": "predicate.A",
            "standing": "unresolved",
            "blocked_by": None,
        }
    )
    document["expected_disposition"] = "defer"
    with pytest.raises(CaseDataError):
        GoldenExpectation.of(document)


def test_one_law_may_stand_on_one_subject_and_be_violated_on_another() -> None:
    document = _expectation_document()
    document["expected_trace"].append(
        {
            "law": "role_license_is_operative",
            "subject_id": "anchor.second",
            "standing": "violated",
            "blocked_by": None,
        }
    )
    document["expected_violations"] = [
        {"law": "role_license_is_operative", "subject_id": "anchor.second"}
    ]
    document["expected_disposition"] = "block"
    document["expected_materialized_identity_id"] = None
    document["citations"] = [
        {
            "requirement_id": "LS.role_license_is_operative.satisfied",
            "law": "role_license_is_operative",
            "witness_subject_id": "predicate.A",
            "standing": "satisfied",
        },
        {
            "requirement_id": "LS.role_license_is_operative.violated",
            "law": "role_license_is_operative",
            "witness_subject_id": "anchor.second",
            "standing": "violated",
        },
    ]
    expectation = GoldenExpectation.of(document)
    assert expectation.expected_disposition.value == "block"


def test_a_passing_case_that_reaches_no_materialized_identity_is_refused() -> None:
    document = _expectation_document()
    document["expected_materialized_identity_id"] = None
    with pytest.raises(CaseDataError):
        GoldenExpectation.of(document)


def test_a_subject_scoped_citation_that_names_no_subject_is_refused() -> None:
    document = _expectation_document()
    document["citations"][0]["witness_subject_id"] = None
    with pytest.raises(CaseDataError):
        GoldenExpectation.of(document)


def test_a_case_scoped_citation_that_names_a_subject_is_refused() -> None:
    document = _expectation_document()
    for citation in document["citations"]:
        if citation["requirement_id"] == "LS.anchors_do_not_exceed_arity.satisfied":
            citation["witness_subject_id"] = "nisbah.A"
    with pytest.raises(CaseDataError):
        GoldenExpectation.of(document)


def test_a_citation_that_names_a_standing_other_than_its_cell_is_refused() -> None:
    document = _expectation_document()
    document["citations"][0]["standing"] = "violated"
    with pytest.raises(CaseDataError):
        GoldenExpectation.of(document)


def test_a_citation_with_no_matching_row_in_the_frozen_trace_is_refused() -> None:
    document = _expectation_document()
    document["citations"][0]["witness_subject_id"] = "license.that.is.not.here"
    with pytest.raises(CaseDataError):
        GoldenExpectation.of(document)


def test_a_citation_of_a_requirement_outside_the_matrix_is_refused() -> None:
    document = _expectation_document()
    document["citations"][0]["requirement_id"] = "LS.a_law_that_is_not_frozen.satisfied"
    with pytest.raises(CaseDataError):
        GoldenExpectation.of(document)


def test_a_whole_case_citation_that_names_a_law_is_refused() -> None:
    document = _expectation_document()
    for citation in document["citations"]:
        if citation["requirement_id"] == "OR.pass":
            citation["law"] = "existence_lineage_rederives"
    with pytest.raises(CaseDataError):
        GoldenExpectation.of(document)


def test_a_whole_case_citation_that_constrains_another_verdict_is_refused() -> None:
    document = _expectation_document()
    for citation in document["citations"]:
        if citation["requirement_id"] == "OR.pass":
            citation["requirement_id"] = "OR.block"
    with pytest.raises(CaseDataError):
        GoldenExpectation.of(document)


def test_a_counter_case_with_no_declared_difference_is_refused() -> None:
    document = _case_document()
    document["case_id"] = "case0.counter.without_a_difference"
    document["baseline_case_id"] = "case0.baseline.pass"
    with pytest.raises(CaseDataError):
        GoldenExecutionCase.of(document)


def test_a_counter_case_with_two_undeclared_faults_is_refused() -> None:
    document = _case_document()
    document["case_id"] = "case0.counter.two_faults"
    document["baseline_case_id"] = "case0.baseline.pass"
    document["declared_differences"] = [
        _replace("nisbah.predicate.arity", 2, 3, "الرتبةُ صارت ثلاثًا"),
        _add("nisbah.anchors[1]", _second_anchor(), "زِيد مرتكزٌ ثانٍ"),
    ]
    with pytest.raises(CaseDataError):
        GoldenExecutionCase.of(document)


def test_two_faults_are_admitted_when_multiplicity_is_itself_the_proof() -> None:
    document = _case_document()
    document["case_id"] = "case0.counter.two_subjects"
    document["baseline_case_id"] = "case0.baseline.pass"
    document["declared_differences"] = [
        _replace(
            "nisbah.anchors[0].role_site.license_id",
            "license.term",
            "license.other",
            "رخصةُ المرتكز الأوّل تبدَّلت",
        ),
        _add("nisbah.anchors[1]", _second_anchor(), "مرتكزٌ ثانٍ رخصتُه معطَّلة"),
    ]
    document["multiplicity_is_the_proof"] = (
        "المطلوبُ إثباتُ أنّ قانونًا واحدًا يثبت على موضوعٍ ويُخالَف على آخر في "
        "القراءة نفسِها؛ فالتعدُّدُ هو محلُّ البرهان لا اختصارُ ملفّات"
    )
    case = GoldenExecutionCase.of(document)
    assert len(case.declared_differences) == 2


def test_a_baseline_that_declares_a_difference_from_nothing_is_refused() -> None:
    document = _case_document()
    document["declared_differences"] = [
        _replace("nisbah.predicate.arity", 2, 3, "فرقٌ بلا أصلٍ يُقاس إليه")
    ]
    with pytest.raises(CaseDataError):
        GoldenExecutionCase.of(document)


def test_a_case_document_that_is_not_shaped_as_a_declaration_is_refused() -> None:
    document = _case_document()
    document["document"]["a_key_outside_the_contract"] = True
    with pytest.raises(CaseDataError):
        GoldenExecutionCase.of(document)


def test_a_case_measured_against_an_absent_baseline_is_refused() -> None:
    case = _case_document()
    case["case_id"] = "case0.counter.orphan"
    case["baseline_case_id"] = "case0.a_baseline_that_is_not_written"
    case["declared_differences"] = [
        _replace("nisbah.predicate.arity", 2, 3, "الرتبةُ صارت ثلاثًا")
    ]
    expectation = _expectation_document()
    expectation["case_id"] = "case0.counter.orphan"
    with pytest.raises(CaseDataError):
        GoldenCaseCorpus.of(
            manifest=_read(_CORPUS_ROOT / "MANIFEST.json"),
            cases=tuple(item for _, item in _folder("cases")) + (case,),
            expectations=tuple(item for _, item in _folder("expectations"))
            + (expectation,),
            invalid_input_witnesses=tuple(item for _, item in _folder("invalid")),
            engine_seam_witnesses=tuple(item for _, item in _folder("seam")),
        )


def test_a_case_without_a_frozen_expectation_is_refused() -> None:
    case = _case_document()
    case["case_id"] = "case0.without_an_expectation"
    case["baseline_case_id"] = "case0.baseline.pass"
    case["declared_differences"] = [
        _replace("nisbah.predicate.arity", 2, 3, "الرتبةُ صارت ثلاثًا")
    ]
    with pytest.raises(CaseDataError):
        GoldenCaseCorpus.of(
            manifest=_read(_CORPUS_ROOT / "MANIFEST.json"),
            cases=tuple(item for _, item in _folder("cases")) + (case,),
            expectations=tuple(item for _, item in _folder("expectations")),
            invalid_input_witnesses=tuple(item for _, item in _folder("invalid")),
            engine_seam_witnesses=tuple(item for _, item in _folder("seam")),
        )


def test_an_invalid_input_witness_names_its_faults_and_claims_no_verdict() -> None:
    corpus = _corpus()
    witness = corpus.invalid_input_witnesses[0]
    assert witness.expected_fault_kinds
    cited = {citation.requirement_id for citation in witness.citations}
    assert "OR.invalid_input" in cited
    assert "OR.pass" not in cited


def test_an_invalid_input_witness_that_claims_a_law_cell_is_refused() -> None:
    document = deepcopy(
        _read(_CORPUS_ROOT / "invalid" / "case0.invalid.unknown_key.json")
    )
    document["citations"].append(
        {
            "requirement_id": "LS.existence_lineage_rederives.satisfied",
            "law": "existence_lineage_rederives",
            "witness_subject_id": "linguistic.A",
            "standing": "satisfied",
        }
    )
    with pytest.raises(CaseDataError):
        InvalidInputWitness.of(document)


def test_an_engine_seam_witness_is_given_no_document_of_its_own() -> None:
    corpus = _corpus()
    witness = corpus.engine_seam_witnesses[0]
    assert witness.seam
    assert witness.refused_document_reason
    cited = {citation.requirement_id for citation in witness.citations}
    assert cited == {
        "OR.invariant_error",
        "XS.invariant_error_has_no_verdict_and_no_envelope",
    }


def test_an_engine_seam_witness_that_is_given_a_document_is_refused() -> None:
    document = deepcopy(
        _read(
            _CORPUS_ROOT
            / "seam"
            / "case0.seam.materialized_identity_is_incomplete.json"
        )
    )
    document["document"] = {}
    with pytest.raises(CaseDataError):
        EngineSeamWitness.of(document)


def test_a_witness_that_takes_the_name_of_a_case_is_refused() -> None:
    document = deepcopy(
        _read(_CORPUS_ROOT / "invalid" / "case0.invalid.unknown_key.json")
    )
    document["witness_id"] = "case0.baseline.pass"
    with pytest.raises(CaseDataError):
        GoldenCaseCorpus.of(
            manifest=_read(_CORPUS_ROOT / "MANIFEST.json"),
            cases=tuple(item for _, item in _folder("cases")),
            expectations=tuple(item for _, item in _folder("expectations")),
            invalid_input_witnesses=(document,),
            engine_seam_witnesses=tuple(item for _, item in _folder("seam")),
        )


def test_a_frozen_case_document_is_not_altered_through_the_copy_it_hands_out() -> None:
    case = GoldenExecutionCase.of(_case_document())
    read = case.document
    read["nisbah"]["predicate"]["arity"] = 99
    read["nisbah"]["anchors"].append({"anchor_id": "anchor.smuggled"})
    assert case.document["nisbah"]["predicate"]["arity"] == 2
    assert len(case.document["nisbah"]["anchors"]) == 1
    assert case.document is not read


def test_a_frozen_witness_document_is_not_altered_after_it_is_read() -> None:
    corpus = _corpus()
    witness = corpus.invalid_input_witnesses[0]
    read = witness.document
    read["an_unknown_key"] = "أيًّا كانت"
    assert witness.document["an_unknown_key"] != "أيًّا كانت"


def test_a_document_that_carries_a_value_outside_the_json_contract_is_refused() -> None:
    document = _case_document()
    document["document"]["nisbah"]["predicate"]["arity"] = {1, 2}
    with pytest.raises(CaseDataError):
        GoldenExecutionCase.of(document)


def test_a_counter_case_whose_declared_difference_is_the_actual_one_is_read() -> None:
    case = _counter_case(
        "case0.counter.arity",
        [_replace("nisbah.predicate.arity", 2, 3, "الرتبةُ صارت ثلاثًا")],
    )
    case["document"]["nisbah"]["predicate"]["arity"] = 3
    corpus = _corpus_with(case)
    read = {item.case_id for item in corpus.cases}
    assert "case0.counter.arity" in read


def test_a_counter_case_that_does_not_differ_from_its_baseline_is_refused() -> None:
    case = _counter_case(
        "case0.counter.identical",
        [_replace("nisbah.predicate.arity", 2, 3, "فرقٌ مُدَّعًى لم يقع")],
    )
    with pytest.raises(CaseDataError):
        _corpus_with(case)


def test_a_second_undeclared_difference_is_refused_even_beside_a_true_one() -> None:
    case = _counter_case(
        "case0.counter.two_but_one_declared",
        [_replace("nisbah.predicate.arity", 2, 3, "الرتبةُ صارت ثلاثًا")],
    )
    case["document"]["nisbah"]["predicate"]["arity"] = 3
    case["document"]["nisbah"]["nisbah_id"] = "nisbah.B"
    with pytest.raises(CaseDataError):
        _corpus_with(case)


def test_a_declared_difference_at_a_place_that_did_not_change_is_refused() -> None:
    case = _counter_case(
        "case0.counter.phantom",
        [
            _replace("nisbah.predicate.arity", 2, 3, "الرتبةُ صارت ثلاثًا"),
            _replace("nisbah.nisbah_id", "nisbah.A", "nisbah.B", "الاسمُ تبدَّل"),
        ],
        "تعليلٌ لا يشفع لفرقٍ مُعلَنٍ لم يقع في الوثيقة المكتوبة",
    )
    case["document"]["nisbah"]["predicate"]["arity"] = 3
    with pytest.raises(CaseDataError):
        _corpus_with(case)


def test_a_declared_difference_that_misstates_what_it_became_is_refused() -> None:
    case = _counter_case(
        "case0.counter.misstated_after",
        [_replace("nisbah.predicate.arity", 2, 4, "الرتبةُ صارت أربعًا")],
    )
    case["document"]["nisbah"]["predicate"]["arity"] = 3
    with pytest.raises(CaseDataError):
        _corpus_with(case)


def test_a_declared_difference_that_misstates_what_it_was_is_refused() -> None:
    case = _counter_case(
        "case0.counter.misstated_before",
        [_replace("nisbah.predicate.arity", 1, 3, "الرتبةُ كانت واحدة")],
    )
    case["document"]["nisbah"]["predicate"]["arity"] = 3
    with pytest.raises(CaseDataError):
        _corpus_with(case)


def test_an_added_list_element_is_an_addition_not_a_change_of_length() -> None:
    case = _counter_case(
        "case0.counter.added_anchor",
        [_add("nisbah.anchors[1]", _second_anchor(), "زِيد مرتكزٌ ثانٍ")],
    )
    case["document"]["nisbah"]["anchors"].append(_second_anchor())
    corpus = _corpus_with(case)
    assert "case0.counter.added_anchor" in {item.case_id for item in corpus.cases}


def test_an_added_list_element_declared_as_a_replacement_is_refused() -> None:
    case = _counter_case(
        "case0.counter.added_anchor_as_replacement",
        [_replace("nisbah.anchors[1]", None, _second_anchor(), "زِيد مرتكزٌ ثانٍ")],
    )
    case["document"]["nisbah"]["anchors"].append(_second_anchor())
    with pytest.raises(CaseDataError):
        _corpus_with(case)


def test_a_removed_list_element_is_a_removal_at_its_own_index() -> None:
    removed = _case_document()["document"]["nisbah"]["predicate"]["slots"][1]
    case = _counter_case(
        "case0.counter.removed_slot",
        [_remove("nisbah.predicate.slots[1]", removed, "حُذِف الموضعُ الثاني")],
    )
    case["document"]["nisbah"]["predicate"]["slots"].pop()
    corpus = _corpus_with(case)
    assert "case0.counter.removed_slot" in {item.case_id for item in corpus.cases}


def test_two_changed_places_beside_each_other_are_two_differences() -> None:
    statement = (
        "المطلوبُ إثباتُ أنّ قانونًا واحدًا يثبت على موضوعٍ ويُخالَف على آخر في "
        "القراءة نفسِها؛ فالتعدُّدُ هو محلُّ البرهان لا اختصارُ ملفّات"
    )
    differences = [
        _replace(
            "nisbah.anchors[0].role_site.license_id",
            "license.term",
            "license.other",
            "رخصةُ المرتكز الأوّل تبدَّلت",
        ),
        _replace("nisbah.predicate.arity", 2, 3, "رتبةُ المحمول تبدَّلت"),
    ]
    case = _counter_case("case0.counter.two_subjects", differences, statement)
    case["document"]["nisbah"]["anchors"][0]["role_site"]["license_id"] = (
        "license.other"
    )
    case["document"]["nisbah"]["predicate"]["arity"] = 3
    corpus = _corpus_with(case)
    assert "case0.counter.two_subjects" in {item.case_id for item in corpus.cases}
    case["declared_differences"] = differences[:1]
    with pytest.raises(CaseDataError):
        _corpus_with(case)


def test_a_list_edit_that_hides_its_identity_is_refused() -> None:
    statement = (
        "المطلوبُ إثباتُ أنّ قانونًا واحدًا يثبت على موضوعٍ ويُخالَف على آخر في "
        "القراءة نفسِها؛ فالتعدُّدُ هو محلُّ البرهان لا اختصارُ ملفّات"
    )
    differences = [
        _replace(
            "nisbah.anchors[0].role_site.license_id",
            "license.term",
            "license.other",
            "رخصةُ المرتكز الأوّل تبدَّلت",
        ),
        _add("nisbah.anchors[1]", _second_anchor(), "زِيد مرتكزٌ ثانٍ"),
    ]
    case = _counter_case("case0.counter.list_edit", differences, statement)
    case["document"]["nisbah"]["anchors"][0]["role_site"]["license_id"] = (
        "license.other"
    )
    case["document"]["nisbah"]["anchors"].append(_second_anchor())
    with pytest.raises(CaseDataError):
        _corpus_with(case)


def test_a_baseline_chain_that_turns_back_on_itself_is_refused() -> None:
    first = _counter_case(
        "case0.counter.first",
        [_replace("nisbah.predicate.arity", 2, 3, "الرتبةُ صارت ثلاثًا")],
    )
    first["document"]["nisbah"]["predicate"]["arity"] = 3
    second = _counter_case(
        "case0.counter.second",
        [_replace("nisbah.nisbah_id", "nisbah.A", "nisbah.B", "الاسمُ تبدَّل")],
    )
    second["document"]["nisbah"]["nisbah_id"] = "nisbah.B"
    first["baseline_case_id"] = "case0.counter.second"
    second["baseline_case_id"] = "case0.counter.first"
    with pytest.raises(CaseDataError):
        _corpus_with(first, second)


def test_an_expected_fault_kind_outside_the_closed_vocabulary_is_refused() -> None:
    document = deepcopy(
        _read(_CORPUS_ROOT / "invalid" / "case0.invalid.unknown_key.json")
    )
    document["expected_fault_kinds"] = ["unknown_keey"]
    with pytest.raises(CaseDataError):
        InvalidInputWitness.of(document)


def test_an_expected_fault_kind_is_read_as_a_member_of_its_vocabulary() -> None:
    corpus = _corpus()
    witness = corpus.invalid_input_witnesses[0]
    assert witness.expected_fault_kinds == (InputFaultKind.UNKNOWN_KEY,)


def _baseline_document() -> dict[str, Any]:
    return deepcopy(_read(_CORPUS_ROOT / "cases" / "case0.baseline.pass.json"))


def test_a_direct_constructor_does_not_share_the_document_it_was_given() -> None:
    raw = _baseline_document()["document"]
    case = GoldenExecutionCase(
        case_id="case0.direct",
        document_content=raw,
        baseline_case_id=None,
        declared_differences=(),
        multiplicity_is_the_proof=None,
    )
    raw["nisbah"]["predicate"]["arity"] = 99
    assert case.document["nisbah"]["predicate"]["arity"] != 99


def test_a_direct_witness_does_not_share_the_document_it_was_given() -> None:
    raw = _baseline_document()["document"]
    witness = InvalidInputWitness(
        witness_id="case0.direct.witness",
        document_content=raw,
        expected_fault_kinds=(InputFaultKind.UNKNOWN_KEY,),
        citations=(),
    )
    raw["nisbah"]["predicate"]["arity"] = 99
    assert witness.document["nisbah"]["predicate"]["arity"] != 99


def test_a_direct_difference_does_not_share_the_states_it_was_given() -> None:
    before: dict[str, Any] = {"slots": [1, 2]}
    difference = DeclaredDifference(
        operation=DiffOperation.REPLACE,
        path="nisbah.predicate",
        before=before,
        after={"slots": [1, 2, 3]},
        statement="المحمولُ تبدَّل",
    )
    before["slots"].append(9)
    assert difference.before == {"slots": (1, 2)}


def test_a_document_that_carries_a_non_finite_number_is_refused() -> None:
    raw = _baseline_document()["document"]
    raw["nisbah"]["predicate"]["arity"] = float("inf")
    with pytest.raises(CaseDataError):
        GoldenExecutionCase(
            case_id="case0.direct.infinite",
            document_content=raw,
            baseline_case_id=None,
            declared_differences=(),
            multiplicity_is_the_proof=None,
        )
