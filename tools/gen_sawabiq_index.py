"""فهرسُ السوابق الحرفيّة (SAWABIQ_INDEX.md): باءُ الجرّ ولامُ الجرّ ولامُ الأمر ولامُ كي وألُ التعريف وهمزةُ
الوصل، كلٌّ بعلاقته بما بعده على أبواب الكتاب. (١) على `corpus-certificates.json.gz` أوّلًا (قانونُ
القارئ): كم صورةً من المصحف تُقرأ سابقتُها، بأبوابها، وكم منها موصولةٌ (سقطت همزتُها أو كسرةُ لامها)،
وكم يتعدّد بابُها. (٢) ثمّ على `masaq-shibh.json.gz` (مرجعٌ محجوب): سوابقُ المرجع بأوسامها (`PREP`
بِ/لِ، `DET`، `CV_PREF`، `OTHER` لِ) وحالةُ جذعه: كم يقرؤها القارئُ بالباب الذي يوافق وسمَ المرجع وحالتَه،
وكم يقرؤها ببابٍ آخر فقط، وكم لا يقرؤها — وأكثرُ ما لا يُقرأ بصوره.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.pipeline import GOLD_JIHA
from slge.sawabiq import KINDS, sawabiq
from slge.sawabiq_table import TABLE

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "SAWABIQ_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
MARKS = {"فتح": "َ", "كسر": "ِ", "ضم": "ُ", "سكون": "ْ"}
EXPECT: dict[tuple[str, str, str], str] = {
    ("PREP", "بِ", "*"): "BA_JARR",
    ("PREP", "لِ", "مجرور"): "LAM_JARR", ("PREP", "لِ", "منصوب"): "LAM_KAY",
    ("OTHER", "لِ", "مجزوم"): "LAM_AMR", ("OTHER", "لْ", "مجزوم"): "LAM_AMR",
    ("PREP", "لْ", "مجزوم"): "LAM_AMR", ("CV_PREF", "لْ", "مجزوم"): "LAM_AMR",
    ("OTHER", "لِ", "منصوب"): "LAM_KAY",
    ("DET", "*", "*"): "AL", ("CV_PREF", "ء", "*"): "WASL_FIL",
}
"""وسمُ سابقة المرجع وصورتُها وحالةُ الجذع → البابُ المتوقَّع عندنا؛ `*` أيُّ شيء. ما ليس هنا (لَ التوكيد،
`CONJ`، `IMPERF_PREF`…) ليس من هذا القارئ."""


def corpus_forms() -> list[Word]:
    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    return [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]]


def masaq_rows() -> list[dict[str, Any]]:
    with gzip.open(DATA / "masaq-shibh.json.gz", "rt", encoding="utf-8") as f:
        rows: list[dict[str, Any]] = json.load(f)["rows"]
    return rows


def whole(r: dict[str, Any]) -> Word:
    return (*((a, b) for _, cs in r["pre"] for a, b in cs), *((a, b) for a, b in r["stem"]),
            *((a, b) for _, cs in r["suf"] for a, b in cs))


def vowelled(w: Word) -> str:
    return "".join(k + MARKS[s] for k, s in w)


def expected(tag: str, cell: tuple[str, str] | None, case: str) -> str | None:
    shape = (cell[0] + MARKS[cell[1]]) if cell else ""
    for (t, c, s), k in EXPECT.items():
        if t == tag and c in ("*", shape, cell[0] if cell else "") and s in ("*", case):
            return k
    return None


def measure() -> dict[str, Any]:
    forms = corpus_forms()
    kinds: Counter[str] = Counter()
    read = joined = multi = 0
    for w in forms:
        ms = sawabiq(w)
        if not ms:
            continue
        read += 1
        for k in {m.kind for m in ms}:
            kinds[k] += 1
        joined += any(m.joined for m in ms)
        multi += len({m.kind for m in ms}) > 1
    rows = masaq_rows()
    asked = agree = other = none = mabni = 0
    by_kind: Counter[str] = Counter()
    by_kind_ok: Counter[str] = Counter()
    unread: Counter[str] = Counter()
    for r in rows:
        w = whole(r)
        exp: list[tuple[str, int]] = []  # (البابُ المتوقَّع، موضعُ السابقة)
        for i, (t, cs) in enumerate(r["pre"]):
            kind = expected(str(t), (cs[0][0], cs[0][1]) if cs else None, str(r["case"]))
            if kind is not None:
                exp.append((kind, i))
        if not exp:
            continue
        if r["tag"] not in GOLD_JIHA and any(k in ("BA_JARR", "LAM_JARR") for k, _ in exp):
            mabni += 1  # الجارُّ على مبنيٍّ (لَهُمْ، بِمَا، لِمَنْ): الموزِّعُ لا هذا القارئ
            continue
        asked += 1
        ms = sawabiq(w)
        got = {m.kind for m in ms}
        want = {k for k, _ in exp}
        for k in want:
            by_kind[k] += 1
            by_kind_ok[k] += k in got
        if want <= got:
            agree += 1
        elif got:
            other += 1
        else:
            none += 1
            unread[vowelled(w)] += 1
    return {"table": len(TABLE), "lines": sorted({r[2] for r in TABLE}),
            "forms": len(forms), "read": read, "kinds": dict(kinds), "joined": joined,
            "multi": multi, "asked": asked, "agree": agree, "other": other, "none": none,
            "mabni": mabni,
            "by_kind": {k: (by_kind[k], by_kind_ok[k]) for k in KINDS if by_kind[k]},
            "unread_top": unread.most_common(12)}


def render() -> str:
    m = measure()

    def pct(k: int, d: int) -> str:
        return f"{100 * k / d:.1f}%" if d else "—"

    lines = [
        "# فهرسُ السوابق الحرفيّة — الحرفُ يُقرأ بعلاقته بما بعده على أبواب الكتاب",
        "",
        "مولَّدٌ بـ`python tools/gen_sawabiq_index.py` من `src/slge/sawabiq.py`؛ لا يُحرَّر باليد. "
        "البرهانُ `formal/Slge/Sawabiq.lean`: كلُّ قراءةٍ تُردّ بعينها (`sawabiq_restores`)، "
        "وما سقطت همزتُه لا يُرخَّص وحدَه (`joined_rest_unlicensed`) وقراءتُه قراءةُ أصله "
        "ابتداءً (`joined_is_initial`)، ولامُ الأمر المسكَّنة هي المكسورة (`sakin_is_kasra`)، "
        "وحركةُ الهمزة المردودة من الثالث (`wasl_state_damm_iff`)، وكلُّ صفٍّ من جدول الكتاب "
        "يقرؤه القارئ (`table_read`).",
        "",
        "## الأبوابُ من الكتاب المختوم", "",
        f"{m['table']} صفًّا من خمسة أبوابٍ بأسطرها " + "، ".join(str(n) for n in m["lines"]) +
        " (`tools/deposit_sawabiq.py`): «لام الإضافة ومعناها الملك»، «باء الجر إنما هي "
        "للإلزاق»، «اللام التي في الأمر وذلك قولك ليفعل»، «اللام التي في قولك جئتك لتفعل» (أن "
        "مضمرة)، ألفُ الوصل «مكسورة أبدا إلا أن يكون الحرف الثالث مضموما» و«إذا كان قبلها كلام "
        "حذفت»، و«فعلوا بلام الأمر مع الفاء والواو مثل ذلك: فلينظر». لكلّ صفٍّ شاهدُه في نصّ "
        "الباب وصورةٌ من المصحف يقرؤها القارئ بالباب نفسه.",
        "",
        "## على مودَع المصحف أوّلًا (قانونُ القارئ)", "",
        f"من {m['forms']:,} صورةً تُقرأ سابقتُها في **{m['read']:,} ({pct(m['read'], m['forms'])})**: "
        + "، ".join(f"{k} {v:,}" for k, v in sorted(m["kinds"].items(), key=lambda kv: -kv[1]))
        + f"؛ منها موصولةٌ (سقطت همزتُها أو كسرةُ لامها) {m['joined']:,}، ويتعدّد بابُها في "
        f"{m['multi']:,} — التعدّدُ يُحصى ولا يُحسم هنا.",
        "",
        "## على MASAQ (مرجعٌ محجوب)", "",
        "الكلماتُ التي لسابقتها عند المرجع وسمٌ له بابٌ عندنا ("
        + ", ".join(f"`{k}`" for k in sorted({t for t, _, _ in EXPECT})) + ") وجذعُها معربٌ أو فعل: "
        f"{m['asked']:,} (وسوى ذلك {m['mabni']:,} جارٌّ على مبنيٍّ — لَهُمْ، بِمَا، لِمَنْ — من الموزِّع لا "
        "من هذا القارئ). "
        f"يقرؤها القارئُ بالباب الموافق **{m['agree']:,} ({pct(m['agree'], m['asked'])})**، "
        f"وببابٍ آخر فقط {m['other']:,}، ولا يقرؤها {m['none']:,} ({pct(m['none'], m['asked'])}).",
        "",
        "| البابُ المتوقَّع | سُئل | وافق | النسبة |", "|---|---|---|---|",
        *(f"| `{k}` | {n:,} | {ok:,} | {pct(ok, n)} |" for k, (n, ok) in m["by_kind"].items()),
        "",
        "### أكثرُ ما لا يُقرأ — بصوره", "",
        "| الصورة | العدد |", "|---|---|",
        *(f"| {w} | {n:,} |" for w, n in m["unread_top"]),
        "",
        "## ما ليس هنا — باسمه", "",
        "- لامُ التوكيد والابتداء (لَ) ولامُ القسم ليست في هذا القارئ: لا علاقةَ خانيّةً تقيّدها بما "
        "بعدها.",
        "- خريطةُ أوسام المرجع → الأبواب معلَنة (`EXPECT`)؛ المرجعُ يسم لامَ كي `PREP` تارةً و`OTHER` "
        "تارةً، ويسم لفظَ الجلالة بأل `DET`.",
        "- ما لا يُقرأ أعلاه: صورٌ آخرُها لا يقرؤه `case_class` (المقصور، المضافُ إلى ضمير) أو همزةُ "
        "وصلٍ على قالبٍ ليس في `wasl.WASL_TEMPLATES` أو بلاحقتين؛ لا يُزاد من الذاكرة.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    text = render()
    if "--check" in argv:
        ok = TARGET.read_text(encoding="utf-8") == text
        sys.stdout.write("SAWABIQ_INDEX.md مطابق\n" if ok else "SAWABIQ_INDEX.md غيرُ مطابق\n")
        return 0 if ok else 1
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب SAWABIQ_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
