"""سجلُّ مصالحةٍ موضعيٌّ لموادّ المقاييس: ينسب المقاطعَ ولا يمسّ الأصل.

كشفت مراجعةُ «أبت» أنّ صفًّا واحدًا في الجدول المختوم يحمل متنَ مادّتين:
«أبت» ثمّ «أبث». وكان أثرُ ذلك في `maqayis_link_candidates` تعليقًا عامًّا:
لا يُعتمَد مقطعٌ حتّى يُستوفى حدُّ المادّة كلِّها. وهذا **خلطُ شرطٍ بشرط**:
الحكمُ على مقطعٍ لا يحتاج أين تنتهي المادّة، بل أن يكون هذا النصُّ منها
(`A_SEGMENT_ATTRIBUTION_IS_NOT_A_SETTLED_MATERIAL_EXTENT`).

فهذه الوحدةُ تنقل العملَ من **تسجيل** التعليق إلى **معالجة** سببه:

* **الأصلُ لا يُمَسّ.** بايتاتُ `maqayis_by_root_csv_999.csv` وبصمتُها كما
  هي، والسجلُّ ههنا مُشتَقٌّ يُعاد بناؤه من تلك البايتات عند كلّ نداء؛
  ولا يُكتَب في الجدول صفٌّ ولا يُحذَف منه.
* **المقطعُ وحدةُ النسبة.** كلُّ بندٍ يحمل إزاحتيه ووحدتَهما ومُقتطَفَيه
  المقابَلَين بالبايتات، فيُقابَل البندُ بالمصدر ولا يُصدَّق على نفسه.
* **ثلاثةُ قراراتٍ لا اثنان.** ما ثبتت نسبتُه، وما نُقِضت، وما بقي
  ملتبسًا — والثالثُ بندٌ معلَّقٌ مستقلٌّ لا يُنسَب إلى مفتاح الصفّ لأنّه
  وقع فيه، ولا يُطرَح لأنّ جارَه أجنبيّ
  (`AN_UNRESOLVED_SEGMENT_STAYS_SUSPENDED_ON_ITS_OWN`).

وآلةُ الابتلاع صارت مقيسةً لا مظنونة: تركيبةُ «الهمزة والباء والثاء» **لا
تقع في الملفّ كلِّه ولا مرّةً واحدة**، بينما تقع ترويسةُ كلِّ واحدةٍ من
العشرين. فمادّةُ «أبث» لا ترويسةَ لها في هذه النسخة، وقاسمُ الصفوف يقسم
بالترويسة، فابتُلعت. وهذا تفسيرٌ لموضعِ الخلل لا عذرٌ له.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from alghanem.arabic.madlul_alone_formal import MadlulSection
from alghanem.arabic.maqayis_link_candidates import (
    AdmissionStanding,
    AttributionRoute,
    BoundaryStanding,
    InputUnitKind,
    LinkCandidate,
    MaqayisLinkCandidateError,
    ReviewAttestation,
    ReviewMethod,
    ReviewVerdict,
    SegmentAttribution,
    SegmentDecision,
    SourceReference,
    WitnessReference,
    _boundary_standing,
    _rows_of,
    _source_reference,
    verify,
)
from alghanem.arabic.maqayis_witness_census import weigh_declared_axes_count

__all__ = [
    "THE_ORIGINAL_BYTES_ARE_NEVER_EDITED",
    "THE_SWALLOWING_MECHANISM_IS_A_MISSING_HEAD_FORMULA",
    "THE_OFFSET_UNIT",
    "THE_ABAT_ROW_INDEX",
    "THE_ABAT_MATERIAL_KEY",
    "THE_ABAT_SEGMENTS",
    "THE_ABAT_TRANSITION_OFFSET",
    "THE_QUESTION_THAT_NEEDS_A_HUMAN_DECISION",
    "THE_REFERENCE_COPIES_TO_CONSULT",
    "MeaningExtraction",
    "THE_ABAT_EXTRACTION",
    "THE_EXTRACTIONS",
    "THE_SESSION_REVIEW_METHOD",
    "ReconciliationEntry",
    "reconciliation_ledger",
    "extracted_candidate",
    "extracted_review",
    "transition_evidence",
    "reconciliation_counts",
]

THE_ORIGINAL_BYTES_ARE_NEVER_EDITED: Final[str] = (
    "THE_ORIGINAL_BYTES_ARE_NEVER_EDITED: الجدولُ المختومُ مصدرٌ يُقرَأ ولا "
    "يُصحَّح. فلو أُصلِح الصفُّ بقَسمه إلى صفَّين لضاعت البصمةُ التي تُقابَل "
    "بها كلُّ شهادةٍ سابقة، ولصار المودَعُ تحريرًا لنا لا نسخةً لغيرنا. "
    "فالمصالحةُ طبقةٌ مُشتَقّةٌ فوقه: تُسمّي ما لم يُسمِّه، ولا تُبدِّل منه حرفًا."
)

THE_SWALLOWING_MECHANISM_IS_A_MISSING_HEAD_FORMULA: Final[str] = (
    "THE_SWALLOWING_MECHANISM_IS_A_MISSING_HEAD_FORMULA: ابتلاعُ «أبث» ليس "
    "خطأً عارضًا في صفٍّ واحد، بل أثرٌ لقاعدةٍ: قاسمُ الصفوف يقسم عند ترويسة "
    "«الهمزة و… و…»، وهذه التركيبةُ لمادّة «أبث» **لا تقع في الملفّ كلِّه ولا "
    "مرّةً واحدة**، فلم يجد القاسمُ أين يقسم فأُلحِقت بسابقتها. وهو مقيسٌ "
    "يُعاد اشتقاقُه، لا مظنون؛ ويُنبِّه إلى أنّ لهذا الابتلاع نظائرَ لم تُفحَص."
)

THE_OFFSET_UNIT: Final[str] = (
    "نقاطُ شفرةِ بايثون في `body_text` بعد تسويةِ NFC، والصفرُ أوّلُ الحقل"
)

THE_ABAT_ROW_INDEX: Final[int] = 12
THE_ABAT_MATERIAL_KEY: Final[str] = "أبت:13"

THE_ABAT_TRANSITION_OFFSET: Final[int] = 313
"""موضعُ انتقال المتن عن «أبت»؛ منتهى المقطع المحقَّق ومبتدأ الملتبس."""

THE_SESSION_REVIEW_METHOD: Final[ReviewMethod] = ReviewMethod(
    performed_by="وكيلُ Copilot في هذه الجلسة",
    is_human=False,
    is_independent=False,
    procedure=(
        "قراءةُ متنِ الصفّ من البايتات المختومة سطرًا سطرًا بإزاحاته، ثمّ "
        "قَسمُه عند تبدّلِ الحرف الثالث في صِيَغه، ثمّ مقابلةُ كلِّ بندٍ "
        "بترويسته وبالصفّ التالي، ثمّ تسميةُ ما لا يَحسِمه شيءٌ من ذلك "
        "التباسًا بدل إلحاقه بأقرب جار"
    ),
    materials_consulted=(
        "maqayis_by_root_csv_999.csv — الصفوف 12 و13 و14 من العيّنة",
        "تعدادُ تركيبةِ الترويسة في الملفّ كلِّه (5,539,405 بايتًا)",
    ),
)

THE_QUESTION_THAT_NEEDS_A_HUMAN_DECISION: Final[str] = (
    "البندُ الملتبسُ الأوّل هو المقطع [313, 358) من `body_text` في الرتبة 12: "
    "«وهذا الباب مهملٌ عند الخليل. قال الشّيبانىّ:». والسؤالُ المحدَّد: أهو "
    "خاتمةُ مادّة «أبت» أم مُفتتَحُ مادّة «أبث»؟ ولا يَحسِمه هذا المودَع: "
    "المقطعُ خالٍ من التاء والثاء معًا (0 و0)، فطريقُ اتّساق الجذر لا يعمل "
    "فيه؛ ولا ترويسةَ له؛ والمقابلةُ بالصفّ التالي تُجيب عن حدِّ الصفّ لا عن "
    "هذا البند. والحاسمُ نسخةٌ مرجعيّةٌ يُنظَر فيها: أتطبع «(أبث)» عنوانًا "
    "قبل هذه الجملة أم بعدها؟ وما يُبنى على الجواب: إن كانت مُفتتَحًا فالبندُ "
    "أجنبيٌّ عن «أبت»، وإن كانت خاتمةً فهي منه ويبقى ما بعدها أجنبيًّا."
)

THE_REFERENCE_COPIES_TO_CONSULT: Final[tuple[str, ...]] = (
    "تحقيق عبد السلام محمّد هارون، دار الفكر 1399هـ/1979م — الجزء الأوّل، "
    "بابُ الثلاثيّ الذي أوّلُه الهمزة؛ ويُطلَب تصويرُ الصفحة لا نصُّها المنقول",
    "المكتبة الشاملة: `shamela.ws/book/21710` — ومواضعُ «أبت»/«أبث» قريبةٌ من /78",
    "إسلام ويب: `islamweb.net/ar/library/content/124/25` — وفيه بحسب بحثٍ غيرِ "
    "مباشرٍ أنّ «(أبث)» عنوانٌ يَليه «وهذا الباب مهمل عند الخليل» مباشرةً",
)
"""نسخٌ تُقابَل بها، **لم تُفتَح ههنا**: كلُّ نطاقٍ خارجيٍّ محجوبٌ في هذا
المعمل (فشلُ ترجمةِ الاسم)، فطريقُ النسخة المرجعيّة غيرُ متوفّر بالقياس لا
بالدعوى. ولا يُسجَّل المنقولُ عن بحثٍ وسيطٍ شهادةً: جُرِّب فأخرج نصًّا
مُلفَّقًا مرّتين، فلا يُعتَدّ به إلّا تنبيهًا على موضعِ النظر."""


def _nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


_HARAKAT: Final[frozenset[str]] = frozenset(
    chr(code)
    for code in range(0x0610, 0x06A0)
    if unicodedata.category(chr(code)) == "Mn"
)


def _body_of(root: Path | None = None) -> str:
    """متنُ صفّ «أبت» مُسوًّى بـ NFC؛ يُنتزَع من البايتات عند كلّ طلب."""

    return _nfc(_rows_of(root)[THE_ABAT_ROW_INDEX]["body_text"])


def _bare(text: str) -> str:
    """تجريدُ العلامات المُركَّبة؛ تحويلٌ مُسمًّى يُعلَن قبل أيّ عدّ."""

    return "".join(character for character in text if character not in _HARAKAT)


THE_ABAT_SEGMENTS: Final[tuple[SegmentAttribution, ...]] = (
    SegmentAttribution(
        material_key=THE_ABAT_MATERIAL_KEY,
        row_index=THE_ABAT_ROW_INDEX,
        start_offset=0,
        end_offset=313,
        offset_unit=THE_OFFSET_UNIT,
        quoted_head="الهمزة والباء والتاء أصلٌ واحد",
        quoted_tail="الأَبْتة كالوَغْرة من القَيظ.\n",
        routes=(
            AttributionRoute.HEAD_FORMULA_NAMES_ITS_OWN_RADICALS,
            AttributionRoute.RADICAL_CONSISTENCY_TO_THE_FIRST_FOREIGN_FORM,
        ),
        decision=SegmentDecision.ATTRIBUTED_TO_THIS_MATERIAL,
        collation_source=(
            "البايتاتُ المختومةُ وحدَها: الترويسةُ تُسمّي الهمزةَ والباءَ "
            "والتاء، والمجالُ يحمل 12 صيغةً بالتاء و**صفرَ** صيغةٍ بالثاء"
        ),
        reviewer=THE_SESSION_REVIEW_METHOD.performed_by,
        method=THE_SESSION_REVIEW_METHOD.procedure,
        statement=(
            "مقطعٌ تابعٌ لمادّة «أبت»: يفتتح بترويستها التي تُسمّي حروفَها، "
            "ثمّ لا يخرج عن صِيَغ جذرها حتّى منتهاه. ولا يدّعي هذا البندُ "
            "أين تنتهي المادّةُ في النسخة المطبوعة، بل أنّ هذا النصَّ منها."
        ),
    ),
    SegmentAttribution(
        material_key=THE_ABAT_MATERIAL_KEY,
        row_index=THE_ABAT_ROW_INDEX,
        start_offset=313,
        end_offset=358,
        offset_unit=THE_OFFSET_UNIT,
        quoted_head="وهذا الباب مهملٌ عند الخليل",
        quoted_tail="قال الشّيبانىّ:\n",
        routes=(),
        decision=SegmentDecision.UNRESOLVED,
        collation_source="لا مصدرَ مقابلةٍ متوفّرًا؛ والنسخةُ المرجعيّةُ محجوبة",
        reviewer=THE_SESSION_REVIEW_METHOD.performed_by,
        method=THE_SESSION_REVIEW_METHOD.procedure,
        statement=THE_QUESTION_THAT_NEEDS_A_HUMAN_DECISION,
    ),
    SegmentAttribution(
        material_key=THE_ABAT_MATERIAL_KEY,
        row_index=THE_ABAT_ROW_INDEX,
        start_offset=358,
        end_offset=388,
        offset_unit=THE_OFFSET_UNIT,
        quoted_head="الأبِثُ الأشِرُ النّشيط",
        quoted_tail="قال:\n",
        routes=(AttributionRoute.RADICAL_CONSISTENCY_TO_THE_FIRST_FOREIGN_FORM,),
        decision=SegmentDecision.FOREIGN_TO_THIS_MATERIAL,
        collation_source="البايتاتُ المختومة: «الأبِث» صيغةُ جذرٍ ثالثُه ثاءٌ لا تاء",
        statement=(
            "تفسيرُ مُفرَدةٍ بالثاء مصدَّرةً بالتعريف، وهو مُفتتَحُ تفسيرِ "
            "مادّةٍ أخرى لا استشهادٌ داخل «أبت»."
        ),
        reviewer=THE_SESSION_REVIEW_METHOD.performed_by,
        method=THE_SESSION_REVIEW_METHOD.procedure,
    ),
    SegmentAttribution(
        material_key=THE_ABAT_MATERIAL_KEY,
        row_index=THE_ABAT_ROW_INDEX,
        start_offset=388,
        end_offset=497,
        offset_unit=THE_OFFSET_UNIT,
        quoted_head="إن تلق عمراً فقد لاقيت مدرعاً",
        quoted_tail="أمشى بعضب مجرد.\n",
        routes=(),
        decision=SegmentDecision.UNRESOLVED,
        collation_source="لا مصدرَ مقابلةٍ متوفّرًا",
        reviewer=THE_SESSION_REVIEW_METHOD.performed_by,
        method=THE_SESSION_REVIEW_METHOD.procedure,
        statement=(
            "بيتان مختلطا الشاهد: فيهما أربعُ تاءاتٍ وثاءٌ واحدة، وثانيهما "
            "«وبرك هجود» يُردِّد «بَرْك هجُود» الواقعَ في شاهد «أبت» قبلَه. "
            "فقد يكونان من جهاز شواهد «أبت» أُخِّرا في النقل، وقد يكونا من "
            "«أبث»؛ ولا يَحسِم بينهما هذا المودَع، فيبقيان بندًا مستقلًّا."
        ),
    ),
    SegmentAttribution(
        material_key=THE_ABAT_MATERIAL_KEY,
        row_index=THE_ABAT_ROW_INDEX,
        start_offset=497,
        end_offset=811,
        offset_unit=THE_OFFSET_UNIT,
        quoted_head="أصبَحَ عمَّارٌ نشيطا أبِثَا",
        quoted_tail="وناقة أبثَة.\n",
        routes=(AttributionRoute.RADICAL_CONSISTENCY_TO_THE_FIRST_FOREIGN_FORM,),
        decision=SegmentDecision.FOREIGN_TO_THIS_MATERIAL,
        collation_source="البايتاتُ المختومة: ستُّ صيغٍ بالثاء (أبِثَا · كَبِثَا · أبثَة)",
        reviewer=THE_SESSION_REVIEW_METHOD.performed_by,
        method=THE_SESSION_REVIEW_METHOD.procedure,
        statement=("ذيلُ الصفِّ كلُّه في «أبث» و«كبث»، ولا صيغةَ فيه من جذر «أبت»."),
    ),
)
"""خمسةُ بنودٍ لصفٍّ واحد: واحدٌ محقَّقٌ، واثنان أجنبيّان، واثنان ملتبسان.

