"""شبكةُ الأوزان: الترخيصُ الجبريُّ التدريجيُّ من المصدر — مرآةُ `formal/Slge/Shabaka.lean`.

**الجبر.** على القالب ثلاثُ عمليّاتٍ لا غير (`Edit`): إدخالُ رمزٍ في موضع (`ins`)، حذفُ زائدٍ
(`del`)، وتغييرُ حالةِ موضعٍ (`set`). والمبرهَن (`Slge.Shabaka.wf_run`) أنّ كلَّ تتابعٍ منها
يحفظ سلامةَ القالب — الأصلُ يبقى مستردًّا — فلا تُفقَد الفاءُ والعينُ واللام في أيّ درجة. وبعد كلّ
درجةٍ يُحكَم الترخيصُ على القالب وحدَه (`Wazn.licensed_fill_indep`)، فهذا هو **الترخيصُ
التدريجيّ**: خطوةٌ جبريّة، ثمّ حكمٌ، ثمّ خطوة.

**المسافة.** `distance(a, b)` أقلُّ عددِ عمليّاتٍ تحوّل القالبَ a إلى b (لِيفنشتاين على الرموز:
تغييرُ حالةِ الرمز نفسِه عمليّةٌ واحدة، وتبديلُ رمزٍ بآخرَ حذفٌ فإدخال). متماثلةٌ، فأقلُّ شجرةٍ
موجَّهةٍ من جذرٍ = أقلُّ شجرةٍ مولِّدة (Prim)، **محسوبةٌ لا مقرَّرة**: `minimal_tree(root)`.

**الترتيبان.**
- `COMPUTED`: الشجرةُ الأقلُّ كلفةً من المصدر المجرّد (فَعْل) على الأوزان كلِّها.
- `CLASSICAL`: ترتيبُ البصريّين المودَع (المصدرُ أصلُ المشتقّات؛ الماضي فالمضارع فالأمر؛ المزيدُ
  من المجرّد؛ مصدرُ المزيد ومشتقّاتُه من مضارعه) — **معلن**، كلُّ حافّةٍ فيه مفحوصةٌ بالآلة: الابنُ
  = الأبُ بعد `diff`، وكلفتُها محسوبة.
- `agreement()`: كم أبًا يتّفق فيه الترتيبان — **مقيس** يُطبع ولا يُدَّعى.

والجامدُ ليس في الشبكة: لا أبَ له ولا ابن (قيدٌ معجميّ)، فجذرُ الشبكة المصدرُ المشتقُّ المجرّد.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Final

from slge.cells import STATES, licensed
from slge.wazn import AWZAN, Sym, Template, Wazn, mizan

__all__ = [
    "CLASSICAL", "COMPUTED", "ROOT", "Edit", "agreement", "apply", "diff", "distance",
    "edge_costs", "minimal_tree", "reachable",
]


@dataclass(frozen=True, slots=True)
class Edit:
    """عمليّةٌ على القالب: `ins` (موضع، رمز)، `del` (موضع)، `set` (موضع، حالة)."""

    op: str
    pos: int
    sym: Sym | None = None
    state: str | None = None


def apply(t: Template, edits: Sequence[Edit]) -> Template:
    """تطبيقُ العمليّات بالترتيب؛ حذفُ أصلٍ مرفوضٌ باسمه."""

    out = list(t)
    for e in edits:
        if e.op == "ins" and e.sym is not None:
            out.insert(e.pos, e.sym)
        elif e.op == "del":
            if not _deletable(out, e.pos):
                raise ValueError("CANNOT_DELETE_ROOT_SLOT")
            del out[e.pos]
        elif e.op == "set" and e.state in STATES:
            s = out[e.pos]
            out[e.pos] = Sym(s.slot, s.carrier, e.state)
        else:
            raise ValueError(f"UNKNOWN_EDIT:{e.op}")
    return tuple(out)


def _deletable(t: Sequence[Sym], pos: int) -> bool:
    """يُحذف الزائد، ولا يُحذف الأصلُ إلّا مكرَّرًا (موضعُه حاضرٌ في غيره: فكُّ التضعيف)."""

    s = t[pos]
    return s.slot is None or any(k != pos and x.slot == s.slot for k, x in enumerate(t))


def _anchors(t: Sequence[Sym]) -> frozenset[int]:
    """مواضعُ أوّل ظهورٍ للفاء والعين واللام."""

    seen: dict[int, int] = {}
    for k, s in enumerate(t):
        if s.slot is not None:
            seen.setdefault(s.slot, k)
    return frozenset(seen.values())


def _same(a: Sym, b: Sym) -> bool:
    return a.slot == b.slot and a.carrier == b.carrier


def diff(a: Template, b: Template) -> tuple[Edit, ...]:
    """أقلُّ تتابعِ عمليّاتٍ من a إلى b (لِيفنشتاين على الرموز؛ لا يُحذف أصلٌ إلّا مكرَّرًا)؛
    `apply(a, diff(a, b)) == b`."""

    inf = 10**6
    n, m = len(a), len(b)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    # المرساة: أوّلُ ظهورٍ لكلّ موضعٍ لا يُحذف ولا يُدخَل؛ فالمسافةُ متماثلةٌ وكلُّ خطوةٍ تحفظ الأصل
    dels = [inf if i in _anchors(a) else 1 for i in range(n)]
    inss = [inf if j in _anchors(b) else 1 for j in range(m)]
    for i in range(1, n + 1):
        d[i][0] = d[i - 1][0] + dels[i - 1]
    for j in range(1, m + 1):
        d[0][j] = d[0][j - 1] + inss[j - 1]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            sub = 0 if a[i - 1] == b[j - 1] else (1 if _same(a[i - 1], b[j - 1]) else inf)
            d[i][j] = min(d[i - 1][j] + dels[i - 1], d[i][j - 1] + inss[j - 1],
                          d[i - 1][j - 1] + sub)
    edits: list[Edit] = []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and _same(a[i - 1], b[j - 1]):
            sub = 0 if a[i - 1] == b[j - 1] else 1
            if d[i][j] == d[i - 1][j - 1] + sub:
                if sub:
                    edits.append(Edit("set", i - 1, state=b[j - 1].state))
                i, j = i - 1, j - 1
                continue
        if i > 0 and d[i][j] == d[i - 1][j] + dels[i - 1]:
            edits.append(Edit("del", i - 1))
            i -= 1
        else:
            edits.append(Edit("ins", i, sym=b[j - 1]))
            j -= 1
    return tuple(edits)  # من آخر القالب إلى أوّله، فلا تنزاح المواضع


def distance(a: Template, b: Template) -> int:
    return len(diff(a, b))


ROOT: Final[str] = "فَعْلٌ"
"""جذرُ الشبكة: المصدرُ المشتقُّ المجرّد (البصريّون: المصدرُ أصلُ المشتقّات)."""

_BY_NAME: Final[dict[str, Wazn]] = {w.name: w for w in AWZAN}
_NAMES: Final[tuple[str, ...]] = tuple(w.name for w in AWZAN)


def edge_costs() -> dict[tuple[str, str], int]:
    """كلفةُ كلّ زوجٍ (متماثلة)."""

    out: dict[tuple[str, str], int] = {}
    for i, a in enumerate(_NAMES):
        for b in _NAMES[i + 1:]:
            c = distance(_BY_NAME[a].template, _BY_NAME[b].template)
            out[(a, b)] = out[(b, a)] = c
    return out


def minimal_tree(root: str = ROOT) -> dict[str, str]:
    """أقلُّ شجرةٍ مولِّدةٍ من الجذر (Prim)؛ الابنُ ← أبوه. عند التعادل الأسبقُ في الجدول."""

    cost = edge_costs()
    parent: dict[str, str] = {}
    inside = [root]
    best: dict[str, tuple[int, int, str]] = {
        n: (cost[(root, n)], _NAMES.index(root), root) for n in _NAMES if n != root
    }
    while best:
        n = min(best, key=lambda k: (best[k][0], best[k][1], _NAMES.index(k)))
        _, _, p = best.pop(n)
        parent[n] = p
        inside.append(n)
        for k in best:
            ck = cost[(n, k)]
            if (ck, _NAMES.index(n)) < best[k][:2]:
                best[k] = (ck, _NAMES.index(n), n)
    return parent


COMPUTED: Final[dict[str, str]] = minimal_tree()

CLASSICAL: Final[dict[str, str]] = {
    # المصدرُ المجرّد أصلُ الماضي المجرّد؛ وسائرُ مصادر الثلاثيّ أخواتُ فَعْل
    "فَعَلَ": "فَعْلٌ", "فَعِلَ": "فَعْلٌ", "فَعُلَ": "فَعْلٌ",
    "فُعُولٌ": "فَعْلٌ", "فَعَالَةٌ": "فَعْلٌ", "فُعُولَةٌ": "فَعْلٌ", "فَعَلَانٌ": "فَعْلٌ",
    "فُعَالٌ": "فَعْلٌ", "فِعَالٌ": "فَعْلٌ", "فَعَلٌ": "فَعْلٌ", "فِعَالَةٌ": "فَعْلٌ",
    # الماضي ← المجهول والمضارع؛ المضارع ← الأمر
    "فُعِلَ": "فَعَلَ", "يَفْعَلُ": "فَعِلَ", "يَفْعِلُ": "فَعَلَ", "يَفْعُلُ": "فَعُلَ",
    "يُفْعَلُ": "فُعِلَ", "اِفْعَلْ": "يَفْعَلُ", "اِفْعِلْ": "يَفْعِلُ", "اُفْعُلْ": "يَفْعُلُ",
    # المشتقّاتُ من الثلاثيّ: من الماضي المجرّد
    "فَاعِلٌ": "فَعَلَ", "مَفْعُولٌ": "فَعَلَ", "فَعَّالٌ": "فَاعِلٌ", "مِفْعَالٌ": "فَاعِلٌ",
    "فَعُولٌ": "فَاعِلٌ", "فَعِيلٌ": "فَعُلَ", "أَفْعَلُ": "فَعِلَ", "فَعْلَانُ": "فَعِلَ",
    "مَفْعَلٌ": "يَفْعَلُ", "مَفْعِلٌ": "يَفْعِلُ", "مَفْعَلَةٌ": "مَفْعَلٌ",
    "مِفْعَلٌ": "فَعَلَ", "مِفْعَالٌ (آلة)": "مِفْعَلٌ", "مِفْعَلَةٌ": "مِفْعَلٌ", "فَعَّالَةٌ": "فَعَّالٌ",
    "فَعْلَةٌ": "فَعْلٌ", "فِعْلَةٌ": "فَعْلٌ", "فَعْلِيَّةٌ": "فَعْلٌ",
    # المزيد: ماضيه من الماضي المجرّد؛ مضارعُه من ماضيه؛ مصدرُه ومشتقّاتُه من مضارعه
    "أَفْعَلَ": "فَعَلَ", "فَعَّلَ": "فَعَلَ", "فَاعَلَ": "فَعَلَ", "تَفَعَّلَ": "فَعَّلَ",
    "تَفَاعَلَ": "فَاعَلَ", "اِنْفَعَلَ": "فَعَلَ", "اِفْتَعَلَ": "فَعَلَ", "اِفْعَلَّ": "فَعِلَ",
    "اِسْتَفْعَلَ": "فَعَلَ",
    "يُفْعِلُ": "أَفْعَلَ", "يُفَعِّلُ": "فَعَّلَ", "يُفَاعِلُ": "فَاعَلَ", "يَتَفَعَّلُ": "تَفَعَّلَ",
    "يَتَفَاعَلُ": "تَفَاعَلَ", "يَنْفَعِلُ": "اِنْفَعَلَ", "يَفْتَعِلُ": "اِفْتَعَلَ", "يَفْعَلُّ": "اِفْعَلَّ",
    "يَسْتَفْعِلُ": "اِسْتَفْعَلَ",
    "إِفْعَالٌ": "أَفْعَلَ", "تَفْعِيلٌ": "فَعَّلَ", "مُفَاعَلَةٌ": "فَاعَلَ", "فِعَالٌ (مفاعلة)": "فَاعَلَ",
    "تَفَعُّلٌ": "تَفَعَّلَ", "تَفَاعُلٌ": "تَفَاعَلَ", "اِنْفِعَالٌ": "اِنْفَعَلَ", "اِفْتِعَالٌ": "اِفْتَعَلَ",
    "اِفْعِلَالٌ": "اِفْعَلَّ", "اِسْتِفْعَالٌ": "اِسْتَفْعَلَ",
    "مُفْعِلٌ": "يُفْعِلُ", "مُفْعَلٌ": "مُفْعِلٌ", "مُفَعِّلٌ": "يُفَعِّلُ", "مُفَعَّلٌ": "مُفَعِّلٌ",
    "مُفَاعِلٌ": "يُفَاعِلُ", "مُفَاعَلٌ": "مُفَاعِلٌ", "مُتَفَعِّلٌ": "يَتَفَعَّلُ", "مُتَفَاعِلٌ": "يَتَفَاعَلُ",
    "مُنْفَعِلٌ": "يَنْفَعِلُ", "مُفْتَعِلٌ": "يَفْتَعِلُ", "مُفْتَعَلٌ": "مُفْتَعِلٌ", "مُسْتَفْعِلٌ": "يَسْتَفْعِلُ",
    "مُسْتَفْعَلٌ": "مُسْتَفْعِلٌ",
    # التأنيث من مذكّره
    "فَاعِلَةٌ": "فَاعِلٌ", "فَعْلَاءُ": "أَفْعَلُ", "فَعْلَى": "فَعْلَانُ", "فُعْلَى": "أَفْعَلُ",
    # الجموع من مفردها المجرّد (فَعْل) أو من وزن مفردها
    "أَفْعُلٌ": "فَعْلٌ", "أَفْعَالٌ": "فَعْلٌ", "أَفْعِلَةٌ": "فِعَالٌ", "فِعْلَةٌ (جمع)": "فَعْلٌ",
    "فُعْلٌ": "أَفْعَلُ", "فُعُلٌ": "فِعَالٌ", "فُعَلٌ": "فَعْلٌ",
    "فِعَلٌ": "فِعْلَةٌ", "فَعَلَةٌ": "فَاعِلٌ", "فُعَلَةٌ": "فَاعِلٌ", "فِعَالٌ (جمع)": "فَعْلٌ",
    "فُعُولٌ (جمع)": "فَعْلٌ", "فُعَّالٌ": "فَاعِلٌ", "فُعَّلٌ": "فَاعِلٌ", "فِعْلَانٌ": "فَعْلٌ",
    "فُعْلَانٌ": "فَعْلٌ", "فُعَلَاءُ": "فَعِيلٌ", "أَفْعِلَاءُ": "فَعِيلٌ",
    "مَفَاعِلُ": "مَفْعَلٌ", "مَفَاعِيلُ": "مَفْعُولٌ", "فَوَاعِلُ": "فَاعِلٌ", "فَعَائِلُ": "فَعِيلٌ",
    "أَفَاعِلُ": "أَفْعَلُ", "أَفَاعِيلُ": "إِفْعَالٌ", "تَفَاعِيلُ": "تَفْعِيلٌ", "فَعَالِي": "فَعْلَى",
    "فَعَالَى": "فَعْلَى", "فُعَالَى": "فُعْلَى", "فَيَاعِلُ": "فَاعِلٌ", "فَعَاعِيلُ": "فَعَّالٌ",
    # أمرُ المزيد من مضارعه (كأمر المجرّد)
    "أَفْعِلْ": "يُفْعِلُ", "فَعِّلْ": "يُفَعِّلُ", "فَاعِلْ": "يُفَاعِلُ", "تَفَعَّلْ": "يَتَفَعَّلُ",
    "تَفَاعَلْ": "يَتَفَاعَلُ", "اِنْفَعِلْ": "يَنْفَعِلُ", "اِفْتَعِلْ": "يَفْتَعِلُ", "اِسْتَفْعِلْ": "يَسْتَفْعِلُ",
}
"""ترتيبُ البصريّين (معلن): الابنُ ← أبوه. كلُّ حافّةٍ مفحوصةٌ: `apply(أب, diff) == ابن`."""


def reachable(parent: dict[str, str], root: str = ROOT) -> bool:
    """أكلُّ وزنٍ يصل إلى الجذر بلا دور؟"""

    for n in _NAMES:
        seen = {n}
        while n != root:
            n = parent.get(n, "")
            if not n or n in seen:
                return False
            seen.add(n)
    return True


def agreement() -> tuple[int, int, tuple[str, ...]]:
    """(المتّفق، الكلّ، المختلف): أينَ يختار الحسابُ أبًا غيرَ أبي البصريّين."""

    same = [n for n in CLASSICAL if COMPUTED[n] == CLASSICAL[n]]
    other = tuple(n for n in CLASSICAL if COMPUTED[n] != CLASSICAL[n])
    return len(same), len(CLASSICAL), other


def _check() -> None:
    for child, p in CLASSICAL.items():
        a, b = _BY_NAME[p].template, _BY_NAME[child].template
        if apply(a, diff(a, b)) != b or not licensed(mizan(b)):
            raise ValueError(f"BAD_EDGE:{p}->{child}")
    if not reachable(CLASSICAL) or not reachable(COMPUTED):
        raise ValueError("NETWORK_NOT_ROOTED")


_check()
