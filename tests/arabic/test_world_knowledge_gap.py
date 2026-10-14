"""الفجوة مقيسة: ما ينقص كل سؤال ذهبي، والمولد لا يحكم، والشواهد القرآنية في المودع."""

import re

import pytest

from alghanem.arabic.pipeline_stations import repository_root_path
from alghanem.arabic.world_knowledge_gap import (
    ADMITTED_RULES,
    GENERATED_LICENCES,
    GENERATED_RULES,
    GOLD_QUESTIONS,
    QURAN_WITNESSES,
    gap_reading,
)
from alghanem.ontology.epistemics import Evidence, EvidenceGenus, Scope
from alghanem.ontology.world_knowledge import (
    Admission,
    Literal,
    Outcome,
    WorldKnowledgeError,
    infer,
)

EXPECTED = {
    "موافقة": ["قاعدة:ضرب-أذى", "قاعدة:أذى-محرم"],
    "مخالفة-صفة": ["رافع:سائمة-زكاة"],
    "مخالفة-شرط": ["رافع:حمل-نفقة"],
    "قياس": ["قاعدة:إجارة-إلهاء", "قاعدة:إلهاء-محرم"],
    "ضابط-منطقي": [],
    "كناية": ["قاعدة:قرى-رماد", "رافع:قرى-رماد"],
}


def test_each_gold_question_names_exactly_what_it_lacks() -> None:
    reading = gap_reading()
    assert {q: row["missing"] for q, row in reading.items()} == EXPECTED
    assert all(row["would_agree_with_gold"] for row in reading.values())
    assert sum(len(m) for m in EXPECTED.values()) == 8


def test_no_gold_question_is_answered_from_proposals_alone() -> None:
    reading = gap_reading()
    assert {row["outcome"] for row in reading.values()} == {
        Outcome.ناقص.value,
        Outcome.غير_منتج.value,
    }
    assert all(rule.admission is Admission.مرشح for rule in GENERATED_RULES)
    assert all(lic.is_candidate for lic in GENERATED_LICENCES)


def test_a_proposal_cannot_be_admitted_on_its_own_hypothesis() -> None:
    hypothesis = Evidence(
        evidence_id="رأي",
        genus=EvidenceGenus.DECLARED_HYPOTHESIS,
        statement="رأي سابق",
        source_name="مولد",
        scope=Scope(domain_id="x"),
    )
    for rule in GENERATED_RULES:
        with pytest.raises(WorldKnowledgeError):
            rule.admit(hypothesis)


def test_a_candidate_licence_never_produces() -> None:
    question = next(q for q in GOLD_QUESTIONS if q.question_id == "مخالفة-صفة")
    verdict = infer(
        question.given, question.target, ADMITTED_RULES, GENERATED_LICENCES[:1]
    )
    assert verdict.outcome is Outcome.ناقص
    assert verdict.conclusion is None
    assert verdict.would_conclude == Literal("تجب الزكاة", False)


def test_the_quranic_witnesses_are_in_the_deposited_text() -> None:
    lines = (
        (repository_root_path() / "corpora" / "quran-simple-enhanced.txt")
        .read_text(encoding="utf-8")
        .split("\n")
    )
    for line, text in QURAN_WITNESSES.values():
        bare = re.sub("[ً-ْٰـ]", "", lines[line - 1])
        assert text in bare, line