ولا يُقال «الصفُّ مختلط» فحسب: مجالُ المحقَّق مُعيَّنٌ بإزاحتيه، وموضعُ
الانتقال مُسمًّى (313)، والملتبسُ محفوظٌ بسؤاله لا بإلحاقه بأقرب جار.
"""


# --- المعنى المستخرَج من مقطعٍ ثبتت نسبتُه ------------------------------------


@dataclass(frozen=True, slots=True)
class MeaningExtraction:
    """معنًى مُستخرَجٌ من متن المقطع: نصُّه الدالّ، ووجهُ إسناده، وحدودُه.

    ومصدرُه `body_text` بإزاحتين تُقابَلان بالبايتات، لا `semantic_axes`:
    فحقلُ المحاور صناعةُ ناقلٍ مُلخِّصةٌ قد تخالف المتن، والمتنُ هو الشاهد.
    """

    material_key: str
    row_index: int
    signifying_start: int
    signifying_end: int
    offset_unit: str
    signifying_text: str
    extracted_meaning: str
    mode_of_support: str
    qualifications: tuple[str, ...]
    generalisation_limits: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.extracted_meaning.strip() or not self.mode_of_support.strip():
            raise MaqayisLinkCandidateError("استخراجٌ بلا معنًى أو بلا وجهِ إسنادٍ يُرَدّ.")
        if self.signifying_end <= self.signifying_start:
            raise MaqayisLinkCandidateError("مجالُ النصّ الدالّ غيرُ خالٍ.")


THE_ABAT_EXTRACTION: Final[MeaningExtraction] = MeaningExtraction(
    material_key=THE_ABAT_MATERIAL_KEY,
    row_index=THE_ABAT_ROW_INDEX,
    signifying_start=0,
    signifying_end=49,
    offset_unit=THE_OFFSET_UNIT,
    signifying_text="الهمزة والباء والتاء أصلٌ واحد، وهو الحرّ وشدّته.",
    extracted_meaning="الحرّ وشدّته",
    mode_of_support=(
        "تنصيصٌ من المؤلِّف على أصل المادّة بصيغته المعهودة «أصلٌ واحد، وهو "
        "كذا»؛ فالإسنادُ بتصريحه لا باستنباطٍ من استعمالٍ ولا بمطابقةٍ نصّيّة. "
        "ويُصدِّقه ما بعده في المقطع نفسِه: «أَبَتَ يومنا… إذا اشتدّ حرُّه»"
    ),
    qualifications=(
        "لا نفيَ في المقطع ولا تركيبَ امتناع؛ و«وهذا الباب مهملٌ عند الخليل» "
        "واقعةٌ خارجَ المقطع في البند الملتبس، فلا تُحمَل عليه ولا تُطرَح",
        "استدراكٌ بالتشبيه لا خلافٌ في الأصل: «قال أبو على الأصفهانىّ: "
        "الأَبْتة كالوَغْرة من القَيظ»",
        "النصُّ الدالُّ يقول «الحرّ وشدّته» بالشدّة، وحقلُ `semantic_axes` "
        "يقول «الحر وشدته» بدونها؛ فهما نصّان لا نصٌّ واحد، والمُعتمَدُ المتن",
    ),
    generalisation_limits=(
        "أصلُ المادّة عند هذا المؤلِّف في هذه النسخة؛ لا معنى كلِّ مشتقٍّ منها "
        "(`A_ROOT_ORIGIN_IS_NOT_THE_MEANING_OF_EVERY_DERIVATIVE`)",
        "لا يمتدّ إلى وقوعِ لفظٍ من المادّة في تركيبٍ بعينه",
        "نسخةٌ واحدةٌ لم تُقابَل بثانية، فاستقرارُ اللفظ عبر النسخ غيرُ مقيس",
    ),
)


THE_EXTRACTIONS: Final[tuple[MeaningExtraction, ...]] = (THE_ABAT_EXTRACTION,)
"""الاستخراجاتُ المودَعة؛ واحدٌ اليوم، والعددُ يُعَدّ منها لا يُكتَب."""


def extracted_review(
    extraction: MeaningExtraction = THE_ABAT_EXTRACTION,
) -> ReviewAttestation:
    """المراجعةُ المودَعةُ لهذا الاستخراج، موثَّقةَ المنهج ومنفِّذِها.

    و`SUPPORTS_THE_MEANING` ههنا **نتيجةٌ** لا مفتاح: لا تُنشَأ المراجعةُ
    أصلًا بلا `ReviewMethod` ولا بلا وجهِ إسنادٍ مكتوب، ومنفِّذُها مُصرَّحٌ
    بأنّه آليٌّ غيرُ مستقلّ
    (`AN_AGENT_REVIEW_IS_NOT_A_HUMAN_OR_INDEPENDENT_REVIEW`).
    """

    return ReviewAttestation(
        material_key=extraction.material_key,
        candidate_meaning=extraction.extracted_meaning,
        witness_text=extraction.signifying_text,
        reviewer=THE_SESSION_REVIEW_METHOD.performed_by,
        statement=(
            "نُظِر في النصّ الدالّ بإزاحتيه، فوُجِد المعنى مُصرَّحًا به في "
            "المتن لا مُستنبَطًا، ومُصدَّقًا بما يليه في المقطع نفسِه، ولم "
            "يُوجَد في المقطع ما ينفيه. والمقطعُ ثابتُ النسبة ببندٍ مودَعٍ "
            "بطريقَين، فالحكمُ عليه لا ينتظر استيفاءَ حدِّ المادّة."
        ),
        method=THE_SESSION_REVIEW_METHOD,
        verdict=ReviewVerdict.SUPPORTS_THE_MEANING,
        mode_of_support=extraction.mode_of_support,
        qualifications=extraction.qualifications,
        generalisation_limits=extraction.generalisation_limits,
    )


def _boundary_of(root: Path | None, row_index: int) -> BoundaryStanding:
    """حالُ حدِّ الصفّ بالكاشف وحدَه؛ يُعرَض ولا يُشترَط للحكم على مقطع."""

    return _boundary_standing(_rows_of(root)[row_index], row_index, ())


def extracted_candidate(
    root: Path | None = None,
    extraction: MeaningExtraction = THE_ABAT_EXTRACTION,
) -> LinkCandidate:
    """مرشَّحٌ معناه من المتن لا من `semantic_axes`، وشاهدُه مقطعُه الدالّ.

    ويُبنى من البايتات عند كلّ نداء: لو زاغت إزاحةٌ أو تبدّل حرفٌ في النسخة
    لم يُبنَ المرشَّحُ أصلًا، فلا يُحمَل خطأُ نقلٍ إلى بابِ الاعتماد.
    """

    rows = _rows_of(root)
    row = rows[extraction.row_index]
    body = _nfc(row["body_text"])
    span = body[extraction.signifying_start : extraction.signifying_end]
    if span != extraction.signifying_text:
        raise MaqayisLinkCandidateError(
            "النصُّ الدالُّ لا يُستخرَج بإزاحتيه من هذه النسخة؛ لا يُبنى مرشَّح."
        )
    if extraction.extracted_meaning not in span:
        raise MaqayisLinkCandidateError("المعنى المستخرَجُ ليس مقتطعًا من نصّه الدالّ.")
    return LinkCandidate(
        material_key=extraction.material_key,
        row_index=extraction.row_index,
        root_full=row["root_full"],
        root_display=row["root_display"].strip(),
        entry_num=row["entry_num"],
        source=_source_reference(root),
        extraction_method=(
            "استخراجٌ من `body_text` بإزاحتين: تُؤخَذ جملةُ التنصيص على الأصل، "
            "ويُقتطَع منها ما بعد «وهو» إلى منتهى الجملة؛ ولا يُقرَأ "
            "`semantic_axes` في هذا الطريق البتّة"
        ),
        input_unit=InputUnitKind.ROOT_KEY_DISPLAY_FORM,
        candidate_meaning=extraction.extracted_meaning,
        meaning_field="body_text",
        axis_index=0,
        axis_total=1,
        witness=WitnessReference(
            field_name="body_text",
            start_offset=extraction.signifying_start,
            end_offset=extraction.signifying_end,
            offset_unit=extraction.offset_unit,
            text=span,
        ),
        boundary=_boundary_of(root, extraction.row_index),
        axes_count_standing=weigh_declared_axes_count(row),
        alternatives=(),
        signification_kind=None,
        madlul_section=MadlulSection.MEANING,
    )


# --- السجلّ ---------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ReconciliationEntry:
    """بندُ سجلٍّ مُقابَلٌ بالبايتات عند بنائه؛ لا يُصدَّق بندٌ على نفسه."""

    row_index: int
    row_key: str
    source: SourceReference
    start_offset: int
    end_offset: int
    offset_unit: str
    attributed_material: str | None
    attribution_witness: str
    routes: tuple[AttributionRoute, ...]
    collation_source: str
    decision: SegmentDecision
    reproduces_from_bytes: bool
    text_length: int


def reconciliation_ledger(
    root: Path | None = None,
    segments: tuple[SegmentAttribution, ...] = THE_ABAT_SEGMENTS,
) -> tuple[ReconciliationEntry, ...]:
    """ابنِ السجلَّ من البايتات، وقابِل كلَّ بندٍ بمُقتطَفَيه قبل قبوله.

    و`reproduces_from_bytes` حكمٌ مُشتَقٌّ لا حقلٌ يُكتَب: يصير كاذبًا متى
    زاغت إزاحةٌ أو تبدّلت نسخةٌ، فيَظهر الزيغُ ههنا لا في نثرٍ مكتوب.
    """

    rows = _rows_of(root)
    source = _source_reference(root)
    entries: list[ReconciliationEntry] = []
    for segment in segments:
        row = rows[segment.row_index]
        body = _nfc(row["body_text"])
        span = body[segment.start_offset : segment.end_offset]
        reproduces = bool(
            span
            and span.startswith(_nfc(segment.quoted_head))
            and span.endswith(_nfc(segment.quoted_tail))
        )
        entries.append(
            ReconciliationEntry(
                row_index=segment.row_index,
                row_key=f"{row['root_full']}:{row['entry_num']}",
                source=source,
                start_offset=segment.start_offset,
                end_offset=segment.end_offset,
                offset_unit=segment.offset_unit,
                attributed_material=(
                    segment.material_key if segment.is_established else None
                ),
                attribution_witness=segment.statement,
                routes=segment.established_routes,
                collation_source=segment.collation_source,
                decision=segment.decision,
                reproduces_from_bytes=reproduces,
                text_length=len(span),
            )
        )
    return tuple(entries)


def transition_evidence(root: Path | None = None) -> dict[str, int]:
    """شاهدُ موضعِ الانتقال مقيسًا من البايتات: الجذرُ الثالثُ قبلَه وبعدَه.

    و«الثاء» هي الحدُّ الظاهر: ما قبل الإزاحة خالٍ منها بالكلّيّة وهو يحمل
    التاءَ اثنتَي عشرةَ مرّة، وما بعدها يحملها. وهذا شاهدُ اتّساقٍ لا برهانُ
    حدّ: لا يُخرِج موضعَ الانتقال، بل يُصدِّق موضعًا اقتُرِح.
    """

    body = _body_of(root)
    before = _bare(body[:THE_ABAT_TRANSITION_OFFSET])
    after = _bare(body[THE_ABAT_TRANSITION_OFFSET:])
    return {
        "تاءٌ_قبل_الانتقال": before.count("ت"),
        "ثاءٌ_قبل_الانتقال": before.count("ث"),
        "تاءٌ_بعد_الانتقال": after.count("ت"),
        "ثاءٌ_بعد_الانتقال": after.count("ث"),
    }


def reconciliation_counts(
    root: Path | None = None,
    segments: tuple[SegmentAttribution, ...] = THE_ABAT_SEGMENTS,
) -> dict[str, int]:
    """الأعدادُ بوحداتها مفصولةً؛ ولا يُجمَع صفٌّ إلى مقطعٍ ولا مقطعٌ إلى معنًى."""

    ledger = reconciliation_ledger(root, segments)
    return {
        "صفوف_مصالَحة": len({entry.row_index for entry in ledger}),
        "موادّ_مميَّزة_في_الصفوف": len({entry.row_key for entry in ledger})
        + len(
            {
                entry.row_index
                for entry in ledger
                if entry.decision is SegmentDecision.FOREIGN_TO_THIS_MATERIAL
            }
        ),
        "مقاطع": len(ledger),
        "مقاطع_ثابتة_النسبة": sum(
            1
            for entry in ledger
            if entry.decision is SegmentDecision.ATTRIBUTED_TO_THIS_MATERIAL
        ),
        "مقاطع_منقوضة_النسبة": sum(
            1
            for entry in ledger
            if entry.decision is SegmentDecision.FOREIGN_TO_THIS_MATERIAL
        ),
        "مقاطع_ملتبسة": sum(
            1 for entry in ledger if entry.decision is SegmentDecision.UNRESOLVED
        ),
        "معانٍ_مستخرَجة_من_المتن": len(THE_EXTRACTIONS),
        "أزواج_معتمَدة": sum(
            1
            for extraction in THE_EXTRACTIONS
            if verify(
                extracted_candidate(root),
                root=root,
                segments=segments,
                reviews=(extracted_review(),),
            ).standing
            is AdmissionStanding.ADMITTED
            and extraction is THE_ABAT_EXTRACTION
        ),
    }
