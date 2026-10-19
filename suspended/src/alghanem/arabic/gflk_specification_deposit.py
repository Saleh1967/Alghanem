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

`A_SUPERSEDED_VERSION_IS_RECORDED_NOT_ERASED`: وصلت المواصفةُ في نسختين،
والثانيةُ توسّع الأولى وتُقيّد بعضَ دعاويها. فتُودَع النسختان معًا، ويُسجَّل
لكلّ موضعٍ تغيّر ما قالته كلُّ نسخةٍ فيه وما تقرؤه الشجرةُ في التغيّر. وإيداعُ
المُوسَّع وحده يُخفي أنّ دعوًى أُطلِقت ثمّ قُيِّدت، فتُقرأ المواصفةُ بعد جلساتٍ
كأنّها لم تتغيّر — ويضيع أنفسُ ما فيها: مواضعُ التقييد.

`A_NUMBER_WITHOUT_A_CORPUS_IS_NOT_A_MEASUREMENT`: كلُّ رقمٍ لم تصل بايتاتُ
مصدره — عددَ كلماتٍ كان أو «6/6» — يُسجَّل غيرَ قابلٍ لإعادة الاشتقاق في هذه
الشجرة، بسببٍ مُسمًّى وشرطِ اشتقاقٍ مكتوب. فلم تصل مدوّنةٌ مُبصَّمةٌ لمسار
القياس، ولا `MeasurementRunManifest` (`arabic/encoding/measurement.py`)، ولا
سجلُّ رصدٍ يُطابَق عليه.

`A_REDERIVED_FIGURE_LEAVES_THE_WITHHELD_REGISTER`: وصلت بعدُ بايتاتُ
`maqayis_by_root_csv_999.csv` إلى الشجرة، فبُصِّمت وجُمِّدت في
`maqayis_root_table_deposit`، وأُعيد اشتقاقُ عددين كانا مُسجَّلين هنا
غيرَ قابلين له: ٤٬٥٧٦ سجلًّا و٤٬٠٨٧ جذرًا ثلاثيًّا متمايزًا. فينتقلان من
`GFLK_SPECIFICATION_NUMERIC_CLAIMS` إلى `REDERIVED_SPECIFICATION_FIGURES`
بقاعدةِ عدٍّ مُعلَنةٍ وقيمةٍ مفحوصةٍ في الاختبارات، ومعهما نصُّ **ما لا
يزالان لا يُثبتانه**: مطابقةُ عددٍ لا تُصدِّق الدعوى المبنيّةَ عليه. وأرقامُ
المدوّنة الأربعةُ باقيةٌ بحالها، إذ مسارُ قياسها ليس هذا الملفّ.

`AN_ENUMERATED_EXAMPLE_SWEEP_IS_NOT_A_UNIVERSAL`: «صفرُ انحرافٍ على 4/4» و«6/6
حالة مُختبَرة» عدُّ أمثلةٍ مُعدَّدةٍ لا عدُّ مجتمع؛ ومنزلتُهما منزلةُ
`EnumeratedExamplesAreNotAnExhaustiveCriterion` في `sentence_card_preregistration`
و`ONE_COUNTER_INSTANCE_DECIDES` في `lexical_path_census`، وكلاهما مكتوبٌ قبل
وصول النسخة الثانية. ودعوى العمومِ أثقلُ من النسبة لا أخفّ، إذ يكفي لنقضها
موضعٌ واحد.

`A_SUBMITTED_FREEZE_IS_NOT_A_FREEZE_HERE`: مُعرِّفُ تجميدٍ وصل من خارج الشجرة
يُحفَظ بحروفه ومعه حقلٌ يقول إنّه **غيرُ صادرٍ عنها**، على منوال
`SUBMITTED_FREEZE_IDENTIFIER` في `ibtida_wasl_waqf_registration`. والتسعةُ
المُسمَّاةُ في §٢-ب بصفر تطابقٍ في `src/` و`docs/` و`tests/`، فإعلانُ التجميد
في محادثةٍ خارجيّةٍ لا يُجمّد شيئًا هنا.

`NAMING_A_FREEZE_CHANGES_ITS_CHECKABILITY_NOT_ITS_STANDING`: قبل §٢-ب كان
المذكورُ «تسعةَ سجلّاتٍ مجمَّدة» بلا أسماء، فلم يكن يُمكن حتّى فحصُه بحثًا عن
تطابق؛ وبعده صارت التسعةُ تُفحَص فحصًا آليًّا. وهذا كسبٌ في **قابليّة الفحص**
لا في المنزلة: التسميةُ لا تُجمّد، والمنزلةُ بعد التسمية هي المنزلةُ قبلها —
وهو ما تقوله الرسالةُ الواردةُ نفسُها، فيُسجَّل اتّفاقًا لا تنازلًا.

`A_NAMED_SOURCE_IS_NOT_DEPOSITED_BYTES`: تسميةُ أصلِ المصدر — «معجم مقاييس
اللغة لابن فارس» — ليست بصمةَ ملفّ: نسخُ المعجم تختلف بايتًا، ومَن قاس على نسخةٍ
لم يَقِس على أخرى. فالمصدرُ المُسمَّى بلا بصمةٍ يُسجَّل مُسمًّى، ويبقى رقمُه غيرَ
قابلٍ لإعادة الاشتقاق. ويُرفَع ذلك بأحد وجهين لا ثالثَ لهما: بصمةٌ وصلت
**وطابقت** بصمةً مُجمَّدةً في هذه الشجرة سلفًا (`quran-simple-enhanced.txt`)،
أو بايتاتٌ وصلت بأعيانها فبُصِّمت هنا وصار يُطابَق عليها عند كلّ قراءة
(`maqayis_by_root_csv_999.csv` في `maqayis_root_table_deposit`). والمطابقةُ في
الوجهين مفحوصةٌ في الشيفرة لا مقروءةٌ بالعين. والوجهُ الأوّل يُثبت أنّ الإشارة
تقع على بايتاتٍ معروفةٍ هنا لا أنّ رقمًا قيس عليها؛ والثاني يجعل ما كان عدُّه
متعذّرًا معدودًا، ولا يجعل الدعوى المبنيّةَ على العدد مُصدَّقة.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا
تجميدَ `E0`، ولا استيرادَ من `kernel/`، ولا تقرأ هذه الوحدةَ وحدةٌ فيه. ولا
تُرفَع بها طبقةٌ محجوبة، ولا يُصدَر بها تصنيفُ مقطعٍ أو وزنٍ أو جذر؛ وليس فيها
حقلُ نتيجةٍ ولا حسم، وحارسٌ عند الاستيراد يمنع تسلُّلَهما لاحقًا.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, fields
from enum import Enum
from pathlib import Path
from typing import Final

