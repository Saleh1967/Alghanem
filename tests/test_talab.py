"""الطلب: صورُ الأمر الأربع من الخانة، اللامُ لكلّ شخصٍ وتجزم، الأمرُ ليس نهيًا على الخانة، والقياس.

التوقّعاتُ من الحصر (الأمرُ بالشيء ليس نهيًا عن ضدّه؛ الإلزامُ من القرائن) على الخانات وشواهدِ البوّابة،
والطفرةُ (لَا قبل الأمر نهيًا، لامٌ على ماضٍ، لامٌ ساكنةٌ بلا واو، مصدرٌ بعد فعل) تُرفَض.
"""

from __future__ import annotations

from pathlib import Path

from slge.cells import licensed
from slge.jazm import sukun
from slge.maqam import AMR_TEMPLATES, PRESENT_TEMPLATES, shakhs, with_prefix
from slge.rawabit import cells_of
from slge.talab import FA, ISM_FIL, WAW, lam_amr, lam_amr_after_waw, masdar_amr, talab
from slge.uslub import LA, uslub
from slge.wazn import AWZAN, fill

ROOT_DIR = Path(__file__).resolve().parent.parent
ROOTS = (("ك", "ت", "ب"), ("د", "ر", "س"), ("ن", "ص", "ر"), ("ض", "ر", "ب"))


def test_four_forms_and_lam_for_every_person() -> None:
    for r in ROOTS:
        for k in AMR_TEMPLATES:
            v = fill(AWZAN[k].template, r)
            assert talab((), v) == "صيغة" and shakhs(v) == "مخاطب", (k, r)
            assert uslub(LA, v) == "أمر" and uslub(LA, v) != "نهي"  # الأمرُ ليس نهيًا
        for k in PRESENT_TEMPLATES:
            for p, person in (("ي", "غائب"), ("ء", "متكلم"), ("ن", "متكلم")):
                v = with_prefix(p, fill(AWZAN[k].template, r))
                assert shakhs(v) == person and talab((), lam_amr(v)) == "لام", (k, r, p)
                assert lam_amr(v)[-1][1] == "سكون"
                assert licensed(lam_amr(v)) or k == 27  # المضعّفُ يُجزَم بالفتح — باسمه
                assert talab(WAW, lam_amr_after_waw(v)) == "لام" == talab(FA, lam_amr_after_waw(v))
                assert talab((), lam_amr_after_waw(v)) is None  # الطفرة: لامٌ ساكنةٌ بلا واو
                assert talab((), v) is None
                assert uslub(LA, sukun(v)) == ("أمر" if (k, p) == (5, "ء") else "نهي")  # أَكْتِبْ
        past = fill(AWZAN[0].template, r)
        assert talab((), (("ل", "كسر"), *past)) is None  # الطفرة: لامٌ على ماضٍ
    assert len(ISM_FIL) == 8 and all(talab((), cs) == "اسم فعل" for _, cs in ISM_FIL)
    darb = cells_of("ضَرْبُ")
    assert talab((), masdar_amr(darb)) == "مصدر"
    assert talab(cells_of("كَتَبَ"), masdar_amr(darb)) is None


def test_masaq_measurement_and_index() -> None:
    import subprocess
    import sys

    sys.path.insert(0, str(ROOT_DIR / "tools"))
    from gen_talab_index import measure

    m = measure()
    read, markers, before = m["read"], m["markers"], m["before"]
    assert isinstance(read, dict) and isinstance(markers, dict) and isinstance(before, dict)
    assert read[("فعل أمر", "صيغة")] >= 80 and read[("اسم فعل أمر", "اسم فعل")] >= 1
    assert sum(markers.values()) == 71 and set(markers) <= {"السكون", "حذف النون", "حذف حرف العلة"}
    assert before["بعد الواو أو الفاء"] > before["في الصدر"]
    gen = str(ROOT_DIR / "tools" / "gen_talab_index.py")
    res = subprocess.run([sys.executable, gen, "--check"], capture_output=True, text=True,
                         cwd=ROOT_DIR)
    assert res.returncode == 0, res.stderr
