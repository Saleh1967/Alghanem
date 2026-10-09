"""تقسيماتُ النبهانيّ: توقّعاتٌ مستقلّةٌ عن الشيفرة من نصّ «أبحاث اللغة» المختوم — الأقسامُ الثلاثة وما
تحتها بأعدادها وأسمائها بترتيب النصّ، المركّبُ من الدالّ وحده، النِّسَبُ الثلاث بلا «تضمينيّة»، والترجيحُ
بعشرة أوجه؛ وطفراتٌ مرفوضة (بحثٌ مفقود، عبارةٌ لا ترد في بحثها، ترتيبٌ مقلوب)."""

from __future__ import annotations

import gzip
import hashlib
from itertools import combinations
from pathlib import Path

from slge.nabhani import (
    DALALA,
    DALL_MADLUL,
    IHTIMAL,
    MADLUL,
    MURAKKAB,
    NISBA,
    RANK,
    TARKIB,
    awla,
    tarjih,
)
from slge.nabhani_table import SECTIONS, phrases

DATA = Path(__file__).parent / "data"


def test_sealed_text_and_every_section_anchored_in_it() -> None:
    raw = gzip.decompress((DATA / "nabhani-shakhsiyya-3.txt.gz").read_bytes())
    assert hashlib.sha256(raw).hexdigest().startswith("359bb553")
    lines = raw.decode("utf-8").split("\n")
    keys = [k for k, _, _ in SECTIONS]
    assert len(keys) == 20 and len(set(keys)) == 20 and keys[-1] == "التفكير-المعلومات-السابقة"
    j3 = [(k, n, ph) for k, n, ph in SECTIONS if k != "التفكير-المعلومات-السابقة"]
    assert [n for _, n, _ in j3] == sorted(n for _, n, _ in j3)  # بترتيب النصّ
    for i, (k, n, ph) in enumerate(j3):
        end = j3[i + 1][1] - 1 if i + 1 < len(j3) else n + 29
        body = "\n".join(lines[n - 1:end])
        assert all(p in body for p in ph), k
    # الطفرة: عبارةٌ من بحثٍ آخر لا ترد في بحث «الفعل»
    fil = next(n for k, n, _ in SECTIONS if k == "الفعل")
    assert "الاشتراك، والنقل، والمجاز" not in "\n".join(lines[fil - 1:fil + 40])


def test_three_divisions_with_their_members_in_text_order() -> None:
    assert DALALA == ("دلالة المطابقة", "دلالة التضمن", "دلالة الالتزام")
    assert TARKIB == ("تركيب إسناد", "تركيب مزج", "تركيب إضافة")
    assert MURAKKAB == ("الاستفهام", "الأمر", "الالتماس", "السؤال", "الخبر", "التنبيه")
    assert phrases("المركب")[0] == "من أقسام الدال وحده"  # الخبرُ والإنشاءُ في جبر الدالّ
    assert len(MADLUL) == 5 and MADLUL[-1] == "لفظاً مركباً مهملاً"
    assert "الهذيان" in phrases("المدلول-وحده")
    assert DALL_MADLUL == ("المنفرد", "المتباين", "المترادف", "المشترك", "المنقول", "الحقيقة",
                           "المجاز")
    assert NISBA == ("الإسنادية", "التقييدية", "الإضافية")
    assert "تضمين" not in " ".join(phrases("الوضع-والنسب"))
    # السببيّةُ أربعة أقسام، والمجازُ بالذات في اسم الجنس لا في الحرف ولا العلم
    m = phrases("علاقات-المجاز")
    assert sum(p.startswith("السببية") or p.startswith("الســببية") for p in m) == 4
    assert "المجاز بالذات إنما يكون في اسم الجنس" in m and "ثالثها: العلم" in m


def test_tarjih_is_the_ten_rules_of_the_text() -> None:
    rules = phrases("الترجيح")[2:]
    assert len(rules) == 10
    for r in rules:
        if " أولى من " in r:
            a, b = r.split(" أولى من ")
            assert awla(a, b) and not awla(b, a), r
        else:
            assert r == "الإضمار مثل المجاز" and RANK["الإضمار"] == RANK["المجاز"]
    # كلُّ زوجٍ من الخمسة: أولى أحدُهما أو سيّان، والسيّان المجازُ والإضمارُ فقط
    ties = [(a, b) for a, b in combinations(IHTIMAL, 2) if not awla(a, b) and not awla(b, a)]
    assert ties == [("المجاز", "الإضمار")]
    assert all(awla("التخصيص", x) for x in IHTIMAL if x != "التخصيص")
    assert all(awla(x, "الاشتراك") for x in IHTIMAL if x != "الاشتراك")
    assert tarjih(IHTIMAL) == ("التخصيص", "المجاز", "الإضمار", "النقل", "الاشتراك")
    assert len(tarjih(IHTIMAL)) == 5  # لا يُسقَط احتمال


def test_mutants_are_refused() -> None:
    assert phrases("بحثٌ لا وجودَ له") == ()
    assert not awla("الاشتراك", "النقل") and not awla("النقل", "المجاز")
    assert "التضمينية" not in NISBA