from .compression_model_preregistration import FROZEN_CORPUS
from .maqayis_root_table_deposit import (
    FROZEN_ROOT_TABLE,
    REDERIVED_SPECIFICATION_FIGURES,
)
from .pipeline_stations import repository_root_path

__all__ = [
    "AN_ENUMERATED_EXAMPLE_SWEEP_IS_NOT_A_UNIVERSAL_NOTE",
    "A_NUMBER_WITHOUT_A_CORPUS_IS_NOT_A_MEASUREMENT_NOTE",
    "A_RECORDED_CONFLICT_IS_NOT_A_RESOLVED_ONE_NOTE",
    "A_SUBMITTED_FREEZE_IS_NOT_A_FREEZE_HERE_NOTE",
    "A_NAMED_SOURCE_IS_NOT_DEPOSITED_BYTES_NOTE",
    "A_REDERIVED_FIGURE_LEAVES_THE_WITHHELD_REGISTER_NOTE",
    "A_SUPERSEDED_VERSION_IS_RECORDED_NOT_ERASED_NOTE",
    "GFLK_SPECIFICATION_AMENDMENTS",
    "GFLK_SPECIFICATION_CONFLICTS",
    "GFLK_SPECIFICATION_DEPOSIT",
    "GFLK_SPECIFICATION_NUMERIC_CLAIMS",
    "NAMED_SOURCE_ATTRIBUTIONS",
    "NAMING_A_FREEZE_CHANGES_ITS_CHECKABILITY_NOT_ITS_STANDING_NOTE",
    "NOT_ISSUED_BY_THIS_TREE",
    "SPECIFICATION_RELATIVE_PATH",
    "SUBMITTED_FREEZE_IDENTIFIERS",
    "THE_DEPOSIT_IS_NOT_AN_ADOPTION_NOTE",
    "ConflictStanding",
    "GflkSpecificationConflict",
    "GflkSpecificationDeposit",
    "GflkSpecificationDepositError",
    "NamedSourceAttribution",
    "ProvenanceGenus",
    "SpecificationAmendment",
    "SpecificationNumericClaim",
    "SubmittedFreezeIdentifier",
    "read_specification_bytes",
    "specification_digest",
]

SPECIFICATION_RELATIVE_PATH: Final[str] = (
    "docs/reference/gflk_arabic_letter_specification.md"
)


class GflkSpecificationDepositError(ValueError):
    """رفضٌ عند الإنشاء: إيداعٌ ناقصٌ أو تعارضٌ بلا موضعٍ أو بلا شرطِ حسم."""


NOT_ISSUED_BY_THIS_TREE: Final[str] = (
    "مُعرِّفٌ لم تُصدِره هذه الشجرة ولا يوجد فيها: صفرُ تطابقٍ في `src/` و`docs/` "
    "و`tests/`؛ محفوظٌ بحروفه ليُراجَع لا ليُعمَل به"
)

_NO_CORPUS_REACHED_THIS_TREE: Final[str] = (
    "§٢-ب سمَّت المدوّنةَ ببصمةٍ تُطابق `FROZEN_CORPUS` هنا، والمطابقةُ مفحوصةٌ "
    "عند الاستيراد؛ لكنّ الاسمَ ليس القياس: لا `MeasurementRunManifest` يُجمّد "
    "صورةَ التطبيع وإصدارَ قاعدة Unicode لمسار القياس، ولا سجلُّ رصدٍ يُطابَق "
    "عليه. وقاعدةُ الجذور وصلت بعدُ وبُصِّمت في `maqayis_root_table_deposit`، "
    "وهي شرطٌ من شروط الاشتقاق لا كلُّها"
)

_REDERIVED_FIGURES: Final[frozenset[str]] = frozenset(
    entry.figure for entry in REDERIVED_SPECIFICATION_FIGURES
)
"""أرقامُ النصّ التي غادرت سجلَّ المتعذّر، مقروءةً من موضع اشتقاقها لا منسوخة."""

_REDERIVED_TRILATERAL_ROOT_FIGURE: Final[str] = "4,087"
"""رقمُ الجذور الثلاثيّة، ووجودُه في `_REDERIVED_FIGURES` مفحوصٌ عند الاستيراد."""

