"""تشكيلُ النصّ غير المشكول بمرشَّحي الوضع، بلا تخمين (ADR ١٠٣، أمرُ المالك 2026-10-17).

قال المالك: «تشكيل النصّ غير المشكول: خارج النطاق حتى الآن، قرارك. اعمل lean نفذ».

**المعجم** `corpora/tashkil/mujam.tsv.gz`: هيكلٌ ← صورُه المشكولة كما وردت في المدوّنتين المختومتين.
* المدوّنتان: المصحف (`corpora/quran-simple-enhanced.txt`) والصحيحان
  (`corpora/hadith/sahihain-lines.txt.gz`).
* `RULE_TOKEN`: اللفظُ تتابعُ حروفٍ عربيّة (ء–ي) وعلاماتٍ ثمانٍ (الفتحةُ والضمّةُ والكسرة وتنويناتها
  والسكونُ والشدّة). وما ليس فيه علامةٌ لا يُعدّ شهادةَ تشكيل.
* `RULE_FORM`: الصورةُ اللفظُ بتطبيع NFC (فالشدّةُ بعد الحركة) وبلا تطويل.
* `RULE_HAYKAL`: الهيكلُ الصورةُ بلا علاماتها الثمان. الكراسيُّ تبقى حروفًا كما كُتبت.
* `RULE_TAMAM`: صورةٌ علاماتُها على كلّ حرفٍ بعضُ علامات صورةٍ أخرى من هيكلها تُطوى فيها. فالمعجمُ الصورُ
  التامّة وحدَها («قالَ» و«قَال» تُطويان في «قَالَ»).

**الحكم** على هيكلٍ غير مشكول:
* صورةٌ واحدةٌ في المعجم: معيَّن.
* أكثرُ من صورة: محتمَلٌ بقائمته، لا يُختار منها شيء.
* لا صورة: «لا حكم».

**القياس** (`measure`، بالتسجيل المسبق `docs/tashkil/PREREG.md`) على المرجع المحجوب
`corpora/tashkeela-fadel-test.txt`: تشكيلٌ بشريّ (Fadel et al. 2019، MIT)، لم يدخل المعجم.

`--check` يُسقط البناءَ بأسمائها: `MUSHAF_SEAL_BROKEN`، `HADITH_LINES_SEAL_BROKEN`،
`FADEL_SEAL_BROKEN`، `TASHKIL_MUJAM_DRIFTED`، `TASHKIL_LEAN_DRIFTED`، `TASHKIL_RESULT_DRIFTED`.
معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import math
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MUSHAF = ROOT / "corpora" / "quran-simple-enhanced.txt"
MUSHAF_SHA256 = "37633090743d403886b334d12dd911d1994e49767faa9f2be0f01fd48b466c5a"
HADITH = ROOT / "corpora" / "hadith" / "sahihain-lines.txt.gz"
HADITH_SHA256 = "14b1a4b7a6d67449b23f016f351d12da9a934ce76116e3c283042705c6d71e3b"
FADEL = ROOT / "corpora" / "tashkeela-fadel-test.txt"
FADEL_SHA256 = "4e851ff836f0a178abb15d9f4a8bcf92748b77cc0d67030d9fae2fbe698baa12"
OUT = ROOT / "corpora" / "tashkil"
MUJAM = OUT / "mujam.tsv.gz"
RESULT = ROOT / "docs" / "tashkil" / "result.json"
PREREG = ROOT / "docs" / "tashkil" / "PREREG.md"
LEAN = ROOT / "formal" / "a116" / "A116" / "TashkilData.lean"

MARKS = "ًٌٍَُِّْ"
TOKEN = re.compile(r"[ء-يً-ْـ]+")
WITNESS = ("كتب", "قال", "علم", "الكتاب", "والله")


def _sealed_text(path: Path, sha: str, name: str, gz: bool = False) -> str:
    raw = path.read_bytes()
    data = gzip.decompress(raw) if gz else raw
    if hashlib.sha256(data).hexdigest() != sha:
        raise SystemExit(name)
    return data.decode("utf-8")


def form(tok: str) -> str:
    """`RULE_FORM`."""

    return unicodedata.normalize("NFC", tok.replace("ـ", ""))


def haykal(f: str) -> str:
    """`RULE_HAYKAL`."""

    return "".join(c for c in f if c not in MARKS)


def harakat(f: str) -> list[frozenset[str]]:
    """علاماتُ كلّ حرفٍ من الهيكل بترتيبه."""

    out: list[set[str]] = []
    for c in f:
        if c in MARKS:
            out[-1].add(c)
        else:
            out.append(set())
    return [frozenset(x) for x in out]


def mutadammin(small: str, big: str) -> bool:
    """علاماتُ `small` على كلّ حرفٍ بعضُ علامات `big` (والهيكلُ واحد)."""

    return all(a <= b for a, b in zip(harakat(small), harakat(big), strict=True))


def vocalized(f: str) -> bool:
    return any(c in MARKS for c in f)


def core(f: str) -> str:
    """الصورةُ بلا علامات الحرف الأخير: البنيةُ دون الإعراب."""

    i = len(f)
    while i > 0 and f[i - 1] in MARKS:
        i -= 1
    return f[:i]


def tokens(text: str) -> list[str]:
    return [form(t) for t in TOKEN.findall(text)]


def sources() -> list[str]:
    mushaf = _sealed_text(MUSHAF, MUSHAF_SHA256, "MUSHAF_SEAL_BROKEN")
    hadith = _sealed_text(HADITH, HADITH_SHA256, "HADITH_LINES_SEAL_BROKEN", gz=True)
    hadith = re.sub(r"<[^>]*>", " ", hadith)
    return [mushaf, hadith]


def mujam() -> dict[str, list[str]]:
    out: dict[str, set[str]] = {}
    for text in sources():
        for f in tokens(text):
            if vocalized(f):
                out.setdefault(haykal(f), set()).add(f)
    return {k: sorted(f for f in v if not any(g != f and mutadammin(f, g) for g in v))
            for k, v in sorted(out.items())}


def render_mujam(mj: dict[str, list[str]]) -> str:
    return "".join(f"{k}\t{' '.join(v)}\n" for k, v in mj.items())


def gz(text: str) -> bytes:
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", compresslevel=9, mtime=0) as f:
        f.write(text.encode("utf-8"))
    return buf.getvalue()


def wilson(k: int, n: int) -> list[float]:
    if n == 0:
        return [0.0, 0.0]
    z = 1.959963984540054
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [round((c - h) / d, 6), round((c + h) / d, 6)]


def measure(mj: dict[str, list[str]]) -> dict[str, object]:
    """المقاييسُ المعلنة في `docs/tashkil/PREREG.md` §٥، بأسمائها."""

    text = _sealed_text(FADEL, FADEL_SHA256, "FADEL_SEAL_BROKEN")
    gold = [f for f in tokens(text) if vocalized(f)]
    n = len(gold)
    cnt = {"muayyan": 0, "muhtamal": 0, "laHukm": 0, "exact": 0, "in_set": 0,
           "core_muayyan": 0, "core_exact": 0, "consistent": 0}
    for g in gold:
        cands = mj.get(haykal(g), [])
        if len(cands) == 1:
            cnt["muayyan"] += 1
            cnt["exact"] += cands[0] == g
            cnt["consistent"] += mutadammin(g, cands[0])
        elif cands:
            cnt["muhtamal"] += 1
            cnt["in_set"] += g in cands
        else:
            cnt["laHukm"] += 1
        cores = sorted({core(c) for c in cands})
        if len(cores) == 1:
            cnt["core_muayyan"] += 1
            cnt["core_exact"] += cores[0] == core(g)

    def rate(k: str, d: str | None) -> dict[str, object]:
        den = n if d is None else cnt[d]
        return {"k": cnt[k], "n": den, "rate": round(cnt[k] / den, 6) if den else 0.0,
                "wilson95": wilson(cnt[k], den)}

    return {
        "prereg_sha256": hashlib.sha256(PREREG.read_bytes()).hexdigest(),
        "n_gold_tokens": n,
        "mujam_haykal": len(mj),
        "muayyan_rate": rate("muayyan", None),
        "muhtamal_rate": rate("muhtamal", None),
        "laHukm_rate": rate("laHukm", None),
        "exact_given_muayyan": rate("exact", "muayyan"),
        "consistent_given_muayyan": rate("consistent", "muayyan"),
        "in_set_given_muhtamal": rate("in_set", "muhtamal"),
        "core_muayyan_rate": rate("core_muayyan", None),
        "core_exact_given_core_muayyan": rate("core_exact", "core_muayyan"),
    }


def _s(x: str) -> str:
    return '"' + x.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_lean(mj: dict[str, list[str]], res: dict[str, object] | None) -> str:
    out = ["-- مولَّدٌ بـ`tools/gen_tashkil.py`؛ لا يُحرَّر باليد (ADR ١٠٣).", "",
           "namespace A116.TashkilData", "",
           "/-- عددُ الهياكل في المعجم، وعددُ ما له صورةٌ واحدة. -/",
           f"def haykalCount : Nat := {len(mj)}",
           f"def wahidCount : Nat := {sum(1 for v in mj.values() if len(v) == 1)}", "",
           "/-- صفوفُ الشواهد: (الهيكل، صورُه). -/",
           "def shawahid : List (String × List String) := ["]
    out.append(",\n".join(f"  ({_s(k)}, [{', '.join(_s(f) for f in mj[k])}])"
                          for k in WITNESS if k in mj))
    out += ["]", ""]
    if res is not None:
        def kn(key: str) -> str:
            r = res[key]
            assert isinstance(r, dict)
            return f"({r['k']}, {r['n']})"
        out += ["/-- القياسُ المسجَّل (`docs/tashkil/result.json`): (البسط، المقام). -/",
                f"def muayyan : Nat × Nat := {kn('muayyan_rate')}",
                f"def muhtamal : Nat × Nat := {kn('muhtamal_rate')}",
                f"def laHukm : Nat × Nat := {kn('laHukm_rate')}",
                f"def exact : Nat × Nat := {kn('exact_given_muayyan')}",
                f"def inSet : Nat × Nat := {kn('in_set_given_muhtamal')}",
                f"def coreMuayyan : Nat × Nat := {kn('core_muayyan_rate')}",
                f"def coreExact : Nat × Nat := {kn('core_exact_given_core_muayyan')}", ""]
    out += ["end A116.TashkilData", ""]
    return "\n".join(out)


def main(argv: list[str]) -> int:
    mj = mujam()
    m_tsv = render_mujam(mj)
    if "measure" in argv:
        res = measure(mj)
        RESULT.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        LEAN.write_text(render_lean(mj, res), encoding="utf-8")
        sys.stdout.write(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
        return 0
    res = json.loads(RESULT.read_text(encoding="utf-8")) if RESULT.exists() else None
    lean = render_lean(mj, res)
    if "--check" in argv:
        bad = 0
        if not MUJAM.exists() or gzip.decompress(MUJAM.read_bytes()).decode("utf-8") != m_tsv:
            sys.stderr.write("TASHKIL_MUJAM_DRIFTED: شغّل python tools/gen_tashkil.py\n")
            bad = 1
        if not LEAN.exists() or LEAN.read_text(encoding="utf-8") != lean:
            sys.stderr.write("TASHKIL_LEAN_DRIFTED: شغّل python tools/gen_tashkil.py\n")
            bad = 1
        if res is not None and measure(mj) != res:
            sys.stderr.write("TASHKIL_RESULT_DRIFTED\n")
            bad = 1
        if not bad:
            sys.stdout.write(f"tashkil مطابق: {len(mj)} هيكلًا\n")
        return bad
    OUT.mkdir(parents=True, exist_ok=True)
    MUJAM.write_bytes(gz(m_tsv))
    LEAN.write_text(lean, encoding="utf-8")
    sys.stdout.write(f"كُتب المعجم ({len(mj)} هيكلًا) و{LEAN.name}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
