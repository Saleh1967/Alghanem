"""قوالبُ الاسم على أبنية سيبويه: الهيكلُ مودَعٌ مختوم، والقوالبُ متمايزةٌ على الأصول النظيفة —
مرآةُ `Abniya`.

الهيكلُ (`skeleton_of`) القالبُ حروفًا بلا حركات: الأصولُ ف ع ل والزوائدُ بحواملها، والشدّةُ حرفٌ
واحد، والتاءُ الأخيرةُ تاءُ تأنيثٍ تُسقط؛ والعضويّةُ في أبنية سيبويه (`in_abniya`) تقبل الهمزةَ الأولى
وصلًا أو قطعًا لأنّ الخانةَ لا تميّزهما. الأوزانُ خارج الأبنية 14 بأرقامها (`outside_abniya`)، وقوالبُ
الاسم الأربعةُ المضافة في الأبنية (`ism_in_abniya`). والتمايزُ (`separated`): قالبان مفصولان لا يقرآن
ملءً واحدًا بعد تسوية الآخر على أصلين نظيفين — لكلّ قالبين من الجدول (`separated_sound`،
`awzan_disjoint`) — إلّا الأزواجَ المسمّاة (`ambiguous`؛ `ambiguous_sound`، `awzan_separated`).
القياسُ على المودَع في `tools/gen_abniya_index.py`.
"""

from __future__ import annotations

from typing import Final

from slge.abniya_table import SHA256, SKELETONS
from slge.cells import ALPHABET
from slge.wazn import AWZAN, Sym, Template, skeleton

__all__ = ["AMBIGUOUS", "AUGMENTS", "ISM", "OUTSIDE", "SHA256", "SKELETONS", "ambiguous_pairs",
           "clean", "in_abniya", "separated", "skeleton_of"]

_SKELETONS: Final[frozenset[tuple[int, ...]]] = frozenset(SKELETONS)
AUGMENTS: Final[tuple[str, ...]] = ("ء", "ا", "ت", "س", "م", "ن", "و", "ي")
"""حروفُ الزيادة: ما يظهر زائدًا في قالبٍ من الجدول (`augments`)."""
ISM: Final[tuple[int, ...]] = (121, 122, 123, 124)
"""قوالبُ الاسم المضافة على أبنية سيبويه: فِعْل، فَعَال، فُعَيْل، فَاعُول."""
OUTSIDE: Final[tuple[int, ...]] = (23, 26, 44, 45, 46, 47, 72, 75, 76, 102, 104, 106, 109, 110)
"""الأوزانُ خارج أبنية سيبويه بأرقامها (`outside_abniya`)."""
AMBIGUOUS: Final[tuple[tuple[int, int], ...]] = (
    (0, 36), (11, 54), (14, 116), (15, 117), (30, 94), (35, 41), (35, 93), (41, 93), (48, 115),
    (51, 60), (64, 86),
)
"""الأزواجُ غيرُ المفصولة — مسمّاة (`ambiguous`): الماضي ومصدرُه، الماضي والأمر، والقالبُ المكرَّر."""


def skeleton_of(t: Template) -> tuple[int, ...]:
    """هيكلُ القالب أرقامًا (`skeletonOf`): الشدّةُ حرفٌ واحد والتاءُ الأخيرةُ تُسقط."""

    s = [ALPHABET.index(c) for c in skeleton(t)]
    return tuple(s[:-1] if s and s[-1] == 3 else s)


def in_abniya(t: Template) -> bool:
    """العضويّةُ في أبنية سيبويه: الهيكلُ بعينه، أو بهمزةٍ أولى وصلًا (`inAbniya`)."""

    s = skeleton_of(t)
    return s in _SKELETONS or (bool(s) and s[0] == 0 and (1, *s[1:]) in _SKELETONS)


def clean(root: tuple[str, str, str]) -> bool:
    """أصلٌ نظيف: لا حرفَ زيادةٍ فيه (`Clean`)."""

    return all(c not in AUGMENTS for c in root)


def _sep(x: Sym, y: Sym) -> bool:
    if x.slot is None and y.slot is None:
        return (x.carrier, x.state) != (y.carrier, y.state)
    if x.slot is not None and y.slot is not None:
        return x.state != y.state
    return True


def _sep_last(x: Sym, y: Sym) -> bool:
    if x.slot is None and y.slot is None:
        return x.carrier != y.carrier
    return not (x.slot is not None and y.slot is not None)


def separated(t: Template, u: Template) -> bool:
    """قالبان مفصولان (`separated`): يفترقان في غير الآخر، أو في الآخر بالحامل وحدَه."""

    if len(t) != len(u):
        return True
    if not t:
        return False
    return any(_sep(x, y) for x, y in zip(t[:-1], u[:-1], strict=True)) or _sep_last(t[-1], u[-1])


def ambiguous_pairs() -> tuple[tuple[int, int], ...]:
    """الأزواجُ غيرُ المفصولة في الجدول — محسوبةٌ لا مقرَّرة."""

    n = len(AWZAN)
    return tuple((k, q) for k in range(n) for q in range(k + 1, n)
                 if not separated(AWZAN[k].template, AWZAN[q].template))


def _check() -> None:
    assert len(SKELETONS) == 158 and len(AWZAN) == 125
    assert tuple(k for k in range(len(AWZAN)) if not in_abniya(AWZAN[k].template)) == OUTSIDE
    assert all(in_abniya(AWZAN[k].template) for k in ISM)
    assert ambiguous_pairs() == AMBIGUOUS
    assert skeleton_of(AWZAN[12].template) == (20, 18, 23)  # فَعَّلَ: الشدّةُ حرفٌ واحد
    assert AWZAN[31].name == "فَعَالَةٌ" and AWZAN[31].template[-1].carrier == "ت"
    assert skeleton_of(AWZAN[31].template) == (20, 18, 1, 23)  # فَعَالَةٌ: التاءُ الأخيرةُ تُسقط
    assert clean(("ك", "ت", "ب")) is False and clean(("ذ", "ك", "ر"))  # التاءُ من حروف الزيادة
    assert not separated(AWZAN[0].template, AWZAN[36].template)  # فَعَلَ/فَعَلٌ
    assert separated(AWZAN[121].template, AWZAN[29].template)  # فِعْلٌ/فَعْلٌ: الحالةُ الأولى


_check()
