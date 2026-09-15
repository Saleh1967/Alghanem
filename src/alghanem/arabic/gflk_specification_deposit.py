"""إيداعُ مواصفة GFLK نصًّا مُبصَّمًا، وسجلُّ تعارضاتها مع الشجرة — بلا حسم.

**ما تفعله هذه الوحدة**: تُثبِّت بايتاتِ وثيقةٍ وصلت من محادثةٍ خارجية،
وتُسجِّل مواضعَ تعارضها مع ما في هذه الشجرة. لا أكثر. فنقاشٌ على نصٍّ لا بصمةَ
له نقاشٌ على نصٍّ يتحرّك، وكلُّ طرفٍ يذكر منه ما يذكر.

`THE_DEPOSIT_IS_NOT_AN_ADOPTION`: إيداعُ نصٍّ ليس تصديقًا لرقمٍ فيه ولا
لتصنيف. وللشجرة سابقةٌ في هذا بعينه: نصٌّ من المصدر نفسه ادّعى
`Close(Open(x)) ≅ x` بنسبة ١٠٠٪، فأُعيد اشتقاقُه على المدوّنة المُبصَّمة فخرج
٩٩٫٩٩٢٢٥١٪ (`gflk_codec_revision_audit`). فالإيداعُ يُثبِّت ما يُدقَّق، ولا
يُغني عن التدقيق.

`THE_DIGEST_IS_READ_FROM_THE_FILE_NOT_WRITTEN_HERE`: بصمةُ الوثيقة تُشتَقّ من
بايتاتها عند القراءة. فبصمةٌ مكتوبةٌ بيدٍ في وحدةٍ أخرى بصمةٌ يمكن أن تُحدَّث
وحدها بعد تحريرٍ فتُصادق على ما لم تُبصَّم عليه.

`A_RECORDED_CONFLICT_IS_NOT_A_RESOLVED_ONE`: كلُّ تعارضٍ يحمل موضعَه في
الوثيقة، وما تقوله الشجرةُ في الموضع نفسه بمرجعه، و**ما يلزم لحسمه** — ولا
يحمل حسمًا. فمن سجّل تعارضًا وحسمه في الجلسة نفسها بلا مُدخَلٍ جديدٍ إنّما
رجّح ما كان يرجّحه سلفًا.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا
تجميدَ `E0`، ولا استيرادَ من `kernel/`، ولا تقرأ هذه الوحدةَ وحدةٌ فيه.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Final

from .pipeline_stations import repository_root_path

__all__ = [
    "A_RECORDED_CONFLICT_IS_NOT_A_RESOLVED_ONE_NOTE",
    "GFLK_SPECIFICATION_CONFLICTS",
    "GFLK_SPECIFICATION_DEPOSIT",
    "SPECIFICATION_RELATIVE_PATH",
    "THE_DEPOSIT_IS_NOT_AN_ADOPTION_NOTE",
    "ConflictStanding",
    "GflkSpecificationConflict",
    "GflkSpecificationDeposit",
    "GflkSpecificationDepositError",
    "ProvenanceGenus",
    "read_specification_bytes",
    "specification_digest",
]

SPECIFICATION_RELATIVE_PATH: Final[str] = (
    "docs/reference/gflk_arabic_letter_specification.md"
)


class GflkSpecificationDepositError(ValueError):
    """رفضٌ عند الإنشاء: إيداعٌ ناقصٌ أو تعارضٌ بلا موضعٍ أو بلا شرطِ حسم."""


class ProvenanceGenus(Enum):
    """جنسُ ما وصل: نصُّ محادثةٍ أخرى لا مصدرٌ منشورٌ ولا قياسُ هذه الشجرة."""

    PROSE_FROM_ANOTHER_CONVERSATION = "نصٌّ من محادثةٍ أخرى"


class ConflictStanding(Enum):
    """منزلةُ التعارض. ليس فيها `محسوم`؛ الحسمُ يقع في مرحلةٍ أخرى بشرطها."""

    RECORDED_UNRESOLVED = "مرصودٌ غيرُ محسوم"
    BLOCKS_IMPORT_UNTIL_RESOLVED = "حاجزٌ للاستيراد حتى يُحسَم"


@dataclass(frozen=True, slots=True)
class GflkSpecificationConflict:
    """تعارضٌ مرصود: موضعُه، وما تقوله الشجرة، وما يلزم لحسمه."""

    locus_in_specification: str
    specification_says: str
    this_tree_says: str
    tree_reference: str
    what_would_resolve_it: str
    standing: ConflictStanding

    def __post_init__(self) -> None:
        for field_name in (
            "locus_in_specification",
            "specification_says",
            "this_tree_says",
            "tree_reference",
            "what_would_resolve_it",
        ):
            if not str(getattr(self, field_name)).strip():
                raise GflkSpecificationDepositError(
                    "تعارضٌ بلا موضعٍ أو بلا مرجعٍ أو بلا شرطِ حسمٍ ليس تعارضًا "
                    "مرصودًا بل انطباعًا"
                )


def specification_path(root: Path | None = None) -> Path:
    """مسارُ الوثيقة المُودَعة، مُشتقًّا من جذر المستودع لا مكتوبًا مطلقًا."""

    return (root or repository_root_path()) / SPECIFICATION_RELATIVE_PATH


def read_specification_bytes(root: Path | None = None) -> bytes:
    """بايتاتُ الوثيقة كما هي على القرص، بلا تطبيعٍ ولا فكِّ ترميز."""

    path = specification_path(root)
    if not path.is_file():
        raise GflkSpecificationDepositError(
            f"الوثيقةُ المُودَعة غيرُ موجودةٍ في الشجرة: {SPECIFICATION_RELATIVE_PATH}"
        )
    return path.read_bytes()


def specification_digest(root: Path | None = None) -> str:
    """بصمةُ الوثيقة مُشتقّةً من بايتاتها، لا منسوخةً من حقلٍ في وحدةٍ أخرى."""

    return hashlib.sha256(read_specification_bytes(root)).hexdigest()


@dataclass(frozen=True, slots=True)
class GflkSpecificationDeposit:
    """الإيداع: جنسُ المصدر، وتاريخُ الوصول، وموضعُ النصّ، ولا شيءَ سواه."""

    genus: ProvenanceGenus
    arrival_date: str
    relative_path: str

    def __post_init__(self) -> None:
        if not self.arrival_date.strip() or not self.relative_path.strip():
            raise GflkSpecificationDepositError("إيداعٌ بلا تاريخِ وصولٍ أو بلا موضع")

    def digest(self, root: Path | None = None) -> str:
        """بصمةُ الوثيقة الآن، تُقرأ من الملفّ في كلّ نداء."""

        return specification_digest(root)


GFLK_SPECIFICATION_DEPOSIT: Final[GflkSpecificationDeposit] = GflkSpecificationDeposit(
    genus=ProvenanceGenus.PROSE_FROM_ANOTHER_CONVERSATION,
    arrival_date="2026-09-15",
    relative_path=SPECIFICATION_RELATIVE_PATH,
)


GFLK_SPECIFICATION_CONFLICTS: Final[tuple[GflkSpecificationConflict, ...]] = (
    GflkSpecificationConflict(
        locus_in_specification="§٣ — جدول المخرج",
        specification_says="المخرجُ ثلاثَ عشرةَ فئة",
        this_tree_says=(
            "ثمانيةٌ وعشرون صامتًا في **ستّةَ عشرَ** مخرجًا، والخيشومُ سابعَ عشرَ "
            "مخرجَ غنّةٍ لا مخرجَ حرفٍ مستقلّ"
        ),
        tree_reference=(
            "docs/reference/classical_makharij_ordering.md، "
            "و`classical_makharij_table.CLASSICAL_MAKHARIJ` وفيه حارسٌ يرفض غيرَ ١٦"
        ),
        what_would_resolve_it=(
            "مصدرٌ مسمًّى للثلاثة عشر يُبيّن أنّه تصنيفٌ آخرُ مقصودٌ لا خطأ، أو "
            "إعادةُ صياغة المواصفة على الستّة عشر المُبصَّمة. ولا يُدمَج الرقمان"
        ),
        standing=ConflictStanding.BLOCKS_IMPORT_UNTIL_RESOLVED,
    ),
    GflkSpecificationConflict(
        locus_in_specification="§٣ — حروف الزيادة (سألتمونيها)",
        specification_says=(
            "عشرةُ أحرفِ زيادةٍ تشمل `أ` و`ا` عضوين، والباقي ثمانيةَ عشرَ أصليًّا "
            "محضًا، فالمجموع ثمانيةٌ وعشرون"
        ),
        this_tree_says=(
            "تمييزُ الهمزة عن الألف **هويّةٌ مؤجَّلة** إلى بوّابةِ ولادةٍ لم تُبنَ؛ "
            "وجودُ الحرف هنا مرصودٌ لا ماهويّ"
        ),
        tree_reference=(
            "`LETTER_EXISTENCE_HERE_IS_OBSERVED_NOT_ESSENTIAL` في "
            "`encoding/state_evidence.py`، وتأجيلُ الهويّة في README"
        ),
        what_would_resolve_it=(
            "التصريحُ بأنّ العدَّ عدُّ **أشكالٍ سطحيّة** لا عدُّ حروفٍ ذاتِ هويّة، "
            "أو بوّابةُ ولادةٍ تُثبت الهويّة فيصير العدُّ عدَّ حروف"
        ),
        standing=ConflictStanding.RECORDED_UNRESOLVED,
    ),
    GflkSpecificationConflict(
        locus_in_specification="§١ مقابل §٢ — منزلة DEFER",
        specification_says=(
            "§١: «القرارُ النهائيُّ دومًا ثنائيّ، وDEFER تأجيلٌ إجرائيٌّ لا قيمةٌ "
            "ثالثة». و§٢ يُخرج `AMBIGUOUS_MADD_OR_TANWEEN_ROOT` **عضوًا في مفردة "
            "الحالات** ويسمّيها «حالة DEFER صريحة»"
        ),
        this_tree_says=(
            "التعذّرُ مفردةٌ مستقلّةٌ لا تُجمَع أبدًا مع مفردة الفشل؛ والخلطُ "
            "بين الغياب والتعذّر هو البابُ الذي تُصنَع منه نتيجةٌ زائفة"
        ),
        tree_reference=(
            "`REFUSAL_IS_NOT_FAILURE_TO_DISCRIMINATE` في "
            "`morphological_necessity_measurement.py`"
        ),
        what_would_resolve_it=(
            "إخراجُ الغموض في **حقلِ تعذّرٍ منفصل** لا عضوًا في مفردة الحالات، "
            "فيستقيم §٢ مع §١ بلا تعديلِ أيٍّ منهما"
        ),
        standing=ConflictStanding.RECORDED_UNRESOLVED,
    ),
    GflkSpecificationConflict(
        locus_in_specification="§٦ — أرقام PILOT-3/4/5",
        specification_says=(
            "85.11% و87.67% و88.01% و88.34%، وround-trip «متحقَّقٌ فعليًّا على "
            "تشكيلة (7,4,1)» وحدها"
        ),
        this_tree_says=(
            "لا يُصدَر رقمُ ضغطٍ بلا مطابقةٍ محقّقة، ولا يُقاس على بايتاتٍ بلا "
            "بصمةٍ مُجمَّدة؛ والرقمان — حمولةً وكلّيًّا — يُصدَران معًا أو لا شيء"
        ),
        tree_reference=(
            "`ROUND_TRIP_IS_A_PRECONDITION_OF_ISSUANCE` و`TWO_SIZES_OR_NONE` في "
            "`compression_model_preregistration.py`"
        ),
        what_would_resolve_it=(
            "بصمةُ بايتات النصّ المقيس، ومطابقةٌ محقّقةٌ لكلّ رقمٍ على حدة. "
            "ومنزلةُ الأرقام الأربعة الآن مُسجَّلةٌ في "
            "`compression_model_revision_audit`"
        ),
        standing=ConflictStanding.BLOCKS_IMPORT_UNTIL_RESOLVED,
    ),
    GflkSpecificationConflict(
        locus_in_specification="§٣ و§٧ — إطباق ⊆ استعلاء",
        specification_says=(
            "علاقةُ احتواءٍ «مُثبَتة تحليليًّا لا إحصائيًّا»، ويُبنى عليها توفيرُ "
            "الترميز الشجريّ ١٨٫٧٥٪–٢٣٫٢٪"
        ),
        this_tree_says=(
            "قضيّةٌ تحليليّةٌ لا مضمونَ تجريبيَّ لها: إن كان الإطباقُ مُعرَّفًا بما "
            "يستلزم الاستعلاء فالاحتواءُ تحصيلُ حاصلٍ من التعريف لا اكتشافٌ عن "
            "العربية، والتوفيرُ نتيجةُ بنية التعريف لا بنية اللغة"
        ),
        tree_reference=(
            "`imported_feature_vocabulary.IMPORTED_VOCABULARY_IS_NOT_BORN_NOTE`"
        ),
        what_would_resolve_it=(
            "تسجيلُ نصّ التعريف المستعمَل إلى جانب العلاقة، فيُقرأ الاحتواءُ "
            "تحليليًّا كما وُصِف ولا يُقرأ بعدها اكتشافًا"
        ),
        standing=ConflictStanding.RECORDED_UNRESOLVED,
    ),
)


THE_DEPOSIT_IS_NOT_AN_ADOPTION_NOTE: Final[str] = (
    "TheDepositIsNotAnAdoption: إيداعُ نصٍّ يُثبِّت بايتاتِه ليُدقَّق، ولا "
    "يُصدِّق رقمًا فيه ولا تصنيفًا؛ وقد أُعيد اشتقاقُ ادّعاءٍ سابقٍ من المصدر "
    "نفسه فخرج ٩٩٫٩٩٢٢٥١٪ لا ١٠٠٪"
)

A_RECORDED_CONFLICT_IS_NOT_A_RESOLVED_ONE_NOTE: Final[str] = (
    "ARecordedConflictIsNotAResolvedOne: كلُّ تعارضٍ يحمل موضعَه ومرجعَ الشجرة "
    "وشرطَ حسمه ولا يحمل حسمًا؛ ومن حسم تعارضًا في جلسة رصده بلا مُدخَلٍ جديدٍ "
    "رجّح ما كان يرجّحه سلفًا"
)

THE_DIGEST_IS_READ_FROM_THE_FILE_NOTE: Final[str] = (
    "TheDigestIsReadFromTheFileNotWrittenHere: بصمةُ الوثيقة تُشتَقّ من بايتاتها "
    "عند كلّ نداء؛ وبصمةٌ مكتوبةٌ بيدٍ يمكن أن تُحدَّث وحدها بعد تحريرٍ فتصادق "
    "على ما لم تُبصَّم عليه"
)

THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE: Final[str] = (
    "تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا استيرادَ من "
    "`kernel/`، ولا تقرأ هذه الوحدةَ وحدةٌ فيه"
)
