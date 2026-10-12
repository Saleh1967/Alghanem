"""الماضي ← المضارعُ بزائدةٍ من «أنيت» ← الأمرُ بإزالة الزوائد (`A116.Mudari`، ADR ٢٤).

١. المطابقة: مرآةٌ هنا لتعريفات Lean (`mudari`، `amr`، `amrWasl`) تطابق `amr.csv` (Lean على الجذور
   المرجعيّة × الأوزان التسعة × الأبواب) سطرًا سطرًا: المضارعُ رفعًا، والمجزوم، والأمر، وهمزةُ الوصل.
٢. الشاهد: البوّابةُ لا تعرف المضارع، وتكتب الأمرَ من قوالبها (`gate.derive`) — شيفرةٌ سابقةٌ لهذا
   القانون. فلكلّ جذرٍ ثلاثيٍّ تسترجعه البوّابةُ من المصحف، يُقابَل الأمرُ المشتقُّ بالإزالة بأوامر
   البوّابة؛ والمطابَقُ يُعدّ، وكلُّ ما لم يُطابَق في فجوةٍ مسمّاة (`gap_of`) — لا فجوةَ بلا اسم.
   والأرقامُ في `CLAIMS.md` بمولِّدها.
٣. الطفرتان: همزةُ وصلٍ بقاعدة لام الأداة (`MUTANT_ARTICLE_WASL_IN_VERB`) وأمرٌ لا يعيد همزةَ أفعل
   (`MUTANT_NO_IV_RESTORE`) تخالفان Lean.
٤. باليد: أمثلةُ المالك — قُمْ، اذْهَبْ، خُذْ، أَعْطِ، قِ، صِ، رَ، عِ.
"""

from __future__ import annotations

import unicodedata
from collections import Counter
from pathlib import Path

from gate import Refusal, derive, enter, recover

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "formal" / "a116" / "amr.csv"
CORPUS = ROOT / "corpora" / "quran-simple-enhanced.txt"
F, D, K, S = "َ", "ُ", "ِ", "ْ"
MADD = {F: "ا", D: "و", K: "ي"}
VOWEL_OF = {"ا": F, "و": D, "ي": K}
FORMS = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "X")
REF = ("كتب", "قوم", "بيع", "دعو", "رمي", "وعد", "وقي", "ءمن", "رءي", "مدد", "صبر")
TAKHFIF = ("رءي",)
HADHF_FA = ("ءخذ", "ءكل", "ءمر")
Cell = tuple[str, str]
TC = tuple[Cell, int | None]


def _weak(c: str) -> bool:
    return c in "وي"


def _ta(c: str) -> str:
    return "ط" if c in "صضطظ" else "د" if c in "دذز" else "ت"


def _body(r: str, b: str, f: str) -> tuple[str, list[TC]]:
    def rad(i: int, h: str) -> TC:
        return ((r[i], h), i)

    def lit(c: str, h: str) -> TC:
        return ((c, h), None)

    return {
        "I": (F, [rad(0, S), rad(1, b)]),
        "II": (D, [rad(0, F), rad(1, S), rad(1, K)]),
        "III": (D, [rad(0, F), lit("ا", S), rad(1, K)]),
        "IV": (D, [lit("ء", F), rad(0, S), rad(1, K)]),
        "V": (F, [lit("ت", F), rad(0, F), rad(1, S), rad(1, F)]),
        "VI": (F, [lit("ت", F), rad(0, F), lit("ا", S), rad(1, F)]),
        "VII": (F, [lit("ن", S), rad(0, F), rad(1, K)]),
        "VIII": (F, [(("ت" if _weak(r[0]) else r[0], S), 0), ((_ta(r[0]), F), None), rad(1, K)]),
        "X": (F, [lit("س", S), lit("ت", F), rad(0, S), rad(1, K)]),
    }[f]


def _cons_sukun(c: Cell) -> bool:
    return c[1] == S and c[0] not in "اوي"


def _occ(xs: list[TC], i: int) -> int:
    return sum(1 for x in xs if x[1] == i)


