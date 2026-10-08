"""العلمُ ولفظُ الجلالة (بتوقيع المالك): توقّعاتٌ مستقلّةٌ عن الشيفرة — لفظٌ منفردٌ بلا قياس، يُردّ
بعينه؛ الجلالةُ ثلاثُ صورٍ بموضعها واللهمّ منفرد؛ الممنوعُ بالفتح «نصب/جرّ» والمنصرفُ بالتنوين والمقصورُ
بلا حالة — وطفراتٌ مرفوضة (قالبٌ لا علم؛ بترٌ؛ همزةٌ بعد سابقة؛ تنوينُ الممنوع؛ لاحقةٌ غيرُ موقَّعة)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from slge.alam import ALAM, ALAM_PROCLITICS, JALALA_FORMS, case_of, ilm, restore
from slge.alam_table import SIGNED_BY
from slge.cells import licensed
from slge.rawabit import cells_of

DATA = Path(__file__).parent / "data" / "owner-alam.json"


def test_deposit_is_owner_signed_and_the_tables_mirror_it() -> None:
    raw = DATA.read_bytes()
    assert hashlib.sha256(raw).hexdigest().startswith("09290ebb")
    d = json.loads(raw)
    assert d["signed_by"] == SIGNED_BY and "بتوقيع المالك" in SIGNED_BY
    assert len(d["alam"]) == len(ALAM) == 57
    assert [it["rasm"] for it in d["alam"]] == [r for r, *_ in ALAM]
    kinds = {it["kind"] for it in d["alam"]}
    sarfs = {it["sarf"] for it in d["alam"]}
    assert kinds == {"عربي", "أعجمي"} and sarfs == {"ممنوع", "منصرف", "مقصور", "غير مشهود الجرّ"}
    assert {it["rasm"] for it in d["alam"]} & set(d["excluded_by_name"]) == set()
    # كلُّ علمٍ مرخَّصٌ بفتح آخره، والمقصورُ وحدَه آخرُه ألفٌ ساكنة
    for _, head, last, fixed, _, sarf in ALAM:
        assert licensed((*head, (last, "فتح")))
        assert (sarf == "مقصور") == (last == "ا" and fixed == "سكون")


def test_jalala_has_ten_named_forms_in_their_places_and_lahumma_alone() -> None:
    # سوابقُ الجذع الثماني (و ف ب ل ك س ء لَ) وتاءُ القسم
    assert len(JALALA_FORMS) == 10 and len(ALAM_PROCLITICS) == 9
    assert (("ت", "فتح"),) in ALAM_PROCLITICS
    for word, form, pre, case in (
        ("ءَلْلَهُ", "INITIAL", "", "رفع"),
        ("ءَلْلَهَ", "INITIAL", "", "نصب"),
        ("ءَلْلَهِ", "INITIAL", "", "جرّ"),
        ("بِلْلَهِ", "AFTER_PREFIX", "ب", "جرّ"),
        ("وَلْلَهُ", "AFTER_PREFIX", "و", "رفع"),
        ("لِلْلَهِ", "AFTER_PREFIX", "ل", "جرّ"),
        ("فَلْلَهُ", "AFTER_PREFIX", "ف", "رفع"),
        ("تَالْلَهِ", "MADD", "ت", "جرّ"),
        ("ءَلْلَهُمْمَ", "LAHUMMA", "", "لا تقرؤه الخانة"),
    ):
        w = cells_of(word)
        ms = [m for m in ilm(w) if m.kind == "جلالة"]
        assert ms and all(restore(m) == w for m in ms), word
        assert any(m.form == form and m.case == case and m.sarf == "منفرد"
                   and "".join(k for p in m.pre for k, _ in p) == pre for m in ms), (word, ms)
    # ابتداءً قراءةٌ واحدةٌ لا شبيهَ لها
    assert len(ilm(cells_of("ءَلْلَهُ"))) == 1


def test_proper_nouns_read_their_case_from_the_last_cell() -> None:
    for word, rasm, sarf, kind, case in (
        ("إِبْرَاهِيمَ", "ءبراهيم", "ممنوع", "عربي", "نصب/جرّ"),
        ("إِبْرَاهِيمُ", "ءبراهيم", "ممنوع", "عربي", "رفع"),
        ("فِرْعَوْنَ", "فرعون", "ممنوع", "أعجمي", "نصب/جرّ"),
        ("فِرْعَوْنُ", "فرعون", "ممنوع", "أعجمي", "رفع"),
        ("نُوحٍ", "نوح", "منصرف", "أعجمي", "جرّ"),
        ("نُوحًا", "نوح", "منصرف", "أعجمي", "نصب"),
        ("مُوسَى", "موسا", "مقصور", "أعجمي", "لا تقرؤه الخانة"),
        ("لِفِرْعَوْنَ", "فرعون", "ممنوع", "أعجمي", "نصب/جرّ"),
        ("وَإِبْرَاهِيمَ", "ءبراهيم", "ممنوع", "عربي", "نصب/جرّ"),
    ):
        w = cells_of(word)
        ms = ilm(w)
        assert ms and all(restore(m) == w for m in ms), word
        assert any(m.rasm == rasm and m.sarf == sarf and m.kind == kind and m.case == case
                   for m in ms), (word, ms)
    assert case_of("ممنوع", "فتح", False) == "نصب/جرّ" == case_of("غير مشهود الجرّ", "فتح", False)
    assert case_of("منصرف", "فتح", True) == "نصب"
    assert case_of("غير مشهود الجرّ", "فتح", True) == "نصب"
    assert case_of("مقصور", "سكون", False) == "لا تقرؤه الخانة"


def test_mutants_are_refused() -> None:
    # قالبٌ لا علم؛ وبترُ الآخر؛ وما ليس في الموقَّع
    assert not ilm(cells_of("كَتَبَ")) and not ilm(cells_of("ذَهَبَ"))
    assert not ilm(cells_of("ءَلْلَهُ")[:-1]) and not ilm(cells_of("إِبْرَاهِيمَ")[:-1])
    assert not ilm(cells_of("عَلَيَّ")) and not ilm(cells_of("ءَلْمَلِكُ"))
    # الهمزةُ لا تبقى بعد سابقة (بِءَلْلَهِ)؛ ولا ابتداءَ بساكن (لْلَهِ)؛ ولا مدَّ بلا تاءِ قسمٍ أو همزة
    assert not ilm(cells_of("بِءَلْلَهِ")) and not ilm(cells_of("لْلَهِ"))
    assert not [m for m in ilm(cells_of("وَالْلَهِ")) if m.form == "MADD"]
    # الممنوعُ لا يُنوَّن، والمقصورُ لا يُنوَّن هنا، وتنوينُ غير الآخر لا يُقرأ
    assert not ilm(cells_of("فِرْعَوْنٍ")) and not ilm(cells_of("إِبْرَاهِيمًا"))
    assert not ilm(cells_of("مُوسًى"))
    # لاحقةٌ غيرُ موقَّعة (الضمير) ليست من هذا القارئ
    assert not ilm(cells_of("إِبْرَاهِيمَهُ"))
