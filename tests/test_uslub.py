"""الأسلوب: الخبرُ وحدَه يحتمل الصدقَ والكذب، والإنشاءُ يُقرأ من الخانة؛ والقياسُ على MASAQ.

التوقّعاتُ من الحصر (الإنشاءُ محرومٌ من الصدق والكذب) على الخانات وشواهدِ البوّابة، والطفرةُ (نهيٌ يُقرأ
خبرًا، أمرٌ يُقرأ خبرًا، لَا النافيةُ تُقرأ نهيًا، تعجّبٌ بمرفوع) تُرفَض.
"""

from __future__ import annotations

from pathlib import Path

from slge.jazm import sukun
from slge.maqam import AMR_TEMPLATES, PRESENT_TEMPLATES, with_prefix
from slge.nawasikh import nasb, raf, tanwin
from slge.rawabit import cells_of
from slge.uslub import INSHA, LA, MA, TOOLS, present_any_mood, truth_apt, uslub
from slge.wazn import AWZAN, fill

ROOT_DIR = Path(__file__).resolve().parent.parent
ROOTS = (("ك", "ت", "ب"), ("د", "ر", "س"), ("ن", "ص", "ر"), ("ض", "ر", "ب"))


def test_truth_only_for_khabar_and_insha_read_from_cells() -> None:
    assert truth_apt("خبر") and not any(truth_apt(u) for u in INSHA) and len(TOOLS) == 14
    for r in ROOTS:
        for k in AMR_TEMPLATES:
            v = fill(AWZAN[k].template, r)
            assert uslub((), v) == "أمر" and uslub(LA, v) == "أمر" and not truth_apt(uslub((), v))
        for k in PRESENT_TEMPLATES:
            for p in "ءنتي":
                v = with_prefix(p, fill(AWZAN[k].template, r))
                if (k, p) == (5, "ء"):  # أَكْتِبْ مجزومًا = أَكْتِبْ أمرُ أَفْعَلَ بالخانة — باسمه
                    assert uslub(LA, sukun(v)) == "أمر"
                    continue
                assert uslub(LA, sukun(v)) == "نهي" and uslub(LA, v) == "خبر", (k, r, p)
                assert not truth_apt(uslub(LA, sukun(v))) and truth_apt(uslub(LA, v))
                assert present_any_mood(sukun(v)) and uslub((), v) == "خبر"
        afala = fill(AWZAN[11].template, r)
        zayd = cells_of("زَيْدُ")
        assert uslub(MA, afala, tanwin(nasb(zayd))) == "تعجّب"
        assert uslub(MA, afala, tanwin(raf(zayd))) == "خبر"


def test_witnesses_and_mutations() -> None:
    taktub = cells_of("تَكْتُبُ")
    assert uslub(cells_of("هَلْ"), taktub) == "استفهام"
    assert uslub(cells_of("مَتَى"), taktub) == "استفهام"
    assert uslub(cells_of("يَا"), cells_of("رَجُلُ")) == "نداء"
    assert uslub(cells_of("لَيْتَ"), cells_of("زَيْدًا")) == "تمنّ"
    assert uslub(cells_of("لَعَلَّ"), cells_of("زَيْدًا")) == "ترجّ"
    assert uslub((), cells_of("نِعْمَ")) == "مدح وذمّ" and uslub((), cells_of("بِئْسَ")) == "مدح وذمّ"
    assert uslub((), cells_of("كَتَبَ")) == "خبر" and uslub((), cells_of("اَرَّجُلُ")) == "خبر"
    assert uslub((), LA) == "—" and uslub(MA, cells_of("أَكْرَمَ")) == "—"
    assert uslub(cells_of("لَمْ"), sukun(taktub)) == "خبر"  # النفيُ بلَمْ خبرٌ لا نهي


def test_masaq_measurement_and_index() -> None:
    import subprocess
    import sys

    sys.path.insert(0, str(ROOT_DIR / "tools"))
    from gen_uslub_index import measure

    m = measure()
    read = m["read"]
    assert isinstance(read, dict)
    la_ok = read[("لَا", "نهي (إنشاء)", "نهي")] + read[("لَا", "نفي (خبر)", "خبر")]
    la_wrong = read[("لَا", "نهي (إنشاء)", "خبر")] + read[("لَا", "نفي (خبر)", "نهي")]
    assert la_ok >= 20 and la_ok > 2 * la_wrong and read[("لَا", "نفي (خبر)", "نهي")] == 0
    assert read[("أمر", "إنشاء", "أمر")] >= 80 and read[("استفهام", "إنشاء", "استفهام")] >= 20
    gen = str(ROOT_DIR / "tools" / "gen_uslub_index.py")
    res = subprocess.run([sys.executable, gen, "--check"], capture_output=True, text=True,
                         cwd=ROOT_DIR)
    assert res.returncode == 0, res.stderr
