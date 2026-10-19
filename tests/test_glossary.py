"""معجمُ الاصطلاح (`tools/gen_glossary.py`): كلُّ مدخلٍ بمرساةٍ موجودة، وكلُّ وسمٍ ونوعٍ ومرتبةٍ بمدخل،
ولا مدخلَ بلا استعمال؛ والطفراتُ تُرفض باسمها."""

from __future__ import annotations

import importlib.util
import sys

from conftest import ROOT

SPEC = importlib.util.spec_from_file_location("gen_glossary", ROOT / "tools" / "gen_glossary.py")
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
sys.modules["gen_glossary"] = MOD
SPEC.loader.exec_module(MOD)


def test_glossary_is_generated_and_every_anchor_exists() -> None:
    assert MOD.problems() == []
    assert (ROOT / "GLOSSARY.md").read_text(encoding="utf-8") == MOD.render()
    assert len(MOD.TERMS) >= 30 and any(t.name == "الـ116" for t in MOD.TERMS)


def test_mutations_are_refused_by_name(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    t = MOD.TERMS[0]
    ghost = t._replace(name="OntologyHierarchy", latin="ontology",
                       where="formal/a116/A116/OntologyHierarchy.lean")
    monkeypatch.setattr(MOD, "TERMS", (*MOD.TERMS, ghost))
    ps = MOD.problems()
    assert any("HALLUCINATED_REFERENCE" in p and "OntologyHierarchy" in p for p in ps)
    assert any("ENTRY_WITHOUT_USE" in p and "OntologyHierarchy" in p for p in ps)

    bad_anchor = t._replace(name="بتٌّ مزعوم", anchor="هذه الجملةُ ليست في الملفّ")
    monkeypatch.setattr(MOD, "TERMS", (*MOD.TERMS[1:], bad_anchor))
    assert any("HALLUCINATED_REFERENCE" in p and "بتٌّ مزعوم" in p for p in MOD.problems())

    monkeypatch.setattr(MOD, "TERMS", tuple(x for x in MOD.TERMS if x.name != "الأوسمة الخمسة"))
    assert any("TERM_WITHOUT_ENTRY" in p and p.startswith("مبرهن") for p in MOD.problems())
