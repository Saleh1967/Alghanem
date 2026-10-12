"""عقدُ الشرح على مودَع المصحف (SHARH_INDEX.md): لكلّ صورةٍ أسطرُها (`slge.sharh.lines`) بوسمها ومرساتها
من سجلّ الدعاوى — والعدُّ على المودَع كلِّه.

`python tools/gen_sharh_index.py` يكتب الفهرس؛ و`gen_sharh_index.py --claims OUT.json.gz`
يكتب أيضًا مخرَجَ العقد (لا نصَّ فيه: أعدادٌ وحواملُ وأسماء) الذي يُخرج الغانمُ كلماتِه بـ`gate.exit`
(`tools/gen_sharh_text.py` هناك) ليغذّي الواجهة؛ و`--check` يطابق الفهرسَ ويفحص كلَّ سطرٍ بـ`breaches`.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.sharh import Line, anchor, breaches, lines, tag
from slge.status import LEDGER

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "SHARH_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]


def corpus() -> tuple[dict[str, Any], list[tuple[Word, tuple[int, int]]], Counter[int]]:
    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    forms = [(tuple((a, b) for a, b in x["cells"]), (x["integer"], x["ordinal"]))
             for x in d["forms"]]
    return d, forms, Counter(d["stream"])


def _plain(v: Any) -> Any:
    return list(v) if isinstance(v, tuple) else v


def measure() -> dict[str, Any]:
    d, forms, cnt = corpus()
    all_lines = [lines(w, n) for w, n in forms]
    bad = [b for ls in all_lines for b in breaches(ls)]
    by_claim: Counter[str] = Counter()
    by_claim_pos: Counter[str] = Counter()
    by_tag_pos: Counter[str] = Counter()
    for k, ls in enumerate(all_lines):
        for ln in ls:
            by_claim[ln.claim] += 1
            by_claim_pos[ln.claim] += cnt[k]
            by_tag_pos[tag(ln)] += cnt[k]
    used = sorted(by_claim, key=lambda c: [x.claim_id for x in LEDGER].index(c))
    return {"digest": d["corpus_sha256"], "forms": all_lines, "bad": bad, "by_claim": by_claim,
            "by_claim_pos": by_claim_pos, "by_tag_pos": by_tag_pos, "used": used,
            "positions": sum(cnt[k] for k in range(len(forms))),
            "refused": sum(v for k, v in cnt.items() if not 0 <= k < len(forms))}


def claims_json(m: dict[str, Any]) -> dict[str, Any]:
    by_id = {c.claim_id: c for c in LEDGER}
    ledger = {c: [by_id[c].status.name, anchor(Line(c, 0, "خانة")), by_id[c].statement]
              for c in m["used"]}
    return {"corpus_sha256": m["digest"], "ledger": ledger,
            "forms": [[[ln.claim, _plain(ln.value), ln.unit] for ln in ls] for ls in m["forms"]]}


def render(m: dict[str, Any]) -> str:
    total = sum(m["by_tag_pos"].values())
    rows = [f"| `{c}` | {tag(Line(c, 0, 'خانة'))} | `{anchor(Line(c, 0, 'خانة'))}` | "
            f"{m['by_claim'][c]:,} | {m['by_claim_pos'][c]:,} |" for c in m["used"]]
    tags = "، ".join(f"{t} {n:,} ({100 * n / total:.1f}%)"
                     for t, n in sorted(m["by_tag_pos"].items(), key=lambda x: -x[1]))
    return "\n".join([
        "# فهرسُ عقد الشرح — كلُّ سطرٍ بدعواه ووسمه ومرساته من سجلّ الدعاوى",
        "",
        "مولَّدٌ بـ`python tools/gen_sharh_index.py`؛ لا يُحرَّر باليد (ADR ٤٤). "
        "لكلّ صورةٍ من مودَع المصحف أسطرٌ "
        "(الدعوى، القيمة، الوحدة) من قرّاء السُّلَّم القائمين، ووسمُ السطر ومرساتُه وسمُ دعواه وسندُها في "
        "`status.LEDGER` بعينه — فلا سطرَ أقوى من سنده. "
        "لا نصَّ في العقد؛ والكلمةُ تخرج بـ`gate.exit` في "
        "الغانم (`tools/gen_sharh_text.py`).",
        "",
        f"{len(m['forms']):,} صورةً على {m['positions']:,} موضعًا (والمواضعُ المرفوضةُ في البوّابة "
        f"{m['refused']:,} لا أسطرَ لها)؛ أسطرٌ على المواضع: {total:,}؛ خروقُ العقد: {len(m['bad'])}.",
        "",
        f"الوسومُ على المواضع: {tags}.",
        "",
        "| الدعوى | الوسم | المرساة | أسطرٌ على الصور | أسطرٌ على المواضع |",
        "|---|---|---|---:|---:|",
        *rows,
        "",
        "## ما ليس هنا — باسمه",
        "",
        "- رقمُ الآية سورةً وآيةً: لا جدولَ مختومًا لحدود السور، فالآيةُ برقم سطرها في المدوّنة المختومة.",
        "- السطرُ يقول ما يقوله قارئُه على الصورة وحدَها: لا سياقَ جملةٍ ولا حسمَ بين القراءات.",
        "",
    ])


def main() -> int:
    args = sys.argv[1:]
    m = measure()
    if m["bad"]:
        print("\n".join(sorted(set(m["bad"]))[:20]))
        return 1
    text = render(m)
    if "--claims" in args:
        out = Path(args[args.index("--claims") + 1])
        with gzip.open(out, "wt", encoding="utf-8") as f:
            json.dump(claims_json(m), f, ensure_ascii=False, separators=(",", ":"))
        print(f"كُتب {out}")
    if "--check" in args:
        if TARGET.read_text(encoding="utf-8") != text:
            print("SHARH_INDEX.md قديم: شغّل python tools/gen_sharh_index.py")
            return 1
        print("SHARH_INDEX.md مطابق")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    print("كُتب SHARH_INDEX.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