def mudari(r: str, f: str, b: str, pre: str, e: str, *, article_wasl: bool = False) -> list[Cell]:
    pv, bd = _body(r, b, f)
    if f == "IV":
        bd = bd[1:]
    xs: list[TC] = [((pre, pv), None), *bd, ((r[2], e), 2)]
    if f == "I" and r[0] == "و" and b == K:  # المثال
        xs = [x for x in xs if x[1] != 0]
    if (len(xs) >= 3 and r[1] == r[2] and not _weak(r[1]) and xs[-2][1] == 1 and _occ(xs, 1) == 1
            and xs[-1][0][1] != S and xs[-2][0][1] != S and _cons_sukun(xs[-3][0])):  # المضعَّف
        p, a, ll = xs[-3], xs[-2], xs[-1]
        xs = [*xs[:-3], ((p[0][0], a[0][1]), p[1]), ((a[0][0], S), a[1]), ll]
    if r in TAKHFIF and f == "I" and b == F:  # تخفيفُ همزة رأى (المجرّدُ بابَ يَفْعَلُ)
        for j in range(len(xs) - 1):
            p, a = xs[j], xs[j + 1]
            if a[1] == 1 and a[0][0] == "ء" and _cons_sukun(p[0]):
                xs = [*xs[:j], ((p[0][0], a[0][1]), p[1]), *xs[j + 2:]]
                break
    cnt = _occ(xs, 1)  # الأجوف
    for j in range(len(xs) - 1):
        p, a = xs[j], xs[j + 1]
        if a[1] == 1 and _weak(r[1]) and not _weak(r[2]) and cnt == 1 and a[0][1] != S:
            if _cons_sukun(p[0]) or (p[1] == 0 and p[0][1] == S):
                xs = [*xs[:j], ((p[0][0], a[0][1]), p[1]), ((MADD[a[0][1]], S), a[1]), *xs[j + 2:]]
                break
            if p[0][1] == F and j > 0:
                xs = [*xs[:j + 1], (("ا", S), a[1]), *xs[j + 2:]]
                break
    if _weak(r[2]) and len(xs) >= 2:  # الناقص
        ll, p = xs[-1], xs[-2]
        if ll[0][1] == S:
            xs = xs[:-1]
        elif p[0][1] != S:
            xs = [*xs[:-1], ((MADD[p[0][1]], S), ll[1])]
    return [x[0] for x in _drop_madd(xs)]


def _drop_madd(xs: list[TC]) -> list[TC]:
    """المدُّ قبل ساكنٍ صحيحٍ غيرِ مدغمٍ يُحذف — `Mudari.dropMadd` بعينها."""

    if len(xs) < 3:
        return xs
    p, m, c = xs[0], xs[1], xs[2]
    nxt = xs[3][0][0] if len(xs) > 3 else None
    if m[0][1] == S and VOWEL_OF.get(m[0][0]) == p[0][1] and _cons_sukun(c[0]) and nxt != c[0][0]:
        return [p, *_drop_madd(xs[2:])]
    return [p, *_drop_madd(xs[1:])]


def amr_rest(r: str, f: str, b: str, *, restore: bool = True) -> list[Cell]:
    """إزالةُ الزوائد — `Mudari.amrRest`."""

    rest = mudari(r, f, b, "ت", S)[1:]
    if f == "IV" and restore:
        if rest and rest[0] == ("ء", S):
            rest = [("ء", F), ("ا", S), *rest[1:]]
        else:
            rest = [("ء", F), *rest]
    if f == "I" and b == D and r in HADHF_FA and rest and rest[0] == ("ء", S):
        rest = rest[1:]
    return rest


def amr(r: str, f: str, b: str, *, article_wasl: bool = False, restore: bool = True
        ) -> tuple[list[Cell], bool]:
    """الأمر وأأقام قانونُ الابتداء همزةَ وصل — `Mudari.amr` و`amrWasl`."""

    rest = amr_rest(r, f, b, restore=restore)
    if rest and rest[0][1] == S:
        nxt = rest[1] if len(rest) > 1 else None
        if article_wasl and rest[0][0] == "ل":
            v = F
        else:
            v = D if nxt is not None and nxt[1] == D else K
        return [("ء", v), *rest], True
    return rest, False


def _atoms(cells: list[Cell]) -> str:
    return " ".join(c + h for c, h in cells)


def _babs(r: str, f: str) -> tuple[str, ...]:
    if f != "I":
        return (K,)
    if r[0] == "و" and _weak(r[2]):
        return (K,)
    if r[1] == "ي" and not _weak(r[2]):
        return (F, K)
    return (F, D, K)


def _rows() -> list[list[str]]:
    return [line.rstrip("\n").split(",") for line in TABLE.open(encoding="utf-8")]


def test_mirror_matches_lean_amr_table() -> None:
    rows = _rows()
    want = [[str(i), f, b, _atoms(mudari(r, f, b, "ي", D)), _atoms(mudari(r, f, b, "ت", S)),
             _atoms(amr(r, f, b)[0]), "true" if amr(r, f, b)[1] else "false"]
            for i, r in enumerate(REF) for f in FORMS for b in _babs(r, f)]
    assert rows == want


