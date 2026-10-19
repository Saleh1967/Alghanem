"""الدرجةُ بعدد الأصول (`A116.RootGrade`، ADR ٢٠): شاهدُ البوّابة على المدوّنة المختومة، مستقلٌّ عن Lean.

Lean يبرهن جبرًا أنّ كلَّ خانةٍ من الـ113 تقع في صيغةٍ مرخَّصةٍ من وزنٍ ثلاثيٍّ على جذرٍ
ثلاثيٍّ بلا ألف (`cells_exhausted_within_thulathi`). وهنا الدعوى نفسُها من بنيةٍ أخرى: كلماتُ
المصحف التي تقبلها البوّابة (`gate.enter`)، ويرخّصها قيدُ الحدّ (`gate.licence.strict_licensed`)،
وتسترجعها (`gate.recover`) من جذرٍ ثلاثيٍّ بلا ألف — ذرّاتُها تغطّي الخاناتِ المرخَّصة. التوقّعُ
جدولُ `licensable.csv` المودَع (113 خانةً، يطابقه CI بجدول Lean)، لا رقمٌ تحسبه الشيفرةُ المفحوصة.
والطفرتان: ترخيصٌ أعمى عن الساكن الداخليّ، وجذورٌ رباعيّةٌ وحدها.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from functools import cache
from pathlib import Path

from gate import Refusal, enter, recover
from gate.licence import strict_licensed

ROOT = Path(__file__).resolve().parents[1]
LICENSABLE = ROOT / "formal" / "a116" / "licensable.csv"
CORPUS = ROOT / "corpora" / "quran-simple-enhanced.txt"

Words = tuple[tuple[tuple[str, ...], tuple[str, ...]], ...]  # (الذرّات، الجذور)


def _licensable() -> set[str]:
    return {line.strip() for line in LICENSABLE.open(encoding="utf-8") if line.strip()}


@cache
def _corpus_words() -> Words:
    """كلُّ كلمةٍ في المصحف تقبلها البوّابة: ذرّاتُها وجذورُ استرجاعها."""

    words: set[str] = set()
    for line in CORPUS.open(encoding="utf-8"):
        words.update(line.split())
    out = []
    for w in sorted(words):
        cert = enter(w.encode())
        if isinstance(cert, Refusal):
            continue
        _, reads = recover(w)
        out.append((tuple(cert.atoms), tuple(r[0] for r in reads)))
    return tuple(out)


def _covered(licensed: Callable[[Sequence[str]], bool], degree: int) -> set[str]:
    out: set[str] = set()
    for atoms, roots in _corpus_words():
        if licensed(atoms) and any(len(r) == degree and "ا" not in r for r in roots):
            out.update(atoms)
    return out


def test_radicals_are_the_carriers_without_alif() -> None:
    carriers = {a[0] for a in _licensable()}
    assert len(carriers) == 29  # باليد: الحواملُ التسعةُ والعشرون
    assert len(carriers - {"ا"}) == 28  # والأصولُ ثمانيةٌ وعشرون (`RootGrade.toCarrier`)
    assert not any(a[0] == "ا" and a[1:] != "ْ" for a in _licensable())  # الألفُ ساكنةٌ أبدًا


def test_cells_exhausted_within_thulathi_on_the_corpus() -> None:
    assert _covered(strict_licensed, 3) == _licensable()


def test_mutant_licence_blind_to_inner_sukun_is_caught() -> None:
    # MUTANT_NO_INNER_SUKUN: ترخيصٌ يرفض كلَّ ساكنٍ قبل الآخر لا يستنفد الخانات الساكنة
    def mutant(atoms: Sequence[str]) -> bool:
        return strict_licensed(atoms) and all(not a.endswith("ْ") for a in atoms[:-1])

    missing = _licensable() - _covered(mutant, 3)
    # يُسقط خاناتٍ ساكنة؛ ويُسقط معها متحرّكاتٍ لا تقع في كلمات الثلاثيّ هنا إلّا مع ساكنٍ داخليّ — فالشرطُ
    # «بعضُ الناقص ساكن» لا «كلُّه» (صُحِّح في كتابة الاختبار بعد النظر في الناقص، ADR ٢٠).
    assert any(a.endswith("ْ") for a in missing)


def test_mutant_quadriliteral_roots_alone_do_not_exhaust() -> None:
    # MUTANT_QUAD_FIRST: الرباعيُّ قبل الثلاثيّ لا يستنفد الـ113 في المدوّنة — فالترتيبُ ليس اعتباطًا
    assert _covered(strict_licensed, 4) < _licensable()
