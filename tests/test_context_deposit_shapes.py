"""شروطُ مبرهنة المودَع قائمةٌ في مودَع المصحف كلِّه (ADR ٣٦).

`HarfBridge.deposit_eq_line_shape` في Algebra (ADR ٧ هناك) تقول: مودَعُ السياق هو السطرُ
المصلَح وقفًا، وصورةُ ابتداء الأولى، وكلُّ كلمةٍ خامٍ بعد «بَ»، **بشرط** كلّ كلمةٍ بعد الأولى
(`CondB`):

* غيرُ فارغة؛
* من الأشكال (`ShapeA`): أوّلُها متحرّك، أو ساكنٌ ليس حرفَ مدّ، أو حرفُ مدٍّ ساكنٌ يليه متحرّك؛
* وصورةُ ابتدائها (`StartB`): هي نفسُها مبتدأةً بمتحرّك، أو همزةٌ متحرّكةٌ قبلها
  (`hamza_prefix`).

هنا مرآةُ الشرطين بايثونًا مكتوبةً من نصّ المبرهنة لا من شيفرة البوّابة، وطفراتُها، ثمّ الفحصُ
على كلّ موقعٍ داخليٍّ جاهزٍ ما قبله جاهز: الكلمةُ بخاناتها في سياقها
(`tools/gen_context_certificates.py`)، وصورةُ ابتداء ما قبلها من البوّابة في سياق الابتداء.
"""

from __future__ import annotations

import importlib.util
import sys

from conftest import ROOT

from gate import Refusal, gate
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


def test_every_interior_position_of_the_quran_satisfies_the_theorem() -> None:
    dep = MOD.generate("quran")
    forms, stream = dep["forms"], dep["stream"]
    start = gate()
    cache: dict[str, Cells | None] = {}
    lines = MOD.lines_of(MOD.CORPUS.read_bytes())
    pos, checked, failures = 0, 0, []
    for tokens in lines:
        prev: Cells | None = None
        for i, _w in enumerate(tokens):
            f = stream[pos][0]
            pos += 1
            word = forms[f]["cells"] if f >= 0 else None
            if i > 0 and word is not None and prev is not None:
                key = repair(tokens[i - 1])[0]
                if key not in cache:
                    cert = start.enter(tokens[i - 1].encode("utf-8"))
                    cache[key] = None if isinstance(cert, Refusal) else MOD.cells_of(cert.atoms)
                s = cache[key]
                if s is not None:
                    checked += 1
                    if not (shape_ok(word) and start_ok(s, prev)):
                        failures.append((tokens[i - 1], tokens[i]))
            prev = word
    assert checked > 70000 and failures == []
