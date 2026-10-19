"""ختمُ نصوص النبهانيّ ومودَعُ المعلومات السابقة (ADR ٨٧، أمرُ المالك 2026-10-17: «اختم وأودِع»).

ثلاثةُ نصوصٍ مختومةٌ ببصمتها في `corpora/nabhani/`، منسوخةٌ بعينها من
`Saleh1967/alghanem-constitution@f75a43b9` (`suspended/data__sources/`):
* «التفكير» (`tafkir.txt`) — تصديرُ المكتبة الشاملة.
* «الشخصيّة الإسلاميّة» ج1 (`shakhsiyya_j1.txt`) وج3 (`shakhsiyya_j3.txt`).

والمودَعان (ملءُ الوكيل بتفويض المالك، `corpora/nabhani/agent-fill.json`، غيرُ موقَّع):
* `malumat.tsv`: صفوفُ المعلومات السابقة — كلُّ صفٍّ اقتباسٌ بعينه من سطرٍ مسمًّى (السطرُ 1-based)،
  وموضوعُه ونوعُه ومحمولُه وإيجابُه ومرتبتُه كما ملأها الوكيل.
* `tarifat.tsv`: التعريفاتُ التي يقوم عليها النوعُ والمرتبة.
والنصُّ `sharh` هو شرحُ ابن عقيل المختوم (`corpora/ibn-aqil/`).

تولِّد `formal/a116/A116/MalumatData.lean` من المودَعَين. `--check` يُسقط البناءَ بـ`NABHANI_SEAL_BROKEN`
أو `NABHANI_SEAL_MISSING` أو `NABHANI_MANIFEST_DRIFTED` أو `QUOTE_NOT_IN_SEALED_LINE` أو
`MALUMAT_DATA_DRIFTED` أو `AGENT_FILL_DRIFTED` (المودَعُ غيرُ ما سُجّل ملؤه).
معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "corpora" / "nabhani"
MANIFEST = DIR / "MANIFEST.tsv"
MALUMAT = DIR / "malumat.tsv"
TARIFAT = DIR / "tarifat.tsv"
LEAN = ROOT / "formal" / "a116" / "A116" / "MalumatData.lean"
SHARH = ROOT / "corpora" / "ibn-aqil" / "sharh-alfiyya.txt.gz"
SHARH_SHA = "661e43ea265eca8c72b9e4ab7a46cd9182b34e834105b595241bc7787b471f09"
SOURCE = "Saleh1967/alghanem-constitution@f75a43b9f4ed3df059f1feb832f48d96e6f846ba"
STATUS = "مختوم"
LICENCE = "غير معلنة (LICENCE_UNDECLARED)"

# (المفتاح، الملفّ، العنوان، sha256 قبل الضغط، الحجمُ بالبايت)
SEALS: tuple[tuple[str, str, str, str, int], ...] = (
    ("tafkir", "tafkir.txt", "التفكير للنبهاني",
     "f7fcc683237681e8d24dfeb59afb5e9b2e8536822a925eab010e9bed05f5d83c", 339129),
    ("j1", "shakhsiyya_j1.txt", "الشخصية الإسلامية ج1 للنبهاني",
     "77d80c69c80cdb967152702458956553a79d89d5ca220926e2b1b01cc24525ab", 870941),
    ("j3", "shakhsiyya_j3.txt", "الشخصية الإسلامية ج3 للنبهاني",
     "dd57e74bec43534ceec90797ad050cb104a16925b6d0bf0304796d42e70c425e", 1242143),
)
NAW = ("wujud", "haqiqa", "sifa", "khassa", "qabiliyya", "tamyiz", "marsaZaman",
       "marsaMakan", "istilah", "mutawati", "mushakkik", "juzi")


def render_manifest() -> str:
    head = "file\ttitle\tsource\tsha256\tbytes\tstatus\tlicence\n"
    return head + "".join(f"{f}.gz\t{t}\t{SOURCE}\t{h}\t{n}\t{STATUS}\t{LICENCE}\n"
                          for _, f, t, h, n in SEALS)


def _raw(path: Path, sha: str, size: int | None, tag: str) -> str:
    raw = gzip.decompress(path.read_bytes())
    if hashlib.sha256(raw).hexdigest() != sha or (size is not None and len(raw) != size):
        raise ValueError(f"{tag}:{path.name}")
    return raw.decode("utf-8")


def texts() -> dict[str, list[str]]:
    """النصوصُ المختومة أسطرًا بعد التحقّق من بصماتها."""
    out = {k: _raw(DIR / f"{f}.gz", h, n, "NABHANI_SEAL_BROKEN").splitlines()
           for k, f, _, h, n in SEALS}
    out["sharh"] = _raw(SHARH, SHARH_SHA, None, "SHARH_SEAL_BROKEN").splitlines()
    return out


def table(path: Path) -> list[dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    keys = lines[0].split("\t")
    return [dict(zip(keys, ln.split("\t"), strict=True)) for ln in lines[1:]]


def _s(x: str) -> str:
    return '"' + x.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_lean() -> str:
    rows = table(MALUMAT)
    tar = table(TARIFAT)
    out = ["-- مولَّدٌ بـ`tools/gen_nabhani.py` من `corpora/nabhani/malumat.tsv` و`tarifat.tsv`؛"
           " لا يُحرَّر باليد.",
           "import A116.Malumat", "", "namespace A116.Malumat", "",
           "/-- صفوفُ المعلومات السابقة كما ملأها الوكيل (السطرُ 1-based). -/",
           "def rows : List Saff := ["]
    for i, r in enumerate(rows):
        sep = "," if i + 1 < len(rows) else ""
        out.append(f"  ⟨{_s(r['nass'])}, {r['satr']}, {_s(r['iqtibas'])}, {_s(r['mawdu'])}, "
                   f".{r['naw']}, {_s(r['mahmul'])}, {'true' if r['ijab'] == '+' else 'false'}, "
                   f"{'none' if r['martaba'] == '-' else '(some .' + r['martaba'] + ')'}⟩{sep}")
    out += ["]", "", "/-- التعريفاتُ: (الاسم، النصّ، السطر، الاقتباس). -/",
            "def tarifat : List (String × String × Nat × String) := ["]
    for i, r in enumerate(tar):
        sep = "," if i + 1 < len(tar) else ""
        out.append(f"  ({_s(r['ism'])}, {_s(r['nass'])}, {r['satr']}, {_s(r['iqtibas'])}){sep}")
    out += ["]", "", "end A116.Malumat", ""]
    return "\n".join(out)


def breaches() -> list[str]:
    bad: list[str] = []
    for _, f, _, sha, size in SEALS:
        path = DIR / f"{f}.gz"
        if not path.exists():
            bad.append(f"NABHANI_SEAL_MISSING:{f}")
            continue
        raw = gzip.decompress(path.read_bytes())
        if hashlib.sha256(raw).hexdigest() != sha or len(raw) != size:
            bad.append(f"NABHANI_SEAL_BROKEN:{f}")
    if bad:
        return bad
    if not MANIFEST.exists() or MANIFEST.read_text(encoding="utf-8") != render_manifest():
        bad.append("NABHANI_MANIFEST_DRIFTED")
    ts = texts()
    for r in table(MALUMAT) + table(TARIFAT):
        n = int(r["satr"])
        if not (0 < n <= len(ts[r["nass"]]) and r["iqtibas"] in ts[r["nass"]][n - 1]):
            bad.append(f"QUOTE_NOT_IN_SEALED_LINE:{r['nass']}:{n}")
    for r in table(MALUMAT):
        if r["naw"] not in NAW:
            bad.append(f"NAW_UNDECLARED:{r['naw']}")
    fill = json.loads((DIR / "agent-fill.json").read_text(encoding="utf-8"))
    for rel, sha in fill["files"].items():
        if hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() != sha:
            bad.append(f"AGENT_FILL_DRIFTED:{rel}")
    if not LEAN.exists() or LEAN.read_text(encoding="utf-8") != render_lean():
        bad.append("MALUMAT_DATA_DRIFTED")
    return bad


def main(argv: list[str]) -> int:
    if "--check" not in argv:
        MANIFEST.write_text(render_manifest(), encoding="utf-8")
        LEAN.write_text(render_lean(), encoding="utf-8")
    bad = breaches()
    if bad:
        sys.stderr.write("\n".join(bad) + "\n")
        return 1
    sys.stdout.write(f"ختمُ النبهانيّ مطابق: {len(SEALS)} نصوص، {len(table(MALUMAT))} صفًّا\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
