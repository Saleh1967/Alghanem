"""سجلُّ الرفض: كلُّ اسمِ رفضٍ تُطلقه البوّابة مرسًى في Lean/GLOSSARY أو معلَنٌ بصنفه — والطفراتُ تُلتقط:
اسمٌ مزروعٌ بلا مرساةٍ ولا إعلان، وإعلانٌ لاسمٍ لا يُطلَق، وإعلانٌ لاسمٍ له مرساة."""

from __future__ import annotations

import ast
import importlib.util
import sys
from pathlib import Path

from gate import Refusal, enter

ROOT = Path(__file__).resolve().parents[1]


def _tool():
    spec = importlib.util.spec_from_file_location("gen_refusals",
                                                  ROOT / "tools" / "gen_refusals.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen_refusals"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_every_emitted_refusal_is_anchored_or_declared_and_the_registry_is_current() -> None:
    m = _tool()
    assert m.problems() == []
    assert (ROOT / "REFUSALS.md").read_text(encoding="utf-8") == m.render()
    em, an = m.emitted(), m.anchors()
    assert set(an) | set(m.DECLARED) >= set(em) and not (set(an) & set(m.DECLARED))
    # الرفضُ الحيّ من الواجهة يُطلق أسماءً من السجلّ لا غير
    for data, name in ((b"\xff", "NOT_UTF8"), ("كَتَبَ كَتَبَ".encode(), "NOT_ONE_TOKEN"),
                       ("الم".encode(), "UNVOCALIZED_WORD_IS_NEVER_GUESSED"),
                       ("دَاَ".encode(), "BARE_ALIF_OWN_MARK_NOT_LICENSED")):
        r = enter(data)
        assert isinstance(r, Refusal) and name in r.reasons and name in em, name
    # الألفُ: كانت سياسةً بلا تعريف؛ الآن مرساتُها A116.Alif
    assert "BARE_ALIF_OWN_MARK_NOT_LICENSED" in an


def test_mutations_are_caught() -> None:
    m = _tool()
    # (١) اسمٌ مزروع بلا مرساةٍ ولا إعلان
    planted = ast.parse('def f():\n    return _reject("PLANTED_REFUSAL_WITHOUT_ANCHOR")\n')
    assert "PLANTED_REFUSAL_WITHOUT_ANCHOR" in m._names_in(planted)
    orig = m.emitted
    m.emitted = lambda: {**orig(), "PLANTED_REFUSAL_WITHOUT_ANCHOR": ["x.py"]}
    assert any("REFUSAL_WITHOUT_ANCHOR" in p for p in m.problems())
    m.emitted = orig
    # (٢) إعلانٌ لاسمٍ لا يُطلَق، و(٣) إعلانٌ لاسمٍ له مرساة
    m.DECLARED["NEVER_EMITTED"] = ("واجهة", "x")
    m.DECLARED["CVVC_NOT_GEMINATE"] = ("حدّ", "x")
    ps = m.problems()
    assert sum("STALE_DECLARED_REFUSAL" in p for p in ps) == 2
    del m.DECLARED["NEVER_EMITTED"], m.DECLARED["CVVC_NOT_GEMINATE"]
    assert m.problems() == []
