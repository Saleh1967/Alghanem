"""وسمُ الأجناس بقسمة ج3 409 (ADR ٣٥): توقّعاتٌ مستقلّةٌ عن الشيفرة — القيمُ هي أقسامُ النبهانيّ
الخمسة بلفظها في المختوم و«ليس جنسًا» لا غير؛ صفٌّ لكلّ جنسٍ بترتيب الأجناس؛ الاقتراحُ رأيٌ لا
يستهلكه الحكم؛ ولا وسمَ قبل التوقيع، والموقَّعُ لا فراغَ فيه؛ ومطابقةُ تصدير Lean؛ وطفراتٌ مرفوضة
باسمها."""

from __future__ import annotations

import copy
import gzip
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import pytest

from slge.ajnas_table import GENERA
from slge.madlul_table import PROPOSALS, SIGNED, TAGS

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "tests" / "data"
FRAME = DATA / "owner-ajnas-madlul.json"


def _tool() -> Any:
    spec = importlib.util.spec_from_file_location("deposit_madlul",
                                                  ROOT / "tools" / "deposit_madlul.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["deposit_madlul"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_values_are_nabhani_409_verbatim() -> None:
    """القيمُ مأخوذةٌ من سطر ج3 409 بعينه في المودَع المختوم، لا من الذاكرة."""

    raw = gzip.decompress((DATA / "nabhani-shakhsiyya-3.txt.gz").read_bytes()).decode("utf-8")
    line = raw.split("\n")[408]
    assert line.startswith("ينقسم اللفظ باعتبار المدلول وحده إلى خمسة أقسام")
    d = json.loads(FRAME.read_text(encoding="utf-8"))
    values = d["values"]
    assert len(values) == 6 and values[-1] == "ليس جنسًا"
    assert "مدلول اللفظ معنى" in line
    for v in values[1:5]:
        assert v in line, v


def test_frame_has_one_row_per_genus_and_nothing_is_tagged_before_signing() -> None:
    d = json.loads(FRAME.read_text(encoding="utf-8"))
    assert [r["book"] for r in d["rows"]] == [g[0] for g in GENERA] and len(d["rows"]) == 73
    assert [r["title"] for r in d["rows"]] == [g[1] for g in GENERA]
    assert set(TAGS) == {g[0] for g in GENERA} and set(PROPOSALS) == set(TAGS)
    assert bool(d["signed_by"]) == SIGNED
    if not SIGNED:
        assert all(v is None for v in TAGS.values())  # الآلةُ لا تصنّف بدلًا من المالك
    # الاقتراحُ رأيٌ معروضٌ: كتابُ خلق الإنسان معنى، «باب الممدود» لفظٌ مفرد، والسِّفرُ ليس جنسًا
    by_title = {r["title"]: r["proposal"] for r in d["rows"]}
    assert by_title["كتاب خلق الإنسان"] == "مدلول اللفظ معنى"
    assert by_title["باب الممدود"] == "لفظاً مفرداً مستعملاً"
    assert by_title["السفر السادس"] == "ليس جنسًا"
    # الحكمُ لا يقرأ الاقتراح
    src = (ROOT / "src" / "slge" / "hukm.py").read_text(encoding="utf-8")
    assert "PROPOSALS" not in src and "proposal" not in src


def test_mutations_are_refused_by_name() -> None:
    m = _tool()
    d = m.read_frame()
    m.verify(d)
    bad = copy.deepcopy(d)
    bad["rows"][1]["madlul"] = "جنسٌ حسّيّ"  # قيمةٌ ليست من قسمة 409
    with pytest.raises(SystemExit, match="VALUE_NOT_IN_409"):
        m.verify(bad)
    bad = copy.deepcopy(d)
    bad["signed_by"] = "x"  # توقيعٌ على إطارٍ فيه فراغ
    bad["rows"][1]["madlul"] = None
    with pytest.raises(SystemExit, match="SIGNED_FRAME_HAS_EMPTY_ROW"):
        m.verify(bad)
    bad = copy.deepcopy(d)
    bad["rows"][1]["title"] = "كتاب آخر"
    with pytest.raises(SystemExit, match="FRAME_DRIFTED_FROM_GENERA"):
        m.verify(bad)
    bad = copy.deepcopy(d)
    bad["values"] = [*d["values"], "علامة_جزء"]
    with pytest.raises(SystemExit, match="VALUES_ARE_NOT_NABHANI_409"):
        m.verify(bad)
    # التوقيعُ وحده يُدخل الوسوم: «ليس جنسًا» لا قسمَ له
    signed = copy.deepcopy(d)
    signed["signed_by"] = "اختبار"
    for r in signed["rows"]:
        r["madlul"] = r["proposal"]
    m.verify(signed)
    tags = dict(m.tags(signed))
    assert tags[1] == "مدلول اللفظ معنى" and tags[413] is None
    assert all(v is None for v in dict(m.tags(d)).values()) or bool(d["signed_by"])


def test_python_tags_match_the_lean_export() -> None:
    rows = (ROOT / "formal" / "out" / "madlul_table.csv").read_text(encoding="utf-8").splitlines()
    assert rows[0] == f"signed,{'true' if SIGNED else 'false'}"
    exported = [r.split(",") for r in rows if r.startswith("tag,")]
    assert [(int(b), None if t == "-" else t) for _, b, t in exported] == list(TAGS.items())
