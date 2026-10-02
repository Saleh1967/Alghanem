"""آلةُ المرشَّحات: ربطٌ معجميٌّ مُرشَّحٌ بين مفتاح مادّةٍ ومعنًى، بثلاث شهادات.

هذه الوحدةُ تُخرِج **مرشَّحَ ربطٍ معجميّ**، ولا تُخرِج زوجًا معتمَدًا إلّا
باستيفاء شروطه؛ والفرقُ بينهما مبنيٌّ في النوع لا موصوفٌ في النثر::

    LinkCandidate        != AdmittedLink
    ASourceOfAccess      != AKindOfSignification
    AQuotedAxisField     != AnExtractedWitness
    FindingTheWordOrigin != SupportingThisMeaning
    AbsentEvidence       != EvidenceOfAbsence

**أوّلًا: وحدةُ المدخل مُسمّاةٌ ومقيسة.** العشرون المُنتزَعةُ من `root_display`
ليست ألفاظًا مستعملةً ولا عناوينَ موادّ: هي **صورةُ عرضٍ لمفتاح جذر**. وهذا
مقيسٌ لا مُدَّعًى: `input_unit_reading` تقيس كم منها يخالف `root_full` (طيُّ
التضعيف في المضاعف: «أجج» تُعرَض «أج»)، وكم منها يحمل حركةً مكتوبة. فمفتاحٌ
مطويُّ التضعيف عاري الحركة ليس لفظًا وقع في نصّ
(`A_ROOT_KEY_DISPLAY_FORM_IS_NOT_A_USED_WORD`).

**وثانيًا: السلسلةُ خمسُ وصلاتٍ لا وصلةٌ واحدة.** مفتاحُ المادّة ← المادّةُ
المحقَّقة ← المعنى المستخرَج ← اللفظُ ← الاستعمال. وهذه الآلةُ تبلغ الثالثةَ
بشرطها، وتقف عند الرابعة **امتناعًا مُعلَنًا داخل النظام** لا نقصَ دليل: أصلُ
الجذر عند ابن فارس لا يصير معنًى تلقائيًّا لكلّ مشتقٍّ ولا لكلّ وقوع
(`A_ROOT_ORIGIN_IS_NOT_THE_MEANING_OF_EVERY_DERIVATIVE`).

**وثالثًا: المصدرُ ليس نوعَ دلالة.** «مقاييس اللغة» مصدرٌ وطريقةُ وصول، فلا
يُضاف قناةً رابعةً إلى المطابقة والتضمّن والالتزام. ولذلك يُمثَّل كلُّ واحدٍ
منفصلًا: المصدرُ ونسختُه، وطريقةُ الاستخراج، ونوعُ وحدة المدخل، والمعنى
المرشَّح، ونوعُ الدلالة **إن ثبت**، وحالُ الاعتماد
(`A_SOURCE_IS_A_ROUTE_OF_ACCESS_NOT_A_KIND_OF_SIGNIFICATION`).

وغيابُ النصّ الحاكم (ج٣) يُعلِّق **ما يتبعه وحدَه**: تصنيفَ نوع الدلالة. ويبقى
العملُ المعجميُّ ماضيًا بشهاداته، فلا يُقفَل بابٌ بغياب مفتاحِ بابٍ آخر
(`THE_ABSENCE_OF_ONE_SOURCE_SUSPENDS_ONLY_WHAT_DEPENDS_ON_IT`). وحضورُ النصّ
الحاكم لا يُثبِت بنفسه انطباقَ قسمٍ دلاليٍّ على زوجٍ بعينه.

**ورابعًا: `semantic_axes` يُولِّد المرشَّح ولا يشهد له.** العمودُ مُسوًّى
مُعادُ الصياغة لا منقولًا من المتن، وقد سُمّي خللُه قبلَ هذه الوحدة في
`maqayis_semantic_leak_audit`. فيُستعمَل **مولِّدًا** فقط، وتُفحَص لكلّ مرشَّحٍ
ثلاثُ شهاداتٍ **منفصلة**:

1. سلامةُ المصدر: الشاهدُ واقعٌ في البايتات المختومة بعينها.
2. صحّةُ النسبة: الشاهدُ تابعٌ للمادّة المقصودة ضمن حدٍّ محقَّق — ويُقاس
   بمِسبارٍ لا يُصدِّق نفسَه: أتُسمّي جملةُ الشاهد حروفَ جذرِ صفِّها؟
3. كفايةُ الاستشهاد: أيُسنِد الشاهدُ **هذا المعنى بعينه**؟ ووقوعُ لفظ
   «أصل» في المتن، أو وقوعُ المقتطف داخل الملفّ، لا يُثبِت هذه الثالثة
   (`FINDING_THE_WORD_ORIGIN_DOES_NOT_SUPPORT_A_PARTICULAR_MEANING`).

**وخامسًا: حدُّ المادّة يُستدعى ولا يُستأنَف.** تصنيفُ الترويسة قائمٌ في
`maqayis_deviation_attribution.classify_header`، فيُستعمَل كما هو: ترويسةٌ
غائبةٌ أو فاسدةٌ حدٌّ مشتبه، فتُعلَّق النتائجُ التابعة له. ومراجعةُ مادّةٍ
واحدةٍ لا تفتح سائرَ الموادّ
(`A_REVIEWED_MATERIAL_DOES_NOT_OPEN_ITS_NEIGHBOURS`).

**وسادسًا: النصُّ الأصليُّ محفوظ، والتسويةُ طبقةٌ مستقلّةٌ تُسمّى.** تجريدُ
التشكيل أداةٌ تُسجَّل نتيجتُها باسمها `SUPPORTED_UNDER_A_NAMED_NORMALISATION`،
ولا تُقرأ موافقةً حرفيّة. ومقتطفُ العرض مفصولٌ عن مرجع الشاهد الكامل، فحدُّ
الطول لا يبتر ما يُتحقَّق به (`A_DISPLAY_EXCERPT_IS_NOT_THE_EVIDENCE`).

**وسابعًا: الترخيصُ لكلّ مرشَّحٍ على حدة.** لا يُرخَّص ملفٌّ لأنّ أزواجًا خرجت
منه، ولا يُقرأ المعلَّقُ مرفوضًا، ولا يُقرأ غيابُ الشاهد إثباتًا لعدم المعنى.
وأسبابُ التعليق أربعةٌ مفصولةٌ بأعيانها في `SuspensionGenus`.

**وثامنًا: لا شيءَ ههنا مولَّدٌ من البنية.** المعنى المرشَّحُ **منقولٌ من
رصيدٍ** معجميّ، لا مولَّدٌ من الـ١١٦ ولا مُثبَتٌ بعمليّة ربط؛ والنسبُ الثلاثُ
تُخرَج معدودةً في `provenance_shares` فلا تُدَّعى ولادةٌ لم تقع
(`A_TRANSPORTED_MEANING_IS_NOT_A_GENERATED_ONE`).

تسجيلٌ لا سلطة: لا ولادةَ ههنا، ولا حكمَ ولادةٍ، ولا تجميدَ `E0`، ولا استيرادَ
من `kernel/`، ولا يُقرأ اعتمادُ ربطٍ معجميٍّ تصديقًا لواقعةٍ خارج اللغة
(`AN_ADMITTED_LEXICAL_LINK_ASSERTS_NO_EXTERNAL_FACT`).
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Final

from .dal_madlul_bridge import (
    THE_DECLARED_MATERIALS,
    SealStanding,
    governing_seal_reading,
    seal_reading_for,
)
from .dalalat_thalath import DalalaKind
from .madlul_alone_formal import MadlulSection
from .maqayis_deviation_attribution import HeaderForm, classify_header
from .maqayis_root_table_deposit import (
    ROOT_TABLE_RELATIVE_PATH,
    root_table_rows,
)
from .maqayis_witness_census import (
    AXES_AGREEMENT_COUNTING_RULE,
    AxesStanding,
    split_witness_segments,
    weigh_declared_axes_count,
)
from .quran_corpus_word_total import strip_diacritics

__all__ = [
    "AN_ADMITTED_LEXICAL_LINK_ASSERTS_NO_EXTERNAL_FACT",
    "A_DISPLAY_EXCERPT_IS_NOT_THE_EVIDENCE",
    "A_PROCESSED_FIELD_IS_NOT_AN_EXHAUSTED_MEANING",
    "A_REVIEWED_MATERIAL_DOES_NOT_OPEN_ITS_NEIGHBOURS",
    "A_ROOT_KEY_DISPLAY_FORM_IS_NOT_A_USED_WORD",
    "A_ROOT_ORIGIN_IS_NOT_THE_MEANING_OF_EVERY_DERIVATIVE",
    "A_SOURCE_IS_A_ROUTE_OF_ACCESS_NOT_A_KIND_OF_SIGNIFICATION",
    "A_TRANSPORTED_MEANING_IS_NOT_A_GENERATED_ONE",
    "FINDING_THE_WORD_ORIGIN_DOES_NOT_SUPPORT_A_PARTICULAR_MEANING",
    "MAQAYIS_LINK_CANDIDATE_NAMED_RESIDUALS",
    "THE_ABSENCE_OF_ONE_SOURCE_SUSPENDS_ONLY_WHAT_DEPENDS_ON_IT",
    "THE_ADMISSION_RULE",
    "THE_CANDIDATE_SAMPLE_RULE",
    "THE_CANDIDATE_SAMPLE_SIZE",
    "THE_DISPLAY_EXCERPT_LIMIT",
    "THE_EXTRACTION_METHOD",
    "THE_LETTER_NAMES",
    "THE_OFFSET_UNIT",
    "THE_REFUSAL_FORMULAE",
    "THE_WITNESS_SELECTION_RULE",
    "AdmissionStanding",
    "AttributionCheck",
    "BoundaryStanding",
    "DalProcessing",
    "DalReading",
    "InputUnitKind",
    "InputUnitReading",
    "LinkCandidate",
    "LinkChainRung",
    "MaqayisLinkCandidateError",
    "ProvenanceShares",
    "ReviewAttestation",
    "SourceReference",
    "SufficiencyCheck",
    "SuspensionGenus",
    "VerificationReading",
    "WitnessReference",
    "candidate_counts",
    "chain_reach",
    "dal_readings",
    "input_unit_reading",
    "link_candidates",
    "provenance_shares",
    "report_rows",
    "verify",
]


class MaqayisLinkCandidateError(ValueError):
    """رفضٌ صريحٌ عند الآلة؛ ولا يُحمَل مدخلٌ مرفوضٌ على أقرب حالةٍ مقبولة."""


# --- البقايا المُسمّاة -------------------------------------------------------

A_ROOT_KEY_DISPLAY_FORM_IS_NOT_A_USED_WORD: Final[str] = (
    "A_ROOT_KEY_DISPLAY_FORM_IS_NOT_A_USED_WORD: `root_display` صورةُ عرضٍ "
    "لمفتاح جذرٍ مطويِّ التضعيف عاري الحركة، لا لفظٌ وقع في نصٍّ ولا عنوانُ "
    "مادّة؛ ومن عدَّه لفظًا مستعملًا نسب إلى الاستعمال ما لم يُقَس فيه"
)

A_ROOT_ORIGIN_IS_NOT_THE_MEANING_OF_EVERY_DERIVATIVE: Final[str] = (
    "A_ROOT_ORIGIN_IS_NOT_THE_MEANING_OF_EVERY_DERIVATIVE: أصلُ الجذر عند "
    "ابن فارس حكمٌ على المادّة، فلا يُحمَل معنًى تلقائيًّا على كلّ مشتقٍّ منها "
    "ولا على كلّ وقوعٍ لها في عبارة؛ والوصلتان الرابعةُ والخامسةُ ممتنعتان "
    "ههنا امتناعًا مُعلَنًا داخل النظام لا تعذُّرَ أداةٍ ولا غيابَ دليل"
)

A_SOURCE_IS_A_ROUTE_OF_ACCESS_NOT_A_KIND_OF_SIGNIFICATION: Final[str] = (
    "A_SOURCE_IS_A_ROUTE_OF_ACCESS_NOT_A_KIND_OF_SIGNIFICATION: المقاييسُ "
    "مصدرٌ وطريقةُ وصول، والمطابقةُ والتضمّنُ والالتزامُ أقسامُ دلالةٍ من "
    "قسمةٍ أخرى؛ فإضافةُ المصدر إليها قناةً رابعةً خلطُ وعاءٍ بقسمة"
)

THE_ABSENCE_OF_ONE_SOURCE_SUSPENDS_ONLY_WHAT_DEPENDS_ON_IT: Final[str] = (
    "THE_ABSENCE_OF_ONE_SOURCE_SUSPENDS_ONLY_WHAT_DEPENDS_ON_IT: غيابُ النصّ "
    "الحاكم يُعلِّق تصنيفَ نوع الدلالة وحدَه، ويبقى العملُ المعجميُّ ماضيًا "
    "بشهاداته؛ وحضورُه لا يُثبِت بنفسه انطباقَ قسمٍ على زوجٍ بعينه"
)

FINDING_THE_WORD_ORIGIN_DOES_NOT_SUPPORT_A_PARTICULAR_MEANING: Final[str] = (
    "FINDING_THE_WORD_ORIGIN_DOES_NOT_SUPPORT_A_PARTICULAR_MEANING: وقوعُ "
    "«أصل» أو «أصلان» في المتن، ووقوعُ المقتطف داخل الملفّ، شهادتان من "
    "الأوّلتين لا الثالثة؛ وكفايةُ الاستشهاد أن يُسنِد الشاهدُ هذا المعنى "
    "بعينه، وتُبيَّن معها العلاقةُ بين عبارته والصياغة المستخرَجة"
)

A_REVIEWED_MATERIAL_DOES_NOT_OPEN_ITS_NEIGHBOURS: Final[str] = (
    "A_REVIEWED_MATERIAL_DOES_NOT_OPEN_ITS_NEIGHBOURS: المراجعةُ تُودَع "
    "لمادّةٍ بمفتاحها ومعنًى بنصّه، فلا تُقرأ إذنًا عامًّا في سائر الموادّ "
    "ولا في سائر معاني المادّة نفسِها"
)

A_DISPLAY_EXCERPT_IS_NOT_THE_EVIDENCE: Final[str] = (
    "A_DISPLAY_EXCERPT_IS_NOT_THE_EVIDENCE: المقتطفُ المقطوعُ عرضٌ، والشاهدُ "
    "مرجعُه الكاملُ بإزاحتيه ووحدةِ إزاحته؛ فلا يُبتَر بحدِّ عرضٍ ما يُعاد به "
    "التحقّق، ولا يُتحقَّق من المقتطف بدلًا من مرجعه"
)

A_TRANSPORTED_MEANING_IS_NOT_A_GENERATED_ONE: Final[str] = (
    "A_TRANSPORTED_MEANING_IS_NOT_A_GENERATED_ONE: المعنى ههنا منقولٌ من "
    "رصيدٍ معجميّ، لا مولَّدٌ من بنيةٍ ولا مُثبَتٌ بعمليّة ربط؛ والنسبُ الثلاثُ "
    "تُعَدّ وتُعرَض، فلا تُدَّعى ولادةٌ لم تقع"
)

A_PROCESSED_FIELD_IS_NOT_AN_EXHAUSTED_MEANING: Final[str] = (
    "A_PROCESSED_FIELD_IS_NOT_AN_EXHAUSTED_MEANING: «عولجت محاورُه المُعلَنةُ "
    "كلُّها» حكمٌ على الحقول المتاحة في هذا الملفّ، لا على معاني المادّة في "
    "العربيّة؛ فاكتمالُ المعالجة ليس استيفاءً للمعاني الممكنة"
)

AN_ADMITTED_LEXICAL_LINK_ASSERTS_NO_EXTERNAL_FACT: Final[str] = (
    "AN_ADMITTED_LEXICAL_LINK_ASSERTS_NO_EXTERNAL_FACT: اعتمادُ ربطٍ معجميٍّ "
    "يقول إنّ هذا المصدرَ أسند هذا المعنى لهذه المادّة، ولا يقول إنّ شيئًا "
    "في العالم وقع؛ ولا يُشتَقّ منه تصديقُ واقعةٍ خارجَ اللغة"
)

MAQAYIS_LINK_CANDIDATE_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "A_ROOT_KEY_DISPLAY_FORM_IS_NOT_A_USED_WORD": (
        A_ROOT_KEY_DISPLAY_FORM_IS_NOT_A_USED_WORD
    ),
    "A_ROOT_ORIGIN_IS_NOT_THE_MEANING_OF_EVERY_DERIVATIVE": (
        A_ROOT_ORIGIN_IS_NOT_THE_MEANING_OF_EVERY_DERIVATIVE
    ),
    "A_SOURCE_IS_A_ROUTE_OF_ACCESS_NOT_A_KIND_OF_SIGNIFICATION": (
        A_SOURCE_IS_A_ROUTE_OF_ACCESS_NOT_A_KIND_OF_SIGNIFICATION
    ),
    "THE_ABSENCE_OF_ONE_SOURCE_SUSPENDS_ONLY_WHAT_DEPENDS_ON_IT": (
        THE_ABSENCE_OF_ONE_SOURCE_SUSPENDS_ONLY_WHAT_DEPENDS_ON_IT
    ),
    "FINDING_THE_WORD_ORIGIN_DOES_NOT_SUPPORT_A_PARTICULAR_MEANING": (
        FINDING_THE_WORD_ORIGIN_DOES_NOT_SUPPORT_A_PARTICULAR_MEANING
    ),
    "A_REVIEWED_MATERIAL_DOES_NOT_OPEN_ITS_NEIGHBOURS": (
        A_REVIEWED_MATERIAL_DOES_NOT_OPEN_ITS_NEIGHBOURS
    ),
    "A_DISPLAY_EXCERPT_IS_NOT_THE_EVIDENCE": A_DISPLAY_EXCERPT_IS_NOT_THE_EVIDENCE,
    "A_TRANSPORTED_MEANING_IS_NOT_A_GENERATED_ONE": (
        A_TRANSPORTED_MEANING_IS_NOT_A_GENERATED_ONE
    ),
    "A_PROCESSED_FIELD_IS_NOT_AN_EXHAUSTED_MEANING": (
        A_PROCESSED_FIELD_IS_NOT_AN_EXHAUSTED_MEANING
    ),
    "AN_ADMITTED_LEXICAL_LINK_ASSERTS_NO_EXTERNAL_FACT": (
        AN_ADMITTED_LEXICAL_LINK_ASSERTS_NO_EXTERNAL_FACT
    ),
}
"""البقايا المُسمّاةُ مجموعةً؛ وكلُّ اسمٍ منها مُصدَّرٌ بنصّه لا بعنوانه."""


# --- وحدةُ المدخل ------------------------------------------------------------


class InputUnitKind(Enum):
    """نوعُ وحدة المدخل؛ مُعلَنٌ قبل أن يُقرأ عنه رقم، ولا رابعَ يُحمَل عليه."""

    ROOT_KEY_DISPLAY_FORM = "صورةُ عرضٍ لمفتاح جذر"
    MATERIAL_TITLE = "عنوانُ مادّة"
    USED_WORD = "لفظٌ مستعمَل"


@dataclass(frozen=True, slots=True)
class InputUnitReading:
    """قراءةُ نوعِ وحدة المدخل مقيسةً: كم طُوِي تضعيفُه، وكم حمل حركة."""

    examined: int
    equal_to_root_full: int
    collapsed_gemination: int
    bearing_a_written_haraka: int

    @property
    def kind(self) -> InputUnitKind:
        """النوعُ مُشتَقٌّ من القياس: مفتاحٌ لا لفظٌ ما دام عاريَ الحركة."""

        if self.bearing_a_written_haraka == 0:
            return InputUnitKind.ROOT_KEY_DISPLAY_FORM
        return InputUnitKind.USED_WORD


# --- سلسلةُ الوصلات ----------------------------------------------------------


class LinkChainRung(Enum):
    """وصلاتُ السلسلة الخمس بترتيبها؛ وبلوغُ وصلةٍ لا يُدَّعى بلا شرطها."""

    MATERIAL_KEY = "مفتاحُ المادّة"
    VERIFIED_MATERIAL = "المادّةُ المحقَّقة"
    EXTRACTED_MEANING = "المعنى المستخرَج"
    LAFZ = "اللفظ"
    USAGE = "الاستعمال"


THE_EXTRACTION_METHOD: Final[str] = (
    "تُقرأ صفوفُ البايتات المختومة بقارئ `maqayis_root_table_deposit` وحدَه؛ "
    "ثمّ يُولَّد مرشَّحٌ عن كلّ مقطعٍ من `semantic_axes` تحت قاعدة الفصل "
    "القائمة في `maqayis_witness_census.split_witness_segments`، ويُنتزَع "
    "شاهدُه من `body_text` تحت `THE_WITNESS_SELECTION_RULE`. ولا يُولَّد "
    "مرشَّحٌ من `axes_count` ولا من `poetry_evidence`"
)

THE_WITNESS_SELECTION_RULE: Final[str] = (
    "شاهدُ المرشَّح جملةُ `body_text` الأولى، وحدُّها أوّلُ نقطةٍ أو فاصلِ "
    "سطرٍ بعد مَطلع النصّ، وتدخل علامةُ الوقف في الجملة. والقاعدةُ مكتوبةٌ "
    "قبل النظر في نتيجتها، ولا تُنتقى جملةٌ من وسط المتن توافق معنًى مطلوبًا"
)

THE_OFFSET_UNIT: Final[str] = (
    "الإزاحتان مَعدودتان بنقاط الشفرة في `body_text` بعد تسويته بـ NFC، "
    "ومبدؤهما أوّلُ الحقل لا أوّلُ الملفّ؛ ووحدةُ الإزاحة مكتوبةٌ لأنّ البايتةَ "
    "والمحرفَ والنقطةَ تُعطي ثلاثةَ أعدادٍ مختلفة"
)

THE_DISPLAY_EXCERPT_LIMIT: Final[int] = 160
"""حدُّ مقتطفِ العرض بنقاط الشفرة؛ عرضٌ مقطوعٌ لا شاهدٌ مبتور.

