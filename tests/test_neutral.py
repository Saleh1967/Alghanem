"""الألفُ عنصرًا محايدًا: المعتلُّ والمهموزُ والمضعَّفُ في الأوزان (`A116.Neutral`، ADR ١٧).

١. المطابقة: مرآةٌ هنا لـ`Neutral.realizeN` تبني الصورَ من `wazn-body.csv` (جسمُ الأوزان من
   Lean) وتطابق `neutral.csv` (Lean على الجذور المرجعيّة الإحدى عشرة والأوزان الإحدى والثلاثين،
   وصلًا ووقفًا) سطرًا سطرًا.
٢. البوّابة: لكلّ كلمةٍ في المصحف تسترجعها البوّابةُ فعلًا معتلًّا أو مهموزًا أو مضعَّفًا في
   3MS/2MS، تُقابَل ذرّاتُها بالمرآة؛ وما لم يتطابق فجواتٌ بأسمائها (لا يُخفى منه شيء ولا يُسقط).
٣. الطفرتان: مرآةٌ تُحايد الفاء (`MUTANT_NEUTRAL_FA`) أو لا تحذف المحايدَ قبل الساكن
   (`MUTANT_NO_DROP`) تخالف Lean.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from gate import Refusal, enter, recover

ROOT = Path(__file__).resolve().parents[1]
BODY = ROOT / "formal" / "a116" / "wazn-body.csv"
NEUTRAL = ROOT / "formal" / "a116" / "neutral.csv"
CORPUS = ROOT / "corpora" / "quran-simple-enhanced.txt"
F, D, K, S = "َ", "ُ", "ِ", "ْ"
MADD = set("اوي")
ALIF = "ا" + S

LABELS = (
    [("PAST", f) for f in ("I-a", "I-i", "I-u", "II", "III", "IV", "V", "VI", "VII", "VIII", "X")]
    + [("PASSIVE", f) for f in ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "X")]
    + [("IMPERATIVE", f) for f in ("I-a", "I-i", "I-u", "II", "III", "IV", "V", "VI", "VII",
                                   "VIII", "X")]
)
Sym = tuple[str, str, str]  # ("lit", حرف، حالة) أو ("slot", رقم، حالة)


def _body() -> list[tuple[bool, int, list[Sym]]]:
    out = []
    for line in BODY.open(encoding="utf-8"):
        _, wasl, last, toks = line.rstrip("\n").split(",")
        syms: list[Sym] = [("slot", t[0], t[1:]) if t[0] in "123" else ("lit", t[0], t[1:])
                           for t in toks.split(" ")]
        out.append((wasl == "true", int(last) - 1, syms))
    return out


def _occ(syms: list[Sym], i: int) -> int:
    return sum(1 for s in syms if s[0] == "slot" and int(s[1]) - 1 == i)


def _cons_sukun(cell: str) -> bool:
    return cell[1:] == S and cell[0] not in MADD


def realize(wazn: tuple[bool, int, list[Sym]], root: str, pause: bool, h: str,
            neutral_fa: bool = False, drop: bool = True) -> list[str]:
    wasl, last, body = wazn
    syms = body + [("slot", str(last + 1), h)]
    # المضعَّف (`mergeT`)
    if body and body[-1][0] == "slot":
        j, hj = int(body[-1][1]) - 1, body[-1][2]
        if (root[j] == root[last] and j != last and root[j] not in "وي" and _occ(syms, j) == 1
                and h != S and hj != S):
            before = list(body[:-1])
            if before:
                b = before[-1]
                if b[0] == "slot" and b[2] == S and root[int(b[1]) - 1] not in "وي":
                    before[-1] = ("slot", b[1], hj)
                elif b[0] == "lit" and _cons_sukun(b[1] + b[2]):
                    before[-1] = ("lit", b[1], hj)
            syms = before + [("slot", str(j + 1), S), ("slot", str(last + 1), h)]
    # التقييمُ بالمحايد (`stepN`)
    acc: list[str] = []
    for kind, a, mark in syms:
        if kind == "lit":
            acc.append(a + mark)
            continue
        i = int(a) - 1
        if root[i] == "ء" and mark == S and acc and acc[-1] == "ء" + F:
            acc.append(ALIF)
        elif ((i != 0 or neutral_fa) and not (i == 1 and root[2] in "وي") and root[i] in "وي"
              and _occ(syms, i) == 1 and mark == F):
            if not acc:
                acc.append(root[i] + mark)
            elif acc[-1][1:] == F:
                acc.append(ALIF)
            elif _cons_sukun(acc[-1]):
                acc[-1] = acc[-1][0] + F
                acc.append(ALIF)
            else:
                acc.append(root[i] + mark)
        else:
            acc.append(root[i] + mark)
    # المحايدُ قبل ساكنٍ صحيحٍ غيرِ مدغمٍ يُحذف (`dropNeutral`)
    core: list[str] = []
    k = 0
    while k < len(acc):
        if (drop and k + 1 < len(acc) and acc[k] == ALIF and _cons_sukun(acc[k + 1])
                and (k + 2 >= len(acc) or acc[k + 2][0] != acc[k + 1][0])):
            core.append(acc[k + 1])
            k += 2
            continue
        core.append(acc[k])
        k += 1
    if pause and core:
        core[-1] = core[-1][0] + S
    if wasl and len(core) >= 2 and core[0][1:] == S:
        v = F if core[0][0] == "ل" else (D if core[1][1:] == D else K)
        core = ["ء" + v] + core
    return core


def _lean_rows() -> list[tuple[str, int, list[str], list[str]]]:
    out = []
    for line in NEUTRAL.open(encoding="utf-8"):
        root, i, cont, pause = line.rstrip("\n").split(",")
        out.append((root, int(i), cont.split(" "), pause.split(" ")))
    return out


def _last_h(i: int) -> str:
    return F if i < 20 else S


def test_mirror_matches_lean_neutral_table() -> None:
    body = _body()
    rows = _lean_rows()
    assert len(body) == 31 and len(rows) == 11 * 31
    for root, i, cont, pause in rows:
        assert realize(body[i], root, False, _last_h(i)) == cont, (root, i)
        assert realize(body[i], root, True, _last_h(i)) == pause, (root, i)


def test_lean_table_rejects_named_mutants() -> None:
    body = _body()
    rows = _lean_rows()
    fa = [r for r in rows
          if realize(body[r[1]], r[0], False, _last_h(r[1]), neutral_fa=True) != r[2]]
    nodrop = [r for r in rows
              if realize(body[r[1]], r[0], False, _last_h(r[1]), drop=False) != r[2]]
    assert fa and nodrop  # MUTANT_NEUTRAL_FA، MUTANT_NO_DROP


def _weak(root: str) -> bool:
    return len(root) == 3 and (bool(set(root) & set("وي")) or "ء" in root or root[1] == root[2])


def corpus_comparison() -> tuple[Counter[str], list[tuple[str, str, tuple[str, ...], list[str]]]]:
    body = _body()
    index = {lab: n for n, lab in enumerate(LABELS)}
    words = {w for w in CORPUS.read_text(encoding="utf-8").split() if w != "<sel>"}
    hits: Counter[str] = Counter()
    misses = []
    for w in sorted(words):
        cert = enter(w.encode("utf-8"))
        if isinstance(cert, Refusal):
            continue
        _, readings = recover(cert)
        for root, kind, form, person in readings:
            if (kind, form) not in index or not _weak(root):
                continue
            if person != ("2MS" if kind == "IMPERATIVE" else "3MS"):
                continue
            n = index[(kind, form)]
            got = realize(body[n], root, False, _last_h(n))
            # الحركةُ الأخيرة تنتظر الحدّ: يُقابَل ما سواها، والمحايدُ آخرًا ثابت
            same_carriers = [a[0] for a in got] == [a[0] for a in cert.atoms]
            if not same_carriers or got[:-1] != list(cert.atoms[:-1]):
                misses.append((w, f"{kind}/{form}/{root}", cert.atoms, got))
            else:
                hits[f"{kind}/{form}"] += 1
    return hits, misses


def test_gate_corpus_weak_hamza_doubled() -> None:
    hits, misses = corpus_comparison()
    assert sum(hits.values()) > 0
    # كلُّ ما لم يتطابق مسمًّى في فجوةٍ من فجوات ADR ١٧ (لا فجوةَ بلا اسم)
    named = {gap_of(lab, atoms) for _, lab, atoms, _ in misses}
    assert "UNNAMED" not in named, [m for m in misses if gap_of(m[1], m[2]) == "UNNAMED"][:5]


def gap_of(label: str, atoms: tuple[str, ...]) -> str:
    kind, form, root = label.split("/")
    if kind == "PASSIVE" and set(root[1:]) & set("وي"):
        return "PASSIVE_WEAK_NOT_NEUTRAL"
    if kind == "IMPERATIVE":
        return "IMPERATIVE_WEAK_DELETION"
    if form == "VIII" and root[0] in "ويء" + "صضطظدذز":
        return "IFTAAL_IBDAL"
    if label == "PAST/X/حوذ":
        return "ISTAHWADHA_NOT_NEUTRALIZED"
    if root[0] in "وي":
        return "MITHAL"
    if root[2] in "وي" and atoms[-1][0] == "ي":
        return "LAM_YA_AFTER_KASRA"
    return "UNNAMED"
