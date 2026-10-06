"""الجهةُ والزمن: الصيغةُ من الحالات، الأمرُ للمخاطب، الإزاحةُ على المضارع وحده، والقياسُ على MASAQ.

التوقّعاتُ من الحصر المُرسَل (الأمرُ للمخاطب؛ الماضي لا يُصاغ للمستقبل) على الخانات وشواهدِ البوّابة،
والطفرةُ (سينٌ على ماضٍ، أمرٌ يُقرأ غائبًا، ماضٍ يُقرأ مضارعًا، لَمْ على ماضٍ) تُرفَض.
"""

from __future__ import annotations

from pathlib import Path

from slge.cells import licensed
from slge.jiha import KANA, LAM, LAN, SA, SAWFA, SHIFTS, jiha, shift, sigha, states_disjoint
from slge.maqam import AMR_TEMPLATES, PAST_TEMPLATES, PRESENT_TEMPLATES, shakhs, with_prefix
from slge.rawabit import cells_of
from slge.wazn import AWZAN, fill

ROOT_DIR = Path(__file__).resolve().parent.parent
ROOTS = (("د", "ر", "س"), ("ك", "ت", "ب"), ("ن", "ص", "ر"), ("ض", "ر", "ب"), ("ع", "ل", "م"))


def test_sigha_is_a_function_of_states_for_every_root() -> None:
    assert states_disjoint()
    for r in ROOTS:
        for k in PAST_TEMPLATES:
            assert sigha(fill(AWZAN[k].template, r)) == "ماضٍ", (k, r)
        for k in AMR_TEMPLATES:
            assert sigha(fill(AWZAN[k].template, r)) == "أمر", (k, r)
        for k in PRESENT_TEMPLATES:
            m = fill(AWZAN[k].template, r)
            assert all(sigha(with_prefix(p, m)) == "مضارع" for p in "ءنتي"), (k, r)
            assert sigha(with_prefix("ب", m)) is None  # الطفرة
    assert sigha(cells_of("زَيْدٌ")) is None and sigha(cells_of("كَتَبْتُ")) is None


def test_amr_is_mukhatab_and_ghaib_by_lam() -> None:
    for r in ROOTS:
        for k in AMR_TEMPLATES:
            v = fill(AWZAN[k].template, r)
            assert shakhs(v) == "مخاطب" and sigha(v) == "أمر", (k, r)
    assert shakhs(cells_of("اُكْتُبْ")) == "مخاطب" and shakhs(cells_of("يَكْتُبُ")) == "غائب"
    assert sigha(cells_of("يَكْتُبُ")) == "مضارع" and cells_of("لِيَكْتُبْ")[:1] == cells_of("لِ")
    assert cells_of("لِيَكْتُبْ")[1:] == shift("لم", cells_of("يَكْتُبُ"))[1]  # type: ignore[index]


def test_shift_only_on_present() -> None:
    kataba, yaktubu, uktub = cells_of("كَتَبَ"), cells_of("يَكْتُبُ"), cells_of("اُكْتُبْ")
    for s in SHIFTS:
        assert shift(s, kataba) is None and shift(s, uktub) is None, s  # الطفرة
        got = shift(s, yaktubu)
        assert got is not None and licensed(got[1]), s
    assert shift("س", yaktubu) == ((), (*SA, *yaktubu))
    assert shift("سوف", yaktubu) == (SAWFA, yaktubu)
    assert shift("لم", yaktubu) == (LAM, cells_of("يَكْتُبْ"))
    assert shift("لن", yaktubu) == (LAN, cells_of("يَكْتُبَ"))
    assert shift("كان", yaktubu) == (KANA, yaktubu)
    assert jiha((), cells_of("سَيَكْتُبُ")) == "مستقبل" and jiha((), cells_of("سَكَتَبَ")) == "—"
    assert jiha(LAM, cells_of("يَكْتُبْ")) == "ماضٍ منفيّ" and jiha(LAM, kataba) == "ماضٍ"
    assert jiha(KANA, yaktubu) == "ماضٍ مستمرّ" and jiha(SAWFA, kataba) == "ماضٍ"


def test_masaq_measurement_and_index() -> None:
    import subprocess
    import sys

    sys.path.insert(0, str(ROOT_DIR / "tools"))
    from gen_jiha_index import measure

    m = measure()
    bare, fut = m["bare"], m["fut"]
    assert isinstance(bare, dict) and isinstance(fut, dict)
    agree = sum(v for (t, s), v in bare.items() if t == s)
    wrong = sum(v for (t, s), v in bare.items() if s not in (t, "—"))
    assert agree > 4000 and agree > 15 * wrong
    assert fut["مضارع"] > 100 and fut.get("ماضٍ", 0) + fut.get("أمر", 0) <= 1
    gen = str(ROOT_DIR / "tools" / "gen_jiha_index.py")
    res = subprocess.run([sys.executable, gen, "--check"], capture_output=True, text=True,
                         cwd=ROOT_DIR)
    assert res.returncode == 0, res.stderr
