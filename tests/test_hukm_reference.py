"""عيّنةُ الأحكام المحجوبة (ADR ٩، 2026-10-10): إطارٌ من المصحف ببذرةٍ معلَنة يملؤه المالكُ بيده (الجذر،
الجنس، القابليّة) فيصير مرجعَ الأحكام الذي تُقاس عليه المعلوماتُ السابقة في SLGE (المادّة ١٢). الإطارُ
عمياءُ (لا حكمَ للسُّلَّم فيه) ويُعاد سحبُه ببذرته فلا تتحرّك مواقعُه؛ ولا رقمَ عليه قبل ملئه."""

from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRAME = ROOT / "corpora" / "hukm-sample-frame.tsv"


def _tool():
    spec = importlib.util.spec_from_file_location("gen_hukm_sample",
                                                  ROOT / "tools" / "gen_hukm_sample.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen_hukm_sample"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_hukm_frame_is_blind_seeded_and_reproducible() -> None:
    m = _tool()
    rows = m.draw()
    assert len(rows) == m.SIZE == 300 and len({(r["line"], r["pos"]) for r in rows}) == 300
    assert all(1 <= int(r["line"]) <= 6236 for r in rows)
    with FRAME.open(encoding="utf-8", newline="") as f:
        frame = list(csv.DictReader(f, delimiter="\t"))
    assert [{k: r[k] for k in m.FIXED} for r in frame] == [{k: r[k] for k in m.FIXED} for r in rows]
    assert list(frame[0]) == [*m.FIXED, *m.OWNER] == [
        "id", "line", "pos", "left", "word", "right", "root", "jins", "qabiliyya", "note"]
    assert not any(c in frame[0] for c in ("status", "atoms", "reading", "hukm"))  # عمياء
    # الكلمةُ بعينها من سطرها في المدوّنة المختومة
    corpus = ROOT / "corpora" / "quran-simple-enhanced.txt"
    lines = corpus.read_text(encoding="utf-8").splitlines()
    for r in frame[:20]:
        assert lines[int(r["line"]) - 1].split(" ")[int(r["pos"]) - 1] == r["word"]
    # الطفرة: بذرةٌ أخرى تسحب مواقعَ أخرى — الإطارُ دالّةٌ في بذرته المعلَنة لا في اختيار أحد
    m.SEED = 1
    assert [(r["line"], r["pos"]) for r in m.draw()] != [(r["line"], r["pos"]) for r in rows]
