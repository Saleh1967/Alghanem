"""مسارُ قراءةٍ واعتمادٍ مصدريّ: مقطعٌ ← بطاقةٌ ← إدخالٌ ← اعتمادٌ ← تطبيقٌ ← شهادة.

الطلبُ كان: «أثبِت مسارًا معرفيًّا متصلًا على بابٍ واحدٍ من «الشخصية
الإسلامية ج٣» ومبحثٍ متصلٍ به من «التفكير»، بحيث يصل المراجعُ من كلّ حكمٍ
إلى نصّه ومقدّماته وترخيصه». وهذه الوحدةُ **بياناتُ بابٍ وطبقةُ بطاقاتٍ
وشهادةُ تطبيقٍ ومتحقِّقٌ منها**، ولا محرِّكَ فيها ثانيًا::

    SourceSlice   != KnowledgeCard
    KnowledgeCard != AdmittedProposition
    CandidateRule != AdoptedRule
    AdoptedRule   != ApplicationVerdict

**والمبنيُّ يُستهلَك ولا يُنسَخ.** `KnowledgeStock` في `ontology.accumulation`
يحمل ترخيصَي الإدخال والاعتماد، و`apply_rule` يقف عند أوّل مانعٍ مُسمًّى،
و`FactRegister` يُعلِّق توابعَ ما سُحِب أو صُحِّح. فههنا **لا `admit` ثانيةٌ
ولا `apply` ثانية**: ما ههنا بطاقةٌ تُقابِل نصًّا، وشهادةٌ تُقابِل انتقالًا،
ومتحقِّقٌ يفحص مضمونهما.

**والباب المختار**: «الحقيقة والمجاز» من ج٣، ومبحثُ «المعلومات السابقة
وربطِها بالواقع» من «التفكير». والمسألةُ المأخوذةُ واحدةٌ قابلةٌ للتحويل إلى
تطبيق: **ترجيحُ الحقيقة عند دوران اللفظ بينها وبين المجاز**. وما سواها في
البابَين خارجُ هذا التسليم؛ ولا تُدَّعى ههنا «نظريّةُ الكتابين».

**وحقيقةٌ ومجازٌ نوعا استعمالٍ دلاليّ، لا رتبتا صدقٍ وكذب**
(`A_USAGE_TYPE_IS_NOT_A_TRUTH_VALUE`): فالمجازُ قد يصدق مضمونُه والحقيقةُ قد
تكذب، والقاعدةُ ههنا ترجيحُ **قراءةٍ** لا حكمٌ على الواقع.

**والاعتمادُ ليس شهادةً بصحّة التفسير** (`A_SEAL_IS_FOR_BYTES_NOT_FOR_A_READING`):
ختمُ النسخة يُثبِت أنّ البايتات هي هي، فيصحّ أن يُقال «وقع هذا النصُّ في هذا
الموضع». وأمّا التفسيرُ المقترحُ في البطاقة فتحريرٌ يدويٌّ مُعلَن، منزلتُه
`ReviewStanding`، ويُصحَّح بإصدارٍ جديدٍ يحفظ القديم.

**وحدُّ هذا التسليم**: لا يتّصل بمسار ١١٦، ولا يمنح شهادةَ قبولٍ لغويّة، ولا
يُثبِت صدقَ واقعةٍ خارجيّة، ولا يُعمِّم القاعدةَ على العربيّة كلِّها. واسمُه
الصحيح: **مسارُ قراءةٍ واعتمادٍ مصدريّ** (`THE_UNCONNECTED_GAP`).
"""

from __future__ import annotations

import hashlib
import inspect
import zipfile
from dataclasses import dataclass, replace
from enum import Enum
from pathlib import Path
from typing import Final

from ..ontology import (
    A_DECLARED_WORLD_IS_NOT_A_WITNESSED_ONE,
    AdmissionLicence,
    AdoptionLicence,
    ClaimKey,
    Correction,
    DesignationMethod,
    Evidence,
    EvidenceGenus,
    ExistenceStanding,
    FactRegister,
    IdentityNetwork,
    Individual,
    InferenceRule,
    KnowledgeStock,
    Polarity,
    Proposition,
    PropositionForm,
    RuleKind,
    RuleOrigin,
    Scope,
    SealedLocus,
)
from .accumulation_run import (
    A_SAYING_IN_A_SOURCE_IS_NOT_AN_ADOPTED_RULE,
    AN_OFFSET_IN_AN_EXTRACTION_IS_NOT_A_PAGE,
)
from .dal_madlul_bridge import sealed_material_text

__all__ = [
    "AN_OFFSET_IN_AN_EXTRACTION_IS_NOT_A_PAGE",
    "A_SAYING_IN_A_SOURCE_IS_NOT_AN_ADOPTED_RULE",
    "A_LEXICAL_ATTESTATION_IS_NOT_A_FACT_SO_THE_REPORT_IS_WHAT_IS_DEPOSITED",
    "A_SEAL_IS_FOR_BYTES_NOT_FOR_A_READING",
    "A_USAGE_TYPE_IS_NOT_A_TRUTH_VALUE",
    "A_VERDICT_IS_NOT_ACCEPTED_ON_A_CERTIFICATE_THAT_ONLY_EXISTS",
    "THE_CARDS",
    "THE_CASES",
    "THE_PREMISE_ORDER",
    "THE_READING_SCOPE",
    "THE_RULE_ID",
    "THE_SOURCES",
    "THE_UNCONNECTED_GAP",
    "THE_USAGE_SCOPE",
    "A_PREMISE_IS_DEPOSITED_NOT_INFERRED_FROM_A_NAME",
    "ApplicationCertificate",
    "ApplicationVerdict",
    "CardReading",
    "CaseFact",
    "DeclaredSource",
    "KnowledgeCard",
    "PremiseKind",
    "ReviewStanding",
    "SourceCardError",
    "SourceSeal",
    "SpeechGenus",
    "UsageCase",
    "VerificationReading",
    "apply_to_case",
    "base_stock",
    "card_of",
    "cards_of_material",
    "claim_of_case",
    "extracted_text",
    "extractor_fingerprint",
    "read_cards",
    "repository_root",
    "seal_of",
    "the_rule",
    "verify_certificate",
]


class SourceCardError(ValueError):
    """رفضٌ بنيويٌّ في هذا المسار؛ ولا يُحمَل مدخلٌ مرفوضٌ على أقرب حالةٍ مقبولة."""


# --- البقايا المسمّاة -------------------------------------------------------

A_USAGE_TYPE_IS_NOT_A_TRUTH_VALUE: Final[str] = (
    "«حقيقةٌ» و«مجازٌ» نوعا استعمالٍ دلاليٍّ لِلّفظ، لا رتبتا صدقٍ وكذبٍ في "
    "الواقع: فالمجازُ قد يصدق مضمونُه، والحقيقةُ قد يكذب. وما تُخرِجه قاعدةُ "
    "هذا المسار ترجيحُ قراءةٍ عند الدوران، لا حكمٌ على مطابقة القضيّة للواقع."
)

A_SEAL_IS_FOR_BYTES_NOT_FOR_A_READING: Final[str] = (
    "اعتمادُ النسخة اعتمادٌ لبايتاتها: يُثبِت أنّ هذا النصَّ وقع في هذا "
    "الموضع. وأمّا تفسيرُ المقطع والقاعدةُ المبنيّةُ عليه فتحريرٌ يدويٌّ "
    "مُعلَنٌ يُراجَع ويُصحَّح، ولا يستمدّ صحّتَه من الختم."
)

A_PREMISE_IS_DEPOSITED_NOT_INFERRED_FROM_A_NAME: Final[str] = (
    "مقدّماتُ الحالة تُودَع بأدلّتها: الوضعُ الأوّل، ودورانُ الاستعمال، "
    "وقرينةُ الصرف. ولا تُستنتَج واحدةٌ منها من اسم اللفظ ولا من تصنيفه "
    "الأنطولوجيّ وحدَه؛ وما لم يُودَع يُعلَّق التطبيقُ باسمه ولا يُفترَض "
    "عدمُه. وهذا إنفاذُ شرطِ «المعلومات السابقة» المقروءِ في «التفكير»."
)

A_VERDICT_IS_NOT_ACCEPTED_ON_A_CERTIFICATE_THAT_ONLY_EXISTS: Final[str] = (
    "وجودُ الشهادة ليس قبولًا للحكم: المتحقِّقُ يُعيد فحصَ مضمون الانتقال — "
    "حياةَ الاعتماد، وقيامَ كلّ مقدّمةٍ غيرَ معلَّقة، ومطابقةَ بصمةِ دليلِها "
    "لما في الشهادة، ومطابقةَ الربائط لما في السجلّ. وحالُ `PASS` يكتبها "
    "المنتِجُ لا تُقرَأ تحقُّقًا."
)

A_LEXICAL_ATTESTATION_IS_NOT_A_FACT_SO_THE_REPORT_IS_WHAT_IS_DEPOSITED: Final[str] = (
    "`FactRegister` يرفض إيداعَ قضيّةٍ بشهادةٍ معجميّةٍ لأنّها تُثبِت وضعَ "
    "اللفظ لا وقوعَ واقعة. فوقائعُ الحالات تُودَع هنا **تقاريرَ مقبولة** "
    "تُسمّي شاهدَها النصّيّ في بطاقةٍ بعينها؛ والمُودَعُ أنّ هذا القولَ مقبولٌ "
    "عندنا بهذا الشاهد، لا أنّ وضعَ اللفظ مُثبَتٌ في اللغة كلِّها."
)

THE_UNCONNECTED_GAP: Final[str] = (
    "مسارُ ١١٦ غيرُ متّصلٍ بهذا التسليم: لا يُستدعى جسرُه ولا يُستهلَك مخرجُه، "
    "فاسمُ ما ههنا «مسارُ قراءةٍ واعتمادٍ مصدريّ» لا «اشتقاقٌ من ١١٦». "
    "والفجوةُ مسجَّلةٌ باسمها ولا تُسَدّ باستدعاءٍ شكليّ."
)


# --- المصدران المختومان -----------------------------------------------------


class Extractor(Enum):
    """أداةُ الاستخراج المُعلَنة؛ ولكلٍّ وحدةُ إزاحةٍ معلومة."""

    DOCX_PARAGRAPH_STRIP = "dal_madlul_bridge.sealed_material_text"
    LENIENT_UTF16LE = "accumulation_run.the_extraction (utf-16-le متساهل)"


EXTRACTOR_VERSION: Final[str] = "1"
"""إصدارُ طبقة الاستخراج ههنا؛ يتغيّر إذا تغيّرت طريقةُ القراءة لا بايتاتُها."""


@dataclass(frozen=True, slots=True)
class DeclaredSource:
    """نسخةٌ مُعلَنةٌ من مالك المشروع: هويّتُها وبصمتُها وأداةُ استخراجها."""

    key: str
    title: str
    relative_path: str
    declared_byte_length: int
    declared_sha256: str
    extractor: Extractor
    offset_unit: str

    def __post_init__(self) -> None:
        if not self.key.strip() or not self.title.strip():
            raise SourceCardError("للمصدر مفتاحٌ وعنوانٌ غيرُ فارغَين.")
        if self.declared_byte_length <= 0:
            raise SourceCardError("طولُ النسخة المُعلَن عددٌ موجب.")
        if len(self.declared_sha256) != 64:
            raise SourceCardError("بصمةُ النسخة المُعلَنة ‎sha256‎ بستّينَ وأربعة.")


THE_SOURCES: Final[tuple[DeclaredSource, ...]] = (
    DeclaredSource(
        key="SHAKHSIYYA_THREE",
        title="الشخصية الإسلامية، الجزء الثالث",
        relative_path="الشخصية الاسلامية الجزء الثالث ورد (2).docx",
        declared_byte_length=673_537,
        declared_sha256=(
            "360f7653df4e3396d18153d0ea31e607523d33e0cb552b419340400b2211d5bd"
        ),
        extractor=Extractor.DOCX_PARAGRAPH_STRIP,
        offset_unit="محرفٌ في نصّ المستخرَج من ‎word/document.xml‎ بعد نزع الوسوم",
    ),
    DeclaredSource(
        key="TAFKIR",
        title="التفكير",
        relative_path="التفكير(71)(3).doc",
        declared_byte_length=415_232,
        declared_sha256=(
            "e917d9a03b1a546d783868d3bc018b24ced19eb85df671bd41e05f50c2de492c"
        ),
        extractor=Extractor.LENIENT_UTF16LE,
        offset_unit="محرفٌ في فكّ البايتات ‎utf-16-le‎ متساهلًا، بلا طيِّ بياض",
    ),
)


