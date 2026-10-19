"""مرجعُ الصحيحين بتوقيع المالك (2026-10-10): تشكيلُ الطبعة مرجعٌ محجوبٌ لقانون الترخيص وحدَه، وعيّنةٌ
محجوبةٌ ببذرةٍ يملؤها المالك بيده. التوقيعُ يربط بصمةَ المدوّنة المختومة؛ ونطاقُه مكتوبٌ فلا يُوسَم «مقيسًا»
خارجَه؛ والإطارُ عمياءُ (لا قراءةَ للبوّابة فيه) ويُعاد سحبُه ببذرته فلا تتحرّك مواقعُه."""

from __future__ import annotations

import csv
import importlib.util
import json
import sys
from pathlib import Path

from gate.api import HADITH_LINES_SHA256

ROOT = Path(__file__).resolve().parents[1]
HADITH = ROOT / "corpora" / "hadith"


def _tool():
    spec = importlib.util.spec_from_file_location("gen_hadith_sample",
                                                  ROOT / "tools" / "gen_hadith_sample.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen_hadith_sample"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_owner_signature_binds_the_sealed_lines_and_names_its_scope() -> None:
    d = json.loads((HADITH / "owner-reference.json").read_text(encoding="utf-8"))
    assert d["signed_by"] and d["signed_on"] == "2026-10-10"
    assert d["reference"]["sha256"] == HADITH_LINES_SHA256
    assert d["reference"]["licence"] == "ODbL 1.0"
    assert d["scope"] and "الترخيص" in d["scope"][0]
    assert {"الاشتقاق", "الاسترجاع"} <= set(d["excludes"])  # لا «مقيس» لهما حتى تُملأ العيّنة
    assert d["sample"] == {**d["sample"], "file": "sample-frame.tsv", "seed": 20261010, "size": 500}
    assert d["sample"]["filled_sha256"] is None  # الإطارُ لم يُملأ بعد: لا رقمَ عليه


def test_sample_frame_is_blind_seeded_and_reproducible() -> None:
    m = _tool()
    rows = m.draw()
    assert len(rows) == m.SIZE == 500 and len({(r["line"], r["pos"]) for r in rows}) == 500
    assert {r["book"] for r in rows} == {"bukhari", "muslim"}
    with (HADITH / "sample-frame.tsv").open(encoding="utf-8", newline="") as f:
        frame = list(csv.DictReader(f, delimiter="\t"))
    assert [{k: r[k] for k in m.FIXED} for r in frame] == [{k: r[k] for k in m.FIXED} for r in rows]
    assert list(frame[0]) == [*m.FIXED, *m.OWNER]
    assert all(not r["word"].startswith("<") for r in frame)  # رموزُ الطبعة ليست مواقع
    assert all(k in frame[0] for k in ("root", "segmentation", "wasl_vowel"))
    assert not any(c in frame[0] for c in ("status", "atoms", "reading"))  # عمياء
    # الطفرة: بذرةٌ أخرى تسحب مواقعَ أخرى — فالإطارُ دالّةٌ في بذرته المعلَنة لا في اختيار أحد
    m.SEED = 1
    assert [(r["line"], r["pos"]) for r in m.draw()] != [(r["line"], r["pos"]) for r in rows]
