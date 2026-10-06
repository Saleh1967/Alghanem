"""شبهُ الجملة: صورتان، زائدٌ يُردّ، حظرٌ بالجدول، مرتكزٌ ومحلٌّ من الخانة، والقياسُ على MASAQ.

التوقّعاتُ من الحصر المُرسَل (الصورتان، الزائد، قانونُ الحظر، مرتكزاتٌ ثلاثة، مصفوفةُ المحلّ الرباعيّة)
وشواهدِ البوّابة؛ والطفرةُ (كلمةٌ خارج الجداول، جرٌّ يمسّ المحلّ) تُرفَض.
"""

from __future__ import annotations

from pathlib import Path

from slge.cells import licensed
from slge.marifa import MAWSUL, al
from slge.nawasikh import nasb, raf
from slge.rawabit import cells_of
from slge.shibh import anchor, jarr_majrur, kawn, kind, mahall, zaid_restores, zarf
from slge.tawabi import case_class
from slge.zuruf import STEMS

SLICE = Path(__file__).parent / "data" / "masaq-shibh.json.gz"


def test_two_forms_and_the_table_is_exhaustive() -> None:
    fi, dar = cells_of("فِي"), cells_of("اَدَّارُ")
    assert kind(jarr_majrur(fi, dar)) == "جار ومجرور" and licensed(jarr_majrur(fi, dar))
    assert jarr_majrur(fi, dar)[len(fi):] == cells_of("اَدَّارِ")
    assert case_class(cells_of("اَدَّارِ")) == "جرّ"
    assert kind(cells_of("لَهُمْ")) == "جار ومجرور" and kind(cells_of("إِلَيْهِ")) == "جار ومجرور"
    for w in ("فَوْقَ", "أَمَامَكَ", "بَيْنَهُمْ", "إِذَا", "إِذْ", "حَيْثُ", "مَسَاءً"):
        assert kind(cells_of(w)) == "ظرف", w
    assert len(STEMS) == 17
    assert kind(zarf(cells_of("مَسْجِدُ"))) == "—"  # قانونُ الحظر: المختصُّ خارج الجدول
    assert kind(jarr_majrur(fi, al(cells_of("مَسْجِدُ")))) == "جار ومجرور"
    for w in ("زَيْدٌ", "دَرَسَ", "كَرِيمُ", "مَعَ"):  # مَعَ ليست في الجدول المودَع — باسمها
        assert kind(cells_of(w)) == "—", w


def test_zaid_is_restored_by_raf() -> None:
    for w in ("أَحَدُ", "كِتَابُ", "رَجُلُ", "شَهِيدُ"):
        assert zaid_restores(cells_of(w)), w
    min_ = cells_of("مِنْ")
    assert (*jarr_majrur(min_, cells_of("أَحَدُ")), ("ن", "سكون")) == cells_of("مِنْأَحَدٍ")
    assert raf(jarr_majrur(min_, cells_of("أَحَدُ"))[len(min_):]) == cells_of("أَحَدُ")


def test_anchor_and_mahall_from_the_preceding_cells() -> None:
    assert anchor(cells_of("جَلَسَ")) == "فعل" and anchor(cells_of("قَائِمٌ")) == "مشتق"
    assert anchor(cells_of("اَلْعِلْمُ")) == "كون محذوف" and anchor(cells_of("هُوَ")) == "كون محذوف"
    assert mahall(cells_of("اَلْعِلْمُ")) == "خبر" and mahall(cells_of("طَائِرًا")) == "نعت"
    assert mahall(cells_of("اَلْعُصْفُورَ")) == "حال" and mahall(cells_of("اَلْكِتَابِ")) == "حال"
    for m in MAWSUL.values():
        assert mahall(m) == "صلة"
    for name in ("كِتَابُ", "رَجُلُ", "مُجْتَهِدُ"):
        w = cells_of(name)
        assert mahall((*nasb(w), ("ن", "سكون"))) == "نعت", name
        assert mahall(raf(al(w))) == "خبر" and mahall(nasb(al(w))) == "حال", name
    assert mahall(cells_of("هُوَ")) == "خبر" and mahall(cells_of("كِتَابِي")) == "—"  # المضافُ إلى الياء
    assert case_class(kawn("خبر")) == "رفع" and case_class(kawn("حال")) == "نصب"
    assert kawn("صلة") == cells_of("اِسْتَقَرَّ")
    assert all(licensed(kawn(m)) for m in ("خبر", "نعت", "حال", "صلة"))


def test_masaq_measurement_and_index() -> None:
    import subprocess
    import sys

    sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
    from gen_shibh_index import measure

    m = measure()
    kinds = m["kinds"]
    assert isinstance(kinds, dict)
    assert kinds[("جار ومجرور", "جار ومجرور")] > 8000 and kinds[("ظرف", "ظرف")] > 1300
    assert kinds.get(("ظرف", "جار ومجرور"), 0) < 30
    majrur = m["majrur"]
    assert isinstance(majrur, dict) and majrur["جرّ"] > 5000
    anch = m["anchor"]
    assert isinstance(anch, dict)
    assert anch[("خبر", "كون محذوف")] > 500 and anch[("نائب فاعل", "فعل")] > 5
    root = Path(__file__).parent.parent
    res = subprocess.run([sys.executable, str(root / "tools" / "gen_shibh_index.py"), "--check"],
                         capture_output=True, text=True, cwd=root)
    assert res.returncode == 0, res.stderr
