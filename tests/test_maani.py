"""معاني الحروف: الجدولُ منقولٌ من المصدر بترتيبه، والترتيبُ بالقرينة لا يُسقط معنًى — توقّعاتُه من
المصدر (مبحث الحرف في الشخصيّة ج3) لا من الشيفرة، وطفراتُه مرفوضةٌ بأسمائها."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys

from conftest import ROOT
from slge.huruf import TABLE as HURUF
from slge.maani import GHAYA, MULTI, is_zarf, jarr_uncovered, rank, senses_of
from slge.maani_table import SENSES, TABLE
from slge.zaman import STEMS as ZAMAN
from slge.zaman import forms_of
from slge.zuruf import STEMS as ZURUF
from slge.zuruf import jarr

DEPOSIT = ROOT / "tests" / "data" / "nabhani-huruf.json"


def test_deposit_is_sealed_and_tables_are_generated_from_it() -> None:
    sha = hashlib.sha256(DEPOSIT.read_bytes()).hexdigest()
    assert sha == "5f6f3d64736e981a867524d7478ab1773670033d2a229f8aefcbbaf4905f4766"
    dep = json.loads(DEPOSIT.read_text(encoding="utf-8"))
    assert len(dep["entries"]) == 25 and len(dep["skipped"]) == 4
    assert all(e["unmatched"] == [] for e in dep["entries"]), "عبارةٌ لم تُلتقط: لا تخمين"
    assert {s["name"] for s in dep["senses"]} == set(SENSES)
    res = subprocess.run([sys.executable, str(ROOT / "tools" / "deposit_maani.py"), "--check"],
                         capture_output=True, text=True, cwd=ROOT)
    assert res.returncode == 0, res.stdout + res.stderr


def test_table_follows_the_source_order() -> None:
    """المصدر: «من» لابتداء الغاية، وللتبعيض، ولبيان الجنس، وزائدة — بهذا الترتيب؛ «الباء» سبعةٌ
    أوّلُها الإلصاق وآخرُها زائدة؛ «في» الظرفيّة ثمّ بمعنى على ثمّ التجوّز؛ «أو» أربعة؛ «لا» النافية
    ثلاثة."""

    assert senses_of(5) == ("ابتداء الغاية", "التبعيض", "بيان الجنس", "زائدة")
    assert senses_of(0)[0] == "الإلصاق" and senses_of(0)[-1] == "زائدة" and len(senses_of(0)) == 7
    assert senses_of(9) == ("الظرفية", "بمعنى على", "التجوّز")
    assert senses_of(6) == senses_of(10) == ("انتهاء الغاية", "بمعنى مع")
    assert senses_of(53) == ("تعليق الحكم بأحد المذكورين", "الشك", "التخيير", "الإباحة")
    assert senses_of(61) == ("نفي المستقبل", "النهي", "الدعاء")
    assert senses_of(3) == senses_of(4) == ("القسم",)
    assert MULTI == (0, 1, 5, 6, 9, 10, 52, 53, 61)
    assert jarr_uncovered() == (13, 14, 15)
    assert [HURUF[i].name for i in jarr_uncovered()] == ["خَلَا", "عَدَا", "حَاشَا"]
    # الأصلُ أوّلًا: حيث ذكر المصدرُ غايةً ذكرها أوّلًا
    for h, ss in TABLE.items():
        names = [SENSES[i] for i in ss]
        if any(n in GHAYA for n in names):
            assert names[0] in GHAYA, h


def test_rank_by_clue_keeps_every_sense() -> None:
    for h in TABLE:
        ss = senses_of(h)
        for nafy in (False, True):
            for zarf in (False, True):
                r = rank(ss, nafy_before=nafy, zarf_after=zarf)
                assert sorted(r) == sorted(ss) and len(r) == len(ss)
        assert rank(ss) == ss
    assert rank(senses_of(5), nafy_before=True) == (
        "زائدة", "ابتداء الغاية", "التبعيض", "بيان الجنس")
    assert rank(senses_of(5), nafy_before=True, zarf_after=True) == senses_of(5)
    assert rank(senses_of(9), zarf_after=True) == senses_of(9)


def test_zarf_clue_is_the_two_proven_tables() -> None:
    assert is_zarf(jarr(ZURUF[0].stem)) and all(is_zarf(f) for f in forms_of(ZAMAN["يَوْم"]))
    assert not is_zarf(HURUF[5].cells) and not is_zarf(())


def test_mutations_are_refused() -> None:
    # (١) طفرةُ الترتيب: ترتيبٌ يخالف المصدر مرفوض
    assert senses_of(5) != ("التبعيض", "ابتداء الغاية", "بيان الجنس", "زائدة")
    # (٢) طفرةُ الإسقاط: ترتيبٌ يُسقط معنًى ليس ترتيبًا
    dropped = tuple(s for s in senses_of(0) if s != "زائدة")
    assert sorted(dropped) != sorted(rank(senses_of(0), nafy_before=True))
    # (٣) طفرةُ الاختيار: لا معنى لحرفٍ لم يذكره المصدر — خلا/عدا/حاشا فارغة لا «استثناء»
    assert senses_of(13) == () and "الاستثناء" not in SENSES
    # (٤) طفرةُ المودَع: تغييرُ بايتٍ واحد يُسقط البصمة
    raw = bytearray(DEPOSIT.read_bytes())
    raw[-2] ^= 1
    assert hashlib.sha256(bytes(raw)).hexdigest() != \
        "5f6f3d64736e981a867524d7478ab1773670033d2a229f8aefcbbaf4905f4766"


def test_numbers_on_masaq() -> None:
    """الأرقامُ من `MAANI_INDEX.md` المولَّد: 7,369 وقوعًا لحرفٍ له معانٍ؛ القرينتان غيّرتا الترتيب في 8
    فقط (مِنْ 2، بِ 6)؛ وشواهدُ المصدر غيرُ الأولى: يقدّمها الترتيبُ في 1 من 5 — دينٌ باسمه لا نجاحٌ."""

    text = (ROOT / "MAANI_INDEX.md").read_text(encoding="utf-8")
    assert "وقع حرفٌ له معانٍ 7,369 مرّةً" in text
    assert "| مِنْ | 1,670 | 298 | 2 | 2 |" in text and "| بِ | 2,041 | 20 | 6 | 6 |" in text
    assert "في 1 من 5 شواهدَ" in text
