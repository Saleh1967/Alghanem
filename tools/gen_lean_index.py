"""ولّد `LEAN_INDEX.md`: فهرسُ مبرهنات Lean (الـ116 في الغانم بإيداعه المثبَّت، وSLGE) مرتَّبًا على
درجات الترخيص التدريجيّ للبرهان؛ و‎--check‎ يفشل إن كان الملفُّ قديمًا.

المصادر: ملفّاتُ `.lean` نفسُها (اسمُ المبرهنة وسطرُها الأوّل من تعليقها)، و`Audit.lean` (أهي مدقَّقة؟)،
و`out/axioms.txt` (مسلّماتُها كما طبعها Lean). لا يُكتب هنا اسمٌ ليس في الشجرة.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORMAL = ROOT / "formal"
A116 = FORMAL / ".lake" / "packages" / "a116" / "formal" / "a116" / "A116"
SLGE = FORMAL / "Slge"
TARGET = ROOT / "LEAN_INDEX.md"

# درجاتُ الترخيص التدريجيّ: من البايت إلى الجواب. كلُّ درجةٍ تستهلك ما قبلها ولا تقفز.
LADDER: tuple[tuple[str, str, tuple[tuple[str, str], ...]], ...] = (
    ("١", "البايتُ والنقطة: UTF-8 تقابلٌ ذاتيُّ الحدّ", (("A116", "Unicode"),)),
    ("٢", "الحدّ: ابتداءٌ ووصلٌ ووقف", (("A116", "Boundary"),)),
    ("٣", "الخانة: 29 حاملًا × 4 حالات = 116", (("A116", "Cells"),)),
    ("٤", "الترخيصُ الثنائيّ: لا ابتداءَ بساكن ولا تجاورَ ساكنين", (("A116", "Model"),)),
    ("٥", "العدّ: ‎U(n+2) = 87U(n+1) + 87·29·U(n)‎", (("A116", "Count"),)),
    ("٦", "الطيُّ والعدد: المرخَّصةُ ↔ عددُها", (("A116", "Fold"), ("A116", "Numbering"))),
    ("٧", "الليفُ والبقيّة: الرسمُ ↔ الذرّات، وقواعدُ الطبعة تُردّ بعينها",
     (("A116", "Fiber"), ("A116", "Residue"))),
    ("٨", "التقطيعُ الثلاثيّ: cv/v/c، المدّ، الوقف، الوصل",
     (("A116", "Stages"), ("A116", "Ternary"), ("A116", "Pause"), ("A116", "Junction"))),
    ("٩", "الإعلالُ والهمزة: تعديلاتٌ على الخانات تُردّ، والكرسيُّ دالّةٌ في السياق",
     (("A116", "Ilal"), ("A116", "Hamza"))),
    ("١٠", "الاشتقاقُ والاسترجاع: الأصلُ يُستردّ بالقالب، والصيغةُ وحدَها لا تعيّنه",
     (("A116", "Ishtiqaq"), ("A116", "Derivation"), ("A116", "Recovery"), ("A116", "Field112"),
      ("A116", "Ladder"))),
    ("١١", "الجسرُ إلى SLGE: ترميزان، برهانٌ واحد",
     (("Slge", "Bridge"), ("Slge", "Consistency"), ("Slge", "Rasm"))),
    ("١٢", "التسلسل: النصُّ تيارُ شهاداتٍ ذاتيُّ الحدّ", (("Slge", "Sequence"),)),
    ("١٣", "المنح: لا اسمَ قبل قبضته", (("Slge", "Grant"),)),
    ("١٤", "الأقانيم: الصنفُ عضويّةٌ قابلةٌ للفصل؛ وأسماءُ الإشارة نواةٌ بثلاث عمليّات",
     (("Slge", "Categories"), ("Slge", "Ishara"), ("Slge", "Marifa"))),
    ("١٥", "الوزنُ وشبكتُه: القالبُ يُرخَّص مرّةً لكلّ الأصول، والجبرُ يحفظ الأصل",
     (("Slge", "Wazn"), ("Slge", "Shabaka"))),
    ("١٦", "الإعرابُ بالحروف وبالنون والضمائرُ: الأسماءُ الخمسة والأفعالُ الخمسة ونا والتاء",
     (("Slge", "Khamsa"), ("Slge", "Afal"), ("Slge", "Damair"), ("Slge", "Nida"),
      ("Slge", "Zuruf"), ("Slge", "Zaman"), ("Slge", "Adad"), ("Slge", "Sarf"))),
    ("١٧", "أدواتُ الربط والاستفهام: الخانةُ فالحدُّ فالعمل، والمعنى معلَن",
     (("Slge", "Rawabit"), ("Slge", "Istifham"))),
    ("١٨", "التوابعُ والنواسخُ والجزم: الحالةُ لا العلامة، وأبوابٌ عمليّتان، وعلاماتٌ ثلاثٌ عمليّاتٌ ثلاث",
     (("Slge", "Tawabi"), ("Slge", "Nawasikh"), ("Slge", "Jazm"), ("Slge", "Mansubat"),
      ("Slge", "Majrurat"), ("Slge", "Wasl"), ("Slge", "Ism"), ("Slge", "Fil"),
      ("Slge", "Huruf"), ("Slge", "Jumla"), ("Slge", "Filiyya"),
      ("Slge", "Shibh"), ("Slge", "Nisab"), ("Slge", "Talil"), ("Slge", "Maqam"),
      ("Slge", "Jiha"), ("Slge", "Naat"), ("Slge", "Uslub"), ("Slge", "Talab"),
      ("Slge", "Kulli"), ("Slge", "Wad"), ("Slge", "Tabayun"), ("Slge", "Madd"),
      ("Slge", "Ilal"), ("Slge", "Jidh"), ("Slge", "MaqayisTable"), ("Slge", "Maqayis"))),
    ("١٩", "المعرفةُ والترجيح: الإنتاجُ والتعارضُ وقطعيُّ الدلالة",
     (("Slge", "Ghazali"), ("Slge", "Rank"))),
)

THEOREM = re.compile(r"^theorem\s+([A-Za-z0-9_.']+)")


def theorems(path: Path) -> list[tuple[str, str]]:
    """(الاسم، أوّلُ سطرٍ من تعليقه) لكلّ `theorem` في الملفّ، بترتيبه."""

    out: list[tuple[str, str]] = []
    doc = ""
    pending: list[str] = []
    in_doc = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("/--"):
            in_doc = True
            pending = [line[3:].strip().rstrip("-/").strip()]
            if line.rstrip().endswith("-/"):
                in_doc = False
            continue
        if in_doc:
            if line.rstrip().endswith("-/"):
                in_doc = False
            else:
                pending.append(line.strip())
            continue
        m = THEOREM.match(line)
        if m:
            doc = " ".join(p for p in pending if p)[:120]
            out.append((m.group(1), doc))
        if line.strip() and not line.startswith("theorem") and not line.startswith(" "):
            pending = []
    return out


def namespace(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("namespace "):
            return line.split()[1]
    return ""


def audited() -> set[str]:
    text = (FORMAL / "Audit.lean").read_text(encoding="utf-8")
    return set(re.findall(r"^#print axioms\s+(\S+)", text, re.M))


def axioms() -> dict[str, str]:
    out: dict[str, str] = {}
    path = FORMAL / "out" / "axioms.txt"
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"'([^']+)' (?:depends on axioms: \[(.*)\]|does not depend on any axioms)",
                     line)
        if m:
            out[m.group(1)] = m.group(2) or "لا مسلّمات"
    return out


def render() -> str:
    aud, ax = audited(), axioms()
    covered = {f"{p}/{m}" for _, _, fs in LADDER for p, m in fs}
    on_disk = {f"A116/{f.stem}" for f in A116.glob("*.lean")} | {
        f"Slge/{f.stem}" for f in SLGE.glob("*.lean")}
    if covered != on_disk:
        raise SystemExit(f"LADDER_DOES_NOT_COVER_TREE:{sorted(covered ^ on_disk)}")
    total = checked = 0
    lines = [
        "# فهرسُ مبرهنات Lean على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_lean_index.py` من ملفّات `.lean` و`Audit.lean` و`out/axioms.txt`؛ "
        "لا يُحرَّر باليد. الـ116 من الغانم بإيداعه المثبَّت في `formal/lakefile.toml`.",
        "",
        "كلُّ درجةٍ تستهلك ما قبلها: لا تدخل الكلمةُ درجةً قبل أن تُرخَّص في التي تحتها. "
        "«مدقَّق» = في `Audit.lean` وطُبعت مسلّماتُه؛ وما ليس مدقَّقًا مبرهَنٌ في Lean لكن لم يُطبع "
        "سندُه بعدُ فلا يُستشهد به في `status.py`.",
        "",
    ]
    for num, title, files in LADDER:
        lines += [f"## الدرجة {num} — {title}", ""]
        for pkg, mod in files:
            path = (A116 if pkg == "A116" else SLGE) / f"{mod}.lean"
            if not path.exists():
                raise SystemExit(f"MISSING_LEAN_FILE:{path}")
            ns = namespace(path)
            ths = theorems(path)
            lines += [f"### `{pkg}/{mod}.lean` — {len(ths)} مبرهنة (`{ns}`)", "",
                      "| المبرهنة | ما تقول | التدقيق | المسلّمات |", "|---|---|---|---|"]
            for name, doc in ths:
                full = f"{ns}.{name}" if ns and not name.startswith(ns) else name
                total += 1
                is_aud = full in aud
                checked += is_aud
                lines.append(f"| `{name}` | {doc or '—'} | {'مدقَّق' if is_aud else '—'} | "
                             f"{ax.get(full, '—') if is_aud else '—'} |")
            lines.append("")
    lines[4:4] = [f"**{total} مبرهنة، منها {checked} مدقَّقةُ المسلّمات.**", ""]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    text = render()
    if "--check" in argv:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != text:
            print("LEAN_INDEX.md قديم: شغّل python tools/gen_lean_index.py", file=sys.stderr)
            return 1
        print("LEAN_INDEX.md مطابق")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    print(f"كُتب {TARGET.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
