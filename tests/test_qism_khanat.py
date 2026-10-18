"""قسمُ الكلمة من الخانات (ADR ١٠٦، `A116/QismKhanat.lean`، `tools/gen_qism_khanat.py`).

* المراسي أسطرٌ بأعيانها في «الكتاب» المختوم (JK006989) وشرح ابن عقيل المختوم.
* العلاماتُ على ذرّاتٍ مكتوبةٍ هنا باليد، وعلى ذرّات البوّابة لكلماتٍ بأعيانها.
* قاعدةُ الاختيار والأعدادُ المشتقّة في `result.json` تُعاد بحسابٍ مستقلّ من أعداده الخام.
* وفي `-m slow`: السقفُ وقارئُ العلامات بشيفرةٍ مستقلّة على المجتمع نفسه، وأعدادُ شاهدَي Lean.
"""

from __future__ import annotations

import gzip
import hashlib
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import pytest

import gate

ROOT = Path(__file__).resolve().parents[1]
LEAN = (ROOT / "formal/a116/A116/QismKhanat.lean").read_text(encoding="utf-8")
PREREG = ROOT / "docs/qism-khanat/PREREG.md"
RESULT = json.loads((ROOT / "docs/qism-khanat/result.json").read_text(encoding="utf-8"))


def _tool() -> Any:
    path = ROOT / "tools/gen_qism_khanat.py"
    spec = importlib.util.spec_from_file_location("gen_qism_khanat", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen_qism_khanat"] = mod
    spec.loader.exec_module(mod)
    return mod


G = _tool()


def lines(rel: str) -> list[str]:
    return gzip.decompress((ROOT / rel).read_bytes()).decode("utf-8").splitlines()


KITAB = {110: "فنحو ثم وسوف", 120: "الزوائد الأربع الهمزة", 121: "والتاء والياء والنون",
         123: "وللحاق التنوين", 124: "من الأفعال لن", 125: "والجزم لم يفعل",
         129: "وسوف يفعل ذلك", 130: "كما تلحق الألف واللام الأسماء"}
AQIL = {223: "بالجر والتنوين والندا وأل", 265: "تاء التأنيث", 266: "فاحترزنا بالساكنة",
        270: "بياء أفعلي", 271: "تضربين", 275: "ومما يميز الفعل نون أقبلن",
        276: "لنسفعا", 280: "كهل وفي ولم", 282: "بخلوه عن علامات الأسماء", 286: "مختص بالأسماء كفي"}


def test_anchors() -> None:
    k = lines("corpora/kitab/0180Sibawayhi.KitabSibawayhi.JK006989-ara1.gz")
    for n, s in KITAB.items():
        assert s in k[n - 1], (n, s)
    a = lines("corpora/ibn-aqil/sharh-alfiyya.txt.gz")
    for n, s in AQIL.items():
        assert s in a[n - 1], (n, s)
    pre = PREREG.read_text(encoding="utf-8")
    for n in ("س109–110", "س123", "س124–125", "س129", "س130", "س265–266", "س270–271",
              "س274–276", "س280", "س282", "س286"):
        assert n in pre, n


# (الذرّات، ذرّاتُ السابق، العلامة، يُطلق؟) — باليد.
HAND = [
    (("قَ", "اْ", "لَ", "تْ"), None, "TA_SAKINA", True),
    (("رَ", "حْ", "مَ", "تَ", "نْ"), None, "TA_SAKINA", False),   # تاءُ الاسم متحرّكة
    (("رَ", "حْ", "مَ", "تُ"), None, "TA_SAKINA", False),
    (("قُ", "لْ", "تُ"), None, "TA_FAIL", True),
    (("ءَ", "نْ", "تَ"), None, "TA_FAIL", True),                    # «أَنْتَ»: خطأُ العلامة
    (("ءَ", "لْ", "لَ", "اْ"), None, "AL", True),                    # «أَلَّا»: خطأُ العلامة
    (("وَ", "لْ", "كِ", "تَ", "اْ", "بِ"), None, "AL", True),
    (("يَ", "كُ", "نْ"), None, "TANWIN", True),                     # جزمُ «يَكُنْ» كالتنوين
    (("يَ", "كُ", "نْ"), ("لَ", "مْ"), "BAD_LAM_LAN_SAWFA", True),
    (("يَ", "كُ", "نْ"), ("مِ", "نْ"), "BAD_LAM_LAN_SAWFA", False),
    (("سَ", "نَ", "تِ", "نْ"), None, "SA", True),                    # «سَنَةٍ»: خطأُ العلامة
    (("سَ", "يَ", "قُ", "وْ", "لُ"), None, "SA", True),
    (("ثُ", "مْ", "مَ"), None, "HARF_LAFZ", True),
    (("ثُ", "مْ", "مَ", "ا"), None, "HARF_LAFZ", False),
    (("لَ", "يَ", "خْ", "رُ", "جَ", "نْ", "نَ"), None, "NUN_TAWKID", True),
    (("تَ", "ضْ", "رِ", "بِ", "يْ", "نَ"), None, "YA_FAILA", True),
    (("دَ", "اْ", "رِ"), ("فِ", "يْ"), "BAD_FI", True),
]


def test_signs_by_hand() -> None:
    for w, p, name, expect in HAND:
        assert G.SIGNS[name][0](w, p) is expect, (w, name)


def test_gate_atoms() -> None:
    # ذرّاتُ البوّابة للكلمات التي تقوم عليها العلامات.
    for word, atoms in [("قَالَتْ", ("قَ", "اْ", "لَ", "تْ")),
                        ("رَحْمَةً", ("رَ", "حْ", "مَ", "تَ", "نْ")),
                        ("يَكُن", ("يَ", "كُ", "نْ")), ("فِي", ("فِ", "يْ")),
                        ("عَلَى", ("عَ", "لَ", "اْ")), ("عَلَا", ("عَ", "لَ", "اْ"))]:
        assert tuple(gate.enter(word.encode()).atoms) == atoms, word  # type: ignore[union-attr]
    # «عَلَى» و«عَلَا» ذرّاتٌ واحدة وعددان: الرتبةُ في عدد الشهادة.
    a, b = gate.enter("عَلَى".encode()), gate.enter("عَلَا".encode())
    assert a.integer != b.integer  # type: ignore[union-attr]


def kept_by_rule(sel: dict[str, dict[str, Any]], pct: int = 1) -> list[str]:
    return [n for n, s in sel.items()
            if s["fires_A"] >= 1 and 100 * s["misfires_A"] <= pct * s["fires_A"]]


def test_result_consistent() -> None:
    r = RESULT
    assert r["prereg_sha256"] == hashlib.sha256(PREREG.read_bytes()).hexdigest()
    assert sorted(kept_by_rule(r["selection"])) == sorted(r["kept"])
    k, n = r["K"], r["n_B"]
    assert k["muayyan"] + k["muhtamal"] + k["la_hukm"] == n
    assert k["wrong"] == k["muayyan"] - k["sahih"]
    assert k["wrong"] <= sum(k["misfires_B"].values())        # `khata_qari_le` عددًا
    assert abs(k["muayyan_share"] - k["muayyan"] / n) < 1e-6
    # `damj_la_yazid`: نسيانُ الرتبة لا يرفع السقف.
    assert r["ceiling_atoms"] <= r["ceiling_integer"] <= n
    assert r["H1_precision_ge_99"] == (100 * k["sahih"] >= 99 * k["muayyan"])
    # MUTANT_THRESHOLD_5: عتبةٌ أرخى تُبقي «AL» فيتغيّر المُبقى.
    assert sorted(kept_by_rule(r["selection"], 5)) != sorted(r["kept"])


def test_lean_text() -> None:
    for name in ("TA_SAKINA", "BAD_LAM_LAN_SAWFA", "HARF_LAFZ", "AL"):
        assert f"`{name}`" in LEAN, name
    assert "⟨437, 0, 115⟩" in LEAN and "⟨30, 5, 0⟩" in LEAN
    assert "85 من 4,804" in LEAN
    s = RESULT["selection"]["AL"]
    assert (s["misfires_A"], s["fires_A"]) == (85, 4804)


def harf_by_absence(cands: tuple[int, ...]) -> tuple[int, ...]:
    """MUTANT_HARF_BY_ABSENCE: الخلوُّ من العلامات حرف."""
    return (2,) if cands == (0, 1, 2) else cands


@pytest.mark.slow
def test_independent_recount() -> None:
    rows, _ = G.population()
    b = [x for x in rows if x[0] % 2 == 0]
    kept = RESULT["kept"]
    mu = sa = 0
    mu_mut = sa_mut = 0
    for _s, w, p, _n, q in b:
        fired = [G.SIGNS[k] for k in kept if G.SIGNS[k][0](w, p)]
        c = tuple(x for x in (0, 1, 2) if all(x in keep for _f, keep in fired))
        if len(c) == 1:
            mu += 1
            sa += c[0] == q
        m = harf_by_absence(c)
        if len(m) == 1:
            mu_mut += 1
            sa_mut += m[0] == q
    assert (mu, sa) == (RESULT["K"]["muayyan"], RESULT["K"]["sahih"])
    assert sa_mut * 100 < 99 * mu_mut          # الطفرةُ تُسقط H1
    per: dict[tuple[str, ...], Counter[int]] = defaultdict(Counter)
    for _s, w, _p, _n, q in b:
        per[w][q] += 1
    assert sum(max(c.values()) for c in per.values()) == RESULT["ceiling_atoms"]
    assert per[("مَ", "اْ")] == Counter({0: 437, 2: 115})
    assert per[("ءَ", "عْ", "لَ", "مُ")] == Counter({0: 30, 1: 5})
