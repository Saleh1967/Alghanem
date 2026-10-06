"""فهرسُ الجملة الاسميّة على درجات الترخيص التدريجيّ (JUMLA_INDEX.md) من `slge.jumla` وشريحة MASAQ.

الشريحةُ `tests/data/masaq-jumla.json`: كلماتُ المصحف التي وسمها MASAQ مبتدأً أو خبرًا، خاناتُها من
شهادات بوّابة الغانم (الجذعُ والسوابقُ واللواحقُ بأوسامها). الأزواجُ تُبنى هنا: لكلّ مبتدأٍ أقربُ خبرٍ في
نافذته (بين المبتدأ قبله والمبتدأ بعده)، والمؤخّرُ يأخذ ما قبله.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from slge.cells import index
from slge.jumla import (
    WITNESSES,
    Jumla,
    admissible,
    agree,
    agree_loose,
    broken_plural,
    gender,
    khabar_kind,
    mubtada_kind,
    nakira,
    number,
    order,
    rabit,
)

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "JUMLA_INDEX.md"
SLICE = ROOT / "tests" / "data" / "masaq-jumla.json"
KEEP = ("PREP", "IMPERF_PREF", "IV3MP", "IV3MS", "DET")
Word = tuple[tuple[str, str], ...]


def _cells(r: dict[str, Any], keep: tuple[str, ...] = KEEP) -> Word:
    pre = [(a, b) for t, cs in r["pre"] for a, b in cs if t in keep]
    return (*pre, *((a, b) for a, b in r["stem"]))


def _is_mub(r: dict[str, Any]) -> bool:
    return r["role"] in ("مبتدأ", "مبتدأ مؤخر")


def _is_kh(r: dict[str, Any]) -> bool:
    return (r["role"] == "خبر" or "خبر" in r["pfs"] or r["pf"] == "خبر") and not _is_mub(r)


def pairs() -> list[tuple[dict[str, Any], dict[str, Any], bool]]:
    rows = json.loads(SLICE.read_text(encoding="utf-8"))["rows"]
    by: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        by[str(r["ref"])].append(r)
    out: list[tuple[dict[str, Any], dict[str, Any], bool]] = []
    for verse in by.values():
        verse.sort(key=lambda r: int(str(r["pos"])))
        idx = [i for i, r in enumerate(verse) if _is_mub(r)]
        for n, i in enumerate(idx):
            r = verse[i]
            lo = idx[n - 1] if n > 0 else -1
            hi = idx[n + 1] if n + 1 < len(idx) else len(verse)
            after = [j for j in range(i + 1, hi) if _is_kh(verse[j])]
            before = [j for j in range(i - 1, lo, -1) if _is_kh(verse[j])]
            first, second = (before, after) if r["role"] == "مبتدأ مؤخر" else (after, before)
            if first:
                out.append((r, verse[first[0]], first is before))
            elif second:
                out.append((r, verse[second[0]], second is before))
    return out


def measure() -> dict[str, Any]:
    rows = json.loads(SLICE.read_text(encoding="utf-8"))["rows"]
    ps = pairs()
    mk: Counter[tuple[str, str]] = Counter()
    kk: Counter[tuple[str, str]] = Counter()
    rutba: Counter[tuple[str, str, bool]] = Counter()
    agreement: Counter[tuple[str, str]] = Counter()
    rab: Counter[str] = Counter()
    for m, k, kf in ps:
        mc, kc = _cells(m, ("DET",)), _cells(k)
        j = Jumla(mc, kc, kf)
        mk[(str(m["decl"]), mubtada_kind(mc))] += 1
        kk[(str(k["phrase"]) or "مفرد", khabar_kind(kc))] += 1
        rutba[(order(j), "الخبرُ أوّلًا" if kf else "المبتدأُ أوّلًا", admissible(j))] += 1
        if str(k["tag"]).startswith(("NOUN_ACTIVE_PART", "NOUN_PASSIVE_PART", "ADJ")) and \
                m["decl"] == "معرب" and not k["phrase"]:
            ms = _cells(m, ("DET",))
            if m["suf"]:
                ms = (*ms, *((a, b) for _, cs in m["suf"] for a, b in cs))
            ks = (*kc, *((a, b) for _, cs in k["suf"] for a, b in cs))
            kind = "مطابق" if agree(ms, ks) else "بالاستثناء" if agree_loose(ms, ks) else "غيره"
            label = f"{gender(ms)} {number(ms)}" + (" (تكسيرٌ محتمل)" if broken_plural(ms) else "")
            agreement[(label, kind)] += 1
        if k["phrase"] == "جملة فعلية":
            ks = (*kc, *((a, b) for _, cs in k["suf"] for a, b in cs))
            rab[rabit(mc, ks)] += 1
    return {"n": len(rows), "pairs": len(ps), "mk": mk, "kk": kk, "rutba": rutba,
            "agree": agreement, "rabit": rab,
            "nakira": sum(1 for m, _, _ in ps if nakira(_cells(m, ("DET",))))}


def _w(w: Word) -> str:
    return "-".join(str(index(c)) for c in w)


def render() -> str:
    m = measure()
    mk: Counter[tuple[str, str]] = m["mk"]
    kk: Counter[tuple[str, str]] = m["kk"]
    rutba: Counter[tuple[str, str, bool]] = m["rutba"]
    ag: Counter[tuple[str, str]] = m["agree"]
    rab: Counter[str] = m["rabit"]
    ok = sum(v for (_, _, a), v in rutba.items() if a)
    lines = [
        "# فهرسُ الجملة الاسميّة على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_jumla_index.py` من `src/slge/jumla.py`؛ لا يُحرَّر باليد. البرهانُ: "
        "`formal/Slge/Jumla.lean`.",
        "",
        "## د٤ الخانة — طرفان مرفوعان، وصورُهما تُقرأ", "",
        "الرفعُ عمليّةٌ واحدةٌ على المبتدأ والخبر (`nominal`): تُقرأ رفعًا لكلّ جذع (`nominal_reads_raf`) "
        "وتحفظ الترخيص (`nominal_licensed`). صورُ المبتدأ: الضميرُ المنفصل من جدوله "
        "(`pronoun_is_damir`)، "
        "والاسمُ الظاهرُ المبنيُّ من جداوله (الإشارة، الموصول، الاستفهام)، والمعربُ من رفعه "
        "(`raf_is_ism`)؛ "
        "والمصدرُ المؤوّل تيارٌ لا كلمة — باسمه. صورُ الخبر (`khabarKind`): شبهُ الجملة من صدرها "
        "(حرفُ جرٍّ "
        "من خانتين، أو متّصلٌ تليه أل، أو جارٌّ وضميرٌ متّصل، أو ظرفٌ من جداوله)، والجملةُ الفعليّةُ من قالب "
        "الفعل، والمفردُ من رفعه (`kinds_witnesses`).",
        "",
        "## د٨ الحدّ — الرتبةُ من الخانات لا من الموضع", "",
        "التقديمُ عمليّةٌ على الزوج (`swap`؛ `swap_swap`)، والرتبةُ دالّةٌ في الخانات (`order`؛ "
        "`order_swap`): "
        "لامُ الابتداء تمسك المبتدأ لكلّ مبتدأ وخبر (`order_lam`)، وصدارةُ الاستفهام والنكرةُ مع "
        "شبه الجملة "
        "والضميرُ العائدُ معها تقدّم الخبر، والخبرُ الفعليُّ وتساوي الرتبة يؤخّرانه، وما سواه جواز. "
        "والموضعُ المخالفُ يُرفض (`admissible`؛ `lam_refuses_khabar_first`). الحصرُ بإلّا وإنّما تيارٌ "
        "(كلمتان) — خارج القارئ باسمه.",
        "",
        "| الجملة | المبتدأ | الخبر | الرتبة |", "|---|---|---|---|",
        *[f"| {n} | `{_w(j.mubtada)}` | `{_w(j.khabar)}` | {order(j)} |"
          for n, j in WITNESSES.items()],
        "",
        "## د١٦ — المطابقةُ عمليّاتٌ، والرابطُ يُقرأ", "",
        "التأنيثُ والتثنيةُ وجمعا السلامة عمليّاتٌ على الخبر تحفظ الترخيص (`ops_licensed`)، "
        "ويقرؤها الجنسُ "
        "والعددُ من اللاحقة بعد إسقاطها (`gender_taNith`، `number_ops`، `gender_jamF`)؛ والمطابقةُ "
        "تساوي "
        "القراءتين، فالعمليّةُ الواحدةُ على الطرفين تُطابق (`agree_ops`؛ `agree_witnesses`). "
        "استثناءُ جمع "
        "غير العاقل (الْجِبَالُ شَاهِقَةٌ) يقرؤه القالبُ احتمالًا (`brokenPlural`) والعقلُ معجم. الرابطُ في "
        "الخبر الجملة: ضميرٌ متّصل، أو اسمُ إشارة، أو إعادةُ اللفظ (`rabit_repeat` لكلّ مبتدأ؛ "
        "`rabit_witnesses`)؛ والعمومُ معنًى.",
        "",
        "## القياس على MASAQ", "",
        f"على {m['n']:,} كلمةً وسمها MASAQ مبتدأً أو خبرًا (بشهادات البوّابة)، منها {m['pairs']:,} "
        "زوجًا "
        f"(مبتدأ، خبر) في نافذة الآية؛ المبتدأُ نكرةٌ بالخانة في {m['nakira']:,} منها.",
        "",
        "### صورُ المبتدأ (وسمُ MASAQ × القارئ)", "",
        "| وسم MASAQ | القارئ | العدد |", "|---|---|---|",
        *[f"| {a} | {b} | {v} |" for (a, b), v in mk.most_common()],
        "",
        "### صورُ الخبر (وسمُ MASAQ × القارئ)", "",
        "| وسم MASAQ | القارئ | العدد |", "|---|---|---|",
        *[f"| {a} | {b} | {v} |" for (a, b), v in kk.most_common()],
        "",
        f"### الرتبة: القارئُ مقابل موضع المصحف — المقبولُ {ok:,} من {m['pairs']:,}", "",
        "| رتبةُ القارئ | موضعُ المصحف | مقبول | العدد |", "|---|---|---|---|",
        *[f"| {a} | {b} | {'نعم' if c else 'لا'} | {v} |" for (a, b, c), v in rutba.most_common()],
        "",
        "ما رُفض: خبرٌ مقدَّمٌ مفردٌ بعد حصرٍ أو استفهامٍ (تيار)، وخبرٌ لا يقرؤه القارئ (المعتلُّ على "
        "القالب، والمضافُ إلى الضمير) — بقيّةٌ مسمّاة.",
        "",
        "### المطابقة (الخبرُ المفردُ المشتقّ مع المبتدأ المعرب)", "",
        "| المبتدأ (جنسٌ عدد) | الحكم | العدد |", "|---|---|---|",
        *[f"| {a} | {b} | {v} |" for (a, b), v in ag.most_common()],
        "",
        "### الرابطُ في الخبر الجملة الفعليّة (أوّلُ كلمةٍ منها)", "",
        "| الرابط | العدد |", "|---|---|",
        *[f"| {a} | {v} |" for a, v in rab.most_common()],
        "",
        "الفاعلُ المستتر (مُحَمَّدٌ دَرَسَ — والفاعلُ هو) لا خانةَ له: الضميرُ المستترُ بقيّةٌ مسمّاة؛ "
        "والظاهرُ من اللواحق.",
        "",
        "## ما لا تقرؤه الخانة — باسمه", "",
        "- المصدرُ المؤوّل مبتدأً (أَنْ تَصُومُوا خَيْرٌ): تيارٌ (أَنْ + فعل).",
        "- الحصرُ بإلّا وإنّما في الرتبة: تيار.",
        "- المتّصلُ الجارُّ على نكرةٍ (بِزَيْدٍ) لا تفرّقه الخانةُ من حرف الأصل (كَرِيم): معجم.",
        "- العقلُ في استثناء المطابقة، والعمومُ رابطًا، والتقديرُ في حذف الخبر (كونٌ عامّ): معلَن.",
        "- التلاؤمُ الأنطولوجيّ (رَجُلٌ طَوِيلٌ لا حَجَرٌ طَوِيلٌ، ولا رَجُلٌ كِتَابَةٌ): معجمٌ ودلالة.",
        "- شريحةُ MASAQ: 192 كلمةً مستبعَدة (غيرُ محاذاة 143، عدٌّ مخالف 16، مرفوضٌ بالاسم 33).",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("JUMLA_INDEX.md غيرُ مطابق؛ شغّل tools/gen_jumla_index.py\n")
            return 1
        sys.stdout.write("JUMLA_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب JUMLA_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
