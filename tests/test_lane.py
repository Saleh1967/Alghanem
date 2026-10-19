"""المجالُ المعلَنُ الرابع — معجمُ لين (ADR ٣٣): الختم، والاستخراج، والوزنُ من الشهادة.

التوقّعاتُ مكتوبةٌ باليد لا محسوبةٌ بالأداة: رموزُ مدخلٍ مصنوعة، وذرّاتٌ مكتوبة، وأوزانٌ متوقَّعة. والطفراتُ
بأسمائها تُبدَّل في نسخةٍ من الأداة فتسقط توقّعاتٌ بعينها:
`MUTANT_SEP_ANY_TEXT` (الفاصلُ يقبل أيَّ نصّ)، `MUTANT_ARROW_IS_SPAN` (الإحالةُ ↓ تُعدّ وسمًا)،
`MUTANT_KEEP_CASE` (حركةُ الإعراب الأخيرة تبقى في الوزن)، `MUTANT_TRANSITIVE_IGNORED` (التعديةُ لا
تُقرأ).
"""

from __future__ import annotations

import gzip
import hashlib
import importlib.util
import sys
from typing import Any

from conftest import ROOT

from gate.api import LANE_CORPUS, LANE_LINES_SHA256, SEALED_CORPORA, Gate
from gate.residue import repair

SPEC = importlib.util.spec_from_file_location("gen_lane", ROOT / "tools" / "gen_lane.py")
assert SPEC and SPEC.loader
MOD: Any = importlib.util.module_from_spec(SPEC)
sys.modules["gen_lane"] = MOD
SPEC.loader.exec_module(MOD)

FA, KA, DA, SU = "َ", "ِ", "ُ", "ْ"

ENTRY = [
    ("t", ", aor. "), ("ar", "كَتُبَ"), ("t", ", inf. n. "), ("ar", "كَتْبٌ"), ("t", " and "),
    ("ar", "كِتَابٌ"), ("t", " (S, K) and "), ("ar", "كِتَابَةٌ"), ("t", "; (Msb;) the first agreeable "),
    ("ar", "كِتْبَةٌ"),
]
ARROW = [("t", " inf. n. "), ("ar", "ضَرْبٌ"), ("t", " and "), ("arrow", "ضرّبهُ"), ("t", " and "),
         ("ar", "ضِرَابٌ")]
PLURALS = [("t", "a pl., rarely a sing.: the pl. pl. "), ("ar", "أَكَالِبُ"),
           ("t", "; and pl. [of pauc.] "), ("ar", "أَكْلُبٌ"), ("t", " and [of mult.] "),
           ("ar", "كِلَابٌ"), ("t", " which may be pl. of "), ("ar", "كَلْبَةٌ")]


def test_lines_are_sealed_and_regenerated() -> None:
    raw = gzip.decompress(LANE_CORPUS.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == LANE_LINES_SHA256 == SEALED_CORPORA[LANE_CORPUS.name]
    assert MOD.render(MOD.lines()) == raw
    assert len(MOD.LANE_SOURCES) == 38 and MOD.LANE_COMMIT.startswith("7dd04e1")


def test_spans_after_stops_at_prose_and_arrow() -> None:
    assert MOD.spans_after(ENTRY, MOD.INF) == ["كَتْبٌ", "كِتَابٌ", "كِتَابَةٌ"]
    assert MOD.spans_after(ARROW, MOD.INF) == ["ضَرْبٌ"]
    # «a pl.,» لا يليها وسم، و«pl. pl.» جمعُ الجمع: الأوّلُ الصحيح «pl. [of pauc.]»
    assert MOD.spans_after(PLURALS, MOD.PL) == ["أَكْلُبٌ", "كِلَابٌ"]


def test_cited_noun_and_verb_class() -> None:
    assert MOD.cited_noun("كَتْبٌ") and MOD.cited_noun("أَكَالِبُ") and MOD.cited_noun("كَسْرَى")
    assert not MOD.cited_noun("كَسُدَ") and not MOD.cited_noun("كَتَبَ عَنْهُ")
    vp = f"1{FA} 2{DA} 3"
    assert MOD.verb_class(vp, "1") == "u"  # فَعُلَ لا يكون إلّا لازمًا
    assert MOD.verb_class(f"1{FA} 2{FA} 3", "1") == "transitive"
    assert MOD.verb_class(f"1{FA} 2{KA} 3", "0") == "intransitive_i"
    assert MOD.verb_class(f"1{FA} 2{FA} 3", "0") == "intransitive_a"
    assert MOD.verb_class(f"1{DA} 2{KA} 3", "0") is None  # مبنيٌّ للمجهول: ليس فَعَلَ


def test_pattern_from_certificate_atoms() -> None:
    word = "كِتَابَةٌ"
    gate = Gate(corpus=LANE_CORPUS, domain={repair(word)[0], repair("أَكْلُبٌ")[0]})
    atoms = gate.enter(word.encode()).atoms
    assert atoms == ("كِ", "تَ", "اْ", "بَ", "تُ", "نْ")
    assert MOD.pattern(atoms, "كتب", word) == f"1{KA} 2{FA} ا{SU} 3{FA} ة"
    assert MOD.pattern(("ءَ", "كْ", "لُ", "بُ", "نْ"), "كلب", "أَكْلُبٌ") == f"ء{FA} 1{SU} 2{DA} 3"
    assert MOD.pattern(("كَ", "تَ", "بَ"), "كتب", "كَتَبَ") == f"1{FA} 2{FA} 3"
    assert MOD.pattern(("كَ", "تَ", "بَ"), "كلب", "كَتَبَ") is None
    assert gate.enter("زَيْدٌ".encode()).status == "OUTSIDE_DECLARED_DOMAIN"


def _mutant(old: str, new: str) -> Any:
    src = (ROOT / "tools" / "gen_lane.py").read_text(encoding="utf-8")
    assert old in src
    ns: dict[str, Any] = {"__name__": "gen_lane_mutant", "__file__": str(ROOT / "tools" / "x.py")}
    exec(compile(src.replace(old, new, 1), "gen_lane_mutant", "exec"), ns)  # noqa: S102
    return ns


def test_named_mutants_are_caught() -> None:
    m = _mutant('SEP = re.compile(r"^(?:', 'SEP = re.compile(r"^(?:.|')  # MUTANT_SEP_ANY_TEXT
    assert m["spans_after"](ENTRY, m["INF"]) != ["كَتْبٌ", "كِتَابٌ", "كِتَابَةٌ"]
    # MUTANT_ARROW_IS_SPAN
    m = _mutant('if k2 != "ar" or not SEP.match(sep):', "if not SEP.match(sep):")
    assert m["spans_after"](ARROW, m["INF"]) != ["ضَرْبٌ"]
    m = _mutant("    out[-1] = base\n", "")  # MUTANT_KEEP_CASE
    assert m["pattern"](("ءَ", "كْ", "لُ", "بُ", "نْ"), "كلب", "أَكْلُبٌ") != f"ء{FA} 1{SU} 2{DA} 3"
    m = _mutant('    if transitive == "1":\n', '    if False:\n')  # MUTANT_TRANSITIVE_IGNORED
    assert m["verb_class"](f"1{FA} 2{FA} 3", "1") != "transitive"
