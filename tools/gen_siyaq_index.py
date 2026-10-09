"""فهرسُ السياق (SIYAQ_INDEX.md): المصحفُ موقعًا موقعًا في حدّه. يقرأ مودَعَي الغانم معًا —
`corpus-certificates.json.gz` (كلُّ موقعٍ ابتداءً) و`context-certificates.json.gz` (الموقعُ نفسُه في
سياقه: وصلًا بما قبله، وقفًا في آخر الآية) بمواقعهما المشتركة (78,245) — ويقيس: (١) حالَ كلّ موقعٍ في
السياق (جاهزٌ أو رفضٌ باسمه) مقابلَ حاله ابتداءً؛ (٢) علاقةَ صورة السياق بصورة الابتداء كما طبعتهما
البوّابة (`siyaq.classify`): هي، ساقطةُ الوصل، مسكَّنةُ الوقف، الاثنان، أو غيرُ ذلك باسمه؛ (٣) قاعدةَ ردّ
الهمزة الساقطة (`sawabiq.lift`، المبرهَنةُ حركتُها من الثالث `wasl_state_damm_iff`) على صورة الابتداء
الحقيقيّة: كم يردّها بعينها وكم يخطئ حركتَها وبأيّ حركتين؛ (٤) ما يُخفيه الوقف: حالةُ آخر الكلمة التي
سكّنها الوقفُ بتوزيعها. لا نصَّ هنا: خاناتٌ وأعداد، والصورُ تُطبع من خاناتها للعرض.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.sawabiq import lift
from slge.siyaq import TANWIN, Hadd, classify, relation, restore, waqf

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "SIYAQ_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
MARKS = {"فتح": "َ", "كسر": "ِ", "ضم": "ُ", "سكون": "ْ"}


def _load(name: str) -> dict[str, Any]:
    with gzip.open(DATA / name, "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    return d


def _forms(d: dict[str, Any]) -> list[Word]:
    return [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]]


def vowelled(w: Word) -> str:
    return "".join(k + MARKS[s] for k, s in w)


def positions() -> list[tuple[Word | None, Word | None, Hadd, str | None, str | None]]:
    """لكلّ موقع: صورةُ الابتداء (أو لا شهادة)، صورةُ السياق (أو لا)، الحدُّ، اسمُ رفض السياق، ووجهُ
    الوصل في آخر الكلمة اليساريّة (التقاءُ الساكنين) إن كان."""

    start, ctx = _load("corpus-certificates.json.gz"), _load("context-certificates.json.gz")
    assert start["tokens"] == ctx["tokens"] == len(start["stream"]) == len(ctx["stream"])
    assert start["corpus_sha256"] == ctx["corpus_sha256"]
    sf, cf = _forms(start), _forms(ctx)
    out: list[tuple[Word | None, Word | None, Hadd, str | None, str | None]] = []
    pos = 0
    for n in ctx["line_lengths"]:
        for i in range(n):
            s_idx, (c_idx, exit_, ref, jn) = start["stream"][pos], ctx["stream"][pos]
            out.append((sf[s_idx] if s_idx >= 0 else None, cf[c_idx] if c_idx >= 0 else None,
                        Hadd(i > 0, exit_ == 1), ctx["refusals"][ref] if ref >= 0 else None,
                        ctx["junctions"][jn] if jn >= 0 else None))
            pos += 1
    assert pos == ctx["tokens"]
    return out


def measure() -> dict[str, Any]:
    rows = positions()
    status: Counter[str] = Counter()
    refusals: Counter[str] = Counter()
    rel: Counter[str] = Counter()
    lift_ok = lift_bad = 0
    lift_pairs: Counter[str] = Counter()
    bad_top: Counter[str] = Counter()
    hidden: Counter[str] = Counter()
    restored = named = 0
    other_top: Counter[str] = Counter()
    junction: Counter[str] = Counter()
    for s, c, h, ref, jn in rows:
        if jn:
            junction[jn] += 1
        key = (("ابتداءً جاهز" if s else "ابتداءً مرفوض") + "، "
               + ("سياقًا جاهز" if c else "سياقًا مرفوض"))
        status[key] += 1
        if ref:
            refusals[ref] += 1
        if s is None or c is None:
            continue
        r = classify(s, c)
        rel[relation(r)] += 1
        if r is None:
            other_top[f"{vowelled(s)} ← {vowelled(c)}"] += 1
            continue
        dropped, k = r
        named += 1
        restored += s in restore(h, c)
        if dropped:  # سقطت الهمزة: قاعدةُ الردّ على الأصل الحقيقيّ (قبل الوقف)
            target = waqf(k, s) if k else s
            back = lift(c)
            if back == target:
                lift_ok += 1
            else:
                lift_bad += 1
                lift_pairs[f"{back[0][1]} ← {s[0][1]}"] += 1
                bad_top[vowelled(s)] += 1
        if k:  # ما أخفاه الوقف: حالةُ الآخر (أو تنوينُه) ابتداءً
            last = s[-1][1] if s[-1] != TANWIN else "تنوين " + s[-2][1]
            hidden[last] += 1
    return {
        "tokens": len(rows),
        "status": dict(sorted(status.items())),
        "refusals": dict(sorted(refusals.items())),
        "junctions": dict(sorted(junction.items())),
        "both_ready": sum(rel.values()),
        "relation": dict(sorted(rel.items(), key=lambda kv: -kv[1])),
        "lift_ok": lift_ok, "lift_bad": lift_bad,
        "lift_pairs": dict(sorted(lift_pairs.items())),
        "lift_bad_top": bad_top.most_common(10),
        "hidden_by_pause": dict(sorted(hidden.items())),
        "named": named, "restored": restored,
        "other_top": other_top.most_common(10),
    }


def render() -> str:
    m = measure()

    def pct(k: int, d: int) -> str:
        return f"{100 * k / d:.1f}%" if d else "—"

    lines = [
        "# فهرسُ السياق — المصحفُ موقعًا موقعًا في حدّه",
        "",
        "مولَّدٌ بـ`python tools/gen_siyaq_index.py` من `src/slge/siyaq.py` على مودَعَي الغانم "
        "(`corpus-certificates.json.gz` ابتداءً، `context-certificates.json.gz` في السياق)؛ لا يُحرَّر "
        "باليد. البرهانُ `formal/Slge/Siyaq.lean`: الإسقاطُ إلى الحدّ — الوقفُ بوجهٍ من أربعة كما "
        "طبعتها البوّابة (تسكينٌ؛ تنوينُ النصب ألفًا؛ حذفُ التنوين مع التسكين؛ تاءُ التأنيث هاءً) ثمّ "
        "الوصلُ يُسقط همزةَ الوصل — والردُّ مرشَّحاتٍ كلُّها يُسقَط إلى الصورة بعينها "
        "(`project_restore`)، والصورةُ نفسُها مرشَّحة (`self_mem_restore`)، وبلا حدٍّ لا شيء "
        "(`restore_plain`)، والعددُ ≤ 26 (`restore_length_le`). وما يُقاس هنا لا يُبرهَن: حركةُ الهمزة "
        "المردودة هي حركةُ الأصل، ووجهُ الوقف الذي اختارته البوّابة.",
        "",
        "## الحالُ في السياق مقابلَ الحال ابتداءً", "",
        f"{m['tokens']:,} موقعًا (المواقعُ نفسُها في المودَعين؛ بصمةُ المدوّنة واحدة):",
        "",
        "| الحال | المواقع |", "|---|---|",
        *(f"| {k} | {v:,} |" for k, v in m["status"].items()),
        "",
        "الرفضُ في السياق باسمه (ما يرفضه الحدُّ لا الكلمة):", "",
        "| الرفض | المواقع |", "|---|---|",
        *(f"| `{k}` | {v:,} |" for k, v in sorted(m["refusals"].items(), key=lambda kv: -kv[1])),
        "",
        "التقاءُ الساكنين على الحدّ — ما فعله الوصلُ بآخر الكلمة اليساريّة (`A116.Iltiqa`، وجهٌ مسمًّى "
        "تحمله شهادةُ الموقع؛ ذرّاتُ الكلمة نفسِها لا تُمسّ):", "",
        "| الوجه | المواقع |", "|---|---|",
        *(f"| `{k}` | {v:,} |" for k, v in sorted(m["junctions"].items(), key=lambda kv: -kv[1])),
        "",
        "## علاقةُ صورة السياق بصورة الابتداء (كما طبعتهما البوّابة)", "",
        f"على {m['both_ready']:,} موقعًا جاهزًا في الحالين (`siyaq.classify`):",
        "",
        "| العلاقة | المواقع | النسبة |", "|---|---|---|",
        *(f"| {k} | {v:,} | {pct(v, m['both_ready'])} |" for k, v in m["relation"].items()),
        "",
        "## ردُّ الهمزة الساقطة (`sawabiq.lift`) على الأصل الحقيقيّ", "",
        f"من {m['lift_ok'] + m['lift_bad']:,} موقعًا سقطت همزتُه في الوصل يردّها `lift` بعينها "
        f"**{m['lift_ok']:,} ({pct(m['lift_ok'], m['lift_ok'] + m['lift_bad'])})**، ويخطئ "
        f"حركتَها في {m['lift_bad']:,}: "
        + ("، ".join(f"{k} {v:,}" for k, v in m["lift_pairs"].items()) or "—") + ".",
        "",
        "أكثرُ ما تُخطَأ حركتُه — بصوره ابتداءً (مثلان في الصدر: أل الشمسيّة عند `lift` وهي افتعلَ "
        "المدغمُ أو تفاعلَ المدغمُ عند البوّابة — اتَّخَذَ، اثَّاقَلْتُمْ؛ القرينةُ لا الخانات تفصل):", "",
        "| الصورة | المواقع |", "|---|---|",
        *(f"| {w} | {n:,} |" for w, n in m["lift_bad_top"]),
        "",
        "## ما يُخفيه الوقف", "",
        "آخرُ الكلمة ابتداءً (حالتُه أو تنوينُه) حيث غيّره الوقف: "
        + "، ".join(f"{k} {v:,}" for k, v in m["hidden_by_pause"].items()) + ".",
        "",
        f"الردُّ `restore` يحوي الأصلَ بين مرشَّحاته في **{m['restored']:,} من {m['named']:,}** "
        f"({pct(m['restored'], m['named'])}) من المواقع ذات العلاقة المسمّاة.",
        "",
        "## غيرُ ذلك — باسمه", "",
        *(["| ابتداءً ← في السياق | المواقع |", "|---|---|",
           *(f"| {w} | {n:,} |" for w, n in m["other_top"])] if m["other_top"]
          else ["لا شيء: كلُّ علاقةٍ بين الصورتين مسمّاةٌ بوجهها."]),
        "",
        "## ما ليس هنا — باسمه", "",
        "- الحدُّ هنا حدُّ الآية (سطرُ المدوّنة): وقفٌ في آخرها ووصلٌ فيما بينها؛ الوقفُ داخلَ الآية "
        "والوصلُ بين آيتين ليسا في المودَع.",
        "- ما رُفض في السياق باسمه (الحروفُ المقطّعة قبل كلمة، مدُّ الفرق موصولًا…) لا يُقاس عليه: دَينُ "
        "البوّابة لا هذا القارئ.",
        "- وجهُ الوصل (حذفُ المدّ، كسرُ التنوين، سقوطُ الألف الفارقة) مسجَّلٌ على الموقع ولا يدخل خانات "
        "الكلمة الثانية؛ أثرُه على الكلمة اليساريّة مسألةُ شهادة الموقع (م١+م٢) لا هذا الفهرس.",
        "- «غيرُ ذلك» أعلاه علاقاتٌ لا يسمّيها `classify`؛ لا تُزاد قاعدةٌ من الذاكرة بل من الشاهد.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    text = render()
    if "--check" in argv:
        ok = TARGET.read_text(encoding="utf-8") == text
        sys.stdout.write("SIYAQ_INDEX.md مطابق\n" if ok else "SIYAQ_INDEX.md غيرُ مطابق\n")
        return 0 if ok else 1
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب SIYAQ_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
