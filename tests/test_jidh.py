"""الجذع: تسويةُ الآخر قبل القالب، وفصلُ الزوائد بردٍّ بعينه، والرقمُ قبلُ وبعدُ على المودَع نفسه.

التوقّعاتُ من فحص الشجرة (القوالبُ مودَعةٌ بآخرٍ واحد؛ الزوائدُ من الجداول الحاصرة) على الخانات وشواهدِ
البوّابة وقسمةِ MASAQ المحجوبة، والطفرةُ (قراءةٌ لا تُردّ إلى الكلمة؛ جذعٌ بألف؛ سابقةٌ من غير الجداول)
تُرفَض.
"""

from __future__ import annotations

from pathlib import Path

from slge.cells import SUKUN
from slge.jidh import ENCLITICS, PROCLITICS, Reading, jidh, on_template_mod, stem_senses
from slge.rawabit import cells_of
from slge.wazn import AWZAN, fill, root_of
from slge.zuruf import set_last

ROOT_DIR = Path(__file__).resolve().parent.parent
ROOTS = (("ك", "ت", "ب"), ("د", "ر", "س"), ("ض", "ر", "ب"))
STATES = ("فتح", "كسر", "ضم", SUKUN)


def test_case_is_the_last_cell_not_the_template() -> None:
    for k in range(len(AWZAN)):
        t = AWZAN[k].template
        for r in ROOTS:
            w = fill(t, r)
            for st in STATES:
                v = set_last(w, st)
                assert on_template_mod(k, v) and root_of(t, v) == r, (k, r, st)
                assert k in stem_senses(v), (k, r, st)
    assert stem_senses(cells_of("رَبِّ")) == (29,) and stem_senses(cells_of("رَبُّ")) == (29,)
    assert stem_senses(cells_of("كَذَّبُ")) == (12,)  # الماضي قبل واو الجماعة
    # الطفرة: جذعٌ بألفٍ في موضع أصلٍ لا يُقرأ (الألفُ ليست أصلًا)
    assert stem_senses(cells_of("قَالَ")) == ()


def test_peeling_restores_the_word_exactly() -> None:
    words = ("وَلْأَرْضِ", "أَلْأَرْضُ", "وَشَّمْسِ", "رَبِّ", "كَذَّبُو", "تَجْعَلُو", "بِكِتَابِهِمْ", "وَجَدَ",
             "فَبِمَا", "يَكْتُبُونَ", "كِتَابُكُمْ")
    for w in words:
        c = cells_of(w)
        rs = jidh(c)
        assert rs, w
        for r in rs:
            assert r.restore() == c, (w, r)  # jidh_restores
            assert all(p in PROCLITICS for p in r.pre), (w, r)
            assert r.suf == () or r.suf in ENCLITICS, (w, r)
            assert r.templates and r.stem
    assert [(len(r.pre), r.al, r.templates) for r in jidh(cells_of("وَلْأَرْضِ"))] == [(1, 2, (29,))]
    assert [(len(r.pre), r.al, r.templates) for r in jidh(cells_of("أَلْأَرْضُ"))] == [(0, 1, (29,))]
    rs2 = jidh(cells_of("بِكِتَابِهِمْ"))
    assert len(rs2) == 1 and len(rs2[0].pre) == 1 and len(rs2[0].suf) == 2
    assert rs2[0].templates == (35, 41, 93)
    assert [r.templates for r in jidh(cells_of("وَجَدَ"))] == [(0, 36)]
    # الطفرة: قراءةٌ مزوَّرةٌ لا تُردّ
    fake = Reading(((("و", "فتح"),),), 0, cells_of("أَرْضِ"), (), (29,))
    assert fake.restore() != cells_of("وَلْأَرْضِ")
    assert jidh(cells_of("لَا")) == () and jidh(cells_of("هُوَ")) == ()


def test_numbers_before_and_after_on_the_same_deposit() -> None:
    import subprocess
    import sys

    sys.path.insert(0, str(ROOT_DIR / "tools"))
    from gen_jidh_index import measure

    m = measure()
    assert m["forms"] == 18179
    assert m["before"] == 1743 and m["step1"] == 4682 and m["step2"] == 13706
    assert m["before"] < m["step1"] < m["step2"]
    assert m["gold_match"] > 14000 and m["gold_match"] + m["gold_among"] > 18000
    assert m["only_wrong"] < m["gold_match"] / 2
    gen = str(ROOT_DIR / "tools" / "gen_jidh_index.py")
    res = subprocess.run([sys.executable, gen, "--check"], capture_output=True, text=True,
                         cwd=ROOT_DIR)
    assert res.returncode == 0, res.stderr