_REDERIVATION_CONDITION: Final[str] = (
    "`MeasurementRunManifest` لمسار القياس على البايتات المُبصَّمة، وسجلُّ "
    "رصدٍ يُطابَق عليه، وتوقّعٌ مكتوبٌ قبل القياس على منوال "
    "`OCP_PREREGISTERED_EXPECTATION`؛ وقاعدةُ الجذور المُبصَّمة تحقّقت في "
    "`maqayis_root_table_deposit` فلم تَعُد من الناقص"
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


@dataclass(frozen=True, slots=True)
class SpecificationAmendment:
    """موضعٌ تغيّر بين النسختين: ما قالته كلٌّ منهما، وما تقرؤه الشجرةُ في التغيّر.

    `A_SUPERSEDED_VERSION_IS_RECORDED_NOT_ERASED`: التغيّرُ حدثٌ يُسجَّل بنصّه؛
    وقراءةُ الشجرة للتغيّر ليست حسمًا للتعارض القائم في الموضع نفسه.
    """

    locus: str
    first_version_said: str
    second_version_says: str
    what_this_tree_reads_in_the_change: str

    def __post_init__(self) -> None:
        for field_name in (
            "locus",
            "first_version_said",
            "second_version_says",
            "what_this_tree_reads_in_the_change",
        ):
            if not str(getattr(self, field_name)).strip():
                raise GflkSpecificationDepositError(
                    "موضعُ تغيّرٍ بلا نصِّ النسختين أو بلا قراءةٍ للتغيّر يُقرأ "
                    "بعد جلساتٍ كأنّ شيئًا لم يتغيّر؛ والتغيّرُ حدثٌ يُسجَّل"
                )


@dataclass(frozen=True, slots=True)
class SpecificationNumericClaim:
    """رقمٌ ورد في المواصفة: نصُّه، وسببُ تعذّر اشتقاقه، وشرطُ اشتقاقه.

    `A_DEPENDENT_FIGURE_IS_NOT_A_SECOND_WITNESS`: رقمٌ يقوم على رقمٍ آخرَ في
    الوثيقة نفسِها يُسمّيه في `depends_on_figure`، فلا يُقرأ الاثنان شاهدين
    مستقلّين. ورقمٌ فئتُه مُعرَّفةٌ بالباقي (`is_residue_defined`) لا يُقبَل بلا
    وسمِ تبعيّةٍ يُسمّي ما يقوم عليه.
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
                raise GflkSpecificationDepositError(
                    "رقمٌ بلا سببِ تعذّرٍ أو بلا شرطِ اشتقاقٍ يُقرأ مقيسًا في "
                    "هذه الشجرة، وهو ما لم يقع"
                )
        if self.depends_on_figure is not None and not self.depends_on_figure.strip():
            raise GflkSpecificationDepositError(
                "وسمُ التبعيّة يُسمّي الرقمَ المُعتمَدَ عليه بنصّه؛ ووسمٌ فارغٌ "
                "يُخفي التبعيّةَ ولا يُسجّلها"
            )
        if self.is_residue_defined and self.depends_on_figure is None:
            raise GflkSpecificationDepositError(
                "رقمٌ فئتُه مُعرَّفةٌ بالباقي لا يُسجَّل بلا وسمِ تبعيّةٍ يُسمّي "
                "ما يقوم عليه: فئةٌ عُرِّفت بأنّها «ما لم يُطابِق» تتحرّك بحركة "
                "ما طابَق، فليست شاهدًا مستقلًّا عنه"
            )


@dataclass(frozen=True, slots=True)
class NamedSourceAttribution:
    """مصدرٌ سُمّي في §٢-ب: ما هو، وكيف وصل هناك، وبصمتُه هنا إن وُجدت.

    `A_NAMED_SOURCE_IS_NOT_DEPOSITED_BYTES`: الاسمُ ليس البايتات. و
    `digest_in_this_tree` لا يُملأ إلّا ببصمةٍ **مُجمَّدةٍ في هذه الشجرة سلفًا**
    تُقرأ من موضعها لا تُنسَخ رقمًا، ووجودُها لا يعني أنّ رقمًا قيس عليها.
    """

    source_name: str
    what_it_is: str
    how_it_reached_the_other_conversation: str
    what_is_still_missing: str
    digest_in_this_tree: str | None = None

    def __post_init__(self) -> None:
        for field_name in (
            "source_name",
            "what_it_is",
            "how_it_reached_the_other_conversation",
            "what_is_still_missing",
        ):
            if not str(getattr(self, field_name)).strip():
                raise GflkSpecificationDepositError(
                    "مصدرٌ مُسمًّى بلا بيانِ ما بقي ناقصًا يُقرأ بعد جلساتٍ مصدرًا "
                    "مُودَعًا، والتسميةُ ليست إيداعًا"
                )
        digest = self.digest_in_this_tree
        if digest is None:
            return
        if len(digest) != 64 or any(
            character not in "0123456789abcdef" for character in digest
        ):
            raise GflkSpecificationDepositError(
                "بصمةُ مصدرٍ تُسجَّل كاملةً بالنظام السادس عشر الصغير (64 خانة)؛ "
                "و«3763...6c5a» طرفان لا بصمة، ولا يُطابَق عليهما"
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
                raise GflkSpecificationDepositError(
                    "مُعرِّفُ تجميدٍ وارد بلا حقلٍ يقول إنّه غيرُ صادرٍ عن هذه "
                    "الشجرة يُقرأ بعد جلساتٍ تجميدًا فيها؛ والوسمُ لازمٌ لا زينة"
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
    """الإيداع: جنسُ المصدر، وتاريخُ الوصول، وموضعُ النصّ، وعددُ النسخ المُودَعة."""

    genus: ProvenanceGenus
    arrival_date: str
    relative_path: str
    deposited_versions: int = 2
    deposited_follow_up_messages: int = 1

    def __post_init__(self) -> None:
        if not self.arrival_date.strip() or not self.relative_path.strip():
            raise GflkSpecificationDepositError("إيداعٌ بلا تاريخِ وصولٍ أو بلا موضع")
        if self.deposited_versions != 2:
            raise GflkSpecificationDepositError(
                "النسختان تُودَعان معًا؛ وإيداعُ المُوسَّعة وحدها يمحو أنّ دعوًى "
                "أُطلِقت ثمّ قُيِّدت"
            )
        if self.deposited_follow_up_messages != 1:
            raise GflkSpecificationDepositError(
                "رسالةُ التسمية اللاحقةُ تُعَدّ نصًّا لاحقًا لا نسخةً ثالثة؛ "
                "وعدُّها نسخةً يجعل التسميةَ تعديلًا للمواصفة وهي ليست كذلك"
            )

    def digest(self, root: Path | None = None) -> str:
        """بصمةُ الوثيقة الآن، تُقرأ من الملفّ في كلّ نداء."""

        return specification_digest(root)


GFLK_SPECIFICATION_DEPOSIT: Final[GflkSpecificationDeposit] = GflkSpecificationDeposit(
    genus=ProvenanceGenus.PROSE_FROM_ANOTHER_CONVERSATION,
    arrival_date="2026-09-15",
    relative_path=SPECIFICATION_RELATIVE_PATH,
    deposited_versions=2,
    deposited_follow_up_messages=1,
)


SUBMITTED_FREEZE_IDENTIFIERS: Final[tuple[SubmittedFreezeIdentifier, ...]] = (
    SubmittedFreezeIdentifier(
        identifier="JARAD-MAZID-CORRECTED-AR-1",
        what_it_declares=(
            "تجميدٌ يُعلن تصحيحَ معيار مجرد/مزيد بمطابقة الهيكل الساكن الكامل "
            "على قاعدة جذورٍ مُسمَّاة، وأنّ الخانة الجذريّة صامتٌ حقيقيٌّ ومدّ"
        ),
        not_issued_by_this_tree=NOT_ISSUED_BY_THIS_TREE,
    ),
    SubmittedFreezeIdentifier(
        identifier="FI'L-AMR-SYLLABLE-SIGNATURE-AR-1",
        what_it_declares=(
            "تجميدٌ يُعلن لفعل الأمر بصمةً صوتيّةً موحَّدة: وزن CVC-CVC وسكونٌ "
            "ختاميٌّ صريح، بصفر انحرافٍ على أربعة أمثلة"
        ),
        not_issued_by_this_tree=NOT_ISSUED_BY_THIS_TREE,
    ),
    SubmittedFreezeIdentifier(
        identifier="MUDARI-WEAK-RADICAL-IDENTITY-AR-1",
        what_it_declares=(
            "تجميدٌ يُعلن حسمَ هويّة حرف العلّة من صيغة المضارع: ضمّةٌ قبل المدّ "
            "تدلّ على الواو، وكسرةٌ على الياء"
        ),
        not_issued_by_this_tree=NOT_ISSUED_BY_THIS_TREE,
    ),
    SubmittedFreezeIdentifier(
        identifier="LUZUM-TA'ADDI-STRUCTURAL-TOOL-AR-1",
        what_it_declares=(
            "تجميدٌ يُعلن أداةً بنيويّةً للتعدّي: وجودُ مبنيٍّ للمجهول يستلزم "
            "متعدّيًا حقيقيًّا، استلزامًا أحاديَّ الاتجاه"
        ),
        not_issued_by_this_tree=NOT_ISSUED_BY_THIS_TREE,
    ),
    SubmittedFreezeIdentifier(
        identifier="FI'L-FOUR-DIMENSIONS-AR-1",
        what_it_declares=(
            "تجميدٌ يُعلن للفعل أربعةَ أبعادٍ مُميِّزة، سُمّي في §٢-ب ولم يَرِد "
            "نصُّه ولا مسطرةُ قياسه"
        ),
        not_issued_by_this_tree=NOT_ISSUED_BY_THIS_TREE,
    ),
    SubmittedFreezeIdentifier(
        identifier="FI'L-LAZIM-MAJHUL-FOUR-DIMENSIONS-AR-1",
        what_it_declares=(
            "تجميدٌ يُعلن الأبعادَ الأربعةَ نفسَها للّازم والمبنيِّ للمجهول، "
            "سُمّي في §٢-ب ولم يَرِد نصُّه"
        ),
        not_issued_by_this_tree=NOT_ISSUED_BY_THIS_TREE,
    ),
    SubmittedFreezeIdentifier(
        identifier="MASDAR-SYLLABLE-LOGIC-AR-1",
        what_it_declares=(
            "تجميدٌ يُعلن منطقًا مقطعيًّا للمصدر يفصل السماعيَّ عن القياسيّ، "
            "سُمّي في §٢-ب ولم يَرِد نصُّه"
        ),
        not_issued_by_this_tree=NOT_ISSUED_BY_THIS_TREE,
    ),
    SubmittedFreezeIdentifier(
        identifier="SAMA'I-SYLLABLE-RELATIONS-AR-1",
        what_it_declares=(
            "تجميدٌ يُعلن علاقاتٍ ثلاثًا بين مقاطع المصدر السماعيّ (تجاورٌ "
            "وتخطٍّ)، سُمّي في §٢-ب ولم يَرِد نصُّه"
        ),
        not_issued_by_this_tree=NOT_ISSUED_BY_THIS_TREE,
    ),
    SubmittedFreezeIdentifier(
        identifier="MAZID-VERB-SYLLABLE-LOGIC-AR-1",
        what_it_declares=(
            "تجميدٌ يُعلن منطقًا مقطعيًّا لأوزان المزيد: تحوّلُ عينِ الفعل "
            "CV←CVV، سُمّي في §٢-ب ولم يَرِد نصُّه"
        ),
        not_issued_by_this_tree=NOT_ISSUED_BY_THIS_TREE,
    ),
)


NAMED_SOURCE_ATTRIBUTIONS: Final[tuple[NamedSourceAttribution, ...]] = (
    NamedSourceAttribution(
        source_name="quran-simple-enhanced.txt",
        what_it_is=(
            "المدوّنةُ التي تقول §٢-ب إنّ أعدادَ الضغط والصرف قيست عليها، "
            "مذكورةً ببصمةٍ مُختصَرةٍ طرفاها «3763» و«6c5a»"
        ),
        how_it_reached_the_other_conversation=(
            "لم يُذكَر؛ والمذكورُ أنّ بصمتَها «مُسجَّلةٌ سابقًا في الإيداع الأوّل»"
        ),
        what_is_still_missing=(
            "أنّ البصمةَ تقع على بايتاتٍ مُجمَّدةٍ هنا لا يعني أنّ رقمًا قيس "
            "عليها: لا `MeasurementRunManifest` لمسار القياس، ولا سجلَّ رصدٍ "
            "يُطابَق عليه، ولا توقّعٌ مكتوبٌ قبل القياس"
        ),
        digest_in_this_tree=FROZEN_CORPUS.sha256_hex,
    ),
    NamedSourceAttribution(
        source_name="maqayis_by_root_csv_999.csv",
        what_it_is=(
            "ملفُّ الجذور الذي تقول §٢-ب إنّ عددَي ٤٬٥٧٦ سجلًّا و٤٬٠٨٧ جذرًا "
            "ثلاثيًّا مأخوذان منه، وأصلُه «معجم مقاييس اللغة لابن فارس»"
        ),
        how_it_reached_the_other_conversation=(
            "رفعَه المستخدمُ مباشرةً في تلك المحادثة، بنصِّ §٢-ب؛ ثمّ رفعَه إلى "
            "هذه الشجرة بأعيان بايتاته، فبُصِّم فيها"
        ),
        what_is_still_missing=(
            "أنّ هذه النسخةَ هي التي قيس عليها هناك: البصمةُ الآن مُجمَّدةٌ في "
            "`maqayis_root_table_deposit` ويُطابَق عليها عند كلّ قراءة، لكنّ "
            "النصَّ الواردَ لم يذكر بصمةً تُقابَل بها، ونسخُ المعجم تختلف "
            "بايتًا. والعددان صارا مُعادَي الاشتقاق هنا، وهذا عدٌّ لا تصديق"
        ),
        digest_in_this_tree=FROZEN_ROOT_TABLE.sha256_hex,
    ),
)


GFLK_SPECIFICATION_AMENDMENTS: Final[tuple[SpecificationAmendment, ...]] = (
    SpecificationAmendment(
        locus="§٣ — إطباق ⊆ استعلاء",
        first_version_said="«علاقةُ احتواءٍ مُثبَتةٌ تحليليًّا (لا إحصائيًّا)» بإطلاق",
        second_version_says=(
            "«تحليليًّا **بالنسبة للتعريف التقليدي المُعلَن**، لا تحليليًّا "
            "بإطلاق»، ونصُّ التعريف مذكورٌ: «استعلاء + التصاق حاصر» (جنس+فصل)"
        ),
        what_this_tree_reads_in_the_change=(
            "تقييدٌ يوافق نصًّا ما كان مكتوبًا في الشجرة قبل وصوله: "
            "`AN_ANALYTIC_TRUTH_IS_NOT_A_DISCOVERY` و`AnalyticRegistration."
            "definition_text` في `gflk_feature_table_import_barrier`. وموافقةُ "
            "نصٍّ واردٍ لشرطٍ قائمٍ تُسجَّل ولا تُقرأ حسمًا للتعارض المُسجَّل في "
            "الموضع نفسه: الحسمُ ليس من شأن الإيداع"
        ),
    ),
    SpecificationAmendment(
        locus="عمومُ ألفاظ «تحليلي» و«برهان» و«يقين منطقي»",
        first_version_said="مُستعمَلةٌ بلا قيدٍ مُعلَن",
        second_version_says=(
            "مقروءةٌ كلُّها بالتحفّظ نفسِه: تحليليّةٌ بالنسبة للتعريف المُعلَن "
            "لا بإطلاق — ومنها ثنائيّةُ PASS/FAIL في §١، وشرطُ بدء المقطع "
            "بصامتٍ متحرّكٍ في §٥"
        ),
        what_this_tree_reads_in_the_change=(
            "تقييدٌ جنسيٌّ لا درجيّ: دعوى اليقين صارت مشروطةً بتعريفها. ولا "
            "يرفع هذا حجبًا عن طبقةٍ محجوبة، ولا يُحوّل رقمًا غيرَ مُبصَّمٍ إلى "
            "مقيس"
        ),
    ),
    SpecificationAmendment(
        locus="§٣ — الألف والتاء المربوطة",
        first_version_said="غيرُ واردتين في جداول الصفة والمخرج",
        second_version_says=(
            "الألفُ «العنصر السابع عشر المحايد»: N/A على المحاور الأربعة معًا، "
            "ومحايدةٌ معلوماتيًّا في ثلاثةٍ من أربعة أدوارٍ لا في الرابع (حاملة "
            "التنوين)؛ والتاءُ المربوطة مُستبعَدةٌ اصطلاحيًّا لا حيادًا"
        ),
        what_this_tree_reads_in_the_change=(
            "إضافةٌ تستلزم فرزَ أدوار الألف الأربعة، وفيها همزةُ الوصل — وهي "
            "`HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS` في "
            "`ibtida_wasl_waqf_registration`. وقراءةُ `p_extractor` تفرز من "
            "الأربعة ثلاثةً: حاملةَ التنوين، وحرفَ المدّ، والألفَ الفارقة؛ "
            "وتبقى همزةُ الوصل وحدَها متعذّرةً، فتبقى الدعوى المعلوماتيّةُ — "
            "وهي على الأدوار الأربعة معًا — غيرَ قابلةٍ للاختبار هنا "
            "(`alif_neutrality_registration`)"
        ),
    ),
    SpecificationAmendment(
        locus="مجرد/مزيد — `JARAD-MAZID-CORRECTED-AR-1`",
        first_version_said="غيرُ واردٍ في المواصفة أصلًا",
        second_version_says=(
            "معيارٌ مُصحَّحٌ بمطابقة الهيكل الساكن الكامل على 4,087 جذرًا، بأربعة "
            "أعدادٍ على المدوّنة، وبخانةٍ جذريّةٍ = صامتٌ حقيقيٌّ + مدّ تفصل "
            "المزيدَ عن المجرّد في 6/6"
        ),
        what_this_tree_reads_in_the_change=(
            "إضافةٌ بلا مدوّنةٍ واصلة: الطبقةُ `JARAD_ANALYSIS` محجوبةٌ في "
            "`word_structure_dictionary` ومنزلتُها `HYPOTHESIS_WITH_A_DECLARED_"
            "DEFECT`، وملفُّ الجذور المُسمَّى غيرُ موجودٍ في الشجرة ولا بصمةَ له"
        ),
    ),
    SpecificationAmendment(
        locus="فعل الأمر — `FI'L-AMR-SYLLABLE-SIGNATURE-AR-1`",
        first_version_said="غيرُ واردٍ في المواصفة أصلًا",
        second_version_says=(
            "وزنٌ موحَّدٌ CVC-CVC وسكونٌ ختاميٌّ صريح، بصفر انحرافٍ على 4/4 "
            "أمثلة، وحدٌّ مفتوحٌ واحدٌ مُعلَن: تصادمُه مع أسماءٍ مماثلة الوزن"
        ),
        what_this_tree_reads_in_the_change=(
            "إضافةٌ تصطدم بثلاثة حواجزَ قائمةٍ قبل وصولها، والحدُّ المُعلَن فيها "
            "أضيقُ منها: المقطعُ محجوب، وهمزةُ الوصل في «اُكْتُبْ» متعذّرة، "
            "والسكونُ الختاميُّ غيرُ مُميَّزٍ وقفًا من وصلٍ "
            "(`PAUSAL_SUKUN_IS_NOT_DISTINGUISHED_FROM_CONNECTED_SUKUN`)"
        ),
    ),
    SpecificationAmendment(
        locus="متعدٍّ/لازم — البناء الهرميّ التاسع",
        first_version_said="غيرُ واردٍ في المواصفة أصلًا",
        second_version_says=(
            "تسعةُ مستوياتٍ متتاليةٍ «كلٌّ منها مجمَّدٌ بسجلّه الخاصّ»، تُختَم "
            "بـ«وجود مبنيٍّ للمجهول ⟹ متعدٍّ حقيقي»"
        ),
        what_this_tree_reads_in_the_change=(
            "إضافةٌ تُحيل إلى سجلّاتٍ مجمَّدةٍ لا وجودَ لها هنا: أربعةُ "
            "مُعرِّفاتٍ مُسجَّلةٌ في `SUBMITTED_FREEZE_IDENTIFIERS` بصفر تطابق. "
            "ومسارُ المفعوليّة الوحيدُ في الشجرة مقيسٌ على مدوّنةٍ صحفيّةٍ "
            "بحدودٍ مكتوبة (`ud_objecthood_measurement`، `ACCUSATIVE_IS_NOT_"
            "OBJECTHOOD`)، ولا يقرأ مبنيًّا للمجهول أصلًا"
        ),
    ),
    SpecificationAmendment(
        locus="§٦ — أرقام الضغط",
        first_version_said="85.11٪ و87.67٪ و88.01٪ و88.34٪ بسجلّ تصحيحاتها",
        second_version_says="الأرقامُ نفسُها بلا تغييرٍ في قيمةٍ ولا في سندٍ",
        what_this_tree_reads_in_the_change=(
            "رقمٌ تكرّر في نسختين من المصدر نفسِه ليس شاهدين: منزلتُه في الشجرة "
            "كما كانت في `compression_model_revision_audit`، والتعارضُ المُسجَّل "
            "عليه قائمٌ بحاله"
        ),
    ),
)


GFLK_SPECIFICATION_NUMERIC_CLAIMS: Final[tuple[SpecificationNumericClaim, ...]] = (
    SpecificationNumericClaim(
        figure="10,599",
        locus="§٢-أ — نتيجةٌ أوّليّةٌ على المدوّنة",
        claim_text="«مجرد مؤكَّد=10,599»",
        not_rederivable_because=_NO_CORPUS_REACHED_THIS_TREE,
        what_would_make_it_rederivable=_REDERIVATION_CONDITION,
        depends_on_figure=_REDERIVED_TRILATERAL_ROOT_FIGURE,
    ),
    SpecificationNumericClaim(
        figure="11,467",
        locus="§٢-أ — نتيجةٌ أوّليّةٌ على المدوّنة",
        claim_text="«غير مؤكَّد (٣ أحرف، لا يطابق جذرًا مُبصَّمًا)=11,467»",
        not_rederivable_because=(
            f"{_NO_CORPUS_REACHED_THIS_TREE}؛ والفئةُ مُعرَّفةٌ سلبًا بعدم "
            "المطابقة، فعددُها دالّةٌ في قاعدة الجذور لا في العربية"
        ),
        what_would_make_it_rederivable=_REDERIVATION_CONDITION,
        depends_on_figure=_REDERIVED_TRILATERAL_ROOT_FIGURE,
        is_residue_defined=True,
    ),
    SpecificationNumericClaim(
        figure="37,682",
        locus="§٢-أ — نتيجةٌ أوّليّةٌ على المدوّنة",
        claim_text="«مزيد محتمل (>٣ أحرف صامتة)=37,682»",
        not_rederivable_because=(
            f"{_NO_CORPUS_REACHED_THIS_TREE}؛ وعدُّ الصوامت يستلزم فرزَ الصامت "
            "من المدّ، وهو ما تحجبه `SYLLABLES_AND_WAZN`"
        ),
        what_would_make_it_rederivable=_REDERIVATION_CONDITION,
    ),
    SpecificationNumericClaim(
        figure="18,333",
        locus="§٢-أ — نتيجةٌ أوّليّةٌ على المدوّنة",
        claim_text="«غير محدَّد (<٣)=18,333»",
        not_rederivable_because=_NO_CORPUS_REACHED_THIS_TREE,
        what_would_make_it_rederivable=_REDERIVATION_CONDITION,
    ),
    SpecificationNumericClaim(
        figure="6/6",
        locus="§٢-أ — الخانة الجذريّة = صامتٌ حقيقيٌّ + مدّ",
        claim_text=(
            "«3 خانات=مجرد حتمًا (يشمل بلا استثناء: سالم كَتَبَ، أجوف قَالَ، "
            "ناقص واوي دَعَا، ناقص يائي رَمَى، لفيف وَقَى/وَفَى — 6/6 حالة "
            "مُختبَرة بنجاح)»"
        ),
        not_rederivable_because=(
            "أمثلةٌ مُعدَّدةٌ ستٌّ لا مجتمعٌ مُعرَّف، و«بلا استثناء» دعوى عمومٍ "
            "لا تُقاس على ستّة؛ ولم تصل مدوّنةٌ يُعَدّ فيها المخالف"
        ),
        what_would_make_it_rederivable=_REDERIVATION_CONDITION,
    ),
    SpecificationNumericClaim(
        figure="4/4",
        locus="§٢-أ — `FI'L-AMR-SYLLABLE-SIGNATURE-AR-1`",
        claim_text="«مُختبَر بصفر انحراف على 4/4 أمثلة (اُكْتُبْ، اِضْرِبْ، اِذْهَبْ، اُنْظُرْ)»",
        not_rederivable_because=(
            "أربعةُ أمثلةٍ مُعدَّدةٍ لا مجتمع؛ و«صفرُ انحراف» دعوى عمومٍ يكفي "
            "لنقضها موضعٌ واحدٌ خارجها. ومقطعةُ الأمثلة نفسِها متعذّرةٌ هنا: "
            "همزةُ الوصل غيرُ مُميَّزة، والسكونُ الختاميُّ غيرُ مفروزٍ وقفًا من وصل"
        ),
        what_would_make_it_rederivable=_REDERIVATION_CONDITION,
    ),
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
    GflkSpecificationConflict(
        locus_in_specification="§٢-أ — فعل الأمر: وزن CVC-CVC وسكونٌ ختاميٌّ صريح",
        specification_says=(
            "بصمةٌ صوتيّةٌ موحَّدةٌ لفعل الأمر، مُختبَرةٌ بصفر انحرافٍ على أربعة "
            "أمثلةٍ تبدأ كلُّها بهمزة وصلٍ وتُختَم بسكون"
        ),
        this_tree_says=(
            "الوزنُ والمقطعُ محجوبان (`DictionaryLayer.SYLLABLES_AND_WAZN`)، "
            "وهمزةُ الوصل غيرُ مُميَّزةٍ من العلامات المكتوبة، والسكونُ الختاميُّ "
            "غيرُ مفروزٍ وقفًا من وصلٍ — فالحدّان اللذان تقوم عليهما البصمةُ "
            "كلاهما متعذّرٌ هنا قبل وصول النصّ"
        ),
        tree_reference=(
            "`HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS` في "
            "`ibtida_wasl_waqf_registration`، و"
            "`PAUSAL_SUKUN_IS_NOT_DISTINGUISHED_FROM_CONNECTED_SUKUN` في "
            "`encoding/sakin_adjacency`، وحجبُ الطبقة في "
            "`word_structure_dictionary`"
        ),
        what_would_resolve_it=(
            "رفعُ الحجب عن طبقة المقطع بشرطها المكتوب في "
            "`DICTIONARY_LAYER_REGISTRATIONS`، ومقياسٌ يفرز همزةَ الوصل والسكونَ "
            "الوقفيَّ من غيرهما؛ ثمّ عدُّ المخالف على مدوّنةٍ مُبصَّمةٍ لا على "
            "أربعة أمثلة"
        ),
        standing=ConflictStanding.BLOCKS_IMPORT_UNTIL_RESOLVED,
    ),
    GflkSpecificationConflict(
        locus_in_specification="§٢-أ — «وجود مبنيٍّ للمجهول ⟹ متعدٍّ حقيقي»",
        specification_says=(
            "أداةٌ بنيويّةٌ للتعدّي باسم `LUZUM-TA'ADDI-STRUCTURAL-TOOL-AR-1`، "
            "خاتمةُ بناءٍ من تسعة مستوياتٍ «كلٌّ منها مجمَّدٌ بسجلّه الخاصّ»"
        ),
        this_tree_says=(
            "المفعوليّةُ مقيسةٌ هنا على طبقة علاقات UD في مدوّنةٍ صحفيّةٍ لا "
            "قرآنيّة، و`obj` فيها مفعوليّةُ UD لا المفعولُ به الكلاسيكيّ، "
            "والحالةُ ليست الوظيفة؛ ولا تُقرأ في الشجرة صيغةُ مجهولٍ أصلًا"
        ),
        tree_reference=(
            "`ACCUSATIVE_IS_NOT_OBJECTHOOD` في `irab_case_readout`، و"
            "`OBJ_IS_UD_OBJECTHOOD_NOT_CLASSICAL_MAFUL` و"
            "`REGISTER_IS_NEWSWIRE_NOT_QURANIC` في `ud_objecthood_preregistration`"
        ),
        what_would_resolve_it=(
            "تسجيلٌ قَبْليٌّ يُعرّف كاشفَ المجهول من العلامات المكتوبة وحدها، "
            "ومدوّنةٌ مُبصَّمةٌ يُقاس عليها، وتوقّعٌ مكتوبٌ قبل القياس؛ والاستلزامُ "
            "أحاديُّ الاتجاه يبقى أحاديًّا: غيابُ المجهول لا يُثبت اللزوم"
        ),
        standing=ConflictStanding.BLOCKS_IMPORT_UNTIL_RESOLVED,
    ),
    GflkSpecificationConflict(
        locus_in_specification="§٢-أ — أربعةُ مُعرِّفات تجميدٍ واردة",
        specification_says=(
            "تسعةُ مستوياتٍ «كلٌّ منها مجمَّدٌ بسجلّه الخاصّ»، ويُسمّي منها أربعةَ "
            "مُعرِّفاتٍ بأسمائها"
        ),
        this_tree_says=(
            "المُعرِّفاتُ الأربعةُ بصفر تطابقٍ في `src/` و`docs/` و`tests/`؛ فما "
            "جُمِّد جُمِّد في موضعٍ آخر، وإعلانُ التجميد في محادثةٍ خارجيّةٍ لا "
            "يُجمّد شيئًا هنا"
        ),
        tree_reference=(
            "`SUBMITTED_FREEZE_IDENTIFIERS` في هذه الوحدة، على منوال "
            "`SUBMITTED_FREEZE_IDENTIFIER` في `ibtida_wasl_waqf_registration`"
        ),
        what_would_resolve_it=(
            "وصولُ نصّ كلّ سجلٍّ مُجمَّدٍ ببايتاته ومدوّنته، فيُودَع كلٌّ منها "
            "على حدة؛ ولا يُقرأ اسمُ تجميدٍ سندًا لمضمونه"
        ),
        standing=ConflictStanding.RECORDED_UNRESOLVED,
    ),
    GflkSpecificationConflict(
        locus_in_specification="§٢-أ — الألف «العنصر السابع عشر المحايد»",
        specification_says=(
            "حيادٌ تامٌّ صفاتيًّا على المحاور الأربعة، وحيادٌ معلوماتيٌّ في ثلاثةٍ "
            "من أربعة أدوارٍ وظيفيّةٍ للألف"
        ),
        this_tree_says=(
            "فرزُ أدوار الألف الأربعة غيرُ ممكنٍ من العلامات المكتوبة: همزةُ "
            "الوصل متعذّرة، والدورُ الوحيدُ المقروءُ هنا حاملُ التنوين على "
            "الوحدة القائمة؛ فالقسمةُ الرباعيّةُ مُدخَلٌ لا مخرج"
        ),
        tree_reference=(
            "`HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS`، و"
            "`DictionaryLayer.TANWEEN_ANALYSIS` دورًا على `tanwin_alif_seat`"
        ),
        what_would_resolve_it=(
            "مقياسٌ يفرز الأدوارَ الأربعةَ من العلامات وحدها، أو التصريحُ بأنّ "
            "القسمةَ مأخوذةٌ من تحليلٍ نحويٍّ سابقٍ لا مقروءةٌ من النصّ"
        ),
        standing=ConflictStanding.RECORDED_UNRESOLVED,
    ),
    GflkSpecificationConflict(
        locus_in_specification="§٢-أ — أعدادُ مجرد/مزيد الأربعة",
        specification_says=(
            "«مجرد مؤكَّد=10,599؛ غير مؤكَّد=11,467؛ مزيد محتمل=37,682؛ غير "
            "محدَّد=18,333» على مدوّنةٍ وقاعدةِ جذورٍ مُسمَّاة"
        ),
        this_tree_says=(
            "الطبقةُ `JARAD_ANALYSIS` محجوبةٌ ومنزلتُها فرضٌ مُعلَنُ العطب، ولا "
            "ملفَّ الجذور في الشجرة ولا بصمةَ له؛ وفئةُ «غير المؤكَّد» مُعرَّفةٌ "
            "بعدم المطابقة فتتحرّك بحركة القاعدة لا بحركة اللغة"
        ),
        tree_reference=(
            "`word_structure_dictionary.WITHHELD_LAYERS`، و"
            "`SpecificationNumericClaim.is_residue_defined` في هذه الوحدة"
        ),
        what_would_resolve_it=(
            "إيداعُ بايتات قاعدة الجذور والمدوّنة مُبصَّمتين، و"
            "`MeasurementRunManifest` لمسار القياس، وتوقّعٌ مكتوبٌ قبل القياس؛ "
            "وعندها يصير العدُّ سكربتَ اشتقاقٍ في `examples/reference/` لا نصًّا يُقرأ"
        ),
        standing=ConflictStanding.BLOCKS_IMPORT_UNTIL_RESOLVED,
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


A_SUPERSEDED_VERSION_IS_RECORDED_NOT_ERASED_NOTE: Final[str] = (
    "ASupersededVersionIsRecordedNotErased: النسختان تُودَعان معًا، ولكلّ موضعٍ "
    "تغيّر نصُّ النسختين فيه وقراءةُ الشجرة للتغيّر؛ وإيداعُ المُوسَّعة وحدها "
    "يمحو أنّ دعوًى أُطلِقت ثمّ قُيِّدت"
)

A_NUMBER_WITHOUT_A_CORPUS_IS_NOT_A_MEASUREMENT_NOTE: Final[str] = (
    "ANumberWithoutACorpusIsNotAMeasurement: كلُّ رقمٍ بقي في "
    "`GFLK_SPECIFICATION_NUMERIC_CLAIMS` غيرُ قابلٍ لإعادة الاشتقاق بسببٍ "
    "مُسمًّى؛ ومسارُ قياسه على المدوّنة بلا `MeasurementRunManifest` ولا سجلِّ "
    "رصدٍ يُطابَق عليه ولا توقّعٍ مكتوبٍ قبل القياس"
)

A_REDERIVED_FIGURE_LEAVES_THE_WITHHELD_REGISTER_NOTE: Final[str] = (
    "ARederivedFigureLeavesTheWithheldRegister: وصلت بايتاتُ "
    "`maqayis_by_root_csv_999.csv` فبُصِّمت في `maqayis_root_table_deposit`، "
    "فغادر ٤٬٥٧٦ و٤٬٠٨٧ سجلَّ المتعذّر إلى `REDERIVED_SPECIFICATION_FIGURES` "
    "بقاعدتَي عدٍّ مُعلَنتين؛ ومطابقةُ العدد عدٌّ لا تصديقٌ لدعوى، وأرقامُ "
    "المدوّنة الأربعةُ باقيةٌ بحالها"
)

AN_ENUMERATED_EXAMPLE_SWEEP_IS_NOT_A_UNIVERSAL_NOTE: Final[str] = (
    "AnEnumeratedExampleSweepIsNotAUniversal: «4/4» و«6/6» عدُّ أمثلةٍ لا عدُّ "
    "مجتمع، و«بلا استثناء» دعوى عمومٍ يكفي لنقضها موضعٌ واحدٌ خارج الأمثلة"
)

A_SUBMITTED_FREEZE_IS_NOT_A_FREEZE_HERE_NOTE: Final[str] = (
    "ASubmittedFreezeIsNotAFreezeHere: المُعرِّفاتُ التسعةُ محفوظةٌ بحروفها ومعها "
    "`NOT_ISSUED_BY_THIS_TREE`؛ واسمُ التجميد ليس سندًا لمضمونه، ولا يُقرأ "
    "إعلانُ التجميد في محادثةٍ خارجيّةٍ تجميدًا في هذه الشجرة"
)

NAMING_A_FREEZE_CHANGES_ITS_CHECKABILITY_NOT_ITS_STANDING_NOTE: Final[str] = (
    "NamingAFreezeChangesItsCheckabilityNotItsStanding: «تسعةُ سجلّاتٍ مجمَّدة» "
    "بلا أسماءٍ لم تكن تُفحَص أصلًا؛ وبعد تسميتِها في §٢-ب فُحِصت التسعةُ في "
    "`src/` و`docs/` و`tests/` بصفر تطابقٍ خارج مواضع تسجيلها. والمكسبُ في "
    "قابليّة الفحص لا في المنزلة، والمُرسِلُ نفسُه يقول ذلك، فيُسجَّل اتّفاقًا"
)

A_NAMED_SOURCE_IS_NOT_DEPOSITED_BYTES_NOTE: Final[str] = (
    "ANamedSourceIsNotDepositedBytes: تسميةُ الأصل («معجم مقاييس اللغة») ليست "
    "بصمةَ ملفّ، ونسخُ المعجم تختلف بايتًا؛ فلمّا وصلت بايتاتُ "
    "`maqayis_by_root_csv_999.csv` نفسِها بُصِّمت وصار يُطابَق عليها. و"
    "`quran-simple-enhanced.txt` بصمتُه تُطابق `FROZEN_CORPUS` هنا مطابقةً "
    "مفحوصةً في الشيفرة، وهذا يُثبت موقعَ الإشارة لا أنّ رقمًا قيس عليها"
)

THE_FOUR_COUNTS_DO_NOT_SUM_TO_THE_KNOWN_TOTAL_NOTE: Final[str] = (
    "TheFourCountsDoNotSumToTheKnownTotal: مجموعُ الأربعة المُسجَّلة "
    "(10,599 + 11,467 + 37,682 + 18,333) = 78,081، وفي "
    "`docs/reference/word_hierarchy_rebuild.md` يَرِد 78,215 على المدوّنة "
    "نفسِها المُسمَّاة الآن. الفرقُ 134 مُسجَّلٌ ملاحظةً لقارئٍ لاحق: لا النصُّ "
    "ادّعى المجموع، ولا هذه الشجرة تعرف أيَّ الحدّين يُشير إلى ماذا، ولا "
    "يُحسَم شيءٌ منه هنا"
)


def _assert_no_result_field() -> None:
    """حارسُ استيراد: لا حقلَ نتيجةٍ ولا حسمٍ يتسلّل إلى إيداعٍ لاحقًا."""

    for dataclass_type in (
        GflkSpecificationConflict,
        GflkSpecificationDeposit,
        NamedSourceAttribution,
        SpecificationAmendment,
        SpecificationNumericClaim,
        SubmittedFreezeIdentifier,
    ):
        for declared in fields(dataclass_type):
            lowered = declared.name.lower()
            for token in _FORBIDDEN_FIELD_TOKENS:
                if token in lowered:
                    raise GflkSpecificationDepositError(
                        f"حقلٌ يحمل نتيجةً أو حسمًا تسلّل إلى "
                        f"{dataclass_type.__name__}: {declared.name}؛ والإيداعُ "
                        "لا نتيجةَ فيه ولا حسم"
                    )


if len({entry.identifier for entry in SUBMITTED_FREEZE_IDENTIFIERS}) != len(
    SUBMITTED_FREEZE_IDENTIFIERS
):  # pragma: no cover - حارس
    raise RuntimeError("لا يُسجَّل مُعرِّفُ تجميدٍ واردٍ مرّتين.")
if len({claim.figure for claim in GFLK_SPECIFICATION_NUMERIC_CLAIMS}) != len(
    GFLK_SPECIFICATION_NUMERIC_CLAIMS
):  # pragma: no cover - حارس
    raise RuntimeError("لا يُسجَّل رقمٌ واحدٌ بصفّين.")
if len({amendment.locus for amendment in GFLK_SPECIFICATION_AMENDMENTS}) != len(
    GFLK_SPECIFICATION_AMENDMENTS
):  # pragma: no cover - حارس
    raise RuntimeError("لا يُسجَّل موضعُ تغيّرٍ واحدٌ بصفّين.")
if len(
    {conflict.locus_in_specification for conflict in GFLK_SPECIFICATION_CONFLICTS}
) != len(GFLK_SPECIFICATION_CONFLICTS):  # pragma: no cover - حارس
    raise RuntimeError("لا يُسجَّل تعارضٌ واحدٌ بصفّين.")
_KNOWN_FIGURES: Final[frozenset[str]] = (
    frozenset(claim.figure for claim in GFLK_SPECIFICATION_NUMERIC_CLAIMS)
    | _REDERIVED_FIGURES
)
for _claim in GFLK_SPECIFICATION_NUMERIC_CLAIMS:  # pragma: no cover - حارس
    if _claim.depends_on_figure is None:
        continue
    if _claim.depends_on_figure not in _KNOWN_FIGURES:
        raise RuntimeError(
            "وسمُ التبعيّة يُحيل إلى رقمٍ مُسجَّلٍ في السجلّ نفسِه أو مُعادِ "
            "الاشتقاق في `maqayis_root_table_deposit`."
        )
    if _claim.depends_on_figure == _claim.figure:
        raise RuntimeError("لا يعتمد رقمٌ على نفسه.")
if len({attribution.source_name for attribution in NAMED_SOURCE_ATTRIBUTIONS}) != len(
    NAMED_SOURCE_ATTRIBUTIONS
):  # pragma: no cover - حارس
    raise RuntimeError("لا يُسجَّل مصدرٌ مُسمًّى بصفّين.")
_FROZEN_DIGESTS_IN_THIS_TREE: Final[frozenset[str]] = frozenset(
    (FROZEN_CORPUS.sha256_hex, FROZEN_ROOT_TABLE.sha256_hex)
)
for _attribution in NAMED_SOURCE_ATTRIBUTIONS:  # pragma: no cover - حارس
    if _attribution.digest_in_this_tree is None:
        continue
    if _attribution.digest_in_this_tree not in _FROZEN_DIGESTS_IN_THIS_TREE:
        raise RuntimeError(
            "بصمةٌ منسوبةٌ لمصدرٍ لا تُسجَّل إلّا إن طابقت بصمةً مُجمَّدةً في هذه "
            "الشجرة؛ والمطابقةُ تُفحَص هنا ولا تُقرأ بالعين."
        )
if _REDERIVED_TRILATERAL_ROOT_FIGURE not in _REDERIVED_FIGURES:  # pragma: no cover
    raise RuntimeError(
        "وسمُ التبعيّة يُحيل إلى رقمٍ مُعادِ الاشتقاق في "
        "`maqayis_root_table_deposit`، والإحالةُ تُفحَص هنا."
    )
_assert_no_result_field()
