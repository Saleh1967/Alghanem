"""جدولُ العوامل (ADR ٧١): من مرفق المالك (الأعمدةُ الأربعة الأولى وحدَها) إلى مودَعٍ بصنف الأثر وباب
الألفيّة، ومنه `A116/AwamilData.lean` الذي تفحصه النواة.

* المودَع `corpora/awamil/awamil.tsv`: العاملُ، الأسلوبُ، حكمُ المرفق بلفظه، صنفُ الأثر (ثلاثةَ عشرَ صنفًا
  مغلقًا، `ATHAR`)، وسطرُ باب الألفيّة في شرح ابن عقيل المختوم (`corpora/ibn-aqil/`) الذي يُرسي الصنف.
* أعمدةُ المرفق الأخرى (الأوزان، CV pattern، الباب الصرفيّ، FOL…) **مرفوضة** باسمها
  `ATTACHMENT_COLUMNS_REJECTED`: مولَّدةٌ آليًّا وتناقض المودَع (ظنّ «ثلاثي مزيد III»، «إنّ: فَاعِلٌ | مَفْعُولٌ»).
* `--check` يُسقط البناءَ بـ`AWAMIL_LEAN_DRIFTED` أو `AWAMIL_BAB_LINE_DRIFTED` (سطرُ الباب ليس عنوانَ
  بابٍ في الشرح المختوم) أو `AWAMIL_CLASS_UNKNOWN`. معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import gzip
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TSV = ROOT / "corpora" / "awamil" / "awamil.tsv"
LEAN = ROOT / "formal" / "a116" / "A116" / "AwamilData.lean"
SHARH = ROOT / "corpora" / "ibn-aqil" / "sharh-alfiyya.txt.gz"
SHARH_SHA256 = "661e43ea265eca8c72b9e4ab7a46cd9182b34e834105b595241bc7787b471f09"

ATHAR = ("NASB_RAF", "RAF_NASB", "NASB_NASB", "RAF_TAWIL", "JARR", "JARR_OR_NASB", "TABI",
         "JAZM_FIL", "NASB_FIL", "JARR_OR_NASB_FIL", "JAZM_FILAYN", "NIDA", "NONE")
LEAN_NAME = {a: "".join(w.capitalize() for w in a.lower().split("_")) for a in ATHAR}
LEAN_NAME = {a: n[0].lower() + n[1:] for a, n in LEAN_NAME.items()}

# عناوينُ الأبواب التي تُرسي الأصناف، بأسطرها في الشرح المختوم (العنوانُ يبدأ بـ«### |»)
BAB_TITLES = {
    1847: "كان وأخواتها", 2202: "أفعال المقاربة", 2339: "إن وأخواتها", 2794: "ظن وأخواتها",
    4074: "الاستثناء", 4634: "حروف الجر", 6440: "عطف النسق", 6680: "النداء",
    7398: "إعراب الفعل", 7577: "عوامل الجزم",
}


def rows() -> list[dict[str, str]]:
    head, *body = TSV.read_text(encoding="utf-8").splitlines()
    keys = head.split("\t")
    return [dict(zip(keys, ln.split("\t"))) for ln in body if ln.strip()]


def sharh_lines() -> list[str]:
    raw = gzip.decompress(SHARH.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == SHARH_SHA256, "IBN_AQIL_SEAL_BROKEN"
    return raw.decode("utf-8").split("\n")


def render_lean(rs: list[dict[str, str]]) -> str:
    body = ",\n".join(f'  ("{r["amil"]}", .{LEAN_NAME[r["athar"]]}, {r["bab_line"]})' for r in rs)
    return (
        "import A116.Awamil\n\n"
        "/-! مولَّدٌ بـ`tools/gen_awamil.py` من `corpora/awamil/awamil.tsv` (ADR ٧١)؛ "
        "لا يُحرَّر باليد. -/\n\n"
        "namespace A116.Awamil\n\n"
        "/-- (العامل، صنفُ أثره، سطرُ باب الألفيّة في الشرح المختوم؛ 0 حيث لا باب). -/\n"
        "def rows : List (String × Athar × Nat) := [\n" + body + "]\n\nend A116.Awamil\n"
    )


def breaches() -> list[str]:
    bad: list[str] = []
    rs = rows()
    lines = sharh_lines()
    for r in rs:
        if r["athar"] not in ATHAR:
            bad.append(f"AWAMIL_CLASS_UNKNOWN:{r['amil']}:{r['athar']}")
        ln = int(r["bab_line"])
        if ln and (ln not in BAB_TITLES or BAB_TITLES[ln] not in lines[ln - 1]
                   or not lines[ln - 1].startswith("###")):
            bad.append(f"AWAMIL_BAB_LINE_DRIFTED:{r['amil']}:{ln}")
    if not LEAN.exists() or LEAN.read_text(encoding="utf-8") != render_lean(rs):
        bad.append("AWAMIL_LEAN_DRIFTED")
    return bad


def main(argv: list[str]) -> int:
    if "--check" not in argv:
        LEAN.write_text(render_lean(rows()), encoding="utf-8")
    bad = breaches()
    if bad:
        sys.stderr.write("\n".join(bad) + "\n")
        return 1
    sys.stdout.write(f"العواملُ مطابقة: {len(rows())} عاملًا\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
