"""سجلُّ الرفض (REFUSALS.md): كلُّ اسمِ رفضٍ تُطلقه البوّابةُ له مرساةٌ أو هو دَينٌ معلَنٌ باسمه. «الرفضُ مسمًّى ولا
يُخمَّن شيء» شعارٌ ما لم يُفحص: الاسمُ الذي يرفض به الجسرُ أو الترخيصُ كلمةً حكمٌ لغويٌّ يعمل على المدوّنة،
فإمّا أن يكون له موضعُ تعريف — مبرهنةٌ أو تعريفٌ في `formal/a116/A116/*.lean` باسمه، أو مدخلٌ في
`GLOSSARY.md` (الأقوالُ في ADR سردٌ لا مرساة) — وإمّا أن يُعلَن دَينًا هنا (`DECLARED`) بصنفه وشرطِ
سداده. هذه الأداةُ تمشي على `gate/*.py` بشجرة التركيب (لا بالنصّ) فتجمع كلَّ اسمٍ يمرّ في
`_defer("…")`، `_reject("…")`، `Refusal(…, ("…",))`، و`{"reason": "…"}`، وتكتب السجلَّ، و`--check`
يُسقط البناء على: اسمٍ بلا مرساةٍ ولا إعلان (`REFUSAL_WITHOUT_ANCHOR`)، ودَينٍ معلَنٍ صار له مرساةٌ أو
لم يعد يُطلَق (`STALE_DECLARED_REFUSAL`)، وسجلٍّ غيرِ مطابق. الاكتشافُ الذي أوجب الأداة:
`BARE_ALIF_OWN_MARK_NOT_LICENSED` كان سياسةً في بايثون بلا تعريفٍ في Lean حتى `A116.Alif`
(2026-10-09).
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "REFUSALS.md"
GATE = ROOT / "gate"
LEAN = ROOT / "formal" / "a116" / "A116"
GLOSSARY = ROOT / "GLOSSARY.md"
EMITTERS = ("_defer", "_reject")

KINDS = ("واجهة", "رسم", "همزة", "ترخيص", "حدّ", "استرجاع")
"""أصنافُ الرفض: واجهةٌ (بايتاتٌ ومجالٌ وسياقٌ معلَن)، رسمٌ (علاماتٌ متعارضةٌ أو ناقصة)، همزةٌ (الوصلُ
والقطعُ والألف)، ترخيصٌ (التقطيع)، حدٌّ (الوصلُ والوقف)، استرجاعٌ (الشهادةُ والليف)."""

DECLARED: dict[str, tuple[str, str]] = {
    # — واجهة: ليست حكمًا لغويًّا؛ مرساتُها بروتوكولُ الجسر (A116-CANONICAL-TXT-1.1) في
    #   `gate/bridge.py` —
    "NOT_UTF8": ("واجهة",
                 "بايتاتٌ ليست UTF-8؛ `A116.Unicode` يبرهن التقابلَ على المجال لا على ما خارجه"),
    "NOT_ONE_TOKEN": ("واجهة", "المدخلُ كلمةٌ واحدة بلا فراغ — قيدُ الواجهة لا اللغة"),
    "NOT_ONE_EXACT_WORD_SPAN": ("واجهة", "النصُّ أكثرُ من كلمةٍ أو لا كلمةَ فيه — قيدُ الواجهة"),
    "NO_ARABIC_WORD_IN_SOURCE": ("واجهة", "لا حرفَ عربيًّا في المدخل"),
    "A_MULTI_WORD_TEXT_NEEDS_A_BOUNDARY_INTERFACE": ("واجهة",
                                                      "عدّةُ كلماتٍ تدخل بحدودها لا دفعةً واحدة"),
    "ANNOTATION_CONTRADICTS_AN_EXPLICIT_MARK": ("واجهة", "الحاشيةُ لا تُبطل علامةً مكتوبة"),
    "LEFT_CONTEXT_HAS_NO_CERTIFICATE": ("واجهة", "الجارُ الأيسر لا شهادةَ له فلا وصلَ يُحكم"),
    "ATOM_OUTSIDE_A116": ("واجهة", "ذرّةٌ ليست من الـ116 — `A116.cells_length` يحصر الشبكة"),
    "UNSUPPORTED_LETTER": ("واجهة", "حرفٌ خارج الحوامل الـ29 المعلَنة في الجسر"),
    "UNSUPPORTED_MARK": ("واجهة", "علامةٌ خارج علامات البروتوكول"),
    # — رسم: تعارضُ العلامات أو نقصُها؛ لا يُخمَّن. شرطُ السداد: تعريفُ «العلامةِ المقروءة» في Lean —
    "CONFLICTING_MARKS": ("رسم", "علامتان متعارضتان على حرفٍ واحد — لا تُرجَّح إحداهما"),
    "SHADDA_WITH_SUKUN": ("رسم", "شدّةٌ مع سكون — تركيبٌ لا خانةَ له"),
    "VOWEL_WITH_SUKUN": ("رسم", "حركةٌ مع سكونٍ على حرفٍ واحد"),
    "TANWIN_WITH_ANOTHER_HARAKA": ("رسم", "تنوينٌ مع حركةٍ أخرى"),
    "HARAKA_IS_ABSENT_AND_IS_NEVER_GUESSED": ("رسم",
                                              "حرفٌ بلا حركةٍ في غير مواضع الإسقاط المسمّاة "
                                              "(`residue`)"),
    "FINAL_HARAKA_IS_ABSENT": ("رسم", "آخرُ الكلمة بلا حركة؛ الوقفُ يُعلَن بالحدّ لا يُخمَّن من الرسم"),
    "TA_MARBUTA_IS_NOT_FINAL": ("رسم", "تاءٌ مربوطة في غير الآخر"),
    "UNVOCALIZED_WORD_IS_NEVER_GUESSED": ("رسم",
                                          "كلمةٌ بلا أيّ علامة (الحروفُ المقطّعة) لا تُشكَّل تخمينًا"),
    # — همزة: ما لم يُحسم في `A116.Hamza`/`Boundary` بعدُ (حركةُ الوصل من الثالث مرساتُها
    #   `Boundary.waslVowel`) —
    "WASL_IS_DECLARED_OUTSIDE_A_WORD_START": ("همزة", "وصلٌ معلَنٌ في غير أوّل الكلمة"),
    "THE_ROLE_OF_THIS_ALIF_IS_UNDECIDED": ("همزة", "ألفٌ لا يُعرف أهي مدٌّ أم كرسيٌّ أم فارقة"),
    "ALIF_AFTER_A_POSSIBLE_PREFIX_MAY_BE_WASL": ("همزة",
                                                 "ألفٌ بعد سابقةٍ محتملة قد تكون وصلًا — تحتاج الحدّ"),
    "TANWIN_ATTACHMENT_IS_AMBIGUOUS": ("همزة", "موضعُ التنوين على الألف أو ما قبلها غيرُ محسوم"),
}
"""الرفضُ المعلَن: (الصنف، الملاحظة). ما له مرساةٌ لا يُدرَج هنا؛ وما يُدرَج ثمّ يُسدَّد يُحذَف منه."""


def _names_in(tree: ast.AST) -> set[str]:
    out: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fn = node.func
            fname = (fn.id if isinstance(fn, ast.Name)
                     else fn.attr if isinstance(fn, ast.Attribute) else "")
            if fname in EMITTERS and node.args and isinstance(node.args[0], ast.Constant):
                if isinstance(node.args[0].value, str):
                    out.add(node.args[0].value)
            if fname == "Refusal" and len(node.args) >= 2:
                for elt in _tuple_strings(node.args[1]):
                    out.add(elt)
        elif isinstance(node, ast.Dict):
            for k, v in zip(node.keys, node.values, strict=True):
                if (isinstance(k, ast.Constant) and k.value == "reason"
                        and isinstance(v, ast.Constant) and isinstance(v.value, str)):
                    out.add(v.value)
    return out


def _tuple_strings(node: ast.AST) -> list[str]:
    if isinstance(node, ast.Tuple):
        return [e.value for e in node.elts
                if isinstance(e, ast.Constant) and isinstance(e.value, str)]
    if isinstance(node, ast.IfExp):
        return _tuple_strings(node.body) + _tuple_strings(node.orelse)
    return []


def emitted() -> dict[str, list[str]]:
    """الاسمُ ← الملفّاتُ التي تُطلقه."""

    out: dict[str, list[str]] = {}
    for py in sorted(GATE.glob("*.py")):
        tree = ast.parse(py.read_text(encoding="utf-8"), filename=str(py))
        for name in _names_in(tree):
            out.setdefault(name, []).append(py.name)
    return out


def anchors() -> dict[str, str]:
    """الاسمُ ← موضعُ مرساته (أوّلُ ملفٍّ يذكره: Lean ثمّ GLOSSARY)."""

    srcs: list[tuple[str, str]] = []
    for p in sorted(LEAN.glob("*.lean")):
        srcs.append((f"formal/a116/A116/{p.name}", p.read_text(encoding="utf-8")))
    srcs.append(("GLOSSARY.md", GLOSSARY.read_text(encoding="utf-8")))
    out: dict[str, str] = {}
    for name in emitted():
        for where, text in srcs:
            if name in text:
                out[name] = where
                break
    return out


def problems() -> list[str]:
    em, an = emitted(), anchors()
    out: list[str] = []
    for name in sorted(em):
        if name not in an and name not in DECLARED:
            out.append(f"{name}: يُطلَق في {', '.join(em[name])} بلا مرساةٍ ولا إعلان — "
                       "REFUSAL_WITHOUT_ANCHOR")
    for name, (kind, _) in DECLARED.items():
        if name not in em:
            out.append(f"{name}: معلَنٌ ولا يُطلَق — STALE_DECLARED_REFUSAL")
        elif name in an:
            out.append(f"{name}: معلَنٌ وله مرساةٌ في {an[name]} — احذفه من DECLARED — "
                       "STALE_DECLARED_REFUSAL")
        if kind not in KINDS:
            out.append(f"{name}: صنفٌ غيرُ معلَن «{kind}» — UNKNOWN_REFUSAL_KIND")
    return out


def render() -> str:
    em, an = emitted(), anchors()
    n_anchor = sum(1 for n in em if n in an)
    n_decl = sum(1 for n in em if n not in an and n in DECLARED)
    lines = [
        "# سجلُّ الرفض — لا اسمَ رفضٍ بلا مرساةٍ أو إعلان",
        "",
        "مولَّدٌ بـ`python tools/gen_refusals.py` بشجرة تركيب `gate/*.py`؛ لا يُحرَّر باليد. كلُّ اسمٍ "
        "تُطلقه البوّابةُ رفضًا إمّا **مرسًى** (مبرهنةٌ أو تعريفٌ في Lean باسمه، أو مدخلٌ في GLOSSARY؛ "
        "وما في ADR سردٌ لا مرساة) وإمّا **معلَنٌ** دَينًا بصنفه وشرطه في `DECLARED`؛ و`--check` "
        "يُسقط البناءَ على اسمٍ بلا "
        "هذا ولا ذاك (`REFUSAL_WITHOUT_ANCHOR`) وعلى إعلانٍ بَطَل (`STALE_DECLARED_REFUSAL`).",
        "",
        f"{len(em)} اسمًا: {n_anchor} مرسًى، {n_decl} معلَنًا.", "",
        "| الاسم | يُطلَق في | المرساة أو الإعلان |", "|---|---|---|",
    ]
    for name in sorted(em):
        where = "، ".join(f"`{f}`" for f in em[name])
        if name in an:
            lines.append(f"| `{name}` | {where} | مرسًى: `{an[name]}` |")
        else:
            kind, note = DECLARED[name]
            lines.append(f"| `{name}` | {where} | **معلَن** ({kind}): {note} |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ps = problems()
    for p in ps:
        sys.stderr.write(p + "\n")
    text = render() if not ps else ""
    if "--check" in sys.argv:
        if ps:
            return 1
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("REFUSALS.md غيرُ مطابق؛ شغّل tools/gen_refusals.py\n")
            return 1
        sys.stdout.write("REFUSALS.md مطابق\n")
        return 0
    if ps:
        return 1
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write(f"كُتب REFUSALS.md ({text.count(chr(10))} سطرًا)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
