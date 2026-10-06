"""النِّسَبُ الثلاث: الإسنادُ عمليّةٌ واحدة، التقييدُ لا يُنشئ رفعًا، التضمينُ ترتيبٌ جزئيّ، والقياسُ على MASAQ.

التوقّعاتُ من الحصر المُرسَل (النسبُ الثلاث؛ خواصُّ الترتيب الجزئيّ الثلاث؛ الفصلُ النوعيّ) وشواهدِ البوّابة،
والطفرةُ (تضمينٌ معكوس، جرٌّ يُقرأ رفعًا، قالبان بصورةٍ واحدة) تُرفَض.
"""

from __future__ import annotations

from pathlib import Path

from slge.jumla import nominal
from slge.nisab import (
    F,
    chain,
    contains,
    dist,
    form_contains_root,
    isnad,
    nisba,
    species_distinct,
    taqyid_case,
)
from slge.rawabit import cells_of
from slge.shabaka import ROOT
from slge.tawabi import case_class, follows
from slge.wazn import AWZAN, FAL, mizan


def test_isnad_is_one_operation() -> None:
    for w in ("اَلْعِلْمَ", "زَيْدٍ", "اَلْمُجْتَهِدُ"):
        c = cells_of(w)
        assert isnad(c) == nominal(c, c).mubtada and case_class(isnad(c)) == "رفع", w


def test_taqyid_never_creates_raf() -> None:
    for w in ("رَاكِبُ", "زَيْدُ", "كِتَابُ"):
        c = cells_of(w)
        assert taqyid_case("حال", c) == "نصب" and taqyid_case("مفعول", c) == "نصب", w
        assert taqyid_case("إضافة", c) == "جرّ" and taqyid_case("نعت", c) == "تبع", w
        assert follows(c, c) and follows(isnad(c), isnad(cells_of("رَجُلُ")))
        assert not follows(isnad(c), cells_of("زَيْدًا"))  # الطفرة: تابعٌ منصوبٌ لمرفوع


def test_containment_is_a_partial_order_and_forms_contain_roots() -> None:
    a, b, c = (1, 2, 3, 4), (2, 4), (4,)
    assert contains(a, a) and contains(b, b)  # انعكاسيّة
    assert contains(a, b) and contains(b, c) and contains(a, c)  # تعدّية
    assert not contains(b, a)  # تضادُّ التباين: a ≠ b فلا يتضمّن كلٌّ الآخر
    assert not contains(a, (3, 2))  # الطفرة: الترتيبُ جزءٌ من التضمين
    for k in range(len(AWZAN)):
        assert form_contains_root(k, FAL) and form_contains_root(k, ("ك", "ت", "ب")), AWZAN[k].name
    assert species_distinct()
    assert mizan(AWZAN[35].template) == mizan(AWZAN[41].template)  # فِعَال مرّتين: قالبٌ واحدٌ بمعنيين
    assert AWZAN[35].template == AWZAN[41].template


def test_chains_end_at_root() -> None:
    names = [w.name for w in AWZAN]
    for k in range(len(AWZAN)):
        ch = chain(k, F)
        assert ch[0] == k and names[ch[-1]] == ROOT and dist(k) == len(ch) - 1
    assert dist(names.index(ROOT)) == 0 and max(dist(k) for k in range(len(AWZAN))) == 5


def test_reader_and_masaq() -> None:
    import subprocess
    import sys

    assert nisba(cells_of("اَلْعِلْمُ"), cells_of("نُورٌ")) == "إسناد"
    assert nisba(cells_of("أَكَلَ"), cells_of("زَيْدٌ")) == "إسناد"
    assert nisba(cells_of("هُوَ"), cells_of("قَائِمٌ")) == "إسناد"
    assert nisba(cells_of("رَجُلٌ"), cells_of("كَرِيمٌ")) == "تقييد"
    assert nisba(cells_of("زَيْدٌ"), cells_of("رَاكِبًا")) == "تقييد"
    assert nisba(cells_of("كِتَابُ"), cells_of("زَيْدٍ")) == "تقييد"
    assert nisba(cells_of("اَلْعِلْمُ"), cells_of("دَرَسَ")) == "إسناد"
    assert nisba(cells_of("دَرَسَ"), cells_of("دَرَسَ")) == "—"
    sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
    from gen_nisab_index import measure

    m = measure()
    read = m["read"]
    assert isinstance(read, dict)
    total = sum(read.values())
    agree = sum(v for (t, n), v in read.items() if t.split(":")[0] == n)
    assert total > 10000 and agree * 100 >= 60 * total
    assert read[("إسناد: مبتدأ وخبر", "إسناد")] > 1200 and read[("تقييد: مفعول به", "تقييد")] > 1900
    root = Path(__file__).parent.parent
    res = subprocess.run([sys.executable, str(root / "tools" / "gen_nisab_index.py"), "--check"],
                         capture_output=True, text=True, cwd=root)
    assert res.returncode == 0, res.stderr
