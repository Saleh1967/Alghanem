"""بقيّةُ المنصوبات: الحالُ والتمييزُ عمليّةٌ واحدة، والاستثناءُ ثلاثُ عمليّات، والقياسُ على MASAQ."""

from __future__ import annotations

import json
from pathlib import Path

from slge.cells import STATES, licensed
from slge.mansubat import (
    TOOLS,
    after_khala,
    derived,
    ghayr_of,
    hal,
    mustathna,
    nasb,
    raf,
    tahwil,
    tamyiz,
)
from slge.nida import has_tanwin
from slge.rawabit import cells_of
from slge.tawabi import case_class, follows

_A, _I, _U, SUKUN = STATES
SLICE = Path(__file__).parent / "data" / "masaq-mansubat.json"


def test_hal_and_tamyiz_one_operation() -> None:
    assert hal is tamyiz
    for w in ("سُجَّدُ", "شَيْبُ", "عُيُونُ", "كَوْكَبُ"):
        x = hal(cells_of(w))
        assert case_class(x) == "نصب" and has_tanwin(x) and licensed(x), w
    assert hal(cells_of("شَيْبُ")) == cells_of("شَيْبًا")
    assert derived(cells_of("ضَاحِكُ")) and derived(cells_of("مُفْسِدُ")) and not derived(cells_of("نَفْسُ"))
    ras, shayb = cells_of("رَأْسُ"), cells_of("شَيْبُ")
    assert tahwil(shayb, ras) == (cells_of("اَرَّأْسُ"), cells_of("شَيْبًا"))
    sukara = cells_of("سُكَارَى")
    assert not has_tanwin(sukara) and case_class(sukara).startswith("لا تقرؤه")


def test_istithna_three_operations() -> None:
    talib = cells_of("طَالِبُ")
    assert mustathna("تامّ مثبت", raf, False, talib) == cells_of("طَالِبًا")
    assert mustathna("تامّ منفي", raf, False, talib) == cells_of("طَالِبًا")
    assert mustathna("تامّ منفي", raf, True, talib) == raf(talib)
    assert follows(mustathna("تامّ منفي", raf, True, talib), raf(cells_of("طُلَّابُ")))
    assert mustathna("ناقص منفي", raf, False, talib) == raf(talib)
    assert mustathna("ناقص منفي", nasb, False, talib) == nasb(talib)
    for w in TOOLS:
        assert licensed(cells_of(w)), w
    assert ghayr_of(raf, cells_of("رَجُلُ")) == cells_of("غَيْرُ") + cells_of("رَجُلِ")
    assert case_class(ghayr_of(raf, cells_of("رَجُلُ"))) == "جرّ"  # الحكمُ في غَيْر لا في آخر التركيب
    assert after_khala(True, talib) == cells_of("طَالِبَ")
    assert after_khala(False, talib) == cells_of("طَالِبِ")


def test_masaq_measurement_and_index() -> None:
    import subprocess
    import sys

    data = json.loads(SLICE.read_text(encoding="utf-8"))
    ok = {"حال": 0, "تمييز": 0, "مستثنى": 0}
    tot = dict.fromkeys(ok, 0)
    nak = {"حال": 0, "تمييز": 0}
    for row in data["cells"]:
        if row["declinable"] != "معرب":
            continue
        stem = tuple((c[0], c[1]) for c in row["stem"])
        role = row["role"]
        tot[role] += 1
        cc = case_class(stem)
        ok[role] += cc in ("نصب", "نصب/جرّ")
        if role in nak and not row["det"]:
            nak[role] += 1
    assert ok["حال"] * 100 >= 90 * tot["حال"] and ok["مستثنى"] * 100 >= 90 * tot["مستثنى"]
    assert ok["تمييز"] * 100 >= 70 * tot["تمييز"]  # الباقي تمييزُ كم الخبريّة مجرور
    assert nak["تمييز"] * 100 >= 95 * tot["تمييز"] and nak["حال"] * 100 >= 95 * tot["حال"]
    neg = {True: {"مستثنى": 0, "other": 0}, False: {"مستثنى": 0, "other": 0}}
    for i in data["illa"]:
        nxt = i["next"][2] if i["next"] else ""
        neg[bool(i["neg"])]["مستثنى" if nxt == "مستثنى" else "other"] += 1
    assert neg[False]["مستثنى"] > neg[True]["مستثنى"]
    assert neg[True]["other"] > 5 * neg[True]["مستثنى"]
    root = Path(__file__).parent.parent
    res = subprocess.run([sys.executable, str(root / "tools" / "gen_mansubat_index.py"), "--check"],
                         capture_output=True, text=True, cwd=root)
    assert res.returncode == 0, res.stderr
