"""حكمُ الموصول في البوّابة هو `strictJoinB` بعينه
(ADR ٣٨، سدُّ `GATE_JOINED_VS_STRICTJOINB_UNPROVEN`).

`Gate.enter` بسياق `joined` يحكم بـ`gate.licence.joined_failure` وحدَه على
`repair_junction(left) + atoms`:

١. على جدول Lean `hadd-join` كلِّه (293,904 زوجًا، أعمدتُه من `Hadd.strictJoinB`/`strictJoinPauseB`
   في النواة):
   الحكمُ «لا رفض» هو عمودُ Lean بعينه وصلًا ووقفًا — والتوقّعُ من الجدول المولَّد لا من الشيفرة.
٢. الشرطُ الساقط من ثلاثةٍ مغلقة بترتيبها: الثلاثيُّ، ثمّ القيد، ثمّ قطعُ الحدّ — وكلٌّ بشرطه.
٣. طفرتان مسمّاتان (حكمٌ بلا فحص القطع، وحكمٌ بلا القيد) يلتقطهما الجدول.
٤. البوّابةُ نفسُها: ترفض بالاسم المسمّى لشرط `joined_failure` الساقط على ذرّاتها بعينها، وتقبل
   بوجهٍ مسمًّى حيث لا شرطَ ساقط، بشواهدَ باليد.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

import pytest
from conftest import ROOT

from gate import Refusal, enter
from gate.api import Context
from gate.licence import (
    continue_licensed,
    hadd_ok,
    hadd_pause_ok,
    joined_failure,
    kind_of,
    pause_licensed,
    repair_junction,
)

JOIN_TABLE = ROOT / "formal" / "a116" / "hadd-join.csv"
Row = tuple[tuple[str, ...], tuple[str, ...], bool, bool]


def _rows() -> list[Row]:
    out = []
    with JOIN_TABLE.open(encoding="utf-8") as fh:
        for line in fh:
            pair, _strict, joined, pause = line.rstrip("\n").split(",")
            left, right = pair.split("|")
            out.append((tuple(left.split(" ")), tuple(right.split(" ")), joined == "true",
                        pause == "true"))
    return out


ROWS = _rows()


def test_gate_verdict_is_lean_strict_join_on_the_whole_table() -> None:
    assert len(ROWS) == 293904
    for left, right, joined, pause in ROWS:
        assert (joined_failure(left, right, False) is None) == joined, (left, right)
        assert (joined_failure(left, right, True) is None) == pause, (left, right)


def test_failed_condition_is_named_by_its_own_check() -> None:
    """الشرطُ الساقطُ هو الأوّلُ بالترتيب: الثلاثيُّ يسقط وحدَه، ثمّ القيدُ بعد الثلاثيّ، ثمّ القطعُ بعدهما."""

    seen = set()
    for left, right, _, _ in ROWS:
        k = kind_of(left + right)
        for pause in (False, True):
            f = joined_failure(left, right, pause)
            tern = pause_licensed(k) if pause else continue_licensed(k)
            hadd = (hadd_pause_ok if pause else hadd_ok)(left + right)
            assert (f == "ternary") == (not tern)
            assert (f == "hadd") == (tern and not hadd)
            seen.add(f)
    assert seen == {None, "ternary", "hadd", "straddle"}


def _mut_no_straddle(left: Sequence[str], right: Sequence[str], pause: bool) -> str | None:
    """`MUTANT_NO_STRADDLE_CHECK`: الحكمُ بلا فحص قطع الحدّ."""

    f = joined_failure(left, right, pause)
    return None if f == "straddle" else f


def _mut_no_hadd(left: Sequence[str], right: Sequence[str], pause: bool) -> str | None:
    """`MUTANT_NO_HADD`: الثلاثيُّ وحدَه بلا قيد الحدّ."""

    k = kind_of(tuple(left) + tuple(right))
    return None if (pause_licensed(k) if pause else continue_licensed(k)) else "ternary"


@pytest.mark.parametrize("mutant", [_mut_no_straddle, _mut_no_hadd],
                         ids=["MUTANT_NO_STRADDLE_CHECK", "MUTANT_NO_HADD"])
def test_table_catches_named_mutants(
        mutant: Callable[[Sequence[str], Sequence[str], bool], str | None]) -> None:
    assert any((mutant(left, right, False) is None) != joined for left, right, joined, _ in ROWS)


def w(s: str) -> tuple[str, ...]:
    return tuple(s.split(" "))


def _joined(left: str, word: str, exit_: str = "continue") -> object:
    return enter(word.encode(), Context(entry="joined", exit=exit_, left=left))


def test_gate_refuses_by_the_failed_condition() -> None:
    """البوّابةُ تقبل حيث لا شرطَ ساقط، وترفض بالاسم المسمّى للشرط الساقط."""

    tilka = _joined("قُلِ", "تِلْكَ")
    assert not isinstance(tilka, Refusal) and tilka.atoms == w("تِ لْ كَ")
    left_atoms, junction = repair_junction(w("ءَ لْ رْ"), tilka.atoms)
    assert junction is None
    r = _joined("الر", "تِلْكَ")
    assert isinstance(r, Refusal) and r.status == "REJECT"
    assert joined_failure(left_atoms, tilka.atoms, False) == "ternary"
    assert r.reasons == ("JUNCTION_NOT_LICENSED",)
    ardi, sirat, mursalun = "الْأَرْضِ", "الصِّرَاطَ", "الْمُرْسَلُونَ"  # برسم المدوّنة (كما في test_iltiqa)
    for left, word, exit_ in (("فِي", ardi, "continue"), ("اهْدِنَا", sirat, "continue"),
                              ("لُوطٍ", mursalun, "pause")):
        c = _joined(left, word, exit_)
        assert not isinstance(c, Refusal) and c.junction is not None
        s = enter(left.encode())
        assert not isinstance(s, Refusal)
        la, j = repair_junction(s.atoms, c.atoms)
        assert j == c.junction and joined_failure(la, c.atoms, exit_ == "pause") is None
