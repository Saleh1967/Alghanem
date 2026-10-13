"""القرينةُ من «المخصَّص» (ADR ٥٩): صفوفٌ باليد، وإعادةُ الأعداد بشيفرةٍ مستقلّة من المودَعين
المصدرين، وقاعدةُ الاختيار على أمثلةٍ باليد.

التوقّعات:

* عنوانا العقدتين 135 و479 منقولان باليد من `nodes.tsv`.
* الأعداد (782، 566، 558، 207، 199) هي ما برهنه `A116.Qarina` على `QarinaData`، وتُعاد هنا من
  `wad.tsv` و`membership.tsv` بطيٍّ مكتوبٍ هنا لا بطيّ الأداة. فإن انحرف المولِّد سقط أحدُ الطرفين.

الطفراتُ بأسمائها:

* `MUTANT_SHARED_QARINA`: القرينةُ تُقبل وإن كانت في حقل أخيه، فيختار معنًى حيث يجب الرفض.
* `MUTANT_FIRST_HIT`: يُؤخذ أوّلُ ما بيّنته القرائن بلا فحص التعارض.
* `MUTANT_NO_HAMZA_FOLD`: ألفُ لين في الجذر لا تُردّ همزةً، فتنقص الأزواجُ التي لها حقل.
"""

from __future__ import annotations

import importlib.util
import sys
from collections.abc import Callable, Sequence
from typing import Any

from conftest import ROOT

SPEC = importlib.util.spec_from_file_location("gen_qarina", ROOT / "tools" / "gen_qarina.py")
assert SPEC and SPEC.loader
MOD: Any = importlib.util.module_from_spec(SPEC)
sys.modules["gen_qarina"] = MOD
SPEC.loader.exec_module(MOD)

WAD = ROOT / "corpora" / "wad" / "wad.tsv"
MEMBERSHIP = ROOT / "corpora" / "mukhassas" / "membership.tsv"
NODES = ROOT / "corpora" / "mukhassas" / "nodes.tsv"
HAMZA = {"أ": "ء", "إ": "ء", "ؤ": "ء", "ئ": "ء", "ى": "ي"}


def _hamza(root: str) -> str:
    """طيٌّ مكتوبٌ هنا: ألفُ لين همزة، وصورُ الهمزة همزة، والمدّةُ همزةٌ وألف."""

    out = []
    for ch in root.replace("آ", "ءا"):
        out.append("ء" if ch == "ا" else HAMZA.get(ch, ch))
    return "".join(out)


def _mushtarak() -> dict[str, list[str]]:
    by: dict[str, list[str]] = {}
    for ln in WAD.read_text(encoding="utf-8").splitlines():
        k, r, _ = ln.split("\t")
        by.setdefault(k, []).append(r)
    return {k: v for k, v in by.items() if len(v) > 1}


def _membership() -> dict[str, set[int]]:
    out: dict[str, set[int]] = {}
    for ln in MEMBERSHIP.read_text(encoding="utf-8").splitlines():
        r, ns = ln.split("\t")
        out[r] = {int(x) for x in ns.split()}
    return out


def _field(fold: Callable[[str], str]) -> Callable[[str], set[int]]:
    mem = _membership()
    return lambda r: mem.get(fold(r), set())


def _counts(f: Callable[[str], set[int]]) -> tuple[int, int, int, int, int]:
    pairs = covered = sep = lafz_cov = lafz_sep = 0
    for ms in _mushtarak().values():
        all_cov = all_sep = True
        for m in ms:
            others: set[int] = set()
            for x in ms:
                if x != m:
                    others |= f(x)
            pairs += 1
            covered += bool(f(m))
            all_cov &= bool(f(m))
            ok = bool(f(m) - others)
            sep += ok
            all_sep &= ok
        lafz_cov += all_cov
        lafz_sep += all_sep
    return pairs, covered, sep, lafz_cov, lafz_sep


def test_deposit_is_what_the_tool_writes() -> None:
    assert MOD.main(["--check"]) == 0


