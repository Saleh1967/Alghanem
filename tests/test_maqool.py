"""المعقوليّة على معايير النبهانيّ المختومة (ADR ٤٩): المراحلُ الأربع من خطّة المالك.

١. المعايير (`mayaatir_table`): أسطرُها بأيدينا من قراءة الكتب المختومة، وكلُّ عبارةٍ في سطرها
   بعينه، وما نُسب في الخطّة الواردة ولم يَرِد بلفظه غائبٌ عن الكتب الثلاثة؛ وطفرةُ سطرٍ تُلتقط.
٢. الحكمُ الثلاثيّ (`maqool`): سبعَ عشرةَ حجّةً معلومةَ الحكم سلفًا مكتوبةً هنا باليد، وأحكامُها
   هنا باليد؛ وجدولُ Lean (`formal/out/maqool.csv`، `Maqool.cases_verdicts`) يطابقها؛ وأربعُ
   طفراتٍ بأسمائها تُلتقط.
٣. بطاقةُ الحوار: لا مادّةَ بلا بطاقةٍ تامّة، والمقبولُ معلومةٌ سابقةٌ لا رأي.
٤. الطيّ في «ز»: الثلاثةُ مجموعُها عددُ الحجج، وكلُّ صفٍّ في «ز» يحمل بابَه بعينه.
"""

from __future__ import annotations

import gzip
from collections.abc import Callable
from dataclasses import replace

import pytest

from conftest import ROOT
from slge.maqool import (
    ANCHOR,
    Bitaqa,
    Hujja,
    Hukm,
    Jawla,
    Sabiqa,
    Shahid,
    admit,
    archive,
    door,
    judge,
    judge_rounds,
)
from slge.mayaatir_table import ABSENT, CRITERIA

DATA = ROOT / "tests" / "data"
BOOK_FILE = {"tafkir": "nabhani-tafkir.txt.gz", "shakhsiyya-1": "nabhani-shakhsiyya-1.txt.gz",
             "shakhsiyya-3": "nabhani-shakhsiyya-3.txt.gz"}
LINES_BY_HAND = {"U1": ("tafkir", 32), "U2": ("tafkir", 37), "U3": ("shakhsiyya-1", 45),
                 "U4": ("shakhsiyya-3", 483), "U5": ("tafkir", 241), "U6": ("tafkir", 71),
                 "U7": ("shakhsiyya-3", 397), "U8": ("tafkir", 38), "M1": ("tafkir", 72),
                 "M2": ("tafkir", 73)}
"""مواضعُ المعايير كما وجدناها بقراءة الكتب المختومة قبل كتابة الأداة."""


def _book(name: str) -> list[str]:
    return gzip.decompress((DATA / BOOK_FILE[name]).read_bytes()).decode("utf-8").split("\n")


def test_criteria_lines_by_hand() -> None:
    assert {k: (b, ln) for k, _, b, ln, _ in CRITERIA} == LINES_BY_HAND


def test_every_phrase_is_in_its_line_and_absent_claims_are_absent() -> None:
    books = {b: _book(b) for b in BOOK_FILE}
    for key, _, b, ln, phrases in CRITERIA:
        assert phrases and all(p in books[b][ln - 1] for p in phrases), key
    for key, phrase in ABSENT:
        assert not any(phrase in line for lines in books.values() for line in lines), key
    # طفرة `MUTANT_LINE_SHIFTED`: سطرٌ بعد سطره لا يحمل عباراته
    assert not all(all(p in books[b][ln] for p in ph) for _, _, b, ln, ph in CRITERIA)


BASE = Hujja(claim=1, kind="wujud", shahid=Shahid("makhtum", 32), presented=7, judged_on=7, mawdu=5,
             prem_topics=(5,), sabiqa=(Sabiqa(2),))

