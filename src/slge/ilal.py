"""الإعلالُ والإبدال: جبرٌ مغلقٌ صعودًا ونزولًا — مرآةُ `Slge.Ilal` (هندسةٌ عكسيّةٌ لـ`A116.Ilal`).

القاعدةُ **صعودٌ** `up` من الأصل إلى الصورة في نافذةٍ تبدأ بالخانة التي قبل موضع التعديل، و**نزولٌ**
`down`
من الصورة إلى الأصول التي يصعد كلٌّ منها إلى الصورة بعينها. المبرهَن في Lean: النزولُ عكسُ الصعود
(`down_sound`/`undo_sound`) ولا أصلَ يفوت (`down_complete`/`undo_complete`)؛ والإغلاقُ على الترخيص
عبر الجسر
إلى أدوات الغانم بعينها (`qalbAyn_closed`، `naql_closed`، `hadhfWaw_closed`، `ibdal_closed`،
`hadhfAyn_forced`، `qalbLam_closed`، `hadhfLam_closed`)؛ وكلُّ ما ينزل إليه القارئُ حتى خطوتين يصعد
بسلسلته
(`descend_ascends`) وما صعد بخطوةٍ في موضعه ينزل (`descend_complete`). الشروطُ اللغويّة (حرفُ المضارعة،
ضمُّ اللام قبل واو الجماعة، مواضعُ النوافذ) معلَنةٌ لا مبرهَنة — كما في الغانم.
"""

from __future__ import annotations

from typing import Final

from slge.cells import SUKUN, Cell

__all__ = ["RULES", "Chain", "Record", "apply", "ascend", "descend", "down", "positions", "record",
           "restore", "undo", "up"]

Word = tuple[Cell, ...]
Chain = tuple[tuple[str, int], ...]
RULES: Final[tuple[str, ...]] = (
    "QALB_AYN", "HADHF_AYN_U", "HADHF_AYN_I", "NAQL", "QALB_LAM", "HADHF_LAM", "HADHF_WAW",
    "HAMZA_MADD", "TA_TTA", "TA_DAL", "FA_TA", "WAW_YA", "YA_WAW",
)
"""القواعدُ بترتيب `Rule.all` (حذفُ العين بوجهيه: ضمُّ الفاء أو كسرُها)."""
_A: Final = "فتح"
_I: Final = "كسر"
_U: Final = "ضم"
ALIF: Final[Cell] = ("ا", SUKUN)
GW: Final[Cell] = ("و", SUKUN)
"""واوٌ ساكنة (واوُ الجماعة)."""
_WY_DAMMA: Final[tuple[Cell, ...]] = (("و", _U), ("ي", _U))


def _vow(x: Cell) -> bool:
    return x[1] != SUKUN


def _wy(x: Cell) -> bool:
    return x[0] in "وي"


def _mudari(x: Cell) -> bool:
    return x[0] in "ءنتي"


def up(rule: str, win: Word) -> Word | None:
    """الصعودُ في نافذة: الأصلُ ← الصورة؛ `None` إن لم ينطبق الشرط."""

    n = len(win)
    if rule == "QALB_AYN" and n >= 3:  # قَوَلَ ← قَالَ (وقَوَلْتُ ← قَالْتُ ثمّ الحذفُ ملزَم)
        p, y = win[0], win[1]
        if p[1] == _A and _wy(y) and y[1] == _A:
            return (p, ALIF, *win[2:])
    elif rule in ("HADHF_AYN_U", "HADHF_AYN_I") and n >= 3:  # قَالْتُ ← قُلْتُ / بَاعْتُ ← بِعْتُ
        p, y, t = win[0], win[1], win[2]
        if p[1] == _A and y == ALIF and not _vow(t):
            return ((p[0], _U if rule == "HADHF_AYN_U" else _I), *win[2:])
    elif rule == "NAQL" and n >= 4:  # يَقْوُلُ ← يَقُولُ
        p, x, y, z = win[0], win[1], win[2], win[3]
        if _vow(p) and not _vow(x) and _wy(y) and _vow(y) and _vow(z):
            return (p, (x[0], y[1]), (y[0], SUKUN), *win[3:])
    elif rule == "QALB_LAM" and n == 2:  # دَعَوَ ← دَعَا
        p, y = win
        if p[1] == _A and _wy(y) and y[1] == _A:
            return (p, ALIF)
    elif rule == "HADHF_LAM" and n >= 3:  # دَعَوُوْ ← دَعَوْ: اللامُ مضمومةٌ قبل واو الجماعة
        p, y, g = win[0], win[1], win[2]
        if _vow(p) and _wy(y) and y[1] == _U and g == GW:
            return (p, *win[2:])
    elif rule == "HADHF_WAW" and n >= 3:  # يَوْعِدُ ← يَعِدُ: بعد حرف المضارعة
        p, y, z = win[0], win[1], win[2]
        if _mudari(p) and _vow(p) and y == GW and _vow(z):
            return (p, *win[2:])
    elif rule == "HAMZA_MADD" and n >= 2:  # ءَءْمَنَ ← ءَامَنَ
        if win[0] == ("ء", _A) and win[1] == ("ء", SUKUN):
            return (win[0], ALIF, *win[2:])
    elif rule == "TA_TTA" and n >= 2:  # اصْتَبَرَ ← اصْطَبَرَ
        p, y = win[0], win[1]
        if p[0] in "صضطظ" and not _vow(p) and y[0] == "ت":
            return (p, ("ط", y[1]), *win[2:])
    elif rule == "TA_DAL" and n >= 2:  # ازْتَادَ ← ازْدَادَ
        p, y = win[0], win[1]
        if p[0] in "دذز" and not _vow(p) and y[0] == "ت":
            return (p, ("د", y[1]), *win[2:])
    elif rule == "FA_TA" and n >= 2:  # اوْتَصَلَ ← اتْتَصَلَ
        y, t = win[0], win[1]
        if _wy(y) and not _vow(y) and t[0] == "ت":
            return (("ت", SUKUN), *win[1:])
    elif rule == "WAW_YA" and n >= 2:  # مِوْزَان ← مِيزَان
        p, y = win[0], win[1]
        if p[1] == _I and y == GW:
            return (p, ("ي", SUKUN), *win[2:])
    elif rule == "YA_WAW" and n >= 2:  # مُيْقِن ← مُوقِن
        p, y = win[0], win[1]
        if p[1] == _U and y == ("ي", SUKUN):
            return (p, GW, *win[2:])
    return None