def test_counts_recomputed_independently() -> None:
    assert _counts(_field(_hamza)) == (782, 566, 558, 207, 199)


def test_mutant_no_hamza_fold_rejected() -> None:
    """`MUTANT_NO_HAMZA_FOLD`: بلا ردّ الألف همزةً تسقط حقولُ الجذور المهموزة."""

    def no_fold(r: str) -> str:
        return "".join(HAMZA.get(ch, ch) for ch in r)

    assert _counts(_field(no_fold))[1] < 566


def _titles() -> dict[int, str]:
    out = {}
    for i, ln in enumerate(NODES.read_text(encoding="utf-8").splitlines()):
        if i:
            a = ln.split("\t")
            out[int(a[0])] = a[4]
    return out


def test_qala_by_hand() -> None:
    f = _field(_hamza)
    assert _mushtarak()["قَ اْ ل"] == ["قول", "قيل"]
    assert 135 in f("قول") and 135 not in f("قيل")
    assert 479 in f("قيل") and 479 not in f("قول")
    t = _titles()
    assert t[135] == "كثرة الكلام والخطأ فيه" and t[479] == "النوم"


QALA = ["قول", "قيل"]


def _fq(m: str) -> Sequence[int]:
    """حقلان صغيران باليد: 1 لقول وحده، 2 لقيل وحده، 3 لهما."""

    return {"قول": [1, 3], "قيل": [2, 3]}[m]


def test_choose_by_hand() -> None:
    assert MOD.mub(QALA, _fq, 1, "قول") and not MOD.mub(QALA, _fq, 3, "قول")
    assert MOD.choose(QALA, _fq, [1]) == "قول"
    assert MOD.choose(QALA, _fq, [2, 3]) == "قيل"
    assert MOD.choose(QALA, _fq, [3]) is None
    assert MOD.choose(QALA, _fq, [1, 2]) is None
    assert MOD.decide_row(QALA, _fq, [3]) == ("NO_QARINA", None)
    assert MOD.decide_row(QALA, _fq, [1, 2]) == ("QARINA_CONFLICT", None)
    assert MOD.by_count(QALA, _fq, [1, 1, 2]) is None
    assert MOD.by_field_size(["قول", "قيل"], lambda m: {"قول": [1], "قيل": [1, 2]}[m]) == "قيل"


def test_mutant_shared_qarina_rejected() -> None:
    """`MUTANT_SHARED_QARINA`: قرينةٌ في الحقلين تُقبل، فيُختار قول على [3] والصوابُ الرفض."""

    def mutant(ms: Sequence[str], f: Callable[[str], Sequence[int]],
               ctx: Sequence[int]) -> str | None:
        hs = [m for m in ms if any(q in ctx for q in f(m))]
        return hs[0] if hs else None

    assert mutant(QALA, _fq, [3]) != MOD.choose(QALA, _fq, [3])


def test_mutant_first_hit_rejected() -> None:
    """`MUTANT_FIRST_HIT`: أوّلُ ما بيّنته القرائن بلا فحص التعارض يختار قول على [1، 2]."""

    def mutant(ms: Sequence[str], f: Callable[[str], Sequence[int]],
               ctx: Sequence[int]) -> str | None:
        hs = MOD.hits(ms, f, ctx)
        return hs[0] if hs else None

    assert mutant(QALA, _fq, [1, 2]) != MOD.choose(QALA, _fq, [1, 2])


def test_verdict_rule_by_hand() -> None:
    assert MOD.verdict([0.9, 0.95], 0.5, [0.4, 0.6], 29) == "QARINA_TOO_FEW"
    assert MOD.verdict([0.7, 0.8], 0.5, [0.4, 0.6], 40) == "QARINA_INFORMATIVE"
    assert MOD.verdict([0.3, 0.6], 0.5, [0.4, 0.6], 40) == "QARINA_NOT_INFORMATIVE"
    assert MOD.verdict([0.55, 0.7], 0.5, [0.4, 0.6], 40) == "QARINA_UNDECIDED"
