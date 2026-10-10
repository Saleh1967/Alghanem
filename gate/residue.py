"""بقيّةُ الرسم: SLGE لقواعد إملاء الطبعة — مرآةُ `formal/a116/A116/Residue.lean`.

الرسمُ في الطبعة = الصورةُ القانونيّة (تقبلها البوّابة) + بقيّةٌ: قائمةُ تعديلاتٍ مسمّاة
‎(قاعدة، موضع)‎ تُطبَّق بالترتيب ثمّ تُردّ بالعكس. المبرهَن هناك: كلُّ قاعدةٍ تُردّ بعينها
(`*_restore`)، والسلسلةُ تُردّ (`chain_restore`)، والرسمُ يحدّد الصورةَ والبقيّةَ معًا
(`residue_separates`). وهنا: `repair(surface) → (canonical, residue)` و`unrepair(canonical,
residue) → surface` بعينه، ومطابقةُ الردّ على كلّ مفردات المصحف في `tests/test_residue.py`.

القواعدُ السبع بترتيب تطبيقها (ترتيبٌ معلَن؛ الردُّ بعكسه):

1. `IDGHAM`   — شدّةٌ أوّلَ الكلمة (إدغامٌ من الوصل): تُحذف.
2. `TANWIN_ALIF` — تنوينُ الفتح بعد الألف: يُقدَّم على الألف (`اً` ← `ًا`).
3. `FARIQA`   — ألفٌ في الآخر بعد واوٍ ساكنة (أو واوٍ بلا علامة ستصير ساكنة): تُحذف.
3ب. `AMR_WAW` — واوٌ بلا علامةٍ في الآخر بعد حرفٍ منوَّن (عَمْرٍو): واوُ عمرو الفارقة، تُحذف.
3ج. `IBN_ALIF` — «بْنُ» بلا ألفٍ بين علمين: تُعاد ألفُ «ابن» فتأخذ حركتَها بـWASL؛ الردُّ يحذفها.
4. `WASL`     — ألفٌ بلا علامةٍ أوّلَ الكلمة قبل ساكن: همزةُ وصلٍ بحركتها بالقاعدة (فتحةٌ في «ال»،
   ضمّةٌ إن كان ثالثُ الفعل مضمومًا، وإلّا كسرة).
5. `WASL_SILENT` — ألفُ وصلٍ بعد لاصقةٍ متحرّكة: صامتةٌ في الوصل، تُحذف.
6. `SHAMSI`   — لامُ «ال» قبل حرفٍ مشدَّد (شمسيّة): مدغمةٌ لا تُنطق، تُحذف.
7. `SUKUN`    — حرفٌ بلا علامة (مدٌّ، ميمُ جمع، نونٌ مخفاة…): يُدخَل بعده سكون؛ إلّا ألفَ التنوين.

كلُّ تعديلٍ يُسجَّل بموضعه في **سلسلة العناقيد** (حرفٌ + علاماتُه) عند لحظة تطبيقه، فالردُّ
بالعكس يعيد الرسم حرفًا حرفًا. وما لا تغطّيه هذه الأربع يبقى موقوفًا باسمه عند البوّابة.
"""

from __future__ import annotations

import unicodedata
from typing import Final

__all__ = ["RULES", "Edit", "clusters", "has_marks", "repair", "unrepair"]

SUKUN: Final = "ْ"
SHADDA: Final = "ّ"
FATHATAN: Final = "ً"
TANWINS: Final = ("\u064b", "\u064c", "\u064d")  # ً ٌ ٍ
WASL_NOUNS: Final = ("\u0628\u0646", "\u0633\u0645", "\u0645\u0631\u0623", "\u0645\u0631\u0624",
                     "\u062b\u0646")
