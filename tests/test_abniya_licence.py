"""أبنيةُ سيبويه على الترخيص الثلاثيّ (ADR ٣٦): توقّعاتٌ مستقلّةٌ عن الشيفرة — الأبنيةُ التي
أوّلُها ألفٌ هي أبنيةُ همزة الوصل (افتعل، استفعل، انفعل…) ولا يُرخَّص لها تشكيلٌ بألفٍ ساكنةٍ
أوّلًا، ويُرخَّص بالقاعدة (اِفْتَعَلَ، اِسْتَفْعَلَ)؛ والألفُ لا تكون إلّا ساكنة؛ والشواهدُ تطابق
تصدير Lean؛ وطفراتٌ مرفوضة."""

from __future__ import annotations

from pathlib import Path

from slge.abniya_licence import counts, is_wasl, vocalizations
from slge.abniya_licence_table import WITNESSES
from slge.abniya_table import SKELETONS
from slge.cells import ALPHABET, STATES, SUKUN
from slge.madd import continue_licensed, pause_licensed

ROOT = Path(__file__).resolve().parents[1]


def _sk(name: str) -> tuple[int, ...]:
    return next(s for s in SKELETONS if "".join(ALPHABET[i] for i in s) == name)


def test_wasl_skeletons_need_the_boundary_rule() -> None:
    wasl = [s for s in SKELETONS if is_wasl(s)]
    names = {"".join(ALPHABET[i] for i in s) for s in wasl}
    assert len(wasl) == 13 and {"افتعل", "استفعل", "افعوعل"} <= names
    for s in wasl:  # فحصٌ شاملٌ لكلّ تشكيلاته: الألفُ الأولى ساكنةً كما رُسمت لا تُرخَّص أبدًا
        assert counts(s, wasl_rule=False)[1:] == (0, 0), s
        assert counts(s)[1] > 0 and counts(s)[2] > 0, s
    # اِفْتَعَلَ واِسْتَفْعَلَ مشكولتين بأيدينا (مستقلّتين عن المولِّد)
    iftaala = (("ء", "كسر"), ("ف", SUKUN), ("ت", "فتح"), ("ع", "فتح"), ("ل", "فتح"))
    istafala = (("ء", "كسر"), ("س", SUKUN), ("ت", "فتح"), ("ف", SUKUN), ("ع", "فتح"), ("ل", "فتح"))
    for w in (iftaala, istafala):
        assert continue_licensed(w) and pause_licensed(w)
        assert not continue_licensed((("ا", SUKUN), *w[1:]))


def test_every_skeleton_has_a_licensed_vocalization_and_alif_is_never_voweled() -> None:
    assert len(SKELETONS) == 158 and len(WITNESSES) == 158
    assert all(counts(s)[1] > 0 and counts(s)[2] > 0 for s in SKELETONS)
    for sk, w in WITNESSES:
        cells = tuple((ALPHABET[k], STATES[s]) for k, s in w)
        assert continue_licensed(cells) and pause_licensed(cells)
        assert all(st == SUKUN for k, st in cells if k == "ا")
        assert [ALPHABET.index(k) for k, _ in cells] == [0 if i == 0 and sk[0] == 1 else x
                                                        for i, x in enumerate(sk)]
    # فَاعِل: الألفُ مدٌّ بعد فتح — لا تشكيلَ بألفٍ متحرّكة في الفضاء أصلًا
    faail = _sk("فاعل")
    assert all(w[1][1] == SUKUN for w in vocalizations(faail))


def test_mutations_change_the_numbers() -> None:
    """الطفرة: لو تُركت الألفُ متحرّكةً لاتّسع الفضاءُ ولعدّ الترخيصُ الثلاثيُّ ما لا يُرخَّص من
    الشبكة (الألفُ المتحرّكة متحرّكٌ عنده) — فقيدُ الألف يغيّر الأرقام ولا يمرّ صامتًا. وحركةُ همزة
    الوصل لا تغيّر الترخيص (كلُّ حركةٍ متحرّك)، فلا تُعدّ طفرةً فاصلة هنا."""

    from itertools import product

    faail = _sk("فاعل")
    tot, cont, _ = counts(faail)
    assert tot == 4 ** 3  # ف ع ل حرّةٌ بأربع حالات، والألفُ ساكنةٌ أبدًا
    letters = [ALPHABET[i] for i in faail]
    free = [tuple(zip(letters, st, strict=True)) for st in product(STATES, repeat=len(letters))]
    cont_free = sum(1 for w in free if continue_licensed(w))
    assert len(free) == 4 ** 4 and cont_free > cont
    istafala = _sk("استفعل")
    damma_always = sum(1 for w in vocalizations(istafala)
                       if continue_licensed((("ء", "ضم"), *w[1:])))
    assert damma_always == counts(istafala)[1]


