"""همزتا الوصل والقطع: الحدُّ مبرهَن، والحصرُ تقسيمُ قوالب، والقياسُ على MASAQ بشهادات البوّابة."""

from __future__ import annotations

import json
from pathlib import Path

from slge.cells import STATES, licensed
from slge.rawabit import cells_of
from slge.wasl import (
    QAT_TEMPLATES,
    TEN,
    WASL_TEMPLATES,
    drop_wasl,
    istifham_verb,
    kind,
    starts_hamza,
)
from slge.wazn import AWZAN

_A, _I, _U, SUKUN = STATES
SLICE = Path(__file__).parent / "data" / "masaq-hamza.json"
_ST = dict(zip("0123", STATES, strict=True))


def test_boundary_laws() -> None:
    intalaqa, akrama = cells_of("اِنْطَلَقَ"), cells_of("أَكْرَمَ")
    assert licensed(intalaqa) and not licensed(drop_wasl(intalaqa))  # لا ابتداءَ بساكن
    assert licensed(cells_of("وَ") + drop_wasl(intalaqa))  # الوصلُ يسقط
    assert not licensed(cells_of("مِنْ") + drop_wasl(intalaqa))  # بعد ساكن: التقاءُ الساكنين
    assert licensed(cells_of("وَ") + akrama) and licensed(cells_of("مِنْ") + akrama)  # القطعُ يبقى
    ikram = cells_of("إِكْرَامُ")
    assert intalaqa[0] == ikram[0] and intalaqa[1][1] == ikram[1][1] == SUKUN  # خانةٌ واحدة
    assert istifham_verb(cells_of("اِسْتَخْرَجْتَ")) == cells_of("أَسْتَخْرَجْتَ")
    assert cells_of("بِ") + cells_of("سْمِ") == cells_of("بِسْمِ")


def test_templates_partition_and_reader() -> None:
    hamza = [k for k in range(len(AWZAN)) if starts_hamza(k)]
    assert hamza == sorted(WASL_TEMPLATES + QAT_TEMPLATES) and len(hamza) == 24
    assert not set(WASL_TEMPLATES) & set(QAT_TEMPLATES)
    for w, k in (("اِقْرَأْ", "وصل"), ("اِنْطَلَقَ", "وصل"), ("اِسْتَخْرَجَ", "وصل"), ("اِنْطِلَاقُ", "وصل"),
                 ("أَكْرَمَ", "قطع"), ("إِكْرَامُ", "قطع"), ("أَبْنَاءُ", "قطع"), ("أَسْمَاءُ", "قطع"),
                 ("أَخَذَ", "قطع أصلي"), ("أَرْضُ", "قطع أصلي"), ("إِلَّا", "لا يُقرأ"), ("اِسْمُ", "وصل"),
                 ("اِبْنَ", "وصل")):
        assert kind(cells_of(w)) == k, w
    assert kind(cells_of("اِنْطِلَاقُ")) != kind(cells_of("إِكْرَامُ"))
    assert len(TEN) == 10 and all(cells_of(w)[1][1] == SUKUN for w in TEN)


def test_masaq_measurement_and_index() -> None:
    import subprocess
    import sys

    rows = json.loads(SLICE.read_text(encoding="utf-8"))
    read = agree = 0
    silent_after_prefix = total_prefix_wasl = 0
    for r in rows:
        if r["k"].startswith("وصل ساقط"):
            silent_after_prefix += 1
        if r["k"] in ("وصل", "قطع") and r["s"]:
            stem = tuple((r["s"][i], _ST[r["s"][i + 1]]) for i in range(0, len(r["s"]), 2))
            k = kind(stem)
            if k != "لا يُقرأ":
                read += 1
                agree += ((r["k"] == "وصل" and k == "وصل")
                          or (r["k"] == "قطع" and k.startswith("قطع")))
        if r["p"] and r["k"] == "وصل":
            total_prefix_wasl += 1
    assert agree * 100 >= 97 * read and read > 3000
    assert total_prefix_wasl == 0 and silent_after_prefix > 900  # بعد السابقة لا وصلَ قائمًا
    root = Path(__file__).parent.parent
    res = subprocess.run([sys.executable, str(root / "tools" / "gen_wasl_index.py"), "--check"],
                         capture_output=True, text=True, cwd=root)
    assert res.returncode == 0, res.stderr
