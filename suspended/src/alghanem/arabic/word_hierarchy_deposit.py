"""إيداعُ هرمية إعادة بناء الكلمة نصًّا مُبصَّمًا، وسجلُّ تعارضاتها — بلا حسم.

**ما تفعله هذه الوحدة**: تُثبِّت بايتاتِ وثيقةٍ وصلت من محادثةٍ خارجية في ثلاثة
نصوص، وتُسجِّل منزلةَ كلّ عقدةٍ فيها، وما سُحِب بينها، ومنزلةَ كلّ رقمٍ ورد،
ومواضعَ تعارضها مع ما في هذه الشجرة. لا أكثر.

`THE_DEPOSIT_IS_NOT_AN_ADOPTION`: إيداعُ نصٍّ ليس تصديقًا لرقمٍ فيه ولا
لتصنيف، على منوال `gflk_specification_deposit`. وللشجرة سابقةٌ في هذا بعينه:
دعوى «١٠٠٪» أُعيد اشتقاقُها فخرجت ٩٩٫٩٩٢٢٥١٪ (`gflk_codec_revision_audit`).

`A_SUPERSEDED_VERSION_IS_RECORDED_NOT_ERASED`: وصلت الهرميةُ في نسختين،
والثانيةُ تُعلن أنّها «تحلّ محلّ الأولى بالكامل»، ثمّ وصل تجميدٌ ثالثٌ يُلغي
رقمَ الفجوة. فتُودَع النصوصُ الثلاثةُ معًا، ويُسجَّل لكلّ دعوى مسحوبةٍ ما حلّ
محلّها وسببُ سحبها كما ورد. وإيداعُ
المُصحَّح وحده يُخفي أنّ دعاوى سُحبت، فتُقرأ الهرميةُ بعد جلساتٍ كأنّها لم
تتغيّر — ويضيع أنفسُ ما فيها: مواضعُ التراجع. وما سقط بلا سببٍ مذكورٍ يُسمّى
`WITHDRAWN_WITHOUT_A_STATED_REASON` ولا يُحمَل على أنّه صُحِّح ولا على أنّه بقي.

`A_DEPENDENT_FIGURE_IS_NOT_A_SECOND_WITNESS`: رقمٌ مُشتَقٌّ من رقمٍ آخرَ في
الوثيقة نفسِها يُسمّي مَن يعتمد عليه في `depends_on_figure`، فلا يُقرأ رقمان
تابعان شاهدين مستقلّين. ورقمٌ وُصِف في الوثيقة بأنّه مخرجُ فئةٍ عُرِّفت
بالباقي (`is_residue_defined`) لا يُقبَل عند الإنشاء بلا هذا الوسم: فئةٌ
عُرِّفت بأنّها «ما تبقّى» لا يتبقّى بعدها شيءٌ بحكم تعريفها، فصفرُها تحصيلُ
حاصلٍ لا قياس — وهو ما يرفضه
`RESIDUE_DEFINED_EXCLUSIONS_ARE_NOT_INDEPENDENT_EVIDENCE` في
`encoding/sakin_adjacency` قبلَ وصول هذا التجميد.

`A_SUBMITTED_FREEZE_IS_NOT_A_FREEZE_HERE`: مُعرِّفُ تجميدٍ وصل من خارج الشجرة
يُحفَظ بحروفه ومعه حقلٌ يقول إنّه **غيرُ صادرٍ عنها**، على منوال
`SUBMITTED_FREEZE_IDENTIFIER` في `ibtida_wasl_waqf_registration`: محفوظٌ
ليُراجَع لا ليُعمَل به. ولا يُقبَل مُعرِّفٌ بلا هذا الحقل، فإعلانُ التجميد
يُقرأ بعد جلساتٍ تجميدًا في هذه الشجرة إن لم يُقيَّد بمصدره.

`AGGREGATION_DOES_NOT_LEVEL_EPISTEMIC_RANK`: عقدُ الهرمية متفاوتةُ المنزلة
تفاوتًا جنسيًّا، فتُصدَّر كلُّ عقدةٍ بمنزلتها من `LayerEpistemicStanding`
الرباعية المغلقة القائمة. ولا تُفتَح هنا مفردةُ منزلةٍ خامسة: من احتاج منزلةً
ليست فيها فقد احتاج تسجيلًا قبْليًّا آخر لا حقلًا يُضاف.

`A_NUMBER_WITHOUT_A_CORPUS_IS_NOT_A_MEASUREMENT`: كلُّ رقمٍ في الوثيقة —
نسبةً كان أو «صفرَ خرق» أو «ن/ن» — يُسجَّل غيرَ قابلٍ لإعادة الاشتقاق في هذه
الشجرة، بسببٍ مُسمًّى وشرطِ اشتقاقٍ مكتوب. فلم تصل مدوّنةٌ مُبصَّمة، ولا
`MeasurementRunManifest` (`arabic/encoding/measurement.py`)، ولا سجلُّ رصدٍ
يُطابَق عليه. و«صفر خرق» دعوى عمومٍ أثقلُ من النسبة لا أخفّ، إذ يكفي لنقضها
موضعٌ واحد.

`A_RECORDED_CONFLICT_IS_NOT_A_RESOLVED_ONE`: كلُّ تعارضٍ يحمل موضعَه في
الوثيقة، وما تقوله الشجرةُ في الموضع نفسه بمرجعه، و**ما يلزم لحسمه** — ولا
يحمل حسمًا. فمن سجّل تعارضًا وحسمه في الجلسة نفسها بلا مُدخَلٍ جديدٍ إنّما
رجّح ما كان يرجّحه سلفًا.

`THE_DIGEST_IS_READ_FROM_THE_FILE_NOT_WRITTEN_HERE`: بصمةُ الوثيقة تُشتَقّ من
بايتاتها عند القراءة، ولا تُكتَب رقمًا يُنسَخ فيُحدَّث وحده بعد تحرير.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا
تجميدَ `E0`، ولا استيرادَ من `kernel/`، ولا تقرأ هذه الوحدةَ وحدةٌ فيه. ولا
تُرفَع بها حواجزُ المخرج/الصفة، ولا حاجزُ «أل»/الوصل، ولا يُصدَر بها تصنيفُ
مقطعٍ أو وزنٍ أو مبنيّ. وليس فيها دالّةُ تحليلٍ ولا حقلُ نتيجة، وحارسٌ عند
الاستيراد يمنع تسلُّلَهما لاحقًا.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, fields
from enum import Enum
from pathlib import Path
from typing import Final

from .gflk_specification_deposit import ConflictStanding, ProvenanceGenus
from .pipeline_stations import repository_root_path
from .word_structure_dictionary import MEASURED_LAYERS
from .word_structure_dictionary_preregistration import (
    DictionaryLayer,
    LayerEpistemicStanding,
)

__all__ = [
    "AGGREGATION_DOES_NOT_LEVEL_EPISTEMIC_RANK_NOTE",
    "A_DEPENDENT_FIGURE_IS_NOT_A_SECOND_WITNESS_NOTE",
    "A_NUMBER_WITHOUT_A_CORPUS_IS_NOT_A_MEASUREMENT_NOTE",
    "A_RECORDED_CONFLICT_IS_NOT_A_RESOLVED_ONE_NOTE",
    "A_SUBMITTED_FREEZE_IS_NOT_A_FREEZE_HERE_NOTE",
    "A_SUPERSEDED_VERSION_IS_RECORDED_NOT_ERASED_NOTE",
    "HIERARCHY_RELATIVE_PATH",
    "NOT_ISSUED_BY_THIS_TREE",
    "SUBMITTED_FREEZE_IDENTIFIERS",
    "SUPERSEDED_CLAIMS",
    "THE_DEPOSIT_IS_NOT_AN_ADOPTION_NOTE",
    "THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE",
    "WITHDRAWN_WITHOUT_A_STATED_REASON",
    "WORD_HIERARCHY_CONFLICTS",
    "WORD_HIERARCHY_DEPOSIT",
    "WORD_HIERARCHY_NODES",
    "WORD_HIERARCHY_NUMERIC_CLAIMS",
    "HierarchyConflict",
    "HierarchyLevel",
    "HierarchyNode",
    "HierarchyNumericClaim",
    "SubmittedFreezeIdentifier",
    "SupersededClaim",
    "WordHierarchyDeposit",
    "WordHierarchyDepositError",
    "hierarchy_digest",
    "hierarchy_path",
    "read_hierarchy_bytes",
]

HIERARCHY_RELATIVE_PATH: Final[str] = "docs/reference/word_hierarchy_rebuild.md"

WITHDRAWN_WITHOUT_A_STATED_REASON: Final[str] = (
    "سقط من النسخة الثانية بلا ذكرِ سببٍ لسقوطه؛ وسقوطٌ بلا سببٍ ليس سحبًا "
    "مُعلَنًا، فلا يُحمَل على أنّه صُحِّح ولا على أنّه بقي"
)

_NO_CORPUS_REACHED_THIS_TREE: Final[str] = (
    "لم تصل مدوّنةٌ مُودَعةٌ مُبصَّمة، ولا `MeasurementRunManifest` يُجمّد صورةَ "
    "التطبيع وإصدارَ قاعدة Unicode، ولا سجلُّ رصدٍ يُطابَق عليه"
)

_REDERIVATION_CONDITION: Final[str] = (
    "إيداعُ بايتات المدوّنة مُبصَّمةً، و`MeasurementRunManifest` لمسار القياس، "
    "وتوقّعٌ مكتوبٌ قبل القياس على منوال `OCP_PREREGISTERED_EXPECTATION`"
)

NOT_ISSUED_BY_THIS_TREE: Final[str] = (
    "مُعرِّفٌ لم تُصدِره هذه الشجرة ولا يوجد فيها: صفرُ تطابقٍ في `src/` و`docs/` "
    "و`tests/`؛ محفوظٌ بحروفه ليُراجَع لا ليُعمَل به"
)

_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "result",
    "outcome_value",
    "verdict",
    "birth",
    "certificate",
    "resolution",
    "resolved",
    "measured_value",
    "proof",
)


class WordHierarchyDepositError(ValueError):
    """رفضٌ عند الإنشاء: عقدةٌ بلا نصّ، أو دعوى بلا سبب، أو تعارضٌ بلا شرطِ حسم."""


class HierarchyLevel(Enum):
    """مستوياتُ الهرمية الستّة كما وردت في النسخة الثانية؛ لا سابعَ لها هنا."""

    LETTER = "المستوى ٠ — الحرف"
    VOWEL = "المستوى ١ — الحركة"
    SYLLABLE = "المستوى ٢ — المقطع"
    WAZN = "المستوى ٣ — الوزن"
    WORD = "المستوى ٤ — الكلمة"
    MABNI = "المستوى ٥ — المبني"


@dataclass(frozen=True, slots=True)
class HierarchyNode:
    """عقدةٌ واحدةٌ من الهرمية: نصُّ دعواها، ومنزلتُها، ومرجعُها في الشجرة.

    `A_STANDING_IS_BOUND_NOT_DECLARED`: من ادّعى لعقدةٍ منزلةَ «مقيسٍ على
    مرمازٍ قائم» لزمه أن يُسمّي الطبقةَ القائمة، وأن تكون في `MEASURED_LAYERS`
    بعينها. فمنزلةٌ تُكتَب بلا ربطٍ تُرقّي المحجوبَ مقيسًا بحرفٍ في سطر.
    """

    node_id: str
    level: HierarchyLevel
    what_the_hierarchy_says: str
    standing: LayerEpistemicStanding
    tree_reference: str
    dictionary_layer: DictionaryLayer | None = None

    def __post_init__(self) -> None:
        for field_name in ("node_id", "what_the_hierarchy_says", "tree_reference"):
            if not str(getattr(self, field_name)).strip():
                raise WordHierarchyDepositError(
                    "عقدةٌ بلا معرّفٍ أو بلا نصِّ دعوًى أو بلا مرجعٍ في الشجرة "
                    "ليست عقدةً مُسجَّلةً بل إحالةً إلى الذاكرة"
                )
        if self.standing is LayerEpistemicStanding.MEASURED_BY_AN_EXISTING_CODEC:
            if self.dictionary_layer is None:
                raise WordHierarchyDepositError(
                    "عقدةٌ منزلتُها «مقيسٌ على مرمازٍ قائم» بلا تسميةِ الطبقة "
                    "القائمة دعوى قياسٍ بلا مقيسٍ عليه"
                )
            if self.dictionary_layer not in MEASURED_LAYERS:
                raise WordHierarchyDepositError(
                    f"الطبقة {self.dictionary_layer.value} محجوبةٌ في "
                    "`word_structure_dictionary`، فلا تُقرأ عقدتُها مقيسةً هنا؛ "
                    "والإيداعُ لا يرفع حجبًا"
                )


@dataclass(frozen=True, slots=True)
class SupersededClaim:
    """دعوى من النسخة الأولى: نصُّها، وما حلّ محلّها، وسببُ سحبها كما ورد."""

    locus: str
    first_version_said: str
    second_version_says: str
    why_it_was_withdrawn: str

    def __post_init__(self) -> None:
        for field_name in (
            "locus",
            "first_version_said",
            "second_version_says",
            "why_it_was_withdrawn",
        ):
            if not str(getattr(self, field_name)).strip():
                raise WordHierarchyDepositError(
                    "دعوى مسحوبةٌ بلا خَلَفٍ أو بلا سببِ سحبٍ تُقرأ بعد جلساتٍ "
                    "كأنّها لم تكن؛ والسحبُ حدثٌ يُسجَّل بنصّه"
                )


@dataclass(frozen=True, slots=True)
class HierarchyNumericClaim:
    """رقمٌ ورد في الوثيقة: نصُّه، وسببُ تعذّر اشتقاقه، وشرطُ اشتقاقه.

    `A_DEPENDENT_FIGURE_IS_NOT_A_SECOND_WITNESS`: رقمٌ يعتمد على رقمٍ آخرَ في
    الوثيقة نفسِها يُسمّيه في `depends_on_figure`، فلا يُقرأ الاثنان شاهدين
    مستقلّين. ورقمٌ وُصِف في الوثيقة مخرجًا لفئةٍ عُرِّفت بالباقي
    (`is_residue_defined`) لا يُقبَل بلا وسمِ تبعيّةٍ يُسمّي ما يقوم عليه.
    """

    figure: str
    locus: str
    claim_text: str
    not_rederivable_because: str
    what_would_make_it_rederivable: str
    depends_on_figure: str | None = None
    is_residue_defined: bool = False

    def __post_init__(self) -> None:
        for field_name in (
            "figure",
            "locus",
            "claim_text",
            "not_rederivable_because",
            "what_would_make_it_rederivable",
        ):
            if not str(getattr(self, field_name)).strip():
                raise WordHierarchyDepositError(
                    "رقمٌ بلا سببِ تعذّرٍ أو بلا شرطِ اشتقاقٍ يُقرأ مقيسًا في "
                    "هذه الشجرة، وهو ما لم يقع"
                )
        if self.depends_on_figure is not None and not self.depends_on_figure.strip():
            raise WordHierarchyDepositError(
                "وسمُ التبعيّة يُسمّي الرقمَ المُعتمَدَ عليه بنصّه؛ ووسمٌ فارغٌ "
                "يُخفي التبعيّةَ ولا يُسجّلها"
            )
        if self.is_residue_defined and self.depends_on_figure is None:
            raise WordHierarchyDepositError(
                "رقمٌ مخرجُه فئةٌ عُرِّفت بالباقي لا يُسجَّل بلا وسمِ تبعيّةٍ "
                "يُسمّي ما يقوم عليه: فئةٌ عُرِّفت بأنّها «ما تبقّى» لا يتبقّى "
                "بعدها شيءٌ بحكم تعريفها، فصفرُها تحصيلُ حاصلٍ لا قياس"
            )


@dataclass(frozen=True, slots=True)
class HierarchyConflict:
    """تعارضٌ مرصود: موضعُه، وما تقوله الشجرة، وما يلزم لحسمه — بلا حسم."""

    locus_in_hierarchy: str
    hierarchy_says: str
    this_tree_says: str
    tree_reference: str
    what_would_resolve_it: str
    standing: ConflictStanding

    def __post_init__(self) -> None:
        for field_name in (
            "locus_in_hierarchy",
            "hierarchy_says",
            "this_tree_says",
            "tree_reference",
            "what_would_resolve_it",
        ):
            if not str(getattr(self, field_name)).strip():
                raise WordHierarchyDepositError(
                    "تعارضٌ بلا موضعٍ أو بلا مرجعٍ أو بلا شرطِ حسمٍ ليس تعارضًا "
                    "مرصودًا بل انطباعًا"
                )


@dataclass(frozen=True, slots=True)
class SubmittedFreezeIdentifier:
    """مُعرِّفُ تجميدٍ وارد: نصُّه، وما يُعلنه، وأنّه غيرُ صادرٍ عن هذه الشجرة."""

    identifier: str
    what_it_declares: str
    not_issued_by_this_tree: str

    def __post_init__(self) -> None:
        for field_name in (
            "identifier",
            "what_it_declares",
            "not_issued_by_this_tree",
        ):
            if not str(getattr(self, field_name)).strip():
                raise WordHierarchyDepositError(
                    "مُعرِّفُ تجميدٍ وارد بلا حقلٍ يقول إنّه غيرُ صادرٍ عن هذه "
                    "الشجرة يُقرأ بعد جلساتٍ تجميدًا فيها؛ والوسمُ لازمٌ لا زينة"
                )


def hierarchy_path(root: Path | None = None) -> Path:
    """مسارُ الوثيقة المُودَعة، مُشتقًّا من جذر المستودع لا مكتوبًا مطلقًا."""

    return (root or repository_root_path()) / HIERARCHY_RELATIVE_PATH


def read_hierarchy_bytes(root: Path | None = None) -> bytes:
    """بايتاتُ الوثيقة كما هي على القرص، بلا تطبيعٍ ولا فكِّ ترميز."""

    path = hierarchy_path(root)
    if not path.is_file():
        raise WordHierarchyDepositError(
            f"الوثيقةُ المُودَعة غيرُ موجودةٍ في الشجرة: {HIERARCHY_RELATIVE_PATH}"
        )
    return path.read_bytes()


def hierarchy_digest(root: Path | None = None) -> str:
    """بصمةُ الوثيقة مُشتقّةً من بايتاتها، لا منسوخةً من حقلٍ في وحدةٍ أخرى."""

    return hashlib.sha256(read_hierarchy_bytes(root)).hexdigest()


@dataclass(frozen=True, slots=True)
class WordHierarchyDeposit:
    """الإيداع: جنسُ المصدر، وتاريخُ الوصول، وموضعُ النصّ، وعددُ النسخ."""

    genus: ProvenanceGenus
    arrival_date: str
    relative_path: str
    deposited_versions: int

    def __post_init__(self) -> None:
        if not self.arrival_date.strip() or not self.relative_path.strip():
            raise WordHierarchyDepositError("إيداعٌ بلا تاريخِ وصولٍ أو بلا موضع")
        if self.deposited_versions != 3:
            raise WordHierarchyDepositError(
                "النصوصُ الثلاثةُ تُودَع معًا؛ وإيداعُ المُصحَّح وحده يمحو أنّ دعاوى سُحبت"
            )

    def digest(self, root: Path | None = None) -> str:
        """بصمةُ الوثيقة الآن، تُقرأ من الملفّ في كلّ نداء."""

        return hierarchy_digest(root)


WORD_HIERARCHY_DEPOSIT: Final[WordHierarchyDeposit] = WordHierarchyDeposit(
    genus=ProvenanceGenus.PROSE_FROM_ANOTHER_CONVERSATION,
    arrival_date="2026-09-15",
    relative_path=HIERARCHY_RELATIVE_PATH,
    deposited_versions=3,
)


SUBMITTED_FREEZE_IDENTIFIERS: Final[tuple[SubmittedFreezeIdentifier, ...]] = (
    SubmittedFreezeIdentifier(
        identifier="SPEECH-PARTS-AND-COMPOSITION-AR-1",
        what_it_declares=(
            "تجميدٌ يُعلن إغلاقَ التركيب النحويّ ١٠٠٪، وصفرَ فجوةٍ بين الكلمة "
            "المنطقيّة والفراغيّة، وغيابَ التركيب المزجيّ شاهدًا في المصحف"
        ),
        not_issued_by_this_tree=NOT_ISSUED_BY_THIS_TREE,
    ),
    SubmittedFreezeIdentifier(
        identifier="WAQF-SEL-MARKER-PROXY-AR-1",
        what_it_declares=(
            "أداةُ قياسٍ يُقترَح بها الوقفُ التامُّ كاشفًا لحدّ الإسناد، "
            "برقمَي ٥٦٪ و٢٣٪، ومُعلَنٌ في نصّها أنّ الربطَ لم يُختبَر تكامليًّا"
        ),
        not_issued_by_this_tree=NOT_ISSUED_BY_THIS_TREE,
    ),
)


WORD_HIERARCHY_NODES: Final[tuple[HierarchyNode, ...]] = (
    HierarchyNode(
        node_id="الحرف_وحالتُه",
        level=HierarchyLevel.LETTER,
        what_the_hierarchy_says="الحرفُ وحدةٌ ذرّيّةٌ تحمل حالةً، صامتةً أو غيرَ صامتة",
        standing=LayerEpistemicStanding.MEASURED_BY_AN_EXISTING_CODEC,
        tree_reference=(
            "`DictionaryLayer.LETTERS` مقيسةٌ على `CarrierStateCodec`؛ "
            "وهي الطبقةُ الوحيدةُ من هذا المستوى التي تُخرِج قيمًا"
        ),
        dictionary_layer=DictionaryLayer.LETTERS,
    ),
    HierarchyNode(
        node_id="المخرج_ثلاثَ_عشرةَ_فئة",
        level=HierarchyLevel.LETTER,
        what_the_hierarchy_says="مخرجٌ في ١٣ فئةً، شجرةَ شفة/أسنان/لسان/حلق",
        standing=LayerEpistemicStanding.IMPORTED_BEHIND_AN_OPEN_BARRIER,
        tree_reference=(
            "`DictionaryLayer.PHONETIC_FEATURES` محجوبة، و`CLASSICAL_MAKHARIJ` "
            "مجمَّدٌ على ستّةَ عشرَ مخرجًا مرقَّمًا"
        ),
    ),
    HierarchyNode(
        node_id="الصفة_اثنا_عشرَ_محورًا",
        level=HierarchyLevel.LETTER,
        what_the_hierarchy_says=(
            "صفةٌ في ١٢ محورًا شجريًّا، وإطباقٌ ⊆ استعلاء تحليليًّا بتعريفٍ معلَن"
        ),
        standing=LayerEpistemicStanding.IMPORTED_BEHIND_AN_OPEN_BARRIER,
        tree_reference=(
            "`gflk_feature_table_import_barrier` و"
            "`AN_IMPORTED_TABLE_IS_NOT_A_CLAIM_OF_THIS_TREE`"
        ),
    ),
    HierarchyNode(
        node_id="همزة_الوصل",
        level=HierarchyLevel.LETTER,
        what_the_hierarchy_says=(
            "همزةُ وصلٍ محايدةٌ معلوماتيًّا، وقد تكون ضرورةً بنيويّةً في «استفعل»"
        ),
        standing=LayerEpistemicStanding.UNDECIDABLE_FROM_THE_WRITTEN_MARKS,
        tree_reference=(
            "`HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS` في "
            "`ibtida_wasl_waqf_registration`"
        ),
    ),
    HierarchyNode(
        node_id="حامل_التنوين",
        level=HierarchyLevel.LETTER,
        what_the_hierarchy_says="حاملُ التنوين وحده يحمل معلومةً حقيقيّة",
        standing=LayerEpistemicStanding.MEASURED_BY_AN_EXISTING_CODEC,
        tree_reference=(
            "`DictionaryLayer.TANWEEN_ANALYSIS` تُقرأ دورًا على الوحدة القائمة "
            "من `tanwin` و`tanwin_alif_seat` و`seat`"
        ),
        dictionary_layer=DictionaryLayer.TANWEEN_ANALYSIS,
    ),
    HierarchyNode(
        node_id="علّة_الحرف_وضعًا_أو_وظيفة",
        level=HierarchyLevel.LETTER,
        what_the_hierarchy_says=(
            "علّةُ الحرف دلالةٌ وضعيّةٌ في الجذر أو وظيفةٌ في الأداة، بتردّدٍ ×٤٣-١٦٠"
        ),
        standing=LayerEpistemicStanding.HYPOTHESIS_WITH_A_DECLARED_DEFECT,
        tree_reference=(
            "`wad_naql` و`DISTRIBUTIONAL_TRACE_IS_NOT_WAD_PATH`: الوضعُ لا "
            "يُشتَقّ من تردّد"
        ),
    ),
    HierarchyNode(
        node_id="الحركة_العادية",
        level=HierarchyLevel.VOWEL,
        what_the_hierarchy_says="فتحةٌ وضمّةٌ وكسرةٌ وسكون",
        standing=LayerEpistemicStanding.MEASURED_BY_AN_EXISTING_CODEC,
        tree_reference=(
            "`CarrierState` المغلقةُ بسبعة، وفيها `SUKUN_EXPLICIT` و`SUKUN_IMPLICIT`"
        ),
        dictionary_layer=DictionaryLayer.LETTERS,
    ),
    HierarchyNode(
        node_id="قيد_التنوين_آخر_الكلمة",
        level=HierarchyLevel.VOWEL,
        what_the_hierarchy_says=(
            "التنوينُ آخرَ الكلمة حصرًا، بإقصاءٍ تامٍّ مع «أل» ومع الفعل"
        ),
        standing=LayerEpistemicStanding.UNDECIDABLE_FROM_THE_WRITTEN_MARKS,
        tree_reference=(
            "حقلُ التعذّر `tanween_position_unread`: ما لم يُقرأ موضعُه لا "
            "يُحمَل على «آخرِ الكلمة» بالافتراض؛ و«أل» غيرُ مُميَّزةٍ أصلًا"
        ),
    ),
    HierarchyNode(
        node_id="الشدّة_ومصدرها",
        level=HierarchyLevel.VOWEL,
        what_the_hierarchy_says=(
            "الشدّةُ تضعيفٌ جذريٌّ أو إدغامٌ شمسيّ، والإدغامُ الشمسيُّ وجودُ "
            "اللام المُدغَمة بعينه لا ظاهرةٌ مستقلّة"
        ),
        standing=LayerEpistemicStanding.UNDECIDABLE_FROM_THE_WRITTEN_MARKS,
        tree_reference=(
            "`THE_SHADDA_SOURCE_IS_NOT_READ_FROM_THE_MARKS` في "
            "`word_structure_dictionary`: الدورُ مرصودٌ ومصدرُه حقلُ تعذّر"
        ),
    ),
    HierarchyNode(
        node_id="المقطع_بالوظيفة",
        level=HierarchyLevel.SYLLABLE,
        what_the_hierarchy_says="المقطعُ جذريٌّ أو صرفيٌّ أو نحويّ، والوزنُ خاصّةٌ عرضيّة",
        standing=LayerEpistemicStanding.IMPORTED_BEHIND_AN_OPEN_BARRIER,
        tree_reference=(
            "`DictionaryLayer.SYLLABLES_AND_WAZN` محجوبةٌ بحقلِ تعذّر؛ "
            "والتصنيفُ بالوظيفة لا يرفع الحجب عن التصنيف بالموقع"
        ),
    ),
    HierarchyNode(
        node_id="اندماج_وزن_X_الحدّي",
        level=HierarchyLevel.SYLLABLE,
        what_the_hierarchy_says=(
            "المقطعُ الصرفيُّ المركَّب في «اسْتَفْعَلَ» قد يندمج حدّيًّا مع فاء "
            "الفعل الساكنة فيكسر القصَّ النظيف"
        ),
        standing=LayerEpistemicStanding.HYPOTHESIS_WITH_A_DECLARED_DEFECT,
        tree_reference=(
            "معلَنُ العطب في نصّه؛ وسحبُ العموم عند مثالٍ مضادٍّ واحد يوافق "
            "`ONE_COUNTER_INSTANCE_DECIDES` في `lexical_path_census`"
        ),
    ),
    HierarchyNode(
        node_id="ثبات_مبنيات_الوزن",
        level=HierarchyLevel.WAZN,
        what_the_hierarchy_says=(
            "مبنياتُ الوزن ثابتةٌ ١٠٠٪، والمقطعُ النحويُّ نقطةُ التأثّر الحصريّة"
        ),
        standing=LayerEpistemicStanding.IMPORTED_BEHIND_AN_OPEN_BARRIER,
        tree_reference="`DictionaryLayer.SYLLABLES_AND_WAZN` محجوبة، فلا مقطعَ يُخرَج",
    ),
    HierarchyNode(
        node_id="الوصل_وحده_علاقة",
        level=HierarchyLevel.WAZN,
        what_the_hierarchy_says=(
            "الوصلُ وحده علاقةٌ حقيقيّة، والابتداءُ والوقفُ خاصّتان حديّتان"
        ),
        standing=LayerEpistemicStanding.UNDECIDABLE_FROM_THE_WRITTEN_MARKS,
        tree_reference=(
            "`ibtida_wasl_waqf_registration`: الوقفُ غيرُ مقروءٍ من العلامات، "
            "والعدُّ على السكون المكتوب وحده"
        ),
    ),
    HierarchyNode(
        node_id="مجرد_أو_مزيد_مسحوب",
        level=HierarchyLevel.WAZN,
        what_the_hierarchy_says=(
            "مجرد/مزيد معيارٌ سطحيٌّ معطوب، **مسحوبٌ** من الخواصّ الموثوقة"
        ),
        standing=LayerEpistemicStanding.HYPOTHESIS_WITH_A_DECLARED_DEFECT,
        tree_reference=(
            "`DictionaryLayer.JARAD_ANALYSIS` منزلتُها `فرضٌ مُعلَنُ العطب` "
            "قبلَ هذه الوثيقة؛ فهذا توافقٌ يُسجَّل لا تعارض"
        ),
    ),
    HierarchyNode(
        node_id="اسم_فعل_حرف",
        level=HierarchyLevel.WORD,
        what_the_hierarchy_says="الكلمةُ اسمٌ أو فعلٌ أو حرفُ معنًى، لا رابعَ",
        standing=LayerEpistemicStanding.HYPOTHESIS_WITH_A_DECLARED_DEFECT,
        tree_reference=(
            "`word_class_formal` يُجمّد `card(Ω)=3` بسؤالين وأربعةِ شهود؛ "
            "فالعددُ موافقٌ، والخلافُ في علاماتِ التمييز لا في المفردة"
        ),
    ),
    HierarchyNode(
        node_id="أل_والتنوين_علامتا_الاسم",
        level=HierarchyLevel.WORD,
        what_the_hierarchy_says="الاسمُ يقبل «أل» أو تنوينًا تبادليًّا، والفعلُ يرفضهما",
        standing=LayerEpistemicStanding.UNDECIDABLE_FROM_THE_WRITTEN_MARKS,
        tree_reference=(
            "`DictionaryLayer.AL_ANALYSIS` محجوبةٌ بحقلِ "
            "`al_undecidable_from_marks`: ألفُ «الْحَمْدُ» لا تحمل علامةً أصلًا"
        ),
    ),
    HierarchyNode(
        node_id="المبني_نوعان",
        level=HierarchyLevel.MABNI,
        what_the_hierarchy_says=(
            "المبنيُّ نوعان: بقاعدةٍ صوتيّةٍ منتجة (أل التعريف)، وبحفظٍ معجميٍّ "
            "مغلق (أل الموصول: ٣ صيغٍ فقط، حالتُها ثابتةٌ بلا قاعدة)"
        ),
        standing=LayerEpistemicStanding.HYPOTHESIS_WITH_A_DECLARED_DEFECT,
        tree_reference=(
            "`MabniIsNotAnUnchangedSurfaceForm` و"
            "`EnumeratedExamplesAreNotAnExhaustiveCriterion` في "
            "`sentence_card_preregistration`، ورفضُ `MAWSUL_WORDS` بلا مصدرٍ وبصمة"
        ),
    ),
)


SUPERSEDED_CLAIMS: Final[tuple[SupersededClaim, ...]] = (
    SupersededClaim(
        locus="المستوى ٠ — الصفة",
        first_version_said="«إطباقٌ مشروطٌ باستعلاء» مطلقًا، بلا تعريفٍ مذكور",
        second_version_says="«إطباق ⊆ استعلاء **تحليليًّا بتعريفٍ معلَن** لا مطلقًا»",
        why_it_was_withdrawn=(
            "صارت الدعوى مشروطةً بتعريفها فلا تُقرأ اكتشافًا عن العربية. ولم "
            "يصل **نصُّ** التعريف المُعلَن، فالإعلانُ قائمٌ والمُعلَنُ غائب"
        ),
    ),
    SupersededClaim(
        locus="المستوى ٣ — مجرد/مزيد",
        first_version_said="«⚠ معيار سطحي» مع إبقائه عضوًا في بنية الوزن",
        second_version_says="«**مسحوب** من الخواصّ الموثوقة»",
        why_it_was_withdrawn=(
            "المعيارُ مُقِرٌّ في نصّه بأنّه لا يُميّز زائدًا مُقحَمًا من أصليٍّ "
            "يصادف كونَه من سألتمونيها؛ وهو منزلةُ `JARAD_ANALYSIS` القائمة"
        ),
    ),
    SupersededClaim(
        locus="المستوى ٣ — الزيادة الصرفية",
        first_version_said="«صفر انحراف عن التنبّؤ (6/6 أمثلة)» على الأوزان كلّها",
        second_version_says=("«2/2 لـV/VI؛ **ينكسر بنيويًّا** لـX عند الاندماج الحدّي»"),
        why_it_was_withdrawn=(
            "ظهر مثالٌ مضادٌّ واحد — اندماجُ مقطع «اسْتَ» مع فاء الفعل الساكنة — "
            "فسُحِب العمومُ ولم يُرقَّع؛ وواحدةٌ تحسم"
        ),
    ),
    SupersededClaim(
        locus="المستوى ٠ — همزة الوصل",
        first_version_said="«تُبنى بصورة العزلة: أَ[ل]، لا تُسقَط إلا وصلًا»",
        second_version_says=(
            "«محايدةٌ معلوماتيًّا (π لا يتغيّر) لكن قد تكون ضرورةً بنيويّة»"
        ),
        why_it_was_withdrawn=(
            "فُصِل الحيادُ المعلوماتيُّ عن الضرورة البنيويّة فلم يعودا دعوًى "
            "واحدة. والصيغتان معًا تستلزمان تمييزَ همزة الوصل، وهو متعذّرٌ من "
            "العلامات، فلم يتغيّر الحجب"
        ),
    ),
    SupersededClaim(
        locus="المستوى ٢ — معيار تصنيف المقطع",
        first_version_said="المقطعُ مُصنَّفٌ بالموقع وبالوزن العروضيّ وحدهما",
        second_version_says="المقطعُ مُصنَّفٌ **بالوظيفة**: جذريٌّ/صرفيٌّ/نحويّ",
        why_it_was_withdrawn=(
            "تبديلُ معيارٍ لا ترقيةُ منزلة؛ والطبقةُ محجوبةٌ قبل التصنيفين "
            "وبعدهما، فلم يُخرِج التبديلُ مقطعًا واحدًا قيمةً"
        ),
    ),
    SupersededClaim(
        locus="المستوى ١ و٣ و٤ — الأرقام الستّة",
        first_version_said=(
            "٨٬٧٥٦ و٧٨٬٢١٥ و٤٬٨٤٢ و١٬٥٧٦ و٥٣٫٧١٪ و٩٥٫٦٧٪ مقرونةً بدعاواها"
        ),
        second_version_says="الدعاوى باقيةٌ والأرقامُ ساقطة",
        why_it_was_withdrawn=WITHDRAWN_WITHOUT_A_STATED_REASON,
    ),
    SupersededClaim(
        locus="الفجوة الجذرية — ٤٫٧٦٪ إلى صفر",
        first_version_said=(
            "٤٫٧٦٪ من التوكِنات الفراغيّة تحوي أكثرَ من كلمةٍ منطقيّةٍ واحدة، "
            "في النسختين الأولى والثانية معًا بنصٍّ واحد"
        ),
        second_version_says=(
            "«الفجوة صفر تمامًا — تصحيح نهائي يُلغي كلًّا من ٤٫٧٦٪ و١٪ "
            "المذكورتين سابقًا» (§٢-ب)؛ و«١٪» لم تصل هذه الشجرةَ قطّ"
        ),
        why_it_was_withdrawn=(
            "سببٌ مذكورٌ هذه المرّة، لا `WITHDRAWN_WITHOUT_A_STATED_REASON`: "
            "«تفسير كل المرشَّحين بإدغام عابر» بفئةٍ ثالثةٍ مُعرَّفةٍ بالباقي. "
            "والسببُ مُسجَّلٌ كما ورد، وتقويمُه في التعارض لا هنا"
        ),
    ),
)


WORD_HIERARCHY_NUMERIC_CLAIMS: Final[tuple[HierarchyNumericClaim, ...]] = (
    HierarchyNumericClaim(
        figure="35.7%",
        locus="المستوى ٢ — المقطع النحويّ",
        claim_text="المقطعُ النحويُّ وظيفيٌّ في ٣٥٫٧٪ من الجذوع، وهي المعرَبة",
        not_rederivable_because=_NO_CORPUS_REACHED_THIS_TREE,
        what_would_make_it_rederivable=(
            f"{_REDERIVATION_CONDITION}. وللشجرة منوالٌ قائم: `irab_case_readout` "
            "قاس على ٤٢٦٥ موضعًا من مدوّنةٍ خارجيّةٍ مُوسَّمة"
        ),
    ),
    HierarchyNumericClaim(
        figure="4.46%",
        locus="المستوى ٤ — المضارع",
        claim_text="تلوّثُ نمط «يَفْعَلُ» ٤٫٤٦٪",
        not_rederivable_because=(
            f"{_NO_CORPUS_REACHED_THIS_TREE}. ولم يُذكَر أهو على قسمٍ محجوبٍ أم "
            "على الكلّ، والفرقُ بينهما مقدارُ الملاءمة"
        ),
        what_would_make_it_rederivable=(
            f"{_REDERIVATION_CONDITION}؛ وإعلانُ الرقمين معًا — على القسم "
            "المحجوب وعلى الكلّ — على منوال `TUNED_ON_DEV_REPORTED_ON_HELD_OUT`"
        ),
    ),
    HierarchyNumericClaim(
        figure="4.76%",
        locus="الفجوة الجذرية",
        claim_text="٤٫٧٦٪ من التوكِنات الفراغيّة تحوي أكثرَ من كلمةٍ منطقيّةٍ واحدة",
        not_rederivable_because=(
            f"{_NO_CORPUS_REACHED_THIS_TREE}. وحدُّ الكلمة المنطقيّة نفسُه غيرُ "
            "مُعرَّفٍ في الشجرة بمرمازٍ يُقاس عليه"
        ),
        what_would_make_it_rederivable=(
            f"{_REDERIVATION_CONDITION}؛ وتعريفٌ مُجمَّدٌ لحدّ الكلمة المنطقيّة "
            "قبل العدّ، فالعدُّ تابعٌ للحدّ لا كاشفٌ عنه"
        ),
    ),
    HierarchyNumericClaim(
        figure="2/2",
        locus="المستوى ٢ و٣ — أوزان V/VI",
        claim_text="حذفٌ عكسيٌّ بمطابقةٍ تامّة في مثالين من مثالين",
        not_rederivable_because=(
            f"{_NO_CORPUS_REACHED_THIS_TREE}. ولم يُسمَّ المثالان، ومثالٌ بلا "
            "اسمٍ لا يُعاد عليه القياس"
        ),
        what_would_make_it_rederivable=(
            "تسميةُ المثالين بأعيانهما مع موضعهما في مدوّنةٍ مُبصَّمة؛ و«٢/٢» "
            "عيّنةٌ لا معدّل، فلا تُقرأ نسبةً على أيّ حال"
        ),
    ),
    HierarchyNumericClaim(
        figure="3/3",
        locus="المستوى ٢ — القالب العروضيّ للمقطع النحويّ",
        claim_text="صفرُ انحرافٍ عن قالب CV عبر الرفع والنصب والجرّ، ثلاثةٌ من ثلاثة",
        not_rederivable_because=(
            f"{_NO_CORPUS_REACHED_THIS_TREE}. والمقطعُ نفسُه طبقةٌ محجوبةٌ لا "
            "تُخرِج قيمةً، فلا شيءَ يُعَدّ عليه"
        ),
        what_would_make_it_rederivable=(
            f"{_REDERIVATION_CONDITION}؛ ورفعُ حجبِ `SYLLABLES_AND_WAZN` بشرطِ "
            "دخولها المكتوب، فقبلَه لا مقطعَ يُقاس قالبُه"
        ),
    ),
    HierarchyNumericClaim(
        figure="20/20",
        locus="المستوى ٢ و٤ — الكلمة الوظيفيّة أحاديّة المقطع",
        claim_text="عشرون من عشرين كلمةً وظيفيّةً أحاديّةَ المقطع ثقيلةٌ حتمًا",
        not_rederivable_because=(
            f"{_NO_CORPUS_REACHED_THIS_TREE}. ولم تُسمَّ العشرون، والقائمةُ "
            "المغلقةُ دعوى حصرٍ تحتاج نصَّها لا تعدادَ أمثلة"
        ),
        what_would_make_it_rederivable=(
            "تسميةُ العشرين بأعيانها، ونصٌّ مصدريٌّ منسوبٌ للقائمة المغلقة؛ "
            "و«٢٠/٢٠» على قائمةٍ اختِيرت بعد العدّ ملاءمةٌ لا تنبّؤ"
        ),
    ),
    HierarchyNumericClaim(
        figure="×43-160",
        locus="المستوى ٠ — علّةُ الحرف",
        claim_text="ترددُ الأداة النوعيُّ أضعافُ تردّد الجذر بمقدار ×٤٣ إلى ×١٦٠",
        not_rederivable_because=(
            f"{_NO_CORPUS_REACHED_THIS_TREE}. ولم يُذكَر مقامُ النسبة: "
            "أتردّدُ نوعٍ أم تردّدُ حدث"
        ),
        what_would_make_it_rederivable=(
            f"{_REDERIVATION_CONDITION}؛ ومع ذلك يبقى الرقمُ لا يُثبِت الوظيفة، "
            "فـ`DISTRIBUTIONAL_TRACE_IS_NOT_WAD_PATH`: الوضعُ لا يُشتَقّ من تردّد"
        ),
    ),
    HierarchyNumericClaim(
        figure="صفر خرق — التنوين آخرَ الكلمة",
        locus="المستوى ١ — التنوين",
        claim_text="التنوينُ آخرَ الكلمة حصرًا، بصفر خرق",
        not_rederivable_because=(
            f"{_NO_CORPUS_REACHED_THIS_TREE}. وموضعُ التنوين غيرُ مقروءٍ من "
            "الحقول القائمة أصلًا (`tanween_position_unread`)"
        ),
        what_would_make_it_rederivable=(
            f"{_REDERIVATION_CONDITION}؛ و«صفر خرق» دعوى عمومٍ أثقلُ من النسبة "
            "لا أخفّ، إذ يكفي لنقضها موضعٌ واحد"
        ),
    ),
    HierarchyNumericClaim(
        figure="صفر تقاطع — أل والتنوين",
        locus="المستوى ١ و٤ — إقصاءُ «أل» والتنوين",
        claim_text="إقصاءٌ تامٌّ بين «أل» والتنوين، مؤكَّدٌ ثنائيَّ الاتجاه مع الفعل",
        not_rederivable_because=(
            f"{_NO_CORPUS_REACHED_THIS_TREE}. و«أل» غيرُ مُميَّزةٍ من العلامات "
            "المكتوبة، فأحدُ طرفَي التقاطع غيرُ مقيس"
        ),
        what_would_make_it_rederivable=(
            "مُدخَلٌ معجميٌّ أو صرفيٌّ منسوبٌ ومُبصَّمٌ يُميّز همزةَ الوصل، وهو "
            "شرطُ دخول `AL_ANALYSIS` المكتوبُ قبل هذه الوثيقة"
        ),
    ),
    HierarchyNumericClaim(
        figure="صفر خرق — الشدّة والإدغام الشمسيّ",
        locus="المستوى ١ — الشدّة",
        claim_text="الإدغامُ الشمسيُّ وجودُ اللام المُدغَمة بعينه، بصفر خرق",
        not_rederivable_because=(
            f"{_NO_CORPUS_REACHED_THIS_TREE}. ولامُ «أل» غيرُ مُميَّزةٍ في "
            "العلامات، وتخرج من المرماز `SUKUN_IMPLICIT` كأيِّ حرفٍ بلا علامة"
        ),
        what_would_make_it_rederivable=(
            "تمييزُ لامِ «أل» بمُدخَلٍ منسوبٍ ومُبصَّم؛ فقبلَه يبقى دورُ الشدّة "
            "مرصودًا ومصدرُه في حقلِ تعذّرٍ لا يُنسَب إلى أحد الاحتمالين"
        ),
    ),
    HierarchyNumericClaim(
        figure="ثابتة 100%",
        locus="المستوى ٣ — مبنيات الوزن",
        claim_text="مبنياتُ الوزن ثابتةٌ ١٠٠٪ لا يمسّها وصلٌ ولا وقف",
        not_rederivable_because=(
            f"{_NO_CORPUS_REACHED_THIS_TREE}. وللشجرة سابقةٌ في «١٠٠٪» بعينها: "
            "أُعيد اشتقاقُها في `gflk_codec_revision_audit` فخرجت ٩٩٫٩٩٢٢٥١٪"
        ),
        what_would_make_it_rederivable=(
            f"{_REDERIVATION_CONDITION}؛ ورفعُ حجبِ `SYLLABLES_AND_WAZN`، فلا "
            "يُقاس ثباتُ مبنًى لم يُخرَج قيمةً"
        ),
    ),
    HierarchyNumericClaim(
        figure="3 صيغ — أل الموصول",
        locus="المستوى ٥ — المبنيّ بحفظٍ معجميٍّ مغلق",
        claim_text="أل الموصول ثلاثُ صيغٍ فقط، حالتُها ثابتةٌ بلا قاعدة",
        not_rederivable_because=(
            "دعوى حصرٍ بالتعداد، وقد رُفض جنسُها قبلَ هذه الوثيقة في "
            "`EnumeratedExamplesAreNotAnExhaustiveCriterion`"
        ),
        what_would_make_it_rederivable=(
            "نصٌّ مصدريٌّ منسوبٌ ومُبصَّمٌ يُثبت الحصر؛ فالحصرُ دعوى نصٍّ لا "
            "استقراءُ أمثلة، ولا يُغني عنه تعدادُ ما وقع"
        ),
    ),
    HierarchyNumericClaim(
        figure="98.9%",
        locus="§٢-ب — فئةُ الإدغام الأولى",
        claim_text="نونٌ ساكنةٌ/تنوينٌ + يرملون تُفسِّر ٩٨٫٩٪ من «الساكن اليتيم»",
        not_rederivable_because=(
            f"{_NO_CORPUS_REACHED_THIS_TREE}. و`MEASURED_SAKIN_CLASH_SOURCES` "
            "**فارغة**، فلا نسبةَ تُحسَب على نصٍّ لم يصل"
        ),
        what_would_make_it_rederivable=(
            f"{_REDERIVATION_CONDITION}؛ ويُشغَّل عليها المسحُ القائم في "
            "`encoding/sakin_adjacency`، فالمسحُ موجودٌ والمدوّنةُ هي الناقصة"
        ),
    ),
    HierarchyNumericClaim(
        figure="مُغلَق 100% — التركيب النحويّ",
        locus="§٢-ب — إغلاق التركيب النحويّ",
        claim_text=(
            "ثلاثُ فئاتِ إدغامٍ متكاملةٍ تُفسِّر كلَّ «ساكن يتيم» بلا استثناءٍ واحدٍ متبقٍّ"
        ),
        not_rederivable_because=(
            f"{_NO_CORPUS_REACHED_THIS_TREE}. والفئةُ الثالثةُ موصوفةٌ في نصّها "
            "بأنّها «تُفسِّر كلَّ ما تبقّى»، فالإغلاقُ محمولٌ بتعريفها. "
            "وللشجرة سابقةٌ في «١٠٠٪»: أُعيد اشتقاقُها في "
            "`gflk_codec_revision_audit` فخرجت ٩٩٫٩٩٢٢٥١٪"
        ),
        what_would_make_it_rederivable=(
            f"{_REDERIVATION_CONDITION}؛ و**نصُّ شرطِ الفئة الثالثة** مكتوبًا "
            "قبل الفحص لا بعده، فيصير وصفُها تنبّؤًا يُنقَض بموضع"
        ),
        depends_on_figure="98.9%",
        is_residue_defined=True,
    ),
    HierarchyNumericClaim(
        figure="صفر تمامًا — الفجوة بين الكلمة المنطقيّة والفراغيّة",
        locus="§٢-ب — الفجوة",
        claim_text="الفجوةُ صفرٌ تمامًا، تصحيحًا نهائيًّا يُلغي ٤٫٧٦٪ و١٪",
        not_rederivable_because=(
            f"{_NO_CORPUS_REACHED_THIS_TREE}. والصفرُ مخرجُ إغلاقِ §١ نفسِه لا "
            "قياسٌ مستقلٌّ: أُزيل المرشَّحون بالفئة الثالثة المُعرَّفة بالباقي"
        ),
        what_would_make_it_rederivable=(
            f"{_REDERIVATION_CONDITION}؛ وتعريفٌ مُجمَّدٌ لحدّ الكلمة المنطقيّة "
            "قبل العدّ، فالعدُّ تابعٌ للحدّ لا كاشفٌ عنه"
        ),
        depends_on_figure="مُغلَق 100% — التركيب النحويّ",
        is_residue_defined=True,
    ),
    HierarchyNumericClaim(
        figure="صفر حالة — التركيب المزجيّ",
        locus="§٢-ب — التركيب المزجيّ",
        claim_text=(
            "صفرُ حالةٍ حقيقيّةٍ في المصحف بعد تفسير كلّ المرشَّحين بإدغامٍ "
            "عابر، نتيجةً سلبيّةً مُقيَّدةً بالمصحف لا نفيًا في العربية عمومًا"
        ),
        not_rederivable_because=(
            f"{_NO_CORPUS_REACHED_THIS_TREE}. والاستبعادُ جرى بالفئة الثالثة "
            "نفسِها، فليست هذه نتيجةً ثانيةً بل قراءةٌ ثانيةٌ للأولى"
        ),
        what_would_make_it_rederivable=(
            f"{_REDERIVATION_CONDITION}؛ وتقييدُ النتيجة بمصدرها المُبصَّم "
            "محمودٌ ومُسجَّلٌ: نتيجةٌ سلبيّةٌ مُقيَّدةٌ أصدقُ من موجبةٍ مُطلَقة"
        ),
        depends_on_figure="مُغلَق 100% — التركيب النحويّ",
        is_residue_defined=True,
    ),
    HierarchyNumericClaim(
        figure="56%",
        locus="§٢-ب — وكيلُ الوقف كاشفًا لحدّ الإسناد",
        claim_text="الرقمُ الأوّل من رقمَي `WAQF-SEL-MARKER-PROXY-AR-1`",
        not_rederivable_because=(
            f"{_NO_CORPUS_REACHED_THIS_TREE}. وعلامةُ الوقف وحدةُ `PASSTHROUGH` "
            "لا تُقرأ سكونًا، فسكونُ الوقف غيرُ مُميَّزٍ من سكون الوصل أصلًا"
        ),
        what_would_make_it_rederivable=(
            f"{_REDERIVATION_CONDITION}؛ وقسمةُ المدوّنة بقاعدةٍ لا علاقةَ لها "
            "بالجواب على منوال `TUNED_ON_DEV_REPORTED_ON_HELD_OUT`"
        ),
    ),
    HierarchyNumericClaim(
        figure="23%",
        locus="§٢-ب — وكيلُ الوقف كاشفًا لحدّ الإسناد",
        claim_text="الرقمُ الثاني من رقمَي `WAQF-SEL-MARKER-PROXY-AR-1`",
        not_rederivable_because=(
            f"{_NO_CORPUS_REACHED_THIS_TREE}. ولم يُذكَر مقامُ الرقمين ولا "
            "أيُّهما على قسمٍ محجوب، والفرقُ بينهما غيرُ مُفسَّرٍ في النصّ"
        ),
        what_would_make_it_rederivable=(
            f"{_REDERIVATION_CONDITION}؛ وتسميةُ ما يعدُّه كلٌّ من الرقمين، "
            "فرقمان بلا مقامٍ لا يُقرآن دقّةً ولا تغطية"
        ),
        depends_on_figure="56%",
    ),
)


WORD_HIERARCHY_CONFLICTS: Final[tuple[HierarchyConflict, ...]] = (
    HierarchyConflict(
        locus_in_hierarchy="§٢ المستوى ٠ — همزة الوصل",
        hierarchy_says=(
            "همزةُ وصلٍ محايدةٌ معلوماتيًّا وقد تكون ضرورةً بنيويّة، وحذفُها من "
            "«استفعل» يخرق الابتداء"
        ),
        this_tree_says=(
            "همزةُ الوصل غيرُ قابلةٍ للتمييز من العلامات المكتوبة: ألفُ "
            "«الْحَمْدُ» لا تحمل علامةً أصلًا، فمنزلتُها `لا_حالة_مكتوبة`"
        ),
        tree_reference=(
            "`HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS` في "
            "`ibtida_wasl_waqf_registration`، و`AL_ANALYSIS` المحجوبة"
        ),
        what_would_resolve_it=(
            "مُدخَلٌ معجميٌّ أو صرفيٌّ منسوبٌ ومُبصَّمٌ يُميّز همزةَ الوصل؛ وما "
            "دونه فالتصنيفُ موضعيٌّ لا قراءةٌ للعلامات"
        ),
        standing=ConflictStanding.BLOCKS_IMPORT_UNTIL_RESOLVED,
    ),
    HierarchyConflict(
        locus_in_hierarchy="§٢ المستوى ١ — الشدّة والإدغام الشمسيّ",
        hierarchy_says=(
            "الإدغامُ الشمسيُّ = وجودُ اللام المُدغَمة بعينه، **لا ظاهرةٌ "
            "مستقلّة**، بصفر خرق"
        ),
        this_tree_says=(
            "مصدرُ التضعيف لا يُقرأ من العلامات: لامُ «أل» غيرُ مُميَّزةٍ فيها، "
            "فيبقى الدورُ مرصودًا والمصدرُ في حقلِ تعذّرٍ لا يُنسَب"
        ),
        tree_reference=(
            "`THE_SHADDA_SOURCE_IS_NOT_READ_FROM_THE_MARKS` في "
            "`word_structure_dictionary`"
        ),
        what_would_resolve_it=(
            "تمييزُ لامِ «أل» بمُدخَلٍ منسوبٍ ومُبصَّم. والنسخةُ الثانية "
            "**شدّدت** الدعوى بنفي استقلال الظاهرة، فزادت حاجتَها إلى التمييز "
            "ولم تُقلّلها"
        ),
        standing=ConflictStanding.BLOCKS_IMPORT_UNTIL_RESOLVED,
    ),
    HierarchyConflict(
        locus_in_hierarchy="§٢ المستوى ٢ — المقطع كلُّه",
        hierarchy_says=(
            "المقطعُ مُصنَّفٌ بالوظيفة إلى جذريٍّ وصرفيٍّ ونحويّ، وله وزنٌ " "خفيفٌ أو ثقيلٌ أو أثقل"
        ),
        this_tree_says=(
            "طبقةُ المقطع والوزن **محجوبةٌ** تُخرِج حقلَ تعذّرٍ مُسمًّى لا قيمة؛ "
            "ولا يصير المحجوبُ مقيسًا بتبديل معيار تصنيفه"
        ),
        tree_reference=(
            "`DictionaryLayer.SYLLABLES_AND_WAZN` في `WITHHELD_LAYERS`، "
            "وشرطُ دخولها في `DICTIONARY_LAYER_REGISTRATIONS`"
        ),
        what_would_resolve_it=(
            "استيفاءُ شرطِ دخول الطبقة المكتوبِ قبل هذه الوثيقة؛ ولا يُرفَع "
            "الحجبُ بحذف سطرٍ من وحدةٍ فوقه"
        ),
        standing=ConflictStanding.BLOCKS_IMPORT_UNTIL_RESOLVED,
    ),
    HierarchyConflict(
        locus_in_hierarchy="§٢ المستوى ٠ — المخرج ثلاثَ عشرةَ فئة",
        hierarchy_says="المخرجُ ثلاثَ عشرةَ فئةً في شجرةِ شفة/أسنان/لسان/حلق",
        this_tree_says=(
            "ثمانيةٌ وعشرون صامتًا في **ستّةَ عشرَ** مخرجًا مرقَّمًا، والخيشومُ "
            "سابعَ عشرَ خارجَ الترقيم قصدًا؛ وقياسُ التنافر جرى على تسعةِ عناقيد"
        ),
        tree_reference=(
            "`classical_makharij_table.CLASSICAL_MAKHARIJ` وفيه حارسٌ يرفض "
            "غيرَ ١٦، و`docs/reference/lisan345_cluster_adjacency.md`"
        ),
        what_would_resolve_it=(
            "مصدرٌ مسمًّى للثلاثة عشر يُبيّن أنّه تصنيفٌ آخرُ مقصودٌ لا خطأ، أو "
            "إعادةُ صياغة الهرمية على المُبصَّم. ولا تُدمَج الأعدادُ الثلاثة"
        ),
        standing=ConflictStanding.BLOCKS_IMPORT_UNTIL_RESOLVED,
    ),
    HierarchyConflict(
        locus_in_hierarchy="§٢ المستوى ٠ — الصفة اثنا عشرَ محورًا",
        hierarchy_says=(
            "الصفةُ اثنا عشرَ محورًا شجريًّا، وإطباقٌ ⊆ استعلاء تحليليًّا " "بتعريفٍ معلَن"
        ),
        this_tree_says=(
            "جدولُ الصفات مستورَدٌ خلف حاجزٍ مفتوح، ولا يُعَدّ دعوى هذه الشجرة؛ "
            "والعلاقةُ التحليليّةُ تحصيلُ حاصلٍ من التعريف لا اكتشافٌ عن العربية"
        ),
        tree_reference=(
            "`gflk_feature_table_import_barrier` و"
            "`AN_IMPORTED_TABLE_IS_NOT_A_CLAIM_OF_THIS_TREE`"
        ),
        what_would_resolve_it=(
            "إيداعُ **نصّ** التعريف المُعلَن الذي يُشتَقّ منه الاحتواء؛ فقولُ "
            "«بتعريفٍ معلَن» بلا نصِّ ما أُعلِن إحالةٌ إلى غائب"
        ),
        standing=ConflictStanding.BLOCKS_IMPORT_UNTIL_RESOLVED,
    ),
    HierarchyConflict(
        locus_in_hierarchy="§٢ المستوى ١ و٤ — «أل» علامةً للاسم",
        hierarchy_says=(
            "الاسمُ يقبل «أل» أو تنوينًا تبادليًّا بصفر تقاطع، والفعلُ يرفضهما " "بصفر خرق"
        ),
        this_tree_says=(
            "طبقةُ «أل» محجوبةٌ متعذّرةٌ من العلامات المكتوبة: لا موافقةٌ ولا "
            "مخالفة، لا صفرٌ ولا غيرُ صفر"
        ),
        tree_reference="`DictionaryLayer.AL_ANALYSIS` وحقلُ `al_undecidable_from_marks`",
        what_would_resolve_it=(
            "استيفاءُ شرطِ دخول الطبقة؛ و«صفر تقاطع» على طرفٍ غيرِ مقيسٍ رقمٌ " "لا شاهدَ له"
        ),
        standing=ConflictStanding.BLOCKS_IMPORT_UNTIL_RESOLVED,
    ),
    HierarchyConflict(
        locus_in_hierarchy="§٢-أ المستوى ٢ — «صفر استثناء بعد إصلاح الساكن اليتيم»",
        hierarchy_says=(
            "المقطعُ يبدأ بصامتٍ متحرّكٍ وجوبًا، بصفر استثناءٍ حقيقيٍّ بعد "
            "إصلاح الساكن اليتيم"
        ),
        this_tree_says=(
            "`MEASURED_SAKIN_CLASH_SOURCES` **فارغة**: لا مدوّنةَ في الشجرة، "
            "والإغلاقُ محمولٌ بالتعريف لا بنسبةٍ مقيسة"
        ),
        tree_reference=(
            "`encoding/sakin_adjacency` و"
            "`MUQATTAAT_ARE_EXCLUDED_BY_DEFINITION_NOT_MEASURED`"
        ),
        what_would_resolve_it=(
            "إيداعُ مدوّنةٍ مُبصَّمةٍ يُشغَّل عليها المسحُ القائم، وتسميةُ "
            "«إصلاح الساكن اليتيم» استثناءً مُعلَنًا لا تصحيحًا صامتًا للبيانات"
        ),
        standing=ConflictStanding.BLOCKS_IMPORT_UNTIL_RESOLVED,
    ),
    HierarchyConflict(
        locus_in_hierarchy="§٢ المستوى ٥ — المبنيّ نوعين",
        hierarchy_says=(
            "المبنيُّ بحفظٍ معجميٍّ مغلق: أل الموصول ثلاثُ صيغٍ فقط، حالتُها "
            "**ثابتة** بلا قاعدة"
        ),
        this_tree_says=(
            "البناءُ حكمٌ على جنس اللفظ لا ثباتٌ مرصودٌ في السطح؛ وتعدادُ ما "
            "وقع مبنيًّا لا يُثبت حصرَ المبنيّات؛ و`MAWSUL_WORDS` لا تُستعمَل "
            "بلا مصدرٍ وبصمة"
        ),
        tree_reference=(
            "`MabniIsNotAnUnchangedSurfaceForm` و"
            "`EnumeratedExamplesAreNotAnExhaustiveCriterion` في "
            "`sentence_card_preregistration`، وشرطُ دخول `AL_ANALYSIS` في "
            "`word_structure_dictionary_preregistration`"
        ),
        what_would_resolve_it=(
            "نصٌّ مصدريٌّ منسوبٌ ومُبصَّمٌ يُثبت الحصرَ ويُعرّف البناءَ بجنس "
            "اللفظ لا بثبات الصورة؛ و`CardItem.MURAB_MABNI` منزلتُه "
            "`AWAITING_SOURCE_TEXT` قبلَ هذه الوثيقة"
        ),
        standing=ConflictStanding.BLOCKS_IMPORT_UNTIL_RESOLVED,
    ),
    HierarchyConflict(
        locus_in_hierarchy="§٢ المستوى ٢ — «٣٥٫٧٪ من الجذوع معرَبة»",
        hierarchy_says="المقطعُ النحويُّ وظيفيٌّ في ٣٥٫٧٪ من الجذوع",
        this_tree_says=(
            "لا مدوّنةَ مُودَعةً يُعاد عليها الاشتقاق. وللشجرة قياسٌ قريبٌ "
            "منواله لا رقمُه: `irab_case_readout` على ٤٢٦٥ موضعًا موسَّمًا"
        ),
        tree_reference="`irab_case_readout` و`arabic/encoding/measurement.py`",
        what_would_resolve_it=_REDERIVATION_CONDITION,
        standing=ConflictStanding.RECORDED_UNRESOLVED,
    ),
    HierarchyConflict(
        locus_in_hierarchy="§٢ المستوى ٤ — «تلوّث ٤٫٤٦٪»",
        hierarchy_says="نمطُ «يَفْعَلُ» للمضارع بتلوّثٍ قدرُه ٤٫٤٦٪",
        this_tree_says=(
            "رقمٌ واحدٌ بلا قسمٍ محجوبٍ لا يُميّز التنبّؤَ من الملاءمة؛ "
            "والرقمان يُصدَران معًا لأنّ فرقَهما هو مقدارُ الملاءمة"
        ),
        tree_reference="`TUNED_ON_DEV_REPORTED_ON_HELD_OUT` في `irab_case_readout`",
        what_would_resolve_it=(
            "قسمةُ المدوّنة بقاعدةٍ لا علاقةَ لها بالجواب، وإعلانُ الرقمين معًا: "
            "على القسم المحجوب وعلى الكلّ"
        ),
        standing=ConflictStanding.RECORDED_UNRESOLVED,
    ),
    HierarchyConflict(
        locus_in_hierarchy="§٢ الفجوة الجذرية — «٤٫٧٦٪»",
        hierarchy_says=("٤٫٧٦٪ من التوكِنات الفراغيّة تحوي أكثرَ من كلمةٍ منطقيّةٍ واحدة"),
        this_tree_says=(
            "لا مدوّنةَ، ولا تعريفَ مُجمَّدًا لحدّ الكلمة المنطقيّة يُقاس عليه؛ "
            "والعدُّ تابعٌ للحدّ لا كاشفٌ عنه"
        ),
        tree_reference="`text_key` و`arabic/encoding/measurement.py`",
        what_would_resolve_it=(
            f"{_REDERIVATION_CONDITION}؛ وتعريفٌ مُجمَّدٌ لحدّ الكلمة المنطقيّة " "قبل العدّ"
        ),
        standing=ConflictStanding.RECORDED_UNRESOLVED,
    ),
    HierarchyConflict(
        locus_in_hierarchy="§٢ المستوى ٣ — مجرد/مزيد مسحوبًا",
        hierarchy_says="مجرد/مزيد معيارٌ سطحيٌّ معطوب، مسحوبٌ من الخواصّ الموثوقة",
        this_tree_says=(
            "منزلةُ الطبقة `فرضٌ مُعلَنُ العطب` مكتوبةٌ قبلَ هذه الوثيقة، "
            "بالعلّة نفسِها: لا يُميّز زائدًا مُقحَمًا من أصليٍّ مصادِف"
        ),
        tree_reference=(
            "`DictionaryLayer.JARAD_ANALYSIS` في `DICTIONARY_LAYER_REGISTRATIONS`"
        ),
        what_would_resolve_it=(
            "لا شيء: هذا **توافقٌ** يُسجَّل لا تعارضٌ يُحسَم. وسُجّل لأنّ "
            "الموافقةَ غيرُ المُسجَّلة تُقرأ بعد جلساتٍ خلافًا"
        ),
        standing=ConflictStanding.RECORDED_UNRESOLVED,
    ),
    HierarchyConflict(
        locus_in_hierarchy="§٢ المستوى ٤ — اسم/فعل/حرف",
        hierarchy_says="الكلمةُ اسمٌ أو فعلٌ أو حرفُ معنًى، لا رابعَ",
        this_tree_says=(
            "`card(Ω)=3` مُجمَّدٌ بسؤالين وأربعةِ شهودٍ من نصٍّ واحد؛ فالعددُ "
            "موافق، والخلافُ في علاماتِ التمييز — «أل» والتنوين — لا في المفردة"
        ),
        tree_reference="`word_class_formal` ومفردتُه `WordClass`",
        what_would_resolve_it=(
            "استيفاءُ شرطِ دخول `AL_ANALYSIS`، فتصير علامةُ التمييز مقيسةً "
            "كالمفردة؛ والموافقةُ في العدد لا تُغني عن ذلك"
        ),
        standing=ConflictStanding.RECORDED_UNRESOLVED,
    ),
    HierarchyConflict(
        locus_in_hierarchy="§٢ المستوى ٠ — تردّد الأداة ×٤٣-١٦٠",
        hierarchy_says="علّةُ الحرف وظيفةٌ لا وضعٌ، بدليل تردّدِ الأداة ×٤٣-١٦٠",
        this_tree_says=(
            "الأثرُ التوزيعيُّ ليس مسارَ وضعٍ: الإحصاءُ يرفع الدرايةَ ولا يصنع "
            "روايةً، والوضعُ لا يُشتَقّ من تردّد"
        ),
        tree_reference=(
            "`DISTRIBUTIONAL_TRACE_IS_NOT_WAD_PATH` و"
            "`STATISTICS_RAISE_DIRAYA_NEVER_MAKE_RIWAYA` في `wad_naql`"
        ),
        what_would_resolve_it=(
            "قراءةُ الرقم أثرًا توزيعيًّا موصوفًا لا دليلَ وضعٍ؛ فإن أُريد به "
            "الوضعُ فمسارُه روايةٌ لا إحصاء"
        ),
        standing=ConflictStanding.RECORDED_UNRESOLVED,
    ),
    HierarchyConflict(
        locus_in_hierarchy="§٢-ب — فئةُ الإدغام الثالثة وإغلاقُ التركيب النحويّ",
        hierarchy_says=(
            "التقاءُ المثلين/المتقاربين عبر حدّ الكلمة «مكتشَفٌ الآن، يُفسِّر "
            "كلَّ ما تبقّى»، فيُغلَق التركيبُ النحويُّ ١٠٠٪ بلا استثناءٍ متبقٍّ"
        ),
        this_tree_says=(
            "استثناءٌ كُتِب **بعد** فحص البواقي ليس شاهدًا للقاعدة التي أنقذها: "
            "فئةٌ عُرِّفت بأنّها «ما تبقّى» لا يتبقّى بعدها شيءٌ بحكم تعريفها، "
            "فالإغلاقُ تحصيلُ حاصلٍ لا نتيجةُ قياس"
        ),
        tree_reference=(
            "`RESIDUE_DEFINED_EXCLUSIONS_ARE_NOT_INDEPENDENT_EVIDENCE` وحقلُ "
            "`SakinClashExclusion.is_residue_defined` في `encoding/sakin_adjacency`"
        ),
        what_would_resolve_it=(
            "**نصُّ شرطِ الفئة الثالثة** صوتيًّا مستقلًّا، مكتوبًا قبل الفحص "
            "لا بعده، فيُطبَّق على مواضعَ لم تُفحَص. والظاهرةُ نفسُها معروفةٌ "
            "لا مُنكَرة؛ والخلافُ في ترتيب الكتابة: ما كُتب قبلَ الفحص ينبّئ، "
            "وما كُتب بعده يصف"
        ),
        standing=ConflictStanding.BLOCKS_IMPORT_UNTIL_RESOLVED,
    ),
    HierarchyConflict(
        locus_in_hierarchy="§٢-ب — وكيلُ الوقف كاشفًا لحدّ الإسناد",
        hierarchy_says=(
            "الوقفُ التامُّ مُقترَحٌ كاشفًا لحدّ الإسناد عبر "
            "`WAQF-SEL-MARKER-PROXY-AR-1` (٥٦٪/٢٣٪)، والربطُ لم يُختبَر تكامليًّا"
        ),
        this_tree_says=(
            "الإشارةُ المُميِّزةُ التي يقوم عليها الوكيلُ **غيرُ مُعرَّفةٍ في "
            "المرماز** لا ضعيفةٌ ولا ناقصة: علامةُ الوقف وحدةُ `PASSTHROUGH` "
            "لا تُقرأ سكونًا على ما قبلها، فسكونُ الوقف لا يُميَّز من سكون الوصل"
        ),
        tree_reference=(
            "`PAUSAL_SUKUN_IS_NOT_DISTINGUISHED_FROM_CONNECTED_SUKUN` في "
            "`encoding/sakin_adjacency`"
        ),
        what_would_resolve_it=(
            "تمييزُ سكون الوقف من سكون الوصل في المرماز أوّلًا، فقبلَه لا "
            "يُختبَر الربطُ تكامليًّا ولا جزئيًّا؛ والنصُّ يسمّي هذا «أخطرَ "
            "DEFER»، والشجرةُ تُشدّد التسميةَ ولا تُخفّفها"
        ),
        standing=ConflictStanding.BLOCKS_IMPORT_UNTIL_RESOLVED,
    ),
    HierarchyConflict(
        locus_in_hierarchy="§٢-ب — استقلالُ التركيب المزجيّ عن إغلاق النحويّ",
        hierarchy_says=(
            "ثلاثُ نتائجَ مستقلّة: إغلاقٌ نحويٌّ، وصفرُ فجوةٍ، وغيابُ التركيب المزجيّ شاهدًا"
        ),
        this_tree_says=(
            "الثلاثةُ مخرجُ فئةٍ واحدةٍ لا ثلاثةُ شهود: صفرُ الفجوة وصفرُ "
            "المزجيّ كلاهما مأخوذٌ بتفسير المرشَّحين بالفئة الثالثة نفسِها. "
            "وعرضُ نتيجةٍ واحدةٍ ثلاثَ مرّاتٍ يُضاعف الثقةَ بلا مُدخَلٍ جديد"
        ),
        tree_reference=(
            "`HierarchyNumericClaim.depends_on_figure` في هذه الوحدة، و"
            "`STATISTICS_RAISE_DIRAYA_NEVER_MAKE_RIWAYA` في `wad_naql`"
        ),
        what_would_resolve_it=(
            "مسارُ اشتقاقٍ لكلِّ نتيجةٍ لا يمرّ بالفئة الثالثة، أو إعلانُ "
            "التبعيّة في النصّ نفسِه؛ والتبعيّةُ مُسجَّلةٌ هنا في كلّ حال"
        ),
        standing=ConflictStanding.RECORDED_UNRESOLVED,
    ),
)


THE_DEPOSIT_IS_NOT_AN_ADOPTION_NOTE: Final[str] = (
    "TheDepositIsNotAnAdoption: إيداعُ الهرمية يُثبِّت بايتاتِها لتُدقَّق، ولا "
    "يُصدِّق رقمًا فيها ولا تصنيفًا ولا يرفع حجبًا عن طبقةٍ محجوبة"
)

A_SUPERSEDED_VERSION_IS_RECORDED_NOT_ERASED_NOTE: Final[str] = (
    "ASupersededVersionIsRecordedNotErased: النسختان تُودَعان معًا، ولكلّ دعوى "
    "مسحوبةٍ خَلَفُها وسببُ سحبها؛ وما سقط بلا سببٍ يُسمّى ساقطًا بلا سبب ولا "
    "يُحمَل على أنّه صُحِّح"
)

A_NUMBER_WITHOUT_A_CORPUS_IS_NOT_A_MEASUREMENT_NOTE: Final[str] = (
    "ANumberWithoutACorpusIsNotAMeasurement: كلُّ رقمٍ هنا غيرُ قابلٍ لإعادة "
    "الاشتقاق بسببٍ مُسمًّى؛ و«صفر خرق» دعوى عمومٍ أثقلُ من النسبة لا أخفّ، إذ "
    "يكفي لنقضها موضعٌ واحد"
)

AGGREGATION_DOES_NOT_LEVEL_EPISTEMIC_RANK_NOTE: Final[str] = (
    "AggregationDoesNotLevelEpistemicRank: كلُّ عقدةٍ تحمل منزلتَها من المفردة "
    "الرباعية المغلقة القائمة، وجمعُها في هرميّةٍ واحدةٍ متجانسةِ الشكل لا "
    "يُسوّي بين المقيس والمستورَد والمتعذّر والفرض"
)

A_RECORDED_CONFLICT_IS_NOT_A_RESOLVED_ONE_NOTE: Final[str] = (
    "ARecordedConflictIsNotAResolvedOne: كلُّ تعارضٍ يحمل موضعَه ومرجعَ الشجرة "
    "وشرطَ حسمه ولا يحمل حسمًا؛ ومن حسم تعارضًا في جلسة رصده بلا مُدخَلٍ جديدٍ "
    "رجّح ما كان يرجّحه سلفًا"
)

A_DEPENDENT_FIGURE_IS_NOT_A_SECOND_WITNESS_NOTE: Final[str] = (
    "ADependentFigureIsNotASecondWitness: رقمٌ يقوم على رقمٍ آخرَ يُسمّيه في "
    "`depends_on_figure`، ورقمٌ مخرجُه فئةٌ عُرِّفت بالباقي لا يُسجَّل بلا هذا "
    "الوسم؛ فثلاثُ نتائجَ من فئةٍ واحدةٍ نتيجةٌ واحدةٌ قُرئت ثلاثًا"
)

A_SUBMITTED_FREEZE_IS_NOT_A_FREEZE_HERE_NOTE: Final[str] = (
    "ASubmittedFreezeIsNotAFreezeHere: مُعرِّفُ التجميد الوارد محفوظٌ بحروفه "
    "ومعه `NOT_ISSUED_BY_THIS_TREE`؛ وإعلانُ التجميد في محادثةٍ خارجيّةٍ لا "
    "يُجمّد شيئًا في هذه الشجرة، ولا إعلانُ الإغلاق يُغلق فيها بابًا"
)

THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE: Final[str] = (
    "ThisIsRegistrationNotAuthority: لا ولادةَ هنا ولا حكمَ ولادةٍ ولا تجميدَ "
    "`E0`؛ والطبقاتُ الأربعُ المحجوبةُ تبقى محجوبةً بعد هذا الإيداع كما كانت قبله"
)


def _assert_no_result_field() -> None:
    """حارسُ استيراد: لا حقلَ نتيجةٍ ولا حسمٍ يتسلّل إلى إيداعٍ لاحقًا."""

    for dataclass_type in (
        HierarchyNode,
        SupersededClaim,
        HierarchyNumericClaim,
        HierarchyConflict,
        SubmittedFreezeIdentifier,
        WordHierarchyDeposit,
    ):
        for declared in fields(dataclass_type):
            lowered = declared.name.lower()
            for token in _FORBIDDEN_FIELD_TOKENS:
                if token in lowered:
                    raise WordHierarchyDepositError(
                        f"حقلٌ يحمل نتيجةً أو حسمًا تسلّل إلى "
                        f"{dataclass_type.__name__}: {declared.name}؛ والإيداعُ "
                        "لا نتيجةَ فيه ولا حسم"
                    )


if len(HierarchyLevel) != 6:  # pragma: no cover - حارس
    raise RuntimeError("مستوياتُ الهرمية ستٌّ كما وردت في النسخة الثانية.")
if len({node.node_id for node in WORD_HIERARCHY_NODES}) != len(WORD_HIERARCHY_NODES):
    raise RuntimeError("لا تُسجَّل عقدةٌ مرّتين بمعرّفٍ واحد.")
if {node.level for node in WORD_HIERARCHY_NODES} != set(HierarchyLevel):
    raise RuntimeError("لكلِّ مستوًى عقدةٌ واحدةٌ على الأقلّ، ولا مستوًى بلا عقدة.")
if len({claim.figure for claim in WORD_HIERARCHY_NUMERIC_CLAIMS}) != len(
    WORD_HIERARCHY_NUMERIC_CLAIMS
):
    raise RuntimeError("لا يُسجَّل رقمٌ واحدٌ بصفّين.")
if len({claim.locus for claim in SUPERSEDED_CLAIMS}) != len(SUPERSEDED_CLAIMS):
    raise RuntimeError("لا تُسجَّل دعوى مسحوبةٌ مرّتين بموضعٍ واحد.")
if len({conflict.locus_in_hierarchy for conflict in WORD_HIERARCHY_CONFLICTS}) != len(
    WORD_HIERARCHY_CONFLICTS
):
    raise RuntimeError("لا يُسجَّل تعارضٌ واحدٌ بصفّين.")
if len({entry.identifier for entry in SUBMITTED_FREEZE_IDENTIFIERS}) != len(
    SUBMITTED_FREEZE_IDENTIFIERS
):
    raise RuntimeError("لا يُسجَّل مُعرِّفُ تجميدٍ واردٍ مرّتين.")
_KNOWN_FIGURES: Final[frozenset[str]] = frozenset(
    claim.figure for claim in WORD_HIERARCHY_NUMERIC_CLAIMS
)
for _claim in WORD_HIERARCHY_NUMERIC_CLAIMS:  # pragma: no cover - حارس
    if _claim.depends_on_figure is None:
        continue
    if _claim.depends_on_figure not in _KNOWN_FIGURES:
        raise RuntimeError("وسمُ التبعيّة يُحيل إلى رقمٍ مُسجَّلٍ في السجلّ نفسِه.")
    if _claim.depends_on_figure == _claim.figure:
        raise RuntimeError("لا يعتمد رقمٌ على نفسه.")
_assert_no_result_field()