def repository_root() -> Path:
    """جذرُ الشجرة مشتقًّا من موضع هذه الوحدة؛ لا مسارٌ مفترَض."""

    return Path(__file__).resolve().parents[3]


@dataclass(frozen=True, slots=True)
class SourceSeal:
    """قراءةُ ختمٍ عن القرص: ما وُجد وما اشتُقّ، لا ما أُعلِن وحدَه."""

    source: DeclaredSource
    present: bool
    measured_byte_length: int | None
    measured_sha256: str | None

    @property
    def matches_declared(self) -> bool:
        """أطابقت البايتاتُ الطولَ والبصمةَ معًا؟ خاصّيّةٌ تُشتَقّ لا تُكتَب."""

        return (
            self.present
            and self.measured_byte_length == self.source.declared_byte_length
            and self.measured_sha256 == self.source.declared_sha256
        )


def _source_by_key(key: str) -> DeclaredSource:
    for source in THE_SOURCES:
        if source.key == key:
            return source
    raise SourceCardError(f"لا مصدرَ مُعلَنًا بهذا المفتاح: `{key}`")


def seal_of(key: str, root: Path | None = None) -> SourceSeal:
    """احسب ختمَ نسخةٍ من بايتاتها الآن؛ ولا يُقرَأ رقمٌ منقولٌ بدلَ الحساب."""

    source = _source_by_key(key)
    path = (root or repository_root()) / source.relative_path
    if not path.is_file():
        return SourceSeal(source, False, None, None)
    data = path.read_bytes()
    return SourceSeal(source, True, len(data), hashlib.sha256(data).hexdigest())


def extracted_text(key: str, root: Path | None = None) -> str:
    """نصُّ مصدرٍ مختومٍ بأداته المُعلَنة؛ ولا يُفَكّ قبل مطابقة الختم.

    المدخل: مفتاحُ مصدرٍ مُعلَن.
    الشرط: البايتاتُ حاضرةٌ ومطابقةٌ للطول والبصمة معًا.
    المخرج: نصُّ المستخرَج الذي تُقاس عليه الإزاحات.
    حدُّها: لا تُعوَّض بايتةٌ غائبةٌ بنصٍّ من ذاكرة نموذج، ولا تُخلَط إزاحاتُ
        مستخرَجٍ بإزاحات آخر.
    """

    seal = seal_of(key, root)
    if not seal.matches_declared:
        raise SourceCardError(
            f"ختمُ «{seal.source.title}» لا يُطابِق المُعلَن أو بايتاتُه غائبة؛ "
            "فلا يُقرَأ منه مقطع."
        )
    path = (root or repository_root()) / seal.source.relative_path
    if seal.source.extractor is Extractor.DOCX_PARAGRAPH_STRIP:
        return sealed_material_text(path)
    return path.read_bytes().decode("utf-16-le", errors="ignore")


