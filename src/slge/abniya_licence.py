"""أبنيةُ سيبويه على الترخيص الثلاثيّ: كم تشكيلًا لكلّ هيكلٍ يرخّصه الوصلُ والوقف — مرآةُ
`AbniyaLicence` (ADR ٣٦).

الهيكلُ في المودَع (`abniya_table.SKELETONS`، 158) حروفٌ بلا حركات — فلا يُقاس الهيكلُ على الترخيص
إلّا بتشكيله. التشكيلُ: لكلّ حاملٍ حالةٌ من الأربع، إلّا الألفَ فساكنةٌ أبدًا («لأن الألف لا تكون
أبدا إلا ساكنة»، الكتاب س18101؛ `Coverage.licensable`). والألفُ الأولى في الهيكل **همزةُ وصل**
(افتعل، استفعل، انفعل…): ابتداءً همزةٌ متحرّكة، مكسورةٌ إلّا أن يكون الثالثُ مضمومًا
(`Sawabiq.wasl_state_damm_iff`، الغانم `Boundary.waslVowel`). فيُعدّ لكلّ هيكلٍ: التشكيلاتُ،
والمرخَّصُ منها وصلًا (`continue_licensed`) ووقفًا (`pause_licensed`) — بالقاعدة، وبلا قاعدة الوصل
(الألفُ الأولى ساكنةً كما رُسمت) شاهدًا على أنّ القاعدةَ هي الفارق.
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from itertools import product
from typing import Final

from slge.abniya_table import SKELETONS
from slge.cells import ALPHABET, STATES, SUKUN, Cell
from slge.madd import continue_licensed, pause_licensed

__all__ = ["ALIF", "HAMZA", "Counts", "counts", "is_wasl", "vocalizations"]

ALIF: Final[str] = ALPHABET[1]
HAMZA: Final[str] = ALPHABET[0]
DAMMA: Final[str] = "ضم"
KASRA: Final[str] = "كسر"
Word = tuple[Cell, ...]
Counts = tuple[int, int, int]
"""(التشكيلات، المرخَّصُ وصلًا، المرخَّصُ وقفًا)."""


def is_wasl(skeleton: Sequence[int]) -> bool:
    """أوّلُ الهيكل ألفٌ: همزةُ وصل."""

    return len(skeleton) > 0 and ALPHABET[skeleton[0]] == ALIF


def vocalizations(skeleton: Sequence[int], wasl_rule: bool = True) -> Iterator[Word]:
    """كلُّ تشكيلات الهيكل: الألفُ ساكنةٌ أبدًا؛ والألفُ الأولى بقاعدة الوصل همزةٌ مكسورةٌ إلّا أن
    يُضمّ الثالث (`wasl_rule=False`: تبقى ألفًا ساكنةً كما رُسمت)."""

    letters = [ALPHABET[i] for i in skeleton]
    wasl = wasl_rule and is_wasl(skeleton)
    if wasl:
        letters[0] = HAMZA
    opts = [[SUKUN] if x == ALIF else list(STATES) for x in letters]
    if wasl:
        opts[0] = [KASRA, DAMMA]
    for states in product(*opts):
        if wasl and (states[0] == DAMMA) != (len(states) > 2 and states[2] == DAMMA):
            continue
        yield tuple(zip(letters, states, strict=True))


def counts(skeleton: Sequence[int], wasl_rule: bool = True) -> Counts:
    tot = cont = pause = 0
    for w in vocalizations(skeleton, wasl_rule):
        tot += 1
        cont += continue_licensed(w)
        pause += pause_licensed(w)
    return tot, cont, pause


def _check() -> None:
    assert len(SKELETONS) == 158 and sum(is_wasl(s) for s in SKELETONS) == 13
    ifta = next(s for s in SKELETONS if "".join(ALPHABET[i] for i in s) == "افتعل")
    assert counts(ifta, wasl_rule=False)[1:] == (0, 0)  # ألفٌ ساكنةٌ أوّلًا: لا ترخيص
    assert counts(ifta)[1] > 0  # بقاعدة الوصل: اِفْتَعَلَ


_check()
