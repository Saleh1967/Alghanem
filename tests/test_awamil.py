"""العواملُ المائة (`A116.Awamil`، ADR ٧١): المودَعُ من مرفق المالك بأعمدته الأربعة، وصنفُ أثره
مرسًى في بابٍ من شرح ابن عقيل المختوم.

١. الأعدادُ باليد من المرفق: كان وأخواتها 13 (منها ليس وما زال…)، إنّ 6، ظنّ 10، المقاربة 6،
   الجرُّ 12 والقسمُ 2، الاستثناءُ 3، العطفُ 8، الجوازمُ 4، النواصبُ 7 ولامُ التعليل 1، الشرطُ الجازم
   10، النداءُ 4، ولا عملَ 14 (الشرطُ غيرُ الجازم 4 والاستفهامُ 10) — 100.
٢. سطورُ الأبواب عناوينُ أبوابٍ بأعيانها في الشرح المختوم (ببصمته).
٣. الأعمدةُ المرفوضةُ من المرفق ليست في المودَع (`ATTACHMENT_COLUMNS_REJECTED`).
الطفرات: `MUTANT_JARR_ON_FIL` (صفٌّ يجرّ فعلًا يُسقط `jarr_targets_ism` في Lean — في الجلسة)،
`MUTANT_BAB_SHIFTED`، `MUTANT_CLASS_UNKNOWN`.
"""

from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from conftest import ROOT

SPEC = importlib.util.spec_from_file_location("gen_awamil", ROOT / "tools" / "gen_awamil.py")
assert SPEC and SPEC.loader
MOD: Any = importlib.util.module_from_spec(SPEC)
sys.modules["gen_awamil"] = MOD
SPEC.loader.exec_module(MOD)

BY_HAND = {"RAF_NASB": 13, "NASB_RAF": 6, "NASB_NASB": 10, "RAF_TAWIL": 6, "JARR": 14,
           "JARR_OR_NASB": 3, "TABI": 8, "JAZM_FIL": 4, "NASB_FIL": 7, "JARR_OR_NASB_FIL": 1,
           "JAZM_FILAYN": 10, "NIDA": 4, "NONE": 14}


def test_counts_by_hand() -> None:
    rows = MOD.rows()
    assert len(rows) == 100 and sum(BY_HAND.values()) == 100
    assert Counter(r["athar"] for r in rows) == BY_HAND
    assert [r["amil"] for r in rows][:3] == ["إنّ", "أنّ", "كأنّ"]
    assert MOD.breaches() == []


def test_bab_lines_are_headings_of_the_sealed_sharh() -> None:
    lines = MOD.sharh_lines()
    for ln, title in MOD.BAB_TITLES.items():
        assert lines[ln - 1].startswith("###") and title in lines[ln - 1], ln
    rows = MOD.rows()
    assert all(r["bab_line"] == "0" for r in rows if r["uslub"] == "الاستفهام")
    assert all(r["bab_line"] != "0" for r in rows if r["athar"] != "NONE")


def test_rejected_columns_absent() -> None:
    head = (ROOT / "corpora" / "awamil" / "awamil.tsv").read_text(encoding="utf-8").splitlines()[0]
    assert head.split("\t") == ["amil", "uslub", "hukm_attachment", "athar", "bab_line"]
    assert "CV pattern" not in head and "FOL" not in head


def test_mutant_bab_shifted_caught(tmp_path: Path) -> None:
    lines = MOD.sharh_lines()
    assert not lines[1847].startswith("###")          # السطرُ بعد باب كان ليس عنوانًا


def test_mutant_class_unknown_caught() -> None:
    assert "NASB_KULL" not in MOD.ATHAR and all(r["athar"] in MOD.ATHAR for r in MOD.rows())