def down(rule: str, win: Word) -> tuple[Word, ...]:
    """النزولُ في نافذة: الأصولُ التي يصعد كلٌّ منها إلى النافذة بعينها."""

    n = len(win)
    if rule == "QALB_AYN" and n >= 3:
        p, y = win[0], win[1]
        if p[1] == _A and y == ALIF:
            return ((p, ("و", _A), *win[2:]), (p, ("ي", _A), *win[2:]))
    elif rule in ("HADHF_AYN_U", "HADHF_AYN_I") and n >= 2:
        f, t = win[0], win[1]
        if f[1] == (_U if rule == "HADHF_AYN_U" else _I) and not _vow(t):
            return (((f[0], _A), ALIF, *win[1:]),)
    elif rule == "NAQL" and n >= 4:
        p, x, y, z = win[0], win[1], win[2], win[3]
        if _vow(p) and _vow(x) and _wy(y) and not _vow(y) and _vow(z):
            return ((p, (x[0], SUKUN), (y[0], x[1]), *win[3:]),)
    elif rule == "QALB_LAM" and n == 2:
        p, y = win
        if p[1] == _A and y == ALIF:
            return ((p, ("و", _A)), (p, ("ي", _A)))
    elif rule == "HADHF_LAM" and n >= 2:
        p, g = win[0], win[1]
        if _vow(p) and g == GW:
            return tuple((p, y, *win[1:]) for y in _WY_DAMMA)
    elif rule == "HADHF_WAW" and n >= 2:
        p, z = win[0], win[1]
        if _mudari(p) and _vow(p) and _vow(z):
            return ((p, GW, *win[1:]),)
    elif rule == "HAMZA_MADD" and n >= 2:
        if win[0] == ("ء", _A) and win[1] == ALIF:
            return ((win[0], ("ء", SUKUN), *win[2:]),)
    elif rule == "TA_TTA" and n >= 2:
        p, y = win[0], win[1]
        if p[0] in "صضطظ" and not _vow(p) and y[0] == "ط":
            return ((p, ("ت", y[1]), *win[2:]),)
    elif rule == "TA_DAL" and n >= 2:
        p, y = win[0], win[1]
        if p[0] in "دذز" and not _vow(p) and y[0] == "د":
            return ((p, ("ت", y[1]), *win[2:]),)
    elif rule == "FA_TA" and n >= 2:
        y, t = win[0], win[1]
        if y == ("ت", SUKUN) and t[0] == "ت":
            return ((("و", SUKUN), *win[1:]), (("ي", SUKUN), *win[1:]))
    elif rule == "WAW_YA" and n >= 2:
        p, y = win[0], win[1]
        if p[1] == _I and y == ("ي", SUKUN):
            return ((p, GW, *win[2:]),)
    elif rule == "YA_WAW" and n >= 2:
        p, y = win[0], win[1]
        if p[1] == _U and y == GW:
            return ((p, ("ي", SUKUN), *win[2:]),)
    return ()


def apply(rule: str, w: Word, i: int) -> Word | None:
    """تطبيقُ القاعدة في الموضع `i` (أوّلُ النافذة = الخانةُ قبل موضع التعديل)."""

    v = up(rule, w[i:])
    return None if v is None else (*w[:i], *v)


