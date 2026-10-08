"""الترخيصُ الثلاثيّ نصًّا: مرآةُ `A116.Stages` و`A116.Ternary` في بايثون.

النموذجُ الثنائيّ (`A116.Admissible`: لا ابتداءَ بساكن، لا تجاورَ ساكنين) أعمى عن المدّ
(`binary_is_blind_to_madd`)، فيرفض «حَاجَّ» وهي مرخَّصةٌ وصلًا (`continue_strictly_extends_binary`).
فهذه الوحدةُ تُسقط ذرّاتِ الـ116 على الأصناف الثلاثة `cv | v | c`، ثمّ تقطّعها كما يقطّعها
`Stages.parse`، وتحكم بـ`ContinueLicensed` و`PauseLicensed` كما في `Ternary.lean`.

كلُّ دالّةٍ هنا تقابل تعريفًا في Lean باسمه، ومطابقتُها بالشواهد الثلاثة المسمّاة هناك
(`hajja`، `bahr`، `tamm`) في `tests/test_gate.py`. وإسقاطُ الذرّةِ على صنفها (`kind_of`) مرآةُ
`A116.Hadd.kindOf`، وقيدُ الحدّ (`hadd_ok`، `strict_licensed`) مرآةُ `Hadd.haddB` و`Hadd.strictB`،
ومطابقتُهما بجدول `lake exe a116-table hadd` (346,200 سطرًا) في `tests/test_hadd.py`؛ والحدُّ بين كلمتين
(`strict_joined`) مرآةُ `Hadd.strictJoinB` بجدول `hadd-join` (293,904 سطرًا).

«ساكن» في الذرّة معناه موضعيّ: موضعٌ لا تتبعه حركةٌ قصيرة. فحرفُ المدّ (`اْ` بعد فتحة) ساكنٌ موضعًا
وجزءٌ ثانٍ من حركةٍ طويلةٍ نطقًا، ودورُه `v` هو ما يفرّقه عن المُغلِق `c`.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Final, Literal

K = Literal["cv", "v", "c"]
Syl = Literal["CV", "CVV", "CVC", "CVVC", "CVCC", "CVVCC"]
Lead = Literal["none", "C", "V", "VC"]

SUKUN: Final = "ْ"
_MADD: Final[dict[str, str]] = {"ا": "َ", "و": "ُ", "ي": "ِ"}

_SYL_OF: Final[dict[tuple[str, ...], Syl]] = {
    (): "CV",
    ("v",): "CVV",
    ("c",): "CVC",
    ("v", "c"): "CVVC",
    ("c", "c"): "CVCC",
    ("v", "c", "c"): "CVVCC",
}
_LEAD_OF: Final[dict[tuple[str, ...], Lead]] = {
    (): "none",
    ("c",): "C",
    ("v",): "V",
    ("v", "c"): "VC",
}
PAUSE_ONLY: Final[frozenset[str]] = frozenset({"CVCC", "CVVCC"})


def kind_of(atoms: Sequence[str]) -> list[K]:
    """ذرّةٌ ← صنفُها (معلن): متحرّكٌ `cv`؛ حرفُ مدٍّ ساكنٌ بعد حركته `v`؛ وإلّا ساكنٌ `c`."""

    out: list[K] = []
    for i, atom in enumerate(atoms):
        carrier, mark = atom[0], atom[1:]
        if mark != SUKUN:
            out.append("cv")
        elif i > 0 and _MADD.get(carrier) == atoms[i - 1][1:]:
            out.append("v")
        else:
            out.append("c")
    return out


def run(k: Sequence[K]) -> tuple[list[K], list[K]]:
    """`Stages.run`: ما قبل أوّل متحرّك، وما بقي."""

    for i, a in enumerate(k):
        if a == "cv":
            return list(k[:i]), list(k[i:])
    return list(k), []


def syls(k: Sequence[K]) -> list[Syl] | None:
    """`Stages.syls`: المقاطعُ من سلسلةٍ تبدأ بمتحرّك."""

    out: list[Syl] = []
    rest = list(k)
    while rest:
        if rest[0] != "cv":
            return None
        coda, rest = run(rest[1:])
        s = _SYL_OF.get(tuple(coda))
        if s is None:
            return None
        out.append(s)
    return out


def parse(k: Sequence[K]) -> tuple[Lead, list[Syl]] | None:
    """`Stages.parse`: القطعةُ الصادرةُ ثمّ المقاطع."""

    lead_atoms, body = run(k)
    lead = _LEAD_OF.get(tuple(lead_atoms))
    ss = syls(body)
    if lead is None or ss is None:
        return None
    return lead, ss


def continue_licensed(k: Sequence[K]) -> bool:
    """`Ternary.continueB`: بلا قطعةٍ صادرة، ولا مقطعَ وقفيًّا."""

    p = parse(k)
    return p is not None and p[0] == "none" and all(s not in PAUSE_ONLY for s in p[1])


def pause_licensed(k: Sequence[K]) -> bool:
    """`Ternary.pauseB`: كذلك، إلّا المقطعَ الأخير."""

    p = parse(k)
    return p is not None and p[0] == "none" and all(s not in PAUSE_ONLY for s in p[1][:-1])


def binary_ok(k: Sequence[K]) -> bool:
    """`Ternary.binOK` = `A116.Admissible` بعد إسقاط `v` و`c` على ساكن."""

    s = [a != "cv" for a in k]
    return bool(s) and not s[0] and all(not (a and b) for a, b in zip(s, s[1:]))


def _carrier(atom: str) -> str:
    return atom[0]


def _is_farq(atoms: Sequence[str]) -> bool:
    """`Hadd.isFarq`: مدُّ الفرق — ءَ اْ لْ في أوّل الكلمة (آلْآنَ)."""

    return len(atoms) >= 3 and atoms[0] == "ءَ" and atoms[1] == "اْ" and _carrier(atoms[2]) == "ل"


def _geminate(pairs: Sequence[tuple[K, str]]) -> bool:
    """`Hadd.geminateB`: كلُّ `v` يليه `c` فالـ`c` يليه حاملُه نفسُه (أوّلُ مثلين)."""

    for i in range(len(pairs) - 1):
        if pairs[i][0] == "v" and pairs[i + 1][0] == "c":
            if i + 2 >= len(pairs) or _carrier(pairs[i + 1][1]) != _carrier(pairs[i + 2][1]):
                return False
    return True


def hadd_ok(atoms: Sequence[str]) -> bool:
    """`Hadd.haddB`: التقاءُ الساكنين على حدّه، إلّا مدَّ الفرق في أوّل الكلمة."""

    pairs = list(zip(kind_of(atoms), atoms))
    return _geminate(pairs[2:] if _is_farq(atoms) else pairs)


def strict_licensed(atoms: Sequence[str]) -> bool:
    """`Hadd.strictB`: مرخَّصٌ ثلاثيًّا وصلًا، وكلُّ قافيةِ مدٍّ فيه مدغمة (أو مدُّ فرق)."""

    return continue_licensed(kind_of(atoms)) and hadd_ok(atoms)


def straddles(left: Sequence[str], right: Sequence[str]) -> bool:
    """`Hadd.straddles`: قافيةُ مدٍّ يقطعها الحدّ — `v | c` أو `v c | x`."""

    k = kind_of(tuple(left) + tuple(right))
    b = len(left)
    return (b >= 1 and b < len(k) and k[b - 1] == "v" and k[b] == "c") or (
        b >= 2 and k[b - 2] == "v" and k[b - 1] == "c"
    )


def strict_joined(left: Sequence[str], right: Sequence[str]) -> bool:
    """`Hadd.strictJoinB`: الموصولُ مرخَّصٌ بالقيد، ولا قافيةَ مدٍّ يقطعها الحدّ (الاستثناءُ داخلَ الكلمة)."""

    return strict_licensed(tuple(left) + tuple(right)) and not straddles(left, right)


def licence(atoms: Sequence[str]) -> tuple[Lead, list[Syl]] | None:
    """ذرّاتٌ ← تقطيعُها الثلاثيّ، أو `None` إن لم تُقطَّع."""

    return parse(kind_of(atoms))