def test_python_matches_the_lean_export() -> None:
    rows = (ROOT / "formal" / "out" / "abniya_licence.csv").read_text(encoding="utf-8").splitlines()
    exported = [r.split(",") for r in rows if r.startswith("witness,")]
    assert len(exported) == len(WITNESSES) == 158
    for (_, sk, n, cont, pause, written), (want_sk, w) in zip(exported, WITNESSES, strict=True):
        assert tuple(int(x) for x in sk.split("-")) == want_sk and int(n) == len(w)
        assert cont == pause == "true"
        cells = tuple((ALPHABET[k], STATES[s]) for k, s in w)
        assert (written == "true") == continue_licensed((("ا", SUKUN), *cells[1:]))


def test_witness_rule_is_pinned_and_hamza_vowel_is_not_a_licence_fact() -> None:
    """الشاهدُ اختيارٌ مسمًّى لا تشكيلُ سيبويه (ADR ٣٧): أوّلُ مرخَّصٍ بترتيب `STATES` المثبَّت هنا؛
    فَعَلَ، فَاعَلَ، ءِفَتَعَلَ مكتوبةً باليد. وطفرةُ الترتيب (السكونُ أوّلًا) تغيّر الشاهد — فالترتيبُ
    جزءٌ من التعريف لا تفصيل. وحركةُ همزة الوصل لا تغيّر الترخيص (`wasl_vowel_irrelevant`)."""

    from itertools import product

    assert STATES == ("فتح", "كسر", "ضم", "سكون")
    a, i = "فتح", "كسر"
    hand = {"فعل": (("ف", a), ("ع", a), ("ل", a)),
            "فاعل": (("ف", a), ("ا", SUKUN), ("ع", a), ("ل", a)),
            "افتعل": (("ء", i), ("ف", a), ("ت", a), ("ع", a), ("ل", a))}
    got = {"".join(ALPHABET[k] for k in sk): tuple((ALPHABET[k], STATES[s]) for k, s in w)
           for sk, w in WITNESSES}
    for name, w in hand.items():
        assert got[name] == w, name
    fal = _sk("فعل")
    reordered = (SUKUN, "فتح", "كسر", "ضم")
    first = next(fw for st in product(reordered, repeat=3)
                 if continue_licensed(fw := tuple(zip(("ف", "ع", "ل"), st, strict=True)))
                 and pause_licensed(fw))
    assert first != got["فعل"] and len(fal) == 3
    for sk, wit in WITNESSES:
        if is_wasl(sk):
            cells = tuple((ALPHABET[k], STATES[s]) for k, s in wit)
            for v in ("فتح", "كسر", "ضم"):
                moved = (("ء", v), *cells[1:])
                assert continue_licensed(moved) == continue_licensed(cells)
                assert pause_licensed(moved) == pause_licensed(cells)


def _tool() -> object:
    import importlib.util
    import sys

    spec = importlib.util.spec_from_file_location(
        "gen_abniya_licence_index", ROOT / "tools" / "gen_abniya_licence_index.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen_abniya_licence_index"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_owner_reference_frame(tmp_path: Path) -> None:
    """الإطارُ المحجوب (ADR ٣٧): صفٌّ لكلّ هيكلٍ بترتيبه، أعمدةُ المالك فارغة فلا رقم؛ وصفٌّ مملوءٌ
    بحالاتٍ (لا نصّ) يُقرأ خاناتٍ، والمخالفُ لشكله يُرفض باسمه (طفرة)."""

    import csv

    tool = _tool()
    rows = tool.reference_rows()  # type: ignore[attr-defined]
    assert [r["skeleton"] for r in rows] == ["".join(ALPHABET[i] for i in s) for s in SKELETONS]
    assert all(not r["states"] and not r["source"] for r in rows)
    assert tool.check_reference() == []  # type: ignore[attr-defined]
    row = next(r for r in rows if r["skeleton"] == "افتعل")
    filled = {**row, "states": "كسر سكون فتح فتح فتح"}
    cells = tool.owner_cells(filled)  # type: ignore[attr-defined]
    assert cells == (("ء", "كسر"), ("ف", SUKUN), ("ت", "فتح"), ("ع", "فتح"), ("ل", "فتح"))
    assert continue_licensed(cells) and pause_licensed(cells)
    assert tool.owner_cells({**row, "states": "كسر سكون فتح"}) is None  # type: ignore[attr-defined]
    bad = [dict(r) for r in rows]
    bad[0]["states"] = "نصب"
    ref = tmp_path / "abniya-reference.tsv"
    with ref.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(bad)
    tool.REFERENCE = ref  # type: ignore[attr-defined]
    assert tool.check_reference() == ["REFERENCE_ROW_MALFORMED A001"]  # type: ignore[attr-defined]