def test_lean_table_rejects_named_mutants() -> None:
    rows = {(r[0], r[1], r[2]): r[5] for r in _rows()}
    lqy = _atoms(amr("لقي", "VIII", K, article_wasl=True)[0])
    assert lqy.startswith("ءَ")  # MUTANT_ARTICLE_WASL_IN_VERB: الْتَقِ بفتح
    assert _atoms(amr("لقي", "VIII", K)[0]).startswith("ءِ")
    i = str(REF.index("ءمن"))
    # MUTANT_NO_IV_RESTORE
    assert rows[(i, "IV", K)] != _atoms(amr("ءمن", "IV", K, restore=False)[0])


def render(form: tuple[list[Cell], bool]) -> str:
    """الذرّاتُ بكتابة `gate.derive`: همزةُ الوصل ألفٌ عارية، وحرفُ المدّ بلا علامة، والمثلان شدّة."""

    cells, wasl = form
    s = ""
    j = 0
    while j < len(cells):
        c, h = cells[j]
        if j == 0 and wasl:
            s += "ا"
            j += 1
            continue
        if (j + 1 < len(cells) and h == S and cells[j + 1][0] == c and cells[j + 1][1] != S
                and c != "ا"):
            s += c + "ّ" + cells[j + 1][1]
            j += 2
            continue
        after_wasl = j == 1 and wasl
        if h == S and c in "اوي" and j > 0 and MADD.get(cells[j - 1][1]) == c and not after_wasl:
            s += c
            j += 1
            continue
        s += c + h
        j += 1
    return unicodedata.normalize("NFC", s)


def gap_of(root: str, form: str) -> str:
    """فجواتٌ مسمّاة: ما يخالف فيه الأمرُ المشتقُّ أوامرَ البوّابة، بسببه."""

    if root in TAKHFIF and form == "I":
        return "RAA_TAKHFIF_OWNER_OVER_GATE"  # نصُّ المالك «رَ»، والبوّابةُ «ارْءَ» بلا تخفيف
    if root[1] == root[2] == "ء":
        return "HAMZA_DOUBLED_ROOT"
    if "ا" in root:
        return "ALIF_IN_ROOT"
    if form == "VIII" and root[0] == "ي" and _weak(root[1]):
        return "YA_FA_IFTAAL_HOLLOW"
    return "UNNAMED"


def corpus_comparison() -> dict[str, object]:
    words = {w for w in CORPUS.read_text(encoding="utf-8").split() if w != "<sel>"}
    roots: set[str] = set()
    for w in words:
        cert = enter(w.encode("utf-8"))
        if isinstance(cert, Refusal):
            continue
        roots.update(r for r, *_ in recover(cert)[1] if len(r) == 3)
    hits: Counter[str] = Counter()
    gaps: Counter[str] = Counter()
    for r in sorted(roots):
        d = derive(r)
        for f in FORMS:
            gate = {unicodedata.normalize("NFC", w) for w, a in d.items() for x in a
                    if x[0] == "IMPERATIVE" and x[2] == "2MS"
                    and (x[1] == f or (f == "I" and (x[1] == "I" or x[1].startswith("I-"))))}
            if not gate:
                continue
            for b in _babs(r, f):
                if render(amr(r, f, b)) in gate:
                    hits[f] += 1
                else:
                    gaps[gap_of(r, f)] += 1
    return {"roots": len(roots), "matched": sum(hits.values()), "matched_by_form": dict(hits),
            "gaps": dict(gaps)}


def test_gate_imperatives_witness_the_law() -> None:
    out = corpus_comparison()
    gaps = out["gaps"]
    assert isinstance(gaps, dict)
    assert "UNNAMED" not in gaps, gaps
    assert out["matched"] > 7000


def test_owner_examples_by_hand() -> None:
    assert render(amr("قوم", "I", D)) == "قُمْ"
    assert render(amr("ذهب", "I", F)) == "اذْهَبْ"
    assert render(amr("ءخذ", "I", D)) == "خُذْ"
    assert render(amr("عطو", "IV", K)) == "أَعْطِ".replace("أ", "ء")
    assert render(amr("وقي", "I", K)) == "قِ"
    assert render(amr("وصي", "I", K)) == "صِ"
    assert render(amr("رءي", "I", F)) == "رَ"
    assert render(amr("وعي", "I", K)) == "عِ"
