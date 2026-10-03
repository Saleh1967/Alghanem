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
    "A_HEADER_DETECTOR_PROPOSES_A_BOUNDARY_IT_DOES_NOT_VERIFY",
    "A_NEGATION_FORM_IS_NOT_A_DETERMINED_COUNTER_CLAIM",
    "A_ROOT_ORIGIN_IS_NOT_THE_MEANING_OF_EVERY_DERIVATIVE",
    "A_SEGMENT_IN_A_ROW_IS_NOT_A_SEGMENT_IN_A_MATERIAL",
    "A_SYNTHETIC_ADMISSION_DOES_NOT_VALIDATE_THE_REAL_SUSPENSIONS",
    "THE_ONE_MATERIAL_ACTUALLY_REVIEWED",
    "THE_ABAT_BOUNDARY_REVIEW",
    "A_TEXTUAL_MATCH_IS_NOT_A_SEMANTIC_SUPPORT",
    "A_SOURCE_IS_A_ROUTE_OF_ACCESS_NOT_A_KIND_OF_SIGNIFICATION",
    "A_TRANSPORTED_MEANING_IS_NOT_A_GENERATED_ONE",
    "FINDING_THE_WORD_ORIGIN_DOES_NOT_SUPPORT_A_PARTICULAR_MEANING",
    "MAQAYIS_LINK_CANDIDATE_NAMED_RESIDUALS",
    "THE_ABSENCE_OF_ONE_SOURCE_SUSPENDS_ONLY_WHAT_DEPENDS_ON_IT",
    "THE_ADMISSION_RULE",
    "THE_CANDIDATE_SAMPLE_RULE",
    "THE_CONDITIONS_FOR_A_LAFZ_BRIDGE",
    "THE_LAFZ_LINK_IS_OUT_OF_THIS_UNITS_SCOPE_NOT_IMPOSSIBLE",
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
    "BoundaryAttestation",
    "CounterClaimDetermination",
    "RefusalStanding",
    "ReviewVerdict",
    "SemanticSupportCheck",
    "SourceReference",
    "SuspensionGenus",
    "TextualMatchCheck",
    "VerificationReading",
    "WitnessReference",
    "candidate_counts",
    "chain_reach",
    "dal_readings",
    "input_unit_reading",
    "link_candidates",
    "provenance_shares",
    "reconciliation_rows",
    "suspension_reason_census",
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
    "ولا على كلّ وقوعٍ لها في عبارة؛ وهذا قيدٌ على ما يُستنتَج من هذا المصدر، "
    "لا حكمٌ على إمكان الوصلتين الرابعة والخامسة في المشروع"
)

A_TEXTUAL_MATCH_IS_NOT_A_SEMANTIC_SUPPORT: Final[str] = (
    "A_TEXTUAL_MATCH_IS_NOT_A_SEMANTIC_SUPPORT: وقوعُ صياغة المعنى في الشاهد "
    "نصًّا يُثبِت وجودَ سلسلةٍ نصّيّةٍ لا غير؛ فقد تقع في سياقٍ ينفيها أو "
    "ينسبها إلى قولٍ مرفوضٍ أو يتحدّث عن مادّةٍ أخرى. وبالعكس: قد يُسنِد "
    "الشاهدُ المعنى بصياغةٍ مختلفةٍ بلا تطابق، فلا يُقرأ غيابُ المطابقة نفيًا "
    "للإسناد؛ والإسنادُ شهادةٌ رابعةٌ مصدرُها مراجعةٌ مودَعةٌ تُسمّي جهتَه"
)

A_NEGATION_FORM_IS_NOT_A_DETERMINED_COUNTER_CLAIM: Final[str] = (
    "A_NEGATION_FORM_IS_NOT_A_DETERMINED_COUNTER_CLAIM: رصدُ «ليس بأصل» "
    "رصدُ تركيبٍ لا تحقيقٌ لتعارض؛ فلا يُعلَم أمنفيُّه استقلالُ المادّة أصلًا، "
    "أم وجودُ قياسٍ يجمع استعمالاتها، أم صحّةُ لفظٍ أو نسبةٍ بعينها، أم "
    "المعنى المرشَّح نفسُه. ونفيُ الأوّل لا يُلازِم نفيَ وجود معنًى معجميّ، "
    "فلا يُرفَع الرصدُ دليلًا مضادًّا إلّا بتعيينٍ مودَعٍ يُسمّي دعواه وسببَ "
    "انطباقها"
)

A_HEADER_DETECTOR_PROPOSES_A_BOUNDARY_IT_DOES_NOT_VERIFY: Final[str] = (
    "A_HEADER_DETECTOR_PROPOSES_A_BOUNDARY_IT_DOES_NOT_VERIFY: حضورُ "
    "الترويسة قرينةُ ابتداءٍ تقترح حدًّا، ولا تقول أين ينتهي المتن، ولا تنفي "
    "ترويسةً داخليّةً ابتُلعت، ولا تُقابِل الصفَّ بتاليه؛ وغيابُها قد يكون "
    "اختلافَ تنسيقٍ في أوائل المواد لا خللًا في المادّة. فيُفصَل حدٌّ مرشَّحٌ "
    "بكاشفٍ مُعلَن عن حدٍّ محقَّقٍ بشهادةٍ مودَعة، ولا يُسوَّى بينهما"
)

