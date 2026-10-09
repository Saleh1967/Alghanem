"""التغطية: توقّعاتٌ مستقلّةٌ عن الشيفرة — الشبكةُ المرخَّصة 113 لأنّ «الألف لا تكون أبدا إلا ساكنة»
(الكتاب)، والمشهودُ في المصحف هو المرخَّصُ بعينه؛ الشاهدُ قاطعٌ أو محتملٌ أو لا شيء بتعريفه؛ والصفوفُ
الموقَّعةُ من المصحف كلُّها مشهودة، وصفوفُ النحو بلا شاهدٍ معلومةٌ تبقى؛ وطفراتٌ مرفوضة."""

from __future__ import annotations

import gzip
import json
from collections import Counter
from pathlib import Path

from slge.alam import ilm
from slge.alam_table import ALAM
from slge.cells import CELLS, STATES, SUKUN
from slge.coverage import (
    ALIF_VOWELLED,
    MAFHUM,
    MALUMAH,
    MUHTAMAL,
    QATI,
    cell_witnesses,
    licensable_cells,
    node_grade,
    root_witnesses,
    row_grade,
    witness_of,
)
from slge.coverage_table import ATTESTED_CELLS, AXES, NODES, ROOTS
from slge.rawabit import cells_of
from slge.sawabiq import sawabiq
from slge.sawabiq_table import TABLE as SAWABIQ_TABLE
from slge.tawzi import TABLE as TAWZI_TABLE
from slge.tawzi import tawzi

DATA = Path(__file__).parent / "data"
Word = tuple[tuple[str, str], ...]


def _forms(name: str) -> list[Word]:
    with gzip.open(DATA / name, "rt", encoding="utf-8") as f:
        return [tuple((a, b) for a, b in x["cells"]) for x in json.load(f)["forms"]]


def test_the_grid_is_licensable_minus_vowelled_alif() -> None:
    lic = licensable_cells()
    assert len(CELLS) == 116 and len(lic) == 113 and len(set(lic)) == 113
    assert set(CELLS) - set(lic) == {("ا", s) for s in STATES if s != SUKUN} == set(ALIF_VOWELLED)
    assert ("ا", SUKUN) in lic and ("ء", "فتح") in lic


def test_attested_cells_are_exactly_the_licensable() -> None:
    """المصحفُ عربيٌّ والألفُ فيه ساكنةٌ أبدًا: كلُّ مرخَّصٍ مشهودٌ ولا ألفَ متحرّكة — على المودَعين معًا."""

    wit = cell_witnesses([*_forms("corpus-certificates.json.gz"),
                          *_forms("context-certificates.json.gz")])
    assert {x for x in wit if wit[x]} == set(licensable_cells()) == set(ATTESTED_CELLS)
    assert all(wit[x] == 0 for x in ALIF_VOWELLED) and len(ATTESTED_CELLS) == 113


def test_witness_of_root_and_node_are_the_defined_ones() -> None:
    assert witness_of(frozenset({7}), 7) == QATI
    assert witness_of(frozenset({7, 9}), 7) == MUHTAMAL == witness_of(frozenset({7, 9}), 9)
    assert witness_of(frozenset({9}), 7) is None and witness_of(frozenset(), 7) is None
    q, m = root_witnesses([frozenset({7}), frozenset({7, 9}), frozenset({9}), frozenset({7})])
    assert q == {7: 2, 9: 1} and m == {7: 3, 9: 2}  # القاطعُ محتمل
    assert node_grade((3, 9, 7), q) == (MAFHUM, 9)  # أوّلُ جذرٍ في العنوان له قاطع
    assert node_grade((3, 4), q) == (MALUMAH, None) and node_grade((), q) == (MALUMAH, None)
    assert row_grade(0) == (MALUMAH, None) and row_grade(3) == (MAFHUM, 3)


def test_deposited_rows_are_graded_by_their_corpus_witnesses() -> None:
    """الأعلامُ موقَّعةٌ من صور المصحف والسوابقُ مولَّدةٌ منه: كلُّ صفٍّ مشهود؛ والموزِّعُ من جداول النحو:
    ما ليس في المصحف (هُنَاكَ، رُبَّ، إِيَّاكِ) معلومةٌ باقية، وما فيه (ذَلِكَ، إِيَّاكَ، هُنَالِكَ) مفهوم."""

    forms = _forms("corpus-certificates.json.gz")
    alam: Counter[str] = Counter(a.rasm for w in forms for a in ilm(w) if a.kind != "جلالة")
    assert all(row_grade(alam[r])[0] == MAFHUM for r, *_ in ALAM) and len(ALAM) == 57
    assert alam["بكة"] == alam["مكة"] == 1  # الصفّان المصحَّحان بالتاء (2026-10-09)
    corpus = set(forms)
    for kind, _, _, _, form, *_ in SAWABIQ_TABLE:
        assert form in corpus and any(s.kind == kind for s in sawabiq(form))
    hits: Counter[tuple[str, str, Word]] = Counter(
        (m.kind, m.name, m.core) for w in forms for m in tawzi(w))
    grades = {(k, n, c): row_grade(hits[(k, n, c)]) for k, n, c in TAWZI_TABLE}
    by_cells = {c: g for (_, _, c), g in grades.items()}
    for s in ("ذَلِكَ", "إِيَّاكَ", "هُنَالِكَ", "هَذَا", "مَنْ"):
        assert by_cells[cells_of(s)][0] == MAFHUM, s
    for s in ("هُنَاكَ", "رُبَّ", "إِيَّاكِ", "مُنْذُ", "تَانِكَ"):
        assert by_cells[cells_of(s)] == (MALUMAH, None), s
    mafhum = sum(1 for g in grades.values() if g[0] == MAFHUM)
    assert (2, len(TAWZI_TABLE), mafhum) in AXES and len(TAWZI_TABLE) == 246
    assert all(a <= t for _, t, a in AXES) and len(AXES) == 6
    assert ROOTS[1] + ROOTS[2] + ROOTS[3] == ROOTS[0] == 4561
    assert NODES[1] + NODES[2] + NODES[3] + NODES[4] == NODES[0] == 1600


def test_mutations_are_refused() -> None:
    # صفٌّ مزروعٌ ليس في المصحف: معلومةٌ لا مفهوم؛ وجذرٌ ليس من جذور الصورة لا شاهدَ له ولو كثرت
    planted: Counter[tuple[str, str, Word]] = Counter()
    assert row_grade(planted[("حرف", "زُور", cells_of("زُورْ"))]) == (MALUMAH, None)
    assert witness_of(frozenset({1, 2, 3}), 4) is None
    # من عدّ المحتملَ قاطعًا خالف التعريف: صورةٌ بجذرين لا قاطعَ فيها
    q, _ = root_witnesses([frozenset({1, 2})])
    assert not q
    # من عدّ الألفَ الساكنة أيضًا ممنوعةً خالف الـ113
    mutant = tuple(x for x in CELLS if x[0] != "ا")
    assert len(mutant) == 112 and set(licensable_cells()) - set(mutant) == {("ا", SUKUN)}
