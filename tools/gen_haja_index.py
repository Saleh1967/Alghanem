"""فهرسُ توقيع الحاجة وقسمة المفرد (HAJA_INDEX.md) من `slge.haja` وجدولِه المرسى، ثمّ على مودَع المصحف.

١. المراسي بأسطرها؛ ٢. حاجاتُ كلّ باب وصدارتُه؛ ٣. أبوابُ الجدول الموحَّد (68)؛ ٤. على مودَع المصحف أوّلًا
(قانونُ القارئ): كلُّ موقعٍ بقراءاته المغلقة (`mughlaq.closed`) ← أبوابُها ← قسمُ المفرد عند النبهانيّ؛ وما
لا قراءةَ
مغلقةً له أقسامُ قراءات جذعه (`jidh`؛ فعلٌ إن كان فيها قالبُ فعل)، وإلّا قارئُ الصيغة (`jiha.sigha`).
مفحوصٌ لا مقيس.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge import haja as H
from slge.haja_table import ANCHORS
from slge.huruf import TABLE as HURUF
from slge.jidh import jidh
from slge.jiha import sigha
from slge.mughlaq import closed
from slge.wujud import FIL, ont_of_reading
from slge.zuruf import set_last

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "HAJA_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]

MUFRAD_AR = {"harf": "حرف", "mudmar": "مضمر (لا يستقلّ)", "fil": "فعل", "ism": "اسم"}
BAB_AR = {"mustaqill": "مستقلّ", "jarr": "الإضافة (الجرّ)", "mushabbaha": "المشبّهة بالفعل",
          "atf": "العطف", "istithna": "الاستثناء", "shart": "الشرط", "nafy": "النفي",
          "amilFil": "الداخلُ على الفعل", "tanbih": "التنبيه", "jawab": "الجواب", "rad": "الردع",
          "istifham": "الاستفهام", "nida": "النداء", "damir": "الضمير", "mawsul": "الموصول",
          "ghayrMusnad": "بلا سند"}
JIHA_AR = {"qabl": "قبل", "bad": "بعد", "ayy": "أيٌّ"}
MA_AR = {"ism": "اسم", "fil": "فعل", "juz": "جزءُ كلام"}


def _forms_and_stream() -> tuple[list[Word], list[int]]:
    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    return [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]], list(d["stream"])


def _open_leaves(w: Word) -> tuple[str, ...]:
    """أقسامُ قراءات الجذع (`jidh`): فعلٌ إن كان في القراءة قالبُ فعل (`wujud.ont_of_reading`)،
    وإلّا اسم؛
    وما لا يقرؤه الجذعُ فعلٌ إن قرأ قارئُ الصيغة هيئتَه، وإلّا اسم."""

    out: list[str] = []
    for rd in jidh(w):
        leaf = "fil" if ont_of_reading(rd) == FIL else "ism"
        if leaf not in out:
            out.append(leaf)
    if out:
        return tuple(out)
    hay = sigha(w) is not None or (bool(w) and sigha(set_last(w, "ضم")) == "مضارع")
    return (H.mufrad_of("mustaqill", hay),)


def babs_of(w: Word) -> tuple[str, ...]:
    """أبوابُ قراءات الصورة المغلقة (`haja.core_babs` لكلّ نواة)، بلا تكرار وبترتيبها."""

    out: list[str] = []
    for m in closed(w):
        for b in H.core_babs(m.core):
            if b not in out:
                out.append(b)
    return tuple(out)


def leaves(w: Word) -> tuple[str, ...]:
    bs = babs_of(w)
    if not bs:
        return _open_leaves(w)
    out: list[str] = []
    for b in bs:
        leaf = H.mufrad_of(b, False) if b != "ghayrMusnad" else "ism"
        if leaf not in out:
            out.append(leaf)
    return tuple(out)


def measure() -> dict[str, Any]:
    forms, stream = _forms_and_stream()
    lv = [leaves(w) for w in forms]
    bb = [babs_of(w) for w in forms]
    order = ("harf", "mudmar", "fil", "ism")
    keys = ["+".join(sorted(x, key=order.index)) for x in lv]
    form_leaf: Counter[str] = Counter(keys)
    pos_leaf: Counter[str] = Counter(keys[i] for i in stream)
    pos_bab: Counter[str] = Counter(b for i in stream for b in bb[i])
    multi_bab = sum(1 for i in stream if len(bb[i]) > 1)
    return {"forms": len(forms), "positions": len(stream),
            "form_leaf": dict(sorted(form_leaf.items())),
            "pos_leaf": dict(sorted(pos_leaf.items())),
            "pos_bab": dict(sorted(pos_bab.items())), "multi_bab_positions": multi_bab}


def _need(h: H.Haja) -> str:
    j, m, ittisal, key = h
    return f"{JIHA_AR[j]} {MA_AR[m]}" + (" متّصلًا" if ittisal else "") + f" (`{key}`)"


def render(m: dict[str, Any]) -> str:
    out = ["# فهرسُ توقيع الحاجة — ما يحتاجه المغلقُ ليتمّ، وقسمةُ المفرد عند النبهانيّ", "",
           "مولَّدٌ بـ`python tools/gen_haja_index.py` من `src/slge/haja.py` وجدولِه المرسى "
           "(`tools/deposit_haja.py`)؛ لا يُحرَّر باليد. البرهانُ `formal/Slge/Haja.lean` (ADR ٥٦):"
           " الحرفُ له "
           "حاجة (`harf_has_need`)، والمستقلُّ لا (`mustaqill_none`)، والصدارةُ للشرط والاستفهام"
           " (`sadr_exactly`)، "
           "وصنفُ الجدول الموحَّد يوافق الحاجة إلّا مسمّاةً (`class_agrees`)، وقسمةُ المفرد تامّة"
           " (`mufrad_partition`).",
           "", "## ١. المراسي", "", "| المفتاح | الكتاب | السطر | ما يثبته |", "|---|---|---|---|"]
    out += [f"| `{k}` | {b} | {ln} | {n} |" for k, b, n, ln, _ in ANCHORS]
    out += ["", "## ٢. حاجاتُ كلّ باب", "", "| الباب | حرفيّ | صدارة | الحاجات |", "|---|---|---|---|"]
    for b in H.BAB_ALL:
        needs = "؛ ".join(_need(h) for h in H.NEEDS[b]) or "—"
        harf = "نعم" if b in H.HARF_BABS else ""
        sadr = "نعم" if b in H.SADR else ""
        out.append(f"| {BAB_AR[b]} | {harf} | {sadr} | {needs} |")
    out += ["", "## ٣. أبوابُ الجدول الموحَّد", "", "| الباب | الحروف |", "|---|---|"]
    for b in H.BAB_ALL:
        names = [h.name for i, h in enumerate(HURUF) if H.bab_of(i) == b]
        if names:
            out.append(f"| {BAB_AR[b]} | {'، '.join(names)} |")
    out += ["", "## ٤. على مودَع المصحف — قسمةُ المفرد (مفحوصٌ لا مقيس)", "",
            f"{m['forms']:,} صورةً و{m['positions']:,} موقعًا. القسمُ من القراءات المغلقة؛ وما لا"
            f" قراءةَ مغلقةً له "
            "فمن قراءات جذعه (فعلٌ إن كان فيها قالبُ فعل)؛ و«+» صورةٌ لها أكثرُ من قسم (اشتراكٌ في"
            " الدالّ).", "",
            "| القسم | الصور | المواقع |", "|---|---|---|"]
    keys = sorted(set(m["form_leaf"]) | set(m["pos_leaf"]))
    for k in keys:
        name = " + ".join(MUFRAD_AR[x] for x in k.split("+"))
        out.append(f"| {name} | {m['form_leaf'].get(k, 0):,} | {m['pos_leaf'].get(k, 0):,} |")
    out += ["", "| الباب | المواقع |", "|---|---|"]
    out += [f"| {BAB_AR[b]} | {n:,} |" for b, n in m["pos_bab"].items()]
    out += ["", f"مواقعُ لصورتها أكثرُ من باب: {m['multi_bab_positions']:,} — الخانةُ لا تحسم الباب "
            "(`la_four`: لَا في أربعة أبواب)، والحسمُ للجوار.", "",
            "## ما ليس هنا — باسمه", "",
            "- `MAIYYA_NEED_UNSOURCED`، `LAT_UNSOURCED`: واوُ المعيّة الاسميّة ولاتَ بلا مرساةٍ في"
            " المختومَين هنا.",
            "- `ISHARA_NEED_UNSOURCED`: الإشارةُ وأدواتُ الربط والمركَّبات «بلا سند» في التوقيع.",
            "- `FIL_BY_TEMPLATE_ONLY`: الفعلُ بقالب قراءة الجذع؛ ما لا يقرؤه الجذعُ ولا قارئُ الصيغة"
            " يُعدّ اسمًا،"
            " فعمودُ الاسم حدٌّ أعلى وعمودُ الفعل حدٌّ أدنى.",
            "- الحاجةُ هنا قيدٌ على الباب؛ قضاؤها في التيّار (الصدارةُ والإغلاقُ والوصل) في ADR ٥٧.", ""]
    return "\n".join(out)


def main(argv: list[str]) -> int:
    text = render(measure())
    if "--check" in argv:
        ok = TARGET.read_text(encoding="utf-8") == text
        sys.stdout.write("HAJA_INDEX.md مطابق\n" if ok else "HAJA_INDEX.md غيرُ مطابق\n")
        return 0 if ok else 1
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب HAJA_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