A_SEGMENT_IN_A_ROW_IS_NOT_A_SEGMENT_IN_A_MATERIAL: Final[str] = (
    "A_SEGMENT_IN_A_ROW_IS_NOT_A_SEGMENT_IN_A_MATERIAL: وقوعُ المقطع في "
    "الصفّ، ووسمُ الصفِّ بهذا المفتاح، مستويان لا يُثبِتان تبعيّةَ المقطع "
    "للمادّة المعجميّة الصحيحة؛ والمادّةُ المبتلعةُ هي الموضعُ الذي ينفصل "
    "فيه الثلاثة، فلا تُبلَغ الثالثةُ إلّا بشهادةِ حدٍّ مودَعة"
)

A_SYNTHETIC_ADMISSION_DOES_NOT_VALIDATE_THE_REAL_SUSPENSIONS: Final[str] = (
    "A_SYNTHETIC_ADMISSION_DOES_NOT_VALIDATE_THE_REAL_SUSPENSIONS: بلوغُ "
    "`ADMITTED` على مدخلٍ مصنوعٍ يُثبِت أنّ مسار القبول يعمل وأنّ الآلة لا "
    "ترفض كلَّ مدخلٍ آليًّا، ولا يُثبِت صحّةَ أسباب تعليق المرشَّحات الحقيقيّة، "
    "ولا قدرةَ الآلة على اعتماد شاهدٍ واقعيٍّ مستوفٍ، ولا خلوَّ الشروط من "
    "زائدٍ يمنع اعتمادًا مشروعًا؛ وهذه الثلاثةُ تُراجَع على مادّةٍ واقعيّةٍ كاملة"
)

THE_LAFZ_LINK_IS_OUT_OF_THIS_UNITS_SCOPE_NOT_IMPOSSIBLE: Final[str] = (
    "THE_LAFZ_LINK_IS_OUT_OF_THIS_UNITS_SCOPE_NOT_IMPOSSIBLE: اللفظُ "
    "والاستعمالُ خارجَ النطاق المُعلَن لهذه الوحدة، إذ مدخلُها مفاتيحُ موادَّ "
    "لا ألفاظٌ مستعمَلة؛ وهذا قيدٌ معماريٌّ محلّيٌّ يُبحَث تغييرُه، لا امتناعٌ "
    "في المشروع. وشروطُ جسرٍ مستقلٍّ لها مُسمّاةٌ في "
    "`THE_CONDITIONS_FOR_A_LAFZ_BRIDGE`"
)

THE_CONDITIONS_FOR_A_LAFZ_BRIDGE: Final[tuple[str, ...]] = (
    "مدوّنةُ ألفاظٍ مختومةٌ تُقرأ منها صورُ الاستعمال لا مفاتيحُ الموادّ",
    "تحليلٌ صرفيٌّ يردّ اللفظَ إلى مادّته، لا وكيلُ إطارٍ سطحيّ",
    "قاعدةٌ مُعلَنةٌ تُبيّن متى يَحمِل المشتقُّ معنى أصلِ مادّته ومتى لا",
    "شاهدُ سياقٍ لكلّ وقوعٍ يُقرأ منه المعنى في موضعه لا في المعجم",
    "مراجعةٌ تُسمّي جهةَ الإسناد في الوقوع كما تُسمّيها في المادّة",
)
"""شروطُ بناء جسرٍ مستقلٍّ للّفظ والاستعمال؛ مُسمّاةٌ كي لا يُقرأ القيدُ امتناعًا."""

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
    "THE_LAFZ_LINK_IS_OUT_OF_THIS_UNITS_SCOPE_NOT_IMPOSSIBLE": (
        THE_LAFZ_LINK_IS_OUT_OF_THIS_UNITS_SCOPE_NOT_IMPOSSIBLE
    ),
    "A_SYNTHETIC_ADMISSION_DOES_NOT_VALIDATE_THE_REAL_SUSPENSIONS": (
        A_SYNTHETIC_ADMISSION_DOES_NOT_VALIDATE_THE_REAL_SUSPENSIONS
    ),
    "A_SEGMENT_IN_A_ROW_IS_NOT_A_SEGMENT_IN_A_MATERIAL": (
        A_SEGMENT_IN_A_ROW_IS_NOT_A_SEGMENT_IN_A_MATERIAL
    ),
    "A_HEADER_DETECTOR_PROPOSES_A_BOUNDARY_IT_DOES_NOT_VERIFY": (
        A_HEADER_DETECTOR_PROPOSES_A_BOUNDARY_IT_DOES_NOT_VERIFY
    ),
    "A_NEGATION_FORM_IS_NOT_A_DETERMINED_COUNTER_CLAIM": (
        A_NEGATION_FORM_IS_NOT_A_DETERMINED_COUNTER_CLAIM
    ),
    "A_TEXTUAL_MATCH_IS_NOT_A_SEMANTIC_SUPPORT": (
        A_TEXTUAL_MATCH_IS_NOT_A_SEMANTIC_SUPPORT
    ),
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
    """حالُ حدِّ المادّة؛ والكاشفُ يقترح حدًّا ولا يُحقِّقه، فلا يُسوَّى بينهما.

    فالترويسةُ الحاضرةُ قرينةُ ابتداءٍ لا شهادةُ حدّ: لا تقول أين ينتهي المتن،
    ولا تنفي ترويسةً داخليّةً ابتُلعت، ولا تُقابِل الصفَّ بتاليه
    (`A_HEADER_DETECTOR_PROPOSES_A_BOUNDARY_IT_DOES_NOT_VERIFY`). ولا يبلغ
    صفٌّ `VERIFIED_BY_A_DEPOSITED_WITNESS` إلّا بشهادةِ حدٍّ مودَعةٍ باسمها.
    """

    CANDIDATE_BY_THE_DETECTOR = "حدٌّ مرشَّحٌ بكاشفٍ مُعلَن"
    UNDETERMINED_BY_THE_DETECTOR = "حدٌّ لم يُعيِّنه الكاشف"
    VERIFIED_BY_A_DEPOSITED_WITNESS = "حدٌّ محقَّقٌ بشهادةٍ مودَعة"