"""الأسماءُ الموصولةُ الهمزة (هياكلُها بعد الألف): ابن/ابنة، اسم، امرأة، امرؤ، اثنان/اثنتان («است»
تُركت: هيكلُها يلتبس باستفعل) — همزتُها مكسورةٌ أبدًا (الكتاب س17573: «مكسورة أبدا في الأسماء والأفعال
إلا في الفعل المضموم الثالث»)."""
WASL_NOUNS_FATHA: Final = ("\u064a\u0645\u0646",)  # ايمن: مفتوحة
ALIF: Final = "ا"
WAW: Final = "و"
YA: Final = "ي"
MADD: Final[dict[str, str]] = {ALIF: "َ", WAW: "ُ", YA: "ِ"}
ALIF_WASLA: Final = "\u0671"
ALIF_MAQSURA: Final = "\u0649"
FATHA: Final = "\u064e"
DAMMA: Final = "\u064f"
KASRA: Final = "\u0650"
LAM: Final = "\u0644"
PROCLITICS: Final = "\u0648\u0641\u0628\u0644\u0643\u0623"  # و ف ب ل ك أ
LETTERS: Final[frozenset[str]] = frozenset("ءآأؤإئابةتثجحخدذرزسشصضطظعغفقكلمنهوىي" + ALIF_WASLA)
"""حروفُ الرسم التي يعرفها الجسر (`bridge._is_arabic_letter`): قاعدةُ السكون لا تُطبَّق على غيرها
(واوٌ صغيرة، ياءٌ صغيرة، تطويل، ترقيم…) كي لا تُصنع علامةٌ بلا حرفٍ تُقرأ كلمةً ثانية."""
DAGGER: Final = "\u0670"
RULES: Final[tuple[str, ...]] = (
    "DAGGER_ALIF", "IDGHAM", "TANWIN_ALIF", "FARIQA", "AMR_WAW", "IBN_ALIF", "WASL", "WASL_SILENT",
    "SHAMSI", "ASSIM", "SUKUN",
)


def _proclitics(prefix: list[str]) -> bool:
    """كلُّ ما قبل الموضع لواصقُ من حرفٍ واحدٍ متحرّك (وَ، فَ، بِ، لِ، كَ، أَ)."""

    return bool(prefix) and all(
        len(c) == 2 and c[0] in PROCLITICS and c[1] in (FATHA, KASRA, DAMMA) for c in prefix
    )

Edit = tuple[str, int, str]
"""(القاعدة، موضعُ العنقود الذي طُبّقت عليه، ما حُذف من الرسم إن حُذف شيء) — `EditRecord.removed`."""


def clusters(text: str) -> list[str]:
    """حرفٌ وما لحقه من علامات، عنقودًا عنقودًا — بترتيب الرسم كما ورد (لا تطبيع، كي يعود بعينه)."""

    out: list[str] = []
    for ch in text:
        if unicodedata.category(ch) == "Mn" and out:
            out[-1] += ch
        else:
            out.append(ch)
    return out


def has_marks(text: str) -> bool:
    """أفي الرسم علامةٌ واحدةٌ على الأقلّ؟ (ما لا علامةَ فيه لا يُصلَح: لا تخمين.)"""

    return any(unicodedata.category(ch) == "Mn" for ch in text) or "\u0622" in text


def _bare(c: str) -> bool:
    return len(c) == 1 and c[0] in LETTERS and c[0] != "آ"  # آ تحمل مدّها في ذاتها


def _plural_waw_stem(cl: list[str]) -> str | None:
    """أمرُ الجماعة من الناقص: ا C₁ْ C₂ُ و (ا | ْا | لاحقة) — يعيد صورةَ الأمر المجرّدة «اC₁ْC₂ُوا» للفهرس،
    أو لا شيء إن لم يكن الشكلُ هذا."""

    if not (len(cl) >= 4 and cl[0] in (ALIF, ALIF_WASLA) and len(cl[1]) == 2 and cl[1][1] == SUKUN
            and cl[1][0] != LAM and len(cl[2]) == 2 and cl[2][1] == DAMMA and cl[3][0] == WAW):
        return None
    if len(cl) == 4 and cl[3] in (WAW, WAW + SUKUN) or len(cl) > 4 and cl[3] == WAW:
        return ALIF + cl[1] + cl[2] + WAW + ALIF
    return None


def damma_stability(imperative: str) -> str | None:
    """ثبوتُ ضمّة الثالث قبل واو الجماعة (الكتاب س17570–17573؛ `A116.Boundary.waslVowelStable`):
    من فهرس الأفعال على جذور المقاييس (`mabni_verbs.verb_index`) — جذرٌ واحدٌ يولّد الأمرَ: ناقصٌ يائيٌّ
    (اِمْشِ ← اِمْشُوا) فالضمّةُ «عارضة»، واويٌّ (اُدْعُ ← اُدْعُوا) فـ«ثابتة»؛ ولا جذرَ أو أكثرُ من واحد فلا يُقرَّر
    (لا تخمين). الفهرسُ يُبنى عند أوّل حاجةٍ (نحو 20 ثانية) ويُحفظ."""

    from .mabni_verbs import normalize, verb_index

    analyses = verb_index().get(normalize(imperative), ())
    roots = {a[0] for a in analyses if a[1] == "IMPERATIVE"}
    if len(roots) != 1:
        return None
    return "عارضة" if roots.pop()[2] == YA else "ثابتة"


