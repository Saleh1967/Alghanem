"""النعتُ الحقيقيّ: المتّجهُ الرباعيّ من الخانة، المطابقةُ في الأربعة، الحملُ واحد، والجملةُ بعد النكرة نعت.

التوقّعاتُ من الحصر المُرسَل (المطابقةُ الرباعيّة؛ الحالُ تشترط صاحبًا معرفة) على الخانات وشواهدِ البوّابة،
والطفرةُ (نعتٌ مخالفٌ إعرابًا أو تعريفًا أو جنسًا أو عددًا؛ حالٌ بعد نكرة) تُرفَض.
"""

from __future__ import annotations

from pathlib import Path

from slge.jumla import dual, jam_m, ta_nith
from slge.majrurat import jarr
from slge.marifa import al
from slge.naat import haml_kind, jumla_mahall, naat, naat_ok, vec
from slge.nawasikh import nasb, raf, tanwin
from slge.rawabit import cells_of
from slge.tawabi import follows

ROOT_DIR = Path(__file__).resolve().parent.parent
STEMS = ("رَجُلُ", "كِتَابُ", "مُسْلِمُ", "طَالِبُ")


def test_four_coordinates_match_for_every_stem() -> None:
    tawil = cells_of("طَوِيلُ")
    for w in STEMS:
        k = cells_of(w)
        for m in (al(k), tanwin(k), tanwin(nasb(k)), al(jarr(k)), tanwin(jarr(k)), al(nasb(k))):
            n = naat(m, tawil)
            assert naat_ok(m, n) and vec(m) == vec(n) and follows(n, m), (w, m)
            assert naat_ok(n, m) and haml_kind(m, n) == "نعت"
        f = ta_nith(k)
        assert naat_ok(tanwin(f), naat(tanwin(f), ta_nith(tawil)))
        assert naat_ok(dual(k), dual(tawil)) and naat_ok(jam_m(k), jam_m(tawil))
    # الطفرة: مخالفةٌ في كلٍّ من الأربعة
    rajul = cells_of("رَجُلُ")
    assert not naat_ok(tanwin(rajul), tanwin(nasb(tawil)))  # الإعراب
    assert not naat_ok(tanwin(rajul), al(tawil))  # التعريف
    assert not naat_ok(tanwin(rajul), tanwin(ta_nith(tawil)))  # الجنس
    assert not naat_ok(dual(rajul), tanwin(tawil))  # العدد
    assert not naat_ok(al(rajul), tanwin(tawil)) and haml_kind(al(rajul), tanwin(tawil)) == "خبر"


def test_clause_after_nakira_is_naat_and_hal_needs_marifa() -> None:
    for w in STEMS:
        k = cells_of(w)
        assert jumla_mahall(tanwin(nasb(k))) == "نعت" and jumla_mahall(tanwin(k)) == "نعت"
        assert jumla_mahall(al(nasb(k))) == "حال" and jumla_mahall(al(k)) == "حال"
        assert jumla_mahall(raf(k)) == "حال"  # مضافٌ: معرفة
    assert jumla_mahall(cells_of("دَرَسَ")) == "—" and jumla_mahall(cells_of("هُوَ")) == "—"


def test_masaq_measurement_and_index() -> None:
    import subprocess
    import sys

    sys.path.insert(0, str(ROOT_DIR / "tools"))
    from gen_naat_index import measure

    m = measure()
    read, case_ok, def_ok = m["read"], m["case"], m["def"]
    assert isinstance(read, dict) and isinstance(case_ok, dict) and isinstance(def_ok, dict)
    assert read[("نعت", True)] > 600 and read[("نعت", True)] > 0.45 * (
        read[("نعت", True)] + read[("نعت", False)])
    assert case_ok["وافق"] > 8 * case_ok["خالف"] and def_ok["وافق"] > 10 * def_ok["خالف"]
    gen = str(ROOT_DIR / "tools" / "gen_naat_index.py")
    res = subprocess.run([sys.executable, gen, "--check"], capture_output=True, text=True,
                         cwd=ROOT_DIR)
    assert res.returncode == 0, res.stderr
