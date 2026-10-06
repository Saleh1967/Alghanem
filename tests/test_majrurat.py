"""المجرورات: الجرُّ عمليّةٌ واحدة وعلاماتُه ثلاث، وسببُه في الحدّ، والقياسُ على MASAQ."""

from __future__ import annotations

import gzip
import json
from pathlib import Path

from slge.adad import uqud
from slge.cells import STATES, licensed
from slge.khamsa import KHAMSA, form
from slge.majrurat import HARFS, PROCLITIC, dual, jarr, jarr_nakira, mudaf, mudaf_dual, mudaf_uqud
from slge.mansubat import derived
from slge.marifa import al
from slge.nida import has_tanwin
from slge.rawabit import PARTICLES, cells_of, govern
from slge.sarf import illa, mamnu_jarr
from slge.tawabi import case_class, compatible, follows

_A, _I, _U, SUKUN = STATES
SLICE = Path(__file__).parent / "data" / "masaq-majrurat.json.gz"
_ST = dict(zip("0123", STATES, strict=True))


def test_one_operation_three_markers() -> None:
    rajul = cells_of("رَجُلُ")
    assert case_class(jarr(rajul)) == "جرّ" and compatible(case_class(jarr_nakira(rajul)), "جرّ")
    assert licensed(jarr(rajul)) and govern("جرّ", jarr(rajul)) and has_tanwin(jarr_nakira(rajul))
    assert compatible(case_class(uqud(rajul, False)), "جرّ")
    assert compatible(case_class(dual(rajul)), "جرّ")
    assert case_class(form(KHAMSA[0], "جر")).startswith("لا تقرؤه")
    masajid = cells_of("مَسَاجِدُ")
    assert case_class(mamnu_jarr(masajid)) == "نصب" and illa(masajid) == "صيغة منتهى الجموع"
    assert al(jarr(masajid)) == cells_of("اَلْمَسَاجِدِ")
    assert case_class(cells_of("إِيمَانِ")) == case_class(cells_of("رَجُلَانِ")) == "رفع"  # خانةٌ واحدة


def test_sabab_in_boundary() -> None:
    for h in HARFS:
        assert licensed(cells_of(h)), h
    amal = {p.name: p.amal for p in PARTICLES}
    assert all(amal[h] == "جرّ" for h in ("بِ", "لِ", "كَ", "مِنْ", "إِلَى", "عَنْ", "عَلَى", "حَتَّى"))
    rajul = cells_of("رَجُلُ")
    for h in PROCLITIC:
        assert licensed(cells_of(h) + jarr(rajul)), h
    # تَاللَّهِ ووَاللَّهِ بخانات البوّابة (ال + لّ ⇒ لْ لَ): الثلاثيُّ يرخّص الأولى والثنائيُّ يردّها
    assert not licensed(cells_of("تَالْلَهِ")) and licensed(cells_of("وَلْلَهِ"))
    kitab = mudaf(cells_of("كِتَابٌ"), jarr_nakira(cells_of("مُحَمَّدُ")))
    assert kitab == cells_of("كِتَابُ") + cells_of("مُحَمَّدٍ") and not has_tanwin(kitab[:4])
    assert mudaf_uqud(cells_of("مُهَنْدِسُ"), True) == cells_of("مُهَنْدِسُو")
    assert mudaf_dual(rajul) == cells_of("رَجُلَيْ")
    assert derived(cells_of("صَانِعُ")) and not derived(cells_of("كِتَابُ"))
    assert follows(jarr_nakira(rajul), jarr_nakira(cells_of("صَالِحُ")))


def test_masaq_measurement_and_index() -> None:
    import subprocess
    import sys

    with gzip.open(SLICE, "rt", encoding="utf-8") as f:
        rows = json.load(f)
    ok = {"الكسرة": 0, "الياء": 0, "الفتحة": 0}
    tot = dict.fromkeys(ok, 0)
    mudaf_tanwin = [0, 0]
    for r in rows:
        stem = tuple((r["s"][i], _ST[r["s"][i + 1]]) for i in range(0, len(r["s"]), 2))
        if r["c"] == "مجرور" and r["e"] == "معرب":
            m = r["m"].replace("الفتحة (ممنوع من الصرف)", "الفتحة")
            if m in ok:
                tot[m] += 1
                cc = case_class(stem)
                ok[m] += {"الكسرة": compatible(cc, "جرّ"),
                          "الياء": cc in ("نصب/جرّ", "لا تقرؤه الخانة"),
                          "الفتحة": cc == "نصب"}[m]
        if r["u"] and r["e"] == "معرب":
            mudaf_tanwin[bool(r["t"]) or has_tanwin(stem)] += 1
    assert ok["الكسرة"] * 100 >= 97 * tot["الكسرة"]
    assert ok["الياء"] * 100 >= 95 * tot["الياء"]
    assert ok["الفتحة"] * 100 >= 90 * tot["الفتحة"]
    assert mudaf_tanwin[0] * 100 >= 98 * sum(mudaf_tanwin)  # المضافُ لا يُنوَّن (والعوضُ مسمًّى)
    root = Path(__file__).parent.parent
    res = subprocess.run([sys.executable, str(root / "tools" / "gen_majrurat_index.py"), "--check"],
                         capture_output=True, text=True, cwd=root)
    assert res.returncode == 0, res.stderr