def repair(surface: str) -> tuple[str, tuple[Edit, ...]]:
    """الرسمُ ← (الصورةُ القانونيّة، البقيّة). لا يُخمَّن شيء: كلُّ تعديلٍ من قاعدةٍ مسمّاة."""

    cl = clusters(surface)
    edits: list[Edit] = []

    # 0. DAGGER_ALIF: ألفٌ خنجريّةٌ فوق الحرف (طبعةُ globalquran: الرَّحْمَٰنِ) — تُحذف فتصير الصورةُ صورةَ
    #    المدوّنة المختومة بعينها، ويُسجَّل العنقودُ كما ورد فيُردّ بعينه (`Residue.daggerAlif_restore`).
    for i, c in enumerate(cl):
        if DAGGER in c:
            edits.append(("DAGGER_ALIF", i, c))
            cl[i] = c.replace(DAGGER, "")

    # 1. IDGHAM
    if cl and SHADDA in cl[0]:
        cl[0] = cl[0].replace(SHADDA, "")
        edits.append(("IDGHAM", 0, SHADDA))

    # 2. TANWIN_ALIF: ...X اً  →  ...Xً ا
    if len(cl) >= 2 and cl[-1] in (ALIF + FATHATAN, ALIF_MAQSURA + FATHATAN) \
            and FATHATAN not in cl[-2]:
        cl[-2] = cl[-2] + FATHATAN
        cl[-1] = cl[-1][0]
        edits.append(("TANWIN_ALIF", len(cl) - 2, ""))

    # 3. FARIQA: ... وْ ا  (أو  و ا  بلا علامة على الواو)
    if len(cl) >= 2 and cl[-1] == ALIF and cl[-2] in (WAW, WAW + SUKUN):
        edits.append(("FARIQA", len(cl) - 1, ALIF))
        cl.pop()

    # 3ب. AMR_WAW: واوُ «عَمْرو» الفارقة — واوٌ بلا علامةٍ في الآخر بعد حرفٍ منوَّن (عَمْرٍو، عَمْرٌو):
    #     لا تُنطق، تُحذف وتُردّ؛ لا تظهر في مدوّنة المصحف (الصحيحان: 1,129 موقعًا).
    if len(cl) >= 2 and cl[-1] == WAW and any(t in cl[-2] for t in TANWINS):
        edits.append(("AMR_WAW", len(cl) - 1, WAW))
        cl.pop()

    # 3ج. IBN_ALIF: «بْنُ/بْنِ/بْنَ» بلا ألف — ألفُ «ابن» تسقط رسمًا بين علمين (الصحيحان: 41,229 موقعًا):
    #     تُعاد ألفُ الوصل ثمّ تأخذ حركتَها بقاعدة WASL أدناه؛ والردُّ يحذفها. لا تظهر في المصحف.
    if len(cl) == 2 and cl[0] in ("\u0628", "\u0628" + SUKUN) and cl[1][0] == "\u0646" \
            and len(cl[1]) == 2 and cl[1][1] in MADD.values():
        cl.insert(0, ALIF)
        edits.append(("IBN_ALIF", 0, ""))

    # 4. WASL: ألفٌ بلا علامةٍ أوّلَ الكلمة قبل ساكنٍ = همزةُ وصل، بحركتها بالقاعدة:
    #    فتحةٌ في «ال»، وضمّةٌ إن كان ثالثُ الفعل مضمومًا، وإلّا كسرة (سيبويه).
    #    (`A116.Boundary.waslVowel`؛ الكتاب س17530–17531). والألفُ المرسومةُ وصلةً (ٱ) بلا علامةٍ كذلك.
    #    وضمّةُ ثالثِ أمرِ الناقص قبل واو الجماعة لا تضمّ الهمزةَ إلّا ثابتةً (`waslVowelStable`).
    if (len(cl) >= 3 and cl[0] in (ALIF, ALIF_WASLA)
            and (_bare(cl[1]) or SUKUN in cl[1] or SHADDA in cl[1])):
        skeleton = "".join(c[0] for c in cl[1:4])
        if cl[1][0] == LAM:
            v = FATHA
        elif skeleton.startswith(WASL_NOUNS_FATHA):
            v = FATHA  # ايْمُنُ اللهِ
        elif (imperative := _plural_waw_stem(cl)) is not None:
            # ضمّةُ الثالث قبل واو الجماعة: ثابتةٌ (اُدْعُوا) فضمّ، عارضةٌ (اِمْشُوا) فكسر، ولا يُعلم
            # فوصلةٌ ساكنةٌ يرفضها الجسرُ باسمها START_VOWEL_OF_WASL_IS_UNKNOWN (الكتاب س17570–17573؛
            # `waslVowelStable`)
            stability = damma_stability(imperative)
            v = DAMMA if stability == "ثابتة" else KASRA if stability == "عارضة" else SUKUN
        elif skeleton.startswith(WASL_NOUNS):
            v = KASRA  # الأسماءُ الموصولة مكسورةٌ أبدًا (الكتاب س17573) ولو ضُمّ ثالثُها: اِبْنُ، اِسْمُ
        elif DAMMA in cl[2]:  # ثالثُ الفعل بعدّ الهمزة: ا ن صُ ر
            v = DAMMA
        else:
            v = KASRA
        edits.append(("WASL", 0, cl[0]))
        cl[0] = ALIF_WASLA + v

    # 5. WASL_SILENT: ألفُ وصلٍ بلا علامةٍ بعد لاصقةٍ متحرّكة (و/ف/ب/ل/ك/أ) قبل لامِ «ال» أو ساكن:
    #    صامتةٌ في الوصل، تُحذف وتُعاد بالسجلّ.
    i = 1
    while i < len(cl) - 1:
        if (cl[i] == ALIF and _proclitics(cl[:i])
                and (cl[i + 1] == LAM or SUKUN in cl[i + 1] or SHADDA in cl[i + 1]
                     or (_bare(cl[i + 1]) and cl[i + 1] not in (ALIF, WAW, YA)
                         and i + 2 < len(cl)))):
            edits.append(("WASL_SILENT", i, ALIF))
            cl.pop(i)
            continue
        i += 1

    # 6. SHAMSI: لامُ «ال» قبل حرفٍ مشدَّدٍ لامٌ مدغمةٌ لا تُنطق: تُحذف، وتُعاد بالسجلّ.
    #    تسبقها ألفُ الوصل، أو لاصقةٌ ابتلعت الألف (لِلشَّمْسِ).
    i = 0
    while i + 1 < len(cl):
        prev = cl[i - 1] if i >= 1 else ""
        if (cl[i] == LAM and SHADDA in cl[i + 1]
                and (prev[:1] in (ALIF, ALIF_WASLA) or (prev[:1] == LAM and len(prev) == 2)
                     or (i >= 1 and _proclitics(cl[:i]) and prev[:1] in PROCLITICS))):
            edits.append(("SHAMSI", i, LAM))
            cl.pop(i)
            continue
        i += 1

    # 7. ASSIM: حرفٌ صحيحٌ بلا علامةٍ قبل حرفٍ مشدَّد (وَجَدتُّم): مدغمٌ فيه لا يُنطق، يُحذف ويُعاد بالسجلّ.
    i = 0
    while i + 1 < len(cl):
        if (_bare(cl[i]) and cl[i] not in (ALIF, WAW, YA, ALIF_MAQSURA) and SHADDA in cl[i + 1]
                and i >= 1 and not _bare(cl[i - 1])):
            edits.append(("ASSIM", i, cl[i]))
            cl.pop(i)
            continue
        i += 1

    # 8. SUKUN: كلُّ حرفٍ بلا علامة (إلّا ألفًا بعد تنوين الفتح: دعامةٌ صامتة)
    for i, c in enumerate(cl):
        if _bare(c) and not (c in (ALIF, ALIF_MAQSURA) and i > 0 and FATHATAN in cl[i - 1]):
            cl[i] = c + SUKUN
            edits.append(("SUKUN", i, ""))

    return "".join(cl), tuple(edits)


def unrepair(canonical: str, residue: tuple[Edit, ...]) -> str:
    """(الصورةُ القانونيّة، البقيّة) ← الرسمُ بعينه؛ الردُّ بعكس ترتيب التطبيق (`restoreAll`)."""

    cl = clusters(canonical)
    for rule, i, removed in reversed(residue):
        if rule == "SUKUN":
            cl[i] = cl[i].replace(SUKUN, "", 1)
        elif rule in ("ASSIM", "SHAMSI", "WASL_SILENT", "FARIQA", "AMR_WAW"):
            cl.insert(i, removed)
        elif rule == "WASL":
            cl[0] = removed
        elif rule == "IBN_ALIF":
            cl.pop(0)
        elif rule == "TANWIN_ALIF":
            cl[i] = cl[i].replace(FATHATAN, "", 1)
            cl[i + 1] = cl[i + 1][0] + FATHATAN
        elif rule == "IDGHAM":
            cl[0] = cl[0][0] + removed + cl[0][1:]
        elif rule == "DAGGER_ALIF":
            cl[i] = removed
        else:
            raise ValueError(f"UNKNOWN_RULE:{rule}")
    return "".join(cl)
