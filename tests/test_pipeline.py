"""السُّلَّمُ رقمًا واحدًا: توقّعاتٌ مستقلّةٌ عن الشيفرة (لا قفزَ مرحلة؛ القمعُ متناقص؛ الصارمُ لا يزيد
على المرتَّب؛ العابرُ آخرَ السُّلَّم عبر الجذعَ ذهبيًّا)، وطفراتٌ مرفوضة."""

from __future__ import annotations

from itertools import pairwise

from slge.pipeline import (
    GOLD_CASE,
    GOLD_JIHA,
    GOLD_NISBA,
    STAGES,
    STOPS,
    Gold,
    run,
    stages_passed,
)
from slge.pipeline_table import MASAQ, RANKED, STRICT
from slge.rawabit import cells_of


def test_stops_name_each_stage_without_a_leap() -> None:
    assert STAGES == ("البوابة", "الجذع", "الجهة", "الحالة", "النسبة")
    # كلُّ مرحلةٍ لها توقّفٌ على الأقلّ، والمرحلةُ الأخيرة PASSED وحدَه
    assert {stages_passed(s) for s in STOPS} == {0, 1, 2, 3, 4, 5}
    assert [s for s in STOPS if stages_passed(s) == 5] == ["PASSED"]
    assert stages_passed("NO_READING") == 1 and stages_passed("NISBA_MISMATCH") == 4


def test_deposited_funnels_are_antitone() -> None:
    assert len(STRICT) == len(RANKED) == len(STAGES) + 1 and STRICT[0] == RANKED[0] == MASAQ
    assert all(b <= a for a, b in pairwise(STRICT))
    assert all(b <= a for a, b in pairwise(RANKED))
    assert STRICT[0] == RANKED[0] and STRICT[1] == RANKED[1]  # لا هيمنةَ لأحدهما بعد الحسم
    # الجذعُ صارمًا = الموزِّعُ أو العلمُ الموقَّع أو قسمةٌ محسومة ذهبيّة: 34,206 (كان 32,592 قبل
    # الأعلام، و26,758 قبل الموزِّع، و15,583 حين عُدّ القالبُ قسمة)
    # ثمّ 34,206 قبل تصحيح همزة الأسماء الموصولة كسرًا (الغانم ADR ٧): المرجعُ المحجوب يقرأ اُسْمُ (22:40)
    # واُبْنُوا (18:21، 37:97) بالضمّ فلم تعد تطابق المودَع (NOT_IN_CERTIFICATES: 40,731 ← 40,728)
    # ثمّ ADR ٨ في الغانم (الضمّةُ العارضة): اِمْشُوا/اِقْضُوا كسرًا، والمرجعُ يقرأ إحداهما بالضمّ
    # (40,728 ← 40,727)
    assert STRICT[1] == 40_727 and STRICT[2] == 34_203
    # الرقمُ الواحد دون 30% — مسجَّلٌ ليُقاس عليه كلُّ تحسين (1,763 ← 1,989 ← 2,070 ← 3,070 ← 3,069)
    assert STRICT[5] / MASAQ < 0.30 and STRICT[5] == 3_069 and RANKED[5] == 3_022


def test_a_sound_verb_crosses_to_the_jiha_and_stops_by_name_when_not_asked() -> None:
    # ذَهَبَ: قراءةٌ واحدةٌ ذهبيّة، جهتُها فعل؛ المرجعُ يقول مبني → تقف باسم «الحالةُ لا تُقرأ»
    w = cells_of("ذَهَبَ")
    g = Gold(pre=(), det=False, suf=(), tag="PV", case="مبني", role="فعل ماضٍ")
    assert run(w, w, None, g, attested=True) == "CASE_NOT_READ"
    # ولو سأله المرجعُ عن حالةٍ معربة لوقف في الحالة لا قبلها
    g2 = Gold(pre=(), det=False, suf=(), tag="PV", case="مرفوع", role="فعل ماضٍ")
    assert run(w, w, None, g2, attested=True) in ("CASE_MISMATCH", "NO_NISBA_IN_REFERENCE")


