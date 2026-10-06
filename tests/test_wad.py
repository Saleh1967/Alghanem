"""الوضعُ والمشتركُ والترادف: الوضعُ متباينٌ في الجذر، المشتركُ محصورٌ ومجدوَل، الميزانُ لا يُشترَك، والقياسُ
على MASAQ.

التوقّعاتُ من الحصر (المشتركُ يحتاج قرينة؛ المترادفان معنًى واحد؛ الوضعُ يُستردّ) على الخانات وشواهدِ
البوّابة، والطفرةُ (زوجٌ يلتقي خارجَ الجدول؛ ميزانٌ يُشترَك؛ جذران على صورةٍ واحدة من قالبٍ واحد) تُرفَض.
"""

from __future__ import annotations

from itertools import combinations
from pathlib import Path

from slge.filiyya import MASDAR_TEMPLATES
from slge.marifa import drop_tanwin
from slge.rawabit import cells_of
from slge.wad import classes, collision_pairs, duplicates, may_collide, senses, unaided, wad
from slge.wazn import AWZAN, fill, mizan, root_of

ROOT_DIR = Path(__file__).resolve().parent.parent
ROOTS = (("ك", "ت", "ب"), ("د", "ر", "س"), ("ق", "ع", "د"), ("ض", "ر", "ب"), ("ن", "ش", "ر"),
         ("ت", "ش", "ر"), ("م", "ن", "ح"), ("ن", "ح", "ت"))


def test_wad_is_injective_in_root_and_recovered_from_the_word() -> None:
    for k in range(len(AWZAN)):
        t = AWZAN[k].template
        forms = {fill(t, r) for r in ROOTS}
        assert len(forms) == len(ROOTS), k  # الوضعُ متباينٌ في الجذر
        for r in ROOTS:
            assert root_of(t, fill(t, r)) == r and k in senses(fill(t, r)), (k, r)
        assert len(classes(mizan(t))) == 1 and classes(mizan(t))[0] <= k  # الميزانُ لا يُشترَك
        assert senses(mizan(t)) == tuple(q for q in range(len(AWZAN))
                                         if AWZAN[q].template == t)


def test_homonymy_is_bounded_and_tabled() -> None:
    pairs = collision_pairs()
    dups = duplicates()
    assert len(pairs) == 42 and len(dups) == 6 and set(dups) <= set(pairs)
    assert sum(AWZAN[k].template != AWZAN[q].template for k, q in pairs) == 36
    # كلُّ التقاءٍ فعليٍّ لجذرين لا ألفَ فيهما زوجُه في الجدول (الطفرة: زوجٌ خارجَه يلتقي)
    for k, q in combinations(range(len(AWZAN)), 2):
        tk, tq = AWZAN[k].template, AWZAN[q].template
        met = any(fill(tk, r) == fill(tq, r2) for r in ROOTS for r2 in ROOTS)
        if met:
            assert (k, q) in pairs and may_collide(tk, tq), (k, q)
        if (k, q) not in pairs:
            assert not met and not may_collide(tk, tq), (k, q)
    intishar = drop_tanwin(cells_of("اِنْتِشَارٌ"))
    assert fill(AWZAN[44].template, ("ت", "ش", "ر")) == intishar
    assert fill(AWZAN[45].template, ("ن", "ش", "ر")) == intishar and (44, 45) in pairs
    assert wad(cells_of("اِنْتِشَارٌ")) == "مشترك الصورة" and not unaided(intishar)
    assert wad(cells_of("مَنْحَةٌ")) == "مشترك الصورة"
    # اشتراكُ الوضع: صورةٌ واحدةٌ لأكثر من باب — والقارئُ يفصله عن اشتراك الصورة
    for w in ("كِتَابٌ", "هِلَالٌ", "بُيُوتٌ", "قُعُودٌ"):
        assert wad(cells_of(w)) == "مشترك الوضع" and len(classes(drop_tanwin(cells_of(w)))) == 1, w
    for w in ("عَيْنٌ", "قَمَرٌ", "كَاتِبٌ", "يَكْتُبُ", "ءَامَنَ"):
        assert wad(cells_of(w)) == "مفرد الوضع" and unaided(drop_tanwin(cells_of(w))), w
    assert wad(cells_of("هُوَ")) == "مجدوَل" and wad(cells_of("لَا")) == "—"


def test_synonyms_share_root_and_differ_in_form() -> None:
    for r in ROOTS:
        forms: dict[tuple[tuple[str, str], ...], int] = {}
        for k in MASDAR_TEMPLATES:
            t = AWZAN[k].template
            w = fill(t, r)
            assert root_of(t, w) == r, (k, r)  # المترادفان يشتركان في الجذر
            if w in forms:
                assert AWZAN[forms[w]].template == t, (k, forms[w])  # لا يتّحدان إلّا بتطابق القالب
            forms.setdefault(w, k)
        assert len(forms) >= len(MASDAR_TEMPLATES) - 3


def test_masaq_measurement_and_index() -> None:
    import subprocess
    import sys

    sys.path.insert(0, str(ROOT_DIR / "tools"))
    from gen_wad_index import measure

    m = measure()
    dist, sura, wadc = m["dist"], m["sura"], m["wad"]
    assert isinstance(dist, dict) and isinstance(sura, dict) and isinstance(wadc, dict)
    readable = dist["مفرد الوضع"] + dist["مشترك الوضع"] + dist["مشترك الصورة"]
    assert dist["مفرد الوضع"] > 2500 and dist["مفرد الوضع"] / readable > 0.9
    assert dist["مشترك الصورة"] > 100 and dist["مشترك الوضع"] > 40 and dist["مجدوَل"] > 2000
    assert all(c in set(collision_pairs()) for (c, _) in sura if len(c) == 2)
    assert sura[((11, 12), "علَم")] > 80  # اللَّهُ بسابقة أل: أَفْعَلَ/فَعَّلَ بالخانة — باسمه
    gen = str(ROOT_DIR / "tools" / "gen_wad_index.py")
    res = subprocess.run([sys.executable, gen, "--check"], capture_output=True, text=True,
                         cwd=ROOT_DIR)
    assert res.returncode == 0, res.stderr
