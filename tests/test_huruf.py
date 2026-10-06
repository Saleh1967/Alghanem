"""الحروفُ والأدوات: جدولٌ واحد، الخانةُ الواحدةُ في أبواب، والعملُ عمليّاتٌ في أبوابها، والقياس."""

from __future__ import annotations

import json
from pathlib import Path

from slge.afal import STEMS, form
from slge.cells import licensed
from slge.huruf import FIL, ISM, MUSHTARAK, TABLE, by_cells, shared
from slge.majrurat import jarr
from slge.nawasikh import AMAL
from slge.nida import has_tanwin
from slge.rawabit import PARTICLES, cells_of, govern

SLICE = Path(__file__).parent / "data" / "masaq-huruf.json"


def test_table_deposited_and_licensed() -> None:
    assert (len(ISM), len(FIL), len(MUSHTARAK), len(TABLE)) == (31, 18, 19, 68)
    assert all(licensed(x.cells) for x in TABLE) and len({x.cells for x in TABLE}) == 53
    looks = sorted({x.name for x in TABLE if has_tanwin(x.cells)})
    assert looks == sorted({"مِنْ", "عَنْ", "أَنْ", "لَنْ", "إِذَنْ", "إِنْ", "لَكِنْ", "إِنْ (النفي)"})
    rajul = cells_of("رَجُلُ")
    for x in TABLE:
        if len(x.cells) == 1:
            assert licensed(x.cells + rajul), x.name


def test_shared_cells_named() -> None:
    sh = shared()
    assert len(by_cells(cells_of("لَا"))) == 4 and len(by_cells(cells_of("وَ"))) == 4
    assert len(by_cells(cells_of("حَتَّى"))) == 3 and len(by_cells(cells_of("لِ"))) == 3
    assert len(by_cells(cells_of("إِنْ"))) == 2 and len(by_cells(cells_of("فَ"))) == 2
    assert {x.amal for x in by_cells(cells_of("حَتَّى"))} == {"جرّ", "نصب الفعل", "تبعيّة"}
    assert sum(len(v) for v in sh.values()) - len(sh) == 68 - 53


def test_amal_is_operation() -> None:
    rajul = cells_of("رَجُلُ")
    assert govern("جرّ", jarr(rajul)) and AMAL["إنّ"] == ("نصب", "رفع")
    for s in STEMS:
        assert govern("نصب", form(s, "الجماعة", "نصب")) and govern("جزم", form(s, "الجماعة", "جزم"))
    amal = {p.name: p.amal for p in PARTICLES}
    assert amal["لَنْ"] == "نصب" and amal["كَيْ"] == "نصب" and amal["لَمْ"] == "جزم"
    assert amal["سَ"] == "" and amal["سَوْفَ"] == "" and amal["قَدْ"] == "" and amal["كَلَّا"] == ""
    assert cells_of("سَ") + cells_of("يَقُولُ") == cells_of("سَيَقُولُ")


def test_masaq_measurement_and_index() -> None:
    import subprocess
    import sys

    data = json.loads(SLICE.read_text(encoding="utf-8"))
    after: dict[tuple[str, str], int] = {(s, a): v for s, a, v in data["after"]}
    lan = sum(v for (s, a), v in after.items() if s == "لن")
    assert after[("لن", "فعل مضارع منصوب")] * 100 >= 95 * lan
    assert after[("أن", "فعل مضارع منصوب")] > 10 * after.get(("أن", "فعل مضارع مرفوع"), 0)
    assert after[("حتى", "فعل مضارع منصوب")] > 50 and after.get(("حتى", "اسم مجرور"), 0) > 0
    roles: dict[str, set[str]] = {}
    for s, r, _ in data["roles"]:
        roles.setdefault(s, set()).add(r)
    assert {"حرف جزم", "لا النافية للجنس"} <= roles["لا"] and "حرف شرط" in roles["إن"]
    root = Path(__file__).parent.parent
    res = subprocess.run([sys.executable, str(root / "tools" / "gen_huruf_index.py"), "--check"],
                         capture_output=True, text=True, cwd=root)
    assert res.returncode == 0, res.stderr