ومرجعُ الشاهد الكامل محفوظٌ بإزاحتيه في `WitnessReference`، فيُعاد انتزاعُه
من البايتات تامًّا ولو طال.
"""


# --- المصدرُ ونسختُه ----------------------------------------------------------


@dataclass(frozen=True, slots=True)
class SourceReference:
    """المصدرُ ونسختُه: مسارُه، وطولُ بايتاته، وبصمتُها كما قِيست لا كما أُعلِنت."""

    material_key: str
    relative_path: str
    measured_byte_length: int
    measured_sha256: str

    def __post_init__(self) -> None:
        if len(self.measured_sha256) != 64:
            raise MaqayisLinkCandidateError("بصمةُ النسخة SHA-256 ستّ عشريّةٌ كاملة.")


@lru_cache(maxsize=4)
def _cached_rows(key: str | None) -> tuple[dict[str, str], ...]:
    """صفوفُ الجدول محفوظةً لهذه الجلسة؛ البصمةُ تُقابَل عند أوّل قراءةٍ لكلّ جذر."""

    return root_table_rows(Path(key) if key is not None else None)


@lru_cache(maxsize=4)
def _cached_source(key: str | None) -> SourceReference:
    """نسخةُ المصدر مقروءةً عن القرص بالمُبصِّم القائم، لا منسوخةً في حقلٍ ثانٍ."""

    for material in THE_DECLARED_MATERIALS:
        if material.key != "MAQAYIS_BY_ROOT":
            continue
        reading = seal_reading_for(material, Path(key) if key is not None else None)
        if reading.standing is not SealStanding.SEALED_AND_PRESENT:
            raise MaqayisLinkCandidateError(
                f"الأصلُ المعجميُّ {reading.standing.value}؛ ولا يُستخرَج "
                "مرشَّحٌ من مادّةٍ لم يُطابَق ختمُها."
            )
        if reading.measured_byte_length is None or reading.measured_sha256 is None:
            raise MaqayisLinkCandidateError("نسخةٌ بلا طولٍ أو بلا بصمةٍ مقيسة.")
        return SourceReference(
            material_key=material.key,
            relative_path=ROOT_TABLE_RELATIVE_PATH,
            measured_byte_length=reading.measured_byte_length,
            measured_sha256=reading.measured_sha256,
        )
    raise MaqayisLinkCandidateError("لا أصلَ معجميًّا في المواد المُعلَنة.")


def _key_of(root: Path | None) -> str | None:
    """مفتاحُ الحفظ نصُّ المسار؛ وجذرٌ آخرُ قراءةٌ أخرى لا نسخةٌ محفوظة."""

    return None if root is None else str(root)


def _rows_of(root: Path | None = None) -> tuple[dict[str, str], ...]:
    return _cached_rows(_key_of(root))


def _source_reference(root: Path | None = None) -> SourceReference:
    return _cached_source(_key_of(root))


# --- حدُّ المادّة --------------------------------------------------------------


class BoundaryStanding(Enum):
    """حالُ حدِّ المادّة، مُشتقًّا من تصنيف الترويسة القائم لا من تصنيفٍ جديد."""

    SOUND = "حدٌّ محقَّق"
    SUSPECT = "حدٌّ مشتبه"


def _boundary_standing(row: Mapping[str, str]) -> BoundaryStanding:
    """حدُّ صفٍّ: ترويسةُ بابٍ أو كتابِ حرفٍ حدٌّ محقَّق، وما سواها مشتبه."""

    form = classify_header(row["chapter_header"])
    if form in (HeaderForm.LETTER_BOOK, HeaderForm.SUB_CHAPTER):
        return BoundaryStanding.SOUND
    return BoundaryStanding.SUSPECT


# --- الشهاداتُ الثلاث ---------------------------------------------------------


class AttributionCheck(Enum):
    """شهادةُ صحّة النسبة: أتابعٌ هذا الشاهدُ للمادّة المقصودة ضمن حدٍّ محقَّق؟"""

    IN_THIS_MATERIAL = "تابعٌ للمادّة المقصودة"
    NOT_IN_THIS_MATERIAL = "ليس من المادّة المقصودة"
    BOUNDARY_SUSPECT = "حدُّ المادّة مشتبه"


class SufficiencyCheck(Enum):
    """شهادةُ كفاية الاستشهاد، وعلاقةُ عبارة الشاهد بالصياغة المستخرَجة فيها."""

    SUPPORTS_VERBATIM = "يُسنِده بحروفه"
    SUPPORTED_UNDER_A_NAMED_NORMALISATION = "يُسنِده بعد تجريدِ تشكيلٍ مُسمًّى"
    NOT_FOUND_IN_THE_WITNESS = "لا تقع صياغتُه في الشاهد"


THE_LETTER_NAMES: Final[Mapping[str, tuple[str, ...]]] = {
    "ء": ("همزة",),
    "أ": ("همزة",),
    "إ": ("همزة",),
    "آ": ("همزة",),
    "ؤ": ("همزة",),
    "ئ": ("همزة",),
    "ا": ("ألف", "الف"),
    "ب": ("باء",),
    "ت": ("تاء",),
    "ث": ("ثاء",),
    "ج": ("جيم",),
    "ح": ("حاء",),
    "خ": ("خاء",),
    "د": ("دال",),
    "ذ": ("ذال",),
    "ر": ("راء",),
    "ز": ("زاي", "زاء"),
    "س": ("سين",),
    "ش": ("شين",),
    "ص": ("صاد",),
    "ض": ("ضاد",),
    "ط": ("طاء",),
    "ظ": ("ظاء",),
    "ع": ("عين",),
    "غ": ("غين",),
    "ف": ("فاء",),
    "ق": ("قاف",),
    "ك": ("كاف",),
    "ل": ("لام",),
    "م": ("ميم",),
    "ن": ("نون",),
    "ه": ("هاء",),
    "ة": ("هاء",),
    "و": ("واو",),
    "ى": ("ألف", "الف"),
    "ي": ("ياء",),
}
"""أسماءُ الحروف كما يفتتح بها ابن فارس شرحَه؛ جدولُ قراءةٍ لا حكمَ صوتيّ.