def test_mutants_are_refused() -> None:
    w = cells_of("ذَهَبَ")
    g = Gold(pre=(), det=False, suf=(), tag="PV", case="مبني", role="فعل ماضٍ")
    # غيرُ مشهود في الشهادات يقف عند البوّابة مهما كان
    assert run(w, w, None, g, attested=False) == "NOT_IN_CERTIFICATES"
    # قسمةٌ ذهبيّة مزوّرة (لاحقةٌ ليست في الكلمة) تُسقط الجذع
    bad = Gold(pre=(), det=False, suf=(("ت", "ضم"),), tag="PV", case="مبني", role="فعل ماضٍ")
    assert run(w, w, None, bad, attested=True) == "READING_NOT_GOLD"
    # وسمٌ اسميٌّ لفعلٍ يُسقط الجهة
    bad2 = Gold(pre=(), det=False, suf=(), tag="NOUN_CONCRETE", case="مبني", role="فعل ماضٍ")
    assert run(w, w, None, bad2, attested=True) == "JIHA_MISMATCH"
    # حرفٌ لا جهةَ له في المرجع يقف باسمه لا بالخطأ
    assert "PREP" not in GOLD_JIHA and "مبني" not in GOLD_CASE and "حرف جر" not in GOLD_NISBA


def test_strict_decides_segments_by_hasm_and_ranked_takes_the_first() -> None:
    # كَتَبَ قسمتان (كَ سابقةً + تَبَ، أو كَتَبَ): الحسمُ بالمعجم والتكرار يختار كَتَبَ فيمضي الصارمُ أيضًا
    w = cells_of("كَتَبَ")
    g = Gold(pre=(), det=False, suf=(), tag="PV", case="مبني", role="فعل ماضٍ")
    assert run(w, w, None, g, attested=True) == "CASE_NOT_READ"
    assert run(w, w, None, g, attested=True, strict=False) == "CASE_NOT_READ"
    assert "SEGMENTS_TIE" in STOPS and stages_passed("SEGMENTS_TIE") == 1


def test_the_divine_name_and_proper_nouns_cross_the_stem_by_the_owner_signature() -> None:
    # ءَلْلَهُ: المرجعُ يعدّ أل سابقةً (det)؛ الموقَّعُ لفظٌ منفرد — يعبر الجذعَ والجهةَ ويُقرأ رفعًا
    w = cells_of("ءَلْلَهُ")
    g = Gold(pre=(), det=True, suf=(), tag="NOUN_PROP", case="مرفوع", role="مبتدأ")
    assert run(w, w, None, g, attested=True) == "NO_NISBA_IN_REFERENCE"  # لا جارَ فلا نسبة
    # إِبْرَاهِيمَ ممنوعٌ: الفتحُ يوافق النصبَ والجرّ؛ ولا يوافق الرفع
    w = cells_of("إِبْرَاهِيمَ")
    g = Gold(pre=(), det=False, suf=(), tag="NOUN_PROP", case="مجرور", role="مضاف إليه")
    assert run(w, w, cells_of("رَبْبِ"), g, attested=True) == "PASSED"
    g2 = Gold(pre=(), det=False, suf=(), tag="NOUN_PROP", case="مرفوع", role="فاعل")
    assert run(w, w, cells_of("قَاْلَ"), g2, attested=True) == "CASE_MISMATCH"
    # وسمٌ فعليٌّ لعلمٍ يُسقط الجهة؛ وأل مرجعيّةٌ على غير الجلالة تُسقط القسمة
    g3 = Gold(pre=(), det=False, suf=(), tag="PV", case="مجرور", role="مضاف إليه")
    assert run(w, w, None, g3, attested=True) == "JIHA_MISMATCH"
    g4 = Gold(pre=(), det=True, suf=(), tag="NOUN_PROP", case="مجرور", role="مضاف إليه")
    assert run(w, w, None, g4, attested=True) == "READING_NOT_GOLD"
