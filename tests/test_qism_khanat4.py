"""الإبدالُ بالأدقّ درجةً، و«ما بعد لمّا»، والوحدةُ مقارنةً بـSLGE وقسمةُ ج3 (ADR ١٠٩).

* المراسي في أسطرها: «الكتاب» المختوم س9783 وس18528–18529، والشخصيّة ج3 المختومة س373، 375، 377، 467.
* `result-4.json` متّسقٌ مع أعداده الخام ومع قاعدة اختيار الأداة نفسها.
* أعدادُ SLGE للخانة وقسمتُه باليد، ونصُّ `WahdaMuqarana.lean`.
"""

from __future__ import annotations

import gzip
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
R4 = json.loads((ROOT / "docs/qism-khanat/result-4.json").read_text(encoding="utf-8"))
LEAN = (ROOT / "formal/a116/A116/WahdaMuqarana.lean").read_text(encoding="utf-8")
KITAB = ROOT / "corpora/kitab/0180Sibawayhi.KitabSibawayhi.JK006989-ara1.gz"
KITAB_SHA = "a160f940bb194e6fe7e6655d2c7f28e41f1fc648c4c5e340cc4e42306d5cb625"
J3 = ROOT / "corpora/nabhani/shakhsiyya_j3.txt.gz"
J3_SHA = "dd57e74bec43534ceec90797ad050cb104a16925b6d0bf0304796d42e70c425e"


