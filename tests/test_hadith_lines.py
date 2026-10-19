"""المدوّنةُ المختومة الثانية — الصحيحان سطورًا (ADR ٧): الختمُ ببصمة المصدر، التحويلُ بلا تطبيع يُردّ
بعينه، رموزُ الطبعة مسمّاة، وقاعدتا الرسم الجديدتان (`AMR_WAW`، `IBN_ALIF`) تردّان الرسمَ وتُحكمان بالحدّ؛
وطفراتٌ مرفوضة. التوقّعاتُ من قواعد الإملاء المشهورة (ألفُ ابن بين علمين؛ واوُ عمرو) ومن الكتاب
(س17573: الأسماءُ الموصولة مكسورةُ الهمزة) لا من الشيفرة."""

from __future__ import annotations

import gzip
import hashlib
import importlib.util
import sys
from pathlib import Path

import pytest

from gate import Refusal
from gate.api import (
    HADITH_CORPUS,
    HADITH_LINES_SHA256,
    SEALED_CORPORA,
    Gate,
    is_marker,
    sealed_forms,
)
from gate.contextual import Context, project
from gate.residue import repair, unrepair

ROOT = Path(__file__).resolve().parents[1]


def _tool():
    spec = importlib.util.spec_from_file_location("gen_hadith_lines",
                                                  ROOT / "tools" / "gen_hadith_lines.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen_hadith_lines"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_sealed_sources_and_lines_match_their_digests() -> None:
    m = _tool()
    for name, sha in m.HADITH_SOURCES.items():
        with gzip.open(ROOT / "corpora" / "hadith" / (name + ".gz"), "rb") as f:
            assert hashlib.sha256(f.read()).hexdigest() == sha, name
    with gzip.open(HADITH_CORPUS, "rb") as f:
        raw = f.read()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == HADITH_LINES_SHA256 == SEALED_CORPORA[HADITH_CORPUS.name]
    lines = raw.decode("utf-8").splitlines()
    assert len(lines) == 12370  # 7,008 بخاريّ + 5,362 مسلم (صفوفُ الملفّين)
    assert (ROOT / "corpora" / "hadith" / "LICENSE.ODbL").exists()


def test_tokenisation_is_lossless_and_names_every_edition_glyph() -> None:
    m = _tool()
    rlm = "‏"
    col = f"{rlm} {rlm}حَدَّثَنَا {rlm} و قَالَ  ح {{ قُلْ }} ص"
    toks = m.tokens_of(col)
    assert toks == ["<rlm>", "<rlm+>", "حَدَّثَنَا", "<rlm>", "<ltr:و>", "قَالَ", "<sp>", "<ltr:ح>",
                    "<q>", "قُلْ", "</q>", "<ltr:ص>"]
    assert m.restore_column(toks) == col
    assert all(is_marker(t) for t in toks if t.startswith("<")) and not is_marker("قَالَ")
    # الطفرة: رمزُ طبعةٍ غيرُ مسمًّى لا يمرّ صامتًا
    with pytest.raises(ValueError, match="UNNAMED_EDITION_GLYPH"):
        m.tokens_of("قَا{لَ")
    # الصحيحان كلُّهما يُردّان صفًّا صفًّا (الأداةُ تفحصه عند التوليد؛ هنا عيّنةٌ من كلّ كتاب)
    for _, cols in m.sources():
        for col in cols[:200]:
            assert m.restore_column(m.tokens_of(col)) == col


def test_edition_rules_restore_the_rasm_and_the_gate_judges_in_context() -> None:
    # واوُ عمرو الفارقة: تُحذف من الصورة وتُردّ في الرسم؛ والصورةُ مرخَّصة
    for w, atoms in (("عَمْرٍو", ("عَ", "مْ", "رِ", "نْ")), ("وَعَمْرٌو", ("وَ", "عَ", "مْ", "رُ", "نْ"))):
        c, r = repair(w)
        assert r[0][0] == "AMR_WAW" and unrepair(c, r) == w
        d = project(c, Context())
        assert d["status"] == "READY" and tuple(d["atoms"]) == atoms, w
    # ألفُ ابن بين علمين: تُعاد فتُكسَر (اسمٌ موصول) وتسقط وصلًا؛ ابتداءً اِبْنُ، ووصلًا بْنُ بعينها
    for w, last in (("بْنُ", "نُ"), ("بْنِ", "نِ"), ("بْنَ", "نَ")):
        c, r = repair(w)
        assert [x[0] for x in r] == ["IBN_ALIF", "WASL"] and unrepair(c, r) == w
        start = project(c, Context())
        assert start["status"] == "READY" and tuple(start["atoms"]) == ("ءِ", "بْ", last), w
        joined = project(c, Context(entry="joined", exit="continue", left="عَبْدُ"))
        assert joined["status"] == "READY" and tuple(joined["atoms"]) == ("بْ", last), w
    # الأسماءُ الموصولة مكسورةٌ ولو ضُمّ ثالثُها (الكتاب س17573)؛ والفعلُ المضمومُ الثالث مضموم
    assert project(repair("اسْمُ")[0], Context())["atoms"][0] == "ءِ"
    assert project(repair("اسْتُخْرِجَ")[0], Context())["atoms"][0] == "ءُ"
    # الطفرات: ما ليس «بن» لا يأخذ الألف؛ واوٌ بعد غير منوَّن ليست عمرو
    assert all(x[0] != "IBN_ALIF" for x in repair("بَنُو")[1])
    assert all(x[0] != "AMR_WAW" for x in repair("عَمْرَو")[1])


def test_the_hadith_gate_is_the_same_law_on_a_second_sealed_corpus() -> None:
    forms = sealed_forms(HADITH_CORPUS)
    assert len(forms) > 50_000
    g = Gate(corpus=HADITH_CORPUS)
    ready = sum(1 for w in list(forms)[:300] if not isinstance(g.enter(w.encode()), Refusal))
    assert ready >= 290  # 99.8% ابتداءً على المميّزات (COVERAGE بعدُ في SLGE)
    # ما ليس من مجال الصحيحين يُرفض باسمه، ولا يُعلَن مجالٌ من خارج المدوّنة المختومة
    r = g.enter("فَسَيَكْفِيكَهُمُ".encode())
    assert isinstance(r, Refusal) and r.status == "OUTSIDE_DECLARED_DOMAIN"
    with pytest.raises(ValueError, match="DOMAIN_OUTSIDE_SEALED_CORPUS"):
        Gate(corpus=HADITH_CORPUS, domain={repair("فَسَيَكْفِيكَهُمُ")[0]})
