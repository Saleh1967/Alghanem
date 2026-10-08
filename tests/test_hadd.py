"""قيدُ الحدّ (`A116.Hadd`): قافيةُ المدّ CVVC لا تُرخَّص وصلًا إلّا والمُغلِقُ أوّلُ مثلين، أو مدَّ فرق.

١. المطابقة: `gate.licence.kind_of` و`continue_licensed` و`strict_licensed` = `Hadd.kindOf` و
   `Ternary.continueB` و`Hadd.strictB` على كلّ سطرٍ من `lake exe a116-table hadd` (346,200 سطرًا).
٢. الطفرات: ثلاثُ مرايا خاطئةٍ مسمّاة يُسقطها الجدولُ نفسُه — فالمطابقةُ تفرّق لا تُصادق على كلّ شيء.
٣. الشواهد: توقّعاتٌ مكتوبةٌ باليد من الاصطلاح (حَاجَّ، ضَالِّينَ، قُلْتُ، آلْآنَ مقبولة؛ قَالْتُ مرفوضة)،
   لا محسوبةٌ بالشيفرة المفحوصة.
٤. المدوّنةُ المختومة: الرقمُ قبلُ وبعدُ واحد (لا جاهزَ سقط)، والوصلُ بعد مدٍّ يُرفض باسمه.
٥. الحدُّ بين كلمتين (`Hadd.strictJoinB`): مطابقةُ `hadd-join` (293,904 سطرًا) وطفرتان مسمّاتان، والعيبُ
   المسدود «يَا + الشَّافِعِينَ» مرفوضٌ في البوّابة باسمه.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from pathlib import Path

import pytest

from gate import Refusal, enter, gate
from gate.contextual import Context
from gate.licence import (
    K,
    continue_licensed,
    hadd_ok,
    kind_of,
    strict_joined,
    strict_licensed,
)

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "formal" / "a116" / "hadd.csv"
JOIN_TABLE = ROOT / "formal" / "a116" / "hadd-join.csv"


def w(s: str) -> tuple[str, ...]:
    return tuple(s.split())


def _rows() -> list[tuple[tuple[str, ...], list[str], bool, bool]]:
    out = []
    with TABLE.open(encoding="utf-8") as fh:
        for line in fh:
            atoms, kinds, cont, strict = line.rstrip("\n").split(",")
            out.append((tuple(atoms.split(" ")), kinds.lower().split("-"), cont == "true",
                        strict == "true"))
    return out


def test_python_mirror_matches_lean_hadd_table() -> None:
    rows = _rows()
    assert len(rows) == 346200
    for atoms, kinds, cont, strict in rows:
        k = kind_of(atoms)
        assert k == kinds, atoms
        assert continue_licensed(k) == cont, atoms
        assert strict_licensed(atoms) == strict, atoms


def _mut_no_gemination(atoms: Sequence[str]) -> bool:
    """الطفرة ١ (`MUTANT_TERNARY_ONLY`): الثلاثيُّ وحدَه — هو الدَّينُ المسدود."""

    return continue_licensed(kind_of(atoms))


def _mut_no_farq(atoms: Sequence[str]) -> bool:
    """الطفرة ٢ (`MUTANT_NO_FARQ`): التضعيفُ بلا استثناء مدّ الفرق."""

    k: list[K] = kind_of(atoms)
    for i in range(len(k) - 1):
        if k[i] == "v" and k[i + 1] == "c":
            if i + 2 >= len(atoms) or atoms[i + 1][0] != atoms[i + 2][0]:
                return False
    return continue_licensed(k)


def _mut_farq_any_madd_lam(atoms: Sequence[str]) -> bool:
    """الطفرة ٣ (`MUTANT_FARQ_WITHOUT_HAMZA`): يُستثنى كلُّ مدٍّ قبل لامٍ في الأوّل، بهمزةٍ أو بغيرها."""

    if len(atoms) >= 3 and atoms[1] == "اْ" and atoms[2][0] == "ل":
        return continue_licensed(kind_of(atoms)) and hadd_ok(("ءَ",) + tuple(atoms[1:]))
    return strict_licensed(atoms)


@pytest.mark.parametrize(
    "mutant", [_mut_no_gemination, _mut_no_farq, _mut_farq_any_madd_lam],
    ids=["MUTANT_TERNARY_ONLY", "MUTANT_NO_FARQ", "MUTANT_FARQ_WITHOUT_HAMZA"],
)
def test_lean_table_rejects_named_mutants(mutant: Callable[[Sequence[str]], bool]) -> None:
    wrong = sum(1 for atoms, _, _, strict in _rows() if mutant(atoms) != strict)
    assert wrong > 0


def test_named_witnesses_with_independent_expectations() -> None:
    """التوقّعاتُ من الاصطلاح لا من الشيفرة؛ وكلُّها شواهدُ مبرهنةٌ بأسمائها في `Hadd.lean`."""

    accepted = {
        "حَاجَّ": w("حَ اْ جْ جَ"),  # hajja_strict
        "ضَالِّينَ": w("ضَ اْ لْ لِ يْ نَ"),  # dallina_strict
        "قُلْتُ": w("قُ لْ تُ"),  # qultu_strict
        "آلْآنَ": w("ءَ اْ لْ ءَ اْ نَ"),  # alaana_strict (مدُّ الفرق)
    }
    refused = {
        "قَالْتُ": w("قَ اْ لْ تُ"),  # hadd_debt_closed
        "بَالْآنَ": w("بَ اْ لْ ءَ اْ نَ"),  # farq_needs_its_hamza
    }
    for name, atoms in accepted.items():
        assert strict_licensed(atoms), name
    for name, atoms in refused.items():
        assert continue_licensed(kind_of(atoms)), name  # الثلاثيُّ وحدَه كان يقبلها
        assert not strict_licensed(atoms), name


def test_sealed_corpus_before_equals_after() -> None:
    """الرقمُ قبلُ وبعدُ على المودَع نفسه: كلُّ جاهزٍ مرخَّصٌ بالقيد، ولا جاهزَ سقط (17,551 كما كان)."""

    g = gate()
    ready = 0
    for surface in g.book.domain:
        cert = g.enter(surface.encode("utf-8"))
        if isinstance(cert, Refusal):
            assert "CVVC_NOT_GEMINATE" not in cert.reasons, surface
            continue
        ready += 1
        assert strict_licensed(cert.atoms), surface
    assert ready == 17551


def test_junction_after_madd_is_refused_by_name() -> None:
    """يَا + الْأَرْضِ: الألفُ ثمّ لامٌ ساكنةٌ غيرُ مدغمة عند الحدّ؛ كان الثلاثيُّ يقبلها، والقيدُ يرفضها
    باسمها ولا يُقصّر المدَّ تخمينًا. وبعد متحرّكٍ (قُلِ) يبقى الوصلُ مقبولًا."""

    after_madd = enter("الْأَرْضِ".encode(), Context(entry="joined", left="يَا"))
    assert isinstance(after_madd, Refusal)
    assert after_madd.reasons == ("JUNCTION_NOT_LICENSED", "CVVC_NOT_GEMINATE")
    after_vowel = enter("الْأَرْضِ".encode(), Context(entry="joined", left="قُلِ"))
    assert not isinstance(after_vowel, Refusal)


def _join_rows() -> list[tuple[tuple[str, ...], tuple[str, ...], bool, bool]]:
    out = []
    with JOIN_TABLE.open(encoding="utf-8") as fh:
        for line in fh:
            pair, strict, joined = line.rstrip("\n").split(",")
            left, right = pair.split("|")
            out.append((tuple(left.split(" ")), tuple(right.split(" ")), strict == "true",
                        joined == "true"))
    return out


def test_python_mirror_matches_lean_hadd_join_table() -> None:
    rows = _join_rows()
    assert len(rows) == 293904
    for left, right, strict, joined in rows:
        assert strict_licensed(left + right) == strict, (left, right)
        assert strict_joined(left, right) == joined, (left, right)


def _mut_no_boundary(left: Sequence[str], right: Sequence[str]) -> bool:
    """الطفرة ٤ (`MUTANT_NO_BOUNDARY`): القيدُ على الموصول بلا حدّ — هو العيبُ المسدود."""

    return strict_licensed(tuple(left) + tuple(right))


def _mut_boundary_after_madd_only(left: Sequence[str], right: Sequence[str]) -> bool:
    """الطفرة ٥ (`MUTANT_BOUNDARY_AFTER_MADD_ONLY`): يُفحص `v | c` ويُنسى `v c | x`."""

    k = kind_of(tuple(left) + tuple(right))
    b = len(left)
    cut = b < len(k) and k[b - 1] == "v" and k[b] == "c"
    return strict_licensed(tuple(left) + tuple(right)) and not cut


@pytest.mark.parametrize(
    "mutant", [_mut_no_boundary, _mut_boundary_after_madd_only],
    ids=["MUTANT_NO_BOUNDARY", "MUTANT_BOUNDARY_AFTER_MADD_ONLY"],
)
def test_lean_join_table_rejects_named_mutants(
    mutant: Callable[[Sequence[str], Sequence[str]], bool],
) -> None:
    wrong = sum(1 for left, right, _, joined in _join_rows() if mutant(left, right) != joined)
    assert wrong > 0


def test_madd_then_geminate_across_words_is_refused_by_name() -> None:
    """`ya_shafiina_straddles`: يَا + الشَّافِعِينَ — المدُّ في الأولى والمدغمُ (لامُ الشمسيّة) في الثانية؛
    الاستثناءُ داخلَ الكلمة الواحدة وحدَها، فيُرفض باسمه. والمدُّ والمدغمُ معًا في الثانية مقبولان."""

    shafiina = "\u0627\u0644\u0634\u0651\u064e\u0627\u0641\u0650\u0639\u0650\u064a\u0646\u064e"
    # الرسمُ بنقاطه في المدوّنة المختومة (الشدّةُ قبل الفتحة)، لا كما تُدخله لوحةُ مفاتيح
    across = enter(shafiina.encode(), Context(entry="joined", left="يَا"))
    assert isinstance(across, Refusal)
    assert across.reasons == ("JUNCTION_NOT_LICENSED", "CVVC_ACROSS_WORD_BOUNDARY")
    assert strict_joined(w("قُ لِ"), w("ضَ اْ لْ لِ يْ نَ"))  # quli_dallina_join
    assert not strict_joined(w("يَ اْ"), w("شْ شَ اْ فِ عِ يْ نَ"))  # ya_shafiina_straddles
    assert strict_licensed(w("يَ اْ شْ شَ اْ فِ عِ يْ نَ"))  # …وكان القيدُ بلا حدٍّ يقبلها