@dataclass(frozen=True, slots=True)
class BoundaryAttestation:
    """شهادةُ حدٍّ مودَعةٌ لصفٍّ بعينه: نهايتُه، وداخلُه، ومقابلتُه بتاليه.

    ولا تُودَع شهادةٌ إلّا ببيانِ ما فُحِص؛ فحدٌّ يُدَّعى تحقّقُه بلا نظرٍ في
    نهايته وترويساته الداخليّة ومقابلته بالمادّة التالية حدٌّ لم يُحقَّق.
    """

    material_key: str
    row_index: int
    end_examined: bool
    internal_headers_examined: bool
    collated_with_the_next_material: bool
    reviewer: str
    statement: str

    def __post_init__(self) -> None:
        if not self.reviewer.strip() or not self.statement.strip():
            raise MaqayisLinkCandidateError("شهادةُ حدٍّ بلا مراجعٍ وبيانٍ تُرَدّ.")

    @property
    def is_complete(self) -> bool:
        """أفُحِصت الثلاثةُ كلُّها؟ وناقصُ واحدةٍ لا يرفع الحدَّ إلى التحقّق."""

        return (
            self.end_examined
            and self.internal_headers_examined
            and self.collated_with_the_next_material
        )


THE_ONE_MATERIAL_ACTUALLY_REVIEWED = (
    "THE_ONE_MATERIAL_ACTUALLY_REVIEWED: مراجعةٌ واقعيّةٌ واحدةٌ أُجرِيت على "
    "الرتبة 12 («أبت»:13)، وهي من الصفوف الثمانية التي يقترح الكاشفُ حدَّها. "
    "فُحِص المنتهى، وفُحِش داخلُه، وقُوبِل بالمادّة التالية («أبد»:14): "
    "فظهر أنّ متنَ الصفِّ يبتلع كلامًا ليس من مادّته — فيه «وهذا الباب مهمل "
    "عند الخليل»، و«الكَبِث: المتغيِّر المُرْوِح»، و«إِنه لأبِثٌ … وناقة أبثَة» "
    "— وهذا من مادّة «أبث» لا من «أبت». فالمقابلةُ لم تُسلِّم، والحدُّ "
    "مردودٌ لا مُحقَّق. وهذه شهادةُ ابتلاعٍ تُثبِت أنّ وسمَ الصفِّ بمفتاحٍ "
    "ليس تبعيّةَ كلِّ مقطعٍ فيه لذلك المفتاح."
)

THE_ABAT_BOUNDARY_REVIEW = BoundaryAttestation(
    material_key="أبت:13",
    row_index=12,
    end_examined=True,
    internal_headers_examined=True,
    collated_with_the_next_material=False,
    reviewer="مراجعةُ هذه الجلسة، بالنظر في متن الصفّ وتاليه",
    statement=THE_ONE_MATERIAL_ACTUALLY_REVIEWED,
)


def _boundary_standing(
    row: Mapping[str, str],
    row_index: int = -1,
    boundaries: tuple[BoundaryAttestation, ...] = (),
) -> BoundaryStanding:
    """حدُّ صفٍّ: شهادةٌ مودَعةٌ تامّةٌ تُحقِّقه، والكاشفُ يقترحه أو لا يُعيِّنه."""

    key = f"{row['root_full']}:{row['entry_num']}"
    for attestation in boundaries:
        if (
            attestation.material_key == key
            and attestation.row_index == row_index
            and attestation.is_complete
        ):
            return BoundaryStanding.VERIFIED_BY_A_DEPOSITED_WITNESS
    form = classify_header(row["chapter_header"])
    if form in (HeaderForm.LETTER_BOOK, HeaderForm.SUB_CHAPTER):
        return BoundaryStanding.CANDIDATE_BY_THE_DETECTOR
    return BoundaryStanding.UNDETERMINED_BY_THE_DETECTOR


# --- الشهاداتُ الثلاث ---------------------------------------------------------


class AttributionCheck(Enum):
    """شهادةُ النسبة على مستواها الثالث: أتابعٌ هذا المقطعُ للمادّة المقصودة؟

    ووقوعُ المقطع في الصفّ (`segment_in_row`) ووسمُ الصفِّ بهذا المفتاح
    مستويان أوّلان لا يُثبِتان الثالث؛ والمادّةُ المبتلعةُ هي الموضعُ الذي
    ينفصل فيه الثلاثةُ فعلًا
    (`A_SEGMENT_IN_A_ROW_IS_NOT_A_SEGMENT_IN_A_MATERIAL`).
    """

    VERIFIED_BY_A_DEPOSITED_WITNESS = "نسبةٌ محقَّقةٌ بشهادةِ حدٍّ مودَعة"
    NOT_DETERMINED = "نسبةٌ غيرُ معيَّنة: الصفُّ موسومٌ ولم يُحقَّق حدُّه"
    REFUTED_BY_THE_PROBE = "نسبةٌ منقوضة: المقطعُ ليس من هذه المادّة"


