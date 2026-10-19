"""الإعلالُ والإبدال على الذرّات — مرآةُ `formal/a116/A116/Ilal.lean`.

القاعدةُ تعديلٌ موضعيٌّ على سلسلة الذرّات (حرفٌ + علامة) له سجلٌّ يردّ الأصلَ بعينه (`restore`).
المبرهَن هناك: الردُّ لكلّ قاعدة (مثولات `edit_roundtrip`)، والإغلاقُ (قلبٌ بين متحرّكين، نقل، حذفُ
ما بين متحرّكين، إبدالُ حامل)، والإلزامُ في حذف عين الأجوف (`hadhf_ayn_forced`: الأصلُ غيرُ مرخَّص).
وهنا: `apply(rule, atoms, i)` و`restore(atoms, record)`، وشواهدُ القواعد الاثنتي عشرة في
`tests/test_ilal.py` مع فحص الترخيص الثلاثيّ لكلّ صورة.
"""

from __future__ import annotations

from typing import Final

__all__ = ["RULES", "Record", "apply", "restore"]

FATHA: Final = "َ"
DAMMA: Final = "ُ"
KASRA: Final = "ِ"
SUKUN: Final = "ْ"
ALIF, WAW, YA, HAMZA, TA, TTA, DAL = "ا", "و", "ي", "ء", "ت", "ط", "د"
ITBAQ: Final = "صضطظ"
DZZ: Final = "دذز"

Record = tuple[str, int, int, tuple[str, ...]]
"""(القاعدة، start، insertedLength، removed) — `Recovery.EditRecord` بعينه."""

RULES: Final[tuple[str, ...]] = (
    "QALB_AYN", "HADHF_AYN", "NAQL", "QALB_LAM", "HADHF_LAM", "HADHF_WAW",
    "HAMZA_MADD", "TA_TTA", "TA_DAL", "FA_TA", "WAW_YA", "YA_WAW",
)


def _mark(a: str) -> str:
    return a[1:]


def _vowelled(a: str) -> bool:
    return _mark(a) != SUKUN


