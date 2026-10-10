"""شجرةُ المخصّص كما هي، والقابليّاتُ بالرسم، والحكمُ بشاهد — توقّعاتُه من المصدر المختوم (عناوينُه بحروفها)
ومن المادّتين ١٣ و١٦، لا من الشيفرة؛ وطفراتُه مرفوضةٌ بأسمائها."""

from __future__ import annotations

import gzip
import hashlib
import re
import subprocess
import sys

from conftest import ROOT
from slge.mukhassas import (
    BOOKS,
    MAFHUM,
    MALUMAH,
    NODES,
    book_of,
    caps_under,
    code_of_root,
    judge,
    judge_in,
    level_of,
    roots_of,
    title_of,
)

SRC = ROOT / "tests" / "data" / "openiti-mukhassas.txt.gz"
SHA = "8d8134c2bce16b70b07bddf974fa5e9c0f7cd80129d8452baf55cd87006b80ac"


def test_tables_are_generated_from_the_sealed_source() -> None:
    assert hashlib.sha256(gzip.decompress(SRC.read_bytes())).hexdigest() == SHA
    res = subprocess.run([sys.executable, str(ROOT / "tools" / "deposit_mukhassas.py"), "--check"],
                         capture_output=True, text=True, cwd=ROOT)
    assert res.returncode == 0, res.stdout + res.stderr


def test_tree_is_the_source_tree() -> None:
    """العناوينُ من المصدر بحروفها: أوّلُ العقد «المقدمة» ثمّ «كتاب خلق الإنسان»؛ «باب الحمل والولادة»
    ابنُه؛ الأعدادُ 73/337/1,190؛ الأبُ أسبقُ وأدنى مستوًى والكتابُ كتابُ الأب."""

    assert title_of(0) == "المقدمة" and title_of(1) == "كتاب خلق الإنسان"
    assert title_of(2) == "باب الحمل والولادة" and NODES[2][2] == 1 and book_of(2) == 1
    assert title_of(163) == "أبواب المشي" and title_of(979) == "كتاب النخل"
    assert [sum(1 for n in NODES if n[1] == k) for k in (1, 2, 3)] == [73, 337, 1190]
    for i, n in enumerate(NODES):
        assert n[0] == i and n[2] < i
        if n[1] == 1:
            assert n[2] == -1 and n[5] == i
        else:
            assert level_of(n[2]) < n[1] and book_of(n[2]) == n[5]
    assert all(level_of(book_of(i)) == 1 for i in range(len(NODES)))
    # لا علامةَ صفحةٍ في عنوان
    assert not any(re.search(r"\bms\d+\b", title_of(i)) for i in range(len(NODES)))


def test_rasm_linking_is_declared_and_measured() -> None:
    assert sum(1 for n in NODES if n[4]) == 1080 and len({c for n in NODES for c in n[4]}) == 608
    assert roots_of(163) == (22018,) and code_of_root(("م", "ش", "ي")) == 22018
    assert roots_of(979) == (code_of_root(("ن", "خ", "ل")),)
    assert 22018 not in caps_under(1) and 4829 not in caps_under(979)
    for b, rs in BOOKS.items():
        assert level_of(b) == 1
        assert set(rs) == {c for n in NODES if n[5] == b for c in n[4]}


def test_judgement_is_two_graded_with_witness() -> None:
    assert judge_in(163, 22018) == (MAFHUM, 163)
    assert judge_in(1, 22018) == (MALUMAH, None) and judge_in(979, 4829) == (MALUMAH, None)
    g, w = judge(980, 4829)
    assert (g, w) == (MALUMAH, None)
    for b in list(BOOKS)[:10]:
        for r in caps_under(b)[:5]:
            g, w = judge_in(b, r)
            assert g == MAFHUM and w is not None and book_of(w) == b and r in roots_of(w)


def test_mutations_are_refused() -> None:
    # (١) «مفهوم» بلا شاهد مرفوض: كلُّ مفهومٍ شاهدُه عقدةٌ تحمل الجذر
    for b in BOOKS:
        for r in caps_under(b):
            g, w = judge_in(b, r)
            assert g == MAFHUM and w is not None and r in roots_of(w)
    # (٢) الغيابُ ليس امتناعًا: لا قيمةَ ثالثة
    assert {judge_in(979, 4829)[0], judge_in(163, 22018)[0]} == {MALUMAH, MAFHUM}
    # (٣) جذرٌ ليس في المقاييس لا رمزَ له
    assert code_of_root(("ف", "ف", "ف")) is None
    # (٤) بايتٌ واحد يُسقط ختمَ المصدر
    raw = bytearray(gzip.decompress(SRC.read_bytes()))
    raw[len(raw) // 3] ^= 1
    assert hashlib.sha256(bytes(raw)).hexdigest() != SHA


def test_numbers_on_the_deposit() -> None:
    text = (ROOT / "MUKHASSAS_INDEX.md").read_text(encoding="utf-8")
    # كانت 324/1,115 و2,794/6,329 قبل زوائد سيبويه (ADR ١٨)
    # كانت 1,128 و6,519 و2,876 قبل تصحيح همزة الأسماء الموصولة كسرًا (الغانم ADR ٧)
    assert "**328 من 1,127 جذرًا** (29.1%)" in text and "2,875 من 6,516 صورة (44.1%)" in text
    assert "رُبط عنوانُ 1,080 عقدةً من 1,600" in text
