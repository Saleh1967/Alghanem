"""ولّد `TAWABI_INDEX.md`: فهرسُ التوابع على درجات الترخيص التدريجيّ من `slge.tawabi`، وقياسُ قانون
«الحالة لا العلامة» على شريحة MASAQ المجمَّدة (أزواجُ تابعٍ ومتبوع بشهادات البوّابة)؛ ‎--check‎."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from slge.cells import index
from slge.tawabi import NASAQ, TAWKID, case_class, follows

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "TAWABI_INDEX.md"
SLICE = ROOT / "tests" / "data" / "masaq-tawabi.json"


def measure() -> tuple[Counter[tuple[str, str]], Counter[tuple[str, str, str]], int]:
    """لكلّ بابٍ: (موافقٌ | مخالفٌ | لا تقرؤه الخانة)؛ وتفصيلُ المخالف (حالةُ التابع، حالةُ المتبوع)."""

    rows = json.loads(SLICE.read_text(encoding="utf-8"))
    out: Counter[tuple[str, str]] = Counter()
    detail: Counter[tuple[str, str, str]] = Counter()
    for row in rows:
        t = tuple((c[0], c[1]) for c in row["tabi"]["stem"])
        h = tuple((c[0], c[1]) for c in row["matbu"]["stem"])
        role = row["tabi"]["role"]
        ct, ch = case_class(t), case_class(h)
        if ct.startswith("لا تقرؤه") or ch.startswith("لا تقرؤه"):
            out[(role, "لا تقرؤه الخانة")] += 1
        elif follows(t, h):
            out[(role, "موافق")] += 1
        else:
            out[(role, "مخالف")] += 1
            detail[(role, ct, ch)] += 1
    return out, detail, len(rows)


def render() -> str:
    table, detail, total = measure()
    roles = ("نعت", "اسم معطوف", "بدل", "توكيد")
    lines = [
        "# فهرسُ التوابع على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_tawabi_index.py` من `src/slge/tawabi.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: `formal/Slge/Tawabi.lean`.",
        "",
        "## د١٦ الإعراب من الخانة — الحالةُ لا العلامة", "",
        "القارئُ `caseClass` يردّ العلاماتِ كلَّها إلى الحالة (ضمّة/واو/ألف ⇒ رفع؛ "
        "فتحة/ياء ⇒ نصب أو جرّ؛ كسرة ⇒ جرّ)، فيتبع «الْعَالِمُ» «أَخُوكَ» وإن اختلفت "
        "علامتاهما (`four_markers_one_case`، `follows_khamsa`). والمبرهَنُ لكلّ جذع: رفعُ "
        "الأسماء الخمسة بالواو رفعٌ (`caseClass_khamsa_raf`)، ونصبُها بالألف لا يقرؤه "
        "القارئُ العامّ — مشتركٌ مع المقصور (`khamsa_nasb_unread`)، والعقودُ بالواو رفعٌ "
        "(`caseClass_uqud_raf`)؛ والتبعيّةُ متماثلةٌ وانعكاسيّة (`follows_symm`، "
        "`follows_refl`).", "",
        "## د٨ الحدّ — عطفُ النسق والتوكيدُ المعنويّ", "",
        f"- حروفُ النسق التسعة ({'، '.join(NASAQ)}) كلُّها في جدول أدوات الربط "
        "(`nasaq_in_rawabit`)؛ "
        "الواوُ والفاءُ حرفان متّصلان لا يُفسدان ما بعدهما.",
        "- التوكيدُ المعنويّ: ألفاظٌ تُضاف إلى ضميرٍ (`tawkid_words_licensed`)، والحالةُ من الجذع "
        "قبل الضمير (`tawkid_case`): "
        + "، ".join(f"{n} `{'-'.join(str(index(c)) for c in w)}`" for n, w in TAWKID.items())
        +
        "؛ وعَامَّة (ألفٌ فميمٌ مشدّدة) خارج الترخيص الثنائيّ كحَاجَّ.", "",
        "## القياس على MASAQ — التابعُ يوافق المتبوعَ في الحالة", "",
        f"على {total} زوجًا (تابع، أقربُ اسمٍ سابق) بشهادات البوّابة، الجذعُ قبل الضمير "
        "وبعد السابقة:", "",
        "| الباب | موافق | مخالف | لا تقرؤه الخانة | نسبةُ الموافقة فيما تقرؤه |",
        "|---|---|---|---|---|",
    ]
    for role in roles:
        ok, bad = table[(role, "موافق")], table[(role, "مخالف")]
        un = table[(role, "لا تقرؤه الخانة")]
        pct = f"{100 * ok // (ok + bad)}%" if ok + bad else "—"
        lines.append(f"| {role} | {ok} | {bad} | {un} | {pct} |")
    lines += [
        "",
        "المخالفُ من جهتين مسمّاتين: (١) **اختيارُ المتبوع**: أقربُ اسمٍ سابق ليس المتبوعَ دائمًا (نعتٌ "
        "لمضافٍ إليه مجرور، ومعطوفٌ على بعيد) — فالمتبوعُ قانونُ تيارٍ يُحسم في النظم؛ (٢) **الممنوعُ من "
        "الصرف**: جرُّه بالفتحة يقرؤه القارئُ نصبًا (`Sarf.jarr_eq_nasb`) — وهو أكثرُ "
        "«جرّ مقابل نصب»:", "",
        "| الباب | حالةُ التابع | حالةُ المتبوع المختار | العدد |", "|---|---|---|---|",
        *[f"| {r} | {a} | {b} | {v} |" for (r, a, b), v in detail.most_common(10)],
        "",
        "## ما لا تفرّقه الخانة — باسمه", "",
        "- النعتُ والبدلُ وعطفُ البيان: كلُّها «تابعٌ يوافق في الحالة»؛ الفرقُ دلاليّ.",
        "- المطابقةُ الأربع (التعريف، الجنس، العدد) للنعت الحقيقيّ: قوانينُ تيارٍ تُقاس "
        "زوجًا زوجًا في النظم.",
        "- التوكيدُ اللفظيّ: تكرارُ الشهادة نفسِها — يُقرأ من التيار لا من الخانة.", "",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    text = render()
    if "--check" in argv:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != text:
            print("TAWABI_INDEX.md قديم: شغّل python tools/gen_tawabi_index.py", file=sys.stderr)
            return 1
        print("TAWABI_INDEX.md مطابق")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    print(f"كُتب {TARGET.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
