"""سجلُّ الانتقالات: كلُّ دالّةٍ عامّة ‎Word → Word‎ في الشجرة مسجَّلةٌ، ومبرهنتُها مدقَّقة أو دَينُها
مسمًّى؛ الحارسُ يرفض بالاسم غيرَ المسجَّل والمبرهنةَ الوهميّة؛ والجدولُ في Lean مطابقٌ للسجلّ."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

from slge.intiqal import KINDS, REGISTRY, Intiqal

ROOT = Path(__file__).resolve().parent.parent


def _tool() -> ModuleType:
    spec = importlib.util.spec_from_file_location("gen_intiqal_index",
                                                  ROOT / "tools" / "gen_intiqal_index.py")
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_every_transition_is_registered_and_its_theorem_audited() -> None:
    g = _tool()
    assert g.problems() == []
    found = set(g.transitions())
    assert found == {(r.module, r.function) for r in REGISTRY} and len(found) == len(REGISTRY)
    ax = g.audited()
    assert all(r.theorem in ax for r in REGISTRY if r.theorem)
    assert all(r.note for r in REGISTRY if r.kind == "—")
    assert set(KINDS) == {r.kind for r in REGISTRY}
    # الإغلاقُ بمبرهنةٍ تحفظ الترخيصَ أو تردّ بعينه؛ لا إغلاقَ بلا مبرهنة
    assert all(r.theorem for r in REGISTRY if r.kind == "إغلاق")
    assert any(r.theorem == "Slge.Zuruf.setLast_licensed" and r.kind == "إغلاق" for r in REGISTRY)


def test_lean_table_mirrors_the_registry() -> None:
    text = (ROOT / "formal" / "Slge" / "IntiqalTable.lean").read_text(encoding="utf-8")
    for r in REGISTRY:
        assert f'("{r.module}", "{r.function}", "{r.theorem}", {KINDS.index(r.kind)})' in text
    assert f"registry.length = {len(REGISTRY)}" in text


def test_mutants_are_refused() -> None:
    g = _tool()
    ax = g.audited()
    # مبرهنةٌ وهميّة لا تمرّ
    fake = Intiqal("zuruf", "set_last", "Slge.Zuruf.no_such_theorem", "إغلاق")
    assert fake.theorem not in ax
    # دالّةٌ غيرُ موجودة في الشجرة
    assert ("zuruf", "no_such_function") not in set(g.transitions())
