"""البروتوكول في الدستور (الباب الرابع، ADR ١١١): توثيقُ كلّ خطوة، وسجلُّ طفرات Lean.

* سجلُّ الخطوات يُقرأ بقاعدته، والرسالةُ بلا خطوةٍ أو بخطوةٍ غيرِ مسجَّلة مرفوضةٌ باسمها.
* سجلُّ الطفرات: كلُّ نصٍّ يقع مرّةً واحدة في ملفّه، وADR كلِّ طفرةٍ موجود؛ والمكرَّرُ والملتبسُ مرفوضان.
* الدستورُ يحمل المواد ١٨–٢٤ بأسمائها، ونصَّ المالك بعينه.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONST = (ROOT / "AGENT_CONSTITUTION.md").read_text(encoding="utf-8")


def _load(name: str) -> Any:
    path = ROOT / "tools" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


P = _load("gen_protocol")
T = _load("gen_tafrat")
H = "khutwa\ttarikh\tunwan\tadr\tfuhus\n"


def test_log_by_hand() -> None:
    rows, errs = P.parse(H + "STEP-0001\t2026-10-18\tت\t111\ttafrat;protocol\n")
    assert errs == [] and rows == {"STEP-0001": ["tafrat", "protocol"]}
    # MUTANT_CHECK_NOT_IN_LIST: فحصٌ خارج القائمة المغلقة.
    _, errs = P.parse(H + "STEP-0001\t2026-10-18\tت\t111\ttafrat;مرّ_كلّه\n")
    assert errs == ["STEP_CHECK_UNKNOWN STEP-0001 مرّ_كلّه"]
    # MUTANT_STEP_SKIPPED: قفزٌ في الترقيم.
    row = "\t2026-10-18\tت\t111\ttafrat\n"
    _, errs = P.parse(H + "STEP-0001" + row + "STEP-0003" + row)
    assert errs == ["STEP_ORDER_BROKEN STEP-0003"]
    # ADR لا ملفَّ له.
    _, errs = P.parse(H + "STEP-0001\t2026-10-18\tت\t9999\ttafrat\n")
    assert errs == ["STEP_ADR_MISSING STEP-0001 9999"]


def test_message_by_hand() -> None:
    rows = {"STEP-0001": ["tafrat"]}
    assert P.message_errors("عنوان\n\nخطوة: STEP-0001\n", rows) == []
    assert P.message_errors("عنوانٌ بلا خطوة\n", rows) == ["STEP_UNDOCUMENTED"]
    assert P.message_errors("خطوة: STEP-0002\n", rows) == ["STEP_UNKNOWN STEP-0002"]


def test_deposited_log() -> None:
    rows, errs = P.parse((ROOT / "docs/protocol/khutuwat.tsv").read_text(encoding="utf-8"))
    assert errs == [] and "STEP-0001" in rows
    assert P.ADOPTION == "STEP-0001"


def test_tafrat_registry() -> None:
    rows = json.loads((ROOT / "docs/tafrat.json").read_text(encoding="utf-8"))
    assert T.validate(rows) == []
    assert len({r["ism"] for r in rows}) == len(rows) >= 10
    # MUTANT_DUPLICATE_NAME وMUTANT_AMBIGUOUS_TEXT: اسمٌ مكرّر، ونصٌّ يقع أكثر من مرّة.
    bad = [dict(rows[0]), dict(rows[0], min="theorem", ila="lemma")]
    errs = T.validate(bad)
    assert f"MUTANT_NAME_DUPLICATED {rows[0]['ism']}" in errs
    assert any(e.startswith(f"MUTANT_TEXT_NOT_UNIQUE {rows[0]['ism']}") for e in errs)


def test_constitution_part_four() -> None:
    for n in ("١٨", "١٩", "٢٠", "٢١", "٢٢", "٢٣", "٢٤"):
        assert f"## المادّة {n} —" in CONST, n
    for v in ("PROTOCOL_BYPASSED", "STEP_UNDOCUMENTED", "MUTANT_NOT_IN_CI",
              "ABSENCE_WITHOUT_SEARCH", "QUOTE_NOT_VERBATIM", "BUILDER_CHOICE_UNDECLARED",
              "COVERAGE_AS_ACCURACY",
              "MAFHUM_USUL_AS_MARTABA"):
        assert f"`{v}`" in CONST, v
    words = ("موافق على الخطة وان تكون بروتوكول جزء من الدستور وان تكون حاكمة لكل مدخلات"
             " ومخرجات المستودعات وان توثق كل خطوة")
    assert f"«{words}»" in CONST
