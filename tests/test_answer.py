"""الجواب: الجملُ موسومة، والمُعيدُ لا يُسقط الوسوم."""

from __future__ import annotations

import pytest

from slge.answer import Answer, Sentence, compose, render, verbalize
from slge.knowledge import Genus, Licence, LicenceGround, Literal, infer
from slge.status import Status
from world_fixture import ADMITTED, PROPOSED_RULES, ev

RULES = {r.rule_id: r for r in ADMITTED + PROPOSED_RULES}


def _answers() -> list[tuple[str, Answer]]:
    zakat = Licence("سائمة-زكاة", LicenceGround.وصف_مفهم, ev("ن", Genus.خبر_مقبول, "نص"))
    cases = [
        ("أيحرم قول أف؟", infer(Literal("أف", True), "محرم", ADMITTED), {}),
        ("أيحرم الضرب؟", infer(Literal("ضرب", True), "محرم", ADMITTED + PROPOSED_RULES), {}),
        ("ليس إنسانًا: أليس حيوانًا؟", infer(Literal("إنسان", False), "حيوان", ADMITTED), {}),
        ("المعلوفة؟", infer(Literal("سائمة", False), "زكاة", ADMITTED, (zakat,)),
         {"سائمة-زكاة": zakat}),
        ("مجهول؟", infer(Literal("قمر", True), "محرم", ADMITTED), {}),
    ]
    return [(q, compose(q, v, RULES, lic)) for q, v, lic in cases]


def test_every_sentence_is_tagged() -> None:
    seen = set()
    for _, a in _answers():
        assert a.sentences
        for s in a.sentences:
            assert s.support.strip() and isinstance(s.status, Status)
            seen.add(s.status)
    assert {Status.مبرهن, Status.دليل, Status.رأي, Status.معلن} <= seen


def test_produced_answer_cites_rule_and_theorem() -> None:
    _, a = _answers()[0]
    text = render(a)
    assert "نعم: محرم" in text and "lean:Slge.Ghazali.ghazali_table" in text
    assert "corpora/quran-simple-enhanced.txt" in text


class _Echo:
    def rephrase(self, sentence: Sentence) -> str:
        return "بعبارةٍ أخرى: " + sentence.text


class _Eraser:
    def rephrase(self, sentence: Sentence) -> str:
        return ""


def test_verbalizer_cannot_drop_tags() -> None:
    for _, a in _answers():
        v = verbalize(a, _Echo())
        assert [(s.status, s.support) for s in v.sentences] == \
            [(s.status, s.support) for s in a.sentences]
        with pytest.raises(ValueError):
            verbalize(a, _Eraser())
