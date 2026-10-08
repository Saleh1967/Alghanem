"""الحسم: توقّعاتٌ مستقلّةٌ عن الشيفرة (القالبُ ليس قسمة؛ الأعلى الوحيدُ أو تعادلٌ باسمه؛ الجوارُ يعلو
المعجمَ والتكرار؛ لا قراءةَ تُحذف)، وطفراتٌ مرفوضة."""

from __future__ import annotations

from slge.adawat import of_cells
from slge.hasm import BOUND, best, hasm, score, seg_of, segments
from slge.hasm_table import ROOT_FREQ, UNIQUE_FORMS
from slge.jidh import jidh
from slge.rawabit import cells_of


def test_template_multiplicity_is_one_segment() -> None:
    # مِنْ: قراءتان على قالبين، قسمةٌ واحدة — تُحسم بلا قرينة
    rs = jidh(cells_of("مِنْ"))
    assert len(rs) == 2 and len(segments(rs)) == 1
    h = hasm(None, rs)
    assert h.name == "UNIQUE" and h.readings == rs and h.seg == seg_of(rs[0])


def test_two_segments_are_decided_by_evidence_without_dropping_readings() -> None:
    # كَتَبَ: (كَ + تَبَ) أو (كَتَبَ) — المعجمُ والتكرارُ يحسمان إلى كَتَبَ؛ القراءاتُ كلُّها باقية
    w = cells_of("كَتَبَ")
    rs = jidh(w)
    assert len(segments(rs)) == 2
    h = hasm(None, rs)
    assert h.name == "DECIDED" and h.seg is not None and h.seg[0] == () and h.seg[2] == w
    assert all(rd in rs for rd in h.readings) and len(rs) == 2
    # إِلَيْكَ: الكافُ لاحقةً
    h2 = hasm(None, jidh(cells_of("إِلَيْكَ")))
    assert h2.name == "DECIDED" and h2.seg is not None and h2.seg[3] == (("ك", "فتح"),)


def test_neighbour_outranks_lexicon_and_frequency() -> None:
    # الدرجةُ ترتيبٌ معجميّ: جوارٌ بلا معجم > معجمٌ بأعلى تكرار
    assert max(ROOT_FREQ.values()) < BOUND and UNIQUE_FORMS > 10_000
    rs = jidh(cells_of("كَتَبَ"))
    a = of_cells(cells_of("لَمْ"))  # أداةُ جزمٍ معمولُها فعل
    assert a is not None
    for _, g in segments(rs):
        s_with, s_without = score(a, g), score(None, g)
        assert s_without < 2 * BOUND and (s_with >= 2 * BOUND or s_with == s_without)


def test_best_is_the_unique_maximum_or_nothing_and_mutants() -> None:
    assert best((5, 3, 5)) is None and best((1, 9, 4)) == 1 and best(()) is None
    assert best((7,)) == 0
    # طفرةٌ: تساوي الدرجات بعد الحسم يُسقطه إلى تعادلٍ باسمه، لا إلى اختيارٍ أعمى
    rs = jidh(cells_of("كَتَبَ"))
    scores = tuple(score(None, g) for _, g in segments(rs))
    assert best(scores) is not None and best(tuple(max(scores) for _ in scores)) is None
    # جذرٌ غيرُ مشهود تكرارُه صفر، والمشهودُ موجب
    assert all(v > 0 for v in ROOT_FREQ.values()) and ROOT_FREQ.get(-1, 0) == 0
