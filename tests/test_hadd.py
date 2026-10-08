"""قيدُ الحدّ (`A116.Hadd`): قافيةُ المدّ CVVC لا تُرخَّص وصلًا إلّا والمُغلِقُ أوّلُ مثلين، أو مدَّ فرق.

١. المطابقة: `gate.licence.kind_of` و`continue_licensed` و`strict_licensed` = `Hadd.kindOf` و
   `Ternary.continueB` و`Hadd.strictB` على كلّ سطرٍ من `lake exe a116-table hadd` (346,200 سطرًا).
٢. الطفرات: ثلاثُ مرايا خاطئةٍ مسمّاة يُسقطها الجدولُ نفسُه — فالمطابقةُ تفرّق لا تُصادق على كلّ شيء.
٣. الشواهد: توقّعاتٌ مكتوبةٌ باليد من الاصطلاح (حَاجَّ، ضَالِّينَ، قُلْتُ، آلْآنَ مقبولة؛ قَالْتُ مرفوضة)،
   لا محسوبةٌ بالشيفرة المفحوصة.
٤. المدوّنةُ المختومة: الرقمُ قبلُ وبعدُ واحد (لا جاهزَ سقط)، والوصلُ بعد مدٍّ يُرفض باسمه.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from pathlib import Path

import pytest

from gate import Refusal, enter, gate
from gate.contextual import Context
from gate.licence import K, continue_licensed, hadd_ok, kind_of, strict_licensed

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "formal" / "a116" / "hadd.csv"


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
