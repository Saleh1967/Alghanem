"""الجملةُ الاسميّة: طرفان مرفوعان، رتبةٌ من الخانة، مطابقةٌ عمليّات، رابطٌ يُقرأ، والقياسُ على MASAQ.

التوقّعاتُ مستقلّةٌ عن الشيفرة: من الحصر المُرسَل (4 + 4 + الجواز، ومصفوفةُ المطابقة، وأربعةُ روابط)
وشواهدِ البوّابة؛ والطفرةُ (تبديلُ الموضع، تبديلُ العمليّة، كلمةٌ من غير الجدول) تُرفَض.
"""

from __future__ import annotations

from pathlib import Path

from slge.categories import PRONOUNS
from slge.cells import licensed
from slge.jumla import (
    WITNESSES,
    Jumla,
    admissible,
    agree,
    agree_loose,
    broken_plural,
    dual,
    gender,
    jam_f,
    jam_m,
    khabar_kind,
    lam,
    mubtada_kind,
    nakira,
    nominal,
    number,
    order,
    rabit,
    shibh_jumla,
    swap,
    ta_nith,
)
from slge.rawabit import cells_of
from slge.tawabi import case_class

SLICE = Path(__file__).parent / "data" / "masaq-jumla.json"


def test_both_sides_raf_and_kinds() -> None:
    j = nominal(cells_of("اَلْعِلْمَ"), cells_of("نُوْرَ"))
    assert case_class(j.mubtada) == "رفع" and case_class(j.khabar) == "رفع"
    assert j.mubtada == cells_of("اَلْعِلْمُ") and licensed(j.mubtada) and licensed(j.khabar)
    assert all(mubtada_kind(p) == "ضمير" for p in PRONOUNS)
    assert mubtada_kind(cells_of("اَلْعِلْمُ")) == "اسم" and mubtada_kind(cells_of("ذَا")) == "مبني"
    assert mubtada_kind(cells_of("اَلْعِلْمَ")) == "—"  # المنصوبُ لا يُقرأ مبتدأً
    assert khabar_kind(cells_of("نُوْرٌ")) == "مفرد" and khabar_kind(cells_of("دَرَسَ")) == "جملة فعلية"
    assert khabar_kind((*cells_of("فِي"), *cells_of("اَدَّارِ"))) == "شبه جملة"
    assert shibh_jumla(cells_of("لَهُمْ")) and shibh_jumla(cells_of("إِلَيْهِ"))
    assert shibh_jumla(cells_of("فَوْقَ"))
    assert not shibh_jumla(cells_of("كَرِيمُ"))  # الكافُ أصلٌ لا جارّة: الخانةُ لا تفرّق — باسمه


def test_order_is_read_from_cells_not_position() -> None:
    expected = {
        "فِي الدَّارِ رَجُلٌ": "تقديم الخبر", "أَيْنَ الْمَفَرُّ": "تقديم الخبر",
        "فِي الْمَدْرَسَةِ طُلَّابُهَا": "تقديم الخبر", "زَيْدٌ دَرَسَ": "تقديم المبتدأ",
        "أَخِي رَفِيقِي": "تقديم المبتدأ", "لَزَيْدٌ قَائِمٌ": "تقديم المبتدأ",
        "السَّلَامَةُ فِي التَّأَنِّي": "جواز",
    }
    for name, j in WITNESSES.items():
        assert order(j) == expected[name] and admissible(j), name
        assert order(swap(j)) == order(j) and swap(swap(j)) == j
        # الطفرة: تبديلُ الموضع يُرفض إلّا في الجواز
        assert admissible(swap(j)) == (expected[name] == "جواز"), name
    zayd, qaim = cells_of("زَيْدٌ"), cells_of("قَائِمٌ")
    assert order(Jumla(lam(zayd), qaim, True)) == "تقديم المبتدأ"
    assert not admissible(Jumla(lam(zayd), qaim, True))
    assert licensed(lam(zayd)) and nakira(zayd) and not nakira(cells_of("اَزَّيْدُ"))


def test_agreement_is_an_operation_and_an_exception() -> None:
    talib, mujtahid = cells_of("طَالِبُ"), cells_of("مُجْتَهِدُ")
    assert (gender(talib), number(talib)) == ("مذكر", "مفرد")
    for op, g, n in ((ta_nith, "مؤنث", "مفرد"), (dual, "مذكر", "مثنى"), (jam_m, "مذكر", "جمع"),
                     (jam_f, "مؤنث", "جمع")):
        assert (gender(op(talib)), number(op(talib))) == (g, n) and licensed(op(talib)), op.__name__
        assert agree(op(talib), op(mujtahid)), op.__name__
    assert gender(dual(ta_nith(talib))) == "مؤنث" and number(dual(ta_nith(talib))) == "مثنى"
    assert not agree(talib, ta_nith(mujtahid)) and not agree(dual(talib), jam_m(mujtahid))
    jibal, shahiqa = cells_of("اَلْجِبَالُ"), cells_of("شَاهِقَةُ")
    assert broken_plural(jibal) and not broken_plural(talib)
    assert not agree(jibal, shahiqa) and agree_loose(jibal, shahiqa)
    assert agree_loose(jibal, jam_f(shahiqa[:-2]))
    assert not agree_loose(talib, shahiqa)  # لا استثناءَ بلا جمع


def test_rabit_four_kinds_three_read() -> None:
    zayd = cells_of("زَيْدٌ")
    assert rabit(zayd, zayd) == "إعادة اللفظ" and rabit(zayd, cells_of("ذَلِكَ")) == "إشارة"
    assert rabit(zayd, cells_of("أَبُوْهُ")) == "ضمير" and rabit(zayd, cells_of("ءَامَنُوْ")) == "ضمير"
    assert rabit(zayd, cells_of("دَرَسَ")) == "—"  # الفاعلُ المستترُ لا خانةَ له؛ والعمومُ معنًى


def test_masaq_measurement_and_index() -> None:
    import subprocess
    import sys

    sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
    from gen_jumla_index import measure

    m = measure()
    rutba = m["rutba"]
    assert isinstance(rutba, dict)
    total = sum(rutba.values())
    ok = sum(v for (_, _, a), v in rutba.items() if a)
    assert total > 3000 and ok * 100 >= 85 * total  # الرتبةُ المقروءةُ تقبل موضعَ المصحف في ≥ 85%
    kh, mb = "الخبرُ أوّلًا", "المبتدأُ أوّلًا"
    assert rutba[("تقديم الخبر", kh, True)] > rutba[("تقديم الخبر", mb, False)]
    assert rutba[("تقديم المبتدأ", mb, True)] > 5 * rutba[("تقديم المبتدأ", kh, False)]
    ag = m["agree"]
    assert isinstance(ag, dict)
    matched = sum(v for (_, k), v in ag.items() if k == "مطابق")
    assert matched * 100 >= 80 * sum(ag.values())
    root = Path(__file__).parent.parent
    res = subprocess.run([sys.executable, str(root / "tools" / "gen_jumla_index.py"), "--check"],
                         capture_output=True, text=True, cwd=root)
    assert res.returncode == 0, res.stderr