class TextualMatchCheck(Enum):
    """ما يُثبِته هذا الفحصُ **وجودُ سلسلةٍ نصّيّة** لا غير، ولا يُسمّى كفاية.

    فقد يقع المعنى بحروفه في سياقٍ ينفيه أو ينسبه إلى قولٍ مرفوضٍ أو يتحدّث
    عن مادّةٍ أخرى؛ وقد يُسنِد الشاهدُ المعنى بصياغةٍ مختلفةٍ بلا تطابق
    (`A_TEXTUAL_MATCH_IS_NOT_A_SEMANTIC_SUPPORT`).
    """

    MATCHES_VERBATIM = "تقع صياغتُه بحروفها"
    MATCHES_UNDER_A_NAMED_NORMALISATION = "تقع بعد تحويلٍ مُسمًّى: تجريدُ تشكيل"
    NO_TEXTUAL_MATCH = "لا تقع صياغتُه نصًّا"


class SemanticSupportCheck(Enum):
    """الإسنادُ الدلاليّ: أيُثبِت المقطعُ هذا المعنى بعينه وبالجهة المطلوبة؟

    ولا تُخرِجه آلةٌ من مطابقةٍ نصّيّة؛ مصدرُه مراجعةٌ مودَعةٌ تقول بأيّ جهةٍ
    أسند الشاهدُ المعنى. وغيابُها تعليقٌ لتعذُّر الأداة لا نفيٌ للإسناد.
    """

    ESTABLISHED_BY_A_DEPOSITED_REVIEW = "مُثبَتٌ بمراجعةٍ مودَعة"
    DENIED_BY_A_DEPOSITED_REVIEW = "منفيٌّ بمراجعةٍ مودَعة"
    NOT_ESTABLISHED_WITHOUT_A_REVIEW = "غيرُ مُثبَتٍ: لا مراجعةَ مودَعة"


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

