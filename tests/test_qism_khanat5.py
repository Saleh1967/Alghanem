"""القياسُ على جدول العوامل الموقَّع بتفويض المالك (ADR ١١٠، التسجيلُ الخامس).

* الجدولُ الثاني يختلف عن الأوّل في أربعة صفوفٍ باليد، وبصمتُه في سجلّ التوقيع وفي النتيجة.
* `result-5.json` متّسقٌ مع أعداده الخام ومع قاعدة اختيار الأداة، وطفرةٌ على الأداة.
* سببُ سقوط `AMIL_OWN_N_NASB_NASB_1`: «ظَنَّ» اسمٌ في آل عمران 154 بوسم QAC المختوم.
"""

from __future__ import annotations

import gzip
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import gate

ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT / "corpora/awamil/awamil-mashkul.tsv"
V2 = ROOT / "corpora/awamil/awamil-mashkul-2.tsv"
SIG = json.loads((ROOT / "corpora/awamil/owner-mashkul.json").read_text(encoding="utf-8"))
R4 = json.loads((ROOT / "docs/qism-khanat/result-4.json").read_text(encoding="utf-8"))
R5 = json.loads((ROOT / "docs/qism-khanat/result-5.json").read_text(encoding="utf-8"))
QAC = ROOT / "corpora/qac/quranic-corpus-morphology-0.4.txt.gz"
F, D, S = "َ", "ُ", "ّ"


def _tool() -> Any:
    path = ROOT / "tools/gen_qism_khanat.py"
    spec = importlib.util.spec_from_file_location("gen_qism_khanat", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen_qism_khanat"] = mod
    spec.loader.exec_module(mod)
    return mod


G = _tool()


def test_signature() -> None:
    sha2 = hashlib.sha256(V2.read_bytes()).hexdigest()
    assert SIG["sha256"] == sha2 == R5["mashkul_sha256"]
    sha1 = hashlib.sha256(V1.read_bytes()).hexdigest()
    assert SIG["supersedes_for_new_measurements"]["sha256"] == sha1
    assert SIG["owner_words"].startswith("موافق وقع انت مفوض")
    assert "بتفويض" in SIG["signed_by"]


def test_four_rows_by_hand() -> None:
    a = V1.read_text(encoding="utf-8").splitlines()
    b = V2.read_text(encoding="utf-8").splitlines()
    assert len(a) == len(b)
    diff = {x.split("\t")[0]: (x.split("\t")[2], y.split("\t")[2])
            for x, y in zip(a, b, strict=True) if x != y}
    assert diff == {
        "ظن" + S + F: ("", "ظ" + F + "ن" + S + F),
        "عد" + S + F: ("", "ع" + F + "د" + S + F),
        "ر" + D + "ب" + S + F: ("", "ر" + D + "ب" + S + F),
        "إذن": ("إِذَنْ", "إ" + "ِ" + "ذ" + "ا" + "ً"),
    }


def test_result5_consistent() -> None:
    r = R5
    assert r["prereg_sha256"] == hashlib.sha256(
        (ROOT / "docs/qism-khanat/PREREG-5.md").read_bytes()).hexdigest()
    for name in ("D1", "D1_sub", "D3"):
        x = r[name]
        assert x["muayyan"] + x["muhtamal"] + x["la_hukm"] == r["n_B"]
        assert x["wrong"] == x["muayyan"] - x["sahih"] <= x["sum_misfires_B"]   # `khata_qari_le`
    d3 = r["D3"]
    assert d3["violations_vs_D1_sub"] == 0                                       # `daraja_tasfiya`
    assert d3["licensed"] == (100 * d3["sahih"] >= 99 * d3["muayyan"])
    assert r["D3_v1"]["muayyan"] == R4["D3"]["muayyan"]
    assert r["D3_delta_muayyan"] == d3["muayyan"] - R4["D3"]["muayyan"]
    assert r["H1"] == d3["licensed"] and r["H2"] == (r["D3_delta_muayyan"] >= 0)
    assert r["H3"] == bool(r["kept_D1_added"] or r["kept_D1_removed"])

    def kept() -> list[str]:
        return sorted(n for n, s in r["selection_D1"].items()
                      if G.keep_rule(s["fires_A"], s["misfires_A"]))
    assert kept() == sorted(r["kept_D1"])
    # MUTANT_SELECT_2 على الأداة: عتبةُ 2٪ تُبقي `AMIL_OWN_N_NASB_NASB_1` (خطأٌ واحد من 54).
    old = G.SELECT_PCT
    try:
        G.SELECT_PCT = 2
        assert "AMIL_OWN_N_NASB_NASB_1" in kept()
        assert kept() != sorted(r["kept_D1"])
    finally:
        G.SELECT_PCT = old


def test_zanna_is_noun_in_3_154() -> None:
    s = R5["selection_D1"]["AMIL_OWN_N_NASB_NASB_1"]
    assert (s["fires_A"], s["misfires_A"], s["kept"]) == (54, 1, False)
    rows = [ln.split("\t") for ln in gzip.decompress(QAC.read_bytes()).decode("utf-8").splitlines()]
    hit = [p for p in rows if p[0].startswith("(3:154:20:")]
    assert hit and hit[0][1] == "Zan~a" and hit[0][2] == "N"
    # و«ظَنَّ» فعلًا واسمًا عددٌ واحد.
    assert not isinstance(gate.enter(("ظ" + F + "ن" + S + F).encode()), gate.Refusal)