def apply(rule: str, atoms: tuple[str, ...], i: int) -> tuple[tuple[str, ...], Record]:
    """تطبيقُ القاعدة في الموضع ‎i‎؛ `ValueError` باسمٍ إن لم ينطبق شرطُها."""

    a = list(atoms)

    def rec(start: int, inserted: int, removed: list[str]) -> Record:
        return (rule, start, inserted, tuple(removed))

    if rule == "QALB_AYN":  # قَوَلَ ← قَالَ: (و|ي، فتحة) بين متحرّكين، وما قبلها مفتوح
        if not (0 < i < len(a) - 1 and a[i][0] in (WAW, YA) and _mark(a[i]) == FATHA
                and _mark(a[i - 1]) == FATHA and _vowelled(a[i + 1])):
            raise ValueError("QALB_AYN_NOT_APPLICABLE")
        removed = [a[i]]
        a[i] = ALIF + SUKUN
        return tuple(a), rec(i, 1, removed)

    if rule == "HADHF_AYN":  # قَالْتُ ← قُلْتُ: ألفٌ ساكنةٌ ثمّ ساكن؛ تُحذف وتُنقل حركةُ الأصل إلى الفاء
        if not (0 < i < len(a) - 1 and a[i] == ALIF + SUKUN and _mark(a[i + 1]) == SUKUN):
            raise ValueError("HADHF_AYN_NOT_APPLICABLE")
        removed = [a[i - 1], a[i]]
        new_fa = a[i - 1][0] + (DAMMA if a[i + 1][0] != YA else KASRA)
        a[i - 1 : i + 1] = [new_fa]
        return tuple(a), rec(i - 1, 1, removed)

    if rule == "NAQL":  # يَقْوُلُ ← يَقُولُ: ساكنٌ ثمّ (و|ي) متحرّك ثمّ متحرّك
        if not (0 < i < len(a) - 2 and _mark(a[i]) == SUKUN and a[i + 1][0] in (WAW, YA)
                and _vowelled(a[i + 1]) and _vowelled(a[i + 2]) and _vowelled(a[i - 1])):
            raise ValueError("NAQL_NOT_APPLICABLE")
        removed = [a[i], a[i + 1]]
        a[i : i + 2] = [a[i][0] + _mark(a[i + 1]), a[i + 1][0] + SUKUN]
        return tuple(a), rec(i, 2, removed)

    if rule == "QALB_LAM":  # دَعَوَ ← دَعَا: (و|ي، فتحة) في الآخر بعد فتحة
        if not (i == len(a) - 1 and i > 0 and a[i][0] in (WAW, YA) and _mark(a[i]) == FATHA
                and _mark(a[i - 1]) == FATHA):
            raise ValueError("QALB_LAM_NOT_APPLICABLE")
        removed = [a[i]]
        a[i] = ALIF + SUKUN
        return tuple(a), rec(i, 1, removed)

    if rule == "HADHF_LAM":  # دَعَوُوْا ← دَعَوْا: لامٌ (و|ي) متحرّكة قبل واو الجماعة الساكنة
        if not (0 < i < len(a) - 1 and a[i][0] in (WAW, YA) and _vowelled(a[i])
                and a[i + 1] == WAW + SUKUN):
            raise ValueError("HADHF_LAM_NOT_APPLICABLE")
        removed = [a[i]]
        del a[i]
        return tuple(a), rec(i, 0, removed)

    if rule == "HADHF_WAW":  # يَوْعِدُ ← يَعِدُ: واوٌ ساكنةٌ بين متحرّكين
        if not (0 < i < len(a) - 1 and a[i] == WAW + SUKUN and _vowelled(a[i - 1])
                and _vowelled(a[i + 1])):
            raise ValueError("HADHF_WAW_NOT_APPLICABLE")
        removed = [a[i]]
        del a[i]
        return tuple(a), rec(i, 0, removed)

    # 7–12: إبدالُ حاملٍ مع بقاء العلامة (`ibdal_restore`، `admissible_replace_carrier`)
    swaps = {
        "HAMZA_MADD": (lambda j: a[j] == HAMZA + SUKUN and j > 0 and a[j - 1][0] == HAMZA
                       and _mark(a[j - 1]) == FATHA, ALIF),
        "TA_TTA": (lambda j: a[j][0] == TA and j > 0 and a[j - 1][0] in ITBAQ
                   and _mark(a[j - 1]) == SUKUN, TTA),
        "TA_DAL": (lambda j: a[j][0] == TA and j > 0 and a[j - 1][0] in DZZ
                   and _mark(a[j - 1]) == SUKUN, DAL),
        "FA_TA": (lambda j: a[j][0] in (WAW, YA) and _mark(a[j]) == SUKUN and j + 1 < len(a)
                  and a[j + 1][0] == TA, TA),
        "WAW_YA": (lambda j: a[j] == WAW + SUKUN and j > 0 and _mark(a[j - 1]) == KASRA, YA),
        "YA_WAW": (lambda j: a[j] == YA + SUKUN and j > 0 and _mark(a[j - 1]) == DAMMA, WAW),
    }
    if rule not in swaps:
        raise ValueError(f"UNKNOWN_RULE:{rule}")
    cond, carrier = swaps[rule]
    if not (0 <= i < len(a) and cond(i)):
        raise ValueError(f"{rule}_NOT_APPLICABLE")
    removed = [a[i]]
    a[i] = carrier + _mark(a[i])
    return tuple(a), rec(i, 1, removed)


def restore(atoms: tuple[str, ...], record: Record) -> tuple[str, ...]:
    """`Recovery.restoreEdit`: ‎take start ++ removed ++ drop (start + inserted)‎."""

    _, start, inserted, removed = record
    return tuple(atoms[:start]) + tuple(removed) + tuple(atoms[start + inserted :])
