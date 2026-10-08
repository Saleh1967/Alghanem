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


def test_deposited_funnels_are_antitone_and_ranked_dominates_strict() -> None:
    assert len(STRICT) == len(RANKED) == len(STAGES) + 1 and STRICT[0] == RANKED[0] == MASAQ
    assert all(b <= a for a, b in pairwise(STRICT))
    assert all(b <= a for a, b in pairwise(RANKED))
    assert all(s <= r for s, r in zip(STRICT, RANKED, strict=True))
    # الجذعُ صارمًا = القسمةُ الذهبيّة بقراءةٍ واحدة في فهرس الجذع (15,583)
    assert STRICT[2] == 15_583
    # الرقمُ الواحد دون 30% — كما تُوقِّع؛ ومسجَّلٌ ليُقاس عليه كلُّ تحسين
    assert STRICT[5] / MASAQ < 0.30 and STRICT[5] == 1_763 and RANKED[5] == 1_943


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


def test_strictness_is_the_only_difference_between_the_two_funnels() -> None:
    # كَتَبَ قراءتان (كَ سابقةً + تَبَ): الصارمُ يقف بالتعدّد، والمرتَّبُ يمضي بالأولى
    w = cells_of("كَتَبَ")
    g = Gold(pre=(), det=False, suf=(), tag="PV", case="مبني", role="فعل ماضٍ")
    assert run(w, w, None, g, attested=True) == "READINGS_AMBIGUOUS"
    assert run(w, w, None, g, attested=True, strict=False) == "CASE_NOT_READ"
