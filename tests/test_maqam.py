"""المقام: الشخصُ من الخانة، المستترُ لا خانةَ له، الظاهرُ للغائب، التوكيدُ مطابقة، والقياسُ على MASAQ.

التوقّعاتُ من الحصر المُرسَل (الاستتارُ والظهورُ والتوكيد) مصحَّحةً بالنحو (الغائبُ يستتر جوازًا) وشواهدِ
البوّابة، والطفرةُ (اسمٌ ظاهرٌ بعد متكلّم، توكيدٌ متقاطعُ الشخص، صدرٌ يقرأ غيرَ شخصه) تُرفَض.
"""

from __future__ import annotations

from pathlib import Path

from slge.categories import PRONOUNS
from slge.filiyya import has_subject
from slge.maqam import (
    DETACHED,
    PRESENT_TEMPLATES,
    hukm_istitar,
    shakhs,
    shakhs_detached,
    tawkid,
    valid,
    with_prefix,
    zuhur,
)
from slge.rawabit import cells_of
from slge.wazn import AWZAN, fill

ROOT_DIR = Path(__file__).resolve().parent.parent


def test_prefix_reads_person_for_every_present_template_and_root() -> None:
    roots = (("د", "ر", "س"), ("ك", "ت", "ب"), ("ن", "ص", "ر"), ("ض", "ر", "ب"), ("ع", "ل", "م"))
    for k in PRESENT_TEMPLATES:
        for r in roots:
            m = fill(AWZAN[k].template, r)
            got = [shakhs(with_prefix(p, m)) for p in "ءنتي"]
            assert got == ["متكلم", "متكلم", "مخاطب/غائبة", "غائب"], (k, r)
            assert shakhs(with_prefix("ب", m)) is None  # الطفرة: صدرٌ ليس من الأربعة
    assert shakhs(cells_of("دَرَسَتْ")) == "غائب" and shakhs(cells_of("اُدْرُسْ")) == "مخاطب"
    assert shakhs(cells_of("يَدْرُسُونَ")) == "غائب" and shakhs(cells_of("تَدْرُسِينَ")) == "مخاطب"
    assert shakhs(cells_of("قُمْتُ")) == "متكلم" and shakhs(cells_of("زَيْدٌ")) is None


def test_concealed_has_no_cell_and_explicit_only_for_ghaib() -> None:
    for w, s in (("أَدْرُسُ", "متكلم"), ("دَرَسَ", "غائب"), ("يَدْرُسُ", "غائب"), ("نَكْتُبُ", "متكلم")):
        c = cells_of(w)
        assert shakhs(c) == s and not has_subject(c), w
    assert has_subject(cells_of("ضَرَبْتُ")) and shakhs(cells_of("ضَرَبْتُ")) == "متكلم"
    assert hukm_istitar("متكلم") == "وجوب" == hukm_istitar("مخاطب")
    assert hukm_istitar("غائب") == "جواز" and hukm_istitar("مخاطب/غائبة") is None
    assert valid("غائب", "ظاهر") and valid("مخاطب/غائبة", "ظاهر")
    assert not valid("متكلم", "ظاهر") and not valid("مخاطب", "ظاهر")  # الطفرة
    assert all(valid(s, z) for s in ("متكلم", "مخاطب", "غائب") for z in ("متصل", "مستتر"))
    zayd, darasa = cells_of("زَيْدٌ"), cells_of("دَرَسَ")
    assert zuhur(darasa, zayd) == "ظاهر" and zuhur(darasa, cells_of("اَدَّرْسَ")) == "مستتر"
    assert zuhur(cells_of("ضَرَبْتُ"), zayd) == "متصل"


def test_emphasis_requires_same_person() -> None:
    ana, anta, huwa, hiya = (cells_of(w) for w in ("أَنَا", "أَنْتَ", "هُوَ", "هِيَ"))
    darabtu, adrusu, darasa, tadrusu = (cells_of(w) for w in ("ضَرَبْتُ", "أَدْرُسُ", "دَرَسَ", "تَدْرُسُ"))
    assert tawkid(darabtu, ana) and tawkid(adrusu, ana) and tawkid(darasa, huwa)
    assert tawkid(tadrusu, anta) and tawkid(tadrusu, hiya)
    assert not tawkid(darabtu, anta) and not tawkid(adrusu, huwa) and not tawkid(darasa, ana)
    assert not tawkid(darasa, cells_of("زَيْدٌ")) and not tawkid(cells_of("زَيْدٌ"), huwa)
    assert len(DETACHED) == len(PRONOUNS) == 12
    assert [shakhs_detached(p) for p in PRONOUNS] == list(DETACHED)
    # لكلّ منفصلٍ فعلٌ يوافقه
    verbs = {"متكلم": darabtu, "مخاطب": cells_of("ضَرَبْتَ"), "غائب": darasa}
    assert all(tawkid(verbs[s], p) for p, s in zip(PRONOUNS, DETACHED, strict=True))


def test_masaq_measurement_and_index() -> None:
    import subprocess
    import sys

    sys.path.insert(0, str(ROOT_DIR / "tools"))
    from gen_maqam_index import measure

    m = measure()
    person, attach, zahir = m["person"], m["attach"], m["zahir"]
    assert isinstance(person, dict) and isinstance(attach, dict) and isinstance(zahir, dict)
    assert person["وافق"] >= 10 * person["خالف"] and person["وافق"] > 500
    assert attach["وافق"] > 0.8 * (attach["وافق"] + attach["خالف"])
    assert zahir["غائب"] > 50 * zahir["حاضر"] and zahir["حاضر"] < 15
    gen = str(ROOT_DIR / "tools" / "gen_maqam_index.py")
    res = subprocess.run([sys.executable, gen, "--check"], capture_output=True, text=True,
                         cwd=ROOT_DIR)
    assert res.returncode == 0, res.stderr
