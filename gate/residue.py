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
RULES: Final[tuple[str, ...]] = (
    "IDGHAM", "TANWIN_ALIF", "FARIQA", "WASL", "WASL_SILENT", "SHAMSI", "ASSIM", "SUKUN",
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


def repair(surface: str) -> tuple[str, tuple[Edit, ...]]:
    """الرسمُ ← (الصورةُ القانونيّة، البقيّة). لا يُخمَّن شيء: كلُّ تعديلٍ من قاعدةٍ مسمّاة."""

    cl = clusters(surface)
    edits: list[Edit] = []

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

    # 4. WASL: ألفٌ بلا علامةٍ أوّلَ الكلمة قبل ساكنٍ = همزةُ وصل، بحركتها بالقاعدة:
    #    فتحةٌ في «ال»، وضمّةٌ إن كان ثالثُ الفعل مضمومًا، وإلّا كسرة (سيبويه).
    if len(cl) >= 3 and cl[0] == ALIF and (_bare(cl[1]) or SUKUN in cl[1] or SHADDA in cl[1]):
        if cl[1][0] == LAM:
            v = FATHA
        elif DAMMA in cl[2]:  # ثالثُ الفعل بعدّ الهمزة: ا ن صُ ر
            v = DAMMA
        else:
            v = KASRA
        cl[0] = ALIF_WASLA + v
        edits.append(("WASL", 0, ALIF))

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
        elif rule in ("ASSIM", "SHAMSI", "WASL_SILENT", "FARIQA"):
            cl.insert(i, removed)
        elif rule == "WASL":
            cl[0] = removed
        elif rule == "TANWIN_ALIF":
            cl[i] = cl[i].replace(FATHATAN, "", 1)
            cl[i + 1] = cl[i + 1][0] + FATHATAN
        elif rule == "IDGHAM":
            cl[0] = cl[0][0] + removed + cl[0][1:]
        else:
            raise ValueError(f"UNKNOWN_RULE:{rule}")
    return "".join(cl)
