"""شروطُ مبرهنة المودَع قائمةٌ في مودَع المصحف كلِّه (ADR ٣٦).

`HarfBridge.deposit_eq_line_shape` في Algebra (ADR ٧ هناك) تقول: مودَعُ السياق هو السطرُ
المصلَح وقفًا، وصورةُ ابتداء الأولى، وكلُّ كلمةٍ خامٍ بعد «بَ»، **بشرط** كلّ كلمةٍ بعد الأولى
(`CondB`):

* غيرُ فارغة؛
* من الأشكال (`ShapeA`): أوّلُها متحرّك، أو ساكنٌ ليس حرفَ مدّ، أو حرفُ مدٍّ ساكنٌ يليه متحرّك؛
* وصورةُ ابتدائها (`StartB`): هي نفسُها مبتدأةً بمتحرّك، أو همزةٌ متحرّكةٌ قبلها
  (`hamza_prefix`).

هنا مرآةُ الشرطين بايثونًا مكتوبةً من نصّ المبرهنة لا من شيفرة البوّابة، وطفراتُها، ثمّ الفحصُ
على كلّ موقعٍ داخليٍّ جاهز: الكلمةُ بخاناتها في سياقها (`tools/gen_context_certificates.py`)،
ويسارُها صورةُ ابتداء ما قبلها كما تأخذها البوّابة (`project` في سياق الابتداء)، وحكمُها هو
`strict_joined_repaired` (وقفًا `strict_joined_pause_repaired`) على يسارها وذرّاتها بعينها
(ADR ٣٨)، وهو حكمُ الميزان `machine_join` (ADR ٤٢). وبعد موضعٍ مرفوضٍ تبدأ قطعةٌ يسارُها
صورةُ ابتداء المرفوض (`segment_eq_line`، ADR ٨ في Algebra): يُفحص أنّ اليسارَ موجود.
والمصحفُ في الاختبار السريع، والصحيحان في البطيء (ADR ٣٨).
"""

from __future__ import annotations

import gzip
import importlib.util
import sys

import pytest
from conftest import ROOT

from gate.contextual import Context, project
from gate.licence import repair_junction, strict_joined_pause_repaired, strict_joined_repaired
from gate.mizan import machine_join
from gate.residue import repair

SPEC = importlib.util.spec_from_file_location("gen_context_certificates",
                                              ROOT / "tools" / "gen_context_certificates.py")
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
sys.modules["gen_context_certificates"] = MOD
SPEC.loader.exec_module(MOD)

SUKUN = "سكون"
MADD = "اوي"
Cells = list[list[str]]


def shape_ok(cells: Cells) -> bool:
    """`ShapeA`: أوّلُها حرّ، أو حرفُ مدٍّ ساكنٌ يليه متحرّك."""
    if not cells:
        return False
    first = cells[0]
    if first[1] != SUKUN or first[0] not in MADD:
        return True
    return len(cells) >= 2 and cells[1][1] != SUKUN


def start_ok(start: Cells, word: Cells) -> bool:
    """`StartB` بسابقة الهمزة: هي نفسُها مبتدأةً بمتحرّك، أو همزةٌ متحرّكةٌ قبلها."""
    if start == word:
        return bool(word) and word[0][1] != SUKUN
    return (len(start) == len(word) + 1 and start[1:] == word and start[0][0] == "ء"
            and start[0][1] != SUKUN)


def test_mirror_by_hand() -> None:
    ba, bs = ["ب", "فتح"], ["ب", SUKUN]
    assert shape_ok([ba]) and shape_ok([bs])                     # متحرّك؛ وساكنٌ ليس حرفَ مدّ («بْ»)
    assert shape_ok([["ي", SUKUN], ["م", "ضم"]])                  # «ايْمُ»
    assert not shape_ok([["ا", SUKUN], bs, ba])                   # «اْبْبَ»: الشاهدُ على لزوم الشرط
    assert not shape_ok([["و", SUKUN]]) and not shape_ok([])
    lh = [["ل", SUKUN], ["ح", "فتح"]]
    assert start_ok([["ء", "فتح"], *lh], lh) and start_ok([ba], [ba])
    assert not start_ok(lh, lh) and not start_ok([["ء", SUKUN], *lh], lh)


