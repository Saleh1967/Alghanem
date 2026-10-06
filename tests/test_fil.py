"""الفعل: الأبوابُ أزواج، الزيادةُ طول، الإعلالُ والإبدالُ عمليّات، والقياسُ على MASAQ."""

from __future__ import annotations

import gzip
import json
from pathlib import Path

from slge.cells import STATES, licensed
from slge.fil import (
    ABWAB,
    MAZID,
    MAZID_AMR,
    MAZID_PRES,
    MISSING,
    added,
    amr_of,
    halqi,
    ibdal,
    idgham,
    iftaal,
    naql,
    qalb,
    read_bab,
    read_doubled,
    read_hollow,
)
from slge.jazm import sukun
from slge.rawabit import cells_of
from slge.wasl import QAT_TEMPLATES, WASL_TEMPLATES
from slge.wazn import AWZAN, fill, mizan

_A, _I, _U, SUKUN = STATES
SLICE = Path(__file__).parent / "data" / "masaq-fil.json.gz"
_ST = dict(zip("0123", STATES, strict=True))


def test_abwab_six_of_nine() -> None:
    nine = {(p, q) for p in (_A, _I, _U) for q in (_A, _I, _U)}
    assert set(ABWAB) | set(MISSING) == nine and not set(ABWAB) & set(MISSING)
    for p, q in ABWAB:
        past = (("ن", _A), ("ص", p), ("ر", _A))
        pres = (("ي", _A), ("ن", SUKUN), ("ص", q), ("ر", _U))
        assert licensed(past) and licensed(pres) and read_bab(past, pres) == (p, q)
    assert read_bab(cells_of("ضَرَبَ"), cells_of("يَضْرِبُ")) == (_A, _I)
    assert read_bab(cells_of("فَتَحَ"), cells_of("يَفْتَحُ")) == (_A, _A) and halqi("ح") and not halqi("ب")
    assert read_bab(cells_of("فَرِحَ"), cells_of("يَفْرَحُ")) == (_I, _A)


def test_mazid_and_rubai() -> None:
    assert [added(k) for k in MAZID] == [1, 1, 1, 2, 2, 2, 2, 2, 3]
    assert [added(k) for k in (0, 1, 2)] == [0, 0, 0]
    assert fill(AWZAN[11].template, ("خ", "ر", "ج")) == cells_of("أَخْرَجَ")
    assert fill(AWZAN[19].template, ("غ", "ف", "ر")) == cells_of("اِسْتَغْفَرَ")
    for w in ("دَحْرَجَ", "زَلْزَلَ", "تَدَحْرَجَ", "اِطْمَأَنَّ"):
        assert licensed(cells_of(w)), w


def test_ilal_and_ibdal_operations() -> None:
    assert qalb(cells_of("قَوَلَ")) == cells_of("قَالَ") and licensed(qalb(cells_of("قَوَلَ")))
    assert (("ي", _A), *naql(cells_of("قْوُلُ"))) == cells_of("يَقُولُ")
    assert not licensed(sukun(cells_of("يَقُولُ"))) and licensed(cells_of("يَقُلْ"))  # الحذفُ ملزَم
    assert ibdal(iftaal(("ص", "ب", "ر"))) == cells_of("اِصْطَبَرَ")
    assert ibdal(iftaal(("ز", "ه", "ر"))) == cells_of("اِزْدَهَرَ")
    assert ibdal(iftaal(("و", "ص", "ل"))) == cells_of("اِتْتَصَلَ")
    for root in (("ص", "ب", "ر"), ("ز", "ه", "ر"), ("و", "ص", "ل"), ("ك", "س", "ب")):
        assert licensed(ibdal(iftaal(root))) == licensed(iftaal(root))
    assert ibdal(cells_of("اِصْتَفَى")) == cells_of("اِصْطَفَى")
    assert ibdal(iftaal(("ء", "خ", "ذ"))) == cells_of("اِتْتَخَذَ")  # الهمزةُ فاءً: دَينٌ سُدِّد


def test_mazid_imperative_and_post_template_readers() -> None:
    """أمرُ المزيد من مضارعه بقاعدة أمر المجرّد؛ وأَفْعِلْ يفرّقه القطعُ؛ والأجوفُ والمضعَّف يُقرآن بعد
    القالب."""

    for p, a in zip(MAZID_PRES, MAZID_AMR, strict=True):
        assert amr_of(AWZAN[p].template) == AWZAN[a].template and AWZAN[a].bab == "أمر مزيد"
        assert licensed(mizan(AWZAN[a].template))
    assert amr_of(AWZAN[20].template) == AWZAN[9].template and AWZAN[113].name == "أَفْعِلْ"
    assert 113 in QAT_TEMPLATES and all(k in WASL_TEMPLATES for k in (118, 119, 120))
    assert not licensed(mizan(amr_of(AWZAN[27].template)))  # اِفْعَلْلْ: ساكنان
    assert fill(AWZAN[120].template, ("غ", "ف", "ر")) == cells_of("اِسْتَغْفِرْ")
    assert fill(AWZAN[113].template, ("ك", "ر", "م")) == cells_of("أَكْرِمْ")
    assert idgham(cells_of("رَدَدَ")) == cells_of("رَدْدَ") and licensed(idgham(cells_of("مَدَدَ")))
    assert read_doubled(cells_of("رَدْدَ")) == ("ر", "د", "د")
    assert read_doubled(cells_of("كَتَبَ")) is None
    assert read_hollow(cells_of("قَالَ")) == ("ق", "ل") and read_hollow(cells_of("جَاءَ")) == ("ج", "ء")
    for root in (("ق", "و", "ل"), ("ب", "ي", "ع")):
        assert qalb(fill(AWZAN[0].template, root)) == ((root[0], _A), ("ا", SUKUN), (root[2], _A))


def test_masaq_measurement_and_index() -> None:
    import subprocess
    import sys

    with gzip.open(SLICE, "rt", encoding="utf-8") as f:
        rows = json.load(f)
    past = {_A: 0, _I: 0, _U: 0}
    pres = {_A: 0, _I: 0, _U: 0}
    for r in rows:
        s = tuple((r["s"][i], _ST[r["s"][i + 1]]) for i in range(0, len(r["s"]), 2))
        madd = any(c[0] in "اوي" and c[1] == SUKUN for c in s)
        if r["g"] == "PV" and len(s) == 3 and s[-1][1] == _A and not madd and s[1][1] in past:
            past[s[1][1]] += 1
        if r["g"] == "IV" and len(s) == 3 and s[0][1] == SUKUN and not madd and s[1][1] in pres:
            pres[s[1][1]] += 1
    assert sum(past.values()) > 500 and sum(pres.values()) > 2500
    assert past[_A] > past[_I] > past[_U] > 0  # الحركاتُ الثلاث حاضرة، والفتحُ الأغلب
    assert all(v > 500 for v in pres.values())
    root = Path(__file__).parent.parent
    res = subprocess.run([sys.executable, str(root / "tools" / "gen_fil_index.py"), "--check"],
                         capture_output=True, text=True, cwd=root)
    assert res.returncode == 0, res.stderr