ورصدُ التركيب **ليس تحقيقًا للتعارض**: النصُّ النافي يُحفَظ، وأمّا المنفيُّ
المحدَّد — أهو استقلالُ المادّة أصلًا، أم وجودُ قياسٍ يجمع استعمالاتها، أم
صحّةُ لفظٍ أو نسبةٍ بعينها، أم المعنى المرشَّح نفسُه؟ — فلا يُعيَّن بلا قراءةِ
سياقٍ مودَعة (`A_NEGATION_FORM_IS_NOT_A_DETERMINED_COUNTER_CLAIM`).
"""


class RefusalStanding(Enum):
    """منزلةُ صيغة النفي في شاهدٍ؛ وأعلاها لا تُبلَغ بلا تعيينٍ مودَع."""

    NO_NEGATION_FORM = "لا صيغةَ نفيٍ في الشاهد"
    TARGET_UNDETERMINED = "صيغةُ نفيٍ لم يُعيَّن منفيُّها"
    DETERMINED_COUNTER_CLAIM = "تعارضٌ محقَّقٌ بتعيينِ دعواه"


@dataclass(frozen=True, slots=True)
class CounterClaimDetermination:
    """تعيينُ تعارضٍ مودَعٌ: النصُّ النافي، والمنفيُّ، والدعوى، وسببُ الانطباق."""

    material_key: str
    negating_text: str
    what_is_denied: str
    claim_it_opposes: str
    why_it_applies: str

    def __post_init__(self) -> None:
        for name in (
            "material_key",
            "negating_text",
            "what_is_denied",
            "claim_it_opposes",
            "why_it_applies",
        ):
            if not str(getattr(self, name)).strip():
                raise MaqayisLinkCandidateError(
                    "تعيينُ التعارض بنصٍّ نافٍ ومنفيٍّ ودعوًى وسببِ انطباق."
                )


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


class ReviewVerdict(Enum):
    """جهةُ المراجعة المودَعة؛ والنافيةُ تُحفَظ كما تُحفَظ المُثبِتة."""

    SUPPORTS_THE_MEANING = "يُسنِد الشاهدُ هذا المعنى"
    DENIES_THE_MEANING = "لا يُسنِد الشاهدُ هذا المعنى"


@dataclass(frozen=True, slots=True)
class ReviewAttestation:
    """مراجعةٌ مودَعةٌ لمادّةٍ بعينها ومعنًى بنصّه؛ لا إذنَ عامٌّ ولا إذنُ ملفّ.

    وهي **مصدرُ الإسناد الدلاليّ الوحيد** في هذه الوحدة: الآلةُ تقيس مطابقةً
    نصّيّةً وتعرضها، ولا تَرفعها إسنادًا؛ والرافعُ مراجعٌ يقول بأيّ جهة.
    """

    material_key: str
    candidate_meaning: str
    witness_text: str
    reviewer: str
    statement: str
    verdict: ReviewVerdict = ReviewVerdict.SUPPORTS_THE_MEANING

    def __post_init__(self) -> None:
        if not isinstance(self.verdict, ReviewVerdict):
            raise MaqayisLinkCandidateError("جهةُ المراجعة عضوٌ من `ReviewVerdict`.")
        for name in ("material_key", "candidate_meaning", "witness_text", "reviewer"):
            if not str(getattr(self, name)).strip():
                raise MaqayisLinkCandidateError(
                    "المراجعةُ المودَعةُ بمادّةٍ ومعنًى وشاهدٍ ومراجعٍ، وناقصُها يُرفَض."
                )


THE_ADMISSION_RULE: Final[str] = (
    "يُعتمَد الربطُ إذا اجتمعت أربعٌ: بصمةُ النسخة مطابقةٌ عند القراءة، "
    "والمقطعُ واقعٌ بإزاحتيه في حقل الصفّ، ومِسبارُ تسمية الحروف لم ينقض "
    "نسبتَه، ونسبتُه إلى المادّة محقَّقةٌ بشهادةِ حدٍّ مودَعةٍ فُحِص فيها "
    "المنتهى والترويساتُ الداخليّةُ والمقابلةُ بالتالي، ومعها مراجعةٌ مودَعةٌ "
    "لهذه المادّة وهذا المعنى وهذا الشاهد تقول `SUPPORTS_THE_MEANING`. "
    "**والمطابقةُ النصّيّةُ ليست شرطًا ولا مانعًا**: تُقاس وتُعرَض، ولا تُرفَع "
    "إسنادًا، ولا يُقرأ غيابُها نفيًا له. وتخلُّفُ شرطٍ يُعلِّق هذا المرشَّحَ "
    "وحدَه بجنسِ سببه، ولا يُعلِّق غيرَه ولا يَرفُضه"
)


@dataclass(frozen=True, slots=True)
class VerificationReading:
    """نتيجةُ التحقّق لمرشَّحٍ واحد: شهاداتُه الثلاث، وحالُه، وسببُ تعليقه.

    والحقولُ مفصولةٌ بما يُثبِته كلُّ فحصٍ وحدَه: `segment_in_row` وجودُ
    المقطع في الصفّ، و`attribution` نسبتُه إلى المادّة، و`textual_match`
    وجودُ سلسلةٍ نصّيّة، و`semantic_support` إسنادُ المعنى. ولا يُقرأ أدناها
    دليلًا على أعلاها، ولا غيابُ أدناها نفيًا لأعلاها.

    و`refusal` **يُسجَّل ولا يَقضي**: صيغةُ النفي واقعةٌ تُحفَظ لتُقوَّم، ولا
    تقلب حالَ الاعتماد آليًّا؛ فقلبُ الحكم بلا تعيينِ دعواه مثلُ إهماله.
    """

    candidate: LinkCandidate
    source_integrity: bool
    segment_in_row: bool
    probe_refutes_the_row: bool
    boundary: BoundaryStanding
    attribution: AttributionCheck
    textual_match: TextualMatchCheck
    semantic_support: SemanticSupportCheck
    refusal: RefusalStanding
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
    """مِسبارٌ **ناقضٌ لا مُثبِت**: يُسقِط نسبةً، ولا يرفع غيرَ المعيَّنة محقَّقةً."""

    bare = strip_diacritics(sentence)
    letters: list[str] = []
    for character in row["root_full"].strip():
        if character in THE_LETTER_NAMES and character not in letters:
            letters.append(character)
    if not letters:
        return AttributionCheck.REFUTED_BY_THE_PROBE
    for character in letters:
        if not any(name in bare for name in THE_LETTER_NAMES[character]):
            return AttributionCheck.REFUTED_BY_THE_PROBE
    return AttributionCheck.NOT_DETERMINED


def _textual_match_of(meaning: str, witness: str) -> TextualMatchCheck:
    """أتقع صياغةُ المعنى في الشاهد نصًّا؟ وجودُ سلسلةٍ لا إسنادُ معنًى."""

    if meaning in witness:
        return TextualMatchCheck.MATCHES_VERBATIM
    if strip_diacritics(meaning) in strip_diacritics(witness):
        return TextualMatchCheck.MATCHES_UNDER_A_NAMED_NORMALISATION
    return TextualMatchCheck.NO_TEXTUAL_MATCH


def _carries_a_refusal(witness: str) -> bool:
    """أتقع في الشاهد صيغةُ نفيٍ؟ رصدُ تركيبٍ لا تحقيقٌ لتعارض."""

    bare = strip_diacritics(witness)
    return any(formula in bare for formula in THE_REFUSAL_FORMULAE)


def _refusal_standing(
    material_key: str,
    witness: str,
    determinations: tuple[CounterClaimDetermination, ...] = (),
) -> RefusalStanding:
    """منزلةُ النفي: لا صيغةَ، أو صيغةٌ غيرُ معيَّنةِ المنفيّ، أو تعارضٌ محقَّق."""

    if not _carries_a_refusal(witness):
        return RefusalStanding.NO_NEGATION_FORM
    bare = strip_diacritics(witness)
    for determination in determinations:
        if determination.material_key == material_key and (
            strip_diacritics(determination.negating_text) in bare
        ):
            return RefusalStanding.DETERMINED_COUNTER_CLAIM
    return RefusalStanding.TARGET_UNDETERMINED


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
    boundaries: tuple[BoundaryAttestation, ...] = (),
    determinations: tuple[CounterClaimDetermination, ...] = (),
) -> VerificationReading:
    """افحص مرشَّحًا بفحوصٍ مفصولةٍ بما يُثبِته كلٌّ منها، وأخرِج حالَه وسببَه.

    والفحوصُ تُعاد من البايتات عند كلّ نداء: لا يُصدَّق حقلٌ محفوظٌ في
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
    segment_in_row = span == candidate.witness.text
    probe_refutes = segment_in_row and (
        _attribution_of(row, candidate.witness.text)
        is AttributionCheck.REFUTED_BY_THE_PROBE
    )
    boundary = _boundary_standing(row, candidate.row_index, boundaries)
    if not segment_in_row or probe_refutes:
        attribution = AttributionCheck.REFUTED_BY_THE_PROBE
    elif boundary is BoundaryStanding.VERIFIED_BY_A_DEPOSITED_WITNESS:
        attribution = AttributionCheck.VERIFIED_BY_A_DEPOSITED_WITNESS
    else:
        attribution = AttributionCheck.NOT_DETERMINED

    textual_match = _textual_match_of(
        candidate.candidate_meaning, candidate.witness.text
    )

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
    if review is None:
        support = SemanticSupportCheck.NOT_ESTABLISHED_WITHOUT_A_REVIEW
    elif review.verdict is ReviewVerdict.SUPPORTS_THE_MEANING:
        support = SemanticSupportCheck.ESTABLISHED_BY_A_DEPOSITED_REVIEW
    else:
        support = SemanticSupportCheck.DENIED_BY_A_DEPOSITED_REVIEW

    refusal = _refusal_standing(
        candidate.material_key, candidate.witness.text, determinations
    )

    unmet: list[str] = []
    genus: SuspensionGenus | None = None
    if not source_integrity:
        unmet.append("سلامةُ المصدر: الشاهدُ لا يقع في النسخة المقروءة بهذه البصمة")
        genus = SuspensionGenus.COUNTER_EVIDENCE
    if not segment_in_row:
        unmet.append("وقوعُ المقطع: الإزاحتان لا تُخرِجان هذا النصَّ من الصفّ")
        genus = genus or SuspensionGenus.COUNTER_EVIDENCE
    elif probe_refutes:
        unmet.append("صحّةُ النسبة: مِسبارُ تسمية الحروف ينقض نسبةَ المقطع")
        genus = genus or SuspensionGenus.COUNTER_EVIDENCE
    elif attribution is AttributionCheck.NOT_DETERMINED:
        unmet.append(
            "صحّةُ النسبة: الصفُّ موسومٌ بالمفتاح ولا شهادةَ حدٍّ مودَعةٍ تُحقِّق "
            "تبعيّةَ المقطع لهذه المادّة"
        )
        genus = genus or SuspensionGenus.TOOL_UNAVAILABLE
    if support is SemanticSupportCheck.NOT_ESTABLISHED_WITHOUT_A_REVIEW:
        unmet.append(
            "الإسنادُ الدلاليّ: لا مراجعةَ مودَعةً تقول إنّ هذا الشاهدَ يُسنِد "
            "هذا المعنى وبالجهة المطلوبة"
        )
        genus = genus or SuspensionGenus.TOOL_UNAVAILABLE
    elif support is SemanticSupportCheck.DENIED_BY_A_DEPOSITED_REVIEW:
        unmet.append("الإسنادُ الدلاليّ: مراجعةٌ مودَعةٌ تنفي إسنادَ هذا الشاهد")
        genus = genus or SuspensionGenus.COUNTER_EVIDENCE
    if refusal is RefusalStanding.DETERMINED_COUNTER_CLAIM:
        unmet.append("تعارضٌ محقَّقٌ: تعيينٌ مودَعٌ يُبيّن الدعوى التي يُعارضها")
        genus = SuspensionGenus.COUNTER_EVIDENCE

    standing = AdmissionStanding.ADMITTED if not unmet else AdmissionStanding.SUSPENDED
    return VerificationReading(
        candidate=candidate,
        source_integrity=source_integrity,
        segment_in_row=segment_in_row,
        probe_refutes_the_row=probe_refutes,
        boundary=boundary,
        attribution=attribution,
        textual_match=textual_match,
        semantic_support=support,
        refusal=refusal,
        review=review,
        standing=standing,
        suspension_genus=genus,
        unmet_conditions=tuple(unmet),
        scope=(
            "نطاقُ الاعتماد: أنّ هذه النسخةَ من هذا المعجم أسندت هذا المعنى "
            "لهذه المادّة بشهادةِ حدٍّ ومراجعةٍ مودَعتَين؛ ولا يمتدّ إلى مشتقٍّ "
            "ولا إلى وقوعٍ في عبارة، ولا يُقرأ تصديقًا لواقعةٍ خارجَ اللغة"
        ),
    )