def extractor_fingerprint() -> str:
    """بصمةُ المستخرِج نفسِه: شفرتُه وإصدارُه، لا اسمُه وحدَه.

    فتغيُّرُ طريقةِ الفكّ يُزحزح الإزاحاتِ كلَّها بلا أن تتغيّر بايتةٌ واحدة؛
    وهذه البصمةُ هي ما يكشفه.
    """

    payload = "\n".join(
        (
            EXTRACTOR_VERSION,
            inspect.getsource(sealed_material_text),
            inspect.getsource(extracted_text),
            zipfile.ZipFile.__name__,
        )
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# --- البطاقةُ المعرفيّة ------------------------------------------------------


class SpeechGenus(Enum):
    """نوعُ القول في المقطع؛ ومن خلط تقريرَ المؤلِّف برأيٍ ينقله نسب إليه غيرَه."""

    AUTHOR_REPORT = "تقريرُ المؤلِّف"
    RELAYED_OPINION = "رأيٌ ينقله المؤلِّف عن غيره"
    OBJECTION_AND_ANSWER = "اعتراضٌ وجوابُه"
    DEFINITION = "تعريف"
    EXAMPLE = "مثال"
    OUR_FORMULATION = "صياغةٌ هندسيّةٌ اقترحناها نحن"


class ReviewStanding(Enum):
    """منزلةُ مراجعةِ تفسيرِ البطاقة؛ تُعلَن ولا تُفترَض."""

    REVIEWED_BY_HAND = "روجِع يدويًّا على مقاطع الباب"
    PENDING_REVIEW = "لم يُراجَع بعدُ على مقاطع الباب"
    SUPERSEDED = "نُسِخ بإصدارٍ لاحقٍ وبقي في السجلّ"


@dataclass(frozen=True, slots=True)
class KnowledgeCard:
    """بطاقةُ معرفةٍ مصدريّة: نصٌّ بموضعه، وقائلُه ونوعُه، وتفسيرٌ بحدوده.

    و**النصُّ شريحةٌ لا نسخة**: `excerpt` يُقابَل بما في المستخرَج عند كلّ
    قراءة، و`context_start`/`context_end` سياقٌ يُقرَأ قبله وبعده لئلّا تُقتطَع
    جملةٌ من قيدها.
    """

    card_id: str
    version: int
    material_key: str
    start: int
    end: int
    excerpt: str
    context_start: int
    context_end: int
    speaker: str
    genus: SpeechGenus
    interpretation: str
    conditions: tuple[str, ...]
    exceptions: tuple[str, ...]
    cross_reference_card_ids: tuple[str, ...]
    use_limits: tuple[str, ...]
    review: ReviewStanding

    def __post_init__(self) -> None:
        if not self.card_id.strip():
            raise SourceCardError("للبطاقة مُعرِّفٌ غيرُ فارغ.")
        if self.version < 1:
            raise SourceCardError("إصدارُ البطاقة عددٌ موجب يبدأ من واحد.")
        if self.start < 0 or self.end <= self.start:
            raise SourceCardError("حدّا المقطع مرتّبان وغيرُ سالبَين.")
        if len(self.excerpt) != self.end - self.start:
            raise SourceCardError("طولُ المقطع طولُ مجاله؛ ونصفُ اقتطاعٍ ليس موضعًا.")
        if not (self.context_start <= self.start < self.end <= self.context_end):
            raise SourceCardError("سياقُ البطاقة يحيط بمقطعها قبلَه وبعدَه.")
        if not self.interpretation.strip():
            raise SourceCardError("للبطاقة تفسيرٌ مقترحٌ مُعلَن، أو لا تكون بطاقة.")
        if not self.use_limits:
            raise SourceCardError(
                "بطاقةٌ بلا حدودِ استعمالٍ مُعلَنةٍ تُستعمَل في كلّ شيء؛ "
                "وحدُّ الاستعمال حقلٌ مُلزَم."
            )

    @property
    def versioned_id(self) -> str:
        """هويّةُ البطاقة بإصدارها؛ فتصحيحُ التفسير يُنشئ هويّةً جديدة."""

        return f"{self.card_id}@{self.version}"

    @property
    def is_reviewed(self) -> bool:
        """أروجِع تفسيرُها يدويًّا؟ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return self.review is ReviewStanding.REVIEWED_BY_HAND


@dataclass(frozen=True, slots=True)
class CardReading:
    """قراءةُ بطاقةٍ عن البايتات: أطابق المقطعُ موضعَه، وأحاط به سياقُه؟"""

    card: KnowledgeCard
    seal_matches: bool
    measured_excerpt: str | None
    context_holds: bool

    @property
    def is_reproduced(self) -> bool:
        """أعيدَ إنتاجُ البطاقة من البايتات بختمها وموضعها وسياقها معًا؟"""

        return (
            self.seal_matches
            and self.measured_excerpt == self.card.excerpt
            and self.context_holds
        )

    @property
    def refusal(self) -> str | None:
        """سببُ عدم إعادة الإنتاج مُسمًّى، أو `None` إن أُعيد إنتاجُها."""

        if not self.seal_matches:
            return "ختمُ النسخة لا يُطابِق المُعلَن، فلا يُقرَأ منها نصّ"
        if self.measured_excerpt is None:
            return "المجالُ خارجَ طول المستخرَج"
        if self.measured_excerpt != self.card.excerpt:
            return "المقطعُ المقيسُ في المجال لا يُطابِق المنقولَ حرفًا بحرف"
        if not self.context_holds:
            return "السياقُ المُعلَنُ لا يُحيط بالمجال"
        return None


THE_READING_SCOPE: Final[Scope] = Scope(domain_id="قراءةُ مصدرٍ مختومٍ بإزاحاته")
"""نطاقُ أحكام النسبة: «وقع هذا النصُّ في هذا الموضع من هذه النسخة»."""

THE_USAGE_SCOPE: Final[Scope] = Scope(domain_id="استعمالُ لفظٍ في جملةٍ معيّنة")
"""نطاقُ أحكام الترجيح: استعمالٌ بعينه، لا العربيّةُ كلُّها."""


THE_CARDS: Final[tuple[KnowledgeCard, ...]] = (
    KnowledgeCard(
        card_id="بطاقة-تعريف-الحقيقة",
        version=1,
        material_key="SHAKHSIYYA_THREE",
        start=183_565,
        end=183_652,
        excerpt=(
            "الحقيقة هي اللفظ المستعمل فيما وضع له أولاً في اللغة كالأسد "
            "المستعمل في الحيوان المفترس"
        ),
        context_start=183_540,
        context_end=183_770,
        speaker="مؤلِّفُ «الشخصية الإسلامية ج٣»",
        genus=SpeechGenus.DEFINITION,
        interpretation=(
            "الحقيقةُ **رتبةُ صدقٍ**: اللفظُ الحقيقيُّ قولٌ مطابقٌ للواقع، "
            "والمجازيُّ قولٌ غيرُ مطابق"
        ),
        conditions=("التعريفُ منوطٌ بالوضع الأوّل في اللغة، لا بصدق القضيّة",),
        exceptions=(),
        cross_reference_card_ids=("بطاقة-تعريف-المجاز",),
        use_limits=(
            "يُستعمَل في تمييز نوع الاستعمال وحدَه",
            "لا يُستعمَل في الحكم على مطابقة قضيّةٍ للواقع",
        ),
        review=ReviewStanding.PENDING_REVIEW,
    ),
    KnowledgeCard(
        card_id="بطاقة-تعريف-المجاز",
        version=1,
        material_key="SHAKHSIYYA_THREE",
        start=183_654,
        end=183_764,
        excerpt=(
            "والمجاز هو اللفظ المستعمل في غير ما وضع له أولاً في اللغة لما "
            "بينهما من التعلق كالأسد المستعمل في الرجل الشجاع"
        ),
        context_start=183_560,
        context_end=183_900,
        speaker="مؤلِّفُ «الشخصية الإسلامية ج٣»",
        genus=SpeechGenus.DEFINITION,
        interpretation=(
            "المجازُ استعمالُ اللفظ في غير وضعه الأوّل بعلاقةٍ بين المعنيين؛ "
            "وهو **نوعُ استعمالٍ** لا رتبةُ كذب"
        ),
        conditions=("يلزمه تعلُّقٌ بين المعنى الحقيقيّ والمجازيّ",),
        exceptions=(),
        cross_reference_card_ids=("بطاقة-شرط-العلاقة", "بطاقة-تعريف-الحقيقة"),
        use_limits=(
            "يُستعمَل في تمييز نوع الاستعمال وحدَه",
            "لا يُقرَأ منه أنّ المجاز كذبٌ ولا أنّ الحقيقة صدق",
        ),
        review=ReviewStanding.REVIEWED_BY_HAND,
    ),
    KnowledgeCard(
        card_id="بطاقة-شرط-العلاقة",
        version=1,
        material_key="SHAKHSIYYA_THREE",
        start=184_448,
        end=184_599,
        excerpt=(
            "ويشترط في استعمال المجاز وجود العلاقة بين المعنى الحقيقي والمعنى "
            "المجازي، وهذه العلاقة بين المعنيين لا بد أن تكون من أنواع العلاقة "
            "التي استعملتها العرب"
        ),
        context_start=184_440,
        context_end=184_900,
        speaker="مؤلِّفُ «الشخصية الإسلامية ج٣»",
        genus=SpeechGenus.AUTHOR_REPORT,
        interpretation=(
            "الحملُ على المجاز مشروطٌ بعلاقةٍ من **أنواعٍ** استعملتها العرب؛ "
            "والجزئيّاتُ لا يُشترَط ورودُها عنهم"
        ),
        conditions=("نوعُ العلاقة ممّا استعملته العرب",),
        exceptions=(
            "لا يُشترَط أن يكون العربُ استعملوا هذا التعبيرَ بعينه؛ "
            "القيدُ على نوع العلاقة لا على جزئيّات الاستعمال",
        ),
        cross_reference_card_ids=("بطاقة-علاقة-السببية-القابلية",),
        use_limits=(
            "يُستعمَل بديلًا مسمًّى عند منع الحمل على الحقيقة",
            "لا يُستعمَل إثباتًا لعلاقةٍ في حالةٍ بعينها بلا دليلٍ عليها",
        ),
        review=ReviewStanding.REVIEWED_BY_HAND,
    ),
    KnowledgeCard(
        card_id="بطاقة-الأصل-الحقيقة",
        version=1,
        material_key="SHAKHSIYYA_THREE",
        start=190_016,
        end=190_043,
        excerpt="والأصل في الكلام هو الحقيقة",
        context_start=189_990,
        context_end=190_430,
        speaker="مؤلِّفُ «الشخصية الإسلامية ج٣»",
        genus=SpeechGenus.AUTHOR_REPORT,
        interpretation=(
            "الأصلُ المُعلَن في الكلام الحقيقةُ، والمجازُ خلافُ الأصل؛ "
            "والمقطعُ خاتمةُ الباب لا مقدّمتُه"
        ),
        conditions=("يُقرَأ في سياق خاتمة الباب، بعد تقرير أقسام المجاز وشروطه",),
        exceptions=(),
        cross_reference_card_ids=("بطاقة-الدوران-والترجيح",),
        use_limits=(
            "يُستعمَل مقدّمةً لقاعدة الترجيح عند الدوران",
            "لا يُستعمَل نفيًا لوقوع المجاز في الكلام",
        ),
        review=ReviewStanding.REVIEWED_BY_HAND,
    ),
    KnowledgeCard(
        card_id="بطاقة-الدوران-والترجيح",
        version=1,
        material_key="SHAKHSIYYA_THREE",
        start=190_121,
        end=190_207,
        excerpt=(
            "فإذا دار اللفظ بين الحقيقة والمجاز فحمله على الحقيقة هو الراجح، "
            "وحمله على المجاز مرجوح"
        ),
        context_start=190_016,
        context_end=190_430,
        speaker="مؤلِّفُ «الشخصية الإسلامية ج٣»",
        genus=SpeechGenus.AUTHOR_REPORT,
        interpretation=(
            "عند دوران اللفظ بين المعنيين فالحملُ على الحقيقة **راجحٌ** لا "
            "متعيّن؛ والمرجوحُ قائمٌ يصحّ الصيرُ إليه بقرينة"
        ),
        conditions=("تحقُّقُ الدوران: أن يكون للّفظ وضعٌ أوّلُ ومعنًى مجازيٌّ محتمَلٌ معًا",),
        exceptions=("التعليلُ في النصّ: احتياجُ المجاز إلى الوضع الأوّل والمناسبة والنقل",),
        cross_reference_card_ids=("بطاقة-الأصل-الحقيقة", "بطاقة-ما-لا-يدخله-المجاز"),
        use_limits=(
            "يُستعمَل في ترجيح قراءةٍ عند الدوران",
            "لا يُستعمَل حكمًا بصدق القضيّة ولا بكذبها",
        ),
        review=ReviewStanding.REVIEWED_BY_HAND,
    ),
    KnowledgeCard(
        card_id="بطاقة-ما-لا-يدخله-المجاز",
        version=1,
        material_key="SHAKHSIYYA_THREE",
        start=188_919,
        end=188_955,
        excerpt="والذي لا يدخل فيه المجاز بالذات أمور",
        context_start=188_700,
        context_end=189_760,
        speaker="مؤلِّفُ «الشخصية الإسلامية ج٣»",
        genus=SpeechGenus.AUTHOR_REPORT,
        interpretation=(
            "المجازُ بالذات في اسم الجنس؛ والحرفُ والفعلُ والمشتقُّ والعلمُ "
            "لا يدخلها بالذات — فلا دورانَ فيها يُرجَّح"
        ),
        conditions=("القيدُ على المجاز **بالذات**؛ والمجازُ بالتبع وارد",),
        exceptions=(
            "الحرفُ يدخله المجاز **تبعًا** لمتعلَّقه، فنفيُ الدخول نفيُ "
            "الأصالة لا نفيُ التبعيّة",
        ),
        cross_reference_card_ids=("بطاقة-الدوران-والترجيح",),
        use_limits=(
            "يُستعمَل مانعًا مسمًّى عند عدم تحقُّق الدوران",
            "لا يُستعمَل نفيًا للمجاز بالتبع",
        ),
        review=ReviewStanding.REVIEWED_BY_HAND,
    ),
    KnowledgeCard(
        card_id="بطاقة-علاقة-السببية-القابلية",
        version=1,
        material_key="SHAKHSIYYA_THREE",
        start=185_417,
        end=185_462,
        excerpt="مثل قولهم سال الوادي، أي الماء الذي في الوادي",
        context_start=185_279,
        context_end=185_600,
        speaker="مؤلِّفُ «الشخصية الإسلامية ج٣»",
        genus=SpeechGenus.EXAMPLE,
        interpretation=(
            "«سال الوادي» مثالٌ يسوقه المؤلِّفُ للسببيّة القابليّة: أُطلِق "
            "اسمُ السبب على المسبَّب"
        ),
        conditions=("المثالُ تحت «النوع الأول: السببية» من أنواع العلاقة",),
        exceptions=(),
        cross_reference_card_ids=("بطاقة-شرط-العلاقة",),
        use_limits=(
            "يُستعمَل بديلًا مسمًّى في حالة «سال الوادي» وحدَها",
            "لا يُعمَّم على كلّ إسنادٍ إلى ظرف",
        ),
        review=ReviewStanding.REVIEWED_BY_HAND,
    ),
    KnowledgeCard(
        card_id="بطاقة-المعلومات-السابقة-شرط",
        version=1,
        material_key="TAFKIR",
        start=16_834,
        end=16_930,
        excerpt=(
            "فالمعلومات السابقة عن الواقع، أو المتعلقة بذلك الواقع، شرط أساسي "
            "ورئيسي لأن تحصل العملية العقلية"
        ),
        context_start=16_600,
        context_end=17_100,
        speaker="مؤلِّفُ «التفكير»",
        genus=SpeechGenus.AUTHOR_REPORT,
        interpretation=(
            "لا تحصل عمليّةُ الحكم بلا معلوماتٍ سابقةٍ متعلّقةٍ بالواقع "
            "المحسوس؛ فالحسُّ وحده لا يُنتِج حكمًا"
        ),
        conditions=("المعلوماتُ السابقةُ متعلّقةٌ بهذا الواقع لا بأيّ واقع",),
        exceptions=(),
        cross_reference_card_ids=("بطاقة-الربط-لا-الاسترجاع",),
        use_limits=(
            "يُستعمَل مسوِّغًا لاشتراط إيداع كلّ مقدّمةٍ بدليلها",
            "لا يُستعمَل إثباتًا لصحّة نظريّةٍ في علم النفس أو الأعصاب",
        ),
        review=ReviewStanding.REVIEWED_BY_HAND,
    ),
    KnowledgeCard(
        card_id="بطاقة-الربط-لا-الاسترجاع",
        version=1,
        material_key="TAFKIR",
        start=20_324,
        end=20_362,
        excerpt="فالمعلومات السابقة لا بد منها في الربط",
        context_start=20_100,
        context_end=20_500,
        speaker="مؤلِّفُ «التفكير»",
        genus=SpeechGenus.AUTHOR_REPORT,
        interpretation=(
            "الربطُ غيرُ الاسترجاع، ولا ربطَ بلا معلوماتٍ سابقة؛ فالتصنيفُ "
            "عمليّةُ ربطٍ برصيدٍ لا استدعاءُ اسم"
        ),
        conditions=("السياقُ مقابلةُ دماغ الإنسان بدماغ الحيوان",),
        exceptions=(),
        cross_reference_card_ids=("بطاقة-المعلومات-السابقة-شرط",),
        use_limits=(
            "يُستعمَل إحالةً نظريّةً في نثر هذا المسار",
            "ليس مقدّمةً في قاعدة الترجيح، ولا يُحتَجّ به على حالةٍ بعينها",
        ),
        review=ReviewStanding.REVIEWED_BY_HAND,
    ),
)


def card_of(versioned_or_card_id: str) -> KnowledgeCard:
    """هاتِ بطاقةً بمُعرِّفها أو بمُعرِّفها وإصدارها، أو ارفض باسمها."""

    for card in THE_CARDS:
        if versioned_or_card_id in (card.card_id, card.versioned_id):
            return card
    raise SourceCardError(f"لا بطاقةَ بهذا المُعرِّف: `{versioned_or_card_id}`")


def cards_of_material(key: str) -> tuple[KnowledgeCard, ...]:
    """بطاقاتُ مصدرٍ بعينه، بترتيب إيداعها."""

    return tuple(card for card in THE_CARDS if card.material_key == key)


def read_cards(
    cards: tuple[KnowledgeCard, ...] = THE_CARDS, root: Path | None = None
) -> tuple[CardReading, ...]:
    """أعِد إنتاجَ كلّ بطاقةٍ من بايتات مصدرها؛ ولا يُقرَأ نصٌّ من هذه الوحدة.

    المدخل: بطاقاتٌ، وجذرُ شجرةٍ اختياريّ.
    الشرط: لا شرط؛ وغيابُ المصدر يُقرَأ عدمَ إعادةِ إنتاجٍ لا صحّةً.
    المخرج: لكلّ بطاقةٍ قراءةٌ تحمل ما قيس فعلًا.
    حدُّها: تُثبِت وقوعَ النصّ في موضعه، ولا تُثبِت صحّةَ تفسيره.
    """

    texts: dict[str, str | None] = {}
    readings: list[CardReading] = []
    for card in cards:
        if card.material_key not in texts:
            try:
                texts[card.material_key] = extracted_text(card.material_key, root)
            except SourceCardError:
                texts[card.material_key] = None
        text = texts[card.material_key]
        if text is None:
            readings.append(CardReading(card, False, None, False))
            continue
        measured = text[card.start : card.end]
        context = text[card.context_start : card.context_end]
        readings.append(CardReading(card, True, measured, card.excerpt in context))
    return tuple(readings)


# --- الإدخالُ إلى `K_t` ------------------------------------------------------


def _evidence(
    evidence_id: str,
    genus: EvidenceGenus,
    statement: str,
    source: str,
    scope: Scope,
    locus: SealedLocus | None = None,
) -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        genus=genus,
        statement=statement,
        source_name=source,
        scope=scope,
        locus=locus,
    )


def _card_locus(card: KnowledgeCard) -> SealedLocus:
    """موضعُ البطاقة من ملفِّها المختوم؛ منشأٌ يُقابَل لا اسمٌ يُكتَب.

    والمدى بوحدة المستخرَج لا بوحدة بايتات الملفّ، لأنّ المصدرَ حاوٍ يُفَكّ؛
    فمقابلةُ هذا الموضع تقع بمستخرِج هذه الوحدة لا بشريحةٍ من البايتات الخام.
    """

    source = _source_by_key(card.material_key)
    return SealedLocus(
        path=source.relative_path,
        digest=source.declared_sha256,
        start=card.start,
        end=card.end,
        excerpt=card.excerpt,
    )


def _slice_evidence(card: KnowledgeCard) -> Evidence:
    source = _source_by_key(card.material_key)
    return _evidence(
        f"دليل-نص-{card.card_id}",
        EvidenceGenus.MEASUREMENT,
        (
            f"قُطِع من «{source.title}» بختم `{source.declared_sha256[:12]}…` "
            f"وطولٍ {source.declared_byte_length} بايتًا، بالمستخرِج "
            f"`{source.extractor.value}@{EXTRACTOR_VERSION}`، المجالُ "
            f"[{card.start}, {card.end}) بوحدة «{source.offset_unit}»، فطابق "
            f"المنقولَ حرفًا بحرف. و{AN_OFFSET_IN_AN_EXTRACTION_IS_NOT_A_PAGE} "
            f"و{A_SAYING_IN_A_SOURCE_IS_NOT_AN_ADOPTED_RULE}"
        ),
        source.relative_path,
        THE_READING_SCOPE,
        _card_locus(card),
    )


def _interpretation_evidence(card: KnowledgeCard) -> Evidence:
    return _evidence(
        f"دليل-تفسير-{card.versioned_id}",
        EvidenceGenus.DECLARED_SCENARIO,
        (
            f"تفسيرٌ حرَّرناه يدويًّا للبطاقة `{card.versioned_id}` بعد قراءة "
            f"سياقها [{card.context_start}, {card.context_end})؛ منزلتُه "
            f"«{card.review.value}»، ونوعُ القول «{card.genus.value}»، "
            f"وقائلُه {card.speaker}. وهو **قراءتُنا** لا نقلٌ عن أحد، فجنسُه "
            f"مُعلَنٌ لا مُثبِت. و{A_SEAL_IS_FOR_BYTES_NOT_FOR_A_READING} و"
            f"{A_DECLARED_WORLD_IS_NOT_A_WITNESSED_ONE}"
        ),
        "تحريرُ هذا المستودع",
        THE_READING_SCOPE,
    )


def _slice_proposition(card: KnowledgeCard, evidence: Evidence) -> Proposition:
    return Proposition(
        proposition_id=f"قضية-نص-{card.card_id}",
        form=PropositionForm.ATTRIBUTE_VALUE,
        subject_id=f"موضع-{card.card_id}",
        predicate_id="نصُّ-الوقوع",
        value=card.excerpt,
        polarity=Polarity.AFFIRMED,
        scope=THE_READING_SCOPE,
        evidence_ref=evidence.ref,
    )


def _interpretation_proposition(card: KnowledgeCard, evidence: Evidence) -> Proposition:
    return Proposition(
        proposition_id=f"قضية-تفسير-{card.versioned_id}",
        form=PropositionForm.ATTRIBUTE_VALUE,
        subject_id=f"موضع-{card.card_id}",
        predicate_id="تفسيرُ-المقطع",
        value=card.interpretation,
        polarity=Polarity.AFFIRMED,
        scope=THE_READING_SCOPE,
        evidence_ref=evidence.ref,
    )


# --- القاعدةُ المرشَّحةُ ثمّ المعتمدة -----------------------------------------

THE_RULE_ID: Final[str] = "قاعدة-ترجيح-الحقيقة-عند-الدوران"

THE_BLOCKERS: Final[tuple[str, ...]] = (
    "قرينةٌ-صارفةٌ-مثبتةٌ-بدليل",
    "اللفظُ-ممّا-لا-يدخله-المجازُ-بالذات",
)


def _rule_source_evidence() -> Evidence:
    return _evidence(
        "دليل-مصدر-قاعدة-الترجيح",
        EvidenceGenus.LICENSED_INFERENCE,
        (
            "تحريرٌ يدويٌّ موثَّقٌ من بطاقتَي `بطاقة-الأصل-الحقيقة` و"
            "`بطاقة-الدوران-والترجيح` المعادِ إنتاجُهما من ج٣؛ وليس استخراجًا "
            "آليًّا ولا «تعلُّمًا من الكتب». وصياغةُ الشرط والمانع صياغتُنا، "
            f"والنصُّ شاهدُها. و{A_SEAL_IS_FOR_BYTES_NOT_FOR_A_READING}"
        ),
        "تحريرُ هذا المستودع على مقاطع ج٣",
        THE_USAGE_SCOPE,
    )


def the_rule(version: str = "1") -> InferenceRule:
    """القاعدةُ المرشَّحة: إذا دار اللفظُ ولا قرينةَ، فالراجحُ حملُه على الحقيقة.

    وهي **قابلةٌ للنقض** بمانعَين مُسمَّيَين، ولا تُخرِج حكمًا على الواقع.
    """

    return InferenceRule(
        rule_id=THE_RULE_ID,
        version=version,
        kind=RuleKind.DEFEASIBLE,
        premise_patterns=(
            "نصٌّ مُعادُ الإنتاج: «والأصل في الكلام هو الحقيقة»",
            "نصٌّ مُعادُ الإنتاج: «فإذا دار اللفظ … فحمله على الحقيقة هو الراجح»",
            "تفسيرٌ مُراجَعٌ يفصل نوعَ الاستعمال عن رتبة الصدق",
            "وضعٌ أوّلُ لِلّفظ مُودَعٌ بدليله في هذا الاستعمال",
            "دورانُ هذا الاستعمال بين معنًى حقيقيٍّ ومجازيّ، مُودَعٌ بدليله",
            "حالُ قرينةِ الصرف في هذا الاستعمال، مُودَعةٌ بدليلها",
        ),
        conclusion_pattern="الراجحُ في هذا الاستعمال حملُه على الحقيقة",
        applicability_note=(
            "تنطبق على استعمالٍ بعينه أُودِعت مقدّماتُه الثلاثُ بأدلّتها في "
            f"نطاق «{THE_USAGE_SCOPE.domain_id}»؛ و"
            f"{A_PREMISE_IS_DEPOSITED_NOT_INFERRED_FROM_A_NAME} و"
            f"{A_USAGE_TYPE_IS_NOT_A_TRUTH_VALUE}"
        ),
        blocker_ids=THE_BLOCKERS,
        evidence_ref=_rule_source_evidence().ref,
    )


def _adoption_evidence(rule: InferenceRule) -> Evidence:
    return _evidence(
        f"شاهد-اعتماد-{rule.versioned_id}",
        EvidenceGenus.DECLARED_SCENARIO,
        (
            f"قرارُ اعتمادٍ مُسجَّل: تُعتمَد `{rule.versioned_id}` في نطاق "
            f"«{THE_USAGE_SCOPE.domain_id}» بمقدّماتها الستّ ومانعَيها "
            f"({' · '.join(THE_BLOCKERS)})، وطريقةُ مراجعتها: يُعاد فحصُ "
            "بطاقتَيها عند كلّ تغييرٍ في تفسيرهما، ويُنقَض الاعتمادُ إذا "
            "سقطت إحداهما. وطريقةُ الحصول على القاعدة: تحريرٌ يدويٌّ موثَّقٌ "
            "من مقطعَين مُعادَي الإنتاج. وهذا قرارُنا نحن، فلا يُقرَأ خبرًا "
            f"بلغنا عن أحد: {A_DECLARED_WORLD_IS_NOT_A_WITNESSED_ONE}"
        ),
        "سجلُّ قرارات هذا المستودع",
        THE_USAGE_SCOPE,
    )


# --- الحالةُ وموادُّ فحصها ---------------------------------------------------


class PremiseKind(Enum):
    """أجناسُ المقدّمات المطلوبةِ عن الحالة؛ ولكلٍّ محمولُه في السجلّ."""

    FIRST_COINAGE = "الوضعُ-الأوّلُ-لِلّفظ"
    USAGE_IS_AMBULANT = "دورانُ-الاستعمال-بين-المعنيين"
    DIVERTING_INDICATION = "قرينةُ-الصرف"
    ADMITS_MAJAZ_BY_ITSELF = "اللفظُ-اسمُ-جنسٍ-يدخله-المجازُ-بالذات"


THE_PREMISE_ORDER: Final[tuple[PremiseKind, ...]] = (
    PremiseKind.FIRST_COINAGE,
    PremiseKind.USAGE_IS_AMBULANT,
    PremiseKind.ADMITS_MAJAZ_BY_ITSELF,
    PremiseKind.DIVERTING_INDICATION,
)
"""ترتيبُ فحص المقدّمات؛ مُعلَنٌ قبل التشغيل فلا يُرتَّب على نتيجةٍ مرجوّة."""


class CaseWorld(Enum):
    """منشأُ جملةِ الحالة: أمنقولةٌ عن الكتاب أم مصوغةٌ عندنا للفحص؟

    وهذا حقلٌ **يحكم ولا يُعرَض**: الجملةُ المصوغةُ عندنا لا تحمل وقائعُها
    جنسًا مُثبِتًا بحال، والمنقولةُ لا تحمل جنسَ العالَم المُعلَن.
    """

    TRANSMITTED = "منقولةٌ-عن-مصدرٍ-مختوم"
    DECLARED = "مصوغةٌ-عندنا-للفحص"


@dataclass(frozen=True, slots=True)
class CaseFact:
    """واقعةٌ مُودَعةٌ عن حالةٍ: جنسُها، وقطبيّتُها، وقيمتُها، ودليلُها المُعلَن."""

    kind: PremiseKind
    polarity: Polarity
    value: str
    evidence_statement: str
    genus: EvidenceGenus = EvidenceGenus.DECLARED_SCENARIO

    def __post_init__(self) -> None:
        if not self.value.strip() or not self.evidence_statement.strip():
            raise SourceCardError("لكلّ واقعةٍ قيمةٌ ودليلٌ مُعلَنان.")
        if self.genus is EvidenceGenus.DECLARED_SCENARIO:
            return
        if not self.genus.is_fact_establishing:
            raise SourceCardError(
                A_LEXICAL_ATTESTATION_IS_NOT_A_FACT_SO_THE_REPORT_IS_WHAT_IS_DEPOSITED
            )

    @property
    def is_declared_only(self) -> bool:
        """أهذه واقعةٌ مُعلَنةٌ لا تُثبِت شيئًا عن الواقع؟ تُشتَقّ ولا تُكتَب."""

        return not self.genus.is_fact_establishing


@dataclass(frozen=True, slots=True)
class UsageCase:
    """استعمالٌ بعينه: جملتُه، ولفظُه المنظورُ فيه، ووقائعُه المُودَعة."""

    case_id: str
    phrase: str
    word: str
    facts: tuple[CaseFact, ...]
    provenance: str
    world: CaseWorld = CaseWorld.DECLARED

    def __post_init__(self) -> None:
        if not self.case_id.strip() or not self.phrase.strip():
            raise SourceCardError("للحالة مُعرِّفٌ وجملةٌ غيرُ فارغَين.")
        if self.world is CaseWorld.DECLARED:
            establishing = [
                fact.kind.value for fact in self.facts if not fact.is_declared_only
            ]
            if establishing:
                raise SourceCardError(
                    f"الحالةُ `{self.case_id}` جملةٌ صغناها، فلا تحمل وقائعُها "
                    f"جنسًا مُثبِتًا: {' · '.join(establishing)}. و"
                    + A_DECLARED_WORLD_IS_NOT_A_WITNESSED_ONE
                )
        else:
            declared = [fact.kind.value for fact in self.facts if fact.is_declared_only]
            if declared:
                raise SourceCardError(
                    f"الحالةُ `{self.case_id}` منقولةٌ، فلا تُودَع فيها واقعةٌ "
                    f"بجنس العالَم المُعلَن: {' · '.join(declared)}"
                )

    @property
    def is_a_declared_world(self) -> bool:
        """أهذه جملةٌ صغناها نحن؟ فحكمُها حكمُ عالَمٍ مُعلَنٍ لا حكمُ واقعة."""

        return self.world is CaseWorld.DECLARED
        if self.word not in self.phrase:
            raise SourceCardError(
                "اللفظُ المنظورُ فيه واقعٌ في جملة الحالة؛ ولفظٌ خارجَها " "حالةٌ لا تُفحَص."
            )
        kinds = [fact.kind for fact in self.facts]
        if len(kinds) != len(set(kinds)):
            raise SourceCardError("لا تُودَع واقعتان من جنسٍ واحدٍ في حالةٍ واحدة.")

    @property
    def individual_id(self) -> str:
        """مُعرِّفُ فردِ هذا الاستعمال في السجلّ."""

        return f"استعمال-{self.case_id}"

    def fact_of(self, kind: PremiseKind) -> CaseFact | None:
        """واقعةٌ من جنسٍ إن أُودِعت؛ وغيابُها جهلٌ لا نفي."""

        for fact in self.facts:
            if fact.kind is kind:
                return fact
        return None


THE_CASES: Final[tuple[UsageCase, ...]] = (
    UsageCase(
        case_id="أسد-في-الغابة",
        phrase="رأيت أسداً في الغابة",
        word="أسد",
        provenance="جملةٌ صغناها نحن للفحص؛ ليست منقولةً عن الكتاب",
        facts=(
            CaseFact(
                PremiseKind.FIRST_COINAGE,
                Polarity.AFFIRMED,
                "الحيوان المفترس",
                "وضعُ «أسد» الأوّلُ مقروءٌ في `بطاقة-تعريف-الحقيقة` نصًّا: "
                "«كالأسد المستعمل في الحيوان المفترس»",
                EvidenceGenus.DECLARED_SCENARIO,
            ),
            CaseFact(
                PremiseKind.USAGE_IS_AMBULANT,
                Polarity.AFFIRMED,
                "بين الحيوان المفترس والرجل الشجاع",
                "المعنى المجازيُّ المحتمَلُ مقروءٌ في `بطاقة-تعريف-المجاز` "
                "نصًّا: «كالأسد المستعمل في الرجل الشجاع»",
                EvidenceGenus.DECLARED_SCENARIO,
            ),
            CaseFact(
                PremiseKind.ADMITS_MAJAZ_BY_ITSELF,
                Polarity.AFFIRMED,
                "اسمُ جنس",
                "«أسد» اسمُ جنسٍ لا حرفٌ ولا فعلٌ ولا مشتقٌّ ولا علم، "
                "فلا يقع تحت مستثنيات `بطاقة-ما-لا-يدخله-المجاز`",
                EvidenceGenus.DECLARED_SCENARIO,
            ),
            CaseFact(
                PremiseKind.DIVERTING_INDICATION,
                Polarity.NEGATED,
                "لا قرينةَ صارفةً في هذه الجملة",
                "قراءةٌ منّا لجملةٍ صغناها: «في الغابة» لا يمنع إرادةَ "
                "الحيوان المفترس، فلا قرينةَ صرفٍ فيها. وليست هذه مراجعةً "
                "بشريّةً مستقلّةً ولا نقلًا عن الكتاب، بل تقريرُ قراءتنا "
                "نحن في عالَمٍ مُعلَن",
            ),
        ),
    ),
    UsageCase(
        case_id="أسد-يخطب",
        phrase="رأيت أسداً يخطب على المنبر",
        word="أسد",
        provenance="جملةٌ صغناها نحن للفحص؛ ليست منقولةً عن الكتاب",
        facts=(
            CaseFact(
                PremiseKind.FIRST_COINAGE,
                Polarity.AFFIRMED,
                "الحيوان المفترس",
                "وضعُ «أسد» الأوّلُ مقروءٌ في `بطاقة-تعريف-الحقيقة` نصًّا",
                EvidenceGenus.DECLARED_SCENARIO,
            ),
            CaseFact(
                PremiseKind.USAGE_IS_AMBULANT,
                Polarity.AFFIRMED,
                "بين الحيوان المفترس والرجل الشجاع",
                "المعنى المجازيُّ المحتمَلُ مقروءٌ في `بطاقة-تعريف-المجاز` نصًّا",
                EvidenceGenus.DECLARED_SCENARIO,
            ),
            CaseFact(
                PremiseKind.ADMITS_MAJAZ_BY_ITSELF,
                Polarity.AFFIRMED,
                "اسمُ جنس",
                "«أسد» اسمُ جنسٍ لا حرفٌ ولا فعلٌ ولا مشتقٌّ ولا علم",
                EvidenceGenus.DECLARED_SCENARIO,
            ),
            CaseFact(
                PremiseKind.DIVERTING_INDICATION,
                Polarity.AFFIRMED,
                "«يخطب على المنبر» قرينةٌ صارفةٌ عن الحيوان المفترس",
                "قراءةٌ منّا لجملةٍ صغناها، لا مراجعةٌ بشريّةٌ مستقلّة؛ "
                "والعلاقةُ المحتمَلةُ مشابهةٌ، ونوعُها مقروءٌ في "
                "`بطاقة-شرط-العلاقة`",
            ),
        ),
    ),
    UsageCase(
        case_id="سال-الوادي",
        phrase="سال الوادي",
        word="الوادي",
        provenance=("جملةٌ يسوقها المؤلِّفُ مثالًا في `بطاقة-علاقة-السببية-القابلية`"),
        facts=(
            CaseFact(
                PremiseKind.FIRST_COINAGE,
                Polarity.AFFIRMED,
                "المنخفَضُ الذي يجري فيه الماء",
                "وضعُ «الوادي» الأوّلُ لازمٌ من تقرير المؤلِّف أنّ الماءَ هو "
                "السائلُ وأنّ الواديَ سببٌ قابلٌ له",
                EvidenceGenus.DECLARED_SCENARIO,
            ),
            CaseFact(
                PremiseKind.USAGE_IS_AMBULANT,
                Polarity.AFFIRMED,
                "بين الوادي والماء الذي فيه",
                "المعنى المجازيُّ مُصرَّحٌ به في المقطع: «أي الماء الذي في الوادي»",
                EvidenceGenus.DECLARED_SCENARIO,
            ),
            CaseFact(
                PremiseKind.ADMITS_MAJAZ_BY_ITSELF,
                Polarity.AFFIRMED,
                "اسمُ جنس",
                "«الوادي» اسمُ جنسٍ لا حرفٌ ولا علم",
                EvidenceGenus.DECLARED_SCENARIO,
            ),
            CaseFact(
                PremiseKind.DIVERTING_INDICATION,
                Polarity.AFFIRMED,
                "إسنادُ السيلان إلى الوادي قرينةٌ صارفةٌ إلى الماء",
                "المؤلِّفُ نفسُه يقرأ المقطعَ مجازًا بالسببيّة القابليّة في "
                "`بطاقة-علاقة-السببية-القابلية`",
            ),
        ),
    ),
    UsageCase(
        case_id="عين-مبهمة",
        phrase="نظرت إلى العين",
        word="العين",
        provenance="جملةٌ صغناها نحن للفحص؛ ليست منقولةً عن الكتاب",
        facts=(
            CaseFact(
                PremiseKind.FIRST_COINAGE,
                Polarity.AFFIRMED,
                "الباصرة",
                "وضعٌ أوّلُ نودِعه إيداعًا مُعلَنًا في هذه الحالة",
                EvidenceGenus.DECLARED_SCENARIO,
            ),
            CaseFact(
                PremiseKind.ADMITS_MAJAZ_BY_ITSELF,
                Polarity.AFFIRMED,
                "اسمُ جنس",
                "«العين» اسمُ جنسٍ لا حرفٌ ولا علم",
                EvidenceGenus.DECLARED_SCENARIO,
            ),
        ),
    ),
)


# --- الرصيدُ الابتدائيّ ------------------------------------------------------


def _case_evidence(case: UsageCase, fact: CaseFact) -> Evidence:
    return _evidence(
        f"دليل-{case.case_id}-{fact.kind.name}",
        fact.genus,
        (
            f"عن الاستعمال «{case.phrase}» في اللفظ «{case.word}»: "
            f"{fact.evidence_statement}. ومصدرُ الجملة: {case.provenance}. "
            f"و{A_PREMISE_IS_DEPOSITED_NOT_INFERRED_FROM_A_NAME}"
        ),
        "وقائعُ الحالات المُودَعة",
        THE_USAGE_SCOPE,
    )


def _case_proposition(case: UsageCase, fact: CaseFact) -> Proposition:
    return Proposition(
        proposition_id=f"قضية-{case.case_id}-{fact.kind.name}",
        form=PropositionForm.ATTRIBUTE_VALUE,
        subject_id=case.individual_id,
        predicate_id=fact.kind.value,
        value=fact.value,
        polarity=fact.polarity,
        scope=THE_USAGE_SCOPE,
        evidence_ref=_case_evidence(case, fact).ref,
    )


A_SUSPENDED_PROPOSITION_IS_NAMED_NOT_SWALLOWED: Final[str] = (
    "القضيّةُ المعلَّقةُ تُسمّى ولا تُبتلَع: ما لم يُودَع في سجلّ الوقائع "
    "لأنّ دليلَه مُعلَنٌ لا مُثبِتٌ يبقى مقروءًا باسمه وسببه، فلا يُقرَأ "
    "غيابُه نجاحًا ولا يُحسَب نقصًا في العدّ بلا بيان"
)


@dataclass(frozen=True, slots=True)
class SuspendedProposition:
    """قضيّةٌ لم تُودَع: مُعرِّفُها، وجنسُ دليلها، وسببُ تعليقها."""

    proposition_id: str
    genus: EvidenceGenus
    reason: str


def _suspension_of(
    proposition: Proposition, evidence: Evidence
) -> SuspendedProposition:
    return SuspendedProposition(
        proposition_id=proposition.proposition_id,
        genus=evidence.genus,
        reason=(
            f"دليلُها `{evidence.evidence_id}` بجنس `{evidence.genus.value}`، "
            f"وهو لا يُثبِت وقوعًا؛ و{A_DECLARED_WORLD_IS_NOT_A_WITNESSED_ONE}"
        ),
    )


def suspended_propositions(
    cards: tuple[KnowledgeCard, ...] = THE_CARDS,
    cases: tuple[UsageCase, ...] = THE_CASES,
) -> tuple[SuspendedProposition, ...]:
    """القضايا التي يَمنع حارسُ المنشأ إيداعَها، مُسمّاةً بأسبابها.

    المدخل: بطاقاتٌ وحالات.
    الشرط: لا قراءةَ قرصٍ ههنا؛ الجنسُ وحدَه هو الحاكم.
    المخرج: صفٌّ مرتَّبٌ بمُعرِّف كلِّ قضيّةٍ معلَّقةٍ وجنسِ دليلها وسببِها.
    حدُّها: التعليقُ حكمٌ على **منشأ الدليل** لا على صدق المضمون.
    """

    out: list[SuspendedProposition] = []
    for card in cards:
        evidence = _interpretation_evidence(card)
        if evidence.establishes_facts:
            continue
        out.append(
            _suspension_of(_interpretation_proposition(card, evidence), evidence)
        )
    for case in cases:
        for fact in case.facts:
            evidence = _case_evidence(case, fact)
            if evidence.establishes_facts:
                continue
            out.append(_suspension_of(_case_proposition(case, fact), evidence))
    return tuple(out)


def base_stock(
    cards: tuple[KnowledgeCard, ...] = THE_CARDS,
    cases: tuple[UsageCase, ...] = THE_CASES,
    root: Path | None = None,
) -> KnowledgeStock:
    """الرصيدُ بعد إدخال البطاقات المُعادِ إنتاجُها واعتماد القاعدة ووقائع الحالات.

    المدخل: بطاقاتٌ وحالاتٌ وجذرُ شجرةٍ اختياريّ.
    الشرط: كلُّ بطاقةٍ تُدخَل **بعد** إعادة إنتاجها من بايتات مصدرها؛ وما لم
        يُعَد إنتاجُه لا يُدخَل البتّة.
    المخرج: رصيدٌ فيه قضايا النصّ والتفسير وتراخيصُها، والقاعدةُ واعتمادُها،
        ووقائعُ الحالات.
    حدُّها: الإدخالُ يُثبِت وقوعَ النصّ ونسبةَ التفسير إلينا، لا صدقَ المضمون.
    """

    stock = KnowledgeStock(
        stock_id="رصيد-مسار-البطاقة-المصدرية",
        version=0,
        register=FactRegister(register_id="سجلّ-مسار-البطاقة-المصدرية"),
        identity=IdentityNetwork(network_id="شبكة-مسار-البطاقة-المصدرية"),
    )
    order = 0
    for reading in read_cards(cards, root):
        if not reading.is_reproduced:
            raise SourceCardError(
                f"بطاقةٌ لم تُعَد من بايتات مصدرها لا تُدخَل: "
                f"`{reading.card.versioned_id}` — "
                f"{reading.refusal}"
            )
        card = reading.card
        slice_evidence = _slice_evidence(card)
        reading_evidence = _interpretation_evidence(card)
        stock = stock.with_evidence(slice_evidence).with_evidence(reading_evidence)
        stock = replace(
            stock,
            register=stock.register.with_individual(
                Individual(
                    individual_id=f"موضع-{card.card_id}",
                    designation_method=DesignationMethod.DEFINITE_DESCRIPTION,
                    candidate_type_ids=("موضعٌ-في-نصٍّ-مختوم",),
                    existence=ExistenceStanding.ESTABLISHED,
                    evidence_ref=slice_evidence.ref,
                )
            ),
        )
        for proposition, evidence in (
            (_slice_proposition(card, slice_evidence), slice_evidence),
            (_interpretation_proposition(card, reading_evidence), reading_evidence),
        ):
            if not evidence.establishes_facts:
                continue
            stock = stock.admit(
                proposition,
                AdmissionLicence(
                    proposition_id=proposition.proposition_id,
                    scope=proposition.scope,
                    evidence_ref=proposition.evidence_ref,
                    recorded_order=order,
                ),
            )
            order += 1
    rule = the_rule()
    stock = stock.with_evidence(_rule_source_evidence())
    stock = stock.adopt_rule(rule, _adoption_licence(rule), _adoption_evidence(rule))
    for case in cases:
        for fact in case.facts:
            stock = stock.with_evidence(_case_evidence(case, fact))
        stock = replace(
            stock,
            register=stock.register.with_individual(
                Individual(
                    individual_id=case.individual_id,
                    designation_method=DesignationMethod.DEFINITE_DESCRIPTION,
                    candidate_type_ids=("استعمالُ-لفظٍ-في-جملة",),
                    existence=(
                        ExistenceStanding.ASSUMED_FOR_THE_DISCOURSE
                        if case.is_a_declared_world
                        else ExistenceStanding.ESTABLISHED
                    ),
                    evidence_ref=_case_evidence(case, case.facts[0]).ref,
                )
            ),
        )
        for fact in case.facts:
            proposition = _case_proposition(case, fact)
            if fact.is_declared_only:
                continue
            stock = stock.admit(
                proposition,
                AdmissionLicence(
                    proposition_id=proposition.proposition_id,
                    scope=proposition.scope,
                    evidence_ref=proposition.evidence_ref,
                    recorded_order=order,
                ),
            )
            order += 1
    return stock


def _adoption_licence(rule: InferenceRule) -> AdoptionLicence:
    return AdoptionLicence(
        rule_versioned_id=rule.versioned_id,
        origin=RuleOrigin.TRANSMITTED_FROM_A_SOURCE,
        condition_note=(
            "تُطبَّق على استعمالٍ أُودِعت مقدّماتُه الأربعُ بأدلّتها؛ وتُراجَع "
            "بإعادة فحص بطاقتَيها عند كلّ تصحيحِ تفسير"
        ),
        evidence_ref=_adoption_evidence(rule).ref,
    )


# --- التطبيقُ وشهادتُه -------------------------------------------------------


class ApplicationVerdict(Enum):
    """حالُ التطبيق على حالةٍ بعينها؛ ثلاثةٌ لا رابعَ لها."""

    FIRED = "انطلقت القاعدةُ وأُودِع حكمُها"
    SUSPENDED_FOR_A_MISSING_PREMISE = "عُلِّق الحكمُ لمقدّمةٍ ناقصةٍ مُسمّاة"
    BLOCKED_BY_A_NAMED_BLOCKER = "مُنِع التطبيقُ بمانعٍ مُسمًّى"


@dataclass(frozen=True, slots=True)
class ApplicationCertificate:
    """شهادةُ تطبيقٍ قابلةٌ للفحص: ما استُعمِل، وما فُحِص، وما بقي."""

    case_id: str
    rule_versioned_id: str
    verdict: ApplicationVerdict
    premise_rows: tuple[tuple[str, str, str], ...]
    bindings: tuple[tuple[str, str, str], ...]
    conditions_checked: tuple[tuple[str, str], ...]
    blockers_examined: tuple[tuple[str, str], ...]
    conclusion_proposition_id: str | None
    missing_premises: tuple[str, ...]
    alternatives: tuple[str, ...]
    residues: tuple[str, ...]
    stock_version: int

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الشهادة للبصمة والعرض."""

        return {
            "case_id": self.case_id,
            "rule": self.rule_versioned_id,
            "verdict": self.verdict.value,
            "premises": [list(row) for row in self.premise_rows],
            "bindings": [list(row) for row in self.bindings],
            "conditions": [list(row) for row in self.conditions_checked],
            "blockers": [list(row) for row in self.blockers_examined],
            "conclusion": self.conclusion_proposition_id,
            "missing": list(self.missing_premises),
            "alternatives": list(self.alternatives),
            "residues": list(self.residues),
            "stock_version": self.stock_version,
        }


THE_CARD_PREMISE_IDS: Final[tuple[str, ...]] = (
    "قضية-نص-بطاقة-الأصل-الحقيقة",
    "قضية-نص-بطاقة-الدوران-والترجيح",
)
"""مقدّماتُ النصّ: مقطعان مُعادا الإنتاج من ج٣، لا تلخيصٌ لهما."""

THE_INTERPRETATION_PREMISE_CARD: Final[str] = "بطاقة-تعريف-الحقيقة"
"""البطاقةُ التي يُستعمَل **تفسيرُها** مقدّمةً؛ فتصحيحُه يُعيد تقييمَ التابع."""


def _live_interpretation_premise(stock: KnowledgeStock) -> str | None:
    """آخرُ قضيّةِ تفسيرٍ حيّةٍ لبطاقة التعريف، أيًّا كان إصدارُها."""

    prefix = f"قضية-تفسير-{THE_INTERPRETATION_PREMISE_CARD}@"
    live = [
        item.proposition_id
        for item in stock.register.active_propositions
        if item.proposition_id.startswith(prefix)
    ]
    return live[-1] if live else None


def claim_of_case(case: UsageCase) -> ClaimKey:
    """مفتاحُ دعوى الترجيح لهذه الحالة؛ تُقرَأ منزلتُه من أسانيده الحيّة."""

    return ClaimKey(
        subject_id=case.individual_id,
        predicate_id="الراجحُ-في-هذا-الاستعمال",
        value="الحقيقة",
        polarity=Polarity.AFFIRMED,
        scope=THE_USAGE_SCOPE,
    )


def apply_to_case(
    stock: KnowledgeStock,
    case: UsageCase,
    version: str = "1",
    attempt: int = 1,
) -> tuple[KnowledgeStock, ApplicationCertificate]:
    """طبِّق القاعدةَ المعتمدةَ على حالةٍ، وأخرِج شهادةً تُفحَص لا تُصدَّق.

    المدخل: رصيدٌ، وحالةٌ أُودِعت وقائعُها، وإصدارُ القاعدة، ورقمُ المحاولة.
    الشرط: الاعتمادُ حيٌّ، وكلُّ مقدّمةٍ مُودَعةٌ غيرُ معلَّقة.
    المخرج: رصيدٌ بعد التطبيق، وشهادةٌ تحمل المقدّماتِ والربائطَ والموانعَ
        المفحوصةَ والنتيجةَ والبدائلَ والبقايا.
    حدُّها: لا تُثبِت صدقَ القضيّة في الواقع؛ تُرجِّح **قراءةَ** الاستعمال.
    """

    rule_id = f"{THE_RULE_ID}@{version}"
    adoption = stock.adoption_of(rule_id)
    if not adoption.is_live:
        raise SourceCardError(
            f"لا يُطبَّق بترخيصٍ غيرِ حيّ: `{rule_id}`؛ والنتيجةُ المبنيّةُ "
            "على اعتمادٍ منقوضٍ لا تُقبَل ولا تُستأنَف بإعادة الاستدعاء."
        )
    premise_rows: list[tuple[str, str, str]] = []
    bindings: list[tuple[str, str, str]] = []
    conditions: list[tuple[str, str]] = []
    missing: list[str] = []
    premise_ids: list[str] = []

    interpretation_id = _live_interpretation_premise(stock)
    for proposition_id in (*THE_CARD_PREMISE_IDS, interpretation_id):
        if proposition_id is None:
            missing.append(f"تفسيرٌ حيٌّ للبطاقة `{THE_INTERPRETATION_PREMISE_CARD}`")
            continue
        try:
            item = stock.register.proposition_of(proposition_id)
        except Exception:  # noqa: BLE001 — غيابُ المقدّمة يُسمّى ولا يُرفَع
            missing.append(f"مقدّمةٌ نصّيّةٌ غائبة: `{proposition_id}`")
            continue
        if item.suspended:
            missing.append(f"مقدّمةٌ نصّيّةٌ معلَّقة: `{proposition_id}`")
            continue
        premise_ids.append(proposition_id)
        premise_rows.append(
            (proposition_id, item.evidence_ref.evidence_id, item.value or "")
        )

    blockers: list[tuple[str, str]] = []
    blocked: str | None = None
    alternatives: list[str] = []
    for kind in THE_PREMISE_ORDER:
        fact = case.fact_of(kind)
        if fact is None:
            missing.append(f"واقعةٌ غيرُ مُودَعةٍ عن الحالة: `{kind.value}`")
            conditions.append((kind.value, "مجهولةٌ: لم تُودَع بدليل"))
            continue
        proposition_id = f"قضية-{case.case_id}-{kind.name}"
        try:
            item = stock.register.proposition_of(proposition_id)
        except Exception:  # noqa: BLE001
            missing.append(f"واقعةٌ غيرُ مُودَعةٍ في السجلّ: `{proposition_id}`")
            conditions.append((kind.value, "مجهولةٌ: غائبةٌ عن السجلّ"))
            continue
        if item.suspended:
            missing.append(f"واقعةٌ معلَّقةٌ عن الحالة: `{proposition_id}`")
            conditions.append((kind.value, "معلَّقةٌ: سقط دليلُها"))
            continue
        premise_ids.append(proposition_id)
        premise_rows.append(
            (proposition_id, item.evidence_ref.evidence_id, item.value or "")
        )
        bindings.append((kind.value, item.value or "", item.evidence_ref.evidence_id))
        affirmed = item.polarity is Polarity.AFFIRMED
        conditions.append((kind.value, "مثبتةٌ بدليل" if affirmed else "منفيّةٌ بدليل"))
        if kind is PremiseKind.DIVERTING_INDICATION and affirmed:
            blocked = THE_BLOCKERS[0]
            alternatives.append(
                "الحملُ على المجاز بشرط علاقةٍ من أنواع العرب " "(`بطاقة-شرط-العلاقة`)"
            )
        if kind is PremiseKind.ADMITS_MAJAZ_BY_ITSELF and not affirmed:
            blocked = THE_BLOCKERS[1]
            alternatives.append(
                "لا دورانَ بالذات؛ ويبقى المجازُ بالتبع مسألةً أخرى "
                "(`بطاقة-ما-لا-يدخله-المجاز`)"
            )
        blockers.append(
            (
                kind.value,
                f"فُحِص على القضيّة `{proposition_id}` بدليل "
                f"`{item.evidence_ref.evidence_id}`",
            )
        )

    residues = [
        A_USAGE_TYPE_IS_NOT_A_TRUTH_VALUE,
        A_SEAL_IS_FOR_BYTES_NOT_FOR_A_READING,
        THE_UNCONNECTED_GAP,
    ]
    if missing:
        return stock, ApplicationCertificate(
            case_id=case.case_id,
            rule_versioned_id=rule_id,
            verdict=ApplicationVerdict.SUSPENDED_FOR_A_MISSING_PREMISE,
            premise_rows=tuple(premise_rows),
            bindings=tuple(bindings),
            conditions_checked=tuple(conditions),
            blockers_examined=tuple(blockers),
            conclusion_proposition_id=None,
            missing_premises=tuple(missing),
            alternatives=tuple(alternatives),
            residues=tuple(residues),
            stock_version=stock.version,
        )

    conclusion_id = f"حكم-{case.case_id}-{version}-{attempt}"
    conclusion = Proposition(
        proposition_id=conclusion_id,
        form=PropositionForm.ATTRIBUTE_VALUE,
        subject_id=case.individual_id,
        predicate_id="الراجحُ-في-هذا-الاستعمال",
        value="الحقيقة",
        polarity=Polarity.AFFIRMED,
        scope=THE_USAGE_SCOPE,
        evidence_ref=stock.register.proposition_of(premise_ids[0]).evidence_ref,
        derived_from_proposition_ids=tuple(premise_ids),
        derived_by_rule=rule_id,
    )
    licence = AdmissionLicence(
        proposition_id=conclusion_id,
        scope=THE_USAGE_SCOPE,
        evidence_ref=conclusion.evidence_ref,
        recorded_order=stock.version + 1_000,
        depends_on_proposition_ids=tuple(premise_ids),
    )
    updated, blocker = stock.apply_adopted_rule(
        rule_id,
        tuple(premise_ids),
        conclusion,
        licence,
        active_blocker_ids=() if blocked is None else (blocked,),
    )
    if blocker is not None:
        return updated, ApplicationCertificate(
            case_id=case.case_id,
            rule_versioned_id=rule_id,
            verdict=ApplicationVerdict.BLOCKED_BY_A_NAMED_BLOCKER,
            premise_rows=tuple(premise_rows),
            bindings=tuple(bindings),
            conditions_checked=tuple(conditions),
            blockers_examined=(*blockers, ("المانعُ القائم", blocker)),
            conclusion_proposition_id=None,
            missing_premises=(),
            alternatives=tuple(alternatives),
            residues=tuple(residues),
            stock_version=updated.version,
        )
    return updated, ApplicationCertificate(
        case_id=case.case_id,
        rule_versioned_id=rule_id,
        verdict=ApplicationVerdict.FIRED,
        premise_rows=tuple(premise_rows),
        bindings=tuple(bindings),
        conditions_checked=tuple(conditions),
        blockers_examined=tuple(blockers),
        conclusion_proposition_id=conclusion_id,
        missing_premises=(),
        alternatives=("الحملُ على المجاز مرجوحٌ ههنا، ويصير إليه من أقام قرينةً صارفة",),
        residues=tuple(residues),
        stock_version=updated.version,
    )


# --- المتحقِّقُ من الشهادة ----------------------------------------------------


@dataclass(frozen=True, slots=True)
class VerificationReading:
    """قراءةُ تحقُّقٍ: ما فُحِص آليًّا، وما خُرِق، وما بقي لمراجعةٍ بشريّة."""

    certificate: ApplicationCertificate
    machine_checked: tuple[str, ...]
    breaches: tuple[str, ...]
    left_to_human_review: tuple[str, ...]

    @property
    def holds(self) -> bool:
        """أصمدت الشهادةُ لفحص مضمونها؟ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return not self.breaches


def verify_certificate(
    stock: KnowledgeStock, certificate: ApplicationCertificate
) -> VerificationReading:
    """افحص مضمونَ الانتقال في نطاقه؛ ولا يكفي وجودُ الشهادة ولا حالُ `PASS`.

    المدخل: رصيدٌ الآن، وشهادةُ تطبيقٍ أُخرِجت قبلُ.
    الشرط: لا شرط؛ وكلُّ خرقٍ يُسمّى ولا يُرفَع استثناءً.
    المخرج: قراءةٌ تحمل ما فُحِص آليًّا وما خُرِق وما بقي بشريًّا.
    حدُّها: لا تفحص **صحّةَ التفسير** ولا مطابقةَ الحكم للواقع؛ وذانِك
        مُصرَّحٌ بهما في `left_to_human_review`.
    """

    checked: list[str] = []
    breaches: list[str] = []

    try:
        adoption = stock.adoption_of(certificate.rule_versioned_id)
        checked.append(f"حضورُ اعتمادٍ لـ`{certificate.rule_versioned_id}`")
        if not adoption.is_live:
            breaches.append(f"اعتمادٌ غيرُ حيٍّ للقاعدة `{certificate.rule_versioned_id}`")
        else:
            checked.append("حياةُ الاعتماد عند الفحص")
    except Exception:  # noqa: BLE001
        breaches.append(f"لا اعتمادَ في الرصيد لـ`{certificate.rule_versioned_id}`")

    for proposition_id, evidence_id, value in certificate.premise_rows:
        try:
            item = stock.register.proposition_of(proposition_id)
        except Exception:  # noqa: BLE001
            breaches.append(f"مقدّمةٌ في الشهادة غائبةٌ عن السجلّ: `{proposition_id}`")
            continue
        if item.suspended:
            breaches.append(f"مقدّمةٌ معلَّقةٌ تُحتَجّ بها الشهادة: `{proposition_id}`")
        if item.evidence_ref.evidence_id != evidence_id:
            breaches.append(f"دليلُ المقدّمة `{proposition_id}` تبدّل عمّا في الشهادة")
        elif (item.value or "") != value:
            breaches.append(f"مضمونُ المقدّمة `{proposition_id}` تبدّل عمّا في الشهادة")
        else:
            try:
                evidence = stock.register.evidence_of(evidence_id)
            except Exception:  # noqa: BLE001
                breaches.append(f"دليلٌ مذكورٌ في الشهادة غائبٌ عن السجلّ: `{evidence_id}`")
                continue
            if evidence.content_id != item.evidence_ref.content_id:
                breaches.append(
                    f"بصمةُ مضمون الدليل `{evidence_id}` تغيّرت بعد إخراج الشهادة"
                )
            else:
                checked.append(f"قيامُ المقدّمة `{proposition_id}` بمضمونها وبصمتها")

    for predicate, value, evidence_id in certificate.bindings:
        matched = any(
            item.predicate_id == predicate
            and (item.value or "") == value
            and item.evidence_ref.evidence_id == evidence_id
            and not item.suspended
            for item in stock.register.propositions
        )
        if matched:
            checked.append(f"مطابقةُ الرباط `{predicate}` لما في السجلّ")
        else:
            breaches.append(f"رباطٌ في الشهادة لا يُطابِق السجلَّ: `{predicate}`")

    if certificate.verdict is ApplicationVerdict.FIRED:
        conclusion_id = certificate.conclusion_proposition_id
        if conclusion_id is None:
            breaches.append("شهادةُ انطلاقٍ بلا مُعرِّفِ نتيجة")
        else:
            try:
                conclusion = stock.register.proposition_of(conclusion_id)
            except Exception:  # noqa: BLE001
                breaches.append(f"نتيجةٌ مذكورةٌ غائبةٌ عن السجلّ: `{conclusion_id}`")
            else:
                if conclusion.suspended:
                    breaches.append(f"نتيجةُ الشهادة معلَّقة: `{conclusion_id}`")
                elif conclusion.derived_by_rule != certificate.rule_versioned_id:
                    breaches.append("النتيجةُ منسوبةٌ إلى إصدارٍ غير المذكور في الشهادة")
                elif tuple(conclusion.derived_from_proposition_ids) != tuple(
                    row[0] for row in certificate.premise_rows
                ):
                    breaches.append("مقدّماتُ النتيجة ليست مقدّماتِ الشهادة بأعيانها")
                else:
                    checked.append(f"اتّصالُ النتيجة `{conclusion_id}` بمقدّماتها")
    elif certificate.verdict is ApplicationVerdict.SUSPENDED_FOR_A_MISSING_PREMISE:
        if not certificate.missing_premises:
            breaches.append("تعليقٌ بلا تسميةِ الناقص")
        else:
            checked.append("تسميةُ المقدّمة الناقصة في الشهادة")
    else:
        named = [
            row for row in certificate.blockers_examined if row[0] == "المانعُ القائم"
        ]
        if not named:
            breaches.append("منعٌ بلا تسميةِ المانع")
        else:
            checked.append(f"تسميةُ المانع القائم: {named[0][1]}")

    return VerificationReading(
        certificate=certificate,
        machine_checked=tuple(checked),
        breaches=tuple(breaches),
        left_to_human_review=(
            "صحّةُ تفسير البطاقة ومطابقتُه لمراد المؤلِّف — مراجعةٌ بشريّة",
            "صوابُ قراءةِ قرينةِ الصرف في جملة الحالة — مراجعةٌ بشريّة",
            "مطابقةُ القضيّة للواقع الخارجيّ — خارج نطاق هذا المسار",
        ),
    )


# --- التصحيحُ: إصدارٌ جديدٌ يحفظ القديم --------------------------------------


def corrected_card(card: KnowledgeCard, interpretation: str) -> KnowledgeCard:
    """بطاقةٌ بإصدارٍ لاحقٍ وتفسيرٍ مصحَّح؛ والقديمةُ تبقى بنصّها في الشجرة."""

    return replace(
        card,
        version=card.version + 1,
        interpretation=interpretation,
        review=ReviewStanding.REVIEWED_BY_HAND,
    )


def correct_interpretation(
    stock: KnowledgeStock,
    card: KnowledgeCard,
    interpretation: str,
    reason: str,
    recorded_order: int,
) -> tuple[KnowledgeStock, KnowledgeCard]:
    """صحِّح تفسيرَ بطاقةٍ: يُعلَّق القديمُ ويبقى، ويُودَع الجديدُ بترخيصه.

    المدخل: رصيدٌ، وبطاقةٌ مُودَعةٌ، وتفسيرٌ بديل، وسببٌ، ورتبةُ تسجيل.
    الشرط: قضيّةُ التفسير القديمة قائمةٌ غيرُ معلَّقة، والرتبةُ لاحقةٌ لرتبتها.
    المخرج: رصيدٌ فيه القديمُ معلَّقًا بتاريخه والجديدُ مُودَعًا، والبطاقةُ
        الجديدةُ بإصدارها.
    حدُّها: التصحيحُ واقعٌ على **تفسيرٍ صغناه نحن**، لا على نصّ الكتاب؛ والنصُّ
        لا يُمَسّ لأنّه شريحةٌ مختومة.
    """

    replacement_card = corrected_card(card, interpretation)
    evidence = _interpretation_evidence(replacement_card)
    replacement = _interpretation_proposition(replacement_card, evidence)
    correction = Correction(
        correction_id=f"تصحيح-{replacement_card.versioned_id}",
        corrected_proposition_id=f"قضية-تفسير-{card.versioned_id}",
        replacement_proposition_id=replacement.proposition_id,
        scope=THE_READING_SCOPE,
        recorded_order=recorded_order,
        reason=reason,
        evidence_ref=evidence.ref,
    )
    updated = stock.with_evidence(evidence).correct(
        correction,
        replacement,
        AdmissionLicence(
            proposition_id=replacement.proposition_id,
            scope=THE_READING_SCOPE,
            evidence_ref=replacement.evidence_ref,
            recorded_order=recorded_order,
        ),
    )
    return updated, replacement_card


# --- تجربةُ المراجعة المتصلة -------------------------------------------------


@dataclass(frozen=True, slots=True)
class ExperimentStep:
    """خطوةُ تجربةٍ: توقُّعٌ مُعلَنٌ قبل التشغيل، ثمّ ما لوحِظ فعلًا."""

    key: str
    title: str
    expectation: str
    observations: tuple[str, ...]
    stock_content_id: str

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الخطوة للعرض والبصمة."""

        return {
            "key": self.key,
            "title": self.title,
            "expectation": self.expectation,
            "observations": list(self.observations),
            "stock_content_id": self.stock_content_id,
        }


@dataclass(frozen=True, slots=True)
class ExperimentTrace:
    """أثرُ التجربة كلِّها: خطواتٌ مرتّبةٌ، وجدولُ أحكامٍ موصولٍ بنصوصه."""

    steps: tuple[ExperimentStep, ...]
    judgement_rows: tuple[tuple[str, str, str, str], ...]

    def step(self, key: str) -> ExperimentStep:
        """خطوةٌ بمفتاحها، أو رفضٌ باسمه."""

        for item in self.steps:
            if item.key == key:
                return item
        raise SourceCardError(f"لا خطوةَ بهذا المفتاح في الأثر: `{key}`")


THE_ALTERNATIVE_SUPPORT_ID: Final[str] = "قضية-سند-بديل-أسد-في-الغابة"
"""سندٌ مستقلٌّ للدعوى نفسِها: مراجعةٌ ثانيةٌ مُعلَنةٌ لا تمرّ ببطاقات ج٣."""


def _alternative_support(case: UsageCase) -> tuple[Evidence, Proposition]:
    evidence = _evidence(
        f"دليل-سند-بديل-{case.case_id}",
        EvidenceGenus.DECLARED_SCENARIO,
        (
            f"مراجعةٌ ثانيةٌ مُعلَنةٌ قرأت «{case.phrase}» فرجّحت الحقيقةَ فيها "
            "دون المرور ببطاقتَي ج٣؛ فأصلُ هذا السند غيرُ أصل الاشتقاق. و"
            + A_USAGE_TYPE_IS_NOT_A_TRUTH_VALUE
        ),
        "مراجعةُ قارئٍ ثانٍ في هذا المستودع",
        THE_USAGE_SCOPE,
    )
    proposition = Proposition(
        proposition_id=f"قضية-سند-بديل-{case.case_id}",
        form=PropositionForm.ATTRIBUTE_VALUE,
        subject_id=case.individual_id,
        predicate_id="الراجحُ-في-هذا-الاستعمال",
        value="الحقيقة",
        polarity=Polarity.AFFIRMED,
        scope=THE_USAGE_SCOPE,
        evidence_ref=evidence.ref,
    )
    return evidence, proposition


def _amended(evidence: Evidence, addition: str) -> Evidence:
    return replace(evidence, statement=evidence.statement + addition)


def _verdict_line(stock: KnowledgeStock, case: UsageCase) -> str:
    reading = stock.verdict_for(claim_of_case(case))
    return (
        f"{case.case_id}: {reading.standing.value} — أسانيدُ "
        f"{len(reading.supporting_proposition_ids)} في "
        f"{reading.independent_support_count} طائفةً مستقلّة"
    )


def run_experiment(root: Path | None = None) -> ExperimentTrace:
    """شغِّل الحالات السبعَ المُعلَنةَ على رصيدٍ واحدٍ متصل، وأخرِج أثرَها.

    المدخل: جذرُ شجرةٍ اختياريّ.
    الشرط: البطاقاتُ مُعادةُ الإنتاج من بايتات مصدرَيها المختومَين.
    المخرج: أثرٌ فيه لكلّ خطوةٍ توقُّعُها المُعلَنُ وما لوحِظ وبصمةُ الرصيد.
    حدُّها: الأثرُ حكمٌ عن **هذا الرصيد** بمُعرِّفاته، لا عن العالم؛ وتغيُّرُ
        بصمة الرصيد لا يُقرَأ تغيُّرًا في كلّ حكم.
    """

    steps: list[ExperimentStep] = []
    stock = base_stock(root=root)
    sound = THE_CASES[0]
    blocked_case = THE_CASES[1]
    incomplete = THE_CASES[3]

    after_sound, sound_certificate = apply_to_case(stock, sound)
    sound_reading = verify_certificate(after_sound, sound_certificate)
    steps.append(
        ExperimentStep(
            key="أ",
            title="تطبيقٌ مستوفٍ يُخرِج حكمًا بسلسلة مصادره",
            expectation=(
                "تنطلق القاعدةُ على «رأيت أسداً في الغابة» لأنّ مقدّماتِها "
                "الأربعَ مُودَعةٌ وقرينةُ الصرف **منفيّةٌ بدليل**، ويصمد "
                "التحقُّقُ من شهادتها"
            ),
            observations=(
                f"الحكم: {sound_certificate.verdict.value}",
                f"النتيجة: `{sound_certificate.conclusion_proposition_id}`",
                f"المقدّمات: {len(sound_certificate.premise_rows)}",
                f"التحقُّق: {'صمد' if sound_reading.holds else 'خُرِق'}",
                _verdict_line(after_sound, sound),
            ),
            stock_content_id=after_sound.content_id[:16],
        )
    )

    after_blocked, blocked_certificate = apply_to_case(after_sound, blocked_case)
    steps.append(
        ExperimentStep(
            key="أ-٢",
            title="حالةٌ ثانيةٌ في النطاق نفسِه يمنعها مانعٌ مُسمًّى",
            expectation=(
                "تُمنَع «رأيت أسداً يخطب على المنبر» بمانع القرينة الصارفة، "
                "ويُسمّى البديلُ: الحملُ على المجاز بشرط العلاقة"
            ),
            observations=(
                f"الحكم: {blocked_certificate.verdict.value}",
                f"المانع: {blocked_certificate.blockers_examined[-1][1]}",
                f"البدائل: {' · '.join(blocked_certificate.alternatives)}",
            ),
            stock_content_id=after_blocked.content_id[:16],
        )
    )

    _, incomplete_certificate = apply_to_case(after_blocked, incomplete)
    steps.append(
        ExperimentStep(
            key="ب",
            title="تطبيقٌ ناقصُ المقدّمة يُعلِّق الحكمَ ويُسمّي الناقص",
            expectation=(
                "تُعلَّق «نظرت إلى العين» لأنّ دورانَ الاستعمال وقرينةَ الصرف "
                "لم تُودَعا؛ ولا يُفترَض عدمُهما"
            ),
            observations=(
                f"الحكم: {incomplete_certificate.verdict.value}",
                *(
                    f"الناقص: {name}"
                    for name in incomplete_certificate.missing_premises
                ),
            ),
            stock_content_id=after_blocked.content_id[:16],
        )
    )

    alt_evidence, alt_proposition = _alternative_support(sound)
    with_alternative = after_blocked.with_evidence(alt_evidence).admit(
        alt_proposition,
        AdmissionLicence(
            proposition_id=alt_proposition.proposition_id,
            scope=THE_USAGE_SCOPE,
            evidence_ref=alt_proposition.evidence_ref,
            recorded_order=5_000,
        ),
    )
    before_withdrawal = with_alternative.verdict_for(claim_of_case(sound))
    withdrawn = with_alternative.retract_evidence("دليل-نص-بطاقة-الأصل-الحقيقة")
    after_withdrawal = withdrawn.verdict_for(claim_of_case(sound))
    withdrawn_reading = verify_certificate(withdrawn, sound_certificate)
    steps.append(
        ExperimentStep(
            key="ج",
            title="سحبُ شاهدٍ لازمٍ يُوقِف ما اعتمد عليه وحدَه",
            expectation=(
                "سحبُ دليل مقطع «والأصل في الكلام هو الحقيقة» يُعلِّق النتيجةَ "
                "المشتقّةَ به، فتُخرَق شهادتُها باسم المقدّمة المعلَّقة"
            ),
            observations=(
                f"قبل السحب: {before_withdrawal.standing.value} — "
                f"{len(before_withdrawal.supporting_proposition_ids)} سندًا",
                f"بعد السحب: {after_withdrawal.standing.value} — "
                f"{len(after_withdrawal.supporting_proposition_ids)} سندًا",
                f"التحقُّق من الشهادة القديمة: "
                f"{'صمد' if withdrawn_reading.holds else 'خُرِق'}",
                *(f"الخرق: {breach}" for breach in withdrawn_reading.breaches),
            ),
            stock_content_id=withdrawn.content_id[:16],
        )
    )

    steps.append(
        ExperimentStep(
            key="د",
            title="سندٌ بديلٌ صالحٌ يُبقي الحكمَ مدعومًا وتُحدَّث شهادتُه",
            expectation=(
                "الدعوى نفسُها مُودَعةٌ بسندٍ مستقلِّ الأصل، فتبقى مدعومةً بعد "
                "السحب، ويصير سندُها المُسمّى هو البديلَ لا المشتقَّ"
            ),
            observations=(
                "السندُ الباقي: "
                + " · ".join(after_withdrawal.supporting_proposition_ids),
                f"طوائفُ الاستقلال: {after_withdrawal.independent_support_count}",
                f"الحكمُ بعد السحب: {after_withdrawal.standing.value}",
                "الشهادةُ المحدَّثة: القبولُ قائمٌ على السند البديل، "
                "والشهادةُ المشتقّةُ مخروقةٌ باسمها",
            ),
            stock_content_id=withdrawn.content_id[:16],
        )
    )

    definition_card = card_of("بطاقة-تعريف-الحقيقة")
    corrected, new_card = correct_interpretation(
        with_alternative,
        definition_card,
        interpretation=(
            "الحقيقةُ **نوعُ استعمالٍ دلاليّ**: اللفظُ المستعمَلُ فيما وُضِع "
            "له أوّلًا؛ وليست رتبةَ صدقٍ، كما أنّ المجاز ليس رتبةَ كذب"
        ),
        reason=(
            "تفسيرٌ صغناه نحن في الإصدار الأوّل جعل «حقيقة/مجاز» رتبتَي صدقٍ "
            "وكذب، وهو خطأٌ منّا لا في نصّ الكتاب؛ والنصُّ شريحةٌ لم تُمَسّ"
        ),
        recorded_order=6_000,
    )
    old_interpretation = corrected.register.proposition_of(
        f"قضية-تفسير-{definition_card.versioned_id}"
    )
    conclusion_after_correction = corrected.register.proposition_of(
        sound_certificate.conclusion_proposition_id or ""
    )
    untouched = corrected.register.proposition_of("قضية-نص-بطاقة-الدوران-والترجيح")
    reapplied, second_certificate = apply_to_case(corrected, sound, attempt=2)
    second_reading = verify_certificate(reapplied, second_certificate)
    steps.append(
        ExperimentStep(
            key="هـ",
            title="تصحيحُ تفسيرِ بطاقةٍ يُنشئ إصدارًا ويحفظ القديم ويُعيد التقييم",
            expectation=(
                "يُعلَّق تفسيرُ الإصدار الأوّل ويبقى في السجلّ، وتُعلَّق "
                "النتيجةُ المشتقّةُ به وحدَها، ثمّ يُعاد الاشتقاقُ بترخيصٍ "
                "جديدٍ على الإصدار الثاني"
            ),
            observations=(
                f"البطاقةُ الجديدة: `{new_card.versioned_id}`",
                f"التفسيرُ القديمُ محفوظٌ معلَّق: {old_interpretation.suspended}",
                f"النتيجةُ القديمةُ معلَّقة: {conclusion_after_correction.suspended}",
                f"مقطعُ `بطاقة-الدوران-والترجيح` لم يُمَسّ: {not untouched.suspended}",
                f"إعادةُ الاشتقاق: {second_certificate.verdict.value} — "
                f"`{second_certificate.conclusion_proposition_id}`",
                f"التحقُّقُ من الشهادة الجديدة: "
                f"{'صمد' if second_reading.holds else 'خُرِق'}",
            ),
            stock_content_id=reapplied.content_id[:16],
        )
    )

    unrelated = reapplied.register.evidence_of("دليل-نص-بطاقة-الربط-لا-الاسترجاع")
    amended = replace(
        reapplied,
        register=reapplied.register.amend_evidence(
            _amended(unrelated, " — زيادةُ تعليقٍ تحريريٍّ لا تمسّ مقطعًا مستعمَلًا")
        ),
    )
    amended_reading = verify_certificate(amended, second_certificate)
    steps.append(
        ExperimentStep(
            key="و",
            title="تعديلُ دليلٍ غيرِ متعلِّقٍ يُزحزح البصمةَ ولا يُغيِّر حكمًا",
            expectation=(
                "تتغيّر بصمةُ الرصيد لأنّ حدثًا أُضيف، وتبقى شهادةُ الحالة "
                "صامدةً وأحكامُ الحالات كما هي"
            ),
            observations=(
                f"بصمةُ الرصيد قبل: {reapplied.content_id[:16]}",
                f"بصمةُ الرصيد بعد: {amended.content_id[:16]}",
                f"التحقُّق من شهادة الحالة: "
                f"{'صمد' if amended_reading.holds else 'خُرِق'}",
                _verdict_line(amended, sound),
                _verdict_line(amended, blocked_case),
            ),
            stock_content_id=amended.content_id[:16],
        )
    )

    stale_id = f"دليل-{sound.case_id}-{PremiseKind.DIVERTING_INDICATION.name}"
    stale_source = amended.register.evidence_of(stale_id)
    stale = replace(
        amended,
        register=amended.register.amend_evidence(
            _amended(
                stale_source,
                " — مراجعةٌ لاحقةٌ بدّلت جوابَها: صارت القرينةُ عندها محتمَلةً " "لا منفيّة",
            )
        ),
    )
    stale_reading = verify_certificate(stale, second_certificate)
    _, fresh_certificate = apply_to_case(stale, sound, attempt=3)
    steps.append(
        ExperimentStep(
            key="ز",
            title="تقريرُ قبولٍ قديمٌ مع جوابٍ متغيِّرٍ يُرفَض",
            expectation=(
                "تبدُّلُ مضمون تقرير القرينة يُغيِّر بصمتَه فتُعلَّق قضيّتُه "
                "وتوابعُها، وتُرفَض الشهادةُ القديمةُ باسم ما تبدّل؛ ولا يُقبَل "
                "حكمٌ بشهادةٍ تُحيل على بصمةٍ زائلة"
            ),
            observations=(
                f"التحقُّق من الشهادة القديمة: "
                f"{'صمد' if stale_reading.holds else 'خُرِق'}",
                *(f"الخرق: {breach}" for breach in stale_reading.breaches),
                f"إعادةُ التطبيق بعد التبدُّل: {fresh_certificate.verdict.value}",
                *(f"الناقص: {name}" for name in fresh_certificate.missing_premises),
            ),
            stock_content_id=stale.content_id[:16],
        )
    )

    rows: list[tuple[str, str, str, str]] = []
    for case in THE_CASES:
        _, certificate = apply_to_case(stock, case)
        texts = " ⟵ ".join(
            f"«{stock.register.proposition_of(row[0]).value}»"
            for row in certificate.premise_rows
            if row[0].startswith("قضية-نص-")
        )
        conditions = " · ".join(
            f"{name}: {standing}" for name, standing in certificate.conditions_checked
        )
        dependents = (
            certificate.conclusion_proposition_id
            or " · ".join(certificate.missing_premises)
            or "—"
        )
        rows.append((case.case_id, certificate.verdict.value, texts, conditions))
        rows.append((case.case_id, "التبعيّات", dependents, conditions))
    return ExperimentTrace(steps=tuple(steps), judgement_rows=tuple(rows))
