"""المدود: حرفُ المدّ خانةٌ ساكنةٌ بعد حركتها، اللازمُ فاصلُ الثلاثيّ عن الثنائيّ، والأحكامُ من الخانة
التالية والحدّ، والقياسُ على مودَع المصحف.

التوقّعاتُ من الحصر (ثلاثةُ حروف مدّ؛ المتّصلُ بالهمزة في الكلمة والمنفصلُ بها في التالية؛ اللازمُ بالسكون
الأصليّ والعارضُ بالوقف؛ الصلةُ للهاء بين متحرّكين) على الخانات وشواهدِ البوّابة، والطفرةُ (مدٌّ في الصدر؛
مدّان متجاوران؛ لازمٌ في مرخَّصٍ ثنائيًّا؛ عارضٌ وصلًا) تُرفَض.
"""

from __future__ import annotations

from itertools import pairwise
from pathlib import Path

from slge.cells import licensed
from slge.madd import binary_ok, continue_licensed, has_vc, kinds, madd, pause_licensed
from slge.rawabit import cells_of
from slge.wazn import AWZAN, fill, mizan

ROOT_DIR = Path(__file__).resolve().parent.parent
ROOTS = (("ك", "ت", "ب"), ("ق", "و", "ل"), ("ض", "ر", "ب"))


def test_madd_letter_is_sukun_after_its_vowel_and_never_initial_or_adjacent() -> None:
    for k in range(len(AWZAN)):
        for r in ROOTS:
            w = fill(AWZAN[k].template, r)
            ks = kinds(w)
            assert ks[0] != "v", (k, r)
            assert all(not (a == "v" and b == "v") for a, b in pairwise(ks)), (k, r)
            for i, x in enumerate(ks):
                if x == "v":
                    assert w[i][1] == "سكون" and w[i - 1][1] != "سكون", (k, r, i)
                    assert w[i][0] in "اوي", (k, r, i)
            assert binary_ok(w) == licensed(w), (k, r)  # licensed_eq_binOK
        m = mizan(AWZAN[k].template)
        assert continue_licensed(m) and pause_licensed(m) and licensed(m), k
    # الطفرة: مدٌّ في الصدر غيرُ ممكن بالتعريف — ألفٌ ساكنةٌ أوّلًا تُقرأ ساكنًا لا مدًّا
    assert kinds((("ا", "سكون"), ("ب", "فتح"))) == ["c", "cv"]


def test_lazim_separates_ternary_from_binary() -> None:
    dallin = cells_of("اَضَّالِّينَ")
    assert continue_licensed(dallin) and not licensed(dallin) and has_vc(dallin)
    assert madd(dallin)[0] == (3, "لازم مثقَّل")
    hajja = cells_of("حَاجَّ")
    assert continue_licensed(hajja) and not licensed(hajja) and madd(hajja) == [(1, "لازم مثقَّل")]
    for w in ("قَالُو", "كَاتِبٌ", "اَلْعَالَمِينَ", "ءَامَنُو"):
        c = cells_of(w)
        # الطفرة: لازمٌ في مرخَّصٍ ثنائيًّا
        assert continue_licensed(c) and licensed(c) and not has_vc(c), w
    bahr = cells_of("بَحْرْ")
    assert pause_licensed(bahr) and not continue_licensed(bahr)  # وقفٌ لا وصل


def test_rules_read_from_next_cell_and_boundary() -> None:
    kana, illa, unzila = cells_of("كَانَ"), cells_of("إِلَّا"), cells_of("أُنْزِلَ")
    assert madd(cells_of("اَسَّمَاءِ")) == [(4, "متّصل")]
    assert madd(cells_of("ءَالْءَانَ")) == [(1, "لازم مخفَّف"), (4, "طبيعيّ")]
    alamin = cells_of("اَلْعَالَمِينَ")
    assert madd(alamin, pause=True) == [(3, "طبيعيّ"), (6, "عارض")]
    assert madd(alamin) == [(3, "طبيعيّ"), (6, "طبيعيّ")]  # الطفرة: عارضٌ وصلًا
    assert madd(cells_of("خَوْفٌ"), pause=True) == [(1, "لين")] and madd(cells_of("خَوْفٌ")) == []
    assert madd(cells_of("بِمَا"), unzila) == [(2, "منفصل")]
    assert madd(cells_of("بِمَا"), kana) == [(2, "طبيعيّ")]
    assert madd(cells_of("بِمَا"), unzila, pause=True) == [(2, "طبيعيّ")]  # لا منفصلَ وقفًا
    assert madd(cells_of("إِنَّهُ"), kana) == [(3, "صلة صغرى")]
    assert madd(cells_of("إِنَّهُ"), illa) == [(3, "صلة كبرى")]
    assert madd(cells_of("إِنَّهُ")) == []  # لا صلةَ بلا تالية
    assert madd(cells_of("أُولَئِكَ")) == [(1, "محجوب")]
    assert madd(cells_of("أُولُو")) == [(1, "محجوب"), (3, "طبيعيّ")]


def test_corpus_measurement_and_index() -> None:
    import subprocess
    import sys

    sys.path.insert(0, str(ROOT_DIR / "tools"))
    from gen_madd_index import measure

    m = measure()
    wasl = m["wasl"]
    assert isinstance(wasl, dict)
    assert m["forms"] == 18179 and m["tokens"] == 78207 and m["letters"] == 47865
    assert m["ternary_only"] == 65 == m["lazim_forms"]
    assert m["ternary_only_all_lazim"] and m["lazim_all_ternary_only"]  # lazim_iff_not_binary مقيسًا
    assert wasl["لازم مثقَّل"] + wasl["لازم مخفَّف"] == 108 and wasl["متّصل"] > 1500
    assert wasl["منفصل"] > 5000 and wasl["صلة صغرى"] + wasl["صلة كبرى"] > 4000
    assert sum(wasl.values()) >= m["letters"]  # كلُّ حرف مدٍّ له حكمٌ (والصلةُ والمحجوبُ زيادة)
    gen = str(ROOT_DIR / "tools" / "gen_madd_index.py")
    res = subprocess.run([sys.executable, gen, "--check"], capture_output=True, text=True,
                         cwd=ROOT_DIR)
    assert res.returncode == 0, res.stderr