# --- السلسلةُ وبلوغُها ---------------------------------------------------------


def chain_reach(
    root: Path | None = None,
    *,
    reviews: tuple[ReviewAttestation, ...] = (),
    boundaries: tuple[BoundaryAttestation, ...] = (),
    determinations: tuple[CounterClaimDetermination, ...] = (),
) -> tuple[tuple[LinkChainRung, bool, str], ...]:
    """أيُّ الوصلات بلغتها الآلةُ فعلًا، وبأيّ شرط؛ ولا تُدَّعى وصلةٌ لم تُنفَّذ."""

    source = _source_reference(root)
    candidates = link_candidates(root)
    admitted = sum(
        1
        for candidate in candidates
        if verify(
            candidate,
            root=root,
            reviews=reviews,
            boundaries=boundaries,
            determinations=determinations,
        ).is_admitted
    )
    verified_rows = sum(
        1
        for index, row in _sample_rows(root)
        if _boundary_standing(row, index, boundaries)
        is BoundaryStanding.VERIFIED_BY_A_DEPOSITED_WITNESS
    )
    return (
        (
            LinkChainRung.MATERIAL_KEY,
            True,
            f"مفاتيحُ الموادّ مقروءةٌ من نسخةٍ بصمتُها {source.measured_sha256[:8]}…",
        ),
        (
            LinkChainRung.VERIFIED_MATERIAL,
            verified_rows > 0,
            "المادّةُ لا تُحقَّق بالكاشف بل بشهادةِ حدٍّ مودَعةٍ فُحِص فيها المنتهى "
            "والترويساتُ الداخليّةُ والمقابلةُ بالتالي؛ والمُحقَّقُ الآن "
            f"{verified_rows} من {THE_CANDIDATE_SAMPLE_SIZE} "
            f"({A_HEADER_DETECTOR_PROPOSES_A_BOUNDARY_IT_DOES_NOT_VERIFY})",
        ),
        (
            LinkChainRung.EXTRACTED_MEANING,
            admitted > 0,
            f"المعنى المستخرَجُ يبلغ بالاعتماد وحدَه؛ والمعتمَدُ الآن {admitted}",
        ),
        (
            LinkChainRung.LAFZ,
            False,
            THE_LAFZ_LINK_IS_OUT_OF_THIS_UNITS_SCOPE_NOT_IMPOSSIBLE,
        ),
        (
            LinkChainRung.USAGE,
            False,
            THE_LAFZ_LINK_IS_OUT_OF_THIS_UNITS_SCOPE_NOT_IMPOSSIBLE,
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
    refusal: RefusalStanding
    suspension_genera: tuple[SuspensionGenus, ...]


def dal_readings(
    root: Path | None = None,
    *,
    reviews: tuple[ReviewAttestation, ...] = (),
    boundaries: tuple[BoundaryAttestation, ...] = (),
    determinations: tuple[CounterClaimDetermination, ...] = (),
) -> tuple[DalReading, ...]:
    """الدوالُّ العشرون كلُّهم، بما فيهم الفارغُ والمشتبه؛ ولا يُطوى صفٌّ متعذِّر."""

    verifications = tuple(
        verify(
            candidate,
            root=root,
            reviews=reviews,
            boundaries=boundaries,
            determinations=determinations,
        )
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
        boundary = _boundary_standing(row, index, boundaries)
        standing = weigh_declared_axes_count(row)
        body = _nfc(row["body_text"])
        start, end = _first_sentence(body)
        refusal = _refusal_standing(
            f"{row['root_full']}:{row['entry_num']}", body[start:end], determinations
        )
        if not mine:
            processing = DalProcessing.NO_ADMITTED_OUTPUT
        elif (
            boundary is not BoundaryStanding.VERIFIED_BY_A_DEPOSITED_WITNESS
            or standing != AxesStanding.AGREES
        ):
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
                refusal=refusal,
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
                        if refusal is RefusalStanding.DETERMINED_COUNTER_CLAIM
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
    boundaries: tuple[BoundaryAttestation, ...] = (),
    determinations: tuple[CounterClaimDetermination, ...] = (),
) -> ProvenanceShares:
    """النسبُ الثلاثُ معدودةً؛ ولا يُدَّعى توليدُ معنًى من الـ١١٦ ههنا."""

    candidates = link_candidates(root)
    admitted = sum(
        1
        for candidate in candidates
        if verify(
            candidate,
            root=root,
            reviews=reviews,
            boundaries=boundaries,
            determinations=determinations,
        ).is_admitted
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
    boundaries: tuple[BoundaryAttestation, ...] = (),
    determinations: tuple[CounterClaimDetermination, ...] = (),
) -> dict[str, int]:
    """الأعدادُ بوحداتٍ منفصلة؛ ولا يُجمَع دالٌّ إلى محورٍ ولا محورٌ إلى مرشَّح.

    وليس في هذا السجلّ معادلةُ «٢٠ = أزواجٌ + معلَّقون»: الدالُّ وحدةٌ،
    والمحورُ وحدةٌ، والمرشَّحُ وحدةٌ؛ والدالُّ الواحدُ يُخرِج محاورَ عدّة.
    """

    readings = dal_readings(
        root,
        reviews=reviews,
        boundaries=boundaries,
        determinations=determinations,
    )
    verifications = tuple(
        verify(
            candidate,
            root=root,
            reviews=reviews,
            boundaries=boundaries,
            determinations=determinations,
        )
        for candidate in link_candidates(root)
    )
    return {
        "دوال": len(readings),
        "محاور_مكتوبة": sum(reading.declared_axes for reading in readings),
        "مرشحات": len(verifications),
        "معتمدون": sum(1 for reading in verifications if reading.is_admitted),
        "معلقون": sum(1 for reading in verifications if not reading.is_admitted),
        "دوال_بلا_مرشح": sum(1 for reading in readings if reading.candidates == 0),
        "دوال_حدها_مرشح_بالكاشف": sum(
            1
            for reading in readings
            if reading.boundary is BoundaryStanding.CANDIDATE_BY_THE_DETECTOR
        ),
        "دوال_حدها_غير_معين": sum(
            1
            for reading in readings
            if reading.boundary is BoundaryStanding.UNDETERMINED_BY_THE_DETECTOR
        ),
        "دوال_حدها_محقق_بشهادة": sum(
            1
            for reading in readings
            if reading.boundary is BoundaryStanding.VERIFIED_BY_A_DEPOSITED_WITNESS
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
        "دوال_في_شاهدها_صيغة_نفي_غير_معينة": sum(
            1
            for reading in readings
            if reading.refusal is RefusalStanding.TARGET_UNDETERMINED
        ),
        "دوال_تعارضها_محقق": sum(
            1
            for reading in readings
            if reading.refusal is RefusalStanding.DETERMINED_COUNTER_CLAIM
        ),
    }


def reconciliation_rows(
    root: Path | None = None,
    *,
    reviews: tuple[ReviewAttestation, ...] = (),
    boundaries: tuple[BoundaryAttestation, ...] = (),
    determinations: tuple[CounterClaimDetermination, ...] = (),
) -> tuple[dict[str, object], ...]:
    """جدولُ العشرين صفًّا صفًّا؛ ولا عددَ ضمنيٌّ ولا دالٌّ يسقط من الحصيلة.

    فالدوالُّ الثلاثةُ بلا مرشَّحٍ صفوفٌ ههنا كغيرها: لا تختفي لأنّ عدّادَ
    المرشَّحات لا يشملها، ويُقرأ في صفِّها لماذا لم يُخرِج محورًا.
    """

    readings = dal_readings(
        root, reviews=reviews, boundaries=boundaries, determinations=determinations
    )
    by_row: dict[int, list[VerificationReading]] = {}
    for candidate in link_candidates(root):
        checked = verify(
            candidate,
            root=root,
            reviews=reviews,
            boundaries=boundaries,
            determinations=determinations,
        )
        by_row.setdefault(candidate.row_index, []).append(checked)

    rows: list[dict[str, object]] = []
    for reading in readings:
        mine = by_row.get(reading.row_index, [])
        rows.append(
            {
                "دال": reading.root_display,
                "مفتاح_المادة": reading.material_key,
                "رتبة_الصف": reading.row_index,
                "محاور_مصرحة": reading.axes_count_standing,
                "محاور_مكتوبة": reading.declared_axes,
                "مرشحات": reading.candidates,
                "معتمدون": reading.admitted,
                "معلقون": reading.candidates - reading.admitted,
                "مرفوضون": 0,
                "حد_المادة": reading.boundary.value,
                "منزلة_النفي": reading.refusal.value,
                "حال_المعالجة": reading.processing.value,
                "معاني_مرشحة": [
                    checked.candidate.candidate_meaning for checked in mine
                ],
                "مطابقة_نصية": [checked.textual_match.value for checked in mine],
                "إسناد_دلالي": [checked.semantic_support.value for checked in mine],
                "أسباب_التعليق": [list(checked.unmet_conditions) for checked in mine],
                "لماذا_لا_مرشح": (
                    None
                    if mine
                    else "لا محورَ مكتوبًا في `semantic_axes`؛ فراغُ تصريحٍ لا تصريحٌ بغياب"
                ),
            }
        )
    return tuple(rows)


def suspension_reason_census(
    root: Path | None = None,
    *,
    reviews: tuple[ReviewAttestation, ...] = (),
    boundaries: tuple[BoundaryAttestation, ...] = (),
    determinations: tuple[CounterClaimDetermination, ...] = (),
) -> dict[str, int]:
    """أسبابُ التعليق **متداخلةٌ لا متنافية**: كلُّ سببٍ يُعَدّ وحدَه، ثمّ تُعَدّ
    تقاطعاتُه؛ فجمعُ الأعمدة لا يساوي عددَ المعلَّقين ولا يُراد له ذلك."""

    singles: dict[str, int] = {}
    joint: dict[tuple[str, ...], int] = {}
    suspended = 0
    for candidate in link_candidates(root):
        checked = verify(
            candidate,
            root=root,
            reviews=reviews,
            boundaries=boundaries,
            determinations=determinations,
        )
        if checked.is_admitted:
            continue
        suspended += 1
        heads = tuple(
            condition.split(":", 1)[0].strip() for condition in checked.unmet_conditions
        )
        for head in heads:
            singles[head] = singles.get(head, 0) + 1
        joint[heads] = joint.get(heads, 0) + 1
    census = {"معلقون": suspended}
    census.update({f"سبب: {head}": count for head, count in sorted(singles.items())})
    census.update(
        {"تقاطع: " + " + ".join(heads): count for heads, count in sorted(joint.items())}
    )
    return census


# --- السجلّ: سطرٌ لكلّ واقعة ----------------------------------------------------


def report_rows(
    root: Path | None = None,
    *,
    reviews: tuple[ReviewAttestation, ...] = (),
    boundaries: tuple[BoundaryAttestation, ...] = (),
    determinations: tuple[CounterClaimDetermination, ...] = (),
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
    for rung, reached, why in chain_reach(
        root, reviews=reviews, boundaries=boundaries, determinations=determinations
    ):
        rows.append(
            {
                "نوع": "وصلة",
                "الوصلة": rung.value,
                "بلغت": reached,
                "بيان": why,
            }
        )
    for reading in dal_readings(
        root, reviews=reviews, boundaries=boundaries, determinations=determinations
    ):
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
                "منزلة_النفي": reading.refusal.value,
                "أجناس_التعليق": [genus.value for genus in reading.suspension_genera],
            }
        )
    for candidate in link_candidates(root):
        checked = verify(
            candidate,
            root=root,
            reviews=reviews,
            boundaries=boundaries,
            determinations=determinations,
        )
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
                "وقوع_المقطع_في_الصف": checked.segment_in_row,
                "المسبار_ينقض_النسبة": checked.probe_refutes_the_row,
                "حد_المادة": checked.boundary.value,
                "صحة_النسبة": checked.attribution.value,
                "مطابقة_نصية": checked.textual_match.value,
                "إسناد_دلالي": checked.semantic_support.value,
                "منزلة_النفي": checked.refusal.value,
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
    shares = provenance_shares(
        root, reviews=reviews, boundaries=boundaries, determinations=determinations
    )
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
