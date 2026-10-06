"""التعليلُ والسببيّة: العلّةُ لا تُرفَع، صورتاها كلمةٌ واحدة، السببيّةُ ترتيبٌ صارم، التنازعُ للأقرب، والقياس.

التوقّعاتُ من الحصر المُرسَل (الترتيبُ الصارم: لا انعكاس/تعدٍّ/لا دور؛ أدواتُ التعليل معاملات؛ التنازعُ
إعمالُ الثاني بضميرٍ للأوّل) وشواهدِ البوّابة، والطفرةُ (علّةٌ مرفوعة، دورٌ سببيّ، الأوّلُ ينصب المتنازَع
فيه، مفعولٌ به معرَّفٌ يُقرأ علّة) تُرفَض.
"""

from __future__ import annotations

from pathlib import Path

from slge.cells import licensed
from slge.filiyya import sort_fadla
from slge.majrurat import jarr
from slge.nawasikh import nasb, raf
from slge.rawabit import cells_of
from slge.talil import (
    LI_ANNA,
    MIN_AJLI,
    TOOLS,
    apply,
    derives,
    maful_li_ajlih,
    talil,
    tanazu,
    two_forms_same_word,
)
from slge.tawabi import case_class
from slge.wazn import AWZAN

ROOT_DIR = Path(__file__).resolve().parent.parent
N = len(AWZAN)


def test_cause_is_never_raf_and_two_forms_are_one_word() -> None:
    for w in ("حَذَرُ", "رَحْمَةُ", "خَشْيَةُ", "اِبْتِغَاءُ"):
        c = cells_of(w)
        assert case_class(maful_li_ajlih(c)) == "نصب" and two_forms_same_word(c), w
        assert maful_li_ajlih(c)[:-1] == jarr(c)[:-1] and maful_li_ajlih(c) != raf(c), w
        for _, _, amal in TOOLS:
            assert case_class(apply(amal, c)) != "رفع", (w, amal)
    assert len(TOOLS) == 6 and all(licensed(cs) for _, cs, _ in TOOLS)
    assert cells_of("لِأَنَّ") == LI_ANNA and cells_of("مِنْأَجْلِ") == MIN_AJLI
    assert apply("إنّ", cells_of("زَيْدُ")) == nasb(cells_of("زَيْدُ"))
    assert sort_fadla(cells_of("حَذَرَ"), cells_of("دَرَسَ")) == "مفعول لأجله"
    assert sort_fadla(cells_of("دَرْسَ"), cells_of("دَرَسَ")) == "مفعول مطلق"


def test_derivational_causality_is_a_strict_partial_order() -> None:
    rel = {(a, b) for a in range(N) for b in range(N) if derives(a, b)}
    assert rel and not any(derives(a, a) for a in range(N))  # لا انعكاس
    assert all((b, a) not in rel for a, b in rel)  # لا دور
    assert all((a, d) in rel for a, b in rel for (b2, d) in rel if b2 == b)  # تعدٍّ
    assert all(derives(a, 29) for a in range(N) if a != 29)
    assert not any(derives(29, b) for b in range(N))
    # الطفرة: قلبُ العلاقة يكسر التعدّي أو التباين
    flipped = {(b, a) for a, b in rel}
    assert flipped.isdisjoint(rel)


def test_tanazu_nearer_works_and_first_keeps_pronoun() -> None:
    alimtu, amiltu, khayr = cells_of("عَلِمْتُ"), cells_of("عَمِلْتُ"), cells_of("اَلْخَيْرُ")
    hu = (("ه", "ضم"),)
    v1, v2, w = tanazu(alimtu, amiltu, khayr, hu)
    assert v1 == cells_of("عَلِمْتُهُ") and licensed(v1) and v2 == amiltu
    assert case_class(w) == "نصب" and w == nasb(khayr)
    # الطفرة: الفعلُ الأوّل لا يمسّ خانةَ المتنازَع فيه مهما تغيّر
    assert tanazu(cells_of("ضَرَبْتُ"), amiltu, khayr, hu)[2] == w


def test_reader_and_masaq() -> None:
    darasa = cells_of("دَرَسَ")
    assert talil(darasa, cells_of("حَذَرَ")) == "مفعول لأجله"
    assert talil(darasa, cells_of("دَرْسَ")) == "—" and talil(darasa, LI_ANNA) == "لأنّ"
    assert talil(darasa, cells_of("بِضَرْبِ")) == "تعليل بالحرف"
    assert talil(cells_of("أَكَلَ"), cells_of("اَدَّرْسَ")) == "—"  # معرَّفٌ: مفعولٌ به
    import subprocess
    import sys

    sys.path.insert(0, str(ROOT_DIR / "tools"))
    from gen_talil_index import measure

    m = measure()
    read = m["read"]
    assert isinstance(read, dict)
    hit = read[("مفعول لأجله", "مفعول لأجله")]
    total = sum(v for (t, _), v in read.items() if t == "مفعول لأجله")
    bih = sum(v for (t, _), v in read.items() if t == "مفعول به")
    assert total >= 30 and hit / total >= 0.6, (hit, total)
    assert read[("مفعول به", "مفعول لأجله")] < 0.1 * bih
    cases = m["cases"]
    assert isinstance(cases, dict) and set(cases) == {"منصوب"}
    gen = str(ROOT_DIR / "tools" / "gen_talil_index.py")
    res = subprocess.run([sys.executable, gen, "--check"], capture_output=True, text=True,
                         cwd=ROOT_DIR)
    assert res.returncode == 0, res.stderr
