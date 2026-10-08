"""السُّلَّمُ كلُّه رقمًا واحدًا: من شهادة البوّابة إلى النسبة — مرآةُ `Slge.Pipeline`.

كلُّ فهرسٍ يقيس طبقتَه وحدَها؛ هذه الوحدةُ تركّب القرّاءَ القائمين على الكلمة الواحدة مرحلةً فوق مرحلة
ولا تبني قراءةً جديدة: (٠) الشهادة، (١) الجذعُ قراءةً واحدةً توافق قسمةَ المرجع، (٢) الجهةُ الوجوديّة
توافق صنفَ المرجع، (٣) الحالةُ الإعرابيّة توافق حالةَ المرجع، (٤) النسبةُ إلى الجار توافق دورَ المرجع.
الكلمةُ تعبر المرحلةَ إن عبرت ما قبلها؛ وتقف باسمٍ واحد (`STOPS`). القانونُ المبرهَن: لا تقفز كلمةٌ
مرحلةً — عددُ العابرين لا يزيد بزيادة المراحل (`Pipeline.survivors_antitone`)، ومن عبر الكلَّ عبر كلَّ
واحدة (`Pipeline.survive_mem`).
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from typing import Final

from slge.adawat import of_cells
from slge.adawat import rank as rank_adawat
from slge.alam import ilm
from slge.cells import Cell
from slge.hasm import hasm
from slge.jidh import Reading, jidh
from slge.maqayis import rank as rank_maqayis
from slge.nisab import nisba
from slge.tawabi import case_class, compatible
from slge.tawzi import tawzi
from slge.wujud import FIL, ISM, JAM, MASDAR, WASF, ZARF, ont_of_reading

__all__ = ["COARSE", "GOLD_CASE", "GOLD_JIHA", "GOLD_NISBA", "STAGES", "STOPS", "Gold", "run",
           "stages_passed"]

Word = tuple[Cell, ...]

STAGES: Final[tuple[str, ...]] = ("البوابة", "الجذع", "الجهة", "الحالة", "النسبة")
"""المراحلُ بترتيبها؛ `Pipeline.stages` في Lean بالعدد نفسه."""

STOPS: Final[tuple[str, ...]] = (
    "NOT_IN_CERTIFICATES", "NO_READING", "PARTICLE_NOT_IN_TABLE", "SEGMENTS_TIE",
    "READING_NOT_GOLD",
    "NO_JIHA_IN_REFERENCE", "JIHA_MISMATCH", "CASE_NOT_READ", "CASE_MISMATCH",
    "NO_NISBA_IN_REFERENCE", "NISBA_MISMATCH", "PASSED",
)
"""أسماءُ التوقّف — واحدٌ لكلّ كلمة؛ `PASSED` لمن عبر الخمس."""

GOLD_JIHA: Final[dict[str, str]] = {
    "PV": FIL, "IV": FIL, "CV": FIL, "PV_PASS": FIL, "IV_PASS": FIL, "GERUND": MASDAR,
    "NOUN_ACTIVE_PART": WASF, "NOUN_PASSIVE_PART": WASF, "ADJ_QUALIT": WASF, "ADJ_COMP": WASF,
    "NOUN_CONCRETE": ISM, "NOUN_ABSTRACT": ISM, "NOUN_PROP": ISM, "NOUN_PROP_FOREIGN": ISM,
    "ADV": ISM, "NOUN_NUM": ISM, "NOUN_TIME_PLACE": ISM, "NOUN_FIVE": ISM, "NOUN_INSTRUMENT": ISM,
    "ADJ_INTENS": WASF, "NOUN_RELATIVE": WASF, "GERUND_MEEM": MASDAR, "GERUND_INSTANT": MASDAR,
    "GERUND_PROFESSION": MASDAR,
}
"""وسمُ MASAQ → الجهةُ الوجوديّة (كما في فهرس الوجود)؛ ما ليس هنا (حروف، ضمائر) لا جهةَ له في المرجع."""

COARSE: Final[dict[str, str]] = {FIL: FIL, MASDAR: MASDAR, WASF: WASF, ZARF: ISM, JAM: ISM,
                                 ISM: ISM}

GOLD_CASE: Final[dict[str, str]] = {"مرفوع": "رفع", "منصوب": "نصب", "مجرور": "جرّ"}
"""حالةُ MASAQ → صنفُ الحالة عند `tawabi.case_class`؛ المبنيُّ والمجزوم لا يقرؤهما آخرُ الخانة."""

GOLD_NISBA: Final[dict[str, str]] = {
    "مبتدأ": "إسناد", "مبتدأ مؤخر": "إسناد", "خبر": "إسناد", "خبر مقدم": "إسناد",
    "فاعل": "إسناد", "نائب فاعل": "إسناد",
    "مفعول به": "تقييد", "مضاف إليه": "تقييد", "اسم مجرور": "تقييد", "حال": "تقييد",
    "تمييز": "تقييد", "مفعول مطلق": "تقييد", "مفعول لأجله": "تقييد", "مفعول فيه": "تقييد",
}
"""دورُ MASAQ → النسبةُ عند `nisab.nisba`؛ ما ليس هنا لا نسبةَ له في المرجع."""


@dataclass(frozen=True)
class Gold:
    """ما يقوله المرجعُ المحجوب عن الكلمة — يُمرَّر ولا يُقرأ هنا."""

    pre: Word
    det: bool
    suf: Word
    tag: str
    case: str
    role: str


@cache
def _readings(w: Word) -> tuple[Reading, ...]:
    """قراءاتُ الجذع مرتَّبةً بالمعجم — تُحفظ للكلمة الواحدة (الصورةُ تتكرّر في المرجع)."""

    return rank_maqayis(jidh(w))


def _top(w: Word, prev: Word | None) -> tuple[tuple[Reading, ...], Reading | None]:
    rs = _readings(w)
    if not rs:
        return rs, None
    a = of_cells(prev) if prev else None
    return rs, (rank_adawat(a, rs)[0] if a else rs[0])


def _is_gold(r: Reading, g: Gold) -> bool:
    return tuple(c for p in r.pre for c in p) == g.pre and (r.al != 0) == g.det and r.suf == g.suf


def run(w: Word, stem: Word, prev: Word | None, g: Gold, attested: bool,
        strict: bool = True) -> str:
    """اسمُ التوقّف للكلمة `w` (بسوابقها ولواحقها) وجذعِها `stem` (بأل) وجارِها `prev` (بأل).

    `strict`: المرحلةُ (١) تشترط **قسمةً واحدةً محسومة** (`hasm`: واحدةٌ بلا قرينة أو الأعلى الوحيدةُ
    بالقرائن؛ التعادلُ يقف باسمه)؛ وإلّا تكفي أن تكون القراءةُ الأولى بعد الترتيب هي الذهبيّة."""

    if not attested:
        return "NOT_IN_CERTIFICATES"
    jiha = GOLD_JIHA.get(g.tag)
    own_case = case_class(stem)  # حالةُ الجذع من آخره؛ والعلمُ يقرؤها من صرفه (`Alam.caseOf`)
    ms = tawzi(w)
    if ms:  # الموزِّع أوّلًا: مبنيٌّ من جدوله، قسمتُه (سوابق، لاحقة) بلا قالب
        segs = {(m.pre, m.suf) for m in ms}
        if strict and len(segs) > 1:
            return "SEGMENTS_TIE"
        m0 = ms[0]
        if not (tuple(c for p in m0.pre for c in p) == g.pre and not g.det and m0.suf == g.suf):
            return "READING_NOT_GOLD"
        if jiha is None:
            return "NO_JIHA_IN_REFERENCE"
        if not (m0.kind == "ظرف" and jiha == ISM):
            return "JIHA_MISMATCH"
    elif ils := ilm(w):  # ثمّ العلمُ ولفظُ الجلالة: لفظٌ منفردٌ من الموقَّع، لا قالبَ ولا أل
        if strict and len({m.pre for m in ils}) > 1:
            return "SEGMENTS_TIE"
        i0 = ils[0]
        # القسمةُ المرجعُ فيها توقيعُ المالك: لفظُ الجلالة منفردٌ لا أل فيه (خلافَ وسمِ MASAQ)؛ وسوى
        # الجلالة يوافقُ المرجعَ في السوابق وخلوِّ اللاحقة وأل.
        gold_al = g.det and i0.kind != "جلالة"
        if not (tuple(c for p in i0.pre for c in p) == g.pre and not gold_al and not g.suf):
            return "READING_NOT_GOLD"
        if jiha is None:
            return "NO_JIHA_IN_REFERENCE"
        if jiha != ISM:
            return "JIHA_MISMATCH"
        own_case = i0.case
    else:
        rs, top = _top(w, prev)
        if top is None:
            return "PARTICLE_NOT_IN_TABLE" if jiha is None else "NO_READING"
        if strict:
            h = hasm(of_cells(prev) if prev else None, rs)
            if h.name == "TIE":
                return "SEGMENTS_TIE"
            top = h.readings[0]
        if not _is_gold(top, g):
            return "READING_NOT_GOLD"
        if jiha is None:
            return "NO_JIHA_IN_REFERENCE"
        if COARSE[ont_of_reading(top)] != jiha:
            return "JIHA_MISMATCH"
    case = GOLD_CASE.get(g.case)
    if case is None:
        return "CASE_NOT_READ"
    if not compatible(own_case, case):
        return "CASE_MISMATCH"
    expected = GOLD_NISBA.get(g.role)
    if expected is None or prev is None:
        return "NO_NISBA_IN_REFERENCE"
    if nisba(prev, stem) != expected:
        return "NISBA_MISMATCH"
    return "PASSED"


_STAGE_OF_STOP: Final[dict[str, int]] = {
    "NOT_IN_CERTIFICATES": 0, "NO_READING": 1, "PARTICLE_NOT_IN_TABLE": 1, "SEGMENTS_TIE": 1,
    "READING_NOT_GOLD": 1,
    "NO_JIHA_IN_REFERENCE": 2, "JIHA_MISMATCH": 2, "CASE_NOT_READ": 3, "CASE_MISMATCH": 3,
    "NO_NISBA_IN_REFERENCE": 4, "NISBA_MISMATCH": 4, "PASSED": 5,
}


def stages_passed(stop: str) -> int:
    """كم مرحلةً عبرت الكلمةُ قبل توقّفها (0..5)."""

    return _STAGE_OF_STOP[stop]


def _check() -> None:
    assert len(STAGES) == 5 and STOPS[-1] == "PASSED" and len(STOPS) == 12
    assert set(_STAGE_OF_STOP) == set(STOPS)
    assert all(0 <= stages_passed(s) <= 5 for s in STOPS) and stages_passed("PASSED") == 5
    # لا تقفز كلمةٌ مرحلة: كلُّ توقّفٍ في مرحلةٍ يعني عبورَ ما قبلها
    assert sorted(stages_passed(s) for s in STOPS) == [0, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5]
    g = Gold(pre=(), det=False, suf=(), tag="PREP", case="مبني", role="حرف جر")
    assert run((), (), None, g, attested=False) == "NOT_IN_CERTIFICATES"
    assert set(GOLD_JIHA.values()) <= set(COARSE)
    assert set(GOLD_CASE.values()) == {"رفع", "نصب", "جرّ"}


_check()