CASES: tuple[tuple[str, Hujja, Hukm], ...] = (
    ("c01_wujud_sound", BASE, Hukm("maqool", "qati")),
    ("c02_haqiqa_sound", replace(BASE, kind="haqiqa"), Hukm("maqool", "zanni")),
    ("c03_self_premise", replace(BASE, sabiqa=(Sabiqa(2, deps=(1,)),)), Hukm("ghayr", "dawar")),
    ("c04_cycle_two", replace(BASE, sabiqa=(Sabiqa(2, deps=(3,)), Sabiqa(3, deps=(2,)))),
     Hukm("ghayr", "dawar")),
    ("c05_ray", replace(BASE, sabiqa=(Sabiqa(2, ray=True),)), Hukm("ghayr", "ray_mutanakkir")),
    ("c06_ad_hominem", replace(BASE, prem_topics=(5, 9)), Hukm("ghayr", "khuruj_mawdu")),
    ("c07_straw_man", replace(BASE, judged_on=8), Hukm("ghayr", "tahrif_waqi")),
    ("c08_tajrid", replace(BASE, khabar=True, with_circumstances=False), Hukm("ghayr", "tajrid")),
    ("c09_taamim", replace(BASE, khabar=True, covered=(10, 11), witnessed=(10,)),
     Hukm("ghayr", "taamim")),
    ("c10_shumuli", replace(BASE, khabar=True, shumuli=True), Hukm("ghayr", "qiyas_shumuli")),
    ("c11_u5_outside_khabar", replace(BASE, with_circumstances=False, covered=(10, 11),
                                      witnessed=(10,), shumuli=True), Hukm("maqool", "qati")),
    ("c12_no_witness", replace(BASE, shahid=None), Hukm("la_hukm", "bila_shahid")),
    ("c13_card_witness", replace(BASE, shahid=Shahid("bitaqa", 4)),
     Hukm("la_hukm", "shahid_bitaqa")),
    ("c14_cycle_no_witness", replace(BASE, shahid=None, sabiqa=(Sabiqa(2, deps=(1,)),)),
     Hukm("ghayr", "dawar")),
    ("c15_khabar_sound", replace(BASE, khabar=True, covered=(10,), witnessed=(10,)),
     Hukm("maqool", "qati")),
    ("c16_cycle_three", replace(BASE, sabiqa=(Sabiqa(2, deps=(3,)), Sabiqa(3, deps=(4,)),
                                              Sabiqa(4, deps=(2,)))), Hukm("ghayr", "dawar")),
    ("c17_chain_no_cycle", replace(BASE, sabiqa=(Sabiqa(2, deps=(3,)), Sabiqa(3, deps=(4,)),
                                                 Sabiqa(4),)), Hukm("maqool", "qati")),
)


def test_known_verdicts() -> None:
    assert len(CASES) >= 10
    for name, h, expected in CASES:
        assert judge(h) == expected, name


def test_lean_table_agrees() -> None:
    rows = (ROOT / "formal" / "out" / "maqool.csv").read_text(encoding="utf-8").split()
    expected = [f"{n},{j.tag},{j.value},{'U8' if j.tag == 'maqool' else ANCHOR[j.value]}"
                for n, _, j in CASES]
    assert rows == expected


def test_refusal_never_from_absence() -> None:
    for name, h, _ in CASES:
        for s in (None, Shahid("makhtum", 1), Shahid("bitaqa", 1)):
            assert door(replace(h, shahid=s)) == door(h), name
            if s is None:
                assert judge(replace(h, shahid=s)).tag != "maqool", name


def _binary(h: Hujja) -> Hukm:
    """`MUTANT_BINARY`: لا «لا حكم» — ما لا شاهدَ له مرفوض."""

    j = judge(h)
    return Hukm("ghayr", "bila_shahid") if j.tag == "la_hukm" else j


def _self_loop_only(h: Hujja) -> Hukm:
    """`MUTANT_SELF_LOOP_ONLY`: الدورُ معلومةٌ تقوم على نفسها أو على الدعوى وحدَهما."""

    loops = any(s.id in s.deps or h.claim in s.deps for s in h.sabiqa)
    j = judge(replace(h, sabiqa=tuple(Sabiqa(s.id, s.ray, ()) for s in h.sabiqa)))
    return Hukm("ghayr", "dawar") if loops else j


def _u5_everywhere(h: Hujja) -> Hukm:
    """`MUTANT_U5_UNSCOPED`: الآفاتُ الثلاث خارج الخبر أيضًا."""

    return judge(replace(h, khabar=True))


def _ray_ignored(h: Hujja) -> Hukm:
    """`MUTANT_RAY_IGNORED`: الرأيُ السابق يُعامَل معلومة."""

    return judge(replace(h, sabiqa=tuple(Sabiqa(s.id, False, s.deps) for s in h.sabiqa)))