وهي أداةُ مِسبارِ النسبة وحدَها: شرحُ المادّة يفتتح بتسمية حروف جذرها، فجملةٌ
لا تُسمّي حروفَ جذرِ صفِّها جملةٌ نُسبت إلى غير مادّتها. ولا يُقرأ هذا الجدولُ
قسمةً للحروف ولا مخرجًا لها.
"""

THE_REFUSAL_FORMULAE: Final[tuple[str, ...]] = (
    "ليس باصل",
    "ليست باصل",
    "ليس بأصل",
)
"""صيغُ نفيِ الأصل كما ترد في المتن؛ تُلتمَس بعد تجريد التشكيل.

ووقوعُها دليلٌ **مضادٌّ** لدعوى أنّ هذه المادّة تُخرِج أصلًا معجميًّا، وهو غيرُ
غيابِ الدليل؛ ولذلك يُفرَز بجنسِ تعليقٍ آخر.
"""


class SuspensionGenus(Enum):
    """أجناسُ التعليق الأربعة؛ ولا يُقرأ واحدٌ منها رفضًا ولا إثباتًا لعدم."""

    ABSENT_EVIDENCE = "غيابُ دليل"
    COUNTER_EVIDENCE = "دليلٌ مضادّ"
    TOOL_UNAVAILABLE = "تعذُّرُ الأداة"
    FORBIDDEN_IN_A_DECLARED_SYSTEM = "امتناعٌ داخل نظامٍ محدَّد"


class AdmissionStanding(Enum):
    """حالُ اعتماد الربط؛ والمعلَّقُ صنفٌ أوّلٌ لا مرفوضٌ ولا محذوف."""

    ADMITTED = "معتمَد"
    SUSPENDED = "معلَّق"


# --- المرشَّحُ وشاهدُه ----------------------------------------------------------


@dataclass(frozen=True, slots=True)
class WitnessReference:
    """مرجعُ شاهدٍ كاملٌ: حقلُه وإزاحتاه ووحدتُها، ومقتطفُ عرضه مفصولٌ عنه."""

    field_name: str
    start_offset: int
    end_offset: int
    offset_unit: str
    text: str

    def __post_init__(self) -> None:
        if self.start_offset < 0 or self.end_offset <= self.start_offset:
            raise MaqayisLinkCandidateError("إزاحتا الشاهد مجالٌ غيرُ خالٍ وغيرُ سالب.")
        if not self.text.strip():
            raise MaqayisLinkCandidateError("شاهدٌ بنصٍّ فارغٍ لا يُحفَظ.")

    @property
    def display_excerpt(self) -> str:
        """مقتطفُ العرض مقطوعًا؛ عرضٌ لا يُتحقَّق منه ولا يحلّ محلّ المرجع."""

        return self.text[:THE_DISPLAY_EXCERPT_LIMIT]

    @property
    def is_truncated_for_display(self) -> bool:
        """أطال الشاهدُ عن حدّ العرض؟ يُعلَن ولا يُستَر."""

        return len(self.text) > THE_DISPLAY_EXCERPT_LIMIT


@dataclass(frozen=True, slots=True)
class LinkCandidate:
    """مرشَّحُ ربطٍ معجميّ: مادّتُه، ومعناه المرشَّح، وشاهدُه، وبدائلُه، وخلافُه.

    ولا حقلَ ههنا يقول «نوعُ الدلالة» إثباتًا: `signification_kind` يبقى
    `None` ما دام النصُّ الحاكمُ غائبًا، وحضورُه لا يملؤه بنفسه.
    """

    material_key: str
    row_index: int
    root_full: str
    root_display: str
    entry_num: str
    source: SourceReference
    extraction_method: str
    input_unit: InputUnitKind
    candidate_meaning: str
    meaning_field: str
    axis_index: int
    axis_total: int
    witness: WitnessReference
    boundary: BoundaryStanding
    axes_count_standing: str
    alternatives: tuple[str, ...]
    signification_kind: DalalaKind | None
    madlul_section: MadlulSection

    def __post_init__(self) -> None:
        if not self.candidate_meaning.strip():
            raise MaqayisLinkCandidateError("مرشَّحٌ بمعنًى فارغٍ لا يُنشأ.")
        if self.signification_kind is not None and not isinstance(
            self.signification_kind, DalalaKind
        ):
            raise MaqayisLinkCandidateError(
                "نوعُ الدلالة عضوٌ من `DalalaKind` أو لا شيء."
            )
        if not isinstance(self.madlul_section, MadlulSection):
            raise MaqayisLinkCandidateError("صنفُ المدلول عضوٌ من القسمة المُبرهَنة.")

    @property
    def candidate_id(self) -> str:
        """مُعرِّفُ المرشَّح: صفُّه ورتبةُ محوره؛ مُشتَقٌّ لا مكتوبٌ بجانبه."""

        return f"{self.material_key}#{self.axis_index}"


@dataclass(frozen=True, slots=True)
class ReviewAttestation:
    """مراجعةٌ مودَعةٌ لمادّةٍ بعينها ومعنًى بنصّه؛ لا إذنَ عامٌّ ولا إذنُ ملفّ."""

    material_key: str
    candidate_meaning: str
    witness_text: str
    reviewer: str
    statement: str

    def __post_init__(self) -> None:
        for name in ("material_key", "candidate_meaning", "witness_text", "reviewer"):
            if not str(getattr(self, name)).strip():
                raise MaqayisLinkCandidateError(
                    "المراجعةُ المودَعةُ بمادّةٍ ومعنًى وشاهدٍ ومراجعٍ، وناقصُها يُرفَض."
                )


THE_ADMISSION_RULE: Final[str] = (
    "يُعتمَد الربطُ إذا اجتمعت خمسٌ: بصمةُ النسخة مطابقةٌ عند القراءة، "
    "والشاهدُ منتزَعٌ من حقل المادّة نفسِها بإزاحتيه، ونسبتُه مُثبَتةٌ بمِسبارٍ "
    "لا يُصدِّق نفسَه، وحدُّ المادّة محقَّق، وكفايةُ الاستشهاد `SUPPORTS_VERBATIM` "
    "ومعها مراجعةٌ مودَعةٌ لهذه المادّة وهذا المعنى بنصّه. وتخلُّفُ واحدةٍ "
    "يُعلِّق هذا المرشَّحَ وحدَه بجنسِ سببه، ولا يُعلِّق غيرَه ولا يَرفُضه"
)


@dataclass(frozen=True, slots=True)
class VerificationReading:
    """نتيجةُ التحقّق لمرشَّحٍ واحد: شهاداتُه الثلاث، وحالُه، وسببُ تعليقه.

    و`counter_evidence_in_witness` **يُسجَّل ولا يَقضي**: وقوعُ صيغة نفيِ الأصل
    في الشاهد واقعةٌ تُحفَظ لتُقوَّم، ولا تقلب حالَ الاعتماد آليًّا؛ فقلبُ
    الحكم بلا تقويمٍ مثلُ إهماله سواءً بسواء.
    """

    candidate: LinkCandidate
    source_integrity: bool
    attribution: AttributionCheck
    sufficiency: SufficiencyCheck
    counter_evidence_in_witness: bool
    review: ReviewAttestation | None
    standing: AdmissionStanding
    suspension_genus: SuspensionGenus | None
    unmet_conditions: tuple[str, ...]
    scope: str

    @property
    def is_admitted(self) -> bool:
        return self.standing is AdmissionStanding.ADMITTED


# --- الآلة --------------------------------------------------------------------


THE_CANDIDATE_SAMPLE_SIZE: Final[int] = 20
"""حجمُ العيّنة مُسمًّى قبل الرؤية؛ ولا يُوسَّع بعد قراءة نتيجتها."""

THE_CANDIDATE_SAMPLE_RULE: Final[str] = (
    "العيّنةُ أوّلُ عشرين قيمةَ `root_display` متمايزةً بترتيب ورودها في "
    "بايتات الجدول المختومة، ممّا لا يخلو `body_text` فيه؛ وهي قاعدةُ العيّنة "
    "نفسُها التي يُخرِج بها `dal_madlul_bridge` معلَّقيه، فلا تُفتَح عيّنةٌ ثانية"
)

_SENTENCE_END: Final[re.Pattern[str]] = re.compile(r"[.\n]")


def _nfc(text: str) -> str:
    """تسويةُ العرض المُعلَنة قبل عدّ نقطةٍ واحدة."""

    return unicodedata.normalize("NFC", text)


def _sample_rows(root: Path | None = None) -> tuple[tuple[int, dict[str, str]], ...]:
    """صفوفُ العيّنة بترتيب الملفّ، مع رتبة كلِّ صفٍّ فيه لا مُعادَ ترقيمها."""

    seen: list[str] = []
    chosen: list[tuple[int, dict[str, str]]] = []
    for index, row in enumerate(_rows_of(root)):
        display = row["root_display"].strip()
        if not display or display in seen or not row["body_text"].strip():
            continue
        seen.append(display)
        chosen.append((index, row))
        if len(chosen) == THE_CANDIDATE_SAMPLE_SIZE:
            break
    if len(chosen) != THE_CANDIDATE_SAMPLE_SIZE:
        raise MaqayisLinkCandidateError(
            "لم تكتمل العيّنةُ المُعلَنة من البايتات المختومة؛ ولا تُقصّ القاعدةُ "
            "على ما وُجد."
        )
    return tuple(chosen)


def input_unit_reading(root: Path | None = None) -> InputUnitReading:
    """قِس نوعَ وحدة المدخل على العيّنة؛ ولا يُكتَب النوعُ قبل أن يُقاس."""

    rows = _sample_rows(root)
    equal = 0
    collapsed = 0
    vocalised = 0
    for _, row in rows:
        display = row["root_display"].strip()
        full = row["root_full"].strip()
        if display == full:
            equal += 1
        elif len(display) < len(full) and full.startswith(display):
            collapsed += 1
        if strip_diacritics(display) != display:
            vocalised += 1
    return InputUnitReading(
        examined=len(rows),
        equal_to_root_full=equal,
        collapsed_gemination=collapsed,
        bearing_a_written_haraka=vocalised,
    )


def _first_sentence(body: str) -> tuple[int, int]:
    """مجالُ الجملة الأولى تحت `THE_WITNESS_SELECTION_RULE`، بنقاط الشفرة."""

    match = _SENTENCE_END.search(body)
    return (0, match.end() if match else len(body))


def _attribution_of(row: Mapping[str, str], sentence: str) -> AttributionCheck:
    """أتُسمّي جملةُ الشاهد حروفَ جذرِ صفِّها؟ مِسبارٌ لا يَقرأ ما يُقاس به."""

    bare = strip_diacritics(sentence)
    letters: list[str] = []
    for character in row["root_full"].strip():
        if character in THE_LETTER_NAMES and character not in letters:
            letters.append(character)
    if not letters:
        return AttributionCheck.NOT_IN_THIS_MATERIAL
    for character in letters:
        if not any(name in bare for name in THE_LETTER_NAMES[character]):
            return AttributionCheck.NOT_IN_THIS_MATERIAL
    return AttributionCheck.IN_THIS_MATERIAL


def _sufficiency_of(meaning: str, witness: str) -> SufficiencyCheck:
    """أيُسنِد الشاهدُ هذا المعنى بعينه؟ وبأيّ علاقةٍ بين عبارته وصياغته؟"""

    if meaning in witness:
        return SufficiencyCheck.SUPPORTS_VERBATIM
    if strip_diacritics(meaning) in strip_diacritics(witness):
        return SufficiencyCheck.SUPPORTED_UNDER_A_NAMED_NORMALISATION
    return SufficiencyCheck.NOT_FOUND_IN_THE_WITNESS


def _carries_a_refusal(witness: str) -> bool:
    """أتقع في الشاهد صيغةُ نفيِ الأصل؟ دليلٌ مضادٌّ لا غيابُ دليل."""

    bare = strip_diacritics(witness)
    return any(formula in bare for formula in THE_REFUSAL_FORMULAE)


def _signification_kind(governing: SealStanding) -> DalalaKind | None:
    """نوعُ الدلالة لا يُملأ ههنا البتّة، ويُسمّى سببُ خلوّه لا يُسكَت عنه.

    فغيابُ النصّ الحاكم يمنع تعريفَ القسمة أصلًا؛ وحضورُه **لا يكفي** لأنّ
    انطباقَ قسمٍ على زوجٍ بعينه دعوى تُثبَت بشاهدها لا بحضور كتابٍ يُعرِّفها
    (`THE_ABSENCE_OF_ONE_SOURCE_SUSPENDS_ONLY_WHAT_DEPENDS_ON_IT`).
    """

    _ = governing
    return None


def link_candidates(root: Path | None = None) -> tuple[LinkCandidate, ...]:
    """مرشَّحو الربط المعجميّ عن العيّنة المُعلَنة؛ مرشَّحٌ لكلّ محورٍ مكتوب.

    ولا يُخرَج مرشَّحٌ عن صفٍّ لا محورَ مكتوبًا فيه: فراغُ الحقل غيابُ تصريحٍ
    لا تصريحٌ بغياب، ويُحفَظ الصفُّ في `dal_readings` ولا يُحذَف.
    """

    source = _source_reference(root)
    governing = governing_seal_reading(root)
    candidates: list[LinkCandidate] = []
    for index, row in _sample_rows(root):
        body = _nfc(row["body_text"])
        start, end = _first_sentence(body)
        axes = tuple(
            segment.strip()
            for segment in split_witness_segments(row["semantic_axes"])
            if segment.strip()
        )
        witness = WitnessReference(
            field_name="body_text",
            start_offset=start,
            end_offset=end,
            offset_unit=THE_OFFSET_UNIT,
            text=body[start:end],
        )
        for axis_index, meaning in enumerate(axes):
            candidates.append(
                LinkCandidate(
                    material_key=f"{row['root_full']}:{row['entry_num']}",
                    row_index=index,
                    root_full=row["root_full"],
                    root_display=row["root_display"].strip(),
                    entry_num=row["entry_num"],
                    source=source,
                    extraction_method=THE_EXTRACTION_METHOD,
                    input_unit=InputUnitKind.ROOT_KEY_DISPLAY_FORM,
                    candidate_meaning=_nfc(meaning),
                    meaning_field="semantic_axes",
                    axis_index=axis_index,
                    axis_total=len(axes),
                    witness=witness,
                    boundary=_boundary_standing(row),
                    axes_count_standing=weigh_declared_axes_count(row),
                    alternatives=tuple(
                        _nfc(other)
                        for other_index, other in enumerate(axes)
                        if other_index != axis_index
                    ),
                    signification_kind=_signification_kind(governing.standing),
                    madlul_section=MadlulSection.MEANING,
                )
            )
    return tuple(candidates)


def verify(
    candidate: LinkCandidate,
    *,
    root: Path | None = None,
    reviews: tuple[ReviewAttestation, ...] = (),
) -> VerificationReading:
    """افحص مرشَّحًا بثلاث شهاداتٍ منفصلة، وأخرِج حالَه وسببَ تعليقه إن عُلِّق.

    والشهاداتُ تُعاد من البايتات عند كلّ فحص: لا يُصدَّق حقلٌ محفوظٌ في
    المرشَّح على نفسه، فتغيُّرُ الشاهد أو المعنى يُوجِب إعادةَ التحقّق ويظهر
    أثرُه ههنا لا في نثرٍ مكتوب.
    """

    rows = _rows_of(root)
    if not 0 <= candidate.row_index < len(rows):
        raise MaqayisLinkCandidateError("رتبةُ صفٍّ خارجَ البايتات المقروءة.")
    row = rows[candidate.row_index]
    body = _nfc(row["body_text"])

    source = _source_reference(root)
    source_integrity = (
        source.measured_sha256 == candidate.source.measured_sha256
        and candidate.witness.text in body
    )

    span = body[candidate.witness.start_offset : candidate.witness.end_offset]
    if span != candidate.witness.text:
        attribution = AttributionCheck.NOT_IN_THIS_MATERIAL
    else:
        attribution = _attribution_of(row, candidate.witness.text)
    if (
        attribution is AttributionCheck.IN_THIS_MATERIAL
        and _boundary_standing(row) is BoundaryStanding.SUSPECT
    ):
        attribution = AttributionCheck.BOUNDARY_SUSPECT

    sufficiency = _sufficiency_of(candidate.candidate_meaning, candidate.witness.text)

    review = next(
        (
            attestation
            for attestation in reviews
            if attestation.material_key == candidate.material_key
            and attestation.candidate_meaning == candidate.candidate_meaning
            and attestation.witness_text == candidate.witness.text
        ),
        None,
    )

    unmet: list[str] = []
    genus: SuspensionGenus | None = None
    if not source_integrity:
        unmet.append("سلامةُ المصدر: الشاهدُ لا يقع في النسخة المقروءة بهذه البصمة")
        genus = SuspensionGenus.COUNTER_EVIDENCE
    if attribution is AttributionCheck.NOT_IN_THIS_MATERIAL:
        unmet.append("صحّةُ النسبة: الشاهدُ ليس من المادّة المقصودة")
        genus = genus or SuspensionGenus.COUNTER_EVIDENCE
    elif attribution is AttributionCheck.BOUNDARY_SUSPECT:
        unmet.append("صحّةُ النسبة: حدُّ المادّة مشتبهٌ فتُعلَّق نتائجُه التابعة")
        genus = genus or SuspensionGenus.ABSENT_EVIDENCE
    if sufficiency is SufficiencyCheck.NOT_FOUND_IN_THE_WITNESS:
        unmet.append("كفايةُ الاستشهاد: لا تقع صياغةُ المعنى في الشاهد")
        genus = genus or (
            SuspensionGenus.COUNTER_EVIDENCE
            if _carries_a_refusal(candidate.witness.text)
            else SuspensionGenus.ABSENT_EVIDENCE
        )
    elif sufficiency is SufficiencyCheck.SUPPORTED_UNDER_A_NAMED_NORMALISATION:
        unmet.append("كفايةُ الاستشهاد: الموافقةُ بعد تجريدِ تشكيلٍ مُسمًّى لا بحروفها")
        genus = genus or SuspensionGenus.TOOL_UNAVAILABLE
    if review is None:
        unmet.append("قبولُ المعنى موقوفٌ على مراجعةٍ مودَعةٍ لهذه المادّة وهذا المعنى")
        genus = genus or SuspensionGenus.TOOL_UNAVAILABLE

    standing = AdmissionStanding.ADMITTED if not unmet else AdmissionStanding.SUSPENDED
    return VerificationReading(
        candidate=candidate,
        source_integrity=source_integrity,
        attribution=attribution,
        sufficiency=sufficiency,
        counter_evidence_in_witness=_carries_a_refusal(candidate.witness.text),
        review=review,
        standing=standing,
        suspension_genus=genus,
        unmet_conditions=tuple(unmet),
        scope=(
            "نطاقُ الاعتماد: أنّ هذه النسخةَ من هذا المعجم أسندت هذا المعنى "
            "لهذه المادّة؛ ولا يمتدّ إلى مشتقٍّ ولا إلى وقوعٍ في عبارة، ولا "
            "يُقرأ تصديقًا لواقعةٍ خارجَ اللغة"
        ),
    )


# --- السلسلةُ وبلوغُها ---------------------------------------------------------


def chain_reach(
    root: Path | None = None,
    *,
    reviews: tuple[ReviewAttestation, ...] = (),
) -> tuple[tuple[LinkChainRung, bool, str], ...]:
    """أيُّ الوصلات بلغتها الآلةُ فعلًا، وبأيّ شرط؛ ولا تُدَّعى وصلةٌ لم تُنفَّذ."""

    source = _source_reference(root)
    candidates = link_candidates(root)
    admitted = sum(
        1
        for candidate in candidates
        if verify(candidate, root=root, reviews=reviews).is_admitted
    )
    return (
        (
            LinkChainRung.MATERIAL_KEY,
            True,
            f"مفاتيحُ الموادّ مقروءةٌ من نسخةٍ بصمتُها {source.measured_sha256[:8]}…",
        ),
        (
            LinkChainRung.VERIFIED_MATERIAL,
            True,
            "المادّةُ محقَّقةٌ بحدِّها: ترويسةٌ مصنَّفةٌ بالتصنيف القائم، والمشتبهُ معلَّق",
        ),
        (
            LinkChainRung.EXTRACTED_MEANING,
            admitted > 0,
            f"المعنى المستخرَجُ يبلغ بالاعتماد وحدَه؛ والمعتمَدُ الآن {admitted}",
        ),
        (
            LinkChainRung.LAFZ,
            False,
            A_ROOT_ORIGIN_IS_NOT_THE_MEANING_OF_EVERY_DERIVATIVE,
        ),
        (
            LinkChainRung.USAGE,
            False,
            A_ROOT_ORIGIN_IS_NOT_THE_MEANING_OF_EVERY_DERIVATIVE,
        ),
    )


# --- العدُّ بوحداتٍ منفصلة ------------------------------------------------------


class DalProcessing(Enum):
    """حالُ معالجةِ دالٍّ؛ ثلاثةٌ لا تُجمَع، ولا يُقرأ أحدُها استيفاءً للمعاني."""

    ALL_DECLARED_AXES_PROCESSED = "عولجت محاورُه المُعلَنةُ كلُّها في النطاق"
    PARTIALLY_PROCESSED = "عولج جزئيًّا"
    NO_ADMITTED_OUTPUT = "لا مخرجَ معتمَدًا له"


@dataclass(frozen=True, slots=True)
class DalReading:
    """سطرُ دالٍّ محفوظٌ كاملًا: محاورُه، ومرشَّحوه، وحدُّه، وخلافُ عدده."""

    root_display: str
    material_key: str
    row_index: int
    declared_axes: int
    candidates: int
    admitted: int
    boundary: BoundaryStanding
    axes_count_standing: str
    processing: DalProcessing
    carries_a_refusal_formula: bool
    suspension_genera: tuple[SuspensionGenus, ...]


def dal_readings(
    root: Path | None = None,
    *,
    reviews: tuple[ReviewAttestation, ...] = (),
) -> tuple[DalReading, ...]:
    """الدوالُّ العشرون كلُّهم، بما فيهم الفارغُ والمشتبه؛ ولا يُطوى صفٌّ متعذِّر."""

    verifications = tuple(
        verify(candidate, root=root, reviews=reviews)
        for candidate in link_candidates(root)
    )
    by_row: dict[int, list[VerificationReading]] = {}
    for reading in verifications:
        by_row.setdefault(reading.candidate.row_index, []).append(reading)

    readings: list[DalReading] = []
    for index, row in _sample_rows(root):
        mine = tuple(by_row.get(index, ()))
        declared_axes = len(
            [
                segment
                for segment in split_witness_segments(row["semantic_axes"])
                if segment.strip()
            ]
        )
        admitted = sum(1 for reading in mine if reading.is_admitted)
        boundary = _boundary_standing(row)
        standing = weigh_declared_axes_count(row)
        body = _nfc(row["body_text"])
        start, end = _first_sentence(body)
        refusal = _carries_a_refusal(body[start:end])
        if not mine:
            processing = DalProcessing.NO_ADMITTED_OUTPUT
        elif boundary is BoundaryStanding.SUSPECT or standing != AxesStanding.AGREES:
            processing = DalProcessing.PARTIALLY_PROCESSED
        else:
            processing = DalProcessing.ALL_DECLARED_AXES_PROCESSED
        readings.append(
            DalReading(
                root_display=row["root_display"].strip(),
                material_key=f"{row['root_full']}:{row['entry_num']}",
                row_index=index,
                declared_axes=declared_axes,
                candidates=len(mine),
                admitted=admitted,
                boundary=boundary,
                axes_count_standing=standing,
                processing=processing,
                carries_a_refusal_formula=refusal,
                suspension_genera=(
                    tuple(
                        dict.fromkeys(
                            reading.suspension_genus
                            for reading in mine
                            if reading.suspension_genus is not None
                        )
                    )
                    if mine
                    else (
                        (SuspensionGenus.COUNTER_EVIDENCE,)
                        if refusal
                        else (SuspensionGenus.ABSENT_EVIDENCE,)
                    )
                ),
            )
        )
    return tuple(readings)


@dataclass(frozen=True, slots=True)
class ProvenanceShares:
    """نسبُ ما تولّد من البنية، وما نُقل من الرصيد، وما ثبت بعمليّة ربط."""

    generated_from_structure: int
    transported_from_stock: int
    established_by_linking: int


def provenance_shares(
    root: Path | None = None,
    *,
    reviews: tuple[ReviewAttestation, ...] = (),
) -> ProvenanceShares:
    """النسبُ الثلاثُ معدودةً؛ ولا يُدَّعى توليدُ معنًى من الـ١١٦ ههنا."""

    candidates = link_candidates(root)
    admitted = sum(
        1
        for candidate in candidates
        if verify(candidate, root=root, reviews=reviews).is_admitted
    )
    return ProvenanceShares(
        generated_from_structure=0,
        transported_from_stock=len(candidates),
        established_by_linking=admitted,
    )


def candidate_counts(
    root: Path | None = None,
    *,
    reviews: tuple[ReviewAttestation, ...] = (),
) -> dict[str, int]:
    """الأعدادُ بوحداتٍ منفصلة؛ ولا يُجمَع دالٌّ إلى محورٍ ولا محورٌ إلى مرشَّح.

    وليس في هذا السجلّ معادلةُ «٢٠ = أزواجٌ + معلَّقون»: الدالُّ وحدةٌ،
    والمحورُ وحدةٌ، والمرشَّحُ وحدةٌ؛ والدالُّ الواحدُ يُخرِج محاورَ عدّة.
    """

    readings = dal_readings(root, reviews=reviews)
    verifications = tuple(
        verify(candidate, root=root, reviews=reviews)
        for candidate in link_candidates(root)
    )
    return {
        "دوال": len(readings),
        "محاور_مكتوبة": sum(reading.declared_axes for reading in readings),
        "مرشحات": len(verifications),
        "معتمدون": sum(1 for reading in verifications if reading.is_admitted),
        "معلقون": sum(1 for reading in verifications if not reading.is_admitted),
        "دوال_بلا_مرشح": sum(1 for reading in readings if reading.candidates == 0),
        "دوال_حدها_مشتبه": sum(
            1 for reading in readings if reading.boundary is BoundaryStanding.SUSPECT
        ),
        "دوال_مخالفة_العدد_المصرح": sum(
            1
            for reading in readings
            if reading.axes_count_standing == AxesStanding.DIFFERS
        ),
        "دوال_فارغة_التصريح": sum(
            1
            for reading in readings
            if reading.axes_count_standing == AxesStanding.BLANK
        ),
        "دوال_في_شاهدها_نفيُ_أصل": sum(
            1 for reading in readings if reading.carries_a_refusal_formula
        ),
    }


# --- السجلّ: سطرٌ لكلّ واقعة ----------------------------------------------------


def report_rows(
    root: Path | None = None,
    *,
    reviews: tuple[ReviewAttestation, ...] = (),
) -> tuple[dict[str, object], ...]:
    """سجلُّ الآلة صفوفًا: مصدرٌ، ووحدةُ مدخلٍ، وسلسلةٌ، ودوالُّ، ومرشَّحون، وعدّ.

    وكلُّ صفٍّ يحمل جنسَه في `نوع`، فلا يُقرأ صفُّ مرشَّحٍ معتمَدًا ولا العكس.
    """

    source = _source_reference(root)
    governing = governing_seal_reading(root)
    unit = input_unit_reading(root)
    rows: list[dict[str, object]] = [
        {
            "نوع": "مصدر",
            "مفتاح": source.material_key,
            "مسار": source.relative_path,
            "طول_مقيس": source.measured_byte_length,
            "بصمة_مقيسة": source.measured_sha256,
            "طريقة_الاستخراج": THE_EXTRACTION_METHOD,
            "بقية": A_SOURCE_IS_A_ROUTE_OF_ACCESS_NOT_A_KIND_OF_SIGNIFICATION,
        },
        {
            "نوع": "نص_حاكم",
            "الحال": governing.standing.value,
            "ما_يعلقه": "تصنيفُ نوع الدلالة وحدَه",
            "بقية": THE_ABSENCE_OF_ONE_SOURCE_SUSPENDS_ONLY_WHAT_DEPENDS_ON_IT,
        },
        {
            "نوع": "وحدة_مدخل",
            "النوع": unit.kind.value,
            "مفحوص": unit.examined,
            "مساوٍ_للجذر_التام": unit.equal_to_root_full,
            "مطوي_التضعيف": unit.collapsed_gemination,
            "حامل_حركة": unit.bearing_a_written_haraka,
            "بقية": A_ROOT_KEY_DISPLAY_FORM_IS_NOT_A_USED_WORD,
        },
    ]
    for rung, reached, why in chain_reach(root, reviews=reviews):
        rows.append(
            {
                "نوع": "وصلة",
                "الوصلة": rung.value,
                "بلغت": reached,
                "بيان": why,
            }
        )
    for reading in dal_readings(root, reviews=reviews):
        rows.append(
            {
                "نوع": "دال",
                "دال": reading.root_display,
                "مفتاح_المادة": reading.material_key,
                "رتبة_الصف": reading.row_index,
                "محاور_مكتوبة": reading.declared_axes,
                "مرشحات": reading.candidates,
                "معتمدون": reading.admitted,
                "حد_المادة": reading.boundary.value,
                "موقف_العدد_المصرح": reading.axes_count_standing,
                "حال_المعالجة": reading.processing.value,
                "في_شاهده_نفيُ_أصل": reading.carries_a_refusal_formula,
                "أجناس_التعليق": [genus.value for genus in reading.suspension_genera],
            }
        )
    for candidate in link_candidates(root):
        checked = verify(candidate, root=root, reviews=reviews)
        rows.append(
            {
                "نوع": "مرشح",
                "معرف": candidate.candidate_id,
                "دال": candidate.root_display,
                "مفتاح_المادة": candidate.material_key,
                "رتبة_الصف": candidate.row_index,
                "وحدة_المدخل": candidate.input_unit.value,
                "معنى_مرشح": candidate.candidate_meaning,
                "حقل_الصياغة": candidate.meaning_field,
                "محور_رقم": candidate.axis_index,
                "محاور_الصف": candidate.axis_total,
                "بدائل": list(candidate.alternatives),
                "حقل_الشاهد": candidate.witness.field_name,
                "إزاحة_من": candidate.witness.start_offset,
                "إزاحة_إلى": candidate.witness.end_offset,
                "وحدة_الإزاحة": candidate.witness.offset_unit,
                "مقتطف_عرض": candidate.witness.display_excerpt,
                "مقطوع_للعرض": candidate.witness.is_truncated_for_display,
                "سلامة_المصدر": checked.source_integrity,
                "صحة_النسبة": checked.attribution.value,
                "كفاية_الاستشهاد": checked.sufficiency.value,
                "في_شاهده_نفيُ_أصل": checked.counter_evidence_in_witness,
                "نوع_الدلالة": (
                    candidate.signification_kind.value
                    if candidate.signification_kind is not None
                    else None
                ),
                "صنف_المدلول": candidate.madlul_section.value,
                "موقف_العدد_المصرح": candidate.axes_count_standing,
                "قاعدة_العدد": AXES_AGREEMENT_COUNTING_RULE,
                "حال_الاعتماد": checked.standing.value,
                "جنس_التعليق": (
                    checked.suspension_genus.value
                    if checked.suspension_genus is not None
                    else None
                ),
                "الشروط_غير_المستوفاة": list(checked.unmet_conditions),
                "نطاق": checked.scope,
            }
        )
    shares = provenance_shares(root, reviews=reviews)
    rows.append(
        {
            "نوع": "نسب_التوليد",
            "مولد_من_البنية": shares.generated_from_structure,
            "منقول_من_الرصيد": shares.transported_from_stock,
            "ثابت_بعملية_ربط": shares.established_by_linking,
            "بقية": A_TRANSPORTED_MEANING_IS_NOT_A_GENERATED_ONE,
        }
    )
    counts = candidate_counts(root, reviews=reviews)
    rows.append({"نوع": "عدّ", **counts, "قاعدة_الاعتماد": THE_ADMISSION_RULE})
    return tuple(rows)
