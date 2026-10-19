"""تجميدُ معيار مجرّد/مزيد قبل تطبيقه: خانةٌ مُعرَّفة، وحدٌّ دائم، وأعدادٌ لا تُتبنّى.

هذه الوحدةُ تُكتَب قبل `jarad_mazid`، وتُجمِّد ثلاثة أشياء: **ما الخانة**،
و**ما الحدُّ الذي لا يُتجاوَز**، و**ما شرطُ إصدار أيِّ عددٍ على مدوّنة**.

`A_SLOT_IS_A_REAL_CONSONANT_OR_A_MADD`: الخانةُ الجذريّةُ يملؤها صامتٌ حقيقيٌّ
أو حرفُ مدّ؛ وثلاثُ خاناتٍ ⇒ مجرّد، وأربعٌ فأكثرُ ⇒ مزيد. وهذا هو التصحيحُ
الذي أعلنته المواصفةُ على نفسها، لا اجتهادٌ يُضاف إليها.

`LENGTH_ONLY_NEVER_THE_IDENTITY_OF_THE_WEAK_LETTER`: حدٌّ **دائمٌ** لا مؤقّت:
هذا المعيارُ يقيس **عددَ الخانات** ولا يقول شيئًا عن هويّة الواو والياء في
الجذر المعتلّ. فمن قرأ منه «هذا الحرفُ واوٌ أصليّةٌ لا زائدة» قرأ ما لم يُقَس،
ولا يرفع هذا الحدَّ قياسٌ أوسعُ على المعيار نفسِه.

`MATCHING_IS_ON_THE_FULL_SKELETON_NEVER_ON_A_PREFIX`: المطابقةُ على الهيكل
الساكن الكامل؛ ومطابقةُ البادئة هي العطبُ الذي صحّحته المواصفةُ نفسُها، فلا
تُنفَّذ هنا بحالٍ ولو أنتجت أعدادًا أقربَ إلى المُودَع.

`THE_FOUR_CORPUS_COUNTS_ARE_NOT_ADOPTED`: أعدادُ المدوّنة الأربعةُ مُسجَّلةٌ
في `gflk_specification_deposit` بتعارضها ومجموعِها، ولا تُتبنّى هنا ولا تُعاد
كتابتُها: ينقصها `MeasurementRunManifest` في
`arabic/encoding/measurement.py`، وينقصها توقّعٌ مكتوبٌ قبل القياس. فما يُجمَّد
هنا **قواعدُ عدّها** لا أرقامُها، ليُقاس بها لاحقًا فيُنشَر ما خرج ويُسجَّل
فرقُه عن المُودَع.

`ENUMERATED_EXAMPLES_ARE_NOT_A_RULE`: أمثلةُ المعتلّ الستّةُ و«٤/٤» في فعل
الأمر تبقى أمثلةً معدودةً موسومةً بأنّها غيرُ كلّيّة؛ ولا تُشحَن واحدةٌ منها
إجراءَ قرار.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكم، ولا تجميدَ `E0`،
ولا استيرادَ من `kernel/`، ولا رفعَ حجبٍ عن طبقة `JARAD_ANALYSIS`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from alghanem.canonical_content import canonical_bytes, canonical_digest

from .maqayis_root_table_deposit import FROZEN_ROOT_TABLE
from .word_structure_dictionary_preregistration import (
    DictionaryLayer,
    LayerRegistration,
)
from .word_structure_dictionary_preregistration import (
    layer_registration as _dictionary_layer_registration,
)

__all__ = [
    "A_SLOT_IS_A_REAL_CONSONANT_OR_A_MADD",
    "CORPUS_BUCKET_RULES",
    "ENUMERATED_EXAMPLES_ARE_NOT_A_RULE",
    "JARAD_MAZID_PREREGISTRATION_NAMED_RESIDUALS",
    "LENGTH_ONLY_NEVER_THE_IDENTITY_OF_THE_WEAK_LETTER",
    "MATCHING_IS_ON_THE_FULL_SKELETON_NEVER_ON_A_PREFIX",
    "MAZID_MINIMUM_SLOTS",
    "MUJARRAD_SLOT_COUNT",
    "PREREGISTRATION_DIGEST",
    "PUBLICATION_PREREQUISITES",
    "THE_FOUR_CORPUS_COUNTS_ARE_NOT_ADOPTED",
    "THIS_IS_REGISTRATION_NOT_AUTHORITY",
    "CorpusBucketRule",
    "JaradMazidPreregistrationError",
    "PublicationPrerequisite",
    "bucket_named",
    "layer_registration",
    "preregistration_digest",
    "root_table_reference",
]


class JaradMazidPreregistrationError(ValueError):
    """رفضٌ عند الإنشاء: فئةٌ بلا قاعدةِ عدّ، أو رقمٌ يُتبنّى بلا شرطِ إصدار."""


MUJARRAD_SLOT_COUNT: Final[int] = 3
"""عددُ الخانات الذي يُقرأ مجرّدًا؛ مُعلَنٌ لأنّه تعريفُ المعيار لا نتيجتُه."""

MAZID_MINIMUM_SLOTS: Final[int] = MUJARRAD_SLOT_COUNT + 1
"""أدنى عددِ خاناتٍ يُقرأ مزيدًا، مُشتقًّا من الحدّ السابق لا مكتوبًا ثانيةً."""


class PublicationPrerequisite(Enum):
    """شرطُ إصدارِ عددٍ على مدوّنة. مفردةٌ مغلقة، وكلُّها لازمٌ لا أحدُها."""

    MEASUREMENT_RUN_MANIFEST = "بيانُ تشغيلِ قياسٍ مُجمَّدٌ بصيغة التطبيع ونسخة قاعدة يونيكود"
    WRITTEN_EXPECTATION_BEFORE_MEASURING = "توقّعٌ مكتوبٌ قبل القياس بما يُسقطه"
    DIGEST_PINNED_CORPUS = "مدوّنةٌ مُبصَّمةُ البايتات مُسمّاةٌ باسمها"
    DELTA_AGAINST_THE_DEPOSITED_FIGURE = "فرقٌ مُسجَّلٌ صراحةً عن الرقم المُودَع"


PUBLICATION_PREREQUISITES: Final[tuple[PublicationPrerequisite, ...]] = tuple(
    PublicationPrerequisite
)
"""الشروطُ الأربعةُ مجتمعةً؛ ونقصُ واحدٍ منها يمنع الإصدارَ لا يُخفِّض ثقتَه."""


@dataclass(frozen=True, slots=True)
class CorpusBucketRule:
    """فئةُ عدٍّ واحدةٌ من الأربع: قاعدةُ عدّها، ورقمُها المُودَع بلا تبنٍّ."""

    name: str
    counting_rule: str
    deposited_figure: str
    is_adopted: bool = False

    def __post_init__(self) -> None:
        for value, label in (
            (self.name, "اسمُ الفئة"),
            (self.counting_rule, "قاعدةُ العدّ"),
            (self.deposited_figure, "الرقمُ المُودَع"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise JaradMazidPreregistrationError(f"{label} نصٌّ غير فارغ")
        if self.is_adopted:
            raise JaradMazidPreregistrationError(
                "لا يُتبنّى رقمٌ في وحدة تسجيلٍ قبْليّ؛ والتبنّي يحتاج بيانَ "
                "تشغيلٍ وتوقّعًا مكتوبًا قبل القياس"
            )

    def as_canonical_content(self) -> dict[str, str]:
        """محتوى الفئة للبصمة؛ والرقمُ المُودَع جزءٌ منه لأنّه ما سيُقارَن به."""

        return {
            "name": self.name,
            "counting_rule": self.counting_rule,
            "deposited_figure": self.deposited_figure,
        }


CORPUS_BUCKET_RULES: Final[tuple[CorpusBucketRule, ...]] = (
    CorpusBucketRule(
        name="MUJARRAD_CONFIRMED",
        counting_rule=(
            "كلمةٌ هيكلُها الساكنُ ثلاثُ خاناتٍ **ويُطابِق** جذرًا في جدول "
            "الجذور المُبصَّم مطابقةً كاملةً لا بادئةً"
        ),
        deposited_figure="10,599",
    ),
    CorpusBucketRule(
        name="UNCONFIRMED_THREE_SLOTS",
        counting_rule=(
            "ثلاثُ خاناتٍ بلا مطابقةٍ في الجدول؛ وفئةٌ مُعرَّفةٌ سلبًا تتحرّك "
            "بحركة الجدول لا بحركة اللغة، وهذا مُسجَّلٌ في نفس موضع رقمها"
        ),
        deposited_figure="11,467",
    ),
    CorpusBucketRule(
        name="MAZID_PROBABLE",
        counting_rule="أربعُ خاناتٍ فأكثر، بصرف النظر عن المطابقة",
        deposited_figure="37,682",
    ),
    CorpusBucketRule(
        name="UNDETERMINED",
        counting_rule=(
            "ما لم يقع في الثلاث السابقة: أقلُّ من ثلاث خانات، أو كلمةٌ رفضها "
            "المرمازُ قبل القراءة، أو موضعٌ متعذّرٌ مُسجَّل"
        ),
        deposited_figure="18,333",
    ),
)
"""قواعدُ الفئات الأربع مُجمَّدةً؛ وأرقامُها منقولةٌ للمقارنة لا مُتبنّاة."""


def bucket_named(name: str) -> CorpusBucketRule:
    """فئةٌ بعينها من الأربع، مقروءةً من الجدول المُجمَّد لا مُنشأةً عند النداء."""

    for bucket in CORPUS_BUCKET_RULES:
        if bucket.name == name:
            return bucket
    raise JaradMazidPreregistrationError(f"لا فئةَ باسم {name!r}؛ والفئاتُ أربعٌ مغلقة")


def layer_registration() -> LayerRegistration:
    """تسجيلُ طبقة مجرّد/مزيد، مقروءًا من موضعه السابق لا منسوخًا هنا."""

    return _dictionary_layer_registration(DictionaryLayer.JARAD_ANALYSIS)


def root_table_reference() -> str:
    """بصمةُ جدول الجذور المُجمَّد، مقروءةً من إيداعها لا مكتوبةً هنا."""

    return FROZEN_ROOT_TABLE.sha256_hex


A_SLOT_IS_A_REAL_CONSONANT_OR_A_MADD: Final[str] = (
    "ASlotIsARealConsonantOrAMadd: الخانةُ الجذريّةُ صامتٌ حقيقيٌّ أو حرفُ "
    "مدّ؛ وثلاثٌ مجرّدٌ وأربعٌ فأكثرُ مزيد. والحدُّ تعريفٌ مُعلَنٌ يُقاس به، "
    "لا نتيجةٌ خرجت من قياس"
)

LENGTH_ONLY_NEVER_THE_IDENTITY_OF_THE_WEAK_LETTER: Final[str] = (
    "LengthOnlyNeverTheIdentityOfTheWeakLetter: حدٌّ دائم: المعيارُ يقيس عددَ "
    "الخانات ولا يقول أواوٌ في الجذر أم ياء؛ ومن قرأه هويّةً قرأ ما لم يُقَس"
)

MATCHING_IS_ON_THE_FULL_SKELETON_NEVER_ON_A_PREFIX: Final[str] = (
    "MatchingIsOnTheFullSkeletonNeverOnAPrefix: المطابقةُ على الهيكل الكامل؛ "
    "ومطابقةُ البادئة عطبٌ صحّحته المواصفةُ على نفسها، فلا تُعاد هنا"
)

THE_FOUR_CORPUS_COUNTS_ARE_NOT_ADOPTED: Final[str] = (
    "TheFourCorpusCountsAreNotAdopted: تُجمَّد قواعدُ العدّ لا أرقامُه؛ "
    "والأرقامُ الأربعةُ تبقى مُسجَّلةً في الإيداع بتعارضها وبفرق مجموعها، "
    "حتّى يُبنى بيانُ تشغيلٍ ويُكتَب توقّعٌ ثمّ يُنشَر ما خرج"
)

ENUMERATED_EXAMPLES_ARE_NOT_A_RULE: Final[str] = (
    "EnumeratedExamplesAreNotARule: أمثلةُ المعتلّ الستّةُ و«٤/٤» في فعل "
    "الأمر أمثلةٌ معدودةٌ غيرُ كلّيّة؛ ولا يُشحَن مثالٌ إجراءَ قرار"
)

THIS_IS_REGISTRATION_NOT_AUTHORITY: Final[str] = (
    "ThisIsRegistrationNotAuthority: تجميدٌ قبل القياس بلا حكمٍ ولا ولادةٍ "
    "ولا رفعِ حجبٍ عن طبقة `JARAD_ANALYSIS`"
)

JARAD_MAZID_PREREGISTRATION_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_SLOT_IS_A_REAL_CONSONANT_OR_A_MADD,
    ENUMERATED_EXAMPLES_ARE_NOT_A_RULE,
    LENGTH_ONLY_NEVER_THE_IDENTITY_OF_THE_WEAK_LETTER,
    MATCHING_IS_ON_THE_FULL_SKELETON_NEVER_ON_A_PREFIX,
    THE_FOUR_CORPUS_COUNTS_ARE_NOT_ADOPTED,
    THIS_IS_REGISTRATION_NOT_AUTHORITY,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""


def preregistration_digest() -> str:
    """بصمةُ المُجمَّد: يتغيّر بندٌ فيه فتتغيّر، فتسقط قراءةُ وحدة التصنيف."""

    registration = layer_registration()
    return canonical_digest(
        canonical_bytes(
            {
                "mujarrad_slot_count": MUJARRAD_SLOT_COUNT,
                "mazid_minimum_slots": MAZID_MINIMUM_SLOTS,
                "slot_definition": A_SLOT_IS_A_REAL_CONSONANT_OR_A_MADD,
                "permanent_limit": LENGTH_ONLY_NEVER_THE_IDENTITY_OF_THE_WEAK_LETTER,
                "matching_rule": MATCHING_IS_ON_THE_FULL_SKELETON_NEVER_ON_A_PREFIX,
                "corpus_bucket_rules": [
                    bucket.as_canonical_content() for bucket in CORPUS_BUCKET_RULES
                ],
                "publication_prerequisites": [
                    prerequisite.name for prerequisite in PUBLICATION_PREREQUISITES
                ],
                "root_table_sha256": root_table_reference(),
                "layer_entry_condition": registration.entry_condition,
                "layer_refusal_field_name": registration.refusal_field_name,
                "named_residuals": list(JARAD_MAZID_PREREGISTRATION_NAMED_RESIDUALS),
            }
        )
    )


PREREGISTRATION_DIGEST: Final[str] = preregistration_digest()
"""البصمةُ المُجمَّدة، محسوبةً عند الاستيراد لا مكتوبةً رقمًا في الشيفرة."""


def _refuse_an_incomplete_registration() -> None:
    """حارسٌ عند الاستيراد: الفئاتُ أربعٌ متمايزة، والشروطُ كلُّها لازمة."""

    names = [bucket.name for bucket in CORPUS_BUCKET_RULES]
    if len(set(names)) != len(names) or len(names) != 4:
        raise JaradMazidPreregistrationError("فئاتُ العدّ أربعٌ متمايزةٌ لا أقلّ")
    if len(PUBLICATION_PREREQUISITES) != len(PublicationPrerequisite):
        raise JaradMazidPreregistrationError(
            "شروطُ الإصدار كلُّها لازمةٌ مجتمعةً؛ ونقصُ واحدٍ منع لا تخفيض"
        )


_refuse_an_incomplete_registration()
