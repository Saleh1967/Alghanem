"""الصدقُ عند السيرافيّ وصفوفُ القابليّة الثلاثيّة (ADR ٨٩، أمرُ المالك 2026-10-17).

المودَعاتُ في `corpora/sidq/`:
* `sirafi-anchors.tsv`: أسطرُ شرح السيرافيّ المختوم على باب الاستقامة
  (`corpora/kitab/`، Sham19Y0017726، 1-based)، كلُّ اقتباسٍ في سطره بعينه.
* `qabiliyya3.tsv`: صفوفُ القابليّة الثلاثيّة (جنسُ الفاعل، الفعل، جنسُ المفعول، الإيجاب)،
  ملأها الوكيلُ من شواهد السيرافيّ للكذب الظاهر، وكلُّ صفٍّ بسطر شاهده.
* `owner-qabiliyya.json`: توقيعُ المالك على بصمة `qabiliyya3.tsv`. فإن كان `signed_by` فارغًا
  أو اختلفت البصمة، فالصفوفُ مسوّدةٌ لا يقرؤها الحكم (`signed = false`).

تولِّد `formal/a116/A116/SidqData.lean`. و`--check` يُسقط البناءَ بـ`SIRAFI_SEAL_BROKEN`
أو `QUOTE_NOT_IN_SEALED_LINE` أو `ROW_WITHOUT_ANCHOR` أو `MUSHAF_ANCHOR_MISSING`
أو `SIDQ_DATA_DRIFTED`. معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "corpora" / "sidq"
SIRAFI = (ROOT / "corpora" / "kitab"
          / "0368AbuSacidSirafi.SharhKitabSibawayhi.Sham19Y0017726-ara1.gz")
SIRAFI_SHA = "d53137fd4151028c5dee8ab9ff3e42275ecf0c39089e15fbf50bf0eefaa1603a"
MUSHAF = ROOT / "corpora" / "quran-simple-enhanced.txt"
MUSHAF_ANCHOR = (5337, "وَحُمِلَتِ الْأَرْضُ وَالْجِبَالُ")
ANCHORS = DIR / "sirafi-anchors.tsv"
ROWS = DIR / "qabiliyya3.tsv"
SIGN = DIR / "owner-qabiliyya.json"
LEAN = ROOT / "formal" / "a116" / "A116" / "SidqData.lean"


def table(path: Path) -> list[dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    keys = lines[0].split("\t")
    return [dict(zip(keys, ln.split("\t"), strict=True)) for ln in lines[1:]]


def signed() -> bool:
    s = json.loads(SIGN.read_text(encoding="utf-8"))
    sha = hashlib.sha256(ROWS.read_bytes()).hexdigest()
    return bool(s.get("signed_by")) and s.get("rows_sha256") == sha


def _s(x: str) -> str:
    return '"' + x.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_lean() -> str:
    out = ["-- مولَّدٌ بـ`tools/gen_sidq.py` من `corpora/sidq/`؛ لا يُحرَّر باليد.",
           "import A116.Sidq", "", "namespace A116.SidqSirafi", "",
           "/-- صفٌّ ثلاثيّ: جنسُ الفاعل، الفعل، جنسُ المفعول، الإيجاب، وسطرُ شاهده عند السيرافيّ. -/",
           "structure Saff3 where", "  fail : String", "  fil : String", "  mafool : String",
           "  ijab : Bool", "  shahid : Nat", "  deriving DecidableEq, Repr", "",
           "/-- المسوّدة كما ملأها الوكيل. -/", "def musawwada : List Saff3 := ["]
    rows = table(ROWS)
    for i, r in enumerate(rows):
        sep = "," if i + 1 < len(rows) else ""
        out.append(f"  ⟨{_s(r['fail'])}, {_s(r['fil'])}, {_s(r['mafool'])}, "
                   f"{'true' if r['ijab'] == '+' else 'false'}, {r['shahid_satr']}⟩{sep}")
    out += ["]", "", "/-- توقيعُ المالك على بصمة المسوّدة. -/",
            f"def signed : Bool := {'true' if signed() else 'false'}", "",
            "/-- الصفوفُ التي يقرؤها الحكم: الموقَّعةُ وحدَها. -/",
            "def rows3 : List Saff3 := if signed then musawwada else []", "",
            "/-- مراسي السيرافيّ: (السطر، النصّ بعينه). -/",
            "def marasi : List (Nat × String) := ["]
    an = table(ANCHORS)
    for i, r in enumerate(an):
        sep = "," if i + 1 < len(an) else ""
        out.append(f"  ({r['satr']}, {_s(r['iqtibas'])}){sep}")
    out += ["]", "", "end A116.SidqSirafi", ""]
    return "\n".join(out)


def breaches() -> list[str]:
    raw = gzip.decompress(SIRAFI.read_bytes())
    if hashlib.sha256(raw).hexdigest() != SIRAFI_SHA:
        return ["SIRAFI_SEAL_BROKEN"]
    ls = raw.decode("utf-8").splitlines()
    bad = [f"QUOTE_NOT_IN_SEALED_LINE:{r['satr']}" for r in table(ANCHORS)
           if r["iqtibas"] not in ls[int(r["satr"]) - 1]]
    shahid = {int(r["satr"]) for r in table(ANCHORS)}
    bad += [f"ROW_WITHOUT_ANCHOR:{r['fil']}" for r in table(ROWS)
            if int(r["shahid_satr"]) not in shahid]
    mus = MUSHAF.read_text(encoding="utf-8").splitlines()
    if MUSHAF_ANCHOR[1] not in mus[MUSHAF_ANCHOR[0] - 1]:
        bad.append("MUSHAF_ANCHOR_MISSING")
    if not LEAN.exists() or LEAN.read_text(encoding="utf-8") != render_lean():
        bad.append("SIDQ_DATA_DRIFTED")
    return bad


def main(argv: list[str]) -> int:
    if "--check" not in argv:
        LEAN.write_text(render_lean(), encoding="utf-8")
    bad = breaches()
    if bad:
        sys.stderr.write("\n".join(bad) + "\n")
        return 1
    state = "موقَّعة" if signed() else "مسوّدةٌ غيرُ موقَّعة"
    n_a, n_r = len(table(ANCHORS)), len(table(ROWS))
    sys.stdout.write(f"صدقُ السيرافيّ مطابق: {n_a} مرساةً، {n_r} صفوفٍ {state}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
