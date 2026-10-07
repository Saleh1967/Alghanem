"""المتباين: التباينُ متماثلٌ غيرُ انعكاسيّ، والأصلُ في الوضع التباين على القالب المعزول، والقسمُ الثامن،
والقياسُ على MASAQ.

التوقّعاتُ من الحصر (المتباين يكثر طرفاه ومعانيه لا تلتقي؛ التباينُ متماثلٌ غيرُ انعكاسيّ؛ الأصلُ عدم
الترادف) على الخانات وشواهدِ البوّابة، والطفرةُ (كلمةٌ تباين نفسَها؛ تباينٌ من جهةٍ واحدة؛ جذران على
قالبٍ معزول يلتقيان) تُرفَض.
"""

from __future__ import annotations

from itertools import combinations
from pathlib import Path

from slge.marifa import drop_tanwin
from slge.rawabit import cells_of
from slge.tabayun import isolated, mawadd, rel, share_madda, tabayun
from slge.wad import collision_pairs, duplicates
from slge.wazn import AWZAN, fill

ROOT_DIR = Path(__file__).resolve().parent.parent
ROOTS = (("ك", "ت", "ب"), ("د", "ر", "س"), ("ق", "ع", "د"), ("ض", "ر", "ب"), ("ن", "ش", "ر"))


def test_tabayun_is_symmetric_and_irreflexive() -> None:
    forms = [fill(AWZAN[k].template, r) for k in (0, 6, 29, 35, 48, 101) for r in ROOTS]
    forms += [drop_tanwin(cells_of(w)) for w in ("اِنْتِشَارٌ", "نَشْرٌ", "مَنْحَةٌ", "لَا")]
    for a in forms:
        assert not tabayun(a, a)
        assert share_madda(a, a) == bool(mawadd(a))
        for b in forms:
            assert tabayun(a, b) == tabayun(b, a)
            assert rel(a, b) != "—" or not (mawadd(a) and mawadd(b))
            assert share_madda(a, b) == share_madda(b, a)


def test_default_is_divergence_on_isolated_templates() -> None:
    iso = [k for k in range(len(AWZAN)) if isolated(k)]
    assert len(iso) == 81  # كانت 77 من 121؛ قوالبُ الاسم الأربعةُ معزولة
    non_iso = {k for p in collision_pairs() if p not in duplicates() for k in p}
    assert set(iso) == set(range(len(AWZAN))) - non_iso
    for k in iso:
        t = AWZAN[k].template
        for r, r2 in combinations(ROOTS, 2):
            a, b = fill(t, r), fill(t, r2)
            assert a != b and tabayun(a, b), (k, r, r2)
            assert set(mawadd(a)) == {r} and set(mawadd(b)) == {r2}, (k, r, r2)
    # الطفرة: على غير المعزول يقع التداخل (اِنْفِعَالٌ 44 بـ ت‑ش‑ر = اِفْتِعَالٌ 45 بـ ن‑ش‑ر)
    w = fill(AWZAN[44].template, ("ت", "ش", "ر"))
    assert not isolated(44) and set(mawadd(w)) == {("ت", "ش", "ر"), ("ن", "ش", "ر")}


def test_seven_fold_division_and_its_eighth() -> None:
    darb, qatl = cells_of("ضَرْبٌ"), cells_of("قَتْلٌ")
    assert rel(darb, qatl) == rel(qatl, darb) == "متباينان"
    assert rel(darb, cells_of("ضِرَابٌ")) == "متّحدا المادّة"
    assert rel(cells_of("كَتَبَ"), cells_of("كَاتِبٌ")) == "متّحدا المادّة"
    assert rel(cells_of("اِنْتِشَارٌ"), cells_of("نَشْرٌ")) == "متداخلان"
    assert rel(cells_of("كِتَابٌ"), cells_of("كِتَابٌ")) == "منفرد"
    assert rel(cells_of("اِنْتِشَارٌ"), cells_of("اِنْتِشَارٌ")) == "مشترك"
    # سَوَادٌ/بَيَاضٌ كانا «—» قبل فَعَال (أ2) فصارا متباينين على قالبٍ واحد؛ وما ليس على قالبٍ يبقى «—»
    assert rel(cells_of("سَوَادٌ"), cells_of("بَيَاضٌ")) == "متباينان"
    assert rel(cells_of("لَا"), darb) == "—" and rel(cells_of("إِبْرَاهِيمُ"), darb) == "—"


def test_masaq_measurement_and_index() -> None:
    import subprocess
    import sys

    sys.path.insert(0, str(ROOT_DIR / "tools"))
    from gen_tabayun_index import measure

    m = measure()
    pairs, families = m["pairs"], m["families"]
    assert isinstance(pairs, dict) and isinstance(families, dict)
    total = sum(pairs.values())
    assert m["forms"] == 988 and m["isolated"] == 81  # كانت 936 و77 قبل قوالب الاسم (أ2)
    assert pairs["متباينان"] / total > 0.99 and pairs["متّحدا المادّة"] > 500
    assert pairs["متداخلان"] > 0
    assert families[("ن", "ز", "ل")] == 10 and families[("ك", "ف", "ر")] == 10
    gen = str(ROOT_DIR / "tools" / "gen_tabayun_index.py")
    res = subprocess.run([sys.executable, gen, "--check"], capture_output=True, text=True,
                         cwd=ROOT_DIR)
    assert res.returncode == 0, res.stderr
