"""ظروفُ الزمان: التصرُّفُ عددُ الحالات، والبناءُ حالةٌ واحدة — مرآةُ `formal/Slge/Zaman.lean`.

**المتصرِّف** (يَوْم، شَهْر، لَيْل…) اسمٌ تجري عليه عمليّاتُ الظرف الثلاث (`zuruf.mudaf/jarr/qat`) وعمليّتا
التنوين (`raf_tanwin`، `nasb_tanwin`): خمسُ صورٍ مرخَّصةٌ متباينة لكلّ جذع، والخانةُ تفرّق الضمَّ المنوَّن
(مرفوعٌ متصرّف) من الضمّ العاري (مقطوع) (`tanwin_vs_qat`، `hukm_rafTanwin`). والظرفيّةُ نفسُها (معنى
«في») ليست خانةً: الفتحُ يقرأ النصبَ ولا يفرّق ظرفًا من مفعولٍ به — دَينٌ على النظم.

**المبنيُّ** الثمانية (إِذْ، إِذَا، أَمْسِ، الْآنَ، مُذْ، مُنْذُ، قَطُّ، عَوْضُ) صورةٌ واحدةٌ بحالةٍ أخيرةٍ ثابتة
(`constants_states`). فالتصرُّفُ **عددُ الحالات** في الخانة الأخيرة: ≥ 2 للمتصرّف، 1 للمبنيّ — وهذا
ما يُقاس على MASAQ (`tools/gen_zaman_index.py`). وأَمْسِ بأل العهديّة معربٌ (`al_amsu`). والمشتركةُ
(قَبْل، بَعْد، بَيْن، عِنْد) في `zuruf`: زمانٌ أم مكانٌ من المضاف إليه لا من الخانة.
"""

from __future__ import annotations

from typing import Final

from slge.cells import STATES, Cell, licensed
from slge.zuruf import jarr, mudaf, qat, set_last

__all__ = ["CONSTANTS", "STEMS", "forms_of", "hukm", "nasb_tanwin", "raf_tanwin"]

_A, _I, _U, SUKUN = STATES
NUN: Final[Cell] = ("ن", SUKUN)


def raf_tanwin(stem: tuple[Cell, ...]) -> tuple[Cell, ...]:
    return (*set_last(stem, _U), NUN)


def nasb_tanwin(stem: tuple[Cell, ...]) -> tuple[Cell, ...]:
    return (*set_last(stem, _A), NUN)


def hukm(word: tuple[Cell, ...]) -> str:
    """يفرّق المنوَّنَ من المقطوع؛ الفتحُ نصبٌ لا يُقرأ منه ظرفٌ ولا مفعول."""

    if not word:
        return "لا تقرؤه الخانة"
    if len(word) >= 2 and word[-1] == NUN and word[-2][1] != SUKUN:
        return {_U: "مرفوع منوَّن (متصرّف غير ظرف)", _A: "منصوب منوَّن", _I: "مجرور منوَّن"}.get(
            word[-2][1], "لا تقرؤه الخانة")
    return {_U: "مقطوع عن الإضافة", _A: "منصوب (ظرفٌ أو مفعول)", _I: "مجرور"}.get(
        word[-1][1], "لا تقرؤه الخانة")


def _s(*cells: Cell) -> tuple[Cell, ...]:
    return cells


STEMS: Final[dict[str, tuple[Cell, ...]]] = {
    "يَوْم": _s(("ي", _A), ("و", SUKUN), ("م", _A)), "شَهْر": _s(("ش", _A), ("ه", SUKUN), ("ر", _A)),
    "سَنَة": _s(("س", _A), ("ن", _A), ("ت", _A)), "عَام": _s(("ع", _A), ("ا", SUKUN), ("م", _A)),
    "لَيْل": _s(("ل", _A), ("ي", SUKUN), ("ل", _A)),
    "نَهَار": _s(("ن", _A), ("ه", _A), ("ا", SUKUN), ("ر", _A)),
    "صَبَاح": _s(("ص", _A), ("ب", _A), ("ا", SUKUN), ("ح", _A)),
    "مَسَاء": _s(("م", _A), ("س", _A), ("ا", SUKUN), ("ء", _A)),
}
"""المتصرّفةُ الثمانية كما في الحصر المُرسَل."""

CONSTANTS: Final[dict[str, tuple[tuple[Cell, ...], str]]] = {
    "إِذْ": (_s(("ء", _I), ("ذ", SUKUN)), SUKUN),
    "إِذَا": (_s(("ء", _I), ("ذ", _A), ("ا", SUKUN)), SUKUN),
    "أَمْسِ": (_s(("ء", _A), ("م", SUKUN), ("س", _I)), _I),
    "الْآنَ": (_s(("ء", _A), ("ل", SUKUN), ("ء", _A), ("ا", SUKUN), ("ن", _A)), _A),
    "مُذْ": (_s(("م", _U), ("ذ", SUKUN)), SUKUN),
    "مُنْذُ": (_s(("م", _U), ("ن", SUKUN), ("ذ", _U)), _U),
    "قَطُّ": (_s(("ق", _A), ("ط", SUKUN), ("ط", _U)), _U),
    "عَوْضُ": (_s(("ع", _A), ("و", SUKUN), ("ض", _U)), _U),
}
"""المبنيّةُ الثمانية بحالتها الأخيرة المعلَنة في الحصر."""


def forms_of(stem: tuple[Cell, ...]) -> tuple[tuple[Cell, ...], ...]:
    return mudaf(stem), jarr(stem), qat(stem), raf_tanwin(stem), nasb_tanwin(stem)


def _check() -> None:
    for name, stem in STEMS.items():
        fs = forms_of(stem)
        if len(set(fs)) != 5 or not all(licensed(f) for f in fs):
            raise ValueError(f"ZAMAN:{name}")
    for name, (cells, st) in CONSTANTS.items():
        if cells[-1][1] != st or not licensed(cells):
            raise ValueError(f"CONSTANT:{name}")


_check()