@pytest.mark.parametrize("mutant", [_binary, _self_loop_only, _u5_everywhere, _ray_ignored],
                         ids=["MUTANT_BINARY", "MUTANT_SELF_LOOP_ONLY", "MUTANT_U5_UNSCOPED",
                              "MUTANT_RAY_IGNORED"])
def test_cases_catch_named_mutants(mutant: Callable[[Hujja], Hukm]) -> None:
    assert any(mutant(h) != expected for _, h, expected in CASES)


def test_card_gate() -> None:
    good = Bitaqa("محاورة مسمّاة", "0" * 63 + "a", "intiqa", "التصوّر وتتبّع الانتقال من الشكّ")
    assert admit(good, 9) == Sabiqa(9, False, ())
    assert admit(None, 9) is None
    assert admit(replace(good, sha256="0" * 63), 9) is None
    assert admit(replace(good, sha256="0" * 63 + "A"), 9) is None
    assert admit(replace(good, hadd=""), 9) is None
    assert admit(replace(good, masdar=""), 9) is None


def test_zur_folds_without_loss() -> None:
    hs = [h for _, h, _ in CASES]
    a = archive(hs)
    assert (len(a.maqool), len(a.muajjal), len(a.zur)) == (5, 2, 10)
    assert sorted(map(id, [*a.maqool, *a.muajjal, *(h for h, _ in a.zur)])) == sorted(map(id, hs))
    for h, b in a.zur:
        assert judge(h) == Hukm("ghayr", b)


ROUNDS: tuple[tuple[str, Hujja, tuple[Jawla, ...], Hukm], ...] = (
    ("j1_zanni_many_witnesses", replace(BASE, kind="haqiqa"), (Jawla(38), Jawla(241)),
     Hukm("maqool", "zanni")),
    ("j2_lahukm_then_witness", replace(BASE, shahid=None), (Jawla(32),), Hukm("maqool", "qati")),
    ("j3_lahukm_no_witness", replace(BASE, shahid=None), (Jawla(), Jawla()),
     Hukm("la_hukm", "bila_shahid")),
    ("j4_maqool_then_khata", BASE, (Jawla(khata=True),), Hukm("ghayr", "khata")),
    ("j5_khata_then_witness", BASE, (Jawla(khata=True), Jawla(71)), Hukm("ghayr", "khata")),
    ("j6_door_survives_witness", replace(BASE, sabiqa=(Sabiqa(2, ray=True),)), (Jawla(37),),
     Hukm("ghayr", "ray_mutanakkir")),
)
"""الجولاتُ نفسُها في `Maqool.jawlatCases` وأحكامُها في `jawlat_verdicts`؛ وهنا الأحكامُ باليد."""


def test_rounds_by_hand() -> None:
    for name, h, js, expected in ROUNDS:
        assert judge_rounds(h, js) == expected, name


def _raise_after_two(h: Hujja, js: tuple[Jawla, ...]) -> Hukm:
    """`MUTANT_ZANNI_RAISED`: شاهدان جديدان يرفعان الظنّيَّ قطعيًّا."""

    j = judge_rounds(h, js)
    witnesses = sum(x.shahid is not None for x in js)
    return Hukm("maqool", "qati") if j == Hukm("maqool", "zanni") and witnesses >= 2 else j


def _khata_forgotten(h: Hujja, js: tuple[Jawla, ...]) -> Hukm:
    """`MUTANT_KHATA_FORGOTTEN`: الشاهدُ الجديد يمحو الخطأ الذي تبيّن قبله."""

    last_witness = max((i for i, x in enumerate(js) if x.shahid is not None), default=-1)
    return judge_rounds(h, js[last_witness + 1:] if last_witness >= 0 else js) \
        if any(x.khata for x in js[:last_witness + 1]) else judge_rounds(h, js)


@pytest.mark.parametrize("mutant", [_raise_after_two, _khata_forgotten],
                         ids=["MUTANT_ZANNI_RAISED", "MUTANT_KHATA_FORGOTTEN"])
def test_rounds_catch_named_mutants(mutant: Callable[[Hujja, tuple[Jawla, ...]], Hukm]) -> None:
    assert any(mutant(h, js) != expected for _, h, js, expected in ROUNDS)
