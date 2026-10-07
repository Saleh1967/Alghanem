"""إيداعُ معاني الحروف من مبحث «الحرف» في الشخصيّة الإسلاميّة ج3 (أصول الفقه): كلُّ حرفٍ وما
ذُكر له من معانٍ **بترتيب ذكرها في المصدر**، نقلًا لا اختيارًا.

مرحلتان:
- `python tools/deposit_maani.py --extract <ج3.txt>`: يقرأ النصَّ المحوَّل، يقتطع المبحثَ بين
  عنوانَي «الحرف» و«المنطوق والمفهوم»، ويقسمه فقراتٍ؛ كلُّ فقرةٍ تبدأ بـ«حرف» مدخلٌ. المعاني تُلتقط
  **بالمطابقة الحرفيّة** لمفردات معجمٍ مسمًّى (`SENSES`: الاسمُ العربيّ كما يرد في النصّ بسوابقه)
  بترتيب مواضعها؛ ما بقي في المدخل من عبارة «لـ… كقول» لم تلتقطها المفرداتُ يُسجَّل `unmatched`
  ولا يُخمَّن. يكتب المودَعَ `tests/data/nabhani-huruf.json` (وفيه بصمةُ المصدر).
- بلا وسيط: يقرأ المودَعَ (بصمتُه مثبَّتة) ويكتب `formal/Slge/MaaniTable.lean`
  و`src/slge/maani_table.py`؛ وبـ`--check` يقارنهما بما يولَّد الآن.

الحروفُ تُربط بفهارس `Huruf.table` (68) بالاسم والصنف (الإضافة/العطف/النفي…)؛ ما ليس في الجدول
(حروفُ الجواب…) يُسجَّل `skipped` باسمه.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DEPOSIT = ROOT / "tests" / "data" / "nabhani-huruf.json"
LEAN = ROOT / "formal" / "Slge" / "MaaniTable.lean"
PY = ROOT / "src" / "slge" / "maani_table.py"
SHA = "5f6f3d64736e981a867524d7478ab1773670033d2a229f8aefcbbaf4905f4766"

# المعجمُ المسمّى: (اسمُ Lean، الاسمُ العربيّ، صورُه في النصّ بسوابقها). الأطولُ أوّلًا عند التداخل.
SENSES: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("ibtidaGhayaZaman", "ابتداء الغاية في الزمان", ("لابتداء الغاية في الزمان",)),
    ("ibtidaGhaya", "ابتداء الغاية", ("لابتداء الغاية",)),
    ("intihaGhaya", "انتهاء الغاية", ("لانتهاء الغاية",)),
    ("tabid", "التبعيض", ("للتبعيض",)),
    ("bayanJins", "بيان الجنس", ("لبيان الجنس",)),
    ("zaida", "زائدة", ("زائدة",)),
    ("maa", "بمعنى مع", ("بمعنى مع",)),
    ("zarfiyya", "الظرفية", ("للظرفية",)),
    ("ala", "بمعنى على", ("بمعنى على",)),
    ("tajawwuz", "التجوّز", ("يتجوز بها",)),
    ("ilsaq", "الإلصاق", ("للإلصاق",)),
    ("istiana", "الاستعانة", ("للاستعانة",)),
    ("musahaba", "المصاحبة", ("والمصاحبة",)),
    ("minAjl", "بمعنى من أجل", ("بمعنى من أجل",)),
    ("fi", "بمعنى في", ("بمعنى في",)),
    ("ikhtisas", "الاختصاص", ("للاختصاص",)),
    ("taqlil", "التقليل", ("للتقليل",)),
    ("qasam", "القسم", ("مبدلة عن باء الإلصاق", "مبدلة من «الواو»")),
    ("istila", "الاستعلاء", ("للاستعلاء",)),
    ("mubaada", "المباعدة", ("للمباعدة",)),
    ("tashbih", "التشبيه", ("للتشبيه",)),
    ("mutlaqJam", "مطلق الجمع", ("لمطلق الجمع",)),
    ("tartibTaqib", "الترتيب والتعقيب", ("الترتيب والتعقيب",)),
    ("tartibTarakhi", "الترتيب والتراخي", ("الترتيب والتراخي",)),
    ("juzMinMatuf", "المعطوف جزء من المعطوف عليه", ("المعطوف جزء من المعطوف عليه",)),
    ("tartib", "الترتيب", ("تفيد الترتيب،",)),
    ("taliqBiAhad", "تعليق الحكم بأحد المذكورين", ("تعليق الحكم بأحد المذكورين",)),
    ("shakk", "الشك", ("للشك",)),
    ("takhyir", "التخيير", ("للتخيير",)),
    ("ibaha", "الإباحة", ("للإباحة",)),
    ("mukhalafa", "مخالفة المعطوف عليه في حكمه", ("مخالف للمعطوف عليه",)),
    ("nafyHal", "نفي الحال", ("لنفي الحال",)),
    ("nafyMustaqbal", "نفي المستقبل", ("لنفي المستقبل",)),
    ("nahy", "النهي", ("نهياً",)),
    ("dua", "الدعاء", ("أو دعاء",)),
    ("qalbMadi", "قلب المضارع إلى الماضي", ("لقلب المضارع إلى الماضي",)),
    ("takidMustaqbal", "تأكيد المستقبل", ("لتأكيد المستقبل",)),
)

GROUPS = {"الأول": "الإضافة", "الثاني": "المشبهة بالفعل", "الثالث": "العطف", "الرابع": "النفي",
          "الخامس": "التنبيه", "السادس": "النداء", "السابع": "الجواب", "الثامن": "الاستثناء وغيرها",
          "التاسع": "اللامات", "العاشر": "تاء التأنيث", "الحادي عشر": "التنوين والنون"}

# (الصنف، الاسمُ في النصّ) ← فهرسُ `Huruf.table`
INDEX: dict[tuple[str, str], int] = {
    ("الإضافة", "الباء"): 0, ("الإضافة", "اللام"): 1, ("الإضافة", "الكاف"): 2,
    ("الإضافة", "واو القسم"): 3, ("الإضافة", "تاء القسم"): 4, ("الإضافة", "من"): 5,
    ("الإضافة", "إلى"): 6, ("الإضافة", "عن"): 7, ("الإضافة", "على"): 8, ("الإضافة", "في"): 9,
    ("الإضافة", "حتى"): 10, ("الإضافة", "مذ"): 11, ("الإضافة", "منذ"): 12, ("الإضافة", "رب"): 16,
    ("العطف", "الواو"): 49, ("العطف", "الفاء"): 50, ("العطف", "ثم"): 51, ("العطف", "حتى"): 52,
    ("العطف", "أو"): 53, ("العطف", "أم"): 54, ("العطف", "لا"): 55, ("العطف", "بل"): 56,
    ("العطف", "لكن"): 57,
    ("النفي", "ما"): 60, ("النفي", "لا"): 61, ("النفي", "لم"): 62, ("النفي", "لما"): 40,
    ("النفي", "لن"): 63, ("النفي", "إن"): 64,
}

TATWEEL = "ـ"
EXAMPLE = re.compile(r"(?:كقولك|كقوله تعالى|كقولهم|كقوله|نقول|تقول|في قولك)\s*:?\s*([^،.]+)")
LAM_PHRASE = re.compile(
    r"(?:تكون|ترد|يكونان|و)(?:لل|ل)([ء-ي]+(?: [ء-ي]+)?)(?= كقول| مثل| نقول| تقول|،)")
NOT_LAM = ("لا", "لم", "لن", "لكن", "لما")
CUT_MARKERS = ("وقد يلتبس",)
"""ما بعد هذه العبارات في المدخل مقارنةٌ لا تعدادُ معانٍ (الباء/في)؛ لا تُلتقط منه معانٍ."""


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace(TATWEEL, "")).strip()


def extract(text: str) -> dict[str, Any]:
    a = text.index("\nالحـرف\n")
    b = text.index("المنطـوق والمفهـوم")
    section = text[a:b]
    paras = [_norm(p) for p in re.split(r"\n\s*\n", section) if p.strip()]
    group = ""
    entries: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for p in paras:
        m = re.match(r"^(الأول|الثاني|الثالث|الرابع|الخامس|السادس|السابع|الثامن|التاسع|العاشر"
                     r"|الحادي عشر):", p)
        if m:
            group = GROUPS[m.group(1)]
            continue
        if not p.startswith("«"):
            continue
        lead = re.match(r"^(?:«[^»]+»\s*(?:و|،)?\s*)+", p)
        leading = re.findall(r"«([^»]+)»", lead.group(0) if lead else p[:40])
        # مدخلٌ ثانٍ داخل الفقرة: «و«اسم»» لاسمٍ في الجدول غيرِ الأسماء الصدريّة (واو القسم / تاء القسم)
        body = p
        for cm in CUT_MARKERS:
            if cm in body:
                body = body[:body.index(cm)]
        parts: list[tuple[list[str], str]] = [(leading, body)]
        for mm in re.finditer(r" و«([^»]+)» ", body):
            n = mm.group(1)
            if (group, n) in INDEX and n not in leading:
                head, tail = body[:mm.start()], body[mm.start() + 1:]
                parts = [(leading, head), ([n], tail)]
                break
        for names, text in parts:
            body = text
            found: list[tuple[int, str]] = []
            consumed: list[tuple[int, int]] = []
            for lean, _ar, variants in SENSES:
                for v in variants:
                    for mm in re.finditer(re.escape(v), body):
                        span = (mm.start(), mm.end())
                        if any(s <= span[0] < e for s, e in consumed):
                            continue
                        consumed.append(span)
                        found.append((span[0], lean))
            seen: list[str] = []
            for _, lean in sorted(found):
                if lean not in seen:
                    seen.append(lean)
            unmatched = []
            for mm in LAM_PHRASE.finditer(body):
                u = mm.group(1)
                wm = re.search(r"(?:لل|ل)[ء-ي]+", mm.group(0))
                word = wm.group(0) if wm else ""
                if word in NOT_LAM or any(u in v for _, _, vs in SENSES for v in vs):
                    continue
                unmatched.append(u)
            row = {"group": group, "names": names, "senses": seen,
                   "examples": EXAMPLE.findall(text), "unmatched": unmatched, "raw": text}
            idx = [INDEX.get((group, n)) for n in names]
            if all(i is None for i in idx):
                skipped.append({**row, "reason": "OUTSIDE_HURUF_TABLE"})
                continue
            row["huruf"] = [i for i in idx if i is not None]
            entries.append(row)
    return {"source": "الشخصيّة الإسلاميّة ج3 — مبحث الحرف (بين عنوانَي «الحرف» و«المنطوق والمفهوم»)",
            "source_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "section_sha256": hashlib.sha256(section.encode("utf-8")).hexdigest(),
            "senses": [{"lean": ln, "name": n} for ln, n, _ in SENSES],
            "entries": entries, "skipped": skipped}


def load() -> dict[str, Any]:
    raw = DEPOSIT.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != SHA:
        raise SystemExit(f"DEPOSIT_SHA_MISMATCH {sha}")
    dep: dict[str, Any] = json.loads(raw.decode("utf-8"))
    return dep


def table(dep: dict[str, Any]) -> list[tuple[int, list[str]]]:
    out: dict[int, list[str]] = {}
    for e in dep["entries"]:
        for h in e["huruf"]:
            out.setdefault(h, [])
            for s in e["senses"]:
                if s not in out[h]:
                    out[h].append(s)
    return sorted(out.items())


def render_lean(dep: dict[str, Any], rows: list[tuple[int, list[str]]]) -> str:
    names = [s["lean"] for s in dep["senses"]]
    lines = [
        "import Slge.Bridge", "",
        "/-! معاني الحروف كما ذكرها مبحثُ «الحرف» في الشخصيّة الإسلاميّة ج3، بترتيب ذكرها: مولَّدٌ من",
        f"`tests/data/nabhani-huruf.json` (بصمةُ المودَع في `tools/deposit_maani.py`؛ بصمةُ المصدر "
        f"`{dep['source_sha256'][:16]}…`)؛ لا يُحرَّر باليد.",
        "الفهرسُ الأوّل فهرسُ الحرف في `Huruf.table`. -/", "",
        "namespace Slge.Maani", "",
        "inductive Sense where",
    ]
    for i in range(0, len(names), 6):
        lines.append("  | " + " | ".join(names[i:i + 6]))
    lines += ["  deriving DecidableEq, Repr", "",
              f"/-- {len(rows)} حرفًا من `Huruf.table` ومعانيه بترتيب المصدر. -/",
              "def table : List (Nat × List Sense) := ["]
    for i, (h, ss) in enumerate(rows):
        tail = "," if i + 1 < len(rows) else ""
        lines.append(f"  ({h}, [" + ", ".join("." + s for s in ss) + "])" + tail)
    lines += ["]", "", f"theorem table_length : table.length = {len(rows)} := by rfl", "",
              "end Slge.Maani", ""]
    return "\n".join(lines)


def render_py(dep: dict[str, Any], rows: list[tuple[int, list[str]]]) -> str:
    names = [s["lean"] for s in dep["senses"]]
    ar = [s["name"] for s in dep["senses"]]
    lines = [
        '"""معاني الحروف بترتيب المصدر — مولَّدٌ من `tests/data/nabhani-huruf.json`',
        'بـ`tools/deposit_maani.py`؛ لا يُحرَّر باليد."""',
        "", "from __future__ import annotations", "", "from typing import Final", "",
        "SENSES: Final[tuple[str, ...]] = (",
    ]
    for i in range(0, len(ar), 5):
        lines.append("    " + ", ".join(f'"{x}"' for x in ar[i:i + 5]) + ",")
    lines += [")", "", "TABLE: Final[dict[int, tuple[int, ...]]] = {"]
    for h, ss in rows:
        lines.append(f"    {h}: (" + ", ".join(str(names.index(s)) for s in ss) + ",),")
    lines += ["}", ""]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if "--extract" in argv:
        src = Path(argv[argv.index("--extract") + 1])
        dep = extract(src.read_text(encoding="utf-8"))
        DEPOSIT.write_text(json.dumps(dep, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        sys.stdout.write(f"{len(dep['entries'])} مدخلًا، {len(dep['skipped'])} خارج الجدول؛ "
                         f"غيرُ ملتقَط: {sum(len(e['unmatched']) for e in dep['entries'])}\n"
                         f"بصمةُ المودَع: {hashlib.sha256(DEPOSIT.read_bytes()).hexdigest()}\n")
        return 0
    dep = load()
    rows = table(dep)
    lean, py = render_lean(dep, rows), render_py(dep, rows)
    if "--check" in argv:
        ok = LEAN.read_text(encoding="utf-8") == lean and PY.read_text(encoding="utf-8") == py
        sys.stdout.write("جدولا المعاني مطابقان للمودَع\n" if ok else "جدولا المعاني غيرُ مطابقين\n")
        return 0 if ok else 1
    LEAN.write_text(lean, encoding="utf-8")
    PY.write_text(py, encoding="utf-8")
    sys.stdout.write(f"{len(rows)} حرفًا؛ متعدّدُ المعاني {sum(1 for _, s in rows if len(s) > 1)}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
