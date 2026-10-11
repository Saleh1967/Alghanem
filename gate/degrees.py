"""جداولُ الدرجات: مرآةُ `A116.Exhaust` في بايثون (ADR ١٥).

درجةُ الكلمة عددُ مقاطعها في التقطيع المبرهَن (`Stages.parse`). وجدولُ الدرجة d وصلًا
(`Exhaust.table`): ‎d − 1‎ مقطعًا داخليًّا من {CV، CVV، CVC، CVVC} ثمّ طرفيٌّ من {CV، CVV، CVC}
— ‎3·4^(d−1)‎ صفًّا بلا تكرار (`table_length`، `table_nodup`). والعددُ في الدرجة مولَّدٌ من العدد
السابق: ‎N(t ++ [s]) = 4·N(t) + d(s)‎ (`codeI_snoc`)، وعددُ الكلمة ‎3·N(داخليّة) + d(طرفيّ)‎
(`codeW`). وكلُّ كلمةٍ مرخَّصةٍ بقيد الحدّ وصلًا، غيرِ مدّ الفرق، صفٌّ في جدول درجتها
(`strict_mem_table`) — فـ`degree_of` لا يرفض شهادةً جاهزةً إلّا مدَّ الفرق باسمه.

المطابقةُ بجدول `lake exe a116-table degrees` (255 سطرًا مودَعًا) في `tests/test_degrees.py`.
و`attestation` تعدّ على المدوّنة المختومة ما شُهد من صفوف كلّ درجة، ويسجّلها
`tools/gen_claims.py` بمولِّدها.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Sequence
from typing import Any, Final

from .licence import kind_of, parse

INNER: Final[tuple[str, ...]] = ("CV", "CVV", "CVC", "CVVC")
"""المقاطعُ الداخليّةُ وصلًا بأرقامها (`Exhaust.dC`)."""
FINAL: Final[tuple[str, ...]] = ("CV", "CVV", "CVC")
"""المقاطعُ الطرفيّةُ وصلًا (`Exhaust.final`): لا CVCC ولا CVVCC (وقفٌ)، ولا CVVC (لا مثلَ بعد المُغلِق)."""


def decode_inner(k: int, n: int) -> list[str]:
    """`Exhaust.decodeI`."""

    return [] if k == 0 else decode_inner(k - 1, n // 4) + [INNER[n % 4]]


def code_inner(ss: Sequence[str]) -> int:
    """`Exhaust.codeI`: أرقامٌ بالأساس 4، الأقدمُ أعلى."""

    n = 0
    for s in ss:
        n = 4 * n + INNER.index(s)
    return n


def decode_word(k: int, n: int) -> list[str]:
    """`Exhaust.decodeW`: صفُّ الدرجة k+1 ذو العدد n."""

    return decode_inner(k, n // 3) + [INNER[n % 3]]


def table(degree: int) -> list[list[str]]:
    """`Exhaust.table (degree − 1)`."""

    k = degree - 1
    return [decode_word(k, n) for n in range(3 * 4**k)]


def code_word(ss: Sequence[str]) -> int | None:
    """عددُ الصفّ في جدول درجته، أو `None` إن لم يكن صفًّا فيه."""

    if not ss or ss[-1] not in FINAL or any(s not in INNER for s in ss[:-1]):
        return None
    return 3 * code_inner(ss[:-1]) + INNER.index(ss[-1])


def degree_of(atoms: Sequence[str]) -> tuple[int, int, tuple[str, ...]] | str:
    """ذرّاتُ شهادةٍ ← (الدرجة، العدد، المقاطع)، أو اسمُ رفضٍ: `NOT_A_TABLE_ROW` (ومنه مدُّ الفرق)."""

    parsed = parse(kind_of(atoms))
    if parsed is None or parsed[0] != "none":
        return "NOT_A_TABLE_ROW"
    ss = tuple(parsed[1])
    n = code_word(ss)
    if n is None:
        return "NOT_A_TABLE_ROW"
    return len(ss), n, ss


def attestation(surfaces: Iterable[str]) -> dict[str, Any]:
    """على المدوّنة المختومة: لكلّ درجةٍ عددُ الصور، وحجمُ الجدول، والمشهودُ من صفوفه، وغيرُ
    المشهود بأسمائه (للدرجات 1–3)؛ وما ليس صفًّا باسمه. المرفوضُ من البوّابة لا يدخل (لا يُعدّ ولا
    يُخمَّن)."""

    from . import Refusal, enter

    forms: Counter[int] = Counter()
    rows: dict[int, set[tuple[str, ...]]] = {}
    outside: Counter[str] = Counter()
    refused = 0
    for w in surfaces:
        cert = enter(w.encode("utf-8"))
        if isinstance(cert, Refusal):
            refused += 1
            continue
        got = degree_of(cert.atoms)
        if isinstance(got, str):
            outside[got] += 1
            continue
        d, _, ss = got
        forms[d] += 1
        rows.setdefault(d, set()).add(ss)
    by_degree: dict[str, Any] = {}
    for d in sorted(forms):
        size = 3 * 4 ** (d - 1)
        entry: dict[str, Any] = {"forms": forms[d], "table": size, "attested": len(rows[d])}
        if d <= 3:
            entry["unattested"] = ["-".join(r) for r in table(d) if tuple(r) not in rows[d]]
        by_degree[str(d)] = entry
    return {"refused_by_gate": refused, "not_a_table_row": dict(outside), "degrees": by_degree}
