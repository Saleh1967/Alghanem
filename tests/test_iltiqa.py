"""التقاءُ الساكنين على الحدّ (`A116.Iltiqa`): ثلاثةُ أوجهٍ مسمّاة في آخر الكلمة الأولى — الألفُ الفارقة
تسقط، حرفُ المدّ يُحذف، الساكنُ يُكسَر — والثانيةُ لا تُمسّ.

١. المطابقة: `gate.licence.repair_junction` و`strict_joined_repaired`
   و`strict_joined_pause_repaired` = `Iltiqa.repair` و`strictJoinRepairedB`
   و`strictJoinPauseRepairedB` على كلّ سطرٍ من `lake exe a116-table iltiqa` (360,000 زوجًا من ستّة
   حواملَ × أربع حالات).
٢. الطفرات: ثلاثُ مرايا خاطئةٍ مسمّاة يُسقطها الجدول — لا ألفَ فارقة، ولا حذفَ مدٍّ (الكسرُ للكلّ)، والإصلاحُ
   قبل متحرّك.
٣. الشواهد: توقّعاتٌ من الكتاب لا من الشيفرة (فِي الْأَرْضِ ← فِلْأَرْضِ؛ اشْتَرَوُا الضَّلَالَةَ؛ لُوطٍ
   الْمُرْسَلُونَ ← لُوطِنِ…؛ ولا إصلاحَ لِـ«قُلِ الْحَمْدُ» ولا لِـ«الر تِلْكَ»).
٤. البوّابة: ما كان يُرفض `JUNCTION_NOT_LICENSED`/`CVVC_NOT_GEMINATE`/`CVVC_ACROSS_WORD_BOUNDARY` على
   الحدّ يُرخَّص بوجهٍ مسمًّى تحمله الشهادة (`Certificate.junction`)، وذرّاتُ الكلمة الثانية كما هي؛ والحروفُ
   المقطّعة تبقى مرفوضة.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from pathlib import Path

import pytest

from gate import Refusal, enter
from gate.contextual import Context
from gate.licence import (
    REPAIRS,
    kind_of,
    repair_junction,
    strict_joined,
    strict_joined_pause,
    strict_joined_pause_repaired,
    strict_joined_repaired,
)

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "formal" / "a116" / "iltiqa.csv"


def w(s: str) -> tuple[str, ...]:
    return tuple(s.split())


Row = tuple[tuple[str, ...], tuple[str, ...], str, tuple[str, ...], bool, bool, bool]


def _rows() -> list[Row]:
    out = []
    with TABLE.open(encoding="utf-8") as fh:
        for line in fh:
            pair, tag, repaired, sj, sjr, sjpr = line.rstrip("\n").split(",")
            left, right = pair.split("|")
            out.append((tuple(left.split(" ")), tuple(right.split(" ")), tag,
                        tuple(repaired.split(" ")) if repaired else (), sj == "true",
                        sjr == "true", sjpr == "true"))
    return out


def test_python_mirror_matches_lean_iltiqa_table() -> None:
    rows = _rows()
    assert len(rows) == 360000
    for left, right, tag, repaired, sj, sjr, sjpr in rows:
        new_left, t = repair_junction(left, right)
        assert (t or "-") == tag and new_left == repaired, (left, right)
        assert strict_joined(left, right) == sj, (left, right)
        assert strict_joined_repaired(left, right) == sjr, (left, right)
        assert strict_joined_pause_repaired(left, right) == sjpr, (left, right)
        assert not sj or sjr, (left, right)  # الإصلاحُ لا يُسقط مقبولًا: بلا التقاءٍ لا يفعل شيئًا


def _mut_no_farq(left: Sequence[str], right: Sequence[str]) -> str:
    """الطفرة ١ (`MUTANT_NO_FARQ_ALIF`): الألفُ الفارقة تُعامَل كأيّ ساكن (تُكسَر)."""

    if not (right and right[0][1] == "ْ" and left and left[-1][1] == "ْ"):
        return "-"
    if kind_of(left)[-1] == "v":
        return "MADD_DROPPED"
    return "SAKIN_KASRA"


def _mut_kasra_for_all(left: Sequence[str], right: Sequence[str]) -> str:
    """الطفرة ٢ (`MUTANT_KASRA_FOR_MADD`): لا حذفَ مدّ — كلُّ ساكنٍ يُكسَر."""

    if not (right and right[0][1] == "ْ" and left and left[-1][1] == "ْ"):
        return "-"
    if len(left) >= 2 and left[-1] == "اْ" and left[-2] == "وُ":
        return "FARQ_ALIF_DROPPED"
    return "SAKIN_KASRA"


def _mut_before_vowel_too(left: Sequence[str], right: Sequence[str]) -> str:
    """الطفرة ٣ (`MUTANT_REPAIR_BEFORE_VOWEL`): الإصلاحُ ولو كانت الثانيةُ تبدأ بمتحرّك."""

    if not (left and left[-1][1] == "ْ"):
        return "-"
    return repair_junction(left, ("لْ",))[1] or "-"


@pytest.mark.parametrize(
    "mutant", [_mut_no_farq, _mut_kasra_for_all, _mut_before_vowel_too],
    ids=["MUTANT_NO_FARQ_ALIF", "MUTANT_KASRA_FOR_MADD", "MUTANT_REPAIR_BEFORE_VOWEL"],
)
def test_lean_table_rejects_named_mutants(
    mutant: Callable[[Sequence[str], Sequence[str]], str],
) -> None:
    wrong = sum(1 for left, right, tag, *_ in _rows() if mutant(left, right) != tag)
    assert wrong > 0


def test_named_witnesses_with_independent_expectations() -> None:
    """الكتابُ (JK006989 المختوم في SLGE): «تحذف الياء لالتقاء الساكنين» (س14719)، «لا يكون بعد الألف
    حرف ساكن ليس بمدغم» (س14318)، و«أن يكون الساكن الأول مكسورا … لأن التنوين ساكن وقع بعده حرف
    ساكن» (س17600–17602)؛ والألفُ الفارقة لا نطقَ لها."""

    assert repair_junction(w("فِ يْ"), w("لْ ءَ رْ ضِ")) == (w("فِ"), "MADD_DROPPED")  # fi_lardi
    assert strict_joined_repaired(w("فِ يْ"), w("لْ ءَ رْ ضِ"))
    assert not strict_joined(w("فِ يْ"), w("لْ ءَ رْ ضِ"))
    assert repair_junction(w("ءِ لَ اْ"), w("سْ سَ مَ اْ ءِ"))[1] == "MADD_DROPPED"  # ila_ssamai
    assert strict_joined_repaired(w("ءِ لَ اْ"), w("سْ سَ مَ اْ ءِ"))
    ishtarawu = w("ءِ شْ تَ رَ وُ اْ")
    assert repair_junction(ishtarawu, w("ضْ ضَ"))[1] == "FARQ_ALIF_DROPPED"  # ishtarawu_ddalalata
    assert repair_junction(ishtarawu, w("ضْ ضَ"))[0] == ishtarawu[:-1]
    lutin, lmurs = w("لُ وْ طِ نْ"), w("لْ مُ رْ سَ لُ وْ نْ")
    assert repair_junction(lutin, lmurs) == (w("لُ وْ طِ نِ"), "SAKIN_KASRA")  # lutin_lmursalun
    assert not strict_joined_pause(lutin, lmurs) and strict_joined_pause_repaired(lutin, lmurs)
    # لا إصلاحَ بلا التقاء (no_repair_without_clash)
    assert repair_junction(w("فِ يْ"), w("يَ وْ مِ")) == (w("فِ يْ"), None)
    assert repair_junction(w("قُ لِ"), w("لْ حَ مْ دُ")) == (w("قُ لِ"), None)
    assert repair_junction(w("ءَ لْ رْ"), w("تِ لْ كَ")) == (w("ءَ لْ رْ"), None)
    assert not strict_joined_repaired(w("ءَ لْ رْ"), w("تِ لْ كَ"))
    assert REPAIRS == ("FARQ_ALIF_DROPPED", "MADD_DROPPED", "SAKIN_KASRA")


def test_gate_licenses_junctions_by_a_named_repair_and_leaves_the_word_untouched() -> None:
    def joined(left: str, word: str, exit_: str = "continue") -> object:
        return enter(word.encode(), Context(entry="joined", exit=exit_, left=left))

    ardi = "الْأَرْضِ"  # الْأَرْضِ برسم المدوّنة
    c = joined("فِي", ardi)
    assert not isinstance(c, Refusal) and c.junction == "MADD_DROPPED"
    assert c.atoms == w("لْ ءَ رْ ضِ")  # ذرّاتُ الكلمة الثانية كما هي
    assert joined("قُلِ", ardi).junction is None  # type: ignore[union-attr]
    sirat = "الصِّرَاطَ"  # الصِّرَاطَ
    c = joined("اهْدِنَا", sirat)  # كان CVVC_ACROSS_WORD_BOUNDARY
    assert not isinstance(c, Refusal) and c.junction == "MADD_DROPPED"
    dalala = "الضَّلَالَةَ"  # الضَّلَالَةَ
    c = joined("اشْتَرَوُا", dalala)
    assert not isinstance(c, Refusal) and c.junction == "FARQ_ALIF_DROPPED"
    mursalun = "الْمُرْسَلُونَ"
    c = joined("لُوطٍ", mursalun, "pause")  # كان NOT_PAUSE_LICENSED
    assert not isinstance(c, Refusal) and c.junction == "SAKIN_KASRA" and c.atoms[-1] == "نْ"
    r = joined("الر", "تِلْكَ")  # الحروفُ المقطّعة: الساكنان في الأولى نفسِها
    assert isinstance(r, Refusal) and r.reasons == ("JUNCTION_NOT_LICENSED",)
    start = enter(ardi.encode())
    assert not isinstance(start, Refusal) and start.junction is None
