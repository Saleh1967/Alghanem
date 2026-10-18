"""الترخيصُ التدريجيّ بقيمة الوحدة (ADR ١٠٨، `A116/QismDaraja.lean`، التسجيلُ الثالث).

* صورُ الصيغ بالقواعد المعلنة، وحلُّ عدد الشهادة، وقوالبُ المضارع: باليد.
* جدولُ العوامل المشكول (ملءُ الوكيل): هيكلُ كلّ صيغةٍ هيكلُ عاملها، و«لمّا» بشدّتها.
* المرساةُ في سطرها، و`result-3.json` متّسقٌ مع أعداده الخام.
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
R3 = json.loads((ROOT / "docs/qism-khanat/result-3.json").read_text(encoding="utf-8"))
R2 = json.loads((ROOT / "docs/qism-khanat/result-2.json").read_text(encoding="utf-8"))
LEAN = (ROOT / "formal/a116/A116/QismDaraja.lean").read_text(encoding="utf-8")
MARKS = set("ًٌٍَُِّْٰ")


def _tool() -> Any:
    path = ROOT / "tools/gen_qism_khanat.py"
    spec = importlib.util.spec_from_file_location("gen_qism_khanat", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen_qism_khanat"] = mod
    spec.loader.exec_module(mod)
    return mod


G = _tool()


def test_variants_by_hand() -> None:
    # الشدّةُ قبل الحركة، كترتيب المصحف المختوم.
    sh, ka, fa, su = "\u0651", "\u0650", "\u064e", "\u0652"
    m = "م" + ka + "ن" + su
    assert G.variants(m) == [m, "م" + ka + "ن" + ka, "م" + ka + "ن" + fa,
                             "م" + sh + ka + "ن" + su, "م" + sh + ka + "ن" + ka,
                             "م" + sh + ka + "ن" + fa]
    assert G.variants("ف" + ka + "ي") == ["ف" + ka + "ي", "ف" + sh + ka + "ي"]


def test_unpair_by_hand() -> None:
    for w, rank in [("عَلَى", 1), ("عَلَا", 0), ("قَالَ", 0)]:
        c = gate.enter(w.encode())
        f, r = G.unpair(c.integer)  # type: ignore[union-attr]
        assert r == rank == c.core.ordinal  # type: ignore[union-attr]
        assert (f + r) * (f + r + 1) // 2 + r == c.integer  # type: ignore[union-attr]


def skel(s: str) -> str:
    out = "".join(ch for ch in s.split(" (")[0] if ch not in MARKS)
    return out.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")


def test_mashkul_table() -> None:
    lines = (ROOT / "corpora/awamil/awamil-mashkul.tsv").read_text(encoding="utf-8").splitlines()
    awamil = (ROOT / "corpora/awamil/awamil.tsv").read_text(encoding="utf-8").splitlines()
    assert len(lines) == len(awamil)
    for ln, aw in zip(lines[1:], awamil[1:], strict=True):
        amil, athar, m = ln.split("\t")
        assert amil == aw.split("\t")[0] and athar == aw.split("\t")[3]
        if m:
            assert skel(m) == skel(amil), (amil, m)
    lamma = [ln.split("\t")[2] for ln in lines if ln.startswith("لما\t")]
    assert lamma == ["ل" + "\u064e" + "م" + "\u0651\u064e" + "ا"]   # «لَمَّا» بشدّتها
    sha = hashlib.sha256((ROOT / "corpora/awamil/awamil-mashkul.tsv").read_bytes()).hexdigest()
    assert sha == R3["mashkul_sha256"]


def test_mudari_templates2_by_hand() -> None:
    ts, skipped = G.mudari_templates2()
    assert (len(ts), skipped) == (R3["mudari_templates"], R3["mudari_templates_skipped"])
    # صفُّ «قوم» الأوّل في `amr.csv` (بابُ الفتح، قالبٌ آليّ لا صيغةٌ مسموعة): الأوّلُ مقعدٌ والعينُ واوٌ ثابتة.
    assert ts[0] == ("َ", [("S0", "َ"), ("ا", "ْ"), ("S2", "*")], {1: "و"})
    rs = frozenset({"قول", "بيع", "علم", "دعو"})
    assert G.mudari_wazn2(("يَ", "قُ", "وْ", "لُ"), ts, rs, "ءتين")
    assert G.mudari_wazn2(("يَ", "عْ", "لَ", "مُ", "هُ", "مْ"), ts, rs, "تين")   # ضميرُ المفعول
    assert G.mudari_wazn2(("ءَ", "عْ", "لَ", "مُ"), ts, rs, "ءتين")
    assert not G.mudari_wazn2(("ءَ", "عْ", "لَ", "مُ"), ts, rs, "تين")          # YTN بلا همزة
    assert not G.mudari_wazn2(("يَ", "وْ", "مَ"), ts, rs, "ءتين")


def test_anchor() -> None:
    a = gzip.decompress((ROOT / "corpora/ibn-aqil/sharh-alfiyya.txt.gz").read_bytes()).decode(
        "utf-8").splitlines()
    assert "كالياء والكاف من ابني أكرمك" in a[728 - 1]


def kept(sel: dict[str, Any], pct: int = 1) -> list[str]:
    return [n for n, s in sel.items()
            if s["fires_A"] >= 1 and 100 * s["misfires_A"] <= pct * s["fires_A"]]


def test_result3_consistent() -> None:
    r = R3
    assert r["prereg_sha256"] == hashlib.sha256(
        (ROOT / "docs/qism-khanat/PREREG-3.md").read_bytes()).hexdigest()
    assert sorted(kept(r["selection_D1"])) == sorted(r["kept_D1"])
    assert sorted(kept(r["selection_D2"])) == sorted(r["kept_D2"])
    d = r["degrees"]
    assert d[0]["muayyan"] == R2["K2"]["muayyan"] and d[0]["sahih"] == R2["K2"]["sahih"]
    for x in d:
        assert x["muayyan"] + x["muhtamal"] + x["la_hukm"] == r["n_B"]
        assert x["wrong"] == x["muayyan"] - x["sahih"] <= x["sum_misfires_B"]   # `khata_qari_le`
        assert x["violations_vs_previous"] == 0                                 # `daraja_tasfiya`
        ok = 100 * x["sahih"] >= 99 * x["muayyan"]
        assert x["licensed"] == (ok and x["violations_vs_previous"] == 0)
    c = r["ceilings"]
    # المفتاحُ الأدقّ لا يُنقص السقف (`tadqiq_la_yanqus`): الذرّاتُ دالّةٌ في n.
    assert c["atoms"] <= c["n"] and c["prev_atoms_atoms"] <= c["prev_n_n"] <= r["n_B"]
    assert r["H3"] and r["H2"] == (d[2]["muayyan"] > d[1]["muayyan"] and d[2]["licensed"])
    # المُبقى هو ما تقبله قاعدةُ الأداة نفسُها `keep_rule` على الأعداد الخام.
    def tool_kept() -> list[str]:
        return sorted(n for n, s in r["selection_D2"].items()
                      if G.keep_rule(s["fires_A"], s["misfires_A"]))
    assert tool_kept() == sorted(r["kept_D2"])
    # MUTANT_THRESHOLD_2 على الأداة: عتبةٌ أرخى في `SELECT_PCT` تُبقي `MUDARI_YTN` فتنكسر المطابقة.
    old = G.SELECT_PCT
    try:
        G.SELECT_PCT = 2
        assert tool_kept() != sorted(r["kept_D2"])
    finally:
        G.SELECT_PCT = old


def test_variants_effect() -> None:
    # البوّابةُ تطوي الشدّةَ الأولى: «لَّمْ» و«لَمْ» عددٌ واحد، فقاعدةُ التشديد بلا أثر (معلن في ADR ١٠٨).
    lam = "ل" + "\u064e" + "م" + "\u0652"
    gem = "ل" + "\u0651\u064e" + "م" + "\u0652"
    assert gate.enter(lam.encode()).integer == gate.enter(gem.encode()).integer  # type: ignore[union-attr]
    base, _ = G.mashkul_rows()
    old = G.variants
    try:
        # MUTANT_NO_ILTIQA على الأداة: بلا صورتَي التقاء الساكنين تنقص أعدادُ 12 صفًّا.
        G.variants = lambda m: [m]
        mut, _ = G.mashkul_rows()
        assert sum(x[2] != y[2] for x, y in zip(base, mut, strict=True)) == 12
        # وبلا قاعدة التشديد وحدَها لا يتغيّر صفّ.
        G.variants = lambda m: [m] + (
            [m[:-1] + "\u0650", m[:-1] + "\u064e"] if m.endswith("\u0652") else [])
        no_gem, _ = G.mashkul_rows()
        assert sum(x[2] != y[2] for x, y in zip(base, no_gem, strict=True)) == 0
    finally:
        G.variants = old


def test_lean_text() -> None:
    for name in ("daraja_tasfiya", "daraja_muayyan", "adaq_khata_count", "ibdal_cands", "hits_comp",
                 "ala_alaa_rabh", "wahda_radd", "wahdat_nodup", "muayyan_wahda", "shahid_darajat"):
        assert f"theorem {name}" in LEAN, name
