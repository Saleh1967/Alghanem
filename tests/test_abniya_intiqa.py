"""انتقاءُ الأبنية الموقَّع (ADR ١٣): المجالُ المعلَنُ الثالث يمرّ على البوّابة نفسها.

التوقّعاتُ مكتوبةٌ باليد: حالاتُ فَعْلَلَ وٱسْتَفْعَلَ وفَاعِلٌ وفَعْلَةٌ على حروف هياكلها، والأولويّةُ (46 غيرُ
ثلاثيّ أوّلًا)، والهيكلان بلا سطرٍ مختوم. والطفراتُ تُلتقط بأسمائها على نسخةٍ مؤقّتة: صفٌّ بلا طبعة،
وهيكلٌ مخالف، وسطورٌ معدَّلة، وبصمةٌ غيرُ مختومة، وتوقيعٌ على بصمةٍ أخرى؛ ورفضُ البوّابة بيانٌ لا خطأ.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import pytest
from conftest import ROOT

from gate.api import ABNIYA_INTIQA_CORPUS, ABNIYA_INTIQA_SHA256, SEALED_CORPORA

SPEC = importlib.util.spec_from_file_location("gen_abniya_intiqa",
                                              ROOT / "tools" / "gen_abniya_intiqa.py")
assert SPEC and SPEC.loader
MOD: Any = importlib.util.module_from_spec(SPEC)
sys.modules["gen_abniya_intiqa"] = MOD
SPEC.loader.exec_module(MOD)
A, KS, U, S = "فتح", "كسر", "ضم", "سكون"


def test_frame_is_sealed_empty_and_ordered_by_priority() -> None:
    rows = MOD.read_frame()
    assert len(rows) == 158 and len({r["id"] for r in rows}) == 158
    prio = [r["priority"] for r in rows]
    assert prio == ["1"] * 46 + ["2"] * 112
    assert {r["skeleton"] for r in rows if r["kitab_lines"] == "—"} == {"فعاليلن", "فعلو"}
    assert all(not r[k] for r in rows for k in MOD.OWNER)
    assert ABNIYA_INTIQA_CORPUS.read_bytes() == b""
    assert ABNIYA_INTIQA_SHA256 == hashlib.sha256(b"").hexdigest()
    assert SEALED_CORPORA[ABNIYA_INTIQA_CORPUS.name] == ABNIYA_INTIQA_SHA256
    assert MOD.check(None, None) == []
    assert MOD.signature()["signed_by"] is None


@pytest.mark.skipif(not (ROOT.parent / "slge" / "tests" / "data").exists(), reason="SLGE غائب")
def test_machine_columns_are_what_the_sealed_slge_sources_give() -> None:
    assert MOD.check(ROOT.parent / "slge", None) == []


def _fill(tmp: Path, fills: dict[str, str], monkeypatch: pytest.MonkeyPatch,
          signed: str | None = None) -> list[dict[str, str]]:
    rows = MOD.read_frame()
    for r in rows:
        if r["skeleton"] in fills:
            r.update(vocalized=fills[r["skeleton"]], edition="هارون، الخانجي", page="4/245")
    frame, lines, sig = tmp / "abniya-intiqa.tsv", tmp / "intiqa-test.txt", tmp / "sig.json"
    monkeypatch.setattr(MOD, "FRAME", frame)
    monkeypatch.setattr(MOD, "LINES", lines)
    monkeypatch.setattr(MOD, "SIGNATURE", sig)
    MOD.write_frame(rows)
    text = MOD.lines_text(rows)
    lines.write_text(text, encoding="utf-8")
    sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    monkeypatch.setitem(SEALED_CORPORA, lines.name, sha)
    monkeypatch.setattr(MOD, "ABNIYA_INTIQA_SHA256", sha)
    sig.write_text(json.dumps({"signed_by": signed, "signed_on": "2026-10-11" if signed else None,
                               "lines_sha256": sha if signed else None}), encoding="utf-8")
    return rows


def test_filled_rows_enter_through_the_gate(tmp_path: Path,
                                            monkeypatch: pytest.MonkeyPatch) -> None:
    fills = {"فعلل": "فَعْلَلَ", "استفعل": "ٱسْتَفْعَلَ", "فاعل": "فَاعِلٌ", "فعل": "فَعْلَةٌ",
             "فعيل": "فَعْلْلَ"}
    rows = _fill(tmp_path, fills, monkeypatch, signed="صالح الغانم")
    assert MOD.check(None, None) == []
    got = {r["skeleton"]: r for r in MOD.results(rows)}
    assert got["فعلل"]["states"] == [A, S, A, A]
    assert got["استفعل"]["states"] == [KS, S, A, S, A, A]  # همزةُ الوصل مكسورة
    assert got["فاعل"]["states"] == [A, S, KS, U]  # التنوينُ زيادةٌ معلَنة
    assert got["فعل"]["states"] == [A, S, A]  # التاءُ المربوطة زيادةٌ معلَنة
    # «فعيل» بغير حروفه وبساكنين متجاورين: رفضٌ مسمًّى من البوّابة بيانٌ لا خطأ
    assert got["فعيل"]["status"] == "REJECT" and got["فعيل"]["reasons"]
    dep = MOD.deposit(rows)
    assert dep["signed"] is True and len(dep["rows"]) == 5


def test_mutations_are_caught_by_name(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    rows = _fill(tmp_path, {"فعل": "فَعَّلَ"}, monkeypatch)  # حروفُه ف ع ع ل لا ف ع ل
    fal = next(r["id"] for r in rows if r["skeleton"] == "فعل")
    assert MOD.check(None, None) == [f"INTIQA_SKELETON_MISMATCH {fal}"]
    rows[0]["edition"] = ""
    rows[0]["vocalized"] = "فَعَاعِيلُ"
    MOD.write_frame(rows)
    bad = MOD.check(None, None)
    assert f"INTIQA_ROW_MALFORMED {rows[0]['id']}" in bad and "INTIQA_LINES_DRIFTED" in bad
    rows[0]["vocalized"] = ""
    MOD.write_frame(rows)
    MOD.LINES.write_text("فَعَّلَ\nزيادة\n", encoding="utf-8")
    assert MOD.check(None, None) == ["INTIQA_LINES_DRIFTED", "INTIQA_NOT_SEALED"]
    MOD.LINES.write_text(MOD.lines_text(rows), encoding="utf-8")
    MOD.SIGNATURE.write_text(json.dumps({"signed_by": "صالح الغانم", "lines_sha256": "0" * 64}),
                             encoding="utf-8")
    assert MOD.check(None, None)[:1] == ["INTIQA_SIGNATURE_STALE"]
    assert MOD.deposit(rows)["signed"] is False


def test_deposit_is_canonical_and_drift_is_named(tmp_path: Path,
                                                 monkeypatch: pytest.MonkeyPatch) -> None:
    rows = _fill(tmp_path, {"فعلل": "فَعْلَلَ"}, monkeypatch)
    out = tmp_path / "dep.json"
    out.write_text(json.dumps(MOD.deposit(rows), ensure_ascii=False), encoding="utf-8")
    assert MOD.check(None, out) == []
    d = json.loads(out.read_text(encoding="utf-8"))
    d["rows"][0]["states"][0] = KS
    out.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    assert MOD.check(None, out) == ["DEPOSIT_DRIFTED_FROM_GATE"]
    with (tmp_path / "abniya-intiqa.tsv").open(encoding="utf-8") as f:
        assert len(list(csv.DictReader(f, delimiter="\t"))) == 158
