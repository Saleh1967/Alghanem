"""عقدُ الشرح نصًّا: الكلمةُ تخرج بـ`gate.exit` لا من الملفّ، ورقمُ صورتها بترتيب `gen_certificates`.

التوقّعاتُ مكتوبةٌ باليد على مدوّنةٍ صغيرةٍ مؤقّتة: سطران، كلمتان مقبولتان (قَالَ، كَتَبَ) تخرجان بعينهما
برقمَي صورتين 0 و1، والمكرَّرةُ برقمها الأوّل، والمرفوضةُ (قَالْتُ) برفضها المسمّى. والطفراتُ تُلتقط بأسمائها:
بصمةُ مدوّنةٍ أخرى، وعددُ صورٍ مخالف، ومخرجٌ يغيّر الكلمة.
"""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest
from conftest import ROOT

SPEC = importlib.util.spec_from_file_location("gen_sharh_text",
                                              ROOT / "tools" / "gen_sharh_text.py")
assert SPEC and SPEC.loader
MOD: Any = importlib.util.module_from_spec(SPEC)
sys.modules["gen_sharh_text"] = MOD
SPEC.loader.exec_module(MOD)
TEXT = "قَالَ كَتَبَ\nكَتَبَ قَالْتُ\n"


def _corpus(tmp: Path, monkeypatch: pytest.MonkeyPatch) -> str:
    corpus = tmp / "corpus.txt"
    corpus.write_text(TEXT, encoding="utf-8")
    sha = hashlib.sha256(TEXT.encode("utf-8")).hexdigest()
    monkeypatch.setattr(MOD, "CORPUS", corpus)
    monkeypatch.setattr(MOD, "CORPUS_SHA256", sha)
    return sha


def test_words_exit_through_the_gate_with_their_form_numbers(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    sha = _corpus(tmp_path, monkeypatch)
    lines = [[["ENTRY", 3, "خانة"]], [["ENTRY", 3, "خانة"]]]
    ledger = {"ENTRY": ["مفحوص", "t"]}
    out, bad = MOD.build({"corpus_sha256": sha, "forms": lines, "ledger": ledger})
    assert bad == []
    assert out["verses"] == [
        {"line": 1, "words": [["قَالَ", 0, None], ["كَتَبَ", 1, None]]},
        {"line": 2, "words": [["كَتَبَ", 1, None], [None, -1, "OUTSIDE_DECLARED_DOMAIN:"]]},
    ]
    assert out["forms"] == lines and out["ledger"] == ledger


def test_mutations_are_caught_by_name(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    sha = _corpus(tmp_path, monkeypatch)
    two = [[], []]
    assert MOD.build({"corpus_sha256": "0" * 64, "forms": two})[1] == ["SHARH_CORPUS_MISMATCH"]
    assert MOD.build({"corpus_sha256": sha, "forms": [[]] * 3})[1] == ["SHARH_FORMS_MISMATCH"]
    real = MOD.exit
    monkeypatch.setattr(MOD, "exit", lambda c: real(c) + "ـ".encode())
    assert MOD.build({"corpus_sha256": sha, "forms": two})[1] == ["EXIT_IS_NOT_THE_WORD 1",
                                                                  "EXIT_IS_NOT_THE_WORD 1"]