def test_mutants_are_caught() -> None:
    def mutant_any_madd(cells: Cells) -> bool:   # MUTANT_MADD_START_ALWAYS_OK
        return bool(cells)

    def mutant_bare_prefix(start: Cells, word: Cells) -> bool:   # MUTANT_ANY_PREFIX
        return start == word or start[1:] == word

    witness = [["ا", SUKUN], ["ب", SUKUN], ["ب", "فتح"]]
    assert mutant_any_madd(witness) != shape_ok(witness)
    lh = [["ل", SUKUN], ["ح", "فتح"]]
    assert mutant_bare_prefix([["ء", SUKUN], *lh], lh) != start_ok([["ء", SUKUN], *lh], lh)


MARK = {v: k for k, v in MOD.STATE.items()}


def _atoms(cells: Cells) -> tuple[str, ...]:
    return tuple(c + MARK[st] for c, st in cells)


def _check(name: str) -> dict[str, int]:
    """كلُّ موقعٍ داخليٍّ جاهز: شكلُه، وصورةُ ابتداء ما قبله (يسارُ القطعة) موجودة، وحكمُه هو
    `strict_joined_repaired` على يساره وذرّاته بعينها؛ وإن كان ما قبله جاهزًا فصورتُه `StartB` معه."""

    dep = MOD.generate(name)
    forms, stream = dep["forms"], dep["stream"]
    raw = MOD.CORPORA[name].read_bytes()
    if MOD.CORPORA[name].name.endswith(".gz"):
        raw = gzip.decompress(raw)
    cache: dict[str, tuple[str, ...] | None] = {}
    pos = 0
    n = {"checked": 0, "after_refusal": 0}
    failures: list[tuple[str, str, str]] = []
    for tokens in MOD.lines_of(raw):
        prev: Cells | None = None
        for i, _w in enumerate(tokens):
            f, exit_ = stream[pos][0], stream[pos][1]
            pos += 1
            word = forms[f]["cells"] if f >= 0 else None
            if i > 0 and word is not None:
                key = repair(tokens[i - 1])[0]
                if key not in cache:
                    d = project(key, Context())
                    cache[key] = tuple(d["atoms"]) if d["status"] == "READY" else None
                left = cache[key]
                n["checked"] += 1
                if left is None:
                    failures.append(("NO_LEFT", tokens[i - 1], tokens[i]))
                    prev = word
                    continue
                verdict = strict_joined_pause_repaired if exit_ == 1 else strict_joined_repaired
                if not shape_ok(word):
                    failures.append(("SHAPE", tokens[i - 1], tokens[i]))
                if not verdict(left, _atoms(word)):
                    failures.append(("VERDICT", tokens[i - 1], tokens[i]))
                if not machine_join(repair_junction(left, _atoms(word))[0], _atoms(word),
                                    exit_ == 1):
                    failures.append(("MIZAN", tokens[i - 1], tokens[i]))
                if prev is None:
                    n["after_refusal"] += 1
                elif not start_ok(MOD.cells_of(left), prev):
                    failures.append(("START", tokens[i - 1], tokens[i]))
            prev = word
    assert failures == [], failures[:5]
    return n


def test_every_interior_position_of_the_quran_satisfies_the_theorem() -> None:
    n = _check("quran")
    assert n["checked"] > 70000


@pytest.mark.slow
def test_every_interior_position_of_the_sahihain_satisfies_the_theorem() -> None:
    """الصحيحان (~7 دقائق): مودَعُهما بسياقه يُولَّد ثمّ يُفحص كالمصحف."""

    n = _check("sahihain")
    assert n["checked"] > 980000
