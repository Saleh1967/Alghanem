"""الحكم (ADR ٣٤): توقّعاتٌ مستقلّةٌ عن الشيفرة — مودَعُ المعلومات السابقة الأوّل (الأجناسُ والقابليّاتُ من
المخصّص) ببصمته في السجلّ، كلُّ قابليّةٍ فيه بعقدةٍ من الشجرة تشهد لها؛ ودالّةُ الحكم: لا حكمَ إلّا بلا جذر،
ولا إسقاطَ ولا زيادة، ولا «مفهوم» بلا شاهد، والشهادةُ لا تُمسّ، و«مشي» جنسٌ تحت «أبواب المشي» و«ولد»
قابليّةٌ لكتاب خلق الإنسان؛ ومطابقةُ تصدير Lean؛ وطفراتٌ مرفوضة باسمها."""

from __future__ import annotations

import gzip
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import pytest

from slge.ajnas_table import GENERA, KIND
from slge.hukm import (
    JINS,
    QABILIYYA,
    Judgement,
    hukm,
    hukm_of_form,
    judge_jins,
    judge_qabiliyya,
    judge_root,
    rank,
    roots_of_form,
)
from slge.manifest import AJNAS_DIGEST, DEPOSITS
from slge.mukhassas import NODES, level_of, title_of
from slge.rawabit import cells_of
from slge.salsala import DECLARED, ROWS, grade
from slge.shahada import Shahada, fingerprint

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "tests" / "data"