def _tool() -> Any:
    path = ROOT / "tools/gen_qism_khanat.py"
    spec = importlib.util.spec_from_file_location("gen_qism_khanat", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen_qism_khanat"] = mod
    spec.loader.exec_module(mod)
    return mod


G = _tool()


def sealed(path: Path, sha: str) -> list[str]:
    raw = gzip.decompress(path.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == sha
    return raw.decode("utf-8").splitlines()


def test_anchors() -> None:
    k = sealed(KITAB, KITAB_SHA)
    assert "وإذا قال قد فعل فإن نفيه لما يفعل" in k[9783 - 1]
    assert k[18528 - 1].endswith("وأما لما")
    assert "فهي للأمر الذي قد وقع لوقوع غيره وإنما تجئ بمنزلة لو" in k[18529 - 1]
    j = sealed(J3, J3_SHA)
    assert j[373 - 1].startswith("ينقسم المفرد إلى ثلاثة أقسام: اسم، وفعل، وحرف.")
    assert "فإن كان لا يستقل بمعناه، فهو الحرف" in j[373 - 1]
    assert j[375 - 1].startswith("الاسم هو ما دل على معنى في نفسه")
    assert "والفرق بينه وبين الحرف" in j[377 - 1]
    assert j[467 - 1].startswith("الحرف هو ما دل على معنى في غيره")


def kept(sel: dict[str, Any]) -> list[str]:
    return sorted(n for n, s in sel.items() if G.keep_rule(s["fires_A"], s["misfires_A"]))


def test_result4_consistent() -> None:
    r = R4
    assert r["prereg_sha256"] == hashlib.sha256(
        (ROOT / "docs/qism-khanat/PREREG-4.md").read_bytes()).hexdigest()
    for name in ("D1", "D1_sub", "D3"):
        x = r[name]
        assert x["muayyan"] + x["muhtamal"] + x["la_hukm"] == r["n_B"]
        assert x["wrong"] == x["muayyan"] - x["sahih"] <= x["sum_misfires_B"]   # `khata_qari_le`
    d1, sub, d3 = r["D1"], r["D1_sub"], r["D3"]
    lic = 100 * sub["sahih"] >= 99 * sub["muayyan"] and sub["wrong"] <= d1["wrong"]
    assert sub["licensed"] == (lic and sub["conflicts_vs_D1"] == 0)
    assert d3["violations_vs_D1_sub"] == 0                                       # `daraja_tasfiya`
    sel = r["selection_lamma"]
    assert kept(sel) == sorted(r["kept_lamma"]) == ["LAMMA_MADI_ISM"]
    # المتناقضتان على شرطٍ واحد: خطأُ إحداهما صوابُ الأخرى، ولا ثالثَ في المرجع.
    h, i = sel["LAMMA_MADI_HARF"], sel["LAMMA_MADI_ISM"]
    assert h["fires_A"] == i["fires_A"] == r["lamma_A"]["lamma_madi"]
    assert h["misfires_A"] + i["misfires_A"] == h["fires_A"]
    for part in ("lamma_A", "lamma_B"):
        s = r[part]
        assert s["agreement_with_sibawayh"] == s["lamma_madi_harf"] / s["lamma_madi"]
        assert sum(s["by_qism"].values()) == s["lamma"]
    assert r["H1"] == (sub["licensed"] and sub["wrong"] < d1["wrong"])
    assert r["H2"] == ("LAMMA_MUDARI" in r["kept_lamma"])
    assert r["H3"] == (r["lamma_A"]["agreement_with_sibawayh"] < 0.5)
    # MUTANT_SELECT_100 على الأداة: عتبةٌ 100٪ تُبقي المتناقضتين معًا، فتنكسر المطابقة.
    old = G.SELECT_PCT
    try:
        G.SELECT_PCT = 100
        assert {"LAMMA_MADI_HARF", "LAMMA_MADI_ISM"} <= set(kept(sel))
        assert kept(sel) != sorted(r["kept_lamma"])
    finally:
        G.SELECT_PCT = old


SLGE_ORDER = "ءهاعحغخقكجشيضلنرطدتزسصظذثفبمو"


def slge_cell(ch: str, s: int) -> int:
    # `SLGE.Ladder.cellEnc c s = mixEnc 1 4 c 0 s = (c·1 + 0)·4 + s`، باليد.
    return (SLGE_ORDER.index(ch) * 1 + 0) * 4 + s


def test_slge_cells_by_hand() -> None:
    assert len(SLGE_ORDER) == len(set(SLGE_ORDER)) == 29
    assert [slge_cell(c, 0) for c in "كتب"] == [32, 72, 104]
    assert "[32, 72, 104]" in LEAN and SLGE_ORDER in LEAN
    # الصيغةُ المغلقة للاقتران كما في SLGE.Core.
    assert all((u + r) * (u + r + 1) // 2 + r == sum(range(u + r + 1)) + r
               for u in range(30) for r in range(30))


def slge_kind(ind: bool, tim: bool) -> str:
    a, b = ind and not tim, ind              # SLGE.Cat.roles
    return "ism" if a else ("fil" if b else "harf")   # SLGE.Cat.kindOf


def j3_qism(istiqlal: bool, zaman: bool) -> str:
    # ج3 س373: لا يستقلّ ← حرف؛ يدلّ بهيئته على زمان ← فعل؛ وإلّا اسم.
    if not istiqlal:
        return "harf"
    return "fil" if zaman else "ism"


def test_j3_eq_slge_by_hand() -> None:
    for ind in (False, True):
        for tim in (False, True):
            assert slge_kind(ind, tim) == j3_qism(ind, tim)
    # MUTANT_ROLES_SWAP: ‎roles = (ind, ind && !tim)‎ يجعل الفعلَ اسمًا.
    assert any((("ism" if ind else ("fil" if ind and not tim else "harf")) != j3_qism(ind, tim))
               for ind in (False, True) for tim in (False, True))


def test_lean_text() -> None:
    for name in ("slgeOrder_eq_makharij", "cell_slge_eq_makharij", "word_slge", "pair_slge",
                 "encS_injective", "nPair_injective", "tarjama_n", "tarjama_aks",
                 "wahda_tusqit_rutba", "j3_eq_slge", "la_rabia", "muayyan_j3", "shawahid"):
        assert f"theorem {name}" in LEAN, name
