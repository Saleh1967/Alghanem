"""الفعل: أبوابُه أزواجُ حالات، وزيادتُه طولُ قالب، وإعلالُه وإبدالُه عمليّات — مرآةُ `Fil.lean`.

الأبوابُ الستّة أزواجُ (عينِ الماضي، عينِ المضارع) من تسعة (`ABWAB`)، تُقرأ من الخانتين (`read_bab`)؛ وشرطُ
فَتَحَ–يَفْتَحُ حلقيّةٌ (`halqi`). المزيدُ: أحرفُ الزيادة = طولُ القالب − 3 (`added`؛ `MAZID` تسعةٌ: 3 + 5 + 1)؛
ولا خماسيَّ الأصول (جذرُ `wazn` ثلاثيٌّ بالبناء)، والرباعيُّ أشكال. الإعلالُ ثلاثُ عمليّات: `qalb`، `naql`،
والحذفُ ملزَمٌ (`jazm`). الإبدالُ على اِفْتَعَلَ ثلاثُ قواعد (`ibdal`) يحفظ نمطَ السكون. النواسخُ في
`nawasikh`. القياسُ على MASAQ في `tools/gen_fil_index.py`.
"""

from __future__ import annotations

from typing import Final

from slge.cells import STATES, Cell, licensed
from slge.rawabit import cells_of
from slge.wazn import AWZAN, fill, root_of

__all__ = ["ABWAB", "MAZID", "added", "halqi", "ibdal", "iftaal", "naql", "qalb", "read_bab"]

_A, _I, _U, SUKUN = STATES
ABWAB: Final[tuple[tuple[str, str], ...]] = ((_A, _U), (_A, _I), (_A, _A), (_I, _A), (_U, _U),
                                              (_I, _I))
MISSING: Final[tuple[tuple[str, str], ...]] = ((_I, _U), (_U, _A), (_U, _I))
MAZID: Final[tuple[int, ...]] = (11, 12, 13, 16, 17, 18, 14, 15, 19)
HALQ: Final[frozenset[str]] = frozenset("ءهعحغخ")
ITBAQ: Final[frozenset[str]] = frozenset("صضطظ")
DHZ: Final[frozenset[str]] = frozenset("دذز")


def read_bab(past: tuple[Cell, ...], pres: tuple[Cell, ...]) -> tuple[str, str] | None:
    return (past[1][1], pres[2][1]) if len(past) == 3 and len(pres) == 4 else None


def halqi(k: str) -> bool:
    return k in HALQ


def added(k: int) -> int:
    """أحرفُ الزيادة = طولُ القالب − 3."""

    return len(AWZAN[k].template) - 3


def qalb(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    """و/ي متحرّكةٌ بعد فتحٍ ⇒ ألفٌ ساكنة (قَوَلَ ← قَالَ)."""

    if len(word) >= 2 and word[0][1] == _A and word[1][0] in "وي" and word[1][1] != SUKUN:
        return (word[0], ("ا", SUKUN), *word[2:])
    return word


def naql(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    """حركةُ المعتلّ إلى الساكن قبله (قْوُلُ ← قُولُ)."""

    if len(word) >= 2 and word[0][1] == SUKUN and word[1][0] in "وي" and word[1][1] != SUKUN:
        return ((word[0][0], word[1][1]), (word[1][0], SUKUN), *word[2:])
    return word


def iftaal(root: tuple[str, str, str]) -> tuple[Cell, ...]:
    return fill(AWZAN[17].template, root)


def ibdal(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    """على اِفْتَعَلَ: تاءٌ ⇒ طاءٌ بعد الإطباق، تاءٌ ⇒ دالٌ بعد د/ذ/ز، فاءٌ و/ي ⇒ تاءٌ مدغمة."""

    if len(word) < 3:
        return word
    h, f, t = word[0], word[1], word[2]
    if f[0] in ITBAQ:
        return (h, f, ("ط", t[1]), *word[3:])
    if f[0] in DHZ:
        return (h, f, ("د", t[1]), *word[3:])
    if f[0] in "وي":
        return (h, ("ت", f[1]), t, *word[3:])
    return word


def _check() -> None:
    assert len(ABWAB) == 6 and not set(ABWAB) & set(MISSING)
    assert read_bab(cells_of("ضَرَبَ"), cells_of("يَضْرِبُ")) == (_A, _I)
    assert read_bab(cells_of("فَتَحَ"), cells_of("يَفْتَحُ")) == (_A, _A) and halqi("ح")
    assert [added(k) for k in MAZID] == [1, 1, 1, 2, 2, 2, 2, 2, 3]
    assert qalb(cells_of("قَوَلَ")) == cells_of("قَالَ")
    assert (("ي", _A), *naql(cells_of("قْوُلُ"))) == cells_of("يَقُولُ")
    assert ibdal(iftaal(("ص", "ب", "ر"))) == cells_of("اِصْطَبَرَ")
    assert ibdal(iftaal(("ز", "ه", "ر"))) == cells_of("اِزْدَهَرَ")
    ittasala = ibdal(iftaal(("و", "ص", "ل")))
    assert ittasala == cells_of("اِتْتَصَلَ") and licensed(ittasala)
    assert root_of(AWZAN[0].template, cells_of("نَصَرَ")) == ("ن", "ص", "ر")


_check()
