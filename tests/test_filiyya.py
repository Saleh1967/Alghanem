"""الجملةُ الفعليّة: الفعلُ ثلاثُ حالات، الفاعلُ ثلاثُ صور، رتبةٌ من الخانة، نيابةٌ عمليّتان، مفاعيلُ نصب.

التوقّعاتُ من الحصر المُرسَل (أ/ب/ج والجواز، صورُ النائب الأربع، المفاعيلُ الأربعة) وشواهدِ البوّابة؛
والطفرةُ (تبديلُ الموضع، لاحقةٌ بغير حالتها، مصدرٌ بغير جذر الفعل) تُرفَض.
"""

from __future__ import annotations

from pathlib import Path

from slge.cells import licensed
from slge.filiyya import (
    MASDAR_TEMPLATES,
    WITNESSES,
    Filiyya,
    admissible,
    amr_ends_like_jazm,
    fail,
    has_object,
    has_subject,
    maful,
    maiyya,
    majhul,
    majhul_pres,
    mutlaq,
    naib,
    naib_kind,
    order,
    past,
    past_ending,
    sort_fadla,
    tafaala,
    verb_root,
)
from slge.rawabit import cells_of
from slge.tawabi import case_class
from slge.wazn import AWZAN, fill

SLICE = Path(__file__).parent / "data" / "masaq-filiyya.json.gz"


def test_verb_three_states_and_subject_three_forms() -> None:
    kataba = cells_of("كَتَبَ")
    assert past_ending(()) == "فتح" and past_ending(cells_of("تُ")) == "سكون"
    assert past_ending(cells_of("وْ")) == "ضم" and past_ending(cells_of("نَا")) == "سكون"
    for suf, word in ((cells_of("تُ"), "كَتَبْتُ"), (cells_of("وْ"), "كَتَبُوْ"), (cells_of("نَا"), "كَتَبْنَا"),
                      ((), "كَتَبَ")):
        assert past(kataba, suf) == cells_of(word) and licensed(past(kataba, suf)), word
    assert amr_ends_like_jazm()
    assert case_class(fail(cells_of("اَلْمُجْتَهِدَ"))) == "رفع"
    assert has_subject(cells_of("كَتَبْتُ")) and has_subject(cells_of("يَكْتُبُوْنَ"))
    assert not has_subject(cells_of("سَكَنَ"))  # نونُ الأصل بعد فتح لا نونُ النسوة
    assert not has_subject(cells_of("كَتَبَتُ"))  # الطفرة: التاءُ بعد فتحٍ ليست فاعلًا
    assert has_object(cells_of("أَكْرَمَنِي")) and not has_subject(cells_of("أَكْرَمَنِي"))
    assert has_object(cells_of("أَكْرَمَكَ")) and not has_object(cells_of("كَتَبْتُ"))


def test_order_from_cells_and_mutation_refused() -> None:
    expected = {
        "كَتَبْتُ الدَّرْسَ": "الفاعل أولًا", "ضَرَبَ مُوسَى عِيسَى": "الفاعل أولًا",
        "سَكَنَ الدَّارَ صَاحِبُهَا": "المفعول أولًا", "أَكْرَمَنِي أَبُوكَ": "المفعول أولًا",
        "أَيَّ رَجُلٍ قَابَلْتَ": "المفعول قبل الفعل", "أَكَلَ زَيْدٌ تُفَّاحَةً": "جواز",
    }
    for name, j in WITNESSES.items():
        assert order(j) == expected[name] and admissible(j), name
        for pos in ("ف س١ س٢", "ف س٢ س١", "س٢ ف س١"):
            k = Filiyya(j.fil, j.fail, j.maful, pos)
            assert order(k) == order(j)  # الرتبةُ من الخانات لا من الموضع
            assert admissible(k) == (expected[name] == "جواز" or pos == j.pos), (name, pos)


def test_passive_two_state_operations_and_naib() -> None:
    root = ("ك", "ت", "ب")
    assert majhul(fill(AWZAN[0].template, root)) == fill(AWZAN[3].template, root) == cells_of("كُتِبَ")
    assert majhul_pres(fill(AWZAN[4].template, root)) == fill(AWZAN[7].template, root)
    assert majhul_pres(cells_of("يَكْتُبُ")) == cells_of("يُكْتَبُ")
    assert licensed(majhul(cells_of("كَتَبَ"))) and naib(cells_of("اَدَّرْسَ")) == fail(cells_of("اَدَّرْسَ"))
    assert naib_kind(cells_of("اَرَّجُلُ")) == "مفعول به" and naib_kind(cells_of("يَوْمُ")) == "ظرف"
    assert naib_kind((*cells_of("فِي"), *cells_of("اَلْأَمْرِ"))) == "مجرور"
    assert naib_kind(cells_of("فَهْمٌ")) == "مصدر" and naib_kind(cells_of("اَدَّرْسُ")) == "مصدر"  # معجم


def test_four_objects() -> None:
    assert case_class(maful(cells_of("دَرْسُ"))) == "نصب"
    assert maful(cells_of("دَرْسُ")) == cells_of("دَرْسًا")
    assert sort_fadla(cells_of("رَغْبَةً"), cells_of("دَرَسْتُ")) == "مفعول لأجله"
    assert sort_fadla(cells_of("إِجْلَالًا"), cells_of("قُمْتُ")) == "مفعول لأجله"
    assert sort_fadla(cells_of("رَاغِبًا"), cells_of("قُمْتُ")) == "حال"
    assert sort_fadla(cells_of("ضَرْبًا"), cells_of("ضَرَبْتُ")) == "مفعول مطلق"
    assert sort_fadla(cells_of("ضَرْبًا"), cells_of("قُمْتُ")) == "مفعول لأجله"  # الطفرة: غيرُ جذر الفعل
    assert verb_root(cells_of("ضَرَبْتُ")) == ("ض", "ر", "ب") and verb_root(cells_of("قُمْتُ")) is None
    assert mutlaq(29, ("ض", "ر", "ب")) == cells_of("ضَرْبًا") and 63 in MASDAR_TEMPLATES
    nahr = cells_of("اَنَّهْرُ")
    assert maiyya(nahr) == (("و", "فتح"), *cells_of("اَنَّهْرَ")) and licensed(maiyya(nahr))
    assert tafaala(cells_of("تَخَاصَمَ")) and not tafaala(cells_of("سَارَ"))


def test_masaq_measurement_and_index() -> None:
    import subprocess
    import sys

    sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
    from gen_filiyya_index import measure

    m = measure()
    rutba = m["rutba"]
    assert isinstance(rutba, dict)
    total = sum(rutba.values())
    ok = sum(v for (_, _, a), v in rutba.items() if a)
    assert total > 16000 and ok * 100 >= 90 * total
    subj = m["subj"]
    assert isinstance(subj, dict)
    agreed = sum(v for (_, b), v in subj.items() if b)
    assert agreed * 100 >= 85 * sum(subj.values())
    endings = m["endings"]
    assert isinstance(endings, dict)
    assert sum(v for (a, b), v in endings.items() if a == b) * 100 >= 85 * sum(endings.values())
    root = Path(__file__).parent.parent
    res = subprocess.run([sys.executable, str(root / "tools" / "gen_filiyya_index.py"), "--check"],
                         capture_output=True, text=True, cwd=root)
    assert res.returncode == 0, res.stderr
