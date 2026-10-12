"""سجلُّ التراخيص محسوبًا (`A116.Sijill`، ADR ٢٩): شاهدٌ لا مرآة.

١. السجلُّ المودَع: أعدادٌ كُتبت باليد من قراءته قبل الأداة —
الدرجات، والجذرُ الواحد، وسلسلةُ البوّابات حوافَّ
   الدرجات الوحيدة، والبصماتُ المتمايزة (المدوَّراتُ أسماءٌ أخرى للمدخلات نفسِها).
٢. الدليلُ: وحداتُ Lean المدقَّقة سبعٌ بأعدادٍ من مخرج `Audit.lean` الخاصّ بها في الجلسة (38 مجموعًا)،
   كلُّها في الزوائد؛ ولا دليلَ قائمًا في غيرها.
٣. مرآةٌ مستقلّةٌ للبوّابة: أعلى درجةٍ مرخَّصة تُحسب هنا من `evidence.tsv` بشيفرةٍ لا تستورد الأداة — 0،
   كما في `sijill_stops_at_zero`؛ والحمامُ على الدرجة 4 كما في `mana_never_mustawfa`.
٤. صفوفُ `SijillData.lean` تُقرأ نصًّا وتُطابَق بالسجلّ والدليل.
٥. صنفُ المحتوى على بايتاتٍ مكتوبةٍ باليد.
٦. الطفرات: `MUTANT_DECLARED_STATUS` (القانونُ على الحالة المكتوبة يرخّص الدرجات كلَّها)،
   `MUTANT_RECYCLED_COUNTED` (عدُّ المدوَّرات ملفّاتٍ: 1457)، `MUTANT_NAME_CLASSIFIER` (الصنفُ بالاسم).
"""

from __future__ import annotations

import csv
import importlib.util
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "sijill" / "ledger.json"
EVIDENCE = ROOT / "docs" / "sijill" / "evidence.tsv"
LEAN = ROOT / "formal" / "a116" / "A116" / "SijillData.lean"
SPEC = importlib.util.spec_from_file_location("gen_sijill", ROOT / "tools" / "gen_sijill.py")
assert SPEC and SPEC.loader
TOOL: Any = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TOOL)

WAZAIF = 7


def _ledger() -> dict[str, Any]:
    with LEDGER.open(encoding="utf-8") as f:
        return json.load(f)


def _evidence() -> list[dict[str, str]]:
    with EVIDENCE.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def test_ledger_by_hand() -> None:
    led = _ledger()
    ents = led["entries"]
    num = {g["key"]: g["num"] for g in led["degrees"]}
    counts = [sum(1 for e in ents if num[e["degree"]] == d) for d in range(7)]
    assert counts == [29, 383, 88, 36, 4, 404, 150]
    assert [e["id"] for e in ents if e["licensed_by"] is None] == ["f0001"]
    ids = {e["id"]: e for e in ents}
    cross = sorted(e["id"] for e in ents
                   if e["licensed_by"] and num[e["degree"]] != num[ids[e["licensed_by"]]["degree"]])
    assert cross == sorted(g["gate"] for g in led["degrees"] if g["num"] > 0)
    shas = {e["sha256"] for e in ents}
    assert len(shas) == 1094 and {r["sha256"] for r in led["recycled"]} <= shas
    assert led["counts"]["total_in_ledger"] == 1457  # المعلن


def test_mutant_recycled_counted() -> None:
    led = _ledger()
    mutant = len(led["entries"]) + len(led["recycled"])  # MUTANT_RECYCLED_COUNTED
    distinct = len({e["sha256"] for e in led["entries"]} | {r["sha256"] for r in led["recycled"]})
    assert mutant == 1457 != distinct == 1094


def test_evidence_by_hand() -> None:
    rows = _evidence()
    burhan = {r["id"]: int(r["daleel"].split(":")[1])
              for r in rows if r["daleel"].startswith("burhan:")}
    assert burhan == {"f1021": 8, "f1022": 3, "f1023": 3, "f1024": 4, "f1025": 11, "f1026": 3,
                      "f1027": 6}
    assert sum(burhan.values()) == 38
    assert {r["degree"] for r in rows if r["id"] in burhan} == {"zur"}
    assert all(r["kind"] == "LEAN" for r in rows if r["id"] in burhan)
    by_id = {r["id"]: r for r in rows}
    assert by_id["f0051"]["daleel"] == "muallaq:LEAN_BUILD_FAILED"
    assert by_id["f0001"]["kind"] == "UNREAD" and by_id["f0030"]["kind"] == "UNREAD"
    assert all(r["daleel"] == "muallaq:NOT_FOUND_BY_HASH" for r in rows if r["kind"] == "UNREAD")


