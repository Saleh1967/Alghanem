"""التغطية: تعريفُ «الشاهد» لكلّ محورٍ من محاور الفهرس ودرجتُه — مرآةُ `Coverage` (طبقةُ الحكم).
ثلاثةُ محاور يقيسها `tools/gen_coverage_index.py` على مودَعَي شهادات المصحف: (١) **الشبكة**: من
الـ116 ثلاثٌ لا تُرخَّص — الألفُ بالحركات الثلاث («لأن الألف لا تكون أبدا إلا ساكنة»، الكتاب
س18101) — والمرخَّصُ 113 (`licensable_cells`، `licensable_length`)؛ والمبرهَن على المودَع أنّ
المشهودَ هو المرخَّصُ بعينه (`attested_eq_licensable`). (٢) **صفوفُ الجداول** (الموزِّع،
الأعلام، السوابق): شاهدُ الصفّ صورةٌ من المودَع يقرؤها قارئُ الجدول على ذلك الصفّ، ودرجتُه بعدد
شواهده (`row_grade`، `row_mafhum_pos`)؛ والصفُّ بلا شاهدٍ «معلومة» في جدوله لا يُحذف. (٣)
**جذورُ المقاييس وعقدُ المخصّص**: شاهدُ الجذر صورةٌ يقرؤها الجذعُ عليه — قاطعٌ إن لم يقرأها على
غيره (`witness_of`، `qati_iff`)، محتملٌ إن قرأها على غيره أيضًا؛ وشاهدُ العقدة جذرٌ من عنوانها
له شاهدٌ قاطع (`node_grade`، `node_mafhum_has_witness`). لا نصَّ هنا ولا قراءةَ مودَع: دوالُّ
على الخانات والأرقام يستدعيها الفهرس.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from typing import Final

from slge.cells import ALPHABET, CELLS, SUKUN, Cell

__all__ = ["ALIF_VOWELLED", "MAFHUM", "MALUMAH", "MUHTAMAL", "QATI", "cell_witnesses",
           "licensable_cells", "node_grade", "root_witnesses", "row_grade", "witness_of"]

MAFHUM: Final = "مفهوم"
MALUMAH: Final = "معلومة"
QATI: Final = "قاطع"
MUHTAMAL: Final = "محتمل"
Word = tuple[Cell, ...]

ALIF_VOWELLED: Final[tuple[Cell, ...]] = tuple((ALPHABET[1], s) for s in ("فتح", "كسر", "ضم"))
"""الألفُ بالحركات الثلاث: خاناتٌ في الشبكة لا في الكلام (`alifVowelled`)."""


def licensable_cells() -> tuple[Cell, ...]:
    """المرخَّصُ من الشبكة: الـ116 بلا الألف المتحرّكة — 113 (`licensable`)."""

    return tuple(x for x in CELLS if x not in ALIF_VOWELLED)


def cell_witnesses(forms: Iterable[Word]) -> Counter[Cell]:
    """لكلّ خانةٍ كم صورةً من المودَع تحملها."""

    out: Counter[Cell] = Counter()
    for w in forms:
        out.update(set(w))
    return out


def row_grade(n: int) -> tuple[str, int | None]:
    """درجةُ الصفّ بعدد شواهده: مفهومٌ بعددها، أو معلومةٌ بلا شاهد (`rowGrade`)."""

    return (MAFHUM, n) if n > 0 else (MALUMAH, None)


def witness_of(roots: frozenset[int], r: int) -> str | None:
    """شاهدُ الجذر `r` من صورةٍ جذورُ قراءاتها `roots`: قاطعٌ إن كانت وحدَها، محتملٌ إن كان فيها مع غيره،
    وإلّا لا شاهد (`witnessOf`)."""

    if roots == {r}:
        return QATI
    return MUHTAMAL if r in roots else None


def root_witnesses(root_sets: Iterable[frozenset[int]]) -> tuple[Counter[int], Counter[int]]:
    """على صور المودَع (كلٌّ بمجموعة جذور قراءاتها): كم شاهدًا قاطعًا وكم محتملًا لكلّ جذر."""

    qati: Counter[int] = Counter()
    muhtamal: Counter[int] = Counter()
    for roots in root_sets:
        for r in roots:
            w = witness_of(roots, r)
            if w == QATI:
                qati[r] += 1
            if w is not None:
                muhtamal[r] += 1
    return qati, muhtamal


def node_grade(title: tuple[int, ...], qati: Iterable[int]) -> tuple[str, int | None]:
    """درجةُ العقدة: أوّلُ جذرٍ في عنوانها له شاهدٌ قاطع، وإلّا معلومة (`nodeGrade`)."""

    q = frozenset(qati)
    for r in title:
        if r in q:
            return MAFHUM, r
    return MALUMAH, None


def _check() -> None:
    assert len(licensable_cells()) == 113 and (ALPHABET[1], SUKUN) in licensable_cells()
    assert witness_of(frozenset({5}), 5) == QATI and witness_of(frozenset({5, 6}), 5) == MUHTAMAL
    assert witness_of(frozenset({6}), 5) is None
    assert node_grade((1, 2), [2]) == (MAFHUM, 2) and node_grade((1, 2), [3]) == (MALUMAH, None)
    assert row_grade(0) == (MALUMAH, None) and row_grade(2) == (MAFHUM, 2)


_check()
