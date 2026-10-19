"""السلسلةُ كلمةً كلمة على المصحف (ADR ١١٤، المهمّة ٣) — مرآةُ `A116.Silsila` والقياسُ المسجَّلُ مسبقًا.

ينفّذ `docs/silsila/PREREG.md` بعينه:
* المرآة: `khutwa` و`ahkam` و`ramz` كما في `A116/Silsila.lean`، و`tajrid` و`judhur_of` و`ajnas_of`
  و`haml_of` كما في `A116/SilsilaQurra.lean`، ويُطابَق جدولُ Lean `formal/a116/silsila.csv`
  (`tests/test_silsila.py`).
* الطبقات الخمس: الشهادة (`gate.enter`)، والقسم (قارئُ D3₂ مبنيًّا من أسماء علاماته المودَعة في
  نتائج التسجيلات الخمسة)، والصيغةُ والجذر (`gate.recover(peel=True)` للفعل وهياكلُ ابن فارس للاسم)،
  والجنس (كتبُ «المخصَّص»)، والحمل (الوضع، و«لسان العرب» راوٍ مؤكِّد، و`Haqaiq.naql`).
* قبل القياس يُعاد D3₂ على B (`docs/qism-khanat/result-5.json`) بعينه،
  وإلّا `SILSILA_D32_NOT_REPRODUCED`.

`python tools/gen_silsila.py` يكتب `docs/silsila/result.json`، و`--check` يخرج
بـ`SILSILA_RESULT_DRIFTED` إن لم يكن المودَعُ ما يحسبه الآن (ويدخل CI بعد STEP-0007).
معفاةٌ في الحارس لأنّها أداةُ قياس.
"""

from __future__ import annotations

import gzip
import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import gate  # noqa: E402
from gate import Refusal  # noqa: E402
from gate.api import is_marker  # noqa: E402

PREREG = ROOT / "docs" / "silsila" / "PREREG.md"
RESULT = ROOT / "docs" / "silsila" / "result.json"
CORPUS = ROOT / "corpora" / "quran-simple-enhanced.txt"


