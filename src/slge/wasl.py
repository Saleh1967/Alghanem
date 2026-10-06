"""همزتا الوصل والقطع: الوصلُ حدٌّ، والقطعُ خانة، والحصرُ تقسيمُ قوالب — مرآةُ `formal/Slge/Wasl.lean`.

في الابتداء الهمزتان خانةٌ واحدة (همزةٌ متحرّكةٌ فساكن)؛ الفرقُ في الحدّ (الوصلُ يسقط في الوصل
`drop_wasl`، والقطعُ يبقى) وفي بقيّة الرسم `WASL`/`WASL_SILENT` بشهادة البوّابة. الحصرُ الصرفيُّ تقسيمٌ
لقوالب `wazn.AWZAN` المبدوءة بهمزة: `WASL_TEMPLATES` (أمرُ الثلاثيّ، ماضي الخماسيّ والسداسيّ ومصدراهما)
و`QAT_TEMPLATES` (الرباعيُّ ومصدرُه وأَفْعَل والجموع). القارئُ `kind`: السماعيُّ (العشرة) أوّلًا، ثمّ القالب،
ثمّ القطعُ الأصليُّ من الجذر، وما سواه لا يُقرأ. القياسُ على MASAQ في `tools/gen_wasl_index.py`.
"""

from __future__ import annotations

from typing import Final

from slge.cells import STATES, Cell, licensed
from slge.rawabit import cells_of
from slge.wazn import AWZAN, fill, root_of
from slge.zuruf import set_last

__all__ = ["QAT_TEMPLATES", "TEN", "WASL_TEMPLATES", "drop_wasl", "istifham_verb", "kind",
           "radical_hamza", "starts_hamza"]

_A, _I, _U, SUKUN = STATES
WASL_TEMPLATES: Final[tuple[int, ...]] = (8, 9, 10, 16, 17, 18, 19, 44, 45, 46, 47)
QAT_TEMPLATES: Final[tuple[int, ...]] = (11, 38, 54, 83, 84, 85, 100, 105, 106)
TEN: Final[tuple[str, ...]] = ("اِسْمُ", "اِبْنُ", "اِبْنَةُ", "اِمْرُؤُ", "اِمْرَأَةُ", "اِثْنَانِ", "اِثْنَتَانِ", "اِبْنُمُ",
                               "اَيْمُ", "اَيْمُنُ")
_TEN_CELLS: Final[frozenset[tuple[Cell, ...]]] = frozenset(cells_of(w) for w in TEN)


def starts_hamza(k: int) -> bool:
    t = AWZAN[k].template
    return bool(t) and t[0].slot is None and t[0].carrier == "ء"


def _on(k: int, word: tuple[Cell, ...]) -> bool:
    t = AWZAN[k].template
    r = root_of(t, word)
    return r is not None and fill(t, r) == word


def _on_any(k: int, word: tuple[Cell, ...]) -> bool:
    """على القالب بآخرٍ كما هو أو مضمومٍ أو مفتوح، بلا ألفٍ أصلًا (إِلَّا على اِفْعَلْ مردودة)."""

    r = root_of(AWZAN[k].template, word)
    if r is not None and "ا" in r:
        return False
    return _on(k, word) or _on(k, set_last(word, _U)) or _on(k, set_last(word, _A))


def radical_hamza(word: tuple[Cell, ...]) -> bool:
    """الهمزةُ أصلٌ في موضع الفاء: قالبٌ لا همزةَ في صدره وجذرُه يبدأ بهمزة."""

    def radical(k: int) -> bool:
        r = root_of(AWZAN[k].template, word)
        return r is not None and r[0] == "ء"

    return any(not starts_hamza(k) and _on_any(k, word) and radical(k) for k in range(len(AWZAN)))


def kind(word: tuple[Cell, ...]) -> str:
    """وصل | قطع | قطع أصلي | لا يُقرأ — السماعيُّ (العشرة) قبل القالب."""

    if word in _TEN_CELLS or set_last(word, _U) in _TEN_CELLS:
        return "وصل"
    if any(_on_any(k, word) for k in WASL_TEMPLATES):
        return "وصل"
    if any(_on_any(k, word) for k in QAT_TEMPLATES):
        return "قطع"
    if radical_hamza(word):
        return "قطع أصلي"
    return "لا يُقرأ"


def drop_wasl(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    """في الوصل تسقط همزةُ الوصل."""

    return word[1:]


def istifham_verb(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    """همزةُ الاستفهام على فعلٍ بهمزة وصل: تسقط الوصلُ وتبقى الاستفهام."""

    return (("ء", _A), *word[1:])


def _check() -> None:
    hamza = [k for k in range(len(AWZAN)) if starts_hamza(k)]
    assert hamza == sorted(WASL_TEMPLATES + QAT_TEMPLATES)
    assert kind(cells_of("اِنْطَلَقَ")) == "وصل" and kind(cells_of("اِقْرَأْ")) == "وصل"
    assert kind(cells_of("أَكْرَمَ")) == "قطع" and kind(cells_of("إِكْرَامُ")) == "قطع"
    assert kind(cells_of("أَخَذَ")) == "قطع أصلي" and kind(cells_of("أَرْضُ")) == "قطع أصلي"
    assert kind(cells_of("إِلَّا")) == "لا يُقرأ" and kind(cells_of("اِبْنَ")) == "وصل"
    assert all(licensed(cells_of(w)) for w in TEN) and len(TEN) == 10
    w = cells_of("اِنْطَلَقَ")
    assert not licensed(drop_wasl(w)) and licensed(cells_of("وَ") + drop_wasl(w))
    assert licensed(cells_of("وَ") + cells_of("أَكْرَمَ"))
    assert istifham_verb(cells_of("اِسْتَخْرَجْتَ")) == cells_of("أَسْتَخْرَجْتَ")


_check()
