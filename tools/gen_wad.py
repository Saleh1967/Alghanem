"""علاقةُ الوضع مودَعةً (ADR ٥٦): «الوضعُ هو تخصيص لفظ بمعنى» (الشخصيّة ج3 ف393)، و«طريقُ معرفة اللغة
العربية … النقلُ المتواتر وخبرُ الآحاد» (ف397) — فالعلاقةُ تُنقل ولا تُستنتج.

**الواقع.** طرفا العلاقة من مودَعين قائمين لا يُحرَّران هنا:

* `corpora/lane/lane-root-keys.tsv` (ADR ٤٩، `tools/gen_lane_roots.py --check`): كلُّ صيغةٍ وضعها لين
  تحت جذرٍ ثلاثيّ، مفتاحُها خاناتُها كما أخرجتها البوّابةُ على مجال لين (بلا حركة الآخر ولا التنوين). هذا
  **الراوي الأوّل**، بالحركات.
* `corpora/hadith/maqayis-skeletons.tsv` (ADR ٤٧، `tools/gen_hadith_roots.py --check`): كلُّ هيكلٍ وضعه
  ابنُ فارس تحت جذرٍ في «مقاييس اللغة» المختوم. هذا **الراوي الثاني**، بالهيكل وحدَه (بلا حركات).

**القاعدة** (`RULE_W`):

* **اللفظ** مفتاحُ لين (خاناتٌ). و**المعنى** مرساةٌ لا نصّ: مادّةُ الجذر كما وضعه الراوي، فـ(لفظ، جذر)
  زوجٌ في العلاقة إن وضع لينُ اللفظَ تحت الجذر. والمعنى على مستوى **المادّة** لا مستوى المعنى الجزئيّ
  (`SENSE_LEVEL_NOT_DEPOSITED`).
* **الدرجة** عددُ الراويين المستقلّين للزوج: لين وحدَه (1)، أو لين وابن فارس (2) إن كان هيكلُ اللفظ
  (حواملُه مطويّةً بطيّ `gen_hadith_roots.fold`) في معجم ابن فارس تحت الجذرِ نفسِه
  (ألفُ لين في الجذر همزةٌ).
  استقلالُ الراويين معلَنٌ لا مفحوص (`NARRATOR_INDEPENDENCE_DECLARED`)؛ وغيابُ ابن فارس ليس نفيًا.
* **المشترك** (ف418: «يكون اللفظ واحداً والمعنى كثير … وضع لكل واحد من تلك المعاني») لفظٌ له في
  العلاقة جذران فأكثر. ويُطبع إلى `formal/a116/A116/WadData.lean` لتبرهن عليه `A116.Wad`.

`python tools/gen_wad.py` يكتب `corpora/wad/wad.tsv` و`WadData.lean`؛ و`--check` يُسقط البناءَ بـ
`WAD_DEPOSIT_DRIFTED` أو `WAD_LEAN_DRIFTED`. معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANE_KEYS = ROOT / "corpora" / "lane" / "lane-root-keys.tsv"
SKELETONS = ROOT / "corpora" / "hadith" / "maqayis-skeletons.tsv"
OUT = ROOT / "corpora" / "wad" / "wad.tsv"
LEAN = ROOT / "formal" / "a116" / "A116" / "WadData.lean"

FOLD = {"أ": "ء", "إ": "ء", "ؤ": "ء", "ئ": "ء", "ى": "ي"}
LANE = "lane"
IBN_FARIS = "ibn-faris"


def fold(s: str) -> str:
    """طيُّ `gen_hadith_roots.fold` بعينه (منسوخٌ ليبقى المولِّدُ بلا استيرادٍ لأدوات القياس)."""

    return "".join(FOLD.get(c, c) for c in s.replace("آ", "ءا"))


def read_tsv(path: Path) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for ln in path.read_text(encoding="utf-8").splitlines():
        k, vals = ln.split("\t")
        out[k] = vals.split(" ")
    return out


def skeleton_of_key(key: str) -> str:
    """هيكلُ المفتاح: حاملُ كلّ خانةٍ بترتيبها، مطويًّا."""

    return fold("".join(a[0] for a in key.split(" ")))


def lane_root_as_ibn_faris(root: str) -> str:
    """ألفُ لين في الجذر همزةٌ (اوب = أوب)؛ وابنُ فارس يطوي الهمزةَ «ء»."""

    return fold(root.replace("ا", "ء"))


def pairs() -> list[tuple[str, str, tuple[str, ...]]]:
    """(اللفظ، الجذر، الرواة) لكلّ زوجٍ في العلاقة، مرتّبًا."""

    lane = read_tsv(LANE_KEYS)
    faris = {k: set(v) for k, v in read_tsv(SKELETONS).items()}
    out: list[tuple[str, str, tuple[str, ...]]] = []
    for key in sorted(lane):
        sk = skeleton_of_key(key)
        for root in sorted(set(lane[key])):
            ws = [LANE]
            if lane_root_as_ibn_faris(root) in faris.get(sk, set()):
                ws.append(IBN_FARIS)
            out.append((key, root, tuple(ws)))
    return out


def render_tsv(ps: list[tuple[str, str, tuple[str, ...]]]) -> str:
    return "".join(f"{k}\t{r}\t{','.join(ws)}\n" for k, r, ws in ps)


def mushtarak(ps: list[tuple[str, str, tuple[str, ...]]]
              ) -> list[tuple[str, list[tuple[str, tuple[str, ...]]]]]:
    by: dict[str, list[tuple[str, tuple[str, ...]]]] = {}
    for k, r, ws in ps:
        by.setdefault(k, []).append((r, ws))
    return [(k, v) for k, v in sorted(by.items()) if len(v) >= 2]


def _lean_str(s: str) -> str:
    assert '"' not in s and "\\" not in s
    return f'"{s}"'


def render_lean(ps: list[tuple[str, str, tuple[str, ...]]]) -> str:
    rows = mushtarak(ps)
    keys = len({k for k, _, _ in ps})
    two = sum(1 for _, _, ws in ps if len(ws) == 2)
    lines = [
        "/-! علاقةُ الوضع: المشتركُ منها (لفظٌ بجذرين فأكثر) — مولَّدٌ بـ`tools/gen_wad.py` من",
        "`corpora/wad/wad.tsv` (لين وابنُ فارس)، ويطابقه `tests/test_wad.py`؛",
        "لا يُحرَّر باليد (ADR ٥٦). -/",
        "",
        "set_option autoImplicit false",
        "",
        "namespace A116.WadData",
        "",
        "/-- عددُ أزواج العلاقة كلِّها، وعددُ ألفاظها، وعددُ الأزواج التي رواها الراويان معًا. -/",
        f"def pairCount : Nat := {len(ps)}",
        f"def keyCount : Nat := {keys}",
        f"def twoNarrators : Nat := {two}",
        "",
        "/-- (اللفظ، [(الجذر، الرواة)]) لكلّ لفظٍ له في العلاقة جذران فأكثر. -/",
        "def mushtarak : List (String × List (String × List String)) := [",
    ]
    body = []
    for k, v in rows:
        rs = ", ".join(f"({_lean_str(r)}, [{', '.join(_lean_str(w) for w in ws)}])" for r, ws in v)
        body.append(f"  ({_lean_str(k)}, [{rs}])")
    lines.append(",\n".join(body))
    lines += ["]", "", "end A116.WadData", ""]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    ps = pairs()
    tsv, lean = render_tsv(ps), render_lean(ps)
    if "--check" in argv:
        bad = 0
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != tsv:
            sys.stderr.write("WAD_DEPOSIT_DRIFTED: شغّل python tools/gen_wad.py\n")
            bad = 1
        if not LEAN.exists() or LEAN.read_text(encoding="utf-8") != lean:
            sys.stderr.write("WAD_LEAN_DRIFTED: شغّل python tools/gen_wad.py\n")
            bad = 1
        if not bad:
            sys.stdout.write(f"wad مطابق: {len(ps)} زوجًا، {len(mushtarak(ps))} مشتركًا\n")
        return bad
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(tsv, encoding="utf-8")
    LEAN.write_text(lean, encoding="utf-8")
    sys.stdout.write(f"كُتب {OUT.name} ({len(ps)} زوجًا) "
                     f"و{LEAN.name} ({len(mushtarak(ps))} مشتركًا)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
