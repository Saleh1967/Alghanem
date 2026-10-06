"""الجزمُ والشرط: العلاماتُ الثلاث عمليّات، والأداةُ تُعدّ، والقياسُ على MASAQ."""

from __future__ import annotations

import json
from pathlib import Path

from slge.afal import STEMS, form
from slge.cells import licensed
from slge.istifham import FORMS
from slge.jazm import JAZIM_ONE, SHART_GHAYR, SHART_JAZIM, amr, drop_weak, marker, sukun, weak_final
from slge.rawabit import PARTICLES, cells_of

SLICE = Path(__file__).parent / "data" / "masaq-jazm.json"


def test_three_markers_three_operations() -> None:
    yadu, yasa, yaqdi, yaqulu = (cells_of(w) for w in ("يَدْعُو", "يَسْعَى", "يَقْضِي", "يَقُولُ"))
    assert weak_final(yadu) and weak_final(yasa) and weak_final(yaqdi) and not weak_final(yaqulu)
    assert drop_weak(yadu) == cells_of("يَدْعُ") and drop_weak(yaqdi) == cells_of("يَقْضِ")
    assert all(licensed(drop_weak(w)) for w in (yadu, yasa, yaqdi))
    assert marker(drop_weak(yadu)) == "لا تقرؤه الخانة"  # الحركةُ الباقية حركةُ الأصل
    assert not licensed(sukun(yaqulu)) and licensed(cells_of("يَقُلْ"))  # حذفُ العين ملزَم
    assert marker(cells_of("يَلِدْ")) == "سكون" and marker(cells_of("يَقُلْ")) == "سكون"
    for s in STEMS:
        assert form(s, "الجماعة", "جزم") == form(s, "الجماعة", "نصب")
        assert marker(form(s, "الجماعة", "جزم")) == "حذف النون"
    # البوّابةُ تُسقط الألفَ الفارقةَ بقيّةَ رسم (FARIQA): يَدْعُوا = يَدْعُو على الخانات
    assert cells_of("يَدْعُو") == cells_of("يَدْعُوا")[:-1]


def test_tools_counted_and_shared() -> None:
    assert len(JAZIM_ONE) == 4 and len(SHART_JAZIM) == 12 and len(SHART_GHAYR) == 7
    for w in JAZIM_ONE + SHART_JAZIM + SHART_GHAYR:
        assert licensed(cells_of(w)), w
    assert amr(cells_of("يُنْفِقْ")) == cells_of("لِيُنْفِقْ") and marker(cells_of("يُنْفِقْ")) == "سكون"
    amal = {p.name: p.amal for p in PARTICLES}
    assert amal["لَمْ"] == "جزم" and amal["لَا"] == "" and amal["لَوْلَا"] == ""
    ist = {f.name: f.cells for f in FORMS}
    for n in ("مَنْ", "مَا", "مَتَى", "أَيَّانَ", "أَيْنَ", "أَنَّى", "أَيُّ"):
        assert cells_of(n) == ist[n], n
    assert cells_of("لَمَّا") in {cells_of(w) for w in SHART_GHAYR}


def test_masaq_measurement_and_index() -> None:
    import subprocess
    import sys

    rows = json.loads(SLICE.read_text(encoding="utf-8"))
    ok = {"السكون": 0, "حذف النون": 0, "حذف حرف العلة": 0}
    tot = dict.fromkeys(ok, 0)
    for row in rows:
        stem = tuple((c[0], c[1]) for c in row["stem"])
        m = row["marker"]
        tot[m] += 1
        read = marker(stem)
        if m == "حذف حرف العلة":
            ok[m] += read == "لا تقرؤه الخانة"
        elif m == "السكون":
            ok[m] += read == "سكون" or (read == "لا تقرؤه الخانة" and stem[-1][1] != "فتح")
        else:
            ok[m] += read == "حذف النون"
    assert ok["حذف النون"] * 100 >= 95 * tot["حذف النون"]
    assert ok["حذف حرف العلة"] * 100 >= 98 * tot["حذف حرف العلة"]
    assert ok["السكون"] * 100 >= 95 * tot["السكون"]  # السكونُ أو كسرةُ الوصل أو يَكُ
    root = Path(__file__).parent.parent
    res = subprocess.run([sys.executable, str(root / "tools" / "gen_jazm_index.py"), "--check"],
                         capture_output=True, text=True, cwd=root)
    assert res.returncode == 0, res.stderr