def _tool() -> Any:
    spec = importlib.util.spec_from_file_location("deposit_ajnas",
                                                  ROOT / "tools" / "deposit_ajnas.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["deposit_ajnas"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_first_prior_knowledge_deposit_is_registered_by_kind_and_digest() -> None:
    dep = next(d for d in DEPOSITS if d.path == "ajnas-qabiliyyat.json.gz")
    assert dep.kind == KIND == "معلومات سابقة"
    raw = (DATA / dep.path).read_bytes()
    blob = gzip.decompress(raw)
    assert hashlib.sha256(blob).hexdigest() == AJNAS_DIGEST and not dep.sha256  # مشتقٌّ لا مختوم
    doc = json.loads(blob.decode("utf-8"))
    assert doc["kind"] == KIND and doc["source"] == "openiti-mukhassas.txt.gz"
    assert len(doc["genera"]) == len(GENERA) == 73
    assert [g["book"] for g in doc["genera"]] == [g[0] for g in GENERA]
    # الأجناسُ كتبُ الشجرة (المستوى الأوّل) بترتيبها، وكلُّ قابليّةٍ بعقدةٍ تحت كتابها من مستوًى ثانٍ فأعلى
    assert [g[0] for g in GENERA] == [n[0] for n in NODES if n[1] == 1]
    for book, title, roots, caps in GENERA:
        assert title_of(book) == title and tuple(NODES[book][4]) == roots
        for r, w in caps:
            assert NODES[w][5] == book and level_of(w) >= 2 and r in NODES[w][4]
        assert len({r for r, _ in caps}) == len(caps)
    assert sum(len(g[3]) for g in GENERA) == 863


def test_judgement_is_total_witnessed_and_never_drops_a_root() -> None:
    # «مشي» (22018) اسمُ الكتاب 163 «أبواب المشي»؛ «ولد» (24998) في «باب الحمل والولادة» (2) تحت كتاب
    # خلق الإنسان
    assert title_of(163).endswith("المشي") and judge_jins(22018) == Judgement(JINS, 163)
    assert title_of(2) == "باب الحمل والولادة" and judge_qabiliyya(24998) == Judgement(QABILIYYA, 2)
    assert judge_jins(24998).witness is None  # «ولد» ليس اسمَ كتاب: معلومةٌ لا رفض
    assert hukm([]) is None  # لا حكمَ بلا جذر
    rows = hukm([22018, 24998, 5]) or []
    assert [x[0] for x in rows] == [22018, 24998, 5]  # لا إسقاطَ ولا زيادة وبالترتيب
    assert all(x[1].rukn == JINS and x[2].rukn == QABILIYYA for x in rows)
    # المرتبةُ من جدول السلسلة: الركنان في عمود النبهانيّ بمرتبة الظنّ، والقابليّاتُ كانت معلَنةً بلا مرساة
    assert ROWS[JINS][1] == 0 and ROWS[QABILIYYA][1] == 0 and QABILIYYA in DECLARED
    assert rows[0][1].grade == grade(JINS) == "ظنّ" and rows[1][2].grade == "ظنّ"
    assert rows[0][1].name == "الأجناس والأنواع" and rows[1][2].name == "القابليّات"
    assert rows[0][1].kind == "مفهوم" and rows[2][1].kind == "معلومة"
    # الترتيبُ مفهومًا أوّلًا ولا يحذف
    ranked = rank([judge_root(5), judge_root(22018)])
    assert [x[0] for x in ranked] == [22018, 5] and sorted(ranked) == sorted([judge_root(5),
                                                                              judge_root(22018)])
    # لا «مفهوم» بلا شاهدٍ من المودَع: كلُّ شاهدِ جنسٍ كتابٌ جذورُه تحمل الجذر، وكلُّ شاهدِ قابليّةٍ في جدولها
    for r in (22018, 24998, 7011, 6143):
        j, q = judge_jins(r), judge_qabiliyya(r)
        if j.witness is not None:
            assert r in next(g[2] for g in GENERA if g[0] == j.witness)
        if q.witness is not None:
            assert any((r, q.witness) in g[3] for g in GENERA)


def test_judgement_of_a_form_leaves_the_shahada_untouched() -> None:
    w = cells_of("مَشَى")
    s = Shahada(w, (0, 0, 1, 1, 1, 1, 1), None)
    h = hukm_of_form(w)
    assert h is not None and h[0][0] == 22018 and h[0][1] == Judgement(JINS, 163)
    assert fingerprint(s) == fingerprint(Shahada(w, (0, 0, 1, 1, 1, 1, 1), None))
    assert 22018 in roots_of_form(w)
    assert all(x[1].rukn == JINS and x[2].rukn == QABILIYYA for x in h)


def test_mutations_of_the_deposit_are_refused_by_name() -> None:
    m = _tool()
    gs = m.genera()
    m.verify(gs)
    b, t, rs, caps = gs[1]
    with pytest.raises(SystemExit, match="CAP_WITHOUT_WITNESS"):
        # شاهدٌ هو الكتابُ نفسُه لا عقدةٌ تحته
        m.verify([gs[0], (b, t, rs, ((caps[0][0], 1),)), *gs[2:]])
    with pytest.raises(SystemExit, match="CAP_REPEATED"):
        m.verify([gs[0], (b, t, rs, (caps[0], caps[0])), *gs[2:]])
    with pytest.raises(SystemExit, match="GENERA_ARE_NOT_THE_BOOKS"):
        m.verify(gs[1:])
    m.verify(gs)


def test_python_judgement_matches_the_lean_export() -> None:
    """`lake exe slge-table hukm` يطبع لكلّ جذرٍ في المودَع شاهدَ الجنس وشاهدَ القابليّة من `Slge.Hukm`؛
    والمرآةُ البايثونيّة تطابقه جذرًا جذرًا، و`ajnas_table` يطابق الأجناسَ عددًا."""

    rows = (ROOT / "formal" / "out" / "hukm.csv").read_text(encoding="utf-8").splitlines()
    judged = [r.split(",") for r in rows if r.startswith("judge,")]
    assert len(judged) == 608
    for _, r, j, q in judged:
        jj, qq = judge_jins(int(r)), judge_qabiliyya(int(r))
        want = (None if j == "-" else int(j), None if q == "-" else int(q))
        assert (jj.witness, qq.witness) == want
    assert "nohukm,true" in rows
    genera = [r.split(",") for r in (ROOT / "formal" / "out" / "ajnas_table.csv")
              .read_text(encoding="utf-8").splitlines() if r.startswith("genus,")]
    assert [(int(b), int(nr), int(nc)) for _, b, nr, nc in genera] == [
        (g[0], len(g[2]), len(g[3])) for g in GENERA]