def undo(rule: str, w: Word, i: int) -> tuple[Word, ...]:
    """الأصولُ في الموضع `i`؛ كلٌّ منها يعيد `w` بـ`apply` بعينه (`undo_sound`)."""

    return tuple((*w[:i], *u) for u in down(rule, w[i:]))


Record = tuple[int, int, Word]
"""سجلُّ التعديل (البداية، طولُ المدرَج، المحذوف) — `A116.Recovery.EditRecord` بعينه."""


def record(rule: str, u: Word, i: int) -> Record:
    """سجلُّ تطبيق القاعدة في الموضع `i` من الأصل (`Ilal.record`)."""

    d = u[i:]
    if rule in ("HADHF_AYN_U", "HADHF_AYN_I") and len(d) >= 2:
        return (i, 1, d[:2])
    if rule == "NAQL" and len(d) >= 3:
        return (i + 1, 2, d[1:3])
    if rule in ("HADHF_LAM", "HADHF_WAW") and len(d) >= 2:
        return (i + 1, 0, d[1:2])
    if rule == "FA_TA" and len(d) >= 1:
        return (i, 1, d[:1])
    if len(d) >= 2:
        return (i + 1, 1, d[1:2])
    return (i, 0, ())


def restore(out: Word, rec: Record) -> Word:
    """`Recovery.restoreEdit`: ‎take start ++ removed ++ drop (start + inserted)‎ — الردُّ بالسجلّ هو
    الأصلُ بعينه لكلّ قاعدةٍ وأصلٍ وموضع (`apply_roundtrip`)."""

    start, inserted, removed = rec
    return (*out[:start], *removed, *out[start + inserted:])


def positions(rule: str, n: int) -> tuple[int, ...]:
    """مواضعُ النافذة في جذعٍ طولُه `n`: حذفُ واو المثال في الصدر، وحذفُ لام الناقص في الآخر، والباقي في
    أيّ
    موضع — شرطٌ معلَن."""

    if rule == "HADHF_WAW":
        return (0,)
    if rule == "HADHF_LAM":
        return (max(n - 1, 0),)
    return tuple(range(n))


def ascend(chain: Chain, u: Word) -> Word | None:
    """الصعودُ بسلسلةٍ من الأصل إلى الصورة."""

    cur: Word | None = u
    for rule, i in chain:
        if cur is None:
            return None
        cur = apply(rule, cur, i)
    return cur


def _step1(w: Word, n: int) -> tuple[tuple[str, int, Word], ...]:
    return tuple((rule, i, u) for rule in RULES for i in positions(rule, n) for u in undo(rule, w,
    i))


def descend(w: Word, n: int) -> tuple[tuple[Chain, Word], ...]:
    """النزولُ حتى خطوتين: (سلسلةُ الصعود، الأصل)؛ `n` طولُ الجذع في الكلمة. كلُّ أصلٍ يصعد بسلسلته إلى
    `w`
    بعينها (`descend_ascends`)."""

    out: list[tuple[Chain, Word]] = []
    for rule, i, u in _step1(w, n):
        out.append((((rule, i),), u))
        out.extend((((s, j), (rule, i)), v) for s, j, v in _step1(u, n))
    return tuple(out)


def _check() -> None:
    from slge.rawabit import cells_of

    qala, qawala = cells_of("قَالَ"), cells_of("قَوَلَ")
    assert apply("QALB_AYN", qawala, 0) == qala
    assert (("QALB_AYN", 0),) in {ch for ch, u in descend(qala, 3) if u == qawala}
    qul = cells_of("قُلْ")
    assert ascend((("QALB_AYN", 0), ("HADHF_AYN_U", 0)), cells_of("قَوَلْ")) == qul
    assert any(u == cells_of("قَوَلْ") for _, u in descend(qul, 2))
    assert apply("NAQL", cells_of("يَقْوُلُ"), 0) == cells_of("يَقُولُ")
    assert apply("HADHF_WAW", cells_of("يَوْعِدُ"), 0) == cells_of("يَعِدُ")
    assert apply("HAMZA_MADD", cells_of("ءَءْمَنَ"), 0) == cells_of("ءَامَنَ")
    for w in (qala, qul, cells_of("يَقُولُ"), cells_of("دَعَا"), cells_of("مِيزَانُ")):
        for ch, u in descend(w, len(w)):
            assert ascend(ch, u) == w, (ch, u)  # النزولُ عكسُ الصعود بعينه
    for rule in RULES:
        for i in range(len(qawala)):
            v = apply(rule, qawala, i)
            if v is not None:
                assert qawala in undo(rule, v, i), (rule, i)  # لا أصلَ يفوت
                assert restore(v, record(rule, qawala, i)) == qawala  # الردُّ بالسجلّ (roundtrip)
    assert restore(cells_of("يَقُولُ"), record("NAQL", cells_of("يَقْوُلُ"), 0)) == cells_of("يَقْوُلُ")


_check()
