"""النواسخ: أربعةُ أبوابٍ عمليّتان — الترخيص، القراءة، الكفّ، والقياسُ على MASAQ."""

from __future__ import annotations

import json
from pathlib import Path

from slge.cells import STATES, licensed
from slge.marifa import al, has_al
from slge.nawasikh import AMAL, INNA, KADA, KANA, LA, ZANNA, kaffa, nasb, raf, tanwin
from slge.nida import has_tanwin
from slge.rawabit import PARTICLES, cells_of
from slge.tawabi import case_class, compatible

_A, _I, _U, SUKUN = STATES
SLICE = Path(__file__).parent / "data" / "masaq-nawasikh.json"


def test_two_operations_four_babs() -> None:
    assert AMAL["إنّ"] == tuple(reversed(AMAL["كان"])) and AMAL["كاد"] == AMAL["كان"]
    assert AMAL["ظنّ"] == ("نصب", "نصب") and AMAL["لا النافية للجنس"] == AMAL["إنّ"]
    ghafur = cells_of("غَفُورُ")
    assert tanwin(nasb(ghafur)) == cells_of("غَفُورًا") and tanwin(raf(ghafur)) == cells_of("غَفُورٌ")
    assert case_class(tanwin(nasb(ghafur))) == "نصب" and case_class(tanwin(raf(ghafur))) == "رفع"
    assert case_class(al(raf(ghafur))) == "رفع" and case_class(nasb(ghafur)) == "نصب"
    assert licensed(raf(ghafur)) and licensed(nasb(ghafur))
    # الحركةُ وحدَها لا تنوينَ معها
    assert not has_tanwin(raf(cells_of("رَجُلٌ"))) and not has_tanwin(nasb(cells_of("رَجُلٌ")))


def test_la_jins_ism_is_bare_nakira() -> None:
    rayb = nasb(cells_of("رَيْبُ"))
    assert rayb == cells_of("رَيْبَ") and not has_tanwin(rayb) and not has_al(rayb)
    assert case_class(rayb) == "نصب"


def test_deposits_licensed_and_kaffa() -> None:
    for w in KANA + KADA + INNA + ZANNA + (LA,):
        assert licensed(cells_of(w)), w
    assert len(KANA) == 13 and len(KADA) == 12 and len(INNA) == 6 and len(ZANNA) == 15
    assert "جَعَلَ" in KADA and "جَعَلَ" in ZANNA
    for w in INNA:
        assert kaffa(cells_of(w)) == cells_of(w + "مَا") and licensed(kaffa(cells_of(w)))
    amal = {p.name: p.amal for p in PARTICLES}
    assert amal["إِنَّ"] == "نصب الاسم ورفع الخبر" and amal["إِنَّمَا"] == ""
    # دَينٌ سُدِّد: الستُّ كلُّها في جدول أدوات الربط، وأَنْ الناصبةُ معها (`inna_in_rawabit`، `an_in_rawabit`)
    assert all(amal[w] == "نصب الاسم ورفع الخبر" for w in INNA) and amal["أَنْ"] == "نصب"


def test_masaq_measurement_and_index() -> None:
    import subprocess
    import sys

    data = json.loads(SLICE.read_text(encoding="utf-8"))
    expect = {"اسم فعل ناسخ": "رفع", "خبر فعل ناسخ": "نصب", "اسم حرف ناسخ": "نصب",
              "خبر حرف ناسخ": "رفع", "اسم لا النافية للجنس": "نصب"}
    ok = {k: 0 for k in expect}
    tot = {k: 0 for k in expect}
    for row in data["cells"]:
        role = row["role"]
        if row["declinable"] != "معرب" and not role.startswith("اسم لا"):
            continue
        if role.startswith("خبر") and "ب" in row["prefixes"]:
            continue
        cc = case_class(tuple((c[0], c[1]) for c in row["stem"]))
        if cc.startswith("لا تقرؤه"):
            continue
        tot[role] += 1
        ok[role] += compatible(cc, expect[role])
    assert ok["خبر فعل ناسخ"] * 100 >= 95 * tot["خبر فعل ناسخ"]
    assert ok["خبر حرف ناسخ"] * 100 >= 95 * tot["خبر حرف ناسخ"]
    assert ok["اسم فعل ناسخ"] * 100 >= 90 * tot["اسم فعل ناسخ"]
    assert ok["اسم حرف ناسخ"] * 100 >= 85 * tot["اسم حرف ناسخ"]
    assert ok["اسم لا النافية للجنس"] == tot["اسم لا النافية للجنس"] > 60
    # عسى بأَنْ غالبًا، وكاد وطفق بلا أَنْ
    an = {"كاد": [0, 0], "عسى": [0, 0], "طفق": [0, 0]}
    for k in data["kada"]:
        verb = {"كد": "كاد", "عسي": "عسى"}.get(k["verb"], k["verb"])
        an[verb][any(n[0] == "أن" for n in k["next"])] += 1
    assert an["كاد"][1] == 0 and an["طفق"][1] == 0 and an["عسى"][1] > 5 * an["عسى"][0]
    # إنّما لا اسمَ حرفٍ ناسخ بعدها
    assert all(i["next"][0][2] != "اسم حرف ناسخ" for i in data["innama"] if i["next"])
    root = Path(__file__).parent.parent
    res = subprocess.run([sys.executable, str(root / "tools" / "gen_nawasikh_index.py"), "--check"],
                         capture_output=True, text=True, cwd=root)
    assert res.returncode == 0, res.stderr
