"""الاسم: المجرّدُ عشرة، التصغيرُ والنسبُ عمليّات، البناءُ العارضُ حالةٌ ثابتة، والقياسُ على MASAQ."""

from __future__ import annotations

import gzip
import json
from pathlib import Path

from slge.adad import compound
from slge.cells import STATES, licensed
from slge.ism import (
    DROPPED,
    KHUMASI,
    RUBAI,
    TEN,
    TWELVE,
    is_nisba,
    is_tasghir,
    nisba,
    prepare,
    read_thulathi,
    saghir3,
    saghir4,
    saghir5,
    shape,
)
from slge.nawasikh import nasb
from slge.nida import hukm, is_bina
from slge.rawabit import cells_of
from slge.zuruf import hukm as zhukm
from slge.zuruf import qat

_A, _I, _U, SUKUN = STATES
SLICE = Path(__file__).parent / "data" / "masaq-ism.json.gz"
_ST = dict(zip("0123", STATES, strict=True))


def test_thulathi_ten_and_shapes() -> None:
    assert len(TWELVE) == 12 and len(TEN) == 10 and set(DROPPED) == {(_U, _U), (_I, _U)}
    for f, a in TWELVE:
        cw = (("ش", f), ("م", a), ("س", _U))
        assert licensed(cw) and read_thulathi(cw) == (f, a)
    for w, p in (("شَمْسُ", (_A, SUKUN)), ("قَمَرُ", (_A, _A)), ("كَتِفُ", (_A, _I)), ("عَضُدُ", (_A, _U)),
                 ("قُفْلُ", (_U, SUKUN)), ("صُرَدُ", (_U, _A)), ("دُئِلُ", (_U, _I)), ("حِمْلُ", (_I, SUKUN)),
                 ("عِنَبُ", (_I, _A)), ("إِبِلُ", (_I, _I)), ("رَجُلُ", (_A, _U))):
        assert read_thulathi(cells_of(w)) == p and p in TEN, w
    shapes = [shape(cells_of(w)) for w in RUBAI]
    assert len(set(shapes)) == 5 and shapes[0] == shapes[5]  # جَعْفَر وطَحْلَب شكلٌ واحد
    assert len({shape(cells_of(w)) for w in KHUMASI}) == 4


def test_tasghir_and_nisba_operations() -> None:
    assert saghir3("ر", "ج", "ل", _U) == cells_of("رُجَيْلُ")
    assert saghir4("د", "ر", "ه", "م", _U) == cells_of("دُرَيْهِمُ")
    assert saghir5("ع", "ص", "ف", "ر", _U) == cells_of("عُصَيْفِيرُ")
    for w in (saghir3("ر", "ج", "ل", _U), saghir4("د", "ر", "ه", "م", _U), cells_of("بُنَيَّ")):
        assert licensed(w) and is_tasghir(w)
    cases = (("بلا", "مِصْرُ", "مِصْرِيُّ"), ("حذف التاء", "مَكَّةُ", "مَكِّيُّ"), ("مقصور ثالث", "عَصَا", "عَصَوِيُّ"),
             ("مقصور رابع", "مُصْطَفَى", "مُصْطَفِيُّ"), ("منقوص ثالث", "عَمِي", "عَمَوِيُّ"),
             ("منقوص رابع", "قَاضِي", "قَاضِيُّ"))
    for kind, src, dst in cases:
        out = nisba(prepare(kind, cells_of(src)), _U)
        assert out == cells_of(dst) and licensed(out) and is_nisba(out), src
    assert is_nisba(cells_of("عَرَبِيٌّ")[:-1])


def test_arid_bina_in_its_babs() -> None:
    rajul = cells_of("رَجُلُ")
    assert is_bina(hukm(rajul))  # المنادى مضمومًا
    assert nasb(rajul)[-1][1] == _A and zhukm(qat(rajul)).startswith("مقطوع")
    assert compound(rajul, True)[2][1] == _A


def test_masaq_measurement_and_index() -> None:
    import subprocess
    import sys

    with gzip.open(SLICE, "rt", encoding="utf-8") as f:
        rows = json.load(f)
    thul: dict[tuple[str, str], int] = {}
    for r in rows:
        s = tuple((r["s"][i], _ST[r["s"][i + 1]]) for i in range(0, len(r["s"]), 2))
        if s and s[-1] == ("ن", SUKUN) and len(s) >= 2 and s[-2][1] != SUKUN:
            s = s[:-1]
        madd = any(c[0] in "اوي" and c[1] == SUKUN for c in s[:-1])
        if len(s) == 3 and not madd and s[0][1] != SUKUN:
            p = read_thulathi(s)
            assert p is not None
            thul[p] = thul.get(p, 0) + 1
    ten = sum(v for p, v in thul.items() if p in TEN)
    assert ten > 4000 and thul.get((_I, _U), 0) == 0  # فِعُل معدومة
    assert thul.get((_U, _U), 0) < ten // 20  # فُعُل جمعٌ لا مفرد
    root = Path(__file__).parent.parent
    res = subprocess.run([sys.executable, str(root / "tools" / "gen_ism_index.py"), "--check"],
                         capture_output=True, text=True, cwd=root)
    assert res.returncode == 0, res.stderr
