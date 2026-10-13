"""تقسيمُ الكلم والقراءةُ بالفرز (ADR ٥٤) — مرآةُ `A116.Qism`.

الأعدادُ من مخرج Lean (`coverage_counts`: 5، 11، 24؛ `naive_wrong_count`: 5؛
`pairs_length`: 45) لا من هذه الشيفرة. والآخرُ المرئيّ باليد على صورٍ تمرّ بالبوّابة. والطفرات:
`MUTANT_JAMF_LIKE_SAHIH` (جمعُ المؤنّث يُنصب بالفتحة)، `MUTANT_NO_FARIQA` (ألفُ الفارقة تُقرأ
ألفًا)، `MUTANT_TANWIN_ALIF_AS_ALIF` (ألفُ تنوين النصب تُقرأ ألفَ مقصور)،
`MUTANT_READ_ANY_CANDIDATE` (القارئُ يحكم بأوّل مرشَّح فيفقد السلامة).
"""

from __future__ import annotations

import importlib.util
import sys

from conftest import ROOT

from gate import enter, exit
from gate import qism as q

HAND_ENDINGS = {
    "كِتَابٌ": "damma", "كِتَابًا": "fatha", "كِتَابٍ": "kasra", "مُسْلِمَاتٍ": "kasra",
    "الْمُسْلِمِينَ": "ina", "الْمُؤْمِنُونَ": "una", "رَجُلَانِ": "ani", "رَجُلَيْنِ": "ayni",
    "يَدْعُو": "waw", "يَدْعُ": "damma", "يَخْشَى": "alif", "يَفْعَلُونَ": "una", "تَعْلَمُوا": "waw",
    "هُدًى": "alif", "يَكْتُبُ": "damma",
}


def test_counts_equal_lean() -> None:
    assert len(q.PAIRS) == 45
    assert [q.covered(v) for v in (q.blind_view, q.qism_view, q.class_view)] == [5, 11, 24]
    assert sum(1 for c, i in q.PAIRS if q.naive(q.ENDING[c][i]) not in (None, i)) == 5


def test_refinement_never_loses() -> None:
    """`blind_le_qism`، `qism_le_class`: ما يقرؤه الأخشن يقرؤه الألطف بالحالة نفسها."""

    for c, i in q.PAIRS:
        e = q.ENDING[c][i]
        if q.read(q.blind_view, (), e) == i:
            assert q.read(q.qism_view, q.is_ism(c), e) == i
        if q.read(q.qism_view, q.is_ism(c), e) == i:
            assert q.read(q.class_view, c, e) == i


def test_hand_readings() -> None:
    assert q.read(q.class_view, "fMutalW", "damma") == "jazm" and q.naive("damma") == "raf"  # يَدْعُ
    assert q.read(q.blind_view, (), "kasra") is None  # مُسْلِمَاتِ: بلا صنفٍ لا تُقرأ الكسرة
    assert q.read(q.class_view, "iSahih", "kasra") == "jarr"
    assert q.read(q.class_view, "iJamF", "kasra") is None  # نصبٌ وجرٌّ بعلامةٍ واحدة: العاملُ يفصل
    assert q.read(q.qism_view, False, "ina") == "raf" and q.read(q.blind_view, (), "ina") is None


def test_endings_on_certificates() -> None:
    for w, want in HAND_ENDINGS.items():
        cert = enter(w.encode())
        assert q.ending_of(exit(cert).decode()) == want, w


def test_klass_rules() -> None:
    path = ROOT / "tools" / "gen_qac_qism.py"
    spec = importlib.util.spec_from_file_location("gen_qac_qism", path)
    assert spec and spec.loader
    t = importlib.util.module_from_spec(spec)
    sys.modules["gen_qac_qism"] = t
    spec.loader.exec_module(t)
    noun = {"pos": "N", "lem": "x", "root": "ktb", "num": "MD", "person": ""}
    assert t.klass(noun, "ayni", "رَجُلَيْنِ") == "iMuthanna"
    assert t.klass({**noun, "num": "FP"}, "kasra", "مُسْلِمَاتٍ") == "iJamF"
    assert t.klass({**noun, "num": "M", "lem": ">ax"}, "alif", "أَخَا") == "iSitta"
    assert t.klass({**noun, "num": "M"}, "alif", "هُدًى") == "iMaqsur"
    verb = {"pos": "V", "lem": "x", "root": "dEw", "num": "", "person": "3MS"}
    assert t.klass(verb, "damma", "يَدْعُ") == "fMutalW"
    assert t.klass({**verb, "root": "x$y"}, "fatha", "يَخْشَ") == "fMutalAlif"
    assert t.klass({**verb, "root": "dEw"}, "fatha", "يَدْعُوَ") == "fMutalW"
    assert t.klass({**verb, "person": "3MP"}, "una", "يَدْعُونَ") == "fKhamsaW"
    assert t.klass({**verb, "root": "ktb"}, "damma", "يَكْتُبُ") == "fSahih"


def test_mutants_are_caught() -> None:
    # MUTANT_JAMF_LIKE_SAHIH: لو نُصب جمعُ المؤنّث بالفتحة لصار جدولُه جدولَ الصحيح وقرأت الكسرةُ جرًّا
    assert q.ENDING["iJamF"]["nasb"] == "kasra" != q.ENDING["iSahih"]["nasb"]
    # MUTANT_NO_FARIQA: «تَعْلَمُوا» آخرُها ألفُ الفارقة، والآخرُ المرئيّ واو
    assert q.ending_of("تَعْلَمُوا") == "waw" != "alif"
    # MUTANT_TANWIN_ALIF_AS_ALIF: «كِتَابًا» ألفُها ألفُ تنوين، فالآخرُ فتحة
    assert q.ending_of("كِتَابًا") == "fatha"

    # MUTANT_READ_ANY_CANDIDATE: الحكمُ بأوّل مرشَّحٍ يقرأ «مُسْلِمَاتِ» المنصوبة جرًّا
    def first(view: object, k: object, e: str) -> str | None:
        cs = q.cands(view, k, e)  # type: ignore[arg-type]
        return cs[0] if cs else None

    wrong = sum(1 for c, i in q.PAIRS if first(q.class_view, c, q.ENDING[c][i]) not in (None, i))
    assert wrong > 0
    assert all(q.read(q.class_view, c, q.ENDING[c][i]) in (None, i) for c, i in q.PAIRS)