def _highest_licensed(rows: list[dict[str, str]], qaim: Any) -> int:
    """أعلى درجة سجلٍّ مرخَّصة: الدرجةُ k مرخَّصةٌ إن استُوفيت الوظائفُ السبع في كلّ درجةٍ دونها."""

    k = 0
    while k < 6:
        cells = {r["wazifa"] for r in rows if int(_num(r)) == k and qaim(r) and r["wazifa"] != "-"}
        if len(cells) < WAZAIF:
            return k
        k += 1
    return k


NUM = {"daraja-0-usul": 0, "daraja-1-daal": 1, "daraja-2-madlul": 2, "daraja-3-tarkib": 3,
       "daraja-4-mana": 4, "daraja-5-mukhtabar": 5, "zur": 6}


def _num(r: dict[str, str]) -> int:
    return NUM[r["degree"]]


def test_gate_mirror_stops_at_zero() -> None:
    rows = _evidence()
    assert _highest_licensed(rows, lambda r: r["daleel"].startswith("burhan:")) == 0


def test_mutant_declared_status() -> None:
    led = _ledger()
    status = {e["id"]: e["status"] for e in led["entries"]}
    rows = _evidence()
    # MUTANT_DECLARED_STATUS: الدرجةُ تامّةٌ إن كُتب «مرخَّص» لكلّ ملفّاتها — فالدرجاتُ 0..5 تامّة
    declared = [all(status[r["id"]] == "مرخَّص" for r in rows if _num(r) == d) for d in range(6)]
    assert all(declared)
    assert _highest_licensed(rows, lambda r: r["daleel"].startswith("burhan:")) != 6


def test_pigeonhole_on_mana() -> None:
    rows = _evidence()
    mana = [r for r in rows if _num(r) == 4]
    assert len(mana) == 4 < WAZAIF
    # ولو قام دليلُ كلّ ملفٍّ وأُسند كلٌّ إلى وظيفةٍ مختلفة: أربعُ خاناتٍ من سبع
    spread = [{**r, "wazifa": str(i)} for i, r in enumerate(rows)]
    assert _highest_licensed(spread, lambda r: True) == 4


def test_lean_rows_match_ledger_and_evidence() -> None:
    text = LEAN.read_text(encoding="utf-8")
    lean = re.findall(r"⟨(\d+), (\d+), (none|some \.\w+), (none|some \d+)⟩", text)
    rows = _evidence()
    assert len(lean) == len(rows) == 1094
    pos = {r["id"]: i for i, r in enumerate(rows)}
    for (d, a, w, p), r in zip(lean, rows, strict=True):
        assert int(d) == _num(r)
        audited = int(r["daleel"].split(":")[1]) if r["daleel"].startswith("burhan:") else 0
        assert int(a) == audited
        assert w == ("none" if r["wazifa"] == "-" else f"some .{r['wazifa']}")
        assert p == ("none" if r["licensed_by"] == "-" else f"some {pos[r['licensed_by']]}")


def test_content_kind_by_hand() -> None:
    k = TOOL.content_kind
    assert k(b"import Slge.Bridge\nimport Slge.Rank\n") == "IMPORTS_ONLY"
    assert k(b"import A116\nnamespace X\ntheorem t : 1 = 1 := rfl\n") == "LEAN"
    assert k(b"import pytest\n\ndef test_x():\n    assert 1\n") == "PY_TEST"
    assert k(b"def f(x):\n    return x\n") == "PY"
    assert k(b"PK\x03\x04rest") == "ZIP"
    assert k("# عنوان\n\nنصٌّ.\n".encode()) == "TEXT"
    assert k(b'{"a": 1}') == "JSON"
    assert k(b"a,b\n1,2\n3,4\n") == "TABLE"


def test_mutant_name_classifier() -> None:
    def by_name(path: str) -> str:  # MUTANT_NAME_CLASSIFIER: الصنفُ من الاسم والامتداد
        base = path.rsplit("/", 1)[-1]
        if base.startswith("test_") or "/tests/" in path:
            return "PY_TEST"
        return "PY" if path.endswith(".py") else "TEXT"

    content = b"import pytest\n\ndef test_bridge():\n    assert True\n"
    path = "alghanem-constitution/suspended/tests__test_bridge.py"
    assert by_name(path) != TOOL.content_kind(content) == "PY_TEST"


def test_tool_check_passes() -> None:
    assert TOOL.check() == []
