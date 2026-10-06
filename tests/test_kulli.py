"""الكليُّ والجزئيّ: القالبُ في أفراده، الجزئيُّ من جدول، المصدرُ مجرّدٌ من الزمن، والقياسُ على MASAQ.

التوقّعاتُ من الحصر (الكليُّ في الخارج وجودُه في أفراده؛ المصدرُ بلا زمن؛ الفعلُ مهيّأ) على الخانات وشواهدِ
البوّابة، والطفرةُ (مصدرٌ يُقرأ مضارعًا أو يُزاح بالسين؛ ضميرٌ يُقرأ ماهويًّا) تُرفَض.
"""

from __future__ import annotations

from pathlib import Path

from slge.categories import PRONOUNS
from slge.filiyya import MASDAR_TEMPLATES
from slge.ishara import FORMS as ISHARA
from slge.jiha import SHIFTS, shift, sigha
from slge.kulli import kulli
from slge.mansubat import DERIVED
from slge.maqam import AMR_TEMPLATES, PAST_TEMPLATES, PRESENT_TEMPLATES, with_prefix
from slge.marifa import MAWSUL
from slge.rawabit import cells_of
from slge.sarf import on_template
from slge.wazn import AWZAN, fill, root_of

ROOT_DIR = Path(__file__).resolve().parent.parent
ROOTS = (("ك", "ت", "ب"), ("د", "ر", "س"), ("ق", "ع", "د"), ("ض", "ر", "ب"))


def test_universal_lives_in_its_particulars_and_particulars_are_tabled() -> None:
    for k in range(len(AWZAN)):
        t = AWZAN[k].template
        for r in ROOTS:
            w = fill(t, r)
            assert on_template(k, w) and root_of(t, w) == r, (k, r)
    tabled = [*PRONOUNS, *(f.cells for f in ISHARA), *MAWSUL.values()]
    on_some = [w for w in tabled if any(on_template(k, w) for k in range(len(AWZAN)))]
    assert len(on_some) == 4 and all(kulli(w) == "جزئيّ" for w in tabled)
    assert not set(DERIVED) & set(MASDAR_TEMPLATES)


def test_masdar_has_no_tense_and_verb_has() -> None:
    for r in ROOTS:
        for k in MASDAR_TEMPLATES:
            m = fill(AWZAN[k].template, r)
            assert sigha(m) is None and all(shift(s, m) is None for s in SHIFTS), (k, r)
            # مُفَاعَلَةٌ = مُفَاعَلٌ + ة (اسمُ مفعولٍ مؤنّث) بالخانة: يُقرأ عرضيًّا — باسمه
            assert kulli(m) == ("كليّ عرضيّ" if k == 40 else "حدث مجرّد"), (k, r)
        for k in PAST_TEMPLATES + AMR_TEMPLATES:
            assert kulli(fill(AWZAN[k].template, r)) == "حدث مهيّأ", (k, r)
        for k in PRESENT_TEMPLATES:
            for p in "ءنتي":
                assert kulli(with_prefix(p, fill(AWZAN[k].template, r))) == "حدث مهيّأ", (k, r, p)
    # الطفرة المسمّاة: فَعْلَة بفاءٍ هي صدرُ مضارع (نَصْرَةٌ) تشابه نَفْعَلُ — يُستثنى في البرهان بشرطه
    assert kulli(cells_of("كَاتِبٌ")) == "كليّ عرضيّ" and kulli(cells_of("رَجُلٌ")) == "كليّ ماهويّ"
    assert kulli(cells_of("هُوَ")) == "جزئيّ" and kulli(cells_of("لَا")) == "—"


def test_masaq_measurement_and_index() -> None:
    import subprocess
    import sys

    sys.path.insert(0, str(ROOT_DIR / "tools"))
    from gen_kulli_index import measure

    m = measure()
    read, on_mizan = m["read"], m["mizan"]
    assert isinstance(read, dict) and isinstance(on_mizan, dict)
    assert on_mizan["حدث مهيّأ"] == 37 + 2  # 37 قالبَ فعل + أَفْعَلُ التفضيل وأَفْعُلٌ (كمضارع المتكلّم)
    assert on_mizan["حدث مجرّد"] >= 21 and on_mizan["كليّ عرضيّ"] >= 25
    assert read[("جزئيّ", "جزئيّ")] > 2000 and read[("حدث مهيّأ", "حدث مهيّأ")] > 1500
    assert read[("كليّ عرضيّ", "كليّ عرضيّ")] > 500 and read[("كليّ ماهويّ", "كليّ ماهويّ")] > 1500
    gen = str(ROOT_DIR / "tools" / "gen_kulli_index.py")
    res = subprocess.run([sys.executable, gen, "--check"], capture_output=True, text=True,
                         cwd=ROOT_DIR)
    assert res.returncode == 0, res.stderr
