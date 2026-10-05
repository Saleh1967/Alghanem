"""تطبيقُ `G0.LEX-0` على «مقاييس اللغة»: شاهدٌ معجميٌّ مفهرسٌ بالجذر، لا معنًى.

هذه الوحدةُ **محوّلٌ** لا جزءٌ من القلب: الاتّجاه `adapter → core` ولا عكس،
فلا يستورد منها `lexical_evidence_layer` شيئًا، وتقرأ هي من القلب وحدَه.
وموضعُها في الترتيب المُصرَّح `SyntheticAdapter → MASAQAdapter → QuranAdapter`
خارجٌ عن محوّلات المدوَّنات النصّيّة: المقاييسُ **معجمٌ** لا نصًّا، فهو مُدخَلُ
شاهدٍ لا مُدخَلُ تغطية.

**والبايتاتُ لا تُقرأ هنا مرّتين**: `maqayis_root_table_deposit` هو المُبصِّم،
فتُقرأ الصفوفُ منه وحدَه ويُرفَض الملفُّ إن خالف الطولَ أو البصمة. ونسخُ
منطق القراءة هنا يُنشئ بابًا ثانيًا إلى بايتاتٍ يُظَنّ أنّها مُبصَّمة.

**ولا تسجيلَ قبليًّا بأثرٍ رجعيّ**: `NoRetroactivePreregistrationOfMaqayis`.
بايتاتُ هذا الملفّ قُرئت قبل هذه المرحلة، فما هنا **تخصيصٌ** لا تسجيلٌ قبليّ،
ولا يُسمّى بغير اسمه.

**والسطحُ ليس جذرًا**: `SurfaceIsNotRoot`. المقاييسُ مفهرسٌ بالجذر، والوقوعُ
سطحٌ؛ فالمطابقةُ تمرُّ بـ`DerivedMorphologicalCandidate` — بجذرٍ مُقترَحٍ
بأساسِ اشتقاقٍ مُصرَّحٍ به — ولا تُجرى على الصورة الخام. ومَن طابق سطحًا بجذرٍ
فقد أسقط طبقةً كاملةً وسمّى الساقطَ نجاحًا. ولهذا تُرَدّ مقارنةُ هذا المعجم
بمقارِنٍ مفهرسٍ بالسطح `NOT_COMPARABLE` لا فشلًا.

**والعددُ المنقولُ ليس مقدارًا مُشتَقًّا**: `QuotedNumberIsNotDerivedMeasure`.
`axes_count` في الملفّ نصٌّ كتبه المصدر، فيُحفَظ **نصًّا كما ورد** ولا يُحوَّل
عددًا ولا يُجمَع ولا يُقارَن؛ فتحويلُه يجعل هذه الطبقةَ مُصدِرةَ مقدارٍ لم
تَقِسْه. ولهذا يرفض حارسُ الحقول `MaqayisRootEvidence` عن قصد: هي سجلُّ منقولٍ
من مصدر، لا مُرشَّحٌ من مُرشَّحات النواة (`ReportedRecordIsNotCoreCandidate`).

**والفروعُ الثلاثةُ لا تُدمَج**: لكلِّ فرعٍ فهرسُه، وثمنُه معروضٌ بأعيانه —
الجذورُ المنصهرةُ تحته وما أتلفته قاعدتُه — ولا يُرجَّح فرعٌ على فرع.

تسجيلٌ لا سلطة: أقصى ما يخرج من هنا `LexicalEvidenceCandidate`؛ لا مدلولَ
مُثبَت، ولا إفادة، ولا `E0`، ولا استيراد من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final

from .lexical_evidence_layer import (
    DerivedMorphologicalCandidate,
    LexicalEvidenceCandidate,
    LexicalMatchCandidate,
)
from .lexical_evidence_specification import (
    A_LEXICON_IS_A_WITNESS_NOT_AN_AUTHORITY_NOTE,
    NO_RETROACTIVE_PREREGISTRATION_OF_MAQAYIS_NOTE,
    QUOTED_DEFINITION_IS_NOT_DERIVED_SIGNIFIED_NOTE,
    ROOT_EVIDENCE_IS_NOT_SURFACE_MEANING_NOTE,
    NormalizationBranch,
)
from .maqayis_root_table_deposit import (
    FROZEN_ROOT_TABLE,
    root_table_rows,
)
from .root_orthography_bridge import (
    HAMZA_TO_BARE_ALIF_RULE,
    HAMZA_TO_CARRIED_ALIF_RULE,
    NormalisationRule,
    fusions_under,
    normalise_root,
)

__all__ = [
    "BRANCH_RULE_CHAINS",
    "MAQAYIS_INDEXING_UNIT",
    "MAQAYIS_LEXICON_ID",
    "QUOTED_NUMBER_IS_NOT_DERIVED_MEASURE_NOTE",
    "REPORTED_RECORD_IS_NOT_CORE_CANDIDATE_NOTE",
    "SURFACE_IS_NOT_ROOT_NOTE",
    "MaqayisLexicalEvidenceError",
    "MaqayisRootEvidence",
    "MaqayisRootIndex",
    "build_root_index",
    "evidence_for_match",
    "match_derived_root",
    "read_root_evidence",
]

MAQAYIS_LEXICON_ID: Final[str] = "maqayis:by_root:csv_999"

MAQAYIS_INDEXING_UNIT: Final[str] = "root"
"""وحدةُ فهرسة هذا المعجم؛ ومقارنتُه بمُقارِنٍ سطحيٍّ غيرُ قابلةٍ للمقارنة."""

SURFACE_IS_NOT_ROOT_NOTE: Final[str] = (
    "SurfaceIsNotRoot: المقاييسُ مفهرسٌ بالجذر والوقوعُ سطحٌ، فالمطابقةُ تمرُّ "
    "بجذرٍ مُقترَحٍ بأساسِ اشتقاقٍ مُصرَّحٍ به؛ ومطابقةُ السطح بالجذر إسقاطٌ "
    "لطبقةٍ كاملةٍ ثمّ تسميةُ الساقط نجاحًا"
)

QUOTED_NUMBER_IS_NOT_DERIVED_MEASURE_NOTE: Final[str] = (
    "QuotedNumberIsNotDerivedMeasure: عددٌ كتبه المصدرُ في حقلٍ يُحفَظ نصًّا "
    "كما ورد، ولا يُحوَّل عددًا ولا يُجمَع ولا يُقارَن؛ فتحويلُه يجعل هذه "
    "الطبقةَ مُصدِرةَ مقدارٍ لم تَقِسْه، وهو عينُ ما يمنعه حارسُ الحقول"
)

REPORTED_RECORD_IS_NOT_CORE_CANDIDATE_NOTE: Final[str] = (
    "ReportedRecordIsNotCoreCandidate: `MaqayisRootEvidence` سجلُّ منقولٍ من "
    "مصدرٍ خارجيّ، لا مُرشَّحٌ من مُرشَّحات سقف النواة؛ فحارسُ الحقول يردُّها "
    "عن قصدٍ لا عن سهو، وحقولُها تحمل لاحقة `_as_reported` لأنّ النقلَ جزءٌ من "
    "اسم الحقل لا تعليقٌ عليه"
)

BRANCH_RULE_CHAINS: Final[dict[NormalizationBranch, tuple[NormalisationRule, ...]]] = {
    NormalizationBranch.EXACT: (),
    NormalizationBranch.NORMALIZE_TO_ALIF: (HAMZA_TO_BARE_ALIF_RULE,),
    NormalizationBranch.NORMALIZE_TO_HAMZA_ALIF: (HAMZA_TO_CARRIED_ALIF_RULE,),
}
"""سلسلةُ قواعدِ كلّ فرع؛ و`EXACT` سلسلةٌ خاليةٌ مُصرَّحٌ بها لا فرعٌ غائب."""


class MaqayisLexicalEvidenceError(ValueError):
    """رفضٌ صريحٌ في محوّل المقاييس؛ ولا يُحمَل المدخلُ على أقرب مطابقة."""


@dataclass(frozen=True, slots=True)
class MaqayisRootEvidence:
    """مدخلُ جذرٍ منقولٌ بحروفه؛ كلُّ حقلٍ منه نصُّ المصدر لا قراءةً له.

    و`axes_count_as_reported` نصٌّ لا عدد: `QuotedNumberIsNotDerivedMeasure`.
    """

    root_full_as_reported: str
    root_type_as_reported: str
    entry_num_as_reported: str
    root_display_as_reported: str
    semantic_axes_as_reported: str
    axes_count_as_reported: str
    chapter_header_as_reported: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.root_full_as_reported, "الجذرُ التامّ"),
            (self.root_type_as_reported, "نوعُ الجذر"),
            (self.entry_num_as_reported, "رقمُ المدخل"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise MaqayisLexicalEvidenceError(f"{label} نصٌّ غير فارغ كما ورد.")
        for value in (
            self.root_display_as_reported,
            self.semantic_axes_as_reported,
            self.axes_count_as_reported,
            self.chapter_header_as_reported,
        ):
            if not isinstance(value, str):
                raise MaqayisLexicalEvidenceError(
                    "الحقلُ المنقولُ نصُّ المصدر كما ورد؛ "
                    + QUOTED_NUMBER_IS_NOT_DERIVED_MEASURE_NOTE
                )

    @property
    def entry_ref(self) -> str:
        """مرجعُ المدخل: جذرُه ورقمُه معًا، فالجذرُ وحدَه يتكرّر بمداخلَ عدّة."""

        return f"{self.root_full_as_reported}#{self.entry_num_as_reported}"

    @property
    def is_a_derived_signified(self) -> bool:
        """تعريفٌ منقولٌ ليس مدلولًا مُشتَقًّا؛ الجوابُ ثابت."""

        return False

    @property
    def refusal_note(self) -> str:
        return QUOTED_DEFINITION_IS_NOT_DERIVED_SIGNIFIED_NOTE


def read_root_evidence(root: Path | None = None) -> tuple[MaqayisRootEvidence, ...]:
    """اقرأ المداخلَ من البايتات المُبصَّمة عبر المُودِع وحدَه، لا بقراءةٍ ثانية.

    و`body_text` و`poetry_evidence` **لا يُرفَعان هنا**: هما نصُّ المعجم
    بحروفه، وحملُهما في سجلٍّ يُمرَّر يجعل النقلَ الحرفيَّ ناتجَ طبقةٍ؛
    ومرجعُ المدخل يكفي للرجوع إليهما في البايتات المُبصَّمة نفسِها.
    """

    return tuple(
        MaqayisRootEvidence(
            root_full_as_reported=row["root_full"],
            root_type_as_reported=row["root_type"],
            entry_num_as_reported=row["entry_num"],
            root_display_as_reported=row["root_display"],
            semantic_axes_as_reported=row["semantic_axes"],
            axes_count_as_reported=row["axes_count"],
            chapter_header_as_reported=row["chapter_header"],
        )
        for row in root_table_rows(root)
    )


@dataclass(frozen=True, slots=True)
class MaqayisRootIndex:
    """فهرسُ جذورٍ تحت فرعٍ واحدٍ بعينه، ومعه ثمنُ فرعه معروضًا.

    ولا يُبنى فهرسٌ يجمع فرعين: الفرعان يختلفان فيما يُتلفانه، فجمعُهما يخفي
    أيَّ إتلافٍ أنتج أيَّ مطابقة.
    """

    branch: NormalizationBranch
    entries_by_form: dict[str, tuple[MaqayisRootEvidence, ...]]
    fusions: tuple[tuple[str, tuple[str, ...]], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.branch, NormalizationBranch):
            raise MaqayisLexicalEvidenceError("الفرعُ عضوٌ في مفردته الثلاثية.")
        if not self.entries_by_form:
            raise MaqayisLexicalEvidenceError("فهرسٌ خالٍ ليس فهرسًا.")

    @property
    def rule_chain(self) -> tuple[NormalisationRule, ...]:
        return BRANCH_RULE_CHAINS[self.branch]

    @property
    def what_it_destroys(self) -> tuple[str, ...]:
        """ما تُتلفه قواعدُ هذا الفرع بنصّها؛ خاليةٌ في الفرع الصريح."""

        return tuple(rule.what_it_destroys for rule in self.rule_chain)

    def forms_matching(self, normalized_form: str) -> tuple[MaqayisRootEvidence, ...]:
        return self.entries_by_form.get(normalized_form, ())


def _normalize_under(branch: NormalizationBranch, form: str) -> str:
    chain = BRANCH_RULE_CHAINS[branch]
    if not chain:
        return form
    return normalise_root(form, chain).after


def build_root_index(
    branch: NormalizationBranch, root: Path | None = None
) -> MaqayisRootIndex:
    """ابنِ فهرسَ فرعٍ واحد، وسجِّل معه الجذورَ المنصهرةَ تحته بأعيانها."""

    if not isinstance(branch, NormalizationBranch):
        raise MaqayisLexicalEvidenceError("الفرعُ عضوٌ في مفردته الثلاثية.")
    entries = read_root_evidence(root)
    grouped: dict[str, list[MaqayisRootEvidence]] = {}
    for entry in entries:
        key = _normalize_under(branch, entry.root_full_as_reported)
        grouped.setdefault(key, []).append(entry)
    chain = BRANCH_RULE_CHAINS[branch]
    fusions: tuple[tuple[str, tuple[str, ...]], ...] = ()
    if chain:
        fusions = tuple(
            (record.normalised, record.sources)
            for record in fusions_under(
                {entry.root_full_as_reported for entry in entries}, chain
            )
        )
    return MaqayisRootIndex(
        branch=branch,
        entries_by_form={key: tuple(value) for key, value in grouped.items()},
        fusions=fusions,
    )


def match_derived_root(
    derived: DerivedMorphologicalCandidate, index: MaqayisRootIndex
) -> tuple[LexicalMatchCandidate, ...]:
    """طابِق **الجذرَ المُقترَح** لا الصورةَ الخام، وتحت فرعِ الفهرس نفسِه.

    ويُرَدّ اختلافُ الفرع بين الدالّ والفهرس: مطابقةُ دالٍّ مُطبَّعٍ بقاعدةٍ
    على فهرسٍ مبنيٍّ بأخرى تنسب إلى إحدى القاعدتين أثرَ الأخرى.
    """

    if not isinstance(derived, DerivedMorphologicalCandidate):
        raise MaqayisLexicalEvidenceError(
            "المطابقةُ تمرُّ بمُرشَّحٍ صرفيٍّ مُشتَقّ؛ " + SURFACE_IS_NOT_ROOT_NOTE
        )
    if not isinstance(index, MaqayisRootIndex):
        raise MaqayisLexicalEvidenceError("الفهرسُ من بنيته وحدها.")
    if derived.signifier.trace.branch is not index.branch:
        raise MaqayisLexicalEvidenceError(
            "فرعُ الدالّ يخالف فرعَ الفهرس، فلا تُنسَب إلى قاعدةٍ أثرُ أخرى."
        )
    key = _normalize_under(index.branch, derived.proposed_root)
    return tuple(
        LexicalMatchCandidate(
            signifier=derived.signifier,
            lexicon_id=MAQAYIS_LEXICON_ID,
            matched_entry_ref=entry.entry_ref,
            indexing_unit=MAQAYIS_INDEXING_UNIT,
        )
        for entry in index.forms_matching(key)
    )


def evidence_for_match(
    match: LexicalMatchCandidate, entry: MaqayisRootEvidence
) -> LexicalEvidenceCandidate:
    """ارفع الشاهدَ المعجميَّ بمرجعه وأثرِ مصدره؛ ولا يُرفَع به معنًى.

    وأثرُ المصدر يحمل بصمةَ الملفّ المُجمَّد، فشاهدٌ بلا بصمةِ بايتاته يُقرأ
    بعد جلساتٍ شاهدًا من نسخةٍ أخرى.
    """

    if not isinstance(match, LexicalMatchCandidate):
        raise MaqayisLexicalEvidenceError("الشاهدُ يقوم على مطابقة.")
    if not isinstance(entry, MaqayisRootEvidence):
        raise MaqayisLexicalEvidenceError("الشاهدُ يقوم على مدخلٍ منقول.")
    if match.matched_entry_ref != entry.entry_ref:
        raise MaqayisLexicalEvidenceError(
            "الشاهدُ يُرفَع عن المدخل الذي طابقه لا عن غيره."
        )
    return LexicalEvidenceCandidate(
        match=match,
        evidence_ref=entry.entry_ref,
        source_trace=(
            f"{MAQAYIS_LEXICON_ID}@sha256:{FROZEN_ROOT_TABLE.sha256_hex}"
            f" — {A_LEXICON_IS_A_WITNESS_NOT_AN_AUTHORITY_NOTE}"
            f" — {ROOT_EVIDENCE_IS_NOT_SURFACE_MEANING_NOTE}"
            f" — {NO_RETROACTIVE_PREREGISTRATION_OF_MAQAYIS_NOTE}"
        ),
    )
