"""الأدواتُ علاقاتٍ تشغيليّة: البنيةُ على الجدول الموحَّد، والعملُ دالّةً مرخَّصة، والتركيبُ بعينه، والترتيبُ لا
يُسقط قراءةً، والرقمُ قبلُ وبعدُ على MASAQ.

التوقّعاتُ من كتب النحو (الجارُّ يكسر، إنّ تنصب، لم تجزم، إنّما مكفوفة، كأنّ = ك + أنّ) ومن قسمة MASAQ
المحجوبة؛ والطفرةُ (أداةٌ تعمل في غير صنفها؛ ترتيبٌ يُسقط؛ صورةٌ ليست أداة؛ جزمٌ بعد مدّ) تُرفَض.
"""

from __future__ import annotations

from pathlib import Path

from slge.adawat import DECLARED, FIL, ISM, TABLE_ADAWAT, apply, cat_of, fits, of_cells, rank
from slge.cells import SUKUN, licensed
from slge.huruf import TABLE
from slge.jidh import jidh
from slge.rawabit import PARTICLES, cells_of

ROOT_DIR = Path(__file__).resolve().parent.parent


def _tool(text: str):  # type: ignore[no-untyped-def]
    a = of_cells(cells_of(text))
    assert a is not None, text
    return a


def test_every_harf_has_arity_args_and_declared_relation() -> None:
    assert len(TABLE_ADAWAT) == len(TABLE) == len(DECLARED) == 68
    for a in TABLE_ADAWAT:
        assert len(a.args) == a.arity >= 1 and a.rel
        if a.harf.amal in ("جرّ", "نصب الاسم", "نداء", "معيّة"):
            assert a.args[0] == ISM, a.harf.name
        if a.harf.amal in ("نصب الفعل", "جزم", "جزم فعلين"):
            assert a.args[0] == FIL, a.harf.name
        if a.harf.amal == "تبعيّة" or a.rel == "شرط":
            assert a.arity == 2, a.harf.name
    rels = {a.rel for a in TABLE_ADAWAT}
    assert rels >= {"تعدية", "توكيد", "نفي", "شرط", "جمع", "تخيير", "استفهام"}
    assert _tool("إِنَّ").rel == "توكيد" and _tool("ثُمَّ").rel == "ترتيب وتراخٍ"
    # الطفرة: صورةٌ ليست أداة
    assert of_cells(cells_of("كِتَابٌ")) is None and of_cells(()) is None


def test_amal_is_a_licensed_function_on_the_last_cell() -> None:
    kitabu, yaktubu = cells_of("كِتَابُ"), cells_of("يَكْتُبُ")
    assert apply(_tool("فِي"), kitabu) == cells_of("كِتَابِ")
    assert apply(_tool("إِنَّ"), kitabu) == cells_of("كِتَابَ")
    assert apply(_tool("لَنْ"), yaktubu) == cells_of("يَكْتُبَ")
    assert apply(_tool("لَمْ"), yaktubu) == cells_of("يَكْتُبْ")
    assert apply(_tool("هَلْ"), kitabu) == kitabu  # لا عمل
    for a in TABLE_ADAWAT:
        for w in (kitabu, yaktubu):
            out = apply(a, w)
            assert out[:-1] == w[:-1], a.harf.name  # يعمل في الآخر وحدَه
            if w is yaktubu or a.harf.amal not in ("جزم", "جزم فعلين"):
                assert licensed(out), a.harf.name  # `apply_licensed`؛ والجزمُ بعد مدٍّ شأنُ Jazm
    # الطفرة: الجزمُ بعد مدٍّ غيرُ مرخَّص — حذفُ العين ملزَم (شأنُ Jazm لا هذه البنية)
    assert not licensed(apply(_tool("لَمْ"), cells_of("يَقُولُ")))
    assert apply(_tool("لَمْ"), cells_of("يَقُولُ"))[-1][1] == SUKUN


def test_compositions_and_kaff_are_exact() -> None:
    by = {p.name: p for p in PARTICLES}
    assert _tool("كَأَنَّ").harf.cells == _tool("كَ").harf.cells + _tool("أَنَّ").harf.cells
    assert _tool("أَلَا").harf.cells == _tool("أَ").harf.cells + _tool("لَا").harf.cells
    assert by["لِكَيْ"].cells == _tool("لِ").harf.cells + _tool("كَيْ").harf.cells
    assert by["لِكَيْ"].amal == by["كَيْلَا"].amal == "نصب"
    assert by["إِنَّمَا"].cells == _tool("إِنَّ").harf.cells + _tool("مَا").harf.cells
    assert by["إِنَّمَا"].amal == ""  # الكفّ
    # الطفرة: مركّبٌ بغير جزأيه
    assert _tool("كَأَنَّ").harf.cells != _tool("كَ").harf.cells + _tool("إِنَّ").harf.cells


def test_rank_puts_the_fitting_category_first_and_drops_nothing() -> None:
    inna, lam = _tool("إِنَّ"), _tool("لَمْ")
    rs = jidh(cells_of("فَرِيقٌ"))
    assert [cat_of(r) for r in rs] == [ISM, ISM]
    assert rank(inna, rs) == rs and [fits(lam, r) for r in rank(lam, rs)] == [False, False]
    assert len(rank(lam, rs)) == len(rs) and set(rank(lam, rs)) == set(rs)
    wajada = jidh(cells_of("وَجَدَ"))
    assert [cat_of(r) for r in wajada] == [FIL]
    assert fits(lam, wajada[0]) and not fits(inna, wajada[0])
    assert fits(_tool("ثُمَّ"), wajada[0]) and fits(_tool("هَلْ"), rs[0])  # أيٌّ/جملة: الكلُّ يوافق
    mixed = (*rs, *wajada)
    out = rank(lam, mixed)
    assert [cat_of(r) for r in out] == [FIL, ISM, ISM] and set(out) == set(mixed)
    out = rank(inna, mixed)
    assert [cat_of(r) for r in out] == [ISM, ISM, FIL]
    # الطفرة: الترتيبُ لا يُسقط ولا يزيد
    assert rank(inna, ()) == () and len(rank(inna, mixed * 2)) == 6


def test_numbers_before_and_after_on_masaq() -> None:
    import subprocess
    import sys

    sys.path.insert(0, str(ROOT_DIR / "tools"))
    from gen_adawat_index import measure

    m = measure()
    assert m["rows"] == 40731 and m["with_next"] == 29866 and m["table"] == 68
    jarr = m["amal"]["جرّ"]
    assert jarr["موافق"] == 3701 and jarr["موافق"] > 9 * jarr["مخالف"]
    assert m["amal"]["نصب الفعل"]["مخالف"] == 0 and m["amal"]["جزم"]["مخالف"] == 0
    assert m["attached"]["موافق"] == 3093
    b, a = m["before"], m["after"]
    assert sum(b.values()) == sum(a.values()) == 595  # لا كلمةَ تسقط (كانت 593 قبل زوائد سيبويه)
    assert b["موافق"] == 298 and a["موافق"] == 572  # 50.1% ← 96.1% (كان 296 قبل زوائد سيبويه)
    assert m["tool_forms"] == 50
    gen = str(ROOT_DIR / "tools" / "gen_adawat_index.py")
    res = subprocess.run([sys.executable, gen, "--check"], capture_output=True, text=True,
                         cwd=ROOT_DIR)
    assert res.returncode == 0, res.stderr
