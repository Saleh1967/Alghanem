"""الفراكتالُ بقيد الحدّ وإصلاح الوصل (`A116.FractalHadd`، `A116.FractalMushaf`، ADR ٧٨).

التوقّعاتُ المستقلّة، على المصحف كلِّه:
١. **السطرُ وأزواجُه**: كلُّ آيةٍ أجازت البوّابةُ كلَّ موقعٍ فيها في سياقه (حكمُ الزوج: اليسرى
   بصورة ابتدائها واليمنى موصولةً بعد الإصلاح، `gate.enter` بـ`Context`) تقبلها آلةُ الحرف على
   السطر كلِّه وقفًا بحدّها بعد الإصلاح — حكمان من شيفرتين: أزواجُ البوّابة وطيُّ السطر.
٢. **FOR = الاستقراء**: طيُّ السطر يساريًّا كلمةً كلمة يساوي تعريفَه الاستقرائيّ (`Harf.runLine`).
٣. **الإصلاحُ ينهي اليسرى بمتحرّك**: في كلّ حدٍّ مُصلَح آخرُ ذرّات اليسرى ليس ساكنًا.
٤. **الطفرات**: بلا إصلاحٍ تُرفض آياتٌ جاهزة (`MUTANT_NO_REPAIR`)؛ وبحدٍّ هويّةٍ يُقبل
   «يَا + الشَّافِعِينَ» (`MUTANT_HADD_IDENTITY`)؛ والعطفُ «أو» بين الآيات يقبل نصًّا فيه سطرٌ
   مرفوض (`MUTANT_TEXT_OR`).
"""

from __future__ import annotations

import importlib.util
from functools import reduce
from pathlib import Path
from typing import Any

from gate import Refusal
from gate.licence import repair_junction
from gate.mizan import BAD, HADD, QABIL_WAQF, WAQF, run

ROOT = Path(__file__).resolve().parents[1]
SUKUN = "ْ"


def _load(name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


G = _load("gen_fractal")
C = G.C


def corpus_lines() -> list[list[tuple[str, ...]] | None]:
    """كلُّ آيةٍ كلماتٍ بذرّاتها في سياقها، أو `None` إن رُفض موقعٌ فيها."""
    lines = C.lines_of(G.CORPUS.read_bytes())
    joined = C.gates_for(lines, G.CORPUS)
    start = {"continue": C.gate(), "pause": C.Gate(C.Context(exit="pause"), corpus=G.CORPUS)}
    out: list[list[tuple[str, ...]] | None] = []
    for tokens in lines:
        atoms: list[tuple[str, ...]] | None = []
        for i, w in enumerate(tokens):
            exit_ = C.EXITS[i == len(tokens) - 1]
            g = start[exit_] if i == 0 else joined[(C.repair(tokens[i - 1])[0], exit_)]
            cert = g.enter(w.encode("utf-8"))
            if isinstance(cert, Refusal):
                atoms = None
                break
            assert atoms is not None
            atoms.append(tuple(cert.atoms))
        out.append(atoms)
    return out


LINES = corpus_lines()


def repaired(ws: list[tuple[str, ...]], do_repair: bool = True) -> list[tuple[str, ...]]:
    if not do_repair:
        return ws
    return [repair_junction(w, ws[i + 1])[0] if i + 1 < len(ws) else w for i, w in enumerate(ws)]


def line_rec(s: int, ws: list[tuple[str, ...]], hadd: bool = True) -> int:
    """`Harf.runLine` بتعريفه الاستقرائيّ."""
    if not ws:
        return s
    if len(ws) == 1:
        return run(WAQF, s, ws[0])
    nxt = run(WAQF, s, ws[0])
    return line_rec(HADD[nxt] if hadd else nxt, ws[1:], hadd)


def line_for(ws: list[tuple[str, ...]]) -> int:
    """FOR: الأولى من الابتداء، وكلُّ كلمةٍ بعدها ترث بعد الحدّ."""
    return reduce(lambda s, w: run(WAQF, HADD[s], w), ws[1:], run(WAQF, BAD, ws[0]))


def test_line_equals_pairs() -> None:
    ready = [ws for ws in LINES if ws]
    assert ready
    for ws in ready:
        assert QABIL_WAQF[line_rec(BAD, repaired(ws))], ws


def test_for_is_induction() -> None:
    for ws in LINES:
        if ws:
            r = repaired(ws)
            assert line_for(r) == line_rec(BAD, r)


def test_repair_ends_vowel() -> None:
    n = 0
    for ws in LINES:
        if not ws:
            continue
        for i in range(len(ws) - 1):
            fixed, tag = repair_junction(ws[i], ws[i + 1])
            if tag:
                assert not fixed[-1].endswith(SUKUN), (ws[i], ws[i + 1])
                n += 1
    assert n > 0


def test_mutants_rejected() -> None:
    no_repair = [ws for ws in LINES if ws and not QABIL_WAQF[line_rec(BAD, repaired(ws, False))]]
    assert no_repair
    yaa = ("يَ", "اْ")
    shafi = ("شْ", "شَ", "اْ", "فِ", "عِ", "يْ", "نَ")
    assert not QABIL_WAQF[line_rec(BAD, [yaa, shafi])]
    assert QABIL_WAQF[line_rec(BAD, [yaa, shafi], hadd=False)]
    # MUTANT_TEXT_OR: النصُّ «أو» بين آياته يقبل نصًّا فيه سطرٌ مرفوض، و«و» يرفضه.
    text = [repaired(ws) for ws in LINES if ws] + [[yaa, shafi]]
    verdicts = [QABIL_WAQF[line_rec(BAD, ws)] for ws in text]
    assert any(verdicts) and not all(verdicts)
