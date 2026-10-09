"""معجمُ الاصطلاح (GLOSSARY.md): كلُّ مصطلحٍ في هذه الشجرة بتعريفٍ من سطرٍ وموضعِ تعريفه الأوّل.

المصطلحُ لا يُعرَّف هنا من الذاكرة: لكلّ سطرٍ موضعٌ (ملفٌّ ومرساةٌ نصّيّة) يجب أن يوجد في الشجرة
(المادّة ١: لا كلامَ قبل الطبعة)، و`--check` يُسقط البناء على مرساةٍ لا توجد (`HALLUCINATED_REFERENCE`)،
وعلى وسمٍ من الأوسمة الخمسة (المادّة ٢) أو نوعِ مودَعٍ من الأربعة (المادّة ١٢) أو مرتبةٍ من الثلاث
(المادّة ١٥) لا مدخلَ له (`TERM_WITHOUT_ENTRY`)، وعلى مدخلٍ لا يرد اسمُه في `CLAUDE.md` ولا في
`AGENT_CONSTITUTION.md` (`ENTRY_WITHOUT_USE`: معجمٌ لا يُستعمل زيادةُ اصطلاح لا نقصُه).
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "GLOSSARY.md"
USED_IN = ("CLAUDE.md", "AGENT_CONSTITUTION.md")


class Term(NamedTuple):
    name: str
    latin: str
    meaning: str
    where: str  # file
    anchor: str  # نصٌّ يجب أن يوجد في الملفّ بعينه
    forms: tuple[str, ...] = ()  # صورٌ أخرى يُعدّ ورودُها استعمالًا (الصرفُ يغيّر الرسم)


TERMS: tuple[Term, ...] = (
    # — القانون الواحد والبوّابة —
    Term("القانون الواحد", "the one law",
         "لا يدخل الشجرةَ إلّا بتٌّ ولا يخرج منها إلّا بتّ، ومدخلُه ومخرجُه الوحيدان البرهانُ "
         "في `formal/a116` ومرآتُه `gate/`.", "CLAUDE.md", "## القانون الواحد"),
    Term("البتّ", "bit (certificate-or-refusal)",
         "ما تُنتجه البوّابةُ على بايتات: شهادةٌ أو رفضٌ مسمًّى؛ لا نصَّ ولا تخمينَ بينهما.",
         "CLAUDE.md", "لا يدخل إلى هذه الشجرة إلّا بتٌّ", ("بتٌّ", "بتّ")),
    Term("البوّابة", "gate",
         "الواجهةُ الوحيدة: `enter` / `exit` / `derive` / `recover` / `licence`؛ مرآةُ البرهان "
         "في بايثون.", "gate/api.py", "def enter("),
    Term("الـ116", "the 116 (cells)",
         "خاناتُ الذرّات: 29 حاملًا × 4 حالاتٍ (فتح/كسر/ضم/سكون) = 116، عددًا مبرهَنًا نتيجةً لا "
         "مُدخَلًا (`cells_length`)؛ والـ112 ما سوى صفّ الهمزة.", "formal/a116/A116/Cells.lean",
         "theorem cells_length : cells.length = 116"),
    Term("الذرّة", "atom",
         "واحدةٌ من خانات الـ116: حاملٌ (حرف) في حالةٍ (حركة)؛ الشهادةُ قائمةُ ذرّات.",
         "CLAUDE.md", "الشهادةُ ذرّاتٌ من الـ116"),
    Term("الحامل والحالة", "carrier and state (hamil / hala)",
         "جزءا الذرّة: الحاملُ حرفٌ من 29، والحالةُ حركتُه من 4؛ ومنه اسمُ مستودع hamil "
         "(حامل/حالة/زمان).", "formal/a116/A116/Cells.lean", "def carrierCount : Nat := 29",
         ("حامل", "الحوامل", "hamil")),
    Term("الشهادة", "Certificate",
         "مخرجُ `enter` الناجح: ذرّاتٌ من الـ116 وعددٌ يطويها؛ لا تأخذ العالمَ معاملًا "
         "(المادّة ١١).", "gate/api.py", "class Certificate"),
    Term("الرفضُ المسمّى", "named Refusal",
         "مخرجُ `enter` غيرُ الناجح: `DEFER` أو `REJECT` أو `OUTSIDE_DECLARED_DOMAIN` بأسبابه "
         "المسمّاة؛ لا يُخمَّن شيء (المادّة ٥).", "gate/api.py", "class Refusal"),
    Term("الحدّ", "boundary / Context",
         "موضعُ الكلمة: ابتداءٌ أو وصلٌ، ووقفٌ أو استمرار (`Context(entry, exit)`)؛ في الوصل "
         "تُرخَّص الكلمةُ مع ما قبلها.", "gate/contextual.py", "class Context"),
    Term("الترخيصُ الثلاثيّ", "ternary licence (cv | v | c)",
         "تقطيعُ الكلمة إلى مقاطع ثلاثيّةٍ لا ثنائيّة؛ فالثنائيُّ أعمى عن المدّ.",
         "formal/a116/A116/Ternary.lean", "theorem binary_is_blind_to_madd"),
    Term("قيدُ الحدّ", "hadd constraint (CVVC only before a geminate)",
         "«التقاءُ الساكنين على حدّه»: قافيةُ المدّ (CVVC) لا تُرخَّص وصلًا إلّا والمُغلِقُ أوّلُ مثلين "
         "(حَاجَّ) أو مدَّ فرق، والمدُّ والمدغمُ في كلمةٍ واحدة؛ وما سواه رفضٌ مسمًّى "
         "(`CVVC_NOT_GEMINATE`، `CVVC_ACROSS_WORD_BOUNDARY`) — `strictB` و`strictJoinB`.",
         "formal/a116/A116/Hadd.lean", "def strictB (w : List Cell) : Bool", ("قيدُ الحدّ",)),
    Term("المدُّ العارض للسكون", "pausal madd (CVVC licensed only word-finally at pause)",
         "وقفًا يُسكَّن الآخر فتجتمع قافيةُ مدٍّ ومُغلِقٌ في الطرف (الرَّحِيمْ)؛ الطرفُ وحدَه يُقبل "
         "(`strictPauseB`، `strictJoinPauseB`) وكلُّ `v c` داخليٍّ مدغمٌ كما وصلًا؛ وما يرفضه الوقف "
         "`NOT_PAUSE_LICENSED`.",
         "formal/a116/A116/Hadd.lean", "def strictPauseB (w : List Cell) : Bool", ("المدُّ العارض",)),
    Term("التقاءُ الساكنين على الحدّ", "sukun clash at the word boundary (three named repairs)",
         "ساكنٌ آخرَ الأولى يليه ساكنٌ أوّلَ الثانية: الألفُ الفارقة تسقط، أو حرفُ المدّ يُحذف، أو الساكنُ "
         "يُكسَر (الكتاب: «أن يكون الساكن الأول مكسورا») — في آخر الأولى وحدَها، وجهًا مسمًّى في الشهادة "
         "(`Certificate.junction`)؛ وبلا التقاءٍ لا شيء.",
         "formal/a116/A116/Iltiqa.lean", "def repair (l r : List Cell) : List Cell × Option Repair",
         ("التقاء الساكنين",)),
    Term("السكونُ الموضعيّ", "positional sukun",
         "حالةُ `sukun` في الخانة معناها «موضعٌ لا تتبعه حركةٌ قصيرة» لا «عدمُ الحركة نطقًا»؛ فحرفُ المدّ "
         "خانةٌ ساكنةٌ موضعًا وجزءٌ ثانٍ من حركةٍ طويلةٍ نطقًا.",
         "formal/a116/A116/Hadd.lean", "معناه موضعيٌّ", ("موضعيّ",)),
    Term("دورُ المدّ", "madd role (v)",
         "صنفُ الخانة الساكنة إن كانت ا بعد فتحة أو و بعد ضمّة أو ي بعد كسرة (`v`)، وإلّا فهي مُغلِق "
         "(`c`)؛ تعريفٌ في Lean (`kindOf`) ومرآتُه `kind_of`.", "formal/a116/A116/Hadd.lean",
         "def kindOf (w : List Cell) : List K", ("المدّ",)),
    Term("مدُّ الفرق", "madd al-farq",
         "الاستثناءُ الوحيد من قيد الحدّ: ءَ اْ لْ في أوّل الكلمة (آلْآنَ)؛ معلنٌ من اصطلاح القرّاء، "
         "ومشهودٌ في المودَع، وموضعُ نصّه في مصدرٍ مسمًّى لم يُتحقَّق.", "formal/a116/A116/Hadd.lean",
         "def isFarq : List Cell → Bool", ("مدّ الفرق", "مدَّ الفرق")),
    Term("الحركةُ الصفر", "zero vowel",
         "اصطلاحُ «دراسات في علم اللغة» للسكون: عدمٌ نطقًا، عنصرٌ رابعٌ في نظام الحركات وظيفيًّا؛ وهو "
         "في الـ116 حالةُ `sukun` على المستوى الوظيفيّ لا غير (معلن).",
         "docs/adr/0003-hadd-cvvc-geminate.md", "«الحركة الصفر»", ("الحركةُ الصفر",)),
    Term("الاشتقاقُ والاسترجاع", "derive / recover",
         "من الجذر إلى صوره (`derive`) ومن الصورة إلى قراءاتها (`recover`)؛ كلاهما مقيسٌ على "
         "مرجعٍ محجوب.", "gate/api.py", "def recover("),
    Term("البقيّة", "residue",
         "الرسمُ = صورةٌ قانونيّة + بقيّةُ قواعدِ طبعةٍ مسمّاة؛ تحملها الشهادةُ ويُردّ الرسمُ "
         "بعينه (`chain_restore`)؛ ما لا قاعدةَ له يُرفض باسمه.", "formal/a116/A116/Residue.lean",
         "theorem chain_restore"),
    Term("الطبعة", "edition (of the text)",
         "مصدرُ الرسم بعينه (طبعةُ المصحف المختومة، globalquran…)؛ ومنه «لا ثقة بلا طبعة»: لا "
         "كلامَ عن ملفٍّ قبل إثبات وجوده.", "AGENT_CONSTITUTION.md",
         "## المادّة ١ — لا كلامَ قبل الطبعة"),
    # — المودَع والختم —
    Term("المودَع", "deposit",
         "بياناتٌ مودَعةٌ لا تقرؤها شيفرةٌ إلّا أداةُ إيداعٍ معفاة تولّد جدولًا بـ`--check`؛ لا "
         "مودَعَ بلا نوعٍ من أربعة.", "AGENT_CONSTITUTION.md", "## المادّة ١٢ — لا مودَعَ بلا نوع"),
    Term("أنواعُ المودَع الأربعة", "the four deposit kinds",
         "**واقعٌ مختوم** (شهاداتُ النصّ كما نقلتها البوّابة)، **وضع** (اصطلاحُ العرب: المقاييس "
         "والأبنية)، **معلوماتٌ سابقة** (الأجناسُ والقابليّات)، **مرجعٌ محجوب** (وسومٌ بشريّة "
         "يُقاس عليها).", "AGENT_CONSTITUTION.md", "أربعةُ أنواعٍ للمودَع لا خامسَ لها"),
    Term("الختم", "seal",
         "بصمةُ sha256 ورخصةٌ على مودَعٍ بإذن المالك؛ المدوّنةُ مختومةٌ بـ`CORPUS_SHA256` ولا "
         "تُقرأ إن اختلفت بصمتُها.", "gate/api.py", "CORPUS_SHA256", ("مختوم", "ختم")),
    Term("المرجعُ المحجوب", "held-out reference (MASAQ)",
         "وسومٌ بشريّة لا تدخل الشيفرةَ ولا تُقرأ منها قاعدة؛ يُقاس عليها فقط (MASAQ للترخيص؛ "
         "مجازُ القرآن للأحكام إن قيس).", "CLAUDE.md", "مرجعٍ بشريٍّ محجوب (MASAQ)", ("محجوب",)),
    Term("المعلَّق", "suspended",
         "وحدةٌ نُقلت إلى `suspended/` بسجلٍّ يذكر سببَها وشرطَ عودتها؛ نقلٌ لا حذف، ولا "
         "تُستورد ولا يُستشهد بخضرتها.", "CLAUDE.md", "SUSPENDED_REGISTRY.json"),
    Term("الحارس", "guard",
         "فاحصٌ يمشي على الشجرة ويُسقط البناءَ على أيّ قراءةٍ أو كتابةٍ أو تطبيعٍ للنصّ خارج "
         "البوّابة (`breaches()`).", "gate/guard.py", "def breaches"),
    Term("الشرطُ الثلاثيّ للعودة", "the three conditions of readmission",
         "لا تعود وحدةٌ معلَّقة إلّا بثلاثة معًا: مدخلُها ومخرجُها عبر البوّابة، اختباراتٌ "
         "مستقلّةٌ مطعَّمةٌ بالطفرة (20/20)، وADR مسجَّل.", "CLAUDE.md", "منهج 20/20"),
    Term("ADR", "architecture decision record",
         "قرارٌ معماريٌّ مؤرَّخ يسجّل الإذنَ والأركانَ والمقيسَ وما بقي باسمه.",
         "CLAUDE.md", "ADR مسجَّل"),
    # — الأوسمة والمخالفات —
    Term("الأوسمة الخمسة", "the five tags",
         "**مبرهن** (Lean باسمه في `Audit.lean` بالمسلّمات الثلاث)، **مطابَق** (جدولُ Lean يطابقه "
         "اختبار)، **مفحوص** (اختبارٌ باسمه مستقلُّ التوقّع)، **مقيس** (رقمٌ على مرجعٍ محجوب "
         "بأداةٍ مولِّدة)، **معلن / رأي** (ما سوى ذلك).", "AGENT_CONSTITUTION.md",
         "## المادّة ٢ — الوسمُ بقدر السند"),
    Term("المخالفةُ المسمّاة", "named violation",
         "لكلّ مادّةٍ اسمُ مخالفتها (`HALLUCINATED_REFERENCE`، `CLAIM_ABOVE_ITS_SUPPORT`، "
         "`TEST_MIRRORS_CODE`…) يُذكر في الإقرار لا يُلطَّف.", "AGENT_CONSTITUTION.md",
         "## المادّة ٧ — الإقرارُ بالخطأ بالاسم"),
    Term("صيغةُ الجواب", "the binding answer form",
         "ثلاثةُ أقسامٍ لا تُدمج: ما فحصته الآلة / ما استنتجتُه / ما بقي باسمه.",
         "AGENT_CONSTITUTION.md", "## المادّة ٨ — صيغةُ الجواب الملزِمة"),
    # — الباب الثاني والثالث —
    Term("الوضع", "wad' (lexical convention)",
         "اصطلاحُ العرب على ربط لفظٍ بمعنًى؛ مودَعٌ من نوع «وضع» يُقاس على مرجع الترخيص ولا "
         "يحكم على الواقع.", "AGENT_CONSTITUTION.md",
         "## الباب الثاني — الوضعُ والمعلوماتُ السابقة والحكم"),
    Term("المعلوماتُ السابقة", "prior information",
         "حقائقُ الأشياء وخواصُّها (الأجناسُ والقابليّات) مودَعةً بنوعها؛ شرطُ الحكم مع الواقع "
         "والحسّ والدماغ.", "AGENT_CONSTITUTION.md", "## المادّة ١٤ — أركانُ العقل الأربعة"),
    Term("الحكم", "judgement",
         "مطابقةُ النسبة للواقع المودَع؛ فوق سُلَّم الترخيص لا فيه، ثلاثيٌّ على النسبة، ولا "
         "يُسقط ترخيصًا.", "AGENT_CONSTITUTION.md", "## المادّة ١٠ — الحكمُ فوق الترخيص لا فيه"),
    Term("السُّلَّم", "the ladder (of licensing gates)",
         "بوّاباتُ الترخيص المتتابعة (`gate` في الغانم، `gates.LADDER` في SLGE)؛ لا بوّابةَ "
         "فوق مرفوضة، ولا حكمَ داخله.", "AGENT_CONSTITUTION.md", "سُلَّمَ الترخيص"),
    Term("أركانُ العقل الأربعة", "the four pillars of reason",
         "واقعٌ، وحسٌّ ينقله، ودماغ، ومعلوماتٌ سابقة؛ شرطُ قبول أيّ اقتراح، وإلّا فبحثٌ منطقيٌّ "
         "أو توهّم.", "AGENT_CONSTITUTION.md", "## المادّة ١٤ — أركانُ العقل الأربعة"),
    Term("مراتبُ المخرج الثلاث", "the three output grades",
         "**من حيث هي** (ما تدلّ عليه الصورةُ بوضعها)، **معلومة** (معنًى بلا شاهدِ واقعٍ مودَع)، "
         "**مفهوم** (معنًى له واقعٌ مودَعٌ مشهود)؛ لا تُدمج اثنتان.", "AGENT_CONSTITUTION.md",
         "## المادّة ١٥ — ثلاثُ مراتبَ للمخرج"),
    Term("الشاهد", "witness",
         "عقدةٌ أو صورةٌ مودَعةٌ بعينها تُسند «مفهومًا»؛ لا مفهومَ بلا شاهد، والغيابُ ليس امتناعًا.",
         "AGENT_CONSTITUTION.md", "## المادّة ١٦ — لا «مفهوم» بلا واقعٍ مودَع"),
    Term("الزوائد", "augments (huruf al-ziyada)",
         "حروفُ سيبويه العشرة (ء ا ه ي ن ت س م و ل) خاناتٍ من الـ116 لا أفرادًا؛ إلصاقُها عمليّةٌ "
         "تحفظ الترخيص وقطعُها عكسُها (SLGE: `Slge.Zawaid`).", "AGENT_CONSTITUTION.md",
         "## المادّة ١٢ — لا مودَعَ بلا نوع", ("الزوائد", "زائدة", "augments")),
    Term("الدلالةُ من حيث هي", "signification as such",
         "ما يدلّ عليه اللفظُ بوضعه بلا لافظٍ ولا سامع؛ وLean يُبرهن المرويَّ لا اللغة.",
         "AGENT_CONSTITUTION.md", "## المادّة ١٧ — الدلالةُ من حيث هي"),
)

VOCAB = ("مبرهن", "مطابَق", "مفحوص", "مقيس", "معلن", "واقعٌ مختوم", "وضع", "معلوماتٌ سابقة",
         "مرجعٌ محجوب", "من حيث هي", "معلومة", "مفهوم")
"""الأوسمةُ الخمسة وأنواعُ المودَع الأربعة والمراتبُ الثلاث: كلٌّ يجب أن يرد في معنى مدخلٍ ما."""


def problems() -> list[str]:
    out: list[str] = []
    used = "\n".join((ROOT / f).read_text(encoding="utf-8") for f in USED_IN)
    meanings = "\n".join(t.meaning for t in TERMS)
    for t in TERMS:
        p = ROOT / t.where
        if not p.exists():
            out.append(f"{t.name}: لا ملفَّ {t.where} — HALLUCINATED_REFERENCE")
        elif t.anchor not in p.read_text(encoding="utf-8"):
            out.append(f"{t.name}: المرساةُ «{t.anchor}» ليست في {t.where} — HALLUCINATED_REFERENCE")
        if not any(f in used for f in (t.name.split()[0], t.latin.split()[0], *t.forms)):
            out.append(f"{t.name}: لا يرد في {' ولا '.join(USED_IN)} — ENTRY_WITHOUT_USE")
    for v in VOCAB:
        if v not in meanings:
            out.append(f"{v}: وسمٌ أو نوعٌ أو مرتبةٌ بلا مدخل — TERM_WITHOUT_ENTRY")
    names = [t.name for t in TERMS]
    if len(set(names)) != len(names):
        out.append("مدخلٌ مكرَّر")
    return out


def render() -> str:
    lines = [
        "# معجمُ الاصطلاح — كلُّ مصطلحٍ بموضع تعريفه",
        "",
        "مولَّدٌ بـ`python tools/gen_glossary.py` من `TERMS` فيه؛ لا يُحرَّر باليد. لكلّ مدخلٍ "
        "موضعٌ (ملفٌّ ومرساةٌ نصّيّة) يفحصه `--check` في CI: مرساةٌ لا توجد تُسقط البناءَ باسم "
        "`HALLUCINATED_REFERENCE`، ووسمٌ أو نوعُ مودَعٍ أو مرتبةٌ بلا مدخلٍ باسم `TERM_WITHOUT_ENTRY`، "
        "ومدخلٌ لا يُستعمل في `CLAUDE.md` ولا `AGENT_CONSTITUTION.md` باسم `ENTRY_WITHOUT_USE`. "
        "المعاني هنا تعريفاتٌ «معلنة»؛ سندُ كلٍّ منها في موضعه لا هنا. يحكم المستودعاتِ كلَّها "
        "(الغانم، SLGE، hamil، Algebra، الدساتير الثلاثة).",
        "",
        f"{len(TERMS)} مدخلًا.", "",
        "| المصطلح | بالإنجليزيّة | المعنى | موضعُ التعريف |", "|---|---|---|---|",
    ]
    for t in TERMS:
        lines.append(f"| **{t.name}** | {t.latin} | {t.meaning} | `{t.where}` — «{t.anchor}» |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ps = problems()
    for p in ps:
        sys.stderr.write(p + "\n")
    text = render()
    if "--check" in sys.argv:
        if ps:
            return 1
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("GLOSSARY.md غيرُ مطابق؛ شغّل tools/gen_glossary.py\n")
            return 1
        sys.stdout.write("GLOSSARY.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write(f"كُتب GLOSSARY.md ({len(TERMS)} مدخلًا)\n")
    return 1 if ps else 0


if __name__ == "__main__":
    raise SystemExit(main())