def _load(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# ═══ المرآة: `A116.Silsila` ═══

Hal = tuple[str, Any]
"""("m", v) معيَّن، ("p", (v, …)) محتمَل، ("l", سبب) «لا حكم»؛
والسببُ "rafd:<اسم>" أو "dunaha" أو "laQari" أو "kharij"."""

Qari = Callable[[str, Hal], Hal] | None


def saqit(h: Hal) -> bool:
    return h[0] == "l"


def khutwa(w: str, dun: Hal, qari: Qari) -> Hal:
    if saqit(dun):
        return ("l", "dunaha")
    if qari is None:
        return ("l", "laQari")
    return qari(w, dun)


def ahkam(w: str, asl: Hal, qurra: Sequence[Qari]) -> list[Hal]:
    out: list[Hal] = []
    h = asl
    for q in qurra:
        h = khutwa(w, h, q)
        out.append(h)
    return out


def ramz(h: Hal) -> str:
    if h[0] == "m":
        return f"m:{h[1]}"
    if h[0] == "p":
        return "p:" + "|".join(h[1])
    return f"l:{h[1]}"


def rafd(name: str) -> Hal:
    return ("l", f"rafd:{name}")


# ═══ مرآةُ `A116.SilsilaQurra`: الجذرُ من الهيكل، والجنس، والحمل ═══

HAMZA_F, SUKUN = "ءَ", "ْ"
SHAMSI = frozenset("تثدذرزسشصضطظلن")


def tajrid(a: Sequence[str]) -> tuple[str, ...]:
    """`SilsilaQurra.tajrid`: الشمسيّةُ ابتداءً، وإلّا `QiraaMadlul.stripAl`."""
    a = tuple(a)
    if (len(a) >= 3 and a[0] == HAMZA_F and a[1][1:] == SUKUN and a[1][0] == a[2][0]
            and a[1][0] in SHAMSI):
        return a[2:]
    if len(a) >= 2:
        c, d = a[0], a[1]
        if c == HAMZA_F and d == "لْ":
            return a[2:]
        if c == "لْ":
            return a[1:]
        if c[1:] == SUKUN and c[0] == d[0]:
            return a[1:]
    return a


def haykal(a: Sequence[str]) -> str:
    """`QiraaMadlul.haykal`: الحواملُ حروفًا."""
    return "".join(x[0] for x in a)


def judhur_of(hy: dict[str, list[str]], a: Sequence[str]) -> list[str]:
    return list(hy.get(haykal(tajrid(a)), []))


def ajnas_of(aj: Sequence[tuple[str, str]], rs: Sequence[str]) -> list[tuple[str, str]]:
    return list(dict.fromkeys(p for p in aj if p[0] in rs))


def naw_of(manqul: dict[str, str], lafz: str) -> str:
    """`SilsilaQurra.nawOf` = `Haqaiq.haml` بلا قرينة: المنقولُ بنوعه، وإلّا لغويّة."""
    return manqul.get(lafz, "lughawiyya")


def haml_of(manqul: dict[str, str], wad: Sequence[tuple[str, str]], lafz: str, key: str,
            rs: Sequence[str]) -> list[tuple[str, str]]:
    return list(dict.fromkeys((r, naw_of(manqul, lafz)) for k, r in wad if k == key and r in rs))


# ═══ المرآة: `A116.SilsilaFuru` (ADR ١١٥) ═══

SABIQA1 = ("وَ", "فَ")
SABIQA2 = ("بِ", "لِ", "كَ", "لَ")
HAMZA_K = "ءِ"


def qishr(ps: Sequence[str], a: tuple[str, ...] | None) -> tuple[str, ...] | None:
    """`SilsilaFuru.qishr`: سابقةٌ من القائمة وما بقي خانتان فأكثر."""
    if a and a[0] in ps and len(a) - 1 >= 2:
        return a[1:]
    return None


def radd(a: tuple[str, ...]) -> tuple[str, ...]:
    """`SilsilaFuru.radd`: همزةُ الوصل مكسورةً قبل ساكنٍ غيرِ اللام."""
    if a and a[0][1:] == SUKUN and a[0][0] != "ل":
        return (HAMZA_K,) + a
    return a


def qashr(a: Sequence[str]) -> list[tuple[str, ...]]:
    """`SilsilaFuru.qashr`: الكلمةُ، ثمّ بلا «وَ/فَ»، ثمّ بلا «بِ/لِ/كَ/لَ»، ثمّ بلاهما؛ بلا تكرار."""
    a = tuple(a)
    p1, p2 = qishr(SABIQA1, a), qishr(SABIQA2, a)
    p12 = qishr(SABIQA2, p1)
    return list(dict.fromkeys([a] + [radd(x) for x in (p1, p2, p12) if x is not None]))


def awwal(hit: Callable[[tuple[str, ...]], bool], a: Sequence[str]) -> tuple[str, ...] | None:
    """`SilsilaFuru.awwal`: أوّلُ مرشَّحٍ يصيبه المعجم."""
    return next((v for v in qashr(a) if hit(v)), None)


def harf_key(a: Sequence[str]) -> str:
    """`SilsilaFuru.harfKey`: الحواملُ، والساكنُ قبل مثله ساقط."""
    a = tuple(a)
    return "".join(c[0] for i, c in enumerate(a)
                   if not (i + 1 < len(a) and c[1:] == SUKUN and a[i + 1][0] == c[0]))


Shahada = tuple[str, str]
"""(القائل، السطر)؛ والطريقُ نقلٌ والمودَعُ «وضع» في كلّ شهادةٍ هنا
(`HARF_SHAHADA_MAWDA_WAD_DECLARED`)."""


def jisr_wad(ws: Sequence[Shahada]) -> str:
    """`Naql.jisrWad (fun _ => false)` على شهاداتٍ كلُّها نقلٌ من «وضع»:
    مفهومٌ ظنّيٌّ برأسه وعدد ما بعده."""
    if not ws:
        return "maluma:0"
    return f"mafhum:zanni:{ws[0][0]}:{len(ws) - 1}"


def maani_harf(rows: Sequence[tuple[str, str, Sequence[Shahada]]], k: str) -> list[str]:
    """`SilsilaFuru.maaniHarf`: معاني صفوف الحرف بترتيبها، بلا تكرار."""
    return list(dict.fromkeys(m for h, m, _ws in rows if h == k))


def haml_harf(rows: Sequence[tuple[str, str, Sequence[Shahada]]], k: str) -> tuple[Hal, str, str]:
    """`SilsilaFuru.hamlHarf`: المنطوقُ الثلاثيّ ونوعُه (لغويٌّ أبدًا) وجسرُ الوضع على شهادات صفوفه
    بلا تكرار."""
    ms = maani_harf(rows, k)
    m: Hal = ("l", "laHukm") if not ms else ("m", ms[0]) if len(ms) == 1 else ("p", tuple(ms))
    ws = list(dict.fromkeys(w for h, _m, s in rows if h == k for w in s))
    return m, "lughawiyya", jisr_wad(ws)


def haml_wad(manqul: dict[str, str], sh: Sequence[tuple[tuple[str, str], Shahada]], lafz: str,
             keys: Sequence[str]) -> list[tuple[str, str, str]]:
    """`SilsilaFuru.hamlWad`: لكلّ جذرٍ شُهد له لأحد المفاتيح نوعُه وجسرُ الوضع على شهاداته؛
    لا يقرأ الجنس."""
    rs = list(dict.fromkeys(r for (k, r), _s in sh if k in keys))
    return [(r, naw_of(manqul, lafz), jisr_wad([s for (k, r2), s in sh if k in keys and r2 == r]))
            for r in rs]


HURUF = ROOT / "corpora" / "huruf" / "maani.tsv"


def huruf() -> list[tuple[str, str, list[Shahada]]]:
    """مودَعُ معاني الحروف (ج3 س468–507 بترقيم الغانم، و«الكتاب» JK006989 حيث وُجد):
    (المفتاح، المعنى، الشهادات)."""
    out: list[tuple[str, str, list[Shahada]]] = []
    for ln in HURUF.read_text(encoding="utf-8").splitlines()[1:]:
        _lafz, h, m, j3, ks, _kn = ln.split("\t")
        ws: list[Shahada] = [("nabhani", j3)] + ([("sibawayh", ks)] if ks != "0" else [])
        out.append((h, m, ws))
    return out


# ═══ المعاجمُ المودَعة (تُقرأ كما هي؛ لا تُحرَّر) ═══

SKELETONS = ROOT / "corpora" / "hadith" / "maqayis-skeletons.tsv"
MEMBERSHIP = ROOT / "corpora" / "mukhassas" / "membership.tsv"
NODES = ROOT / "corpora" / "mukhassas" / "nodes.tsv"
WAD = ROOT / "corpora" / "wad" / "wad.tsv"
SHUHUD = ROOT / "corpora" / "naql" / "shuhud.tsv.gz"
HAQAIQ = ROOT / "formal" / "a116" / "A116" / "Haqaiq.lean"
FOLD = {"أ": "ء", "إ": "ء", "ؤ": "ء", "ئ": "ء", "ى": "ي"}
MARKS = re.compile(r"[ً-ْٰـ]")
TANWIN = frozenset("ًٌٍ")


def fold(s: str) -> str:
    """طيُّ `gen_hadith_roots.fold` بعينه."""
    return "".join(FOLD.get(c, c) for c in s.replace("آ", "ءا"))


def sk_norm(sk: str) -> str:
    """هيكلُ المعجم بعرف الخانات: التاءُ المربوطة خانتُها تاء (`HAYKAL_CONVENTIONS_DIFFER`)."""
    return sk.replace("ة", "ت")


def lane_root(r: str) -> str:
    """ألفُ لين في الجذر همزةٌ (`gen_wad.lane_root_as_ibn_faris` بعينه)."""
    return fold(r.replace("ا", "ء"))


def in_order(sk: str, root: str) -> bool:
    """`gen_hadith_roots.in_order` بعينه: أصولُ الجذر في الهيكل بترتيبها."""
    i = 0
    for c in root:
        k = sk.find(c, i)
        if k < 0:
            return False
        i = k + 1
    return True


def lexicon_forms(sk: str, root: str) -> list[str]:
    """صورُ هيكل المعجم مفاتيحَ (`RULE_LEX`).

    هو، وبلا واو العطف أو فائه أوّلًا، ثمّ بلا «ال» أوّلًا — كلُّ حذفٍ بشرط بقاء أصول الجذر فيه بترتيبها
    (شرطُ `RULE_ATF` في `gen_naql`)، كما تُجرَّد الكلمةُ من أداتها (`tajrid`)."""
    forms = [sk]
    if sk[:1] in ("و", "ف") and in_order(sk[1:], root):
        forms.append(sk[1:])
    for f in list(forms):
        if f.startswith("ال") and in_order(f[2:], root):
            forms.append(f[2:])
    return [sk_norm(f) for f in forms]


def _add(out: dict[str, list[str]], sk: str, r: str) -> None:
    for f in lexicon_forms(sk, r):
        cur = out.setdefault(f, [])
        if r not in cur:
            cur.append(r)


def hayakil() -> dict[str, list[str]]:
    """هياكلُ ابن فارس (`maqayis-skeletons.tsv`)، ثمّ هياكلُ «لسان العرب» (`shuhud.tsv.gz`، المعجم m).

    واللسانُ بأمر المالك (2026-10-19 01:24)؛ كلاهما بـ`RULE_B`، ومفاتيحُهما بـ`RULE_LEX`."""
    out: dict[str, list[str]] = {}
    for ln in SKELETONS.read_text(encoding="utf-8").splitlines():
        sk, roots = ln.split("\t")
        for r in roots.split(" "):
            _add(out, sk, r)
    for r, sk in lisan_hayakil():
        _add(out, sk, r)
    return out


def lisan_hayakil() -> list[tuple[str, str]]:
    """(جذر، هيكل) وضعه «لسان العرب» تحت الجذر (`shuhud.tsv.gz`: المعجمُ m بين معاجمه)."""
    out: list[tuple[str, str]] = []
    for ln in gzip.decompress(SHUHUD.read_bytes()).decode("utf-8").splitlines():
        r, sk, mu, _q, _p = ln.split("\t")
        if "m" in mu:
            out.append((r, sk))
    return out


def ajnas() -> list[tuple[str, str]]:
    """(جذر، كتاب) من عضويّة «المخصَّص» (`RULE_M`) وكتب العُقَد؛ والعقدةُ بلا كتاب («-») لا جنسَ لها."""
    book: dict[str, str] = {}
    for ln in NODES.read_text(encoding="utf-8").splitlines()[1:]:
        nid, _line, _mark, b, _title = ln.split("\t")
        book[nid] = b
    out: list[tuple[str, str]] = []
    for ln in MEMBERSHIP.read_text(encoding="utf-8").splitlines():
        r, nodes = ln.split("\t")
        out.extend((r, book[n]) for n in nodes.split(" ") if book[n] != "-")
    return list(dict.fromkeys(out))


def wad() -> tuple[list[tuple[str, str]], dict[tuple[str, str], set[str]]]:
    """أزواجُ الوضع (مفتاحُ لين، جذرٌ بعرف ابن فارس) ورواتُها."""
    pairs: list[tuple[str, str]] = []
    rawat: dict[tuple[str, str], set[str]] = {}
    for ln in WAD.read_text(encoding="utf-8").splitlines():
        k, r, ws = ln.split("\t")
        p = (k, lane_root(r))
        pairs.append(p)
        rawat.setdefault(p, set()).update(ws.split(","))
    return list(dict.fromkeys(pairs)), rawat


def lisan() -> dict[tuple[str, str], set[str]]:
    """(جذر، هيكل) ← قائلوه في «لسان العرب» (`shuhud.tsv.gz`، المعجم m)."""
    out: dict[tuple[str, str], set[str]] = {}
    for ln in gzip.decompress(SHUHUD.read_bytes()).decode("utf-8").splitlines():
        r, sk, _mu, _q, pairs = ln.split("\t")
        for pq in pairs.split(","):
            mj, qa = pq.split(":")
            if mj == "m":
                out.setdefault((r, sk_norm(sk)), set()).add(qa)
    return out


NAW_LEAN = {".shariyya": "shariyya", ".urfiyya .amma": "urfiyya_amma",
            ".urfiyya .khassa": "urfiyya_khassa"}


def manqul() -> dict[str, str]:
    """صفوفُ `Haqaiq.naql` من نصّ Lean بعينه."""
    text = HAQAIQ.read_text(encoding="utf-8")
    body = text[text.index("def naql : List Manqul :="):text.index("theorem huruf_la_tunqal")]
    rows = re.findall(r'⟨"([^"]+)", (\.[a-z .]+), (?:true|false), \d+⟩', body)
    return {lafz: NAW_LEAN[naw] for lafz, naw in rows}


def wad_key(a: Sequence[str], word: str) -> str:
    """مفتاحُ لين (`gen_lane_roots.key`): بلا نون التنوين وبلا حركة الخانة الأخيرة."""
    a = tuple(a)
    if word and word[-1] in TANWIN and a and a[-1] == "نْ":
        a = a[:-1]
    if not a:
        return ""
    return " ".join(a[:-1] + (a[-1][0],))


# ═══ الطبقة ٢: قارئُ D3₂ من أسماء علاماته المودَعة ═══

QISM_NAME = {0: "اسم", 1: "فعل", 2: "حرف"}


def d32_signs(QK: Any, pre_n: Callable[[str], int | None]) -> dict[str, Any]:
    """علاماتُ D3₂ بأسمائها في نتائج التسجيلات (لا اختيارَ هنا).

    K، وISM_WAZN، وD1 بعدد الشهادة، و«ما بعد لمّا»؛ وعلاماتُ العوامل بالخانات ساقطةٌ كما في D3₂."""
    r1 = json.loads(QK.RESULT.read_text(encoding="utf-8"))
    r2 = json.loads(QK.RESULT2.read_text(encoding="utf-8"))
    r5 = json.loads(QK.RESULT5.read_text(encoding="utf-8"))
    mrows, _ = QK.mashkul_rows(QK.MASHKUL2)
    s2 = QK.signs2()
    sg: dict[str, Any] = {n: ((lambda r, n=n: QK.SIGNS[n][0](r[1], r[2])), QK.SIGNS[n][1])
                          for n in r1["kept"]}
    sg.update({n: s2[n] for n in r2["kept_new"] if not n.startswith("AMIL_")})
    for name in r5["kept_D1"]:
        kind, rest = name.split("_N_", 1)
        at, q = rest.rsplit("_", 1)
        qi = int(q)
        if kind == "AMIL_OWN":
            sg[name] = (lambda r, at=at, qi=qi: QK.amil_own_n(at, r[3], pre_n(r[7]), mrows) == qi,
                        frozenset({qi}))
        else:
            sg[name] = (lambda r, at=at, qi=qi: QK.amil_next_n(at, r[6], mrows) == qi,
                        frozenset({qi}))
    lamma = next(ns for nm, at, ns in mrows if nm == "لما" and at == "JAZM_FIL")
    lsigns = {"LAMMA_MADI_ISM": (lambda r: (r[3] in lamma or pre_n(r[7]) in lamma) and r[9],
                                 frozenset({QK.ISM}))}
    sg.update({n: lsigns[n] for n in r5["kept_lamma"]})
    return sg


def qism_cands(sg: dict[str, Any], r: Any) -> tuple[int, ...]:
    fired = [keep for fn, keep in sg.values() if fn(r)]
    return tuple(q for q in (0, 1, 2) if all(q in keep for keep in fired))


def reproduce_b(QK: Any) -> dict[str, int]:
    """D3₂ على B كما في `result-5.json`: المعيَّنُ والصائبُ والخطأ."""
    rows = QK.population(rec=True, full=True, nxt=True)[0]
    b = [r for r in rows if r[0] % 2 == 0]
    cache: dict[str, int | None] = {}

    def pre_n(t: str) -> int | None:
        if t not in cache:
            cache[t] = QK.strip_prefix(t)
        return cache[t]

    sg = d32_signs(QK, pre_n)
    mu = sa = 0
    for r in b:
        c = qism_cands(sg, r)
        if len(c) == 1:
            mu += 1
            sa += c[0] == r[4]
    return {"signs": len(sg), "muayyan": mu, "sahih": sa, "wrong": mu - sa}


# ═══ السلسلةُ على المصحف ═══

PAST_KINDS = ("PAST", "PASSIVE")
PREREG2 = ROOT / "docs" / "silsila" / "PREREG-2.md"
RESULT2 = ROOT / "docs" / "silsila" / "result-2.json"
QAC_ROOTS = ROOT / "corpora" / "qac" / "qac-roots.tsv"
HARF = QISM_NAME[2]


def qac_gold() -> dict[tuple[int, int], str]:
    """(سطر، موضع) ← جذرُ QAC (`corpora/qac/qac-roots.tsv`: الموضعُ رقمُ الرمز في السطر من 1)."""
    out: dict[tuple[int, int], str] = {}
    for ln in QAC_ROOTS.read_text(encoding="utf-8").splitlines()[1:]:
        f = ln.split("\t")
        out[(int(f[0]), int(f[1]))] = f[4]
    return out


def norm_root(r: str) -> str:
    """الجذرُ للمقارنة: ألفُ لين همزةٌ، والطيُّ، ولامُ الناقص بلا تمييزٍ بين واوٍ وياء (`gen_qac.wy`)."""
    r = lane_root(r)
    return r[:-1] + "ي" if r.endswith("و") else r


def judge_root(h: Hal, gold: str) -> str:
    """حكمُ طبقة جذرٍ على الذهبيّ: صائب/خاطئ للمعيَّن، فيه/خارجه للمحتمَل، و«لا حكم»، و«حرف» لمعنى حرف."""
    if h[0] == "l":
        return "la_hukm"
    vs = (h[1],) if h[0] == "m" else h[1]
    if any(v.startswith("ح:") for v in vs):
        return "harf"
    rs = {norm_root(v.split(":", 1)[0]) for v in vs}
    g = norm_root(gold)
    if h[0] == "m":
        return "sahih" if g in rs else "khata"
    return "muhtamal_fih" if g in rs else "muhtamal_kharij"


def compute(lines_limit: int | None = None, version: int = 1) -> dict[str, Any]:
    """`lines_limit` لفحص الوصل على السطور الأولى وحدَها (`--smoke N`)؛ القياسُ بلا حدّ.

    `version=1` هو تسجيلُ ADR ١١٤ بعينه (`PREREG.md` ← `result.json`)؛ و`version=2` هو ADR ١١٥
    (`PREREG-2.md` ← `result-2.json`): فرعُ الوضع [الشهادة، القسم، الحمل] مستقلٌّ عن فرع الجنس
    [الشهادة، القسم، الصيغة، الجنس]، وحملُ الحرف من مودَعه، ومرشَّحو التقشير للاسم، والقياسُ على QAC."""
    QK = _load("gen_qism_khanat", ROOT / "tools" / "gen_qism_khanat.py")
    rep = reproduce_b(QK)
    r5 = json.loads(QK.RESULT5.read_text(encoding="utf-8"))
    want = {k: r5["D3"][k] for k in ("signs", "muayyan", "sahih", "wrong")}
    if rep != want:
        raise SystemExit(f"SILSILA_D32_NOT_REPRODUCED {rep} != {want}")
    cache: dict[str, int | None] = {}

    def pre_n(t: str) -> int | None:
        if t not in cache:
            cache[t] = QK.strip_prefix(t)
        return cache[t]

    sg = d32_signs(QK, pre_n)
    recs: dict[str, tuple[str, tuple[Any, ...]]] = {}

    def rec(t: str, c: Any) -> tuple[str, tuple[Any, ...]]:
        if t not in recs:
            recs[t] = gate.recover(c, peel=True)
        return recs[t]

    hy, aj, (wd, rawat), ls, mq = hayakil(), ajnas(), wad(), lisan(), manqul()
    aj_set, wd_set = set(aj), set(wd)
    wd_roots: dict[str, list[str]] = {}
    for k, r in wd:
        wd_roots.setdefault(k, []).append(r)
    hr = huruf() if version == 2 else []
    hr_keys = {h for h, _m, _ws in hr}
    gold = qac_gold() if version == 2 else {}
    nrawi: Counter[int] = Counter()
    wiring_viol = 0
    lines = CORPUS.read_text(encoding="utf-8").splitlines()
    keys = sorted(QK.Q.qac_words(QK.Q.source()))
    if len(keys) != len(lines):
        raise SystemExit("SILSILA_VERSE_COUNT")
    surah = [k[0] for k in keys]
    qism_b: Counter[str] = Counter()
    layers = ("shahada", "qism", "sigha", "jins", "haml")
    kinds: dict[str, Counter[str]] = {k: Counter() for k in layers}
    asbab: dict[str, Counter[str]] = {k: Counter() for k in layers}
    qac: dict[str, Counter[str]] = {"A_haml": Counter(), "B_sigha": Counter()}
    qac_peeled: dict[str, Counter[str]] = {"A_haml": Counter(), "B_sigha": Counter()}
    peeled: Counter[str] = Counter()
    stream = hashlib.sha256()
    n_words = n_verdicts = funnel_viol = above_fall = shared_viol = 0

    def shuhud_wad(k: str, r: str, w: str) -> list[Shahada]:
        """شهاداتُ (مفتاح، جذر): لين ثمّ ابنُ فارس من `wad.tsv`، ثمّ ابنُ منظور مؤكِّدًا من «لسان العرب»."""
        ws: list[Shahada] = [(q, "0") for q in ("lane", "ibn-faris") if q in rawat[(k, r)]]
        sk = fold(haykal(k.split(" ")))
        ws += [(q, "0") for q in sorted(ls.get((r, sk), set()))]
        return ws

    for li, line in enumerate(lines[:lines_limit]):
        toks = line.split(" ")
        idx = [i for i, t in enumerate(toks) if not is_marker(t)]
        raw = [toks[i] for i in idx]
        certs = [gate.enter(t.encode("utf-8")) for t in raw]
        ok = [None if isinstance(c, Refusal) else c for c in certs]
        for j, t in enumerate(raw):
            c = certs[j]
            prev = ok[j - 1] if j > 0 else None
            nxt = ok[j + 1] if j + 1 < len(raw) else None
            row: Any = None
            flag = {"A_haml": False, "B_sigha": False}
            if not isinstance(c, Refusal):
                past = nxt is not None and any(
                    k in PAST_KINDS for _r, k, _f, _p in gate.recover(nxt)[1])
                row = (0, tuple(c.atoms), tuple(prev.atoms) if prev is not None else None,
                       int(c.integer), -1, None, int(prev.integer) if prev is not None else None,
                       t, tuple(nxt.atoms) if nxt is not None else None, past)

            def q_shahada(w: str, _d: Hal, c: Any = c) -> Hal:
                if isinstance(c, Refusal):
                    return rafd("+".join(c.reasons) if c.reasons else c.status)
                return ("m", str(int(c.integer)))

            def q_qism(w: str, _d: Hal, row: Any = row) -> Hal:
                cs = qism_cands(sg, row)
                if not cs:
                    return rafd("QISM_TANAQUD")
                names = tuple(QISM_NAME[q] for q in cs)
                return ("m", names[0]) if len(names) == 1 else ("p", names)

            def ism_roots(a: Sequence[str]) -> list[str]:
                if version == 1:
                    return judhur_of(hy, a)
                v = awwal(lambda x: bool(judhur_of(hy, x)), a)
                if v is not None and v != tuple(a):
                    peeled["B_ism"] += 1
                    flag["B_sigha"] = True
                return judhur_of(hy, v) if v is not None else []

            def q_sigha(w: str, d: Hal, c: Any = c) -> Hal:
                allowed = (d[1],) if d[0] == "m" else d[1]
                if QISM_NAME[1] not in allowed and QISM_NAME[0] not in allowed:
                    return ("l", "kharij")
                rk: set[str] = set()
                if QISM_NAME[1] in allowed:
                    rk |= {f"{fold(r)}:{k}" for r, k, _f, _p in rec(w, c)[1]}
                if QISM_NAME[0] in allowed:
                    rk |= {f"{r}:ISM" for r in ism_roots(c.atoms)}
                if not rk:
                    return rafd("LA_JIDHR")
                v = sorted(rk)
                return ("m", v[0]) if len(v) == 1 else ("p", tuple(v))

            def roots_of(d: Hal) -> list[str]:
                vs = (d[1],) if d[0] == "m" else d[1]
                return list(dict.fromkeys(v.split(":", 1)[0] for v in vs))

            def q_jins(w: str, d: Hal) -> Hal:
                ps = ajnas_of(aj, roots_of(d))
                if not ps:
                    return rafd("LA_JINS_FI_ALMUKHASSAS")
                v = [f"{r}:{b}" for r, b in ps]
                return ("m", v[0]) if len(v) == 1 else ("p", tuple(v))

            def q_haml(w: str, d: Hal, c: Any = c) -> Hal:
                key = wad_key(tajrid(c.atoms), w)
                ps = haml_of(mq, wd, MARKS.sub("", w), key, roots_of(d))
                if not ps:
                    return rafd("LA_WAD" if not any(k == key for k, _r in wd) else
                                "WAD_KHARIJ_AL_JUDHUR")
                v = [f"{r}:{n}" for r, n in ps]
                return ("m", v[0]) if len(v) == 1 else ("p", tuple(v))

            def q_haml2(w: str, d: Hal, c: Any = c) -> Hal:
                """فرعُ الوضع: على القسم وحدَه، لا على الجنس
                (تصحيحُ المالك 02:01، `WAD_GATED_BY_JINS`)."""
                allowed = (d[1],) if d[0] == "m" else d[1]
                if d == ("m", HARF):
                    v = awwal(lambda x: harf_key(x) in hr_keys, c.atoms)
                    if v is None:
                        return rafd("LA_MAANA_HARF")
                    peeled["A_harf"] += v != tuple(c.atoms)
                    k = harf_key(v)
                    m, naw, rk = haml_harf(hr, k)
                    ms = (m[1],) if m[0] == "m" else m[1]
                    vals = tuple(f"ح:{k}:{x}:{naw}:{rk}" for x in ms)
                    return ("m", vals[0]) if m[0] == "m" else ("p", vals)
                if QISM_NAME[0] not in allowed and QISM_NAME[1] not in allowed:
                    return ("l", "kharij")
                v = awwal(lambda x: wad_key(tajrid(x), w) in wd_roots, c.atoms)
                if v is None:
                    return rafd("LA_WAD")
                peeled["A_wad"] += v != tuple(c.atoms)
                flag["A_haml"] = v != tuple(c.atoms)
                k = wad_key(tajrid(v), w)
                lafz = MARKS.sub("", w)
                vals = tuple(f"{r}:{naw_of(mq, lafz)}:{jisr_wad(shuhud_wad(k, r, w))}"
                             for r in dict.fromkeys(wd_roots[k]))
                return ("m", vals[0]) if len(vals) == 1 else ("p", vals)

            start: Hal = ("m", t)
            if version == 1:
                hs = ahkam(t, start, [q_shahada, q_qism, q_sigha, q_jins, q_haml])
                branches = [hs]
            else:
                ha = ahkam(t, start, [q_shahada, q_qism, q_haml2])
                hb = ahkam(t, start, [q_shahada, q_qism, q_sigha, q_jins])
                shared_viol += ha[:2] != hb[:2]
                hs = [hb[0], hb[1], hb[2], hb[3], ha[2]]
                branches = [ha, hb]
            if hs[3][0] != "l":
                low = set(roots_of(hs[2]))
                for v in ((hs[3][1],) if hs[3][0] == "m" else hs[3][1]):
                    r, b = v.split(":", 1)
                    wiring_viol += (r, b) not in aj_set or r not in low
            if hs[4][0] != "l" and not isinstance(c, Refusal):
                vals = (hs[4][1],) if hs[4][0] == "m" else hs[4][1]
                if version == 1:
                    key = wad_key(tajrid(c.atoms), t)
                    low = set(roots_of(hs[3]))
                    sk = fold(haykal(key.split(" ")))
                    for v in vals:
                        r, n = v.split(":", 1)
                        wiring_viol += (key, r) not in wd_set or r not in low
                        wiring_viol += n != "lughawiyya" and mq.get(MARKS.sub("", t)) != n
                        if hs[4][0] == "m":
                            nrawi[len(rawat[(key, r)] | ls.get((r, sk), set()))] += 1
                else:
                    for v in vals:
                        f = v.split(":")
                        if f[0] == "ح":
                            wiring_viol += (f[1] not in hr_keys or f[3] != "lughawiyya"
                                            or f[4] != "mafhum")
                            wiring_viol += f[2] not in maani_harf(hr, f[1])
                        else:
                            wiring_viol += f[2] != "mafhum" or f[3] != "zanni"
                            wiring_viol += f[1] != "lughawiyya" and mq.get(MARKS.sub("", t)) != f[1]
                            wiring_viol += not any((k, f[0]) in wd_set for k in
                                                   (wad_key(tajrid(x), t) for x in qashr(c.atoms)))
                            if hs[4][0] == "m":
                                nrawi[1 + int(f[5])] += 1
            if version == 2 and surah[li] % 2 == 0 and (li + 1, idx[j] + 1) in gold:
                g = gold[(li + 1, idx[j] + 1)]
                for bname, h in (("A_haml", hs[4]), ("B_sigha", hs[2])):
                    qac[bname][judge_root(h, g)] += 1
                    if flag[bname]:
                        qac_peeled[bname][judge_root(h, g)] += 1
            n_words += 1
            n_verdicts += len(hs)
            if surah[li] % 2 == 0:
                qism_b[hs[1][0]] += 1
            for k, h in zip(layers, hs, strict=True):
                kinds[k][h[0]] += 1
                if h[0] == "l":
                    asbab[k][h[1]] += 1
            for br in branches:
                seen_fall = False
                for i, h in enumerate(br):
                    if seen_fall and not saqit(h):
                        above_fall += 1
                    if saqit(h):
                        seen_fall = True
                    if i > 0 and not saqit(h) and saqit(br[i - 1]):
                        funnel_viol += 1
            stream.update(f"{li}\t{j}\t{t}\t".encode() + "\t".join(map(ramz, hs)).encode() + b"\n")
            if lines_limit is not None:
                sys.stdout.write(f"{t}\t" + "\t".join(map(ramz, hs)) + "\n")
    per = {k: {"muayyan": kinds[k]["m"], "muhtamal": kinds[k]["p"], "la_hukm": kinds[k]["l"],
               "asbab": dict(sorted(asbab[k].items()))} for k in layers}
    share = {k: round(kinds[k]["m"] / n_words, 6) for k in layers}
    res: dict[str, Any] = {
        "prereg_sha256": hashlib.sha256(
            (PREREG if version == 1 else PREREG2).read_bytes()).hexdigest(),
        "corpus_lines": len(lines), "n_words": n_words,
        "d32_on_B_reproduced": rep,
        "layers": per, "muayyan_share": share,
        "verdict_stream_sha256": stream.hexdigest(),
        "n_verdicts": n_verdicts, "above_fall": above_fall, "funnel_violations": funnel_viol,
        "H1": n_verdicts == len(layers) * n_words
        and all(sum(kinds[k].values()) == n_words for k in layers),
        "H2": above_fall == 0 and funnel_viol == 0,
        "qism_even_surahs": {"n": sum(qism_b.values()), "muayyan": qism_b["m"],
                             "muayyan_share": round(qism_b["m"] / max(1, sum(qism_b.values())), 6)},
        "H3": qism_b["m"] * 100 >= 20 * sum(qism_b.values()),
        "haml_muayyan_by_narrator_count": {str(k): v for k, v in sorted(nrawi.items())},
        "wiring_violations": wiring_viol,
        "H4": wiring_viol == 0,
    }
    if version == 2:
        before = json.loads(RESULT.read_text(encoding="utf-8"))
        res["shared_prefix_violations"] = shared_viol
        res["H8"] = shared_viol == 0
        res["peeled"] = dict(sorted(peeled.items()))
        res["before_after"] = {k: {"qabl": before["layers"][k]["muayyan"], "bad": kinds[k]["m"]}
                               for k in layers}
        res["H5"] = kinds["haml"]["m"] >= before["layers"]["haml"]["muayyan"]
        res["qac_even_surahs"] = {}
        for bname, cnt in qac.items():
            mu = cnt["sahih"] + cnt["khata"]
            n = sum(cnt.values())
            res["qac_even_surahs"][bname] = {
                "n": n, **dict(sorted(cnt.items())),
                "muayyan_share": round(mu / max(1, n), 6),
                "precision": round(cnt["sahih"] / max(1, mu), 6),
                "inclusion": round((cnt["sahih"] + cnt["muhtamal_fih"]) / max(1, n), 6)}
        res["qac_even_surahs_peeled"] = {b: dict(sorted(c.items())) for b, c in qac_peeled.items()}
        res["H6"] = res["qac_even_surahs"]["A_haml"]["precision"] >= 0.95
        res["H7"] = res["qac_even_surahs"]["B_sigha"]["precision"] >= 0.90
    return res


def render(res: dict[str, Any]) -> str:
    return json.dumps(res, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def main(argv: list[str]) -> int:
    v = 2 if "--v2" in argv else 1
    if "--smoke" in argv:
        compute(int(argv[argv.index("--smoke") + 1]), version=v)
        return 0
    if "--check" in argv:
        targets = [(1, RESULT)] + ([(2, RESULT2)] if RESULT2.exists() else [])
        for ver, path in targets:
            if path.read_text(encoding="utf-8") != render(compute(version=ver)):
                sys.stderr.write(f"SILSILA_RESULT_DRIFTED {path.name}\n")
                return 1
        sys.stdout.write("السلسلةُ على المصحف مطابقة\n")
        return 0
    out = render(compute(version=v))
    (RESULT if v == 1 else RESULT2).write_text(out, encoding="utf-8")
    sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
