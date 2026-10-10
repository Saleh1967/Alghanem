"""السوابقُ الحرفيّة: باءُ الجرّ ولامُ الجرّ ولامُ الأمر ولامُ كي وألُ التعريف وهمزةُ الوصل — مرآةُ
`Slge.Sawabiq` (ADR ٢٥).

الحرفُ الواحد في صدر الكلمة يُقرأ **بعلاقته المرخَّصة بما بعده** لا بنفسه، على أبواب الكتاب لسيبويه
المودَعة بأسطرها في `sawabiq_table` (مولَّدٌ من الكتاب المختوم): لامُ الإضافة (الملك) وباءُ الجرّ (الإلزاق)
أمامَ ما آخرُه جرّ؛ لامُ الأمر أمام مضارعٍ مجزوم («ليفعل»)؛ لامُ كي أمام مضارعٍ منصوب بأن مضمرة («جئتك
لتفعل»)؛ ألُ «الحرف الذي تعرف به الأسماء» بهمزةٍ مفتوحةٍ ابتداءً؛ وهمزةُ الوصل في الأفعال وفي الأسماء
العشرة «مكسورة أبدا إلا أن يكون الحرف الثالث مضموما». وما سقط في الوصل («إذا كان قبلها كلام حذفت»؛
«فعلوا بلام الأمر مع الفاء والواو مثل ذلك: فلينظر وليضرب») يُردّ في `under` وتُقرأ القراءةُ على الأصل
(`joined_is_initial`، `sakin_is_kasra`)؛ وكلُّ قراءةٍ تُردّ بعينها (`sawabiq_restores`). التعدّدُ يُحصى
ولا يُحسم هنا (لِيَوْمٍ: جرٌّ أو أمر).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from slge.cells import SUKUN, Cell
from slge.jidh import ENCLITICS, OBJECT_SUFFIXES, PROCLITICS, _peel_suffix
from slge.marifa import SUN, has_al
from slge.rawabit import cells_of
from slge.tawabi import case_class
from slge.wasl import TEN
from slge.wasl import kind as wasl_kind
from slge.zuruf import set_last

__all__ = ["KINDS", "PROCLITIC_CELLS", "Reading", "lift", "lift_arid", "plural_waw", "restore",
           "sawabiq", "wasl_noun", "wasl_state"]

Word = tuple[Cell, ...]
KINDS: Final[tuple[str, ...]] = ("BA_JARR", "LAM_JARR", "LAM_AMR", "LAM_KAY", "AL", "WASL_FIL",
                                 "WASL_ISM")
"""الأبوابُ السبعة بترتيب `Kind.idx`."""

_BA: Final[Cell] = ("ب", "كسر")
_LAM_I: Final[Cell] = ("ل", "كسر")
_WA: Final[Cell] = ("و", "فتح")
_FA: Final[Cell] = ("ف", "فتح")
PROCLITIC_CELLS: Final[tuple[Cell, ...]] = (*(p[0] for p in PROCLITICS), ("ت", "فتح"))
"""سوابقُ الجذع وتاءُ القسم خانةً خانة (`proclitics`)."""
_PRES: Final[tuple[Word, ...]] = (
    (), *((p,) for p in PROCLITIC_CELLS),
    *((p, q) for p in PROCLITIC_CELLS for q in PROCLITIC_CELLS))
_HAMZA: Final[Cell] = ("ء", "فتح")
_TEN: Final[frozenset[Word]] = frozenset(cells_of(w) for w in TEN)


@dataclass(frozen=True)
class Reading:
    """السوابقُ، البابُ، ما بعد السابقة كما هو، وأصلُه بعد ردّ ما سقط في الوصل."""

    pre: Word
    kind: str
    rest: Word
    under: Word

    @property
    def joined(self) -> bool:
        return self.under != self.rest


def restore(m: Reading) -> Word:
    return (*m.pre, *m.rest)


def _is_mudari(r: Word) -> bool:
    return len(r) >= 3 and r[0][0] in "يتنء" and r[0][1] in ("فتح", "ضم")


def _nun_dropped(r: Word) -> bool:
    if len(r) < 2 or r[-1][1] != SUKUN:
        return False
    y, x = r[-1][0], r[-2][1]
    return (y == "و" and x == "ضم") or (y == "ي" and x == "كسر") or (y == "ا" and x == "فتح")


def _stems(r: Word) -> tuple[Word, ...]:
    """الكلمةُ، ثمّ ما بقي بعد قطع ضميرِ نصبٍ متّصل (يُظْهِرَهُ ← يُظْهِرَ)."""

    return (r, *(s for q in OBJECT_SUFFIXES if (s := _peel_suffix(q, r)) is not None))


def _jazm(r: Word) -> bool:
    return _is_mudari(r) and any(s[-1][1] == SUKUN for s in _stems(r) if s)


def _nasb(r: Word) -> bool:
    return _is_mudari(r) and any(s[-1][1] == "فتح" or _nun_dropped(s) for s in _stems(r) if s)


def _jarr(r: Word) -> bool:
    """آخرُه جرٌّ، أو مضافٌ إلى ضميرٍ متّصل وآخرُ مضافه جرّ (رَبِّهِمْ)."""

    if case_class(r) in ("جرّ", "نصب/جرّ"):
        return True
    return any((s := _peel_suffix(q, r)) is not None and case_class(s) in ("جرّ", "نصب/جرّ")
               for q in OBJECT_SUFFIXES)


def _al_joined(r: Word) -> bool:
    if len(r) < 2 or r[0][1] != SUKUN:
        return False
    return r[0][0] == "ل" or (r[0][0] in SUN and r[0][0] == r[1][0])


WASL_NOUNS: Final[tuple[tuple[str, ...], ...]] = (("ب", "ن"), ("س", "م"), ("م", "ر", "ء"),
                                                   ("ث", "ن"))
"""هياكلُ الأسماء الموصولة الهمزة بعد الهمزة (ابن/ابنة، اسم، امرؤ/امرأة، اثنان؛ «است» تُركت لالتباسها
باستفعل): «مكسورة في الابتداء وإن كان الثالث مضموما… لأنها ليست ضمة تثبت» (الكتاب س17569–17573)؛
مرآةُ `WASL_NOUNS` في بوّابة الغانم (`gate/residue.py`) و`Sawabiq.waslNouns`."""


def wasl_noun(r: Word) -> bool:
    """أهيكلُ ما بعد الهمزة هيكلُ اسمٍ موصول؟ (`waslNoun`)"""

    carriers = tuple(c[0] for c in r[:3])
    return any(carriers[:len(n)] == n for n in WASL_NOUNS)


def wasl_state(r: Word) -> str:
    """حركةُ همزة الوصل المردودة: مضمومةٌ إن كان الثالثُ مضمومًا في غير الأسماء الموصولة، وإلّا مكسورة
    (`waslState`؛ الكتاب س17530 وس17573)."""

    if wasl_noun(r):
        return "كسر"
    return "ضم" if len(r) >= 2 and r[1][1] == "ضم" else "كسر"


def lift(r: Word) -> Word:
    """ردُّ ما سقط في الوصل: همزةُ أل مفتوحة، وهمزةُ الوصل بحركتها (`lift`)."""

    return (("ء", "فتح"), *r) if _al_joined(r) else (("ء", wasl_state(r)), *r)


def plural_waw(r: Word) -> bool:
    """الشكلُ «C₁ْ C₂ُ و…» بعد الهمزة الساقطة: أمرُ الجماعة من الناقص — ضمّةُ C₂ ثابتةٌ (اُدْعُوا) أو عارضةٌ
    (اِمْشُوا) وثبوتُها ليس في الخانات (`pluralWaw`؛ الغانم `A116.Boundary.waslVowelStable`)."""

    return len(r) >= 3 and r[0][1] == SUKUN and r[1][1] == "ضم" and r[2][0] == "و"


def lift_arid(r: Word) -> Word:
    """الردُّ الآخر على شكل أمر الجماعة: همزةٌ مكسورةٌ لضمّةٍ عارضة (`liftArid`)؛ `siyaq.restore` يقدّم
    الوجهين ولا يحسم — الحسمُ عند البوّابة من فهرس الأفعال (الغانم ADR ٨)."""

    return (("ء", "كسر"), *r)


def _wasl_kinds(w: Word) -> tuple[str, ...]:
    if w in _TEN or set_last(w, "ضم") in _TEN or set_last(w, "فتح") in _TEN:
        return ("WASL_ISM",)
    if wasl_kind(w) == "وصل" or any(
            (s := _peel_suffix(q, w)) is not None
            and (wasl_kind(s) == "وصل" or wasl_kind(set_last(s, SUKUN)) == "وصل")
            for q in ENCLITICS):
        return ("WASL_FIL",)  # بلاحقةٍ: الجذعُ على آخره أو مسكَّنًا (أمرُ الجماعة اُسْجُدُوا)
    return ()


def _direct(p: Cell | None, r: Word) -> tuple[str, ...]:
    if p is None:
        return (*(("AL",) if has_al(r) else ()), *_wasl_kinds(r))
    out: list[str] = []
    if p == _BA and _jarr(r):
        out.append("BA_JARR")
    if p == _LAM_I:
        if _jarr(r):
            out.append("LAM_JARR")
        if _jazm(r):
            out.append("LAM_AMR")
        if _nasb(r):
            out.append("LAM_KAY")
    return tuple(out)


def _read_at(pre: Word, r: Word) -> tuple[Reading, ...]:
    p = pre[-1] if pre else None
    out = [Reading(pre, k, r, r) for k in _direct(p, r)]
    if r and p is not None and r[0][1] == SUKUN:
        u = lift(r)
        # همزةُ أل لا تسقط بعد همزة الاستفهام («إلا ما ذكرنا من الألف واللام في الاستفهام»)
        out += [Reading(pre, k, r, u) for k in _direct(None, u) if not (k == "AL" and p == _HAMZA)]
        if p in (_WA, _FA) and r[0][0] == "ل":
            out += [Reading(pre, k, r, (_LAM_I, *r[1:])) for k in _direct(_LAM_I, r[1:])
                    if k == "LAM_AMR"]
    return tuple(out)


def sawabiq(w: Word) -> tuple[Reading, ...]:
    """قراءاتُ طبقة السابقة: كلُّ (سوابق، باب، أصل) يردّ الكلمةَ بعينها (`sawabiq`)."""

    out: list[Reading] = []
    for pre in _PRES:
        if w[: len(pre)] != pre or len(w) == len(pre):
            continue
        for m in _read_at(pre, w[len(pre):]):
            assert restore(m) == w
            out.append(m)
    return tuple(out)


def _check() -> None:
    assert len(PROCLITIC_CELLS) == 9
    assert [m.kind for m in sawabiq(cells_of("لِيَوْمٍ"))] == ["LAM_JARR", "LAM_AMR"]
    assert not sawabiq(cells_of("كَتَبَ"))
    b = sawabiq(cells_of("بِسْمِ"))
    assert {m.kind for m in b} == {"BA_JARR", "WASL_ISM"} and any(m.joined for m in b)
    assert any(m.kind == "LAM_KAY" for m in sawabiq(cells_of("لِيَحْكُمَ")))
    f = sawabiq(cells_of("فَلْيَنْظُرْ"))
    assert any(m.kind == "LAM_AMR" and m.joined and m.under == cells_of("لِيَنْظُرْ") for m in f)
    assert any(m.kind == "AL" and m.joined for m in f)  # أل + يَنْظُرْ صورةً — تعدّدٌ يُحصى
    assert [m.kind for m in sawabiq(cells_of("ءَلْحَمْدُ"))] == ["AL"]
    w = sawabiq(cells_of("وَسْتَغْفِرْ"))
    assert any(m.kind == "WASL_FIL" and m.under == cells_of("اِسْتَغْفِرْ") for m in w)
    assert wasl_state(cells_of("سْكُنْ")) == "ضم" and wasl_state(cells_of("هْدِ")) == "كسر"
    assert [m.kind for m in sawabiq(cells_of("اِبْنَ"))] == ["WASL_ISM"]


_check()
