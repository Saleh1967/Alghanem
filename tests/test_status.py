"""السجلّ: لكلّ دعوى سندٌ موجود، ولا يُقال ما لا سندَ له."""

from __future__ import annotations

import ast
import re

from conftest import ROOT
from slge.status import LEDGER, Status

_LEAN = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "formal" / "Slge").glob("*.lean"))
_AUDIT = (ROOT / "formal" / "Audit.lean").read_text(encoding="utf-8")


def _test_names(rel: str) -> set[str]:
    tree = ast.parse((ROOT / rel).read_text(encoding="utf-8"))
    return {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}


def test_ids_are_unique() -> None:
    ids = [c.claim_id for c in LEDGER]
    assert len(ids) == len(set(ids))


def test_every_support_exists() -> None:
    for c in LEDGER:
        for s in c.support:
            kind, _, ref = s.partition(":")
            if kind == "lean":
                short = ref.rsplit(".", 1)[-1]
                assert re.search(rf"\b(theorem|def)\s+{re.escape(short)}\b", _LEAN), s
                assert f"#print axioms {ref}\n" in _AUDIT, s
            elif kind == "test":
                path, _, name = ref.partition("::")
                assert name in _test_names(path), s
            else:
                raise AssertionError(f"سندٌ مجهولُ النوع: {s}")


def test_status_needs_matching_support() -> None:
    for c in LEDGER:
        kinds = {s.partition(":")[0] for s in c.support}
        if c.status is Status.مبرهن:
            assert "lean" in kinds, c.claim_id
        if c.status in (Status.مفحوص_استقصاء, Status.مفحوص_بعينة):
            assert "test" in kinds, c.claim_id
        if c.status is Status.مفتوح:
            assert c.note or c.support, c.claim_id


def test_status_md_is_current() -> None:
    import importlib.util

    spec = importlib.util.spec_from_file_location("gen_status", ROOT / "tools" / "gen_status.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert (ROOT / "STATUS.md").read_text(encoding="utf-8") == mod.render()
