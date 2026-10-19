"""سدُّ الفجوة (ADR ١٠٧، `A116/QismAwamil.lean`، التسجيلُ الثاني في `tools/gen_qism_khanat.py`).

* قسمُ المعمول في الأداة هو `A116.Awamil.target` بنصّ Lean.
* قوالبُ المضارع هي صفوفُ «صبر» في `amr.csv` بأعيانها.
* العلاماتُ الجديدة على ذرّاتٍ مكتوبةٍ هنا باليد.
* المراسي في أسطرها من شرح ابن عقيل المختوم.
* قاعدةُ الاختيار والأعدادُ المشتقّة في `result-2.json` تُعاد من الأعداد الخام.
"""

from __future__ import annotations

import gzip
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LEAN = (ROOT / "formal/a116/A116/QismAwamil.lean").read_text(encoding="utf-8")
AWAMIL_LEAN = (ROOT / "formal/a116/A116/Awamil.lean").read_text(encoding="utf-8")
PREREG2 = ROOT / "docs/qism-khanat/PREREG-2.md"
R2 = json.loads((ROOT / "docs/qism-khanat/result-2.json").read_text(encoding="utf-8"))
R1 = json.loads((ROOT / "docs/qism-khanat/result.json").read_text(encoding="utf-8"))


def _tool() -> Any:
    path = ROOT / "tools/gen_qism_khanat.py"
    spec = importlib.util.spec_from_file_location("gen_qism_khanat", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen_qism_khanat"] = mod
    spec.loader.exec_module(mod)
    return mod


G = _tool()
CAMEL = {"nasbRaf": "NASB_RAF", "rafNasb": "RAF_NASB", "nasbNasb": "NASB_NASB",
         "rafTawil": "RAF_TAWIL", "jarr": "JARR", "jarrOrNasb": "JARR_OR_NASB",
         "jarrOrNasbFil": "JARR_OR_NASB_FIL", "nida": "NIDA", "jazmFil": "JAZM_FIL",
         "nasbFil": "NASB_FIL", "jazmFilayn": "JAZM_FILAYN", "tabi": "TABI", "none": "NONE"}


def test_target_is_lean() -> None:
    start = AWAMIL_LEAN.index("def target")
    body = AWAMIL_LEAN[start:AWAMIL_LEAN.index("theorem", start)]
    expect: dict[str, int | None] = {}
    rhs_q = {"some .ism": 0, "some .fil": 1, "Option.none": None}
    pat = r"((?:\|\s*\.\w+\s*)+)=>\s*(some \.ism|some \.fil|Option\.none)"
    for lhs, rhs in re.findall(pat, body):
        for name in re.findall(r"\.(\w+)", lhs):
            expect[CAMEL[name]] = rhs_q[rhs]
    assert len(expect) == 13
    assert expect == G.TARGET


def test_mudari_templates_from_amr() -> None:
    ts = G.mudari_templates()
    assert len(ts) == 11
    # باليد: «يَصْبَرُ» و«يَسْتَصْبِرُ».
    assert ts[0] == [("P", "َ"), ("R1", "ْ"), ("R2", "َ"), ("R3", "*")]
    assert ts[-1] == [("P", "َ"), ("س", "ْ"), ("ت", "َ"), ("R1", "ْ"), ("R2", "ِ"), ("R3", "*")]


ROOTS = frozenset({"عبد", "صبر", "كتب", "علم", "قتل"})
HAND_MUDARI = [(("نَ", "عْ", "بُ", "دُ"), True), (("وَ", "سَ", "يَ", "عْ", "لَ", "مُ"), True),
               (("يَ", "صْ", "بِ", "رُ", "وْ", "نَ"), True), (("يَ", "وْ", "مَ"), False),
               (("ءَ", "عْ", "لَ", "مُ"), True),       # اسمُ التفضيل يوافق: خطأُ العلامة
               (("كَ", "تَ", "بَ"), False)]
HAND_ISM = [(("ءَ", "صْ", "صَ", "اْ", "بِ", "رِ", "يْ", "نَ"), True),
            (("مَ", "كْ", "تُ", "وْ", "بُ", "نْ"), True),
            (("قَ", "اْ", "تِ", "لْ"), True),              # أمرُ فاعَلَ يوافق: خطأُ العلامة
            (("كَ", "تَ", "بَ"), False), (("وَ", "لْ", "عَ", "اْ", "لِ", "مِ"), True)]


def test_wazn_by_hand() -> None:
    ts = G.mudari_templates()
    for w, e in HAND_MUDARI:
        assert G.mudari_wazn(w, ts, ROOTS) is e, w
    for w, e in HAND_ISM:
        assert G.ism_wazn(w, ROOTS) is e, w


def test_awamil_by_hand() -> None:
    rows = G.awamil()
    assert G.amil_own("JARR", ("مِ", "نْ"), rows) == 2
    assert G.amil_own("JARR", ("مَ", "نْ"), rows) is None        # «مَن» ليست «من» الجارّة وحدَها
    assert G.amil_own("NASB_FIL", ("ءَ", "نْ"), rows) == 2
    assert G.amil_own("JAZM_FILAYN", ("ءِ", "نْ"), rows) == 2
    assert G.amil_own("NASB_RAF", ("فَ", "ءِ", "نْ", "نَ"), rows) == 2
    assert G.amil_own("RAF_NASB", ("كَ", "اْ", "نَ"), rows) == 1
    assert G.amil_next("JARR", ("فِ", "يْ"), rows) == 0
    assert G.amil_next("JAZM_FIL", ("لَ", "مْ"), rows) == 1
    assert G.amil_next("TABI", ("ثُ", "مْ", "مَ"), rows) is None
    # MUTANT_JAZM_FILAYN_ALL_ISM: «إنْ» اسمًا يُسقط علامتَها حرفًا.
    old = G.own_of
    try:
        G.own_of = lambda n, a: 0 if a == "JAZM_FILAYN" else old(n, a)
        assert G.amil_own("JAZM_FILAYN", ("ءِ", "نْ"), rows) != 2
    finally:
        G.own_of = old


def test_anchors() -> None:
    a = gzip.decompress((ROOT / "corpora/ibn-aqil/sharh-alfiyya.txt.gz").read_bytes()).decode(
        "utf-8").splitlines()
    for n, s in {280: "كهل وفي ولم", 348: "وأسماء الاستفهام", 1853: "فالأفعال كان وأخواتها",
                 1854: "وإن وأخواتها", 2342: "ستة أحرف", 4635: "حروف الجر", 6446: "حروف العطف",
                 6685: "حروف النداء", 7580: "وحرف إذما", 7727: "لو حرف"}.items():
        assert s in a[n - 1], (n, s)


def kept_by_rule(sel: dict[str, Any], pct: int = 1) -> list[str]:
    return [n for n, s in sel.items()
            if s["fires_A"] >= 1 and 100 * s["misfires_A"] <= pct * s["fires_A"]]


def test_result2_consistent() -> None:
    r = R2
    assert r["prereg_sha256"] == hashlib.sha256(PREREG2.read_bytes()).hexdigest()
    assert sorted(kept_by_rule(r["selection"])) == sorted(r["kept_new"])
    k, n = r["K2"], r["n_B"]
    assert k["muayyan"] + k["muhtamal"] + k["la_hukm"] == n == R1["n_B"]
    assert k["wrong"] == k["muayyan"] - k["sahih"] <= k["sum_misfires_B"]   # `khata_qari_le`
    # فحصٌ على هذه النتيجة لا مثولٌ لمبرهنة: `muayyan_baqi` يجيز أن يصير المعيَّنُ «لا حكم».
    assert k["muayyan"] >= R1["K"]["muayyan"]
    assert r["ceiling_atoms"] == R1["ceiling_atoms"] <= r["ceiling_prev_atoms"] <= n
    assert r["H2_more_than_K"] == (k["muayyan"] > R1["K"]["muayyan"])
    # MUTANT_THRESHOLD_10: عتبةٌ أرخى تُبقي `MUDARI_WAZN` فيتغيّر المُبقى.
    assert sorted(kept_by_rule(r["selection"], 10)) != sorted(r["kept_new"])


def test_lean_text() -> None:
    for s in ('cell "مِنْ"', 'cell "ءَنْ"', 'cell "ءَعْلَمُ"', 'cell "قَاْتِلْ"'):
        assert s in LEAN, s
