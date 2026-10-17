"""الأطرُ الثلاثة (ADR ١٠٤، `A116/Itar.lean`): ترخيصُ الدالّ في شواهد Lean يُعاد بالبوّابة.

ما يفحصه هذا الملفّ ترخيصُ الدالّ وحدَه: الوصلُ بـ`gate.licence.strict_joined` (`Hadd.strictJoinB`، وهو
`strictLineB` على كلمتين بـ`NizamLine.line_two`)، والابتداءُ برفض `gate.enter` المسمّى.
والتوقّعاتُ مكتوبةٌ هنا باليد.
وأحكامُ المدلول (حقيقة، مجاز، لا حكم) لا تُعاد هنا: هي `decide` في Lean على مدلولٍ مُعطى.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from pathlib import Path

import gate
from gate import Refusal
from gate.licence import strict_joined, strict_licensed

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "formal/a116/A116/Itar.lean"

Judge = Callable[[Sequence[str], Sequence[str]], bool]

# (اليسار، اليمين، الترخيص وصلًا المتوقّع)
WASL = [
    ("نَطَقَ", "لْوَلَدُ", True),
    ("خُوْطِبَ", "لْكَلْبُ", True),
    ("نَطَقَ", "لْغُوْلُ", True),
    ("فِ", "دْدَاْرِ", True),     # «فِي الدَّارِ» بعد حذف المدّ لالتقاء الساكنين
    ("فِيْ", "دْدَاْرِ", False),  # بلا إصلاح: قافيةُ مدٍّ يقطعها الحدّ
]


def atoms(s: str) -> tuple[str, ...]:
    assert len(s) % 2 == 0, s
    return tuple(s[i:i + 2] for i in range(0, len(s), 2))


def no_seam(a: Sequence[str], b: Sequence[str]) -> bool:
    """MUTANT_NO_SEAM: السطرُ يُحكم بتسطيحه وحدَه، بلا شرط الحدّ."""

    return strict_licensed(tuple(a) + tuple(b))


def verdicts(judge: Judge) -> list[bool]:
    return [judge(atoms(a), atoms(b)) for a, b, _ in WASL]


def test_witnesses_are_lean_witnesses() -> None:
    text = LEAN.read_text(encoding="utf-8")
    for a, b, _ in WASL:
        assert f'k "{a}"' in text and f'k "{b}"' in text, (a, b)
    assert 'k "نْطَقَ"' in text


def test_wasl_by_gate() -> None:
    assert verdicts(strict_joined) == [t for _, _, t in WASL]


def test_ibtida_by_gate() -> None:
    r = gate.enter("نْطَقَ".encode())
    assert isinstance(r, Refusal) and "INITIAL_SUKUN_WITHOUT_REPAIR" in r.reasons
    # ضابطٌ موجب: كلمةٌ من المجال المختوم ابتداؤها بمتحرّك تُقبل.
    assert not isinstance(gate.enter("قَالَ".encode()), Refusal)


def test_mutant_no_seam() -> None:
    assert verdicts(no_seam) != [t for _, _, t in WASL]
